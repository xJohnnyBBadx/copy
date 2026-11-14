# Research audit and gap analysis

*Conducted 2026-11-14. Every repository was cloned and its files read; nothing below relies on a repository's own description.*

## Summary

The existing copywriting skills are mostly prompt libraries for **generating** marketing copy, aimed at SaaS landing pages and conversion. The useful ideas in them are sound but scattered: Ogilvy's priority order, Harry Dry's three questions, a multi-pass editing sweep, a catalogue of AI writing patterns, and one project (copyskills) with a proper critique contract and a deterministic checker. None of them handles the hard part of editorial judgment: knowing which standards apply to which kind of writing, separating strategic problems from sentence-level ones, checking claims, and **leaving good writing alone**. Several encode absolute rules (remove every adverb, ban em dashes) that would damage strong copy.

The best architectural model is not a copywriting project at all: it is Impeccable, the design skill.

## Repositories

### boraoztunc/skills
- **Contents:** about 100 skills, mostly design and animation. Copy-related: `ogilvy`, `copywriting`, `copy-editing`, `stop-slop`, and `better-writing` (UI microcopy).
- **ogilvy:** a priority hierarchy (positioning → promise → brand image → big idea), headline and body-copy rules, sourced to *How to Create Advertising That Sells* and *Ogilvy on Advertising*. A good diagnostic lens; its research figures come from mid-century print direct response and shouldn't be applied to every format.
- **copy-editing:** the "Seven Sweeps" (clarity, voice and tone, so what, prove it, specificity, heightened emotion, zero risk), originally a Copyhackers method. A good multi-pass structure; conversion-specific.
- **stop-slop** (from hardikpandya/stop-slop): a catalogue of AI writing patterns with a 5-dimension 1–10 score. Useful catalogue; absolutist rules ("kill all adverbs," "no em dashes," "no passive constructions").
- **License:** MIT at the top level. `copywriting` and `copy-editing` are uncredited copies of Corey Haines' marketingskills (MIT); `stop-slop` is credited.

### hughgramel/conversion-copywriting
- **Contents:** a landing-page audit built on Harry Dry's Marketing Examples: a 10-slot page structure, a craft layer (the visualize / falsify / nobody-else test, the 2-second test), a report format with an A/B test hypothesis per finding, and a rule against inventing social proof.
- **Strengths:** the three-question test is the single most useful line-level diagnostic in the set; framing changes as hypotheses rather than guarantees is honest.
- **Limits:** landing pages only; conversion is the only goal.
- **License:** none. The repository bundles scraped Marketing Examples posts and transcriptions. **Ideas only**; no text reused.

