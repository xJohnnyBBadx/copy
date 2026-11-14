# Eval results

## 2026-11-14 · first comparison (subset)

Claude Code CLI default model for both the reviewed runs and the judge, one run per cell. A smoke test, not a benchmark: see the limits in [testing.md](testing.md#known-limits).

### Critique: f01, f04, f10, f15, f19

| Condition | Verdict match | Must-flag recall | False positives | Invented facts | Usefulness (0–4) | Cost |
|---|---|---|---|---|---|---|
| baseline | 3/5 | 10/10 | 13 | 9 | 3.20 | $4.43 |
| skill v0.1.0 | 3/5 | 10/10 | 7 | 6 | 3.20 | $7.75 |

- Both conditions found every required problem on the generic (f01) and misleading (f10) pieces. The skill did it with no false positives or invented facts; baseline produced three of each.
- **Both failed the same way on good copy.** On the manifesto (f04) and the help article (f15), both returned Revise. They escalated optional additions to structural defects and stated guesses about reader behaviour ("this article generates support tickets") as fact. On f15 the skill was barely better than baseline (5 vs 6 false positives, 4 vs 3 invented facts).

### Fix (same day)

Added **severity tests** to `rubric.md`: a publication-hold test for P0/P1, an additive test (suggestions to add things are P3 unless the reader can't do the job without them), a speculation test (assumptions about readers are labelled and capped at P2), and a contradiction test. `critique.md` now runs every finding through them and re-checks P1s before choosing Revise over Ship. SKILL.md principle 5 now covers guesses about reader behaviour.

### Re-check after fix: f04, f15 (skill only)

| Fixture | Before | After |
|---|---|---|
| f04 manifesto | Revise · 2 false positives · usefulness 2 | **Ship** · 0 false positives · usefulness 4 (one miscounted sentence length) |
| f15 help article | Revise · 5 false positives · 4 invented · usefulness 2 | **Ship** · 0 false positives · 0 invented · usefulness 4 |

### Rewrites: polish f15, humanize f20

| Condition | Verdict match | Recall | False positives | Invented | Usefulness | Voice kept | Phrases preserved | Similarity to original |
|---|---|---|---|---|---|---|---|---|
| baseline | 1/2 | 3/3 | 0 | 0 | 3.50 | 3.50 | 3/5 | f15 0.996 · f20 0.36 |
| skill | 2/2 | 3/3 | 0 | 0 | 4.00 | 4.00 | 5/5 | f15 1.000 · f20 0.73 |

On humanize, the skill removed the same tells while keeping about twice as much of the original text, and it kept every required fact phrase. Baseline dropped "email, photos, and bank feeds". (Similarity figures were recomputed after a runner fix: difflib's autojunk had been distorting them.)

### Next

Run the full 20-fixture set three times per condition with the fixed skill before calling the v0.2 gate. Fixtures not yet exercised: f02, f03, f05–f09, f11–f14, f16–f18, and the `audit` and `voice check` commands.
