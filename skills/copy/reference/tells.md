# Tells: machine-made and template patterns, with calibration

These patterns make writing read as template or machine output. They were common in weak human writing long before language models; flag them because they weaken the writing, not because of who wrote it. **Never claim a text is AI-generated.**

A tell is evidence of inattention, not a crime. Calibrate:
- **One instance in a strong piece** is P3 at most, and often not worth mentioning.
- **Clusters matter.** Several families in one paragraph, or one family repeated across a page, is P2. When the clustering makes a brand sound like everyone else, it is a symptom of a positioning problem (S2): report it there.
- **Context overrides the list.** Each family has a "don't flag" rule. So does each profile in [contexts.md](contexts.md). BRAND.md vocabulary overrides everything here.
- **Fix the cause, not the word.** Swapping "leverage" for "use" doesn't help a sentence that has nothing to say. Often the fix is a concrete fact; sometimes it is deleting the sentence.

The family IDs match the output of `scripts/tells.py`.

---

### `residue` · Chatbot residue
"Certainly!", "Great question", "I hope this helps", "As an AI", "Here is a revised version", "[Your Company]", "[Insert statistic]", knowledge-cutoff talk.
- **Flag:** always, in anything meant for publication. **P0**: it reveals the piece wasn't read before shipping.
- **Don't flag:** inside a document that is explicitly a draft or a template.

### `vocab` · Stock vocabulary
delve, tapestry, testament to, realm, landscape (as in "the AI landscape"), ever-evolving, fast-paced world, game-changer, synergy, leverage, unlock (potential / value / power), elevate, empower, seamless, cutting-edge, holistic, pivotal, embark, journey (for a customer process), harness, foster, streamline, revolutionize, transformative, paradigm, robust (outside engineering and statistics).
- **Flag:** two or more in a paragraph, or any where a concrete word or fact exists.
- **Don't flag:** literal and technical senses ("robust standard errors," "a landscape painting," "navigate to Settings"); vocabulary listed in BRAND.md; a quote from someone else.
- **Fix:** name the actual thing. "Unlock your team's potential" → what does the team do afterwards that it couldn't before?

### `throat` · Throat-clearing and signposting
"Here's the thing", "It's worth noting", "Let's dive in", "In this article, we'll", "At the end of the day", "When it comes to", "The truth is", "Let me be clear".
- **Flag:** in short copy and openings, where it delays the point.
- **Don't flag:** scripts (the ear needs signposts); long documentation, where navigation aids help.
- **Fix:** delete it and start at the point.

### `reveal` · Reveal constructions
"It's not X, it's Y." "Not just X, but Y." "X isn't about Y. It's about Z." "This isn't a tool. It's a movement."
- **Flag:** when X is a straw man nobody holds; when the construction appears more than once in a piece; when it's used to inflate (a product "isn't software, it's a movement").
- **Don't flag:** a single deliberate correction of a belief the reader really holds. That can be the positioning itself ("Most backup tools protect files. Ours protects the restore.").
- **Fix:** state Y directly, with its proof.

### `triplet` · Reflexive triplets
"Fast, simple, and secure." Three adjectives, three clauses, three bullet points, every time.
- **Flag:** when the pattern repeats in a short span, or when the third item is filler that adds rhythm but no meaning.
- **Don't flag:** a deliberate rhetorical triad in a manifesto, speech, or ad; a genuine list of exactly three things.
- **Fix:** keep the items that are true and specific; two strong items beat three padded ones.

### `puffery` · Puffery and empty intensifiers
world-class, best-in-class, industry-leading, state-of-the-art, next-generation, unparalleled, unmatched, revolutionary, incredibly, truly, deeply, extremely, very, amazing.
- **Flag:** as a credibility issue more than a style one. Unearned superlatives are claims; check them under [claims.md](claims.md).
- **Don't flag:** a superlative the author can substantiate and does; casual intensifiers in social copy or dialogue.
- **Fix:** replace the adjective with the fact that would justify it.

### `attribution` · Vague attribution and hollow proof
"Studies show", "Experts agree", "Research suggests", "Many customers say", "It is widely known", "Trusted by leading companies".
- **Flag:** always, as a claim-integrity issue (P2, or P0 if it carries a material claim).
- **Fix:** name the source, or remove the borrowed authority and own the claim as opinion.

