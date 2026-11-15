# live

A local preview for one copy file: `/copy live [file]`. The page shows the file with every linter hit underlined and re-renders whenever the file is saved. Select any passage (or click an underline) to ask for a critique, alternatives, a quieter or sharper version, or a humanize pass. A chosen alternative can be applied straight back to the file.

## Start it

1. Resolve the file. If none is named, ask which; the page works on one file at a time.
2. Pick the context profile from [contexts.md](contexts.md) (the intent read's profile) and pass it as `--context`.
3. Start the server **in the background**, so the session stays free:
   ```bash
   python3 "<skill-dir>/scripts/live.py" <file> --context <profile>
   ```
   (`python` on Windows.) It opens the browser, binds to `127.0.0.1` only, and prints the URL with a per-run token. Give the user the printed URL.
   Options: `--brand <path>` (defaults to the nearest BRAND.md), `--port` (default 8377, tries the next 20), `--model <model>` for faster passage answers, `--no-open`.
4. Tell the user how to stop it (Ctrl+C, or stop the background task) and stop it yourself when the session's work on that file is done.

## What the page does

- **Linter view:** underlines colour-coded by family; a side panel with counts, document-level metrics (rhythm, formatting), and families suppressed for the profile. The profile can be changed in the header.
- **Ask about a passage:** runs `claude -p` with read-only tools against this skill's files (SKILL.md, restraint, rubric, claims) and the brand profile. It returns a keep or change verdict, a diagnosis, findings with severity, and labelled alternatives. Answers take about a minute.
- **Apply:** replaces the exact passage in the file, only when it appears exactly once. Otherwise it refuses and the user edits by hand.

## Limits

- Needs the `claude` CLI on PATH for passage questions; linting works without it.
- Each question is a separate Claude run and costs tokens.
- Shows the source text (Markdown symbols included), not a rendered page.
- Local files only. For a deployed page, fetch the text first and run `critique`.
