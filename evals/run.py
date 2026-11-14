#!/usr/bin/env python3
"""COPY eval runner: the skill vs. baseline Claude on the fixture corpus.

For each fixture x command x condition it runs Claude Code headless in a
scratch folder holding piece.md (and BRAND.md when the fixture has a brand),
then asks a judge model to grade the output against the fixture's
expectations. Deterministic checks (preserved phrases, similarity, new
numbers) run on rewrite commands.

Conditions:
  skill     claude -p with --plugin-dir <repo>, asked to use the copy skill
  baseline  claude -p with the Skill tool disabled, asked the same task in plain words

Usage (run through testmgr on Luis's machines; see docs/testing.md):
  python evals/run.py --fixtures f01,f04 --commands critique --workers 2
  python evals/run.py --dry-run
Standard library only.
"""

import argparse
import concurrent.futures as cf
import datetime as dt
import difflib
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "evals" / "fixtures"
BRANDS = ROOT / "evals" / "brands"
REWRITE_COMMANDS = {"polish", "humanize"}
MARK_OPEN, MARK_CLOSE = "<<<REVISED", "REVISED>>>"


# ---------------------------------------------------------------- fixtures

def load_fixture(path):
    raw = path.read_text(encoding="utf-8")
    head, text = raw.split("-->", 1)
    meta = json.loads(head.split("<!-- fixture", 1)[1])
    meta["text"] = text.strip() + "\n"
    return meta


def select_fixtures(spec):
    all_fx = sorted(FIXTURES.glob("*.md"))
    if not spec:
        return [load_fixture(p) for p in all_fx]
    wanted = [s.strip() for s in spec.split(",") if s.strip()]
    return [load_fixture(p) for p in all_fx if any(p.stem.startswith(w) for w in wanted)]


# ---------------------------------------------------------------- prompts

def task_prompt(fx, command, condition):
    brand = " and the brand profile in BRAND.md" if fx.get("brand") else ""
    rewrite = ""
    if command in REWRITE_COMMANDS:
        rewrite = (" Put the full revised text between a line containing only %s and a line containing only %s."
                   % (MARK_OPEN, MARK_CLOSE))
    common = (" Brief from the author: %s Work only from piece.md%s. Do not modify any files. "
              "Reply with your %s output only.%s" % (fx["brief"], brand, command, rewrite))
    if condition == "skill":
        return "Use the copy skill to run `%s` on piece.md.%s" % (command, common)
    plain = {
        "critique": "Critique the writing in piece.md.",
        "audit": "Audit piece.md for clichés, AI-sounding language, redundancy, and weak or unsupported claims.",
        "humanize": "Rewrite piece.md so it sounds less robotic and less AI-generated.",
        "polish": "Polish piece.md so it is ready to publish.",
        "voice check": "Check whether piece.md matches the brand voice described in BRAND.md.",
    }[command]
    return plain + common


JUDGE_TEMPLATE = """You are grading an editorial review produced by an AI system. Be strict and literal. Output JSON only.

## The piece that was reviewed
<piece>
{piece}
</piece>

## Author's brief
{brief}
{brand}
## The command that was run
{command}

## Expectations set by a senior editor
Acceptable verdicts: {verdicts} (Ship = publishable as is; Revise = needs targeted changes; Rethink = strategic or integrity problem).
Problems the review MUST identify (by substance, any wording):
{must_flag}
Things the review must NOT do (false positives / harmful advice):
{must_not_flag}

## The review to grade
<review>
{output}
</review>

## Grade it
Return exactly this JSON object:
{{
  "verdict": "Ship" | "Revise" | "Rethink" | "none",
  "verdict_match": true | false,
  "must_flag": {{ "<id>": true | false, ... one key per required problem ... }},
  "false_positives": ["<id from the must-not list that the review violated>", ...],
  "other_false_positives": ["<short description of any other finding a senior editor would call wrong or harmful for this context>", ...],
  "invented_facts": ["<any fact, number, name, quote, or claim the review introduces as true that is not in the piece, brief, or brand profile; placeholders like [NEEDS: ...] do not count>", ...],
  "usefulness": 0-4,
  "voice_preservation": 0-4 or null,
  "notes": "<one or two sentences>"
}}
Rules: "verdict" is the review's overall judgment mapped onto Ship/Revise/Rethink (use "none" if it gives no overall judgment). Usefulness: 0 harmful or misleading; 1 mostly generic or wrong priorities; 2 correct but obvious or unprioritized; 3 specific, prioritized, actionable; 4 what an excellent senior editor would say, including knowing what to leave alone. voice_preservation applies only when the review rewrites text (0 = author's voice gone, 4 = indistinguishable from the author's best draft); otherwise null.
"""


