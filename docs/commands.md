# Command specification

Every command starts with the same setup (SKILL.md): load the target, load BRAND.md if present, write the **intent read** (piece, context profile, reader and awareness level, job, constraints, confidence), load the command's reference, and read `restraint.md` before writing any rewrite.

All findings use one shape: **Problem → Evidence (quoted) → Why it matters → Intervention → Example.** Severity: P0 strategic or integrity · P1 structural · P2 sentence · P3 preference · Alternative (labelled option).

---

## critique

| | |
|---|---|
| **Purpose** | Full editorial and strategic evaluation. The default when someone asks "is this good?" |
| **Input** | Required: the text. Optional: reader, goal, channel, BRAND.md, competitor copy, a second version to compare. |
| **Criteria** | Nine rubric dimensions scored 0–4 or n/a, tiered by the context profile; claim inventory and evidence ladder; lenses named by the profile; calibrated tells. |
| **Process** | Intent read → first read as the reader → strategy pass → structure pass → language pass (own judgment, then linter) → scores → what works → findings → verdict. |
| **Output** | Intent read; reader's experience; verdict (Ship / Revise / Rethink) with reason and the one highest-leverage next step; what works (keep these); up to about seven findings, P0 first; scores table; "not flagged" with linter tally. |
| **Does not** | Rewrite the piece; invent proof; pad a Ship report with findings. |
| **Reference** | `reference/critique.md` |

## audit

| | |
|---|---|
| **Purpose** | Fast language and claim scan before publishing or across many pieces. |
| **Input** | Required: the text. Optional: context profile, BRAND.md (its vocabulary overrides pattern lists; its banned words go to `--avoid`). |
| **Criteria** | Pattern families in `tells.md` with their calibration; `claims.md` for claim candidates; redundancy, synonym cycling, padding by reading. |
| **Process** | Short intent read → linter → confirm or reject every hit → read for what the linter can't see → report. |
| **Output** | Density line with linter tally (hits, confirmed, rejected and why); claims list; pattern table grouped by family with quoted instances and fixes; "left alone"; a closing read on whether the problem is surface-level or a missing idea. |
| **Does not** | Score dimensions or give a strategic verdict. |
| **Reference** | `reference/audit.md` |

## humanize

| | |
|---|---|
| **Purpose** | Remove robotic and template patterns while keeping everything else. |
| **Input** | The text. |
| **Process** | Audit restricted to robotic families → if tells cover a missing idea, stop and recommend critique → otherwise apply confirmed fixes under restraint, with `[NEEDS: …]` where a fix needs a fact. |
| **Output** | Revised text; change log (`"before" → "after" (family)`); left-alone list; claims flagged for the author. |
| **Does not** | Change facts, claims, structure, or deliberate devices. |
| **Reference** | `reference/audit.md#humanize-mode` |

## polish

| | |
|---|---|
| **Purpose** | Publication-ready pass with the smallest diff that fixes real problems. |
| **Input** | Required: the text. Optional: house style or BRAND.md, publication, a prior critique. |
| **Preconditions** | Stops and asks if a known P0/P1 is open, if a strategic hole is evident, or if more than about a quarter of sentences would change (recommends critique). |
| **Process** | Correctness → internal consistency (conflicting facts flagged, not fixed) → sentence-level friction → confirmed tells → light flow → final read and restraint self-check. |
| **Output** | Polished text; change log (corrected, consistency, tightened, tells); "needs the author"; "left alone". |
| **Does not** | Change claims, facts, figures, quotes, legal text, section order, or the headline's angle; add CTAs or urgency. |
| **Reference** | `reference/polish.md` |

## voice

| | |
|---|---|
| **Purpose** | `voice create`: build or update a BRAND.md profile. `voice check`: score a piece against it. |
| **Input (create)** | In order of value: on-voice samples; approved and rejected examples with reasons; strategy and positioning; audience and their words; competitive context; personality and values; mechanics. |
| **Process (create)** | Gather missing inputs in one round → analyse samples by behaviour (register, sentence shape, vocabulary, claims, humour, mechanics, what it never does) → fill the template with "This, not that" pairs → calibrate with an on-voice and a generic passage → confirm location → save. |
| **Output (check)** | `Voice: n/4` with reason; deviations citing the BRAND.md rule broken, with in-voice fixes; passages worth keeping as exemplars; profile gaps. |
| **Does not** | Invent positioning, proof, or audience research; reuse exemplar sentences verbatim unless listed as signature phrases. |
| **Reference** | `reference/voice.md`, `templates/BRAND.md` |

## live

| | |
|---|---|
| **Purpose** | Local preview of one copy file: linter hits underlined in place, passage-level questions, apply-back. |
| **Input** | A local file; optional profile (`--context`), brand profile (`--brand`), model (`--model`). |
| **Process** | Start `scripts/live.py` in the background → give the user the tokenized 127.0.0.1 URL → stop it when work on the file ends. |
| **Output** | A page. Passage questions return verdict (keep/change), diagnosis, findings, and labelled alternatives as JSON; Apply replaces the exact passage only if it occurs once. |
| **Does not** | Bind beyond localhost; edit anything without an explicit Apply click; work on deployed URLs. |
| **Reference** | `reference/live.md` |

## hooks

| | |
|---|---|
| **Purpose** | Run the linter automatically while an agent edits copy files. |
| **Input** | `on`, `off`, or `status`; configuration in `.copy/config.json`. |
| **Behaviour** | Opt-in per project (BRAND.md, `.copy/`, or config). Per edit: immediate tier only (residue, brand-avoid, claim, attribution). End of turn: full deep pass over touched files, once per session, deduplicated. |
| **Does not** | Fire in projects that haven't opted in; fail the agent's turn on any error; repeat a finding in the same session. |
| **Reference** | `reference/hooks.md` |

---

## Planned (v0.2)

Each will be a reference file reusing the rubric, contexts, and restraint. Until built, a request for one runs `critique` with emphasis on the matching dimension and offers two or three labelled alternatives.

| Command | Purpose | Emphasis |
|---|---|---|
| `quieter` | Remove hype, overclaiming, and pressure while keeping energy | L4, S3, T2 |
| `bolder` | Explore more distinctive, confident directions as labelled options | L4, S2 |
| `distill` | Reduce to the essential argument; report what was cut | T1, S2 |
| `sharpen` | Replace vague language with specifics, using `[NEEDS: …]` for missing proof | L2, S3 |
| `position` | Evaluate differentiation against competitor copy | S2, S1 |
| `structure` | Reorder by the reader's questions | T1, T2 |
