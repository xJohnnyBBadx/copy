#!/usr/bin/env python3
"""COPY hook: lint copy files as an agent edits them.

Wired by the plugin's hooks/hooks.json:
  PostToolUse (Edit|Write|MultiEdit)  ->  hook.py post
  Stop                                ->  hook.py stop

Per edit, it reports only the immediate tier: unambiguous problems worth
interrupting for (chatbot residue, brand-banned words, claim candidates,
vague attribution). At the end of the turn, a deep pass runs every family
over the files touched in the session and reports what is left, once.

Off unless the project opts in: a BRAND.md at the project root, a .copy/
folder, or .copy/config.json with "hook": {"enabled": true}. Manage it with
`/copy hooks on|off|status` (reference/hooks.md).

Standard library only. Never fails the agent's turn: any error exits 0 silently.
"""

import fnmatch
import hashlib
import json
import os
import pathlib
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tells  # noqa: E402

IMMEDIATE = {"residue", "brand-avoid", "claim", "attribution"}
DEFAULT_INCLUDE = ["*.md", "*.mdx", "*.markdown", "*.txt", "*.html", "*.astro"]
DEFAULT_EXCLUDE = [
    "node_modules/*", ".git/*", ".claude/*", ".copy/*", "dist/*", "build/*", "vendor/*",
    "CLAUDE.md", "AGENTS.md", "CHANGELOG.md", "LICENSE*", "NOTICE*",
    "*/skills/copy/*", "skills/copy/*", "evals/*",
]
MAX_ITEMS = 12


def load_config(root):
    cfg_path = root / ".copy" / "config.json"
    cfg = {}
    if cfg_path.is_file():
        try:
            cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            cfg = {}
    hook = cfg.get("hook", {}) if isinstance(cfg.get("hook", {}), dict) else {}
    if "enabled" in hook:
        enabled = bool(hook["enabled"])
    else:
        enabled = (root / "BRAND.md").is_file() or (root / ".copy").is_dir()
    return {
        "enabled": enabled,
        "include": hook.get("include") or DEFAULT_INCLUDE,
        "exclude": DEFAULT_EXCLUDE + list(hook.get("exclude") or []),
        "contexts": hook.get("contexts") or {},
        "default_context": hook.get("default_context"),
        "per_edit": hook.get("per_edit", "immediate"),
        "avoid": list(cfg.get("avoid") or []),
        "allow": list(cfg.get("allow") or []),
        "brand": cfg.get("brand"),
    }


def glob_match(rel, pattern):
    pats = [pattern] + ([pattern[3:]] if pattern.startswith("**/") else [])
    name = rel.rsplit("/", 1)[-1]
    return any(fnmatch.fnmatch(rel, p) or ("/" not in p and fnmatch.fnmatch(name, p)) for p in pats)


def relpath(root, path):
    try:
        return pathlib.Path(path).resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return None


def wanted(cfg, rel):
    if rel is None:
        return False
    if any(glob_match(rel, p) for p in cfg["exclude"]):
        return False
    return any(glob_match(rel, p) for p in cfg["include"])


def context_for(cfg, rel, text):
    for pattern, ctx in cfg["contexts"].items():
        if glob_match(rel, pattern):
            return str(ctx)
    for line in text.splitlines()[:15]:
        if line.lower().startswith("copy-context:"):
            return line.split(":", 1)[1].strip()
    return cfg["default_context"]


def brand_lists(root, cfg):
    avoid, allow = list(cfg["avoid"]), list(cfg["allow"])
    brand = root / (cfg["brand"] or "BRAND.md")
    if brand.is_file():
        a, b = tells.brand_lists(brand.read_text(encoding="utf-8", errors="replace"))
        avoid += a
        allow += b
    return avoid, allow


def state_file(root, session):
    digest = hashlib.sha1((session or "none").encode("utf-8")).hexdigest()[:16]
    return root / ".copy" / ".state" / (digest + ".json")


