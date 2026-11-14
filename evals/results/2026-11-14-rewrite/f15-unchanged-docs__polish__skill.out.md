Linter run: 0 findings, 145 words, mean sentence 12.8 words, CV 0.36. Clean on the mechanical pass. My read agrees.

**Intent read**
- **Piece:** Help-centre how-to, ~145 words — intro, prerequisites, four numbered steps, outcome.
- **Context profile:** 12 · Technical & explanatory.
- **Reader:** Small-business owner inside Ledgerly, product-aware, mid-task; not a sysadmin.
- **Job:** Reader completes DNS setup without a support ticket, and knows what to expect while waiting.
- **Constraints:** Help-centre register; UI labels and DNS behaviour are facts, not copy.
- **Confidence:** High.

This piece does its job. It is task-first, uses second person and present tense, keeps one term per concept, and sets the expectation about the 48-hour wait before the reader hits it. One cross-reference needs the author's call; nothing else earns a change.

<<<REVISED
# Set up a custom sending domain

When you send invoices from your own domain (for example, billing@yourcompany.com), fewer of them land in spam. Setup takes about 15 minutes, plus up to 48 hours for your DNS provider to publish the changes.

## Before you start

You need access to your domain's DNS settings. If someone else manages your website, ask them to do steps 3 and 4.

## Steps

1. In Ledgerly, go to **Settings > Email > Sending domain**.
2. Enter your domain and select **Generate records**. Ledgerly shows three CNAME records.
3. Sign in to your DNS provider and add each record exactly as shown.
4. Back in Ledgerly, select **Verify**. If verification fails, wait an hour and try again; DNS changes can take time to spread.

When verification succeeds, Ledgerly sends all new invoices from your domain. Invoices you've already sent are not affected.
REVISED>>>

## Change log

No changes. Correctness, consistency, friction, tells and flow passes all came back clean:

- **Corrected:** nothing. No spelling, grammar, agreement or punctuation errors. The semicolon in step 4 is used correctly.
- **Consistency:** already consistent. UI actions are all "select"; UI labels are all bold; "DNS provider" is used for the provider throughout; numbers follow one convention (words below ten, numerals at ten and above).
- **Tightened:** nothing. Mean sentence length 12.8 words with real variation — no stacked clauses, no ambiguous referents, no sentence that needs rereading.
- **Tells:** none found, by linter or by reading. No marketing language has leaked into the documentation.

## Needs the author

- **"ask them to do steps 3 and 4"** — the cross-reference doesn't match the steps. Step 3 is the DNS work; step 4 is back inside Ledgerly, which the person managing the website may not have access to. If they don't have a Ledgerly login, this should read **"step 3"** and the article should say the owner returns to finish step 4. If your agencies and web developers typically do hold a Ledgerly seat, "steps 3 and 4" is right as written. I can't tell which is true for Ledgerly's customers, so I've left it alone rather than guess — a wrong guess here either misdirects the developer or leaves verification undone.

## Left alone

- **"spread" rather than "propagate."** Reads like a deliberate plain-language choice for a non-technical reader. Kept.
- **"fewer of them land in spam."** Correctly hedged — it doesn't promise deliverability. Kept at that strength.
- **"are not affected"** in the closing. Passive, but the actor is irrelevant and the sentence is the clearest form of the point.
- **The 48-hour expectation in the intro.** Setting it before the reader starts, and pairing it with the hourly retry in step 4, is what keeps this article out of the support queue. It's the best thing here.