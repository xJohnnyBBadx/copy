# COPY eval run 20261114-154420

| Condition | Runs | Verdict match | Must-flag recall | False positives | Invented facts | Usefulness (0-4) | Voice kept (0-4) | Phrases preserved | Cost (USD) |
|---|---|---|---|---|---|---|---|---|---|
| skill | 2 | 2/2 | - | 0 | 1 | 4.00 | 4.00 | - | 2.26 |

| Fixture | Command | Condition | Verdict | Match | Recall | FP | Invented | Useful | Similarity | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| f04-strong-manifesto | critique | skill | Ship | True | - | 0 | 1 | 4 | - | Correctly ships, names the specific lines carrying the piece, and pre-empts all four trap behaviors explicitly (fragments defended as cadence, the 'Not because' |
| f15-unchanged-docs | critique | skill | Ship | True | - | 0 | 0 | 4 | - | Correctly ships the piece and explicitly protects everything the must-not list guards — the unquantified spam claim, the undefined DNS/CNAME terms, the final 'a |
