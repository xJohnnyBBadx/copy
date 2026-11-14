# COPY eval run 20261114-153948

| Condition | Runs | Verdict match | Must-flag recall | False positives | Invented facts | Usefulness (0-4) | Voice kept (0-4) | Phrases preserved | Cost (USD) |
|---|---|---|---|---|---|---|---|---|---|
| baseline | 2 | 1/2 | 3/3 | 0 | 0 | 3.50 | 3.50 | 3/5 | 1.34 |
| skill | 2 | 2/2 | 3/3 | 0 | 0 | 4.00 | 4.00 | 5/5 | 2.24 |

| Fixture | Command | Condition | Verdict | Match | Recall | FP | Invented | Useful | Similarity | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| f15-unchanged-docs | polish | baseline | Ship | True | - | 0 | 0 | 4 | 0.996 | Correctly ships the piece and explicitly declines every trap (passive reassurance, 'Ledgerly' repetition, 'spread' vs 'propagate', step restructuring, persuasio |
| f15-unchanged-docs | polish | skill | Ship | True | - | 0 | 0 | 4 | 1.0 | Correctly ships the piece unchanged, explicitly defends the passive closing, the 'Ledgerly' repetition and the plain-language 'spread' instead of flagging them, |
| f20-humanize-with-facts | humanize | baseline | none | False | 3/3 | 0 | 0 | 3 | 0.022 | The rewrite removes all three throat-clearing phrases, the 'That's where Ledgerly comes in' pivot, and the 'not just X, it's Y' reveal while keeping the IRS thr |
| f20-humanize-with-facts | humanize | skill | Revise | True | 3/3 | 0 | 0 | 4 | 0.006 | All three required tells are caught and fixed (throat-clearing in both the 'vocab' and 'throat' entries, the 'comes in' lead-in as 'agency', and the not-just/it |
