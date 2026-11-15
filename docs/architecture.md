# Architecture

## Design goals

1. **Judgment, not volume.** Success is measured by how reliably the system finds what matters and leaves the rest alone, not by how much it rewrites.
2. **Progressive disclosure.** A request loads SKILL.md (about 150 lines), one command file, and only the references that command needs. The full knowledge base is never in context at once.
3. **Portable.** A plain Agent Skills folder: Markdown plus one optional standard-library Python script. No MCP server, no build step, no API key.
4. **Testable.** Expectations live in fixtures, and every claim about quality can be checked against baseline Claude.

## Layout

```
.claude-plugin/          plugin.json + marketplace.json (Claude Code plugin install)
skills/copy/             the skill; this folder alone is the portable artifact
  SKILL.md               principles, setup, intent read, command table, routing, output contract, hard rules
  reference/             loaded on demand
    critique.md audit.md polish.md voice.md       commands
    rubric.md contexts.md restraint.md claims.md tells.md lenses.md   shared knowledge
  scripts/tells.py       deterministic linter (evidence, not verdict)
  scripts/hook.py        hook runner (PostToolUse immediate tier, Stop deep pass)
  scripts/live.py        local live-preview server + page
hooks/hooks.json         plugin hook wiring
  templates/BRAND.md     voice profile schema
evals/                   fixtures, example brand, runner, results
tests/                   linter unit tests
docs/                    this documentation
```

### What each command loads

| Command | Loads |
|---|---|
| critique | rubric, one contexts profile, its lenses, claims, tells, restraint (before examples), BRAND.md |
| audit / humanize | tells, claims, the profile's "don't flag" list, restraint (before fixes), BRAND.md |
| polish | restraint (first), tells, the profile's "don't flag" list, BRAND.md |
| voice | BRAND template, rubric (L3 anchors), restraint (before examples) |

## Key decisions (2026-11-14)

| Decision | Choice | Why |
|---|---|---|
| Command scope for v0.1 | `critique`, `audit` (+ `humanize` alias), `polish`, `voice` | The spec's ten commands overlap: humanize is audit plus fixes; sharpen overlaps polish; hierarchy is critique's structure layer. Build the judgment core first and prove it with evals before adding directional commands. |
| Scoring | 0–4 behavioural anchors per dimension, n/a allowed, tiers per context, verdict Ship / Revise / Rethink, **no composite score** | 1–10 scales without anchors produce false precision; weighted totals invite gaming and hide a P0 behind good averages. Tiers let a manifesto and a help article be judged by different standards. |
| Dimensions | 9, in three layers: Strategy (purpose & reader fit, positioning & differentiation, credibility & claim integrity), Structure (argument & hierarchy, persuasive design), Language (clarity, specificity, voice fidelity, distinctiveness) | The spec's ten overlapped (originality / memorability / differentiation) and treated persuasion as universal. Layers match the strategic / structural / sentence distinction and the order of diagnosis. |
| Frameworks | One compact lens file, not a folder of framework files | Models already know AIDA and PAS; they are drafting templates, weak as diagnostics. Tokens go to what models get wrong by default: context, restraint, claims, calibration. |
| Tells | Calibrated catalogue + deterministic linter whose hits must be confirmed; the model forms its own judgment before reading linter output | Absolute ban lists cause the over-editing COPY exists to prevent. Following Impeccable, deterministic output is kept from anchoring judgment. |
| Brand voice | BRAND.md with behavioural rules, "This, not that" pairs, approved and rejected exemplars, and a no-verbatim-reuse rule (except listed signature phrases) | "Learning" a voice is really loading a profile and examples at runtime. Pairs carry more signal than adjectives; the anti-copying rule stops exemplar sentences from leaking into new copy. |
| Brand storage | `BRAND.md` at project root, or `.copy/brands/<slug>.md` for multiple clients | Lives with the client's work, versioned with it, like Impeccable's PRODUCT.md. |
| Portability | Agent Skills format only; no agent-specific adapters | The format is read by Claude Code, Codex, Cursor, OpenClaw, Hermes Agent and others. Adapters are maintenance without benefit. |
| UI microcopy | Out of scope; defer to a UX-writing skill | Impeccable's `clarify` and similar skills cover it; COPY can critique it but says the other tool is better. |
| License | Apache-2.0 | Matches Impeccable's lineage; patent grant; NOTICE file for attribution. |
| Local tooling (2026-11-14, Luis chose hooks + live) | Plugin hooks: PostToolUse reports only an immediate tier (residue, brand-avoid, claim, attribution); Stop runs a once-per-session deep pass over touched files. `live.py` serves a token-protected 127.0.0.1 page with in-place underlines, passage questions via `claude -p`, and an exact single-occurrence apply. A `copy` CLI wrapper was not chosen; `tells.py` is the CLI. | Mirrors Impeccable's two-tier detector hook and live mode. Hooks are opt-in per project (BRAND.md or `.copy/`) because Markdown is everywhere in code repos. Stop feedback uses `decision: block` once, guarded by `stop_hook_active`, so it can't loop. |

## Assumptions in the original specification, challenged

- **"Ten commands."** Fragmentation costs routing accuracy and maintenance. Five entry points cover the core; directional commands come once judgment is proven.
- **"Scoring rubrics."** Kept, but without a composite number. The verdict is categorical and explains itself.
- **"Frameworks folder (AIDA, PAS, FAB…)."** Replaced with a single lens file used for diagnosis.
- **"Learn the voice from samples."** Reframed as a profile plus exemplars loaded at runtime, with explicit anti-copying rules.
- **"Hermes compatibility."** Achieved by the open format, not by an adapter.
- **"Compare against baseline Claude."** Kept and built into the eval runner as a first-class condition.

## Roadmap

**v0.1 (this release).** Core commands, rubric, 13 profiles, restraint, claims, calibrated tells, linter, BRAND.md schema, 20 fixtures, skill-vs-baseline runner.

**v0.1.1 (2026-11-14).** Severity tests after the first eval; plugin hooks (per-edit immediate tier + end-of-turn deep pass); `live` preview page; BRAND.md vocabulary feeds the linter; `live` and `hooks` commands.

**v0.2: directional commands**, each a reference file that reuses the rubric and restraint:
- `quieter`: tone down hype and overclaiming (likely the most used; AI copy errs loud).
- `bolder`: distinctive, confident alternatives, labelled as options.
- `distill`: reduce to the essential argument; report what was cut and why.
- `sharpen`: specificity pass, with `[NEEDS: …]` where proof is missing.
- `position`: positioning and competitive differentiation, given competitor copy.
- `structure`: reorder by the reader's questions.

Gate: on the full fixture set, the v0.1 skill beats baseline on false positives and voice preservation without losing must-flag recall.

**v0.3: workflow.**
- `.copy/ignore.md` to suppress findings the author has rejected.
- Critique snapshots to track a piece across revisions.
- A no-argument menu that recommends the next command from the last critique.
- Optional isolated-subagent mode for critique (judgment pass and linter pass kept apart, as Impeccable does).

**Later.** More fixtures (non-English, regulated industries, long documents), fixture contributions from real anonymized copy, a public leaderboard of skill vs. baseline across models.
