# voice

Create or update a brand voice profile, or check a piece against one. The profile is a file, `BRAND.md`, that every other command reads. It turns "our voice is confident and warm" into rules and examples an editor can actually apply.

**Loads:** [../templates/BRAND.md](../templates/BRAND.md) (the schema), [rubric.md](rubric.md) (L3 anchors), [restraint.md](restraint.md) before writing any example.

**Where profiles live:** one brand per project → `BRAND.md` at the project root. Several clients or brands in one workspace → `.copy/brands/<slug>.md`, selected by name ("voice check for acme"). Ask before writing to a location the user hasn't confirmed.

## `voice create` (and update)

### 1. Gather
Ask only for what is missing, in one short round. Useful inputs, in order of value:
1. **Writing samples** the brand considers on-voice: published copy, emails, a founder's posts. Three to ten pieces.
2. **Approved and rejected examples:** "this sounds like us / this doesn't," ideally with a reason. These pairs carry more signal than any adjective.
3. **Strategy:** what the brand does, for whom, its positioning, its proof points.
4. **Audience:** who reads, what they know, the words they use themselves.
5. **Competitive context:** who else the reader sees, and how the brand must not sound.
6. **Personality and values,** if the user has them written down.
7. **Mechanics:** house style for spelling, numerals, capitalization, punctuation, emoji.

With samples, draft first and ask after: it is faster for the user to correct a draft than to answer a questionnaire. Without samples, ask the questions in the template's order, a section at a time.

### 2. Analyse the samples
Describe the voice by behaviour, not adjectives:
- **Register and person:** formal to casual; we / you / I; contractions.
- **Sentence shape:** typical length and range; how often fragments, questions, or lists appear.
- **Vocabulary:** words used repeatedly; words conspicuously absent; jargon level; signature phrases.
- **Claims and proof:** how boldly it claims; how it proves (numbers, names, stories, none).
- **Humour and figurative language:** whether, what kind, how often.
- **Punctuation and mechanics:** dashes, exclamation marks, emoji, capitalization style.
- **What it never does.** Often the most distinctive part.

Mark every observation with how many samples support it. Don't generalize from one sample.

### 3. Write the profile
Fill [the template](../templates/BRAND.md). Rules:
- Every personality trait gets a **"This, not that"** pair: a short on-voice line and an off-voice line, plus the behavioural rule behind it. "Confident" alone means nothing; "states claims without hedges, never uses exclamation marks" does.
- Exemplar sentences are references, not material. Mark the few phrases the brand wants reused as **signature phrases**; everything else is not to be copied word for word.
- Leave unknown fields as `TBD` with the question that would fill them. Never invent positioning, proof points, or audience research.

### 4. Calibrate
Write two short passages for a realistic task (for example, a product announcement opening): one in the profiled voice, one deliberately generic. Ask the user whether the first sounds like them and what's off. Fold corrections into the profile. One round is usually enough; offer a second.

### 5. Save
Show the profile, confirm the location, then write it. Note the date and the inputs used in the profile's front matter.

## `voice check`

Compare a piece with the profile.

1. Load BRAND.md. If there is none, offer `voice create`, or check against the voice the piece establishes in its strongest passages and say so.
2. Score L3 Voice fidelity against the rubric anchors.
3. List deviations, highest impact first. For each: the quote, the BRAND.md rule it breaks (cite the section), why it matters, and an in-voice fix written under the restraint rules.
4. Note on-voice passages worth keeping as future exemplars.
5. Note **profile gaps:** places the piece made a reasonable choice the profile doesn't cover, or where the profile's rule seems wrong for this context. Suggest the profile update; don't make it unasked.

Output: `Voice: <score>/4` with one line of reason, then the deviations in the standard finding format, then "Worth keeping," then "Profile gaps."
