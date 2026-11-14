# COPY eval run 20261114-152310

| Condition | Runs | Verdict match | Must-flag recall | False positives | Invented facts | Usefulness (0-4) | Voice kept (0-4) | Phrases preserved | Cost (USD) |
|---|---|---|---|---|---|---|---|---|---|
| baseline | 5 | 3/5 | 10/10 | 13 | 9 | 3.20 | 3.00 | - | 4.43 |
| skill | 5 | 3/5 | 10/10 | 7 | 6 | 3.20 | 3.25 | - | 7.75 |

| Fixture | Command | Condition | Verdict | Match | Recall | FP | Invented | Useful | Similarity | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| f01-generic-saas-landing | critique | baseline | Rethink | True | 4/4 | 1 | 2 | 4 | - | Catches all four required problems with specific line-level evidence, applies an explicit swap test, names the strategic (not cosmetic) fix, and correctly rules |
| f01-generic-saas-landing | critique | skill | Rethink | True | 4/4 | 0 | 0 | 4 | - | Hits all four required problems with quoted evidence and correct prioritization (swap-test failure as the single highest-leverage fix), and uses [NEEDS: ...] pl |
| f04-strong-manifesto | critique | baseline | Revise | False | - | 4 | 2 | 2 | - | The 'what's load-bearing' section is genuinely excellent editorial judgment — it protects 'Not because slow is a virtue', the unround 'eleven', and the softer ' |
| f04-strong-manifesto | critique | skill | Revise | False | - | 2 | 0 | 2 | - | Craft is high — accurate intent read, precise 'what works', and an explicit 'Not flagged' section that correctly protects the fragments, the 'Not because…' corr |
| f10-misleading-focus-app | critique | baseline | Rethink | True | 6/6 | 2 | 2 | 4 | - | Catches all six required integrity failures with line-level sourcing, correctly refuses to soften the false claims into hedged variants, adds the genuinely seni |
| f10-misleading-focus-app | critique | skill | Rethink | True | 6/6 | 0 | 1 | 4 | - | All six required problems are caught and correctly ranked as P0 integrity failures, with the verdict and the 'remove the clinical claim and the superlative has  |
| f15-unchanged-docs | critique | baseline | Revise | False | - | 6 | 3 | 2 | - | The review avoids all four named traps and praises the piece's real strengths at length, but then manufactures three 'Major' gaps on an article the editor judge |
| f15-unchanged-docs | critique | skill | Revise | False | - | 5 | 4 | 2 | - | The review is well-crafted and explicitly protects the piece's claim discipline, plain language, and absence of persuasion — it dodges three of the four named t |
| f19-strong-longform | critique | baseline | Ship | True | - | 0 | 0 | 4 | - |  |
| f19-strong-longform | critique | skill | Ship | True | - | 0 | 1 | 4 | - | Correctly ships, names what makes the opening work with verbatim evidence, and explicitly protects the long sentence, em-dash aside and tense shift from a later |
