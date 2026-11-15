#!/usr/bin/env python3
"""COPY live: a local preview of one copy file with linter hits marked in place.

  python live.py path/to/page.md [--context 3] [--brand BRAND.md] [--port 8377] [--no-open]

Opens a page on 127.0.0.1 that:
  - shows the file with every linter hit underlined (re-renders when the file is saved);
  - lets you select a passage and ask Claude (via the `claude` CLI, using the copy
    skill's references) to critique it or suggest labelled alternatives;
  - applies a chosen alternative back to the file (exact, single-occurrence replace).

Binds to 127.0.0.1 only and requires a per-run token on every API call.
Standard library only. Stop with Ctrl+C.
"""

import argparse
import json
import os
import pathlib
import re
import secrets
import shutil
import subprocess
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tells  # noqa: E402

SKILL_DIR = pathlib.Path(__file__).resolve().parents[1]
PROFILES = [
    ("", "No profile"), ("1", "1 · Positioning & messaging"), ("2", "2 · Brand manifesto"),
    ("3", "3 · Website & landing page"), ("4", "4 · Advertising campaign"), ("5a", "5a · Headline"),
    ("5b", "5b · Tagline"), ("6", "6 · Corporate communications"), ("7", "7 · Investor communications"),
    ("8", "8 · Product marketing"), ("9", "9 · Social media"), ("10", "10 · Video & audio scripts"),
    ("11", "11 · Thought leadership"), ("12", "12 · Technical & explanatory"), ("13", "13 · Long-form editorial"),
]
ACTIONS = {
    "critique": "Diagnose this passage in the context of the whole piece, following reference/critique.md and the "
                "severity tests in reference/rubric.md. If it works, the verdict is \"keep\" and alternatives may be empty.",
    "alternatives": "Offer two or three labelled alternatives for this passage. Each fixes a named problem or explores a "
                    "clearly labelled direction. If the passage already works, say so and offer at most one option.",
    "quieter": "Tone down hype, overclaiming and pressure in this passage while keeping its energy and voice.",
    "sharpen": "Make this passage more specific, using only facts already in the piece, the brief, or BRAND.md; "
               "where proof is missing, use a [NEEDS: ...] placeholder instead of inventing it.",
    "humanize": "Remove confirmed template or machine-made patterns from this passage only (reference/tells.md "
                "calibration). Keep facts, claims and deliberate devices.",
}

ASK_TEMPLATE = """You are the COPY editorial skill. Before answering, read {skill}/SKILL.md, {skill}/reference/restraint.md and {skill}/reference/rubric.md (and {skill}/reference/claims.md if the passage makes claims). Follow their rules: evidence or silence, never invent facts, preserve the author's voice, leave good writing alone.

The full piece is in {file}.{brand}
Writing-context profile: {profile}.

Task: {task}

The passage (exact text from the file):
<passage>
{passage}
</passage>

Reply with ONLY one JSON object, no prose around it:
{{"verdict": "keep" | "change",
  "diagnosis": "one or two sentences",
  "findings": [{{"severity": "P0|P1|P2|P3", "problem": "...", "why": "..."}}],
  "alternatives": [{{"label": "short name", "text": "drop-in replacement for the whole passage", "why": "the named problem it fixes"}}]}}
Every alternative's "text" must be a complete replacement for the exact passage, in the author's voice."""


