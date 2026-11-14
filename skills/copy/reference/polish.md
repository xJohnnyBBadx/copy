# polish

The publication-ready pass. Fixes what is wrong and what causes real friction, makes the piece consistent, and leaves everything else alone. The output should read as the author's own best draft, not as an editor's rewrite.

**Loads:** [restraint.md](restraint.md) (read first), [tells.md](tells.md), the matching "Don't flag" list in [contexts.md](contexts.md), BRAND.md if present (its mechanics rules govern).

**Input:** the text. Optional: the house style or BRAND.md, the publication, a prior critique.

## Preconditions

- If a prior critique in this conversation found P0 or P1 problems that are still unresolved, say that polish won't fix them, and ask whether to proceed anyway.
- If, on reading, the piece clearly has a strategic hole (no discernible promise, a misleading claim), report it in two lines and ask before polishing. Polishing a broken argument makes it harder to see that it's broken.
- If more than about a quarter of the sentences would need to change, stop and recommend `critique`.

## Passes

Work in this order; later passes must not undo earlier ones.

1. **Correctness.** Spelling, grammar, agreement, punctuation errors, broken sentences, wrong words (affect/effect), duplicated words. Fix them.
2. **Internal consistency.** The same fact stated two ways (a price, a date, a count) gets **flagged, not fixed**: you can't know which is right. Terminology, capitalization, hyphenation, numerals, serial comma, and spelling variant follow BRAND.md, or else the piece's dominant convention. Fix these.
3. **Sentence-level friction.** Only real friction for this reader: ambiguous referents, sentences that need rereading, stacked clauses, buried verbs, redundancy (the same point twice). Each change must name its problem.
4. **Confirmed tells.** Apply only tells confirmed against [tells.md](tells.md) and the profile. Run the linter if available (see [audit.md](audit.md)); confirm before acting.
5. **Flow.** Transitions and paragraph breaks, lightly. Don't re-order sections; that is a structural change for `critique`.
6. **Final read.** Read the result aloud in your head as the reader. Run the restraint self-check on every changed passage. Revert anything that is only different.

## Never in polish

- Changing a claim's strength, a fact, a figure, a name, a quote, or legal text. Flag it instead.
- Re-ordering sections, cutting sections, adding sections, or changing the headline's angle. Offer as a note if needed.
- Adding calls to action, benefits, urgency, or "you" framing that weren't there.
- Normalizing deliberate devices or the author's mechanics.

## Output

```
## Polished text
<the full revised text>

## Change log
Corrected:   "before" → "after"   (one line each; group trivial typos as "N typo fixes")
Consistency: rule applied, e.g. "serial comma throughout (dominant convention)"
Tightened:   "before" → "after" · reason
Tells:       "before" → "after" · family

## Needs the author
- "quote" — two different figures for the same thing; which is right?
- "quote" — claim may need substantiation [NEEDS: …]

## Left alone
One or two lines on deliberate choices kept (e.g. "Kept the fragments in the closing; they carry the rhythm").
```

If the text needed no changes beyond typos, say so plainly. That is a good outcome, not a failed run.