### cyrwheelninja/copywriting-skill
- **Contents:** a personal skill (it addresses one named user) that routes to 34 Copyhackers prompts, plus `ai-tropes.md` and `frameworks.md` (AIDA, PAS, BAB, FAB, PASTOR, SCQA, 4 U's).
- **Strengths:** "few-shot beats instructions": voice examples matter more than voice adjectives. Adopted in the BRAND.md design.
- **Limits:** generation-only; no evaluation.
- **License:** none. The prompts were copied from copyhackers.com. **Nothing reused.**

### srstomp/copyskills
- **Contents:** the most engineered project: 15 skills across 8 domains, a TypeScript core with a deterministic anti-slop checker, an MCP server, a CLI, integrations for several agents including Hermes, unit tests. `copy-critique` returns 7 scores (1–10) plus line-level fixes in YAML and refuses to generate.
- **Strengths:** a fixed output contract; separating deterministic detection from model judgment; critique that doesn't generate.
- **Limits:** scores have no behavioural anchors and equal weight; Voice Match defaults to 5 without context; an "AI-Tell ≥ 5" threshold triggers automatic rewriting; em dashes are banned outright. Its own `OPEN-QUESTIONS.md` records the rubric contradictions this causes (double scoring, a UX dimension that breaks the output contract, unresolved per-dimension targets).
- **License:** MIT (Copydoc). Reusable with attribution; COPY reuses ideas, not code.

### robertbstillwell/marketing-skills
- **Contents:** an aggregation: core skills derived from Corey Haines' marketingskills (copywriting, copy-editing, page-cro, product-marketing-context and others), an orchestrator, and vendored packs from alirezarezvani and openclaudia (both MIT).
- **Strengths:** `product-marketing-context` writes a persistent positioning document that other skills read, the same pattern as Impeccable's PRODUCT.md.
- **License:** no top-level license; take anything from the upstream `coreyhaines31/marketingskills` (MIT) instead.

### Impeccable (pbakaus/impeccable, Apache-2.0)
The architecture COPY follows:
- **One skill, many commands.** A command table in SKILL.md; each command loads one reference file on demand.
- **Persistent context files** (PRODUCT.md, DESIGN.md) that every command reads → COPY's BRAND.md.
- **Modes** (Persuade / Operate / Read / Experience) that set how much ambition is appropriate → COPY's 13 context profiles with dimension tiers.
- **A deterministic detector kept apart from judgment,** run in an isolated assessment so it can't anchor the review → COPY's `tells.py`, run after the model's own language pass.
- **Heuristics scored 0–4 with n/a allowed,** P0–P3 severity → COPY's rubric.
- **"Refinement preserves; redesign replaces"** and a craft-floor file read immediately before edits → COPY's `restraint.md`.
- An ignore list, critique snapshots, and runs that end by asking what to do next. Not in COPY v0.1; candidates for later.

## Style guides and sources

| Source | Use in COPY | Terms |
|---|---|---|
| Google developer documentation style guide | Plain-language lens, technical profile | CC BY 4.0: may be quoted with attribution |
| Microsoft Writing Style Guide | Plain-language lens | Not openly licensed: principles only |
| Claude Hopkins, *Scientific Advertising* (1923) | Specificity lens; one short quotation | Public domain in the US |
| David Ogilvy, *Ogilvy on Advertising* (1983) | Positioning → promise → facts | In copyright: ideas in our own words |
| Eugene Schwartz, *Breakthrough Advertising* (1966) | Awareness levels, market sophistication | In copyright: ideas in our own words |
| Harry Dry, *Marketing Examples* | The three questions | In copyright: idea attributed, our own words |
| Barbara Minto, *The Pyramid Principle* | SCQA | In copyright: idea attributed |
| Robert Cialdini, *Influence* | Persuasion principles as diagnostics | In copyright: idea attributed |

## Gap analysis

| Need | Existing coverage | Gap COPY fills |
|---|---|---|
| Evaluation before generation | copyskills `copy-critique` | Others generate first; COPY's v1 is evaluation-only |
| Context-specific standards | Impeccable's modes (design); none for copy | 13 writing-context profiles with dimension tiers and "don't flag" lists |
| Strategic vs. editorial separation | Ogilvy's hierarchy, as advice | Three-layer rubric (strategy, structure, language) and severity tied to layer |
| Anchored scoring | None (all 1–10 without anchors) | 0–4 behavioural anchors, n/a, no composite; verdict from tiers |
| Claim integrity | "Prove it" sweep; "don't invent social proof" | Claim inventory, evidence ladder, misleading-pattern list, regulated-territory flags |
| Restraint / leave-alone | None | `restraint.md`, mandatory before rewrites; Ship verdicts with short reports |
| Calibrated tells | Absolute ban lists | Every pattern family has "don't flag when"; context suppression in the linter |
| Voice profiles | Positioning docs; style-guide templates | BRAND.md with "This, not that" pairs, approved and rejected exemplars, anti-copying rule |
| Testing judgment | Code unit tests only | Fixture corpus with must-flag / must-not-flag, skill vs. baseline, judge model |

## What makes an editorial system different from a prompt library

A prompt library tells a model how to write. An editorial system has to tell it **when not to**. Its value lies in calibration (which standard applies here), diagnosis (what is wrong, at which level, with what evidence), and restraint (what to keep). Models already generate fluent copy. Left alone, they over-edit with confidence and in generic terms, and that is what COPY is built to correct.

## Licensing

COPY is Apache-2.0. All text in this repository is original. From the five repositories, COPY reuses **ideas and patterns only**, attributed where they are distinctive:
- Impeccable (Apache-2.0): architecture patterns. No text copied.
- copyskills (MIT): the critique-only stance and the separate deterministic checker, as ideas. No code copied.
- stop-slop (MIT), marketingskills (MIT): pattern families and the multi-pass idea, rewritten with calibration.
- hughgramel and cyrwheelninja: no license and third-party scraped content. Only the cited, publicly known concepts (Dry's three questions; voice examples over adjectives) are used, in our own words.