def judge_prompt(fx, command, output):
    def bullets(items):
        return "\n".join("- %s: %s" % (i["id"], i["desc"]) for i in items) or "- (none)"
    brand = ""
    if fx.get("brand"):
        brand = "\n## Brand profile in force\n<brand>\n%s\n</brand>\n" % (BRANDS / fx["brand"]).read_text(encoding="utf-8")
    return JUDGE_TEMPLATE.format(piece=fx["text"], brief=fx["brief"], brand=brand, command=command,
                                 verdicts=", ".join(fx["expect_verdict"]),
                                 must_flag=bullets(fx["must_flag"]), must_not_flag=bullets(fx["must_not_flag"]),
                                 output=output)


# ---------------------------------------------------------------- running claude

def claude_bin():
    found = shutil.which("claude") or shutil.which("claude.cmd")
    if not found:
        sys.exit("claude CLI not found on PATH")
    return found


def run_claude(prompt, cwd, extra, model=None, timeout=900):
    cmd = [claude_bin(), "-p", "--output-format", "json"] + extra
    if model:
        cmd += ["--model", model]
    p = subprocess.run(cmd, input=prompt.encode("utf-8"), cwd=str(cwd), capture_output=True, timeout=timeout)
    raw = p.stdout.decode("utf-8", errors="replace")
    try:
        data = json.loads(raw)
        return {"ok": not data.get("is_error", False), "text": data.get("result", ""),
                "cost_usd": data.get("total_cost_usd"), "turns": data.get("num_turns"),
                "stderr": p.stderr.decode("utf-8", errors="replace")[-2000:]}
    except json.JSONDecodeError:
        return {"ok": False, "text": raw, "cost_usd": None, "turns": None,
                "stderr": p.stderr.decode("utf-8", errors="replace")[-2000:]}


def condition_flags(condition):
    tools = ["--allowedTools", "Read", "Glob", "Grep", "Bash(python:*)", "Bash(python3:*)"]
    if condition == "skill":
        return ["--plugin-dir", str(ROOT)] + tools + ["Skill"]
    return tools + ["--disallowedTools", "Skill"]


# ---------------------------------------------------------------- deterministic checks

def norm(s):
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("—", "-").replace("–", "-")
    return re.sub(r"\s+", " ", s).strip().lower()


def extract_revised(text):
    m = re.search(re.escape(MARK_OPEN) + r"\s*\n(.*?)\n\s*" + re.escape(MARK_CLOSE), text, re.S)
    return m.group(1).strip() if m else None


NUM_RE = re.compile(r"\d[\d,.]*")


def new_numbers(revised, sources):
    have = set(NUM_RE.findall(" ".join(sources)))
    return sorted({n.rstrip(".,") for n in NUM_RE.findall(revised)} - {h.rstrip(".,") for h in have})


def deterministic(fx, command, output):
    if command not in REWRITE_COMMANDS:
        return {}
    revised = extract_revised(output)
    if revised is None:
        return {"revised_found": False}
    sources = [fx["text"], fx["brief"]]
    if fx.get("brand"):
        sources.append((BRANDS / fx["brand"]).read_text(encoding="utf-8"))
    kept = {p: norm(p) in norm(revised) for p in fx.get("preserve", [])}
    sim = difflib.SequenceMatcher(None, norm(fx["text"]), norm(revised)).ratio()
    floor = fx.get("polish_min_similarity")
    return {"revised_found": True, "similarity": round(sim, 3),
            "similarity_ok": (sim >= floor) if floor else None,
            "preserved": kept, "new_numbers": new_numbers(revised, sources)}


# ---------------------------------------------------------------- one job

def run_job(fx, command, condition, out_dir, args):
    slug = "%s__%s__%s" % (fx["id"], command.replace(" ", "-"), condition)
    work = out_dir / "work" / slug
    work.mkdir(parents=True, exist_ok=True)
    (work / "piece.md").write_text(fx["text"], encoding="utf-8")
    if fx.get("brand"):
        shutil.copy(BRANDS / fx["brand"], work / "BRAND.md")

    res = run_claude(task_prompt(fx, command, condition), work, condition_flags(condition), args.model)
    (out_dir / (slug + ".out.md")).write_text(res["text"], encoding="utf-8")
    record = {"fixture": fx["id"], "category": fx["category"], "command": command, "condition": condition,
              "ok": res["ok"], "cost_usd": res["cost_usd"], "turns": res["turns"],
              "checks": deterministic(fx, command, res["text"])}
    if not res["ok"]:
        record["error"] = res["stderr"] or res["text"][:500]
    if args.skip_judge or not res["ok"]:
        return record

    j = run_claude(judge_prompt(fx, command, res["text"]), work,
                   ["--disallowedTools", "Skill", "Bash", "Read", "Write", "Edit", "Glob", "Grep", "WebFetch", "WebSearch"],
                   args.judge_model)
    m = re.search(r"\{.*\}", j["text"], re.S)
    try:
        record["judge"] = json.loads(m.group(0)) if m else {"parse_error": j["text"][:500]}
    except json.JSONDecodeError:
        record["judge"] = {"parse_error": j["text"][:500]}
    record["judge_cost_usd"] = j["cost_usd"]
    return record


# ---------------------------------------------------------------- report

