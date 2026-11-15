# hooks

Manage the copy hook for the current project: `/copy hooks on | off | status`.

When the plugin is installed, two hooks run the linter (`scripts/hook.py`) automatically:
- **After each Edit/Write** of a copy file, only the **immediate tier** is reported back: chatbot residue, brand-banned words, claim candidates, and vague attribution. These are unambiguous enough to interrupt for.
- **At the end of the turn** (Stop), a **deep pass** runs every pattern family over the copy files touched in the session and reports what is left, once. It is deduplicated against the per-edit reports and never repeats in a session.

Hook output is evidence, not instruction to rewrite. When it arrives, confirm each item against [tells.md](tells.md) and [claims.md](claims.md), fix only confirmed items under [restraint.md](restraint.md), and say briefly what you left alone. If the user told you to keep text verbatim, keep it and report instead.

## When it runs

Off by default in every project. It switches on when the project root has a `BRAND.md` or a `.copy/` folder, unless `.copy/config.json` says `"enabled": false`.

Files checked by default: `*.md *.mdx *.markdown *.txt *.html *.astro`. Always skipped: `node_modules`, `.git`, `.claude`, `.copy`, `dist`, `build`, `vendor`, `CLAUDE.md`, `AGENTS.md`, `CHANGELOG.md`, licence files, and this skill's own folder.

## Commands

- **`/copy hooks on`:** create `.copy/config.json` with `"hook": {"enabled": true}` (merge if it exists). Ask which folders hold copy when the project is mostly code, and set `include` to match (e.g. `["content/*", "src/pages/*.astro"]`). Offer to set a `default_context` profile.
- **`/copy hooks off`:** set `"enabled": false`. Don't delete the file.
- **`/copy hooks status`:** report enabled or not and why (config, BRAND.md, or `.copy/` folder), the include/exclude patterns, the profiles mapped, and whether the plugin's hooks are installed. Hooks only run from the plugin install. For a standalone skill install, see "Standalone installs" below.

## Configuration: `.copy/config.json`

```json
{
  "hook": {
    "enabled": true,
    "include": ["content/*", "*.md"],
    "exclude": ["docs/api/*"],
    "contexts": { "content/blog/*": "13", "src/pages/index.astro": "3" },
    "default_context": "3",
    "per_edit": "immediate"
  },
  "avoid": ["synergy"],
  "allow": ["robust"],
  "brand": "BRAND.md"
}
```

- `contexts` maps path patterns to profile numbers from [contexts.md](contexts.md). A file can also set its own with a line `copy-context: 12` in its first 15 lines.
- `per_edit: "all"` reports every family on every edit (noisier).
- `avoid` and `allow` add to the vocabulary read from BRAND.md's "Use / Instead of" table, "We never say" line, and signature phrases.
- Session state lives in `.copy/.state/` (git-ignored automatically).

## Standalone installs

Without the plugin, add the hooks to the project's `.claude/settings.json` yourself, pointing at the skill's script:

```json
{
  "hooks": {
    "PostToolUse": [{ "matcher": "Edit|Write|MultiEdit",
      "hooks": [{ "type": "command", "command": "python ~/.claude/skills/copy/scripts/hook.py post", "timeout": 5 }] }],
    "Stop": [{ "hooks": [{ "type": "command", "command": "python ~/.claude/skills/copy/scripts/hook.py stop", "timeout": 30 }] }]
  }
}
```