### `hedge` · Hedge stacks
"May potentially help", "can help to", "could possibly", "in some ways", "arguably", "it could be said that".
- **Flag:** where the author has the evidence to commit, or where the hedging blurs the point.
- **Don't flag:** honest uncertainty; medical, financial, legal, and forward-looking qualifications (these may be required); scientific writing.
- **Fix:** commit where the evidence supports it; qualify once, precisely, where it doesn't.

### `significance` · Inflated significance
"Plays a pivotal role", "stands as a testament", "marks a significant milestone", "underscores the importance", "a key part of", "serves as a".
- **Flag:** when the sentence asserts importance instead of showing it.
- **Fix:** show the consequence. "Marks a milestone" → what can now happen that couldn't before?

### `agency` · Abstractions as actors
"The data tells a story." "Innovation meets design." "The decision emerges." "This is where X comes in."
- **Flag:** when it hides who did what, especially in corporate or bad-news communications.
- **Don't flag:** in ads and manifestos where personification is deliberate and clear.
- **Fix:** name the person or team who acted.

### `ending` · Generic endings
"The future is bright." "Exciting times ahead." "Only time will tell." "In conclusion," "Ultimately, it's about…" A closing line that restates the opening.
- **Flag:** when the ending adds nothing and could close any piece.
- **Fix:** end on the most specific thing: the next step, the strongest fact, the line the reader should remember.

### `claim` · Claim candidates
Guarantees, "clinically proven," "the only," "#1," "up to 10×," unanchored comparisons, environmental and health words, scarcity and deadlines.
- **Not a style family.** Each hit is a claim to check with [claims.md](claims.md). Report it under Claims, with its place on the evidence ladder, not as a tell.
- **Don't flag:** a claim the brief or BRAND.md shows is substantiated; a guarantee with stated terms.

### `rhythm` · Formulaic rhythm (metrics, not phrases)
The linter reports sentence-length uniformity, paragraphs that all end on a short punchline, runs of dramatic fragments ("Simple. Fast. Secure."), density of rhetorical questions, and comma-heavy trailing clauses.
- **Flag:** metronomic sameness across a whole piece; every paragraph ending in an aphorism.
- **Don't flag:** deliberate cadence in manifestos, ads, scripts, and social copy, where rhythm is part of the craft.
- **Fix:** vary by meaning, not by formula. Let a sentence be long when the thought is.

### `format` · Formatting tells
Title Case on every heading when the house style is sentence case; bold-label bullets on every list ("**Speed:** …"); emoji bullets; em dashes at high density.
- **Em dashes:** never ban them. Flag only density (the linter reports dashes per 100 words) or when every sentence pivots on one. Long-form, editorial, and many brand voices use them well.
- **Don't flag:** formatting that matches BRAND.md or the publication's style.

### `stack` · Heading-stack repetition
The first lines of a block (a slide, card, or section) often stack an eyebrow, a title, and a subtitle. The linter flags a content word that appears in more than one of those first three lines, for example "SCOPE / FEE / SCHEDULE" above "Scope, fee and schedule" above "One fixed fee…". Sentence-level checks can't see this, because each line is fine on its own. Words that open most blocks (a recurring "ACME / SECTION" prefix) count as boilerplate and are ignored. Pass brand names with `--allow`.
- **Flag:** an eyebrow that repeats the title; a subtitle that restates the title instead of giving the bottom line.
- **Don't flag:** a deliberate repeat that builds (a series name carried across slides); a product name that has to appear in both lines.
- **Fix:** give each line one job. The eyebrow says where the reader is, the title says what the block is, and the subtitle gives the bottom line.
- **Input:** keep the structure when you feed the linter. Put one block per slide or card, separated by blank lines, with the eyebrow, title and subtitle on their own lines. A flattened paragraph hides the stack.

### Manual-only: synonym cycling
Calling the same thing three names ("the platform… the solution… the tool"). The linter can't see it; read for it. Especially damaging in technical, investor, and product writing, where readers assume a new word means a new thing.
- **Fix:** pick one term and keep it.