class State:
    def __init__(self, path, context, brand, model):
        self.path = path
        self.context = context
        self.brand = brand
        self.model = model
        self.token = secrets.token_urlsafe(18)
        self.lock = threading.Lock()

    def snapshot(self):
        text = self.path.read_text(encoding="utf-8", errors="replace")
        avoid = allow = None
        if self.brand and self.brand.is_file():
            avoid, allow = tells.brand_lists(self.brand.read_text(encoding="utf-8", errors="replace"))
        result = tells.run(text, context=self.context or None, avoid=avoid, allow=allow)
        return {
            "name": self.path.name, "path": str(self.path), "mtime": self.path.stat().st_mtime,
            "context": self.context or "", "profiles": PROFILES,
            "brand": str(self.brand) if self.brand and self.brand.is_file() else None,
            "text": text, "findings": result["findings"], "metrics": result["metrics"],
            "summary": result["summary"], "suppressed": result["suppressed"],
        }

    def ask(self, action, passage):
        claude = shutil.which("claude") or shutil.which("claude.cmd")
        if not claude:
            return {"error": "The claude CLI isn't on PATH, so passage questions are unavailable. Linting still works."}
        if action not in ACTIONS:
            return {"error": "unknown action"}
        profile = dict(PROFILES).get(self.context or "", "not set; infer it from the piece")
        brand = (" The brand profile is in %s; follow it." % self.brand) if self.brand and self.brand.is_file() else ""
        prompt = ASK_TEMPLATE.format(skill=SKILL_DIR.as_posix(), file=self.path.as_posix(), brand=brand,
                                     profile=profile, task=ACTIONS[action], passage=passage)
        cmd = [claude, "-p", "--output-format", "json", "--strict-mcp-config",
               "--add-dir", str(SKILL_DIR), "--allowedTools", "Read", "Glob", "Grep",
               "--disallowedTools", "Skill", "Bash", "Write", "Edit", "WebFetch", "WebSearch"]
        if self.model:
            cmd += ["--model", self.model]
        try:
            p = subprocess.run(cmd, input=prompt.encode("utf-8"), capture_output=True, timeout=300,
                               cwd=str(self.path.parent))
        except subprocess.TimeoutExpired:
            return {"error": "Claude took longer than 5 minutes; try a shorter passage."}
        raw = p.stdout.decode("utf-8", errors="replace")
        try:
            text = json.loads(raw).get("result", "")
        except ValueError:
            return {"error": "Unexpected output from claude: " + (raw or p.stderr.decode("utf-8", "replace"))[:300]}
        m = re.search(r"\{.*\}", text, re.S)
        try:
            return json.loads(m.group(0)) if m else {"error": "No JSON in reply", "raw": text[:2000]}
        except ValueError:
            return {"error": "Could not parse the reply", "raw": text[:2000]}

    def apply(self, old, new):
        with self.lock:
            text = self.path.read_text(encoding="utf-8", errors="replace")
            count = text.count(old)
            if count != 1:
                return 409, {"error": "The passage appears %d times in the file now; edit it by hand." % count}
            self.path.write_text(text.replace(old, new, 1), encoding="utf-8", newline="")
            return 200, {"ok": True}


def make_handler(state):
    page = PAGE.replace("__TOKEN__", state.token)

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def _authed(self):
            q = parse_qs(urlparse(self.path).query)
            return secrets.compare_digest(self.headers.get("X-Copy-Token", "") or (q.get("t") or [""])[0], state.token)

        def _send(self, code, body, ctype="application/json"):
            data = body.encode("utf-8") if isinstance(body, str) else json.dumps(body).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", ctype + "; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            route = urlparse(self.path).path
            if not self._authed():
                return self._send(403, {"error": "missing or wrong token"})
            if route == "/":
                return self._send(200, page, "text/html")
            if route == "/api/state":
                try:
                    return self._send(200, state.snapshot())
                except OSError as exc:
                    return self._send(500, {"error": str(exc)})
            return self._send(404, {"error": "not found"})

        def do_POST(self):
            route = urlparse(self.path).path
            if not self._authed():
                return self._send(403, {"error": "missing or wrong token"})
            try:
                n = int(self.headers.get("Content-Length", "0"))
                body = json.loads(self.rfile.read(n) or b"{}")
            except ValueError:
                return self._send(400, {"error": "bad json"})
            if route == "/api/context":
                ctx = str(body.get("context", ""))
                if ctx not in dict(PROFILES):
                    return self._send(400, {"error": "unknown profile"})
                state.context = ctx
                return self._send(200, {"ok": True})
            if route == "/api/ask":
                passage = str(body.get("passage", ""))[:4000]
                if not passage.strip():
                    return self._send(400, {"error": "empty passage"})
                return self._send(200, state.ask(str(body.get("action", "")), passage))
            if route == "/api/apply":
                code, out = state.apply(str(body.get("old", "")), str(body.get("new", "")))
                return self._send(code, out)
            return self._send(404, {"error": "not found"})

    return Handler


