# COPY

Editorial judgment for AI agents.

COPY is a skill that gives Claude Code, and any agent that reads the open [Agent Skills](https://agentskills.io) format, the working judgment of a senior editor and creative director. It is not a copy generator. It reads for intent, diagnoses before rewriting, checks claims, preserves the author's voice, and says so when writing already works.

It does for copy what [Impeccable](https://impeccable.style) does for interface design.

```
/copy critique homepage.md
/copy audit launch-email.md
/copy humanize blog-intro.md
/copy polish press-release.md
/copy voice create
```

## Why another writing skill

Most copywriting skills teach a model how to write more. A model's default failure isn't writing too little. It is confident, generic over-editing: deleting every adverb and em dash, flattening a distinctive voice into category language, adding calls to action to a manifesto, and rewriting good copy because it was asked to look at it.

COPY is built around the opposite instincts:

- **Intent before evaluation.** A manifesto, a white paper, a landing page, and an investor letter are held to different standards. Thirteen writing-context profiles set which dimensions matter for each.
- **Strategy before sentences.** A wrong promise or a misleading claim is reported before any sentence-level note, because polishing a broken argument hides it.
- **Evidence or silence.** Every finding quotes the text. COPY never invents statistics, testimonials, research, or results; where proof is missing it writes `[NEEDS: …]`.
- **Restraint.** A dedicated restraint file is read before any rewrite. "This works; change nothing" is a valid result.
- **Calibrated pattern detection.** The AI-tell catalogue says when each pattern is a problem *and when it isn't*. A deterministic linter supplies evidence; judgment decides.

## Commands

| Command | What it does |
|---|---|
| `critique` | Full editorial and strategic evaluation. Intent read, nine dimensions scored 0–4 with behavioural anchors and weighted by context, prioritized findings, verdict: **Ship / Revise / Rethink**. |
| `audit` | Fast scan for AI-sounding patterns, clichés, redundancy, and weak or unsupported claims. Linter plus judgment; no scores. |
| `humanize` | Audit limited to robotic patterns, then applies only confirmed fixes. Refuses when the tells are covering for a missing idea. |
| `polish` | Publication-ready pass with a minimal diff and a change log. Flags facts and claims for the author instead of changing them. |
| `voice` | `voice create` builds a reusable `BRAND.md` profile from strategy, samples, and approved and rejected examples. `voice check` scores a piece against it. |
| `live` | Local preview page: linter hits underlined in place, ask Claude about any passage, apply an alternative back to the file. |
| `hooks` | Turn the automatic copy linter on or off for a project, or check its status. |

Every finding follows one shape: **Problem → Evidence → Why it matters → Intervention → Example.** Severity runs P0 (strategic or integrity) → P1 (structural) → P2 (sentence) → P3 (preference), with subjective options labelled as *Alternatives*, never as corrections.

Planned for v0.2, once the evals show the core judgment holds: `distill`, `sharpen`, `bolder`, `quieter`, `position`, `structure`. See [docs/architecture.md](docs/architecture.md#roadmap).

## Install

### Claude Code (plugin)

```
/plugin marketplace add xJohnnyBBadx/copy
/plugin install copy@copy
```

Plugin skills are namespaced, so the full form is `/copy:copy critique <target>`. Asking in plain words also works ("critique this landing page", "make this sound less AI").

### Claude Code (standalone skill)

Copy `skills/copy/` into your skills folder so that `SKILL.md` sits at `~/.claude/skills/copy/SKILL.md` (or `.claude/skills/copy/` inside a project). Then use `/copy critique <target>`.

```bash
git clone https://github.com/xJohnnyBBadx/copy.git
cp -r copy/skills/copy ~/.claude/skills/copy
```

### Other agents

`skills/copy/` is a standard Agent Skills folder: a `SKILL.md` with front matter, reference files loaded on demand, and one optional script. Agents that read SKILL.md folders (Codex, Cursor, OpenClaw, Hermes Agent and others) should be able to use it without changes; put it wherever that agent loads skills from. Only Claude Code has been tested so far. No MCP server or API key is required.

### Requirements

None for the skill itself. The linter, hooks, and live preview need Python 3.8+ and use only the standard library. Without Python, the commands fall back to a manual scan and say so, and the hooks stay silent. Asking about a passage in the live preview also needs the `claude` CLI on PATH.

## Run it locally

Three ways to use COPY on your own machine, the same way Impeccable does for design:

**1. The linter, by hand.** No AI, instant, Python standard library only:
```bash
python skills/copy/scripts/tells.py --context 3 --brand BRAND.md homepage.md
python skills/copy/scripts/tells.py --json --context 12 docs/setup.md
```
`--context` is a profile number from [contexts.md](skills/copy/reference/contexts.md) (3 landing page, 2 manifesto, 12 technical, 13 long-form…). Exit code 2 means candidates were found. Every hit is a candidate, not a verdict.

**2. Hooks, while Claude writes.** With the plugin installed, put a `BRAND.md` or an empty `.copy/` folder in a project (or run `/copy hooks on`). From then on, every time Claude edits a copy file, the linter runs and pushes unambiguous problems back to it straight away: chatbot residue, brand-banned words, claims to check, vague attribution. At the end of the turn, a deeper pass reports the remaining patterns once. Configuration: [reference/hooks.md](skills/copy/reference/hooks.md).

**3. Live preview.** `/copy live homepage.md`, or directly:
```bash
python skills/copy/scripts/live.py homepage.md --context 3
```
This opens a local page (127.0.0.1 only, with a per-run token) showing the file with every hit underlined, refreshed on each save. Select a passage, or click an underline, and ask for a critique, alternatives, a quieter or sharper version, or a humanize pass. Claude answers through the `claude` CLI using the skill's own rules, in about a minute. Apply a suggestion and it is written back to the file.

**4. Inside your own app.** `tells.py` imports cleanly (standard library only), so a tool can run the linter on its own content and draw the results however it likes:
```python
import importlib.util
spec = importlib.util.spec_from_file_location("tells", "skills/copy/scripts/tells.py")
tells = importlib.util.module_from_spec(spec); spec.loader.exec_module(tells)
avoid, allow = tells.brand_lists(open("BRAND.md", encoding="utf-8").read())
result = tells.run("Our seamless platform is revolutionary.", context="10", avoid=avoid, allow=allow)
for f in result["findings"]:          # family, match, note, start/end offsets into the text
    print(f["family"], f["match"], f["start"], f["end"])
```
For a model's judgment on one passage, send the same JSON contract `live.py` uses (`ASK_TEMPLATE`: verdict, diagnosis, findings, labelled alternatives) to `claude -p` with `--add-dir` pointing at the skill. A video studio's script editor uses exactly this: a dashboard of hits per scene, questions per line, and a chosen alternative written back to the script only on Apply.

## Brand profiles

Run `/copy voice create` with a few writing samples and some "sounds like us / doesn't" examples. COPY drafts a `BRAND.md` (schema: [skills/copy/templates/BRAND.md](skills/copy/templates/BRAND.md)) that turns adjectives into rules and **This, not that** pairs. Every command reads it.

- One brand per project: `BRAND.md` at the project root.
- Several clients in one workspace: `.copy/brands/<slug>.md`, selected by name ("critique this for acme").

An example profile lives at [evals/brands/dirt-road-coffee.md](evals/brands/dirt-road-coffee.md).

## How it's built

```
skills/copy/
├── SKILL.md                 philosophy, setup, intent read, routing, output contract, hard rules
├── reference/
│   ├── critique.md audit.md polish.md voice.md live.md hooks.md   one file per command, loaded on demand
│   ├── rubric.md            9 dimensions × 0–4 anchors, severity, verdict rules
│   ├── contexts.md          13 writing-context profiles: tiers, what good looks like, what not to flag
│   ├── restraint.md         what never to change; read before any rewrite
│   ├── claims.md            claim inventory, evidence ladder, misleading patterns
│   ├── tells.md             AI and template patterns, each with "flag when / don't flag when"
│   └── lenses.md            Ogilvy, Hopkins, Schwartz, Dry, plain-language and structure lenses
├── scripts/
│   ├── tells.py             deterministic linter: evidence, not verdict
│   ├── hook.py              per-edit and end-of-turn hook runner
│   └── live.py              local live-preview server and page
└── templates/BRAND.md       brand voice profile schema
hooks/hooks.json             plugin hooks (PostToolUse, Stop)
evals/                       20 fixtures, an example brand, and a skill-vs-baseline runner
tests/                       linter, hook, and live-server unit tests
docs/                        research audit, architecture, command spec, testing strategy
```

A request loads `SKILL.md`, one command file, and only the references that command needs. The full knowledge base is never in context at once.

## Testing

- `python -m unittest discover -s tests` runs the linter, hook, and live-server tests (33).
- `python evals/run.py` runs every fixture through the skill and through baseline Claude, then grades both with a judge model against expectations a senior editor would hold: problems that must be found, false positives that must be avoided, phrases that must survive a polish, and facts that must not be invented. See [docs/testing.md](docs/testing.md).

The fixtures cover generic AI marketing copy, strong but unconventional writing, technically accurate but unpersuasive writing, persuasive but misleading writing, overcomplicated writing, distinctive brand language, and copy that should stay unchanged.

## Documentation

- [docs/research-audit.md](docs/research-audit.md): what existing skills do, what they miss, licensing
- [docs/architecture.md](docs/architecture.md): design decisions and roadmap
- [docs/commands.md](docs/commands.md): full command specification
- [docs/testing.md](docs/testing.md): testing and validation strategy
- [docs/eval-results.md](docs/eval-results.md): skill vs. baseline results so far

## Credits and license

Apache-2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE).

The architecture is inspired by [Impeccable](https://github.com/pbakaus/impeccable) (Apache-2.0). The diagnostic lenses draw on David Ogilvy, Claude Hopkins, Eugene Schwartz, Harry Dry, Barbara Minto, Robert Cialdini, the Google developer documentation style guide (CC BY 4.0), and the Microsoft Writing Style Guide. All text in this repository is original; no third-party skill text was copied. Details in [docs/research-audit.md](docs/research-audit.md#licensing).
