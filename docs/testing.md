# Testing and validation

COPY's claim is that it judges writing better than an unaided model: it finds what matters, avoids false positives, keeps the author's voice, and invents nothing. That claim is only as good as the tests behind it.

## Layers

| Layer | What it checks | How |
|---|---|---|
| Linter unit tests | `tells.py` finds what it should, ignores literal and contextual uses, keeps strong fixtures quiet | `python -m unittest discover -s tests` |
| Fixture evals | The skill's judgment on 20 pieces with known answers, against baseline Claude | `python evals/run.py` |
| Human review | Whether the judge's grades match an editor's | Read `evals/results/<run>/*.out.md` alongside `summary.md` |

## Fixtures

Each file in `evals/fixtures/` holds a piece of writing and, in a JSON header, what a senior editor would expect:

- `profile`: the context profile it should be judged under.
- `brief`: the author's context, including facts the reviewer may rely on (for misleading-claim fixtures, the true facts).
- `expect_verdict`: acceptable verdicts.
- `must_flag`: problems any good review must find.
- `must_not_flag`: false positives and harmful advice to avoid.
- `preserve` and `polish_min_similarity`: phrases that must survive rewrites, and how similar a polish of good copy must stay.
- `brand`: an optional brand profile copied in as BRAND.md.

| Category | Fixtures | What it tests |
|---|---|---|
| Generic AI marketing copy | f01, f02, f03, f20 | Finds the missing idea under the tells; humanize keeps facts |
| Strong but unconventional | f04, f05, f18, f19 | Leaves fragments, long headlines, repetition, em dashes, and scene-setting alone |
| Technically accurate, unpersuasive | f08, f09 | Finds the buried differentiator and missing narrative; doesn't dumb down jargon or add hype |
| Persuasive but misleading | f10, f11, f12 | Puts claim integrity first (P0); doesn't invent replacement proof |
| Overcomplicated | f13, f14 | Clarity for the stated reader; catches euphemism that hides bad news |
| Distinctive brand language | f06, f07 | Brand vocabulary overrides pattern lists; voice violations caught |
| Should remain unchanged | f15, f16, f17 | Ship verdict; polish changes almost nothing |

## Runner

`evals/run.py` runs each fixture × command under two conditions in a scratch folder containing `piece.md` (and `BRAND.md` when needed):

- **skill:** `claude -p --plugin-dir <repo>`, asked to use the copy skill.
- **baseline:** `claude -p` with the Skill tool disabled, asked the same task in plain words.

A judge model then grades each output against the fixture's expectations and returns JSON: the verdict and whether it matches, must-flag recall, false positives (listed and unlisted), invented facts, usefulness (0–4, anchored), and voice preservation (0–4) for rewrites. Deterministic checks on `polish` and `humanize` outputs: preserved phrases, similarity to the original, and numbers that appear in the rewrite but not in the source.

Output goes to `evals/results/<timestamp>/`: one `.out.md` per run, `results.json`, and `summary.md` with a per-condition table and a per-run table.

```bash
python evals/run.py --dry-run                         # list jobs
python evals/run.py --fixtures f04,f15 --commands critique --workers 2
python evals/run.py                                   # everything (64 jobs, plus judging)
```

On machines that share a CPU budget, wrap it: `testmgr.ps1 run -Name copy-eval -Min 1 -Max 2 -Cmd "python evals/run.py --workers {workers}"`.

## What counts as success

The headline metrics, compared between conditions:

1. **False positives** on strong, unconventional, and should-remain-unchanged fixtures. The most important number: it measures over-editing.
2. **Must-flag recall** on generic, misleading, unpersuasive, and overcomplicated fixtures. COPY must not buy restraint by missing real problems.
3. **Invented facts.** The target is zero.
4. **Voice preservation and similarity** on polish and humanize outputs.
5. **Verdict match.** Useful but secondary; reasonable editors disagree on Revise vs. Rethink.

## Known limits

- **The judge is a model.** It can be lenient or anchored by confident prose. Spot-check judged outputs by hand, especially the verdicts and invented-facts lists. Use a different model for judging when possible (`--judge-model`).
- **Twenty fixtures is a smoke test, not a benchmark.** Add fixtures when a real critique goes wrong; every bug should become a fixture.
- **Single runs are noisy.** For decisions (like the v0.2 gate), run each fixture at least three times and compare distributions.
- **The baseline prompt matters.** It is plain and fair on purpose; don't strengthen or weaken it between runs you intend to compare.