def find_brand(path, explicit):
    if explicit:
        return pathlib.Path(explicit).resolve()
    for folder in [pathlib.Path.cwd(), *path.parents]:
        for cand in (folder / "BRAND.md", folder / ".copy" / "BRAND.md"):
            if cand.is_file():
                return cand
    return None


def main(argv=None):
    ap = argparse.ArgumentParser(description="COPY live preview")
    ap.add_argument("path")
    ap.add_argument("--context", default="", help="profile number from reference/contexts.md")
    ap.add_argument("--brand", default="", help="BRAND.md path (default: nearest BRAND.md)")
    ap.add_argument("--port", type=int, default=8377)
    ap.add_argument("--model", default=None, help="model for passage questions (default: CLI default)")
    ap.add_argument("--no-open", action="store_true")
    args = ap.parse_args(argv)

    path = pathlib.Path(args.path).resolve()
    if not path.is_file():
        sys.stderr.write("copy-live: no such file: %s\n" % path)
        return 1
    state = State(path, args.context, find_brand(path, args.brand), args.model)
    server = None
    for port in range(args.port, args.port + 20):
        try:
            server = ThreadingHTTPServer(("127.0.0.1", port), make_handler(state))
            break
        except OSError:
            continue
    if server is None:
        sys.stderr.write("copy-live: no free port from %d\n" % args.port)
        return 1
    url = "http://127.0.0.1:%d/?t=%s" % (server.server_address[1], state.token)
    print("COPY live: %s" % path, flush=True)
    print("Open: %s" % url, flush=True)
    print("Ctrl+C to stop.", flush=True)
    if not args.no_open:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


PAGE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>COPY live</title>
<style>
:root{
  --bg:#f6f4ef; --paper:#fffdf8; --ink:#1d1b18; --muted:#6b665d; --line:#e2ddd2; --accent:#9a3412;
  --chip:#efebe2; --ok:#166534; --warn:#9a3412;
  --f-residue:#b91c1c; --f-claim:#c2410c; --f-attribution:#b45309; --f-brand:#7c2d12;
  --f-vocab:#7c3aed; --f-puffery:#a21caf; --f-reveal:#1d4ed8; --f-throat:#0e7490; --f-hedge:#4d7c0f;
  --f-significance:#be185d; --f-agency:#0f766e; --f-ending:#57534e; --f-other:#6b7280;
  --serif:"Iowan Old Style","Charter","Georgia",serif;
  --sans:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
  --mono:ui-monospace,"Cascadia Code",Consolas,monospace;
}
@media (prefers-color-scheme: dark){:root{
  --bg:#171614; --paper:#1f1d1a; --ink:#ece7dd; --muted:#a39d91; --line:#34312c; --accent:#fb923c; --chip:#2a2723;
  --ok:#4ade80; --warn:#fb923c;
  --f-residue:#f87171; --f-claim:#fb923c; --f-attribution:#fbbf24; --f-brand:#fdba74;
  --f-vocab:#a78bfa; --f-puffery:#e879f9; --f-reveal:#60a5fa; --f-throat:#22d3ee; --f-hedge:#a3e635;
  --f-significance:#f472b6; --f-agency:#2dd4bf; --f-ending:#a8a29e; --f-other:#9ca3af;
}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 var(--sans)}
header{position:sticky;top:0;z-index:5;display:flex;flex-wrap:wrap;gap:12px 20px;align-items:center;
  padding:12px 20px;background:var(--bg);border-bottom:1px solid var(--line)}
