# Rubric: dimensions, anchors, severity, verdict

Nine dimensions in three layers. The layers match the order of diagnosis: strategy problems outrank structure problems, which outrank sentence problems.

Each dimension is scored **0–4** against the behavioural anchors below, or **n/a** when the writing context makes it irrelevant. The context profile ([contexts.md](contexts.md)) assigns each dimension a tier: **Critical**, **Important**, **Secondary**, or **n/a**. There is no weighted total. The verdict comes from the tiers and the findings (see Verdict).

## The scale

| Score | Meaning |
|---|---|
| **4** Exceptional | Would survive a demanding editor. Little or nothing to gain from change. Rare. |
| **3** Strong | Clearly serves the job. A few lapses that don't change the reader's experience. |
| **2** Adequate | Does the job generically. A competent professional draft lands here. This is the default for decent copy, not a failing grade. |
| **1** Weak | Present but undermines the piece; the reader notices. |
| **0** Failing | Actively works against the piece's job. |

Calibration rules:
- Score what is on the page for this reader, not what you would have written.
- Quote evidence for any score of 0, 1, or 4. A 4 needs a reason as much as a 0 does.
- Do not inflate. If every dimension is 3 or 4, check yourself against the anchors before reporting.
- Do not default to the midpoint when information is missing. Mark the score "(inferred)" and say what would change it.
- A dimension can be strong while the piece fails. Report the dimension honestly; the verdict carries the overall judgment.

## Strategy layer

### S1 · Purpose & reader fit
Does the piece know who it is for, what that reader already knows and believes, and what it wants them to do, think, or feel?
- **0:** No discernible job, or written to the wrong reader. Talks to itself, its org chart, or its investors when the reader is a customer.
- **2:** Job and reader are inferable but generic ("businesses", "teams", "everyone"). Some sections serve a different reader or a different goal.
- **4:** Every part serves a specific reader at their actual level of awareness. Nothing is there for the author's benefit alone.