def summarize(records):
    by = {}
    for r in records:
        by.setdefault(r["condition"], []).append(r)
    lines = ["| Condition | Runs | Verdict match | Must-flag recall | False positives | Invented facts | Usefulness (0-4) | Voice kept (0-4) | Phrases preserved | Cost (USD) |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for cond, rs in sorted(by.items()):
        judged = [r for r in rs if isinstance(r.get("judge"), dict) and "parse_error" not in r["judge"]]
        vm = sum(1 for r in judged if r["judge"].get("verdict_match"))
        flags = [v for r in judged for v in r["judge"].get("must_flag", {}).values()]
        fp = sum(len(r["judge"].get("false_positives", [])) + len(r["judge"].get("other_false_positives", [])) for r in judged)
        inv = sum(len(r["judge"].get("invented_facts", [])) for r in judged)
        use = [r["judge"].get("usefulness") for r in judged if isinstance(r["judge"].get("usefulness"), (int, float))]
        voice = [r["judge"].get("voice_preservation") for r in judged if isinstance(r["judge"].get("voice_preservation"), (int, float))]
        kept = [v for r in rs for v in r.get("checks", {}).get("preserved", {}).values()]
        cost = sum((r.get("cost_usd") or 0) + (r.get("judge_cost_usd") or 0) for r in rs)
        pct = lambda a, b: "%d/%d" % (a, b) if b else "-"
        avg = lambda xs: "%.2f" % (sum(xs) / len(xs)) if xs else "-"
        lines.append("| %s | %d | %s | %s | %d | %d | %s | %s | %s | %.2f |" % (
            cond, len(rs), pct(vm, len(judged)), pct(sum(flags), len(flags)), fp, inv,
            avg(use), avg(voice), pct(sum(kept), len(kept)), cost))
    lines += ["", "| Fixture | Command | Condition | Verdict | Match | Recall | FP | Invented | Useful | Similarity | Notes |",
              "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in sorted(records, key=lambda r: (r["fixture"], r["command"], r["condition"])):
        j = r.get("judge") or {}
        mf = j.get("must_flag", {}) or {}
        lines.append("| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
            r["fixture"], r["command"], r["condition"], j.get("verdict", "-"), j.get("verdict_match", "-"),
            "%d/%d" % (sum(mf.values()), len(mf)) if mf else "-",
            len(j.get("false_positives", [])) + len(j.get("other_false_positives", [])) if j else "-",
            len(j.get("invented_facts", [])) if j else "-", j.get("usefulness", "-"),
            r.get("checks", {}).get("similarity", "-"),
            (r.get("error") or j.get("notes") or j.get("parse_error") or "").replace("|", "/").replace("\n", " ")[:160]))
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fixtures", default="", help="comma-separated id prefixes, e.g. f01,f04 (default: all)")
    ap.add_argument("--commands", default="", help="comma-separated commands to run (default: each fixture's own list)")
    ap.add_argument("--conditions", default="skill,baseline")
    ap.add_argument("--workers", type=int, default=int(os.environ.get("TESTMGR_WORKERS", "2")))
    ap.add_argument("--model", default=None, help="model for the reviewed runs (default: CLI default)")
    ap.add_argument("--judge-model", default=None, help="model for the judge (default: CLI default)")
    ap.add_argument("--out", default=None)
    ap.add_argument("--skip-judge", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    fixtures = select_fixtures(args.fixtures)
    only = {c.strip() for c in args.commands.split(",") if c.strip()}
    conditions = [c.strip() for c in args.conditions.split(",") if c.strip()]
    jobs = [(fx, cmd, cond) for fx in fixtures for cmd in fx["commands"] if not only or cmd in only for cond in conditions]

    if args.dry_run:
        for fx, cmd, cond in jobs:
            print("%-40s %-12s %-9s %s" % (fx["id"], cmd, cond, task_prompt(fx, cmd, cond)[:90]))
        print("%d jobs" % len(jobs))
        return 0

    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = pathlib.Path(args.out) if args.out else ROOT / "evals" / "results" / stamp
    out_dir.mkdir(parents=True, exist_ok=True)
    print("%d jobs, %d workers -> %s" % (len(jobs), args.workers, out_dir), flush=True)

    records = []
    with cf.ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        futs = {pool.submit(run_job, fx, cmd, cond, out_dir, args): (fx["id"], cmd, cond) for fx, cmd, cond in jobs}
        for fut in cf.as_completed(futs):
            key = futs[fut]
            try:
                rec = fut.result()
            except Exception as exc:  # keep the batch going
                rec = {"fixture": key[0], "command": key[1], "condition": key[2], "ok": False, "error": repr(exc)}
            records.append(rec)
            print("done %s %s %s ok=%s" % (key[0], key[1], key[2], rec.get("ok")), flush=True)

    (out_dir / "results.json").write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")
    (out_dir / "summary.md").write_text("# COPY eval run %s\n\n" % stamp + summarize(records), encoding="utf-8")
    print(summarize(records))
    return 0


if __name__ == "__main__":
    sys.exit(main())
