# critique

Full editorial and strategic evaluation. Diagnoses; does not rewrite the piece. Example improvements are short and illustrate a finding.

**Loads:** [rubric.md](rubric.md), the matching profile in [contexts.md](contexts.md), the lenses that profile names in [lenses.md](lenses.md), [claims.md](claims.md), [tells.md](tells.md), and BRAND.md if present. Read [restraint.md](restraint.md) before writing any example.

**Input:** the text (required). Helpful but optional: the reader, the goal, the channel, a brand profile, competitor examples. Don't block on optional inputs; infer, state the inference in the intent read, and mark affected scores "(inferred)".

## Process

Do the passes in order. Strategy first, so that sentence-level noise doesn't crowd out the problems that matter.

1. **Intent read.** As in SKILL.md setup. Choose the context profile and note its tiers.

2. **First read as the reader.** Read the whole piece once without marking it, as the intended reader would. Write two or three sentences: what lands, what the reader would take away, and where they would stop reading or stop believing.

3. **Strategy pass.**
   - State the piece's central promise or thesis in one sentence. If you can't, that is a finding.
   - Run the swap test, and the obvious-thesis test where the profile names it.
   - Check reader fit: does the opening match the reader's awareness level?
   - Inventory the claims and place each on the evidence ladder ([claims.md](claims.md)). Any misleading claim is P0.

4. **Structure pass.** List the reader's questions in the order they would ask them, and compare with the piece's order. Check emphasis, redundancy, missing sections, and for persuasive contexts the objection-and-proof sequence and the fit of the ask.

5. **Language pass.** Clarity, specificity, voice, distinctiveness. Form your own judgment first. Then, if Python is available, run the linter for evidence:
   ```bash
   python3 "<skill-dir>/scripts/tells.py" --json --context <profile-number> <file>
   ```
   (Use `python` on Windows; pass `-` and pipe the text for pasted copy.) Confirm or reject each hit against [tells.md](tells.md) calibration. Never report a raw hit unconfirmed. If Python is unavailable, scan manually using tells.md and say the linter didn't run.

6. **Score** the nine dimensions 0–4 or n/a against the rubric anchors. Quote evidence for every 0, 1, and 4.

7. **Name what works.** One to three specific strengths, quoted. These are the parts any revision must keep. This step is mandatory, even for weak pieces; it is how the critique protects the author from over-editing later.

8. **Write the findings.** Run every candidate through the severity tests in [rubric.md](rubric.md#severity-tests-apply-to-every-finding-before-reporting-it) first; most over-editing happens here, when an optional addition or a hunch about readers gets reported as a structural defect. Then order them: P0, then P1, then P2. Merge findings that share a cause (twelve vague adjectives are one specificity finding, or a symptom of a positioning finding). Cap at about seven meaningful findings. Mention P3 preferences and Alternatives only when they serve the brief, and label them.

9. **Verdict and next step** per [rubric.md](rubric.md). Recommend the single highest-leverage change. Suggest a next command only when it fits: `polish` only when there are no P0 or P1 findings left; `voice create` when voice findings would benefit from a profile; a fresh `critique` after a strategic revision.

## Output

```
## Intent read
Piece · Profile · Reader (awareness) · Job · Constraints · Confidence

## Reader's experience
Two or three sentences.

## Verdict: Ship | Revise | Rethink
One line: the reason. Then: the single highest-leverage next step.

## What works (keep these)
- "quote" — why it works

## Findings
[P0 · Strategy · Credibility & claim integrity] Problem in one line
  Evidence:       "exact quote" (location)
  Why it matters: cost to this reader in this context
  Intervention:   what to change, at the level of the problem
  Example:        short revision in the author's voice, or [NEEDS: …]

(P1 findings, then P2. Then, if useful, a short "Preferences and alternatives" list, labelled.)

## Scores
| Layer | Dimension | Tier | Score | Note |
(Nine rows. Note gives the evidence in a phrase. Mark n/a and (inferred) where they apply.)

## Not flagged
One or two lines naming patterns you deliberately left alone and why (e.g. "Fragments in the second paragraph are deliberate rhythm in a manifesto"). Include "Linter: N hits, M confirmed" or "Linter did not run."
```

## When the piece works

If the verdict is Ship, keep the report short: intent read, verdict, what works, at most three optional notes, scores, and "not flagged." Do not manufacture findings to fill the format.

Before settling on Revise for a piece with no P0, re-read each P1 against the severity tests. If none survives, the verdict is Ship, and the former P1s become optional notes or are dropped. The failure this guards against: a well-made piece earns Revise because the reviewer found things it *could* add. Saying "this works; change nothing" with reasons is a complete and useful critique.

## Comparing versions

If given two or more versions, critique each briefly against the same profile, then say which better serves the job and why, dimension by dimension where they differ. Don't merge them into a third version unless asked.