### S2 · Positioning & differentiation
Is there one clear promise, idea, or thesis, and could a competitor or a hundred other writers sign it unchanged? For non-commercial writing, read this as: is there a thesis that adds something the reader didn't already hold?
- **0:** No promise or thesis, or one that fails the swap test completely (replace the name with a competitor's and nothing breaks).
- **2:** A promise exists but is category-generic, or the real differentiator is present but buried or one item among five.
- **4:** One sharp, ownable idea, stated where the reader will meet it, with everything else in the piece supporting it.

### S3 · Credibility & claim integrity
Are claims proportionate to evidence? Is proof specific, checkable, and placed where doubt arises? Is anything misleading? (Method: [claims.md](claims.md).)
- **0:** Contains a misleading or unsupportable claim: false precision, an implied guarantee, a superlative or comparison with no basis, an outcome presented as typical when it isn't. **Any misleading claim caps this dimension at 1 and is a P0 finding**, however good the rest is.
- **2:** Claims are plausible but asserted with adjectives rather than shown. Proof is generic ("trusted by leading teams").
- **4:** Every material claim is evidenced, honestly qualified, or clearly framed as belief. Proof is specific and sits next to the claim it supports.

## Structure layer

### T1 · Argument & hierarchy
Order, emphasis, and flow. Does the most important thing arrive where this reader needs it? Does each section earn its place?
- **0:** No discernible order. The key point is buried or missing. Sections repeat each other.
- **2:** Logical but flat: equal weight on everything, some redundancy, transitions doing work the structure should do.
- **4:** The order follows the reader's real questions. Emphasis matches importance. Nothing can be moved or cut without loss.

### T2 · Persuasive design
*n/a for purely informational writing.* Does the piece move the reader through desire, proof, objections, and a next step that fits their readiness, without manipulation?
- **0:** Asks without giving a reason, or persuades by pressure: false urgency, invented scarcity, fear without basis, fake social proof.
- **2:** The standard moves are present (benefits, a call to action) but real objections are ignored, or the ask is mismatched to how ready the reader is.
- **4:** Anticipates the reader's actual objections in the order they arise. The ask fits the reader's readiness. Persuades through relevance and evidence.

## Language layer

### L1 · Clarity
Understood on first read by the intended reader. Clarity is relative to the reader: precise technical vocabulary for experts is clarity, not jargon.
- **0:** After reading, the reader can't say what it means. Ambiguous referents, undefined terms, sentences that need rereading.
- **2:** Understandable with effort. Some abstraction, long or stacked clauses, hedges that blur the point.
- **4:** Effortless for the intended reader. The complexity lives in the ideas, not in the prose.

### L2 · Specificity
Concrete nouns, numbers, names, examples, images. Can the reader picture it? Could the claim be shown false?
- **0:** Abstract throughout. Every claim unfalsifiable; nothing to picture.
- **2:** A mix, but the key claims are still vague.
- **4:** The key claims are concrete and checkable. Where the piece goes abstract (a manifesto, a tagline), the abstraction is deliberate and earned by concrete moments around it.

### L3 · Voice fidelity
Consistency with the brand profile, or, without one, with the voice the piece establishes in its strongest passages (mark "(inferred)").
- **0:** Contradicts the brand (an understated brand shouting), or the voice shifts so often that there is none.
- **2:** Neutral and inoffensive; could belong to any brand in the category. Occasional drift.
- **4:** Unmistakably this author or brand, consistent across sections. Tone flexes with the moment without losing identity.

### L4 · Distinctiveness
Originality and memorability. Fresh language, and at least one idea or line a reader would remember and repeat.
- **0:** Assembled from stock phrases. Reads as a template or machine output. Nothing memorable.
- **2:** Clean but forgettable: competent category language.
- **4:** At least one line or idea the reader will remember and attribute to this brand. Fresh without straining.

## Severity

| Level | Covers | Rule |
|---|---|---|
| **P0 · Critical** | Strategic or integrity failure: wrong reader or job; no differentiating idea where the context requires one; a misleading or unsupportable claim; legal, regulatory, or factual risk; chatbot residue or placeholder text in copy meant for publication. | Report first. Sentence edits are wasted until it is resolved. |
| **P1 · Structural** | Order, emphasis, missing or redundant sections, gaps in the argument, persuasion architecture, a buried lede. | Report after P0s. |
| **P2 · Sentence** | Clarity, specificity, redundancy, confirmed tells, rhythm, inconsistency in terms or mechanics. | Group them; don't list every instance. |
| **P3 · Preference** | Defensible either way. Mention only when it serves the brief. Never framed as an error. | Optional. |
| **Alternative** | A creative option: a different headline, angle, or line. Labelled as an option, never as a correction. | Offer two or three at most. |

### Severity tests (apply to every finding before reporting it)

- **P0 / P1 test:** would a demanding editor hold publication for this? If the reader can still understand, believe, and act as intended without the fix, it is not P1.
- **Additive test:** a suggestion to *add* something the piece doesn't contain (an extra section, a failure path, a qualifier for an edge case, a new proof point) is P3 or an Alternative unless the piece's stated scope requires it and its reader cannot complete the job without it. "It could also cover…" is never P1.
- **Speculation test:** a finding that rests on an unstated assumption about readers ("users abandon here," "this generates support tickets," "most readers lack X") or on outside facts not in the piece or brief must say so ("If many readers…") and can't be above P2. Better: ask the author.
- **Contradiction test:** before calling two statements inconsistent, check whether both can be true at once (a 48-hour window and "retry in an hour" are compatible).

Where a finding sits depends on its effect, not its type. One stock phrase in a strong piece is P3. The same phrase repeated across a homepage so that the brand sounds like everyone else is a symptom of an S2 problem and belongs under that finding.

## Verdict

Work out the verdict from the tiers in the active context profile:

- **Rethink:** any P0 finding, or any **Critical**-tier dimension at 0–1. The fix is strategic or structural; polishing is premature.
- **Revise:** no P0, but at least one P1 finding, any **Critical**-tier dimension at 2, or any **Important**-tier dimension at 0–1.
- **Ship:** no P0 or P1, every **Critical**-tier dimension at 3 or above, and no **Important**-tier dimension below 2. Optional P2/P3 notes only.

State the verdict in one line with the reason ("Revise: the differentiator is buried in section three, and claims are unsupported"). Follow it with the single highest-leverage next step.