header h1{font:600 15px/1 var(--sans);margin:0;letter-spacing:.02em}
header h1 span{color:var(--accent)}
.file{font:13px var(--mono);color:var(--muted);overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:40ch}
select,button{font:inherit;font-size:13px;color:var(--ink);background:var(--paper);border:1px solid var(--line);
  border-radius:6px;padding:5px 9px;cursor:pointer}
button:hover{border-color:var(--muted)} button:disabled{opacity:.5;cursor:wait}
button.primary{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.status{font-size:13px;color:var(--muted);margin-left:auto}
main{display:grid;grid-template-columns:minmax(0,1fr) 380px;gap:24px;max-width:1280px;margin:0 auto;padding:24px 20px 80px}
@media (max-width:900px){main{grid-template-columns:1fr}}
.doc{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:40px clamp(18px,5vw,56px);
  font:18px/1.7 var(--serif);white-space:pre-wrap;overflow-wrap:anywhere;min-height:60vh}
mark{background:none;color:inherit;border-bottom:2px solid var(--c,var(--f-other));cursor:pointer;padding-bottom:1px}
mark:hover,mark.on{background:color-mix(in srgb,var(--c) 16%,transparent)}
aside{display:flex;flex-direction:column;gap:16px;align-self:start;position:sticky;top:72px;max-height:calc(100vh - 90px);overflow:auto}
@media (max-width:900px){aside{position:static;max-height:none}}
.card{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:14px 16px}
.card h2{font:600 12px/1 var(--sans);text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin:0 0 10px}
.fam{display:flex;align-items:center;gap:8px;font-size:13px;padding:3px 0}
.dot{width:9px;height:9px;border-radius:50%;background:var(--c);flex:none}
.fam b{margin-left:auto;font-weight:600}
.note{font-size:13px;color:var(--muted);margin:6px 0 0}
.passage{font:15px/1.5 var(--serif);background:var(--chip);border-radius:6px;padding:8px 10px;margin:0 0 10px;
  max-height:9em;overflow:auto;white-space:pre-wrap}
.actions{display:flex;flex-wrap:wrap;gap:6px}
.result p{margin:8px 0;font-size:14px}
.verdict{display:inline-block;font:600 12px/1 var(--sans);padding:4px 8px;border-radius:99px;background:var(--chip)}
.verdict.keep{color:var(--ok)} .verdict.change{color:var(--warn)}
.finding{font-size:13px;border-left:3px solid var(--line);padding:2px 0 2px 10px;margin:8px 0}
.alt{border:1px solid var(--line);border-radius:8px;padding:10px 12px;margin:10px 0}
.alt h3{font:600 13px/1.3 var(--sans);margin:0 0 6px}
.alt .t{font:15px/1.5 var(--serif);white-space:pre-wrap;margin:0 0 6px}
.alt .why{font-size:12.5px;color:var(--muted);margin:0 0 8px}
.empty{font-size:13px;color:var(--muted);margin:0}
.err{color:var(--warn);font-size:13px}
.spin{display:inline-block;width:12px;height:12px;border:2px solid var(--line);border-top-color:var(--ink);border-radius:50%;
  animation:s 0.8s linear infinite;vertical-align:-2px;margin-right:6px}
@keyframes s{to{transform:rotate(360deg)}}
@media (prefers-reduced-motion: reduce){.spin{animation:none}}
</style>
</head>
<body>
<header>
  <h1>COPY <span>live</span></h1>
  <div class="file" id="file"></div>
  <label>Profile <select id="ctx"></select></label>
  <div class="status" id="status">Loading…</div>
</header>
<main>
  <article class="doc" id="doc" aria-label="Document"></article>
  <aside>
    <section class="card" id="sel">
      <h2>Selection</h2>
      <p class="empty">Select any passage, or click an underlined phrase, to ask about it.</p>
    </section>
    <section class="card" id="res" hidden><h2>Editor's notes</h2><div class="result" id="resbody"></div></section>
    <section class="card"><h2>Linter</h2><div id="lint"></div>
      <p class="note">Evidence, not verdict. An underline marks a candidate; some are deliberate and fine.</p></section>
  </aside>
</main>
<script>
const T="__TOKEN__";
const FAM={residue:"--f-residue",claim:"--f-claim",attribution:"--f-attribution","brand-avoid":"--f-brand",vocab:"--f-vocab",
  puffery:"--f-puffery",reveal:"--f-reveal",throat:"--f-throat",hedge:"--f-hedge",significance:"--f-significance",
  agency:"--f-agency",ending:"--f-ending"};
const LABEL={residue:"Chatbot residue",claim:"Claims to check",attribution:"Vague attribution","brand-avoid":"Brand: don't say",
  vocab:"Stock vocabulary",puffery:"Puffery",reveal:"Reveal constructions",throat:"Throat-clearing",hedge:"Hedges",
  significance:"Inflated significance",agency:"Abstractions as actors",ending:"Generic endings",rhythm:"Rhythm",
  format:"Formatting",triplet:"Triplets"};
let S=null, lastM=0, passage="";
const $=id=>document.getElementById(id);
const esc=s=>s.replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const api=(p,b)=>fetch(p,{method:b?"POST":"GET",headers:{"X-Copy-Token":T,"Content-Type":"application/json"},
  body:b?JSON.stringify(b):undefined}).then(async r=>({ok:r.ok,data:await r.json()}));

function render(){
  $("file").textContent=S.path; $("file").title=S.path;
  const sel=$("ctx");
  if(!sel.options.length) S.profiles.forEach(([v,l])=>sel.add(new Option(l,v)));
  sel.value=S.context;
  const spans=S.findings.filter(f=>f.start!=null).sort((a,b)=>a.start-b.start);
  let out="",pos=0,i=0;
  for(const f of spans){ if(f.start<pos) continue;
    out+=esc(S.text.slice(pos,f.start));
    out+=`<mark data-i="${i}" style="--c:var(${FAM[f.family]||"--f-other"})" title="${esc(f.family+": "+f.note)}">${esc(S.text.slice(f.start,f.end))}</mark>`;
    pos=f.end; i++; }
  out+=esc(S.text.slice(pos));
  const y=window.scrollY; $("doc").innerHTML=out; window.scrollTo(0,y);
  $("doc").querySelectorAll("mark").forEach((m,k)=>m.onclick=e=>{e.stopPropagation();pickSentence(spans[k]);});
  const fams=Object.entries(S.summary).sort((a,b)=>b[1]-a[1]);
  const doclevel=S.findings.filter(f=>f.start==null);
  let h=fams.length?fams.map(([f,n])=>`<div class="fam"><span class="dot" style="--c:var(${FAM[f]||"--f-other"})"></span>${esc(LABEL[f]||f)}<b>${n}</b></div>`).join("")
    :`<p class="empty">No candidate patterns.</p>`;
  doclevel.forEach(f=>h+=`<p class="note"><b>${esc(LABEL[f.family]||f.family)}:</b> ${esc(f.note)}. ${esc(f.excerpt)}</p>`);
  const sup=Object.entries(S.suppressed||{});
  if(sup.length) h+=`<p class="note">Usually deliberate in this profile, not shown: ${sup.map(([f,n])=>esc(f)+" "+n).join(", ")}.</p>`;
  if(S.brand) h+=`<p class="note">Brand profile: ${esc(S.brand)}</p>`;
  $("lint").innerHTML=h;
  $("status").textContent=`${S.metrics.words} words · ${spans.length} marked · updated ${new Date(S.mtime*1000).toLocaleTimeString()}`;
}

function pickSentence(f){
  const t=S.text; let a=f.start,b=f.end;
  while(a>0 && !/[.!?\n]/.test(t[a-1])) a--;
  while(b<t.length && !/[.!?\n]/.test(t[b])) b++;
  if(b<t.length && t[b]!=="\n") b++;
  setPassage(t.slice(a,b).trim(), `${LABEL[f.family]||f.family}: “${f.match}” (${f.note})`);
}

function setPassage(p,why){
  passage=p;
  $("sel").innerHTML=`<h2>Selection</h2><div class="passage">${esc(p)}</div>${why?`<p class="note">${esc(why)}</p>`:""}
  <div class="actions">${["critique","alternatives","quieter","sharpen","humanize"].map(a=>`<button data-a="${a}"${a==="critique"?' class="primary"':""}>${a[0].toUpperCase()+a.slice(1)}</button>`).join("")}</div>`;
  $("sel").querySelectorAll("button").forEach(b=>b.onclick=()=>ask(b.dataset.a));
}

async function ask(action){
  const btns=$("sel").querySelectorAll("button"); btns.forEach(b=>b.disabled=true);
  $("res").hidden=false; $("resbody").innerHTML=`<p><span class="spin"></span>Asking Claude (${esc(action)})… this can take a minute.</p>`;
  const asked=passage;
  try{
    const {data}=await api("/api/ask",{action,passage:asked});
    if(data.error){ $("resbody").innerHTML=`<p class="err">${esc(data.error)}</p>${data.raw?`<pre class="note">${esc(data.raw)}</pre>`:""}`; return; }
    let h=`<span class="verdict ${data.verdict==="keep"?"keep":"change"}">${data.verdict==="keep"?"Keep as is":"Change suggested"}</span>`;
    if(data.diagnosis) h+=`<p>${esc(data.diagnosis)}</p>`;
    (data.findings||[]).forEach(f=>h+=`<div class="finding"><b>${esc(f.severity||"")}</b> ${esc(f.problem||"")}<br><span class="note">${esc(f.why||"")}</span></div>`);
    (data.alternatives||[]).forEach((a,k)=>h+=`<div class="alt"><h3>${esc(a.label||"Option "+(k+1))}</h3><p class="t">${esc(a.text||"")}</p>
      <p class="why">${esc(a.why||"")}</p><div class="actions"><button data-k="${k}" class="primary">Apply to file</button><button data-c="${k}">Copy</button></div></div>`);
    $("resbody").innerHTML=h;
    $("resbody").querySelectorAll("[data-k]").forEach(b=>b.onclick=async()=>{
      const alt=data.alternatives[b.dataset.k]; const r=await api("/api/apply",{old:asked,new:alt.text});
      b.textContent=r.ok?"Applied":"Not applied"; if(!r.ok) b.insertAdjacentHTML("afterend",`<p class="err">${esc(r.data.error)}</p>`);
      if(r.ok){ lastM=0; refresh(); }});
    $("resbody").querySelectorAll("[data-c]").forEach(b=>b.onclick=()=>{navigator.clipboard.writeText(data.alternatives[b.dataset.c].text);b.textContent="Copied";});
  }catch(e){ $("resbody").innerHTML=`<p class="err">${esc(String(e))}</p>`; }
  finally{ btns.forEach(b=>b.disabled=false); }
}

document.addEventListener("mouseup",e=>{
  if(!$("doc").contains(e.target)) return;
  const s=window.getSelection().toString(); if(s.trim().length>2) setPassage(s.trim());
});
$("ctx").onchange=async()=>{ await api("/api/context",{context:$("ctx").value}); lastM=0; refresh(); };

async function refresh(){
  try{ const {ok,data}=await api("/api/state"); if(!ok){ $("status").textContent=data.error; return; }
    if(data.mtime!==lastM || data.context!==(S&&S.context)){ S=data; lastM=data.mtime; render(); } }
  catch(e){ $("status").textContent="Server stopped"; }
}
refresh(); setInterval(refresh,1500);
</script>
</body>
</html>
"""

if __name__ == "__main__":
    sys.exit(main())