def load_state(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"touched": [], "reported": [], "deep_done": False}


def save_state(path, state):
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        gi = path.parent.parent / ".gitignore"
        if not gi.exists():
            gi.write_text(".state/\n", encoding="utf-8")
        path.write_text(json.dumps(state), encoding="utf-8")
    except OSError:
        pass


def key(rel, f):
    return "%s|%s|%s|%s" % (rel, f["family"], (f["match"] or f["note"]).lower(), f["excerpt"][:40] if not f["match"] else "")


def lint_file(root, cfg, rel):
    path = root / rel
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None, []
    avoid, allow = brand_lists(root, cfg)
    ctx = context_for(cfg, rel, text)
    result = tells.run(text, context=ctx, avoid=avoid or None, allow=allow or None)
    return ctx, result["findings"]


def fmt(rel, ctx, items):
    out = ["%s (context %s):" % (rel, ctx or "unset")]
    for f in items[:MAX_ITEMS]:
        loc = "L%d" % f["line"] if f["line"] else "doc"
        what = '"%s"' % f["match"] if f["match"] else f["excerpt"]
        out.append("  - [%s] %s %s (%s)" % (f["family"], loc, what, f["note"]))
    if len(items) > MAX_ITEMS:
        out.append("  - ... and %d more" % (len(items) - MAX_ITEMS))
    return "\n".join(out)


HEADER = ("COPY linter: evidence, not verdict. Confirm each item against the copy skill's "
          "reference/tells.md and claims.md calibration before changing anything; leave deliberate "
          "devices, brand vocabulary and substantiated claims alone. Never invent proof; use [NEEDS: ...].")


def on_post(payload, root, cfg):
    tool_input = payload.get("tool_input") or {}
    path = tool_input.get("file_path") or tool_input.get("path")
    if not path:
        return None
    rel = relpath(root, path)
    if not wanted(cfg, rel):
        return None
    sf = state_file(root, payload.get("session_id"))
    state = load_state(sf)
    if rel not in state["touched"]:
        state["touched"].append(rel)
    state["deep_done"] = False
    ctx, findings = lint_file(root, cfg, rel)
    if cfg["per_edit"] != "all":
        findings = [f for f in findings if f["family"] in IMMEDIATE]
    new = [f for f in findings if key(rel, f) not in state["reported"]]
    state["reported"].extend(key(rel, f) for f in new)
    save_state(sf, state)
    if not new:
        return None
    return {"hookSpecificOutput": {"hookEventName": "PostToolUse",
                                   "additionalContext": HEADER + "\n" + fmt(rel, ctx, new)}}


def on_stop(payload, root, cfg):
    if payload.get("stop_hook_active"):
        return None
    sf = state_file(root, payload.get("session_id"))
    state = load_state(sf)
    if state.get("deep_done") or not state["touched"]:
        return None
    blocks = []
    for rel in state["touched"]:
        ctx, findings = lint_file(root, cfg, rel)
        new = [f for f in findings if key(rel, f) not in state["reported"]]
        if new:
            state["reported"].extend(key(rel, f) for f in new)
            blocks.append(fmt(rel, ctx, new))
    state["deep_done"] = True
    save_state(sf, state)
    if not blocks:
        return None
    reason = (HEADER + " End-of-turn deep pass over the copy files you edited. Fix only the confirmed "
              "items, briefly say which you left alone and why, then stop.\n" + "\n".join(blocks))
    return {"decision": "block", "reason": reason}


def main():
    event = sys.argv[1] if len(sys.argv) > 1 else "post"
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except ValueError:
        return 0
    root = pathlib.Path(payload.get("cwd") or os.getcwd())
    cfg = load_config(root)
    if not cfg["enabled"]:
        return 0
    out = on_stop(payload, root, cfg) if event == "stop" else on_post(payload, root, cfg)
    if out:
        sys.stdout.write(json.dumps(out))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:  # a hook must never break the agent's turn
        sys.exit(0)
