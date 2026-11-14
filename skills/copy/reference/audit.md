# audit

A fast scan of the language and the claims: tells, clichés, redundancy, and weak or unsupported claims. No scores and no strategic verdict; that is `critique`'s job. Use audit before publishing, on a large volume of copy, or when the question is "does this read as machine-made or padded?"

**Loads:** [tells.md](tells.md), [claims.md](claims.md), and the matching "Don't flag" list from [contexts.md](contexts.md). BRAND.md if present (its vocabulary overrides the tell lists). Read [restraint.md](restraint.md) before writing any fix.

**Input:** the text. Optional: the context, a brand profile.

## Process

1. **Intent read, short form.** One line: piece, profile, reader. Audit needs the profile to know what not to flag.

2. **Run the linter.**
   ```bash
   python3 "<skill-dir>/scripts/tells.py" --json --context <profile-number> <file>
   ```
   (Use `python` on Windows; pass `-` and pipe the text for pasted copy. Add `--avoid "word,phrase"` for terms BRAND.md lists as banned.) If Python is unavailable, scan manually with [tells.md](tells.md) and say the linter didn't run.

3. **Judge every hit.** Confirm or reject it using the family's calibration and the profile's "Don't flag" list. Keep a count of rejected hits and the main reason ("4 rejected: literal uses of 'robust' in a statistics context").

4. **Read for what the linter can't see:**
   - redundancy: the same point made twice, sentences that restate the heading;
   - synonym cycling for one concept;
   - clichés and dead metaphors not on any list;
   - padding: sentences that could be deleted with no loss;
   - claims: list any that are unsupported or misleading ([claims.md](claims.md)). Misleading claims are P0 even in an audit.

5. **Report.** Group by family, highest severity first. For clusters, quote two or three instances and give the count instead of listing every one.

## Output

```
## Audit: <piece> · <profile>
Density: N confirmed issues in W words. Linter: H hits, C confirmed, R rejected (main reason).

## Claims
- [P0] "quote" — why it misleads → honest version / [NEEDS: …]
- [P2] "quote" — unsupported → the proof that would carry it

## Patterns
| Sev | Family | Instances (quoted, with location) | Fix |

## Left alone
Patterns deliberately not flagged, and why.

## Read
One or two sentences: is the problem surface-level (fixable by editing), or are the tells covering for a missing idea (needs critique)?
```

The last section matters. Copy that is all stock phrases usually has no specific thing to say. Removing the phrases won't create one. When that is the case, say so and recommend `critique`.

## Humanize mode

`humanize` runs this audit restricted to robotic and template patterns (families `residue`, `vocab`, `throat`, `reveal`, `triplet`, `puffery`, `significance`, `agency`, `ending`, `rhythm`, `format`, plus synonym cycling), then applies the confirmed fixes.

1. Run steps 1–4 above.
2. If the read says the tells are covering for a missing idea, stop before rewriting: report that, show two or three representative fixes, and recommend `critique`. Humanizing can't supply substance.
3. Otherwise read [restraint.md](restraint.md) and apply only confirmed fixes. Keep everything else verbatim: facts, claims, structure, voice, deliberate devices.
4. Where a fix needs a fact the text doesn't have, use `[NEEDS: …]` rather than inventing one.
5. Run the restraint self-check on every change.

Humanize output: the revised text, then a change log of the form `"before" → "after" (family)`, then a short "left alone" list. If a fix would change a claim, flag it for the author instead of making it.
