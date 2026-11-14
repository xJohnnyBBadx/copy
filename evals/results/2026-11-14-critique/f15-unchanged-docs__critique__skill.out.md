Critique of `piece.md` — no `BRAND.md` found in the project, so voice is inferred from the piece itself.

---

## Intent read

**Piece:** Help-centre how-to, 145 words — why/how-long intro, prerequisites, four numbered steps, outcome paragraph.
**Profile:** 12 · Technical & explanatory (tiers: S1 C, S3 C, T1 C, L1 C, L2 C; S2 Secondary; T2 and L4 n/a).
**Reader:** A small-business owner inside Ledgerly, solution-aware about the problem (invoices going to spam) and non-technical about DNS. May not manage their own website.
**Job:** The reader completes the setup, and understands the wait, without opening a support ticket.
**Constraints:** Help-centre article; UI strings must match the product; I can't verify Ledgerly's actual screens or record format.
**Confidence:** High on profile and reader. Medium on two product facts I flag as questions rather than findings.

## Reader's experience

The opening does its job in one line: the reader learns why they'd bother, that it costs about 15 minutes of their own time, and that the clock after that isn't Ledgerly's fault. The prerequisites line — "ask them to do steps 3 and 4" — is the moment a non-technical owner relaxes, because someone has thought about how their business actually works.

They stall in two places. If they invoice from a Gmail address, they get four steps in before realising the article was never for them. And if **Verify** fails, they're told to wait an hour — in an article that already said 48 hours — with nothing to do if it fails again.

## Verdict: Revise

A well-built article with gaps at the exact points where readers fail: the prerequisite, the hand-off, and the failure path. No strategic or claim problems; everything here is additive.

**Highest-leverage next step:** rebuild step 4 into a happy path plus a real failure branch, and fix the hand-off line's step numbers in the same pass. Those two edits cover most of the support tickets this article currently generates.

## What works (keep these)

- **Claim discipline.** "fewer of them land in spam" (line 3) and "Invoices you've already sent are not affected" (line 16). The first hedges an outcome most docs overclaim as deliverability; the second closes a scope question before the reader asks it. Any revision that tightens this article must not tighten these.
- **"If someone else manages your website, ask them to do steps 3 and 4."** (line 7) Anticipates the real division of labour at the point the reader is deciding whether to continue. The instinct is the asset — finding 1 fixes the numbers, not the line.
- **"DNS changes can take time to spread"** (line 14). The reader's word, not the internal term ("propagate"). Correct plain-language call for this audience; don't let a later editor upgrade it.

## Findings

```
[P1 · Structure · Argument & hierarchy] The hand-off sends the wrong step to the wrong person
  Evidence:       "ask them to do steps 3 and 4" (line 7), against
                  "4. Back in Ledgerly, select Verify." (line 14)
  Why it matters: Step 4 happens inside Ledgerly, where the web developer has no login. The
                  reader delegates both steps, their developer stalls on step 4, and the setup
                  sits half-finished — in the one line most likely to be acted on literally.
  Intervention:   Split the hand-off at the actual system boundary. One-line fix.
  Example:        "If someone else manages your website, ask them to do step 3; you do step 4
                  in Ledgerly."
```

```
[P1 · Structure · Argument & hierarchy] Failure handling contradicts the article's own timeframe and has no end
  Evidence:       "up to 48 hours for your DNS provider to publish the changes" (line 3) against
                  "If verification fails, wait an hour and try again" (line 14)
  Why it matters: A reader who retries after an hour and fails will reasonably conclude
                  something is broken, because the article told them an hour should be enough.
                  There is also no terminal path: nothing for the reader who has waited the full
                  48 hours. This is where DNS setups get abandoned, and where the ticket gets
                  filed. Mixing the branch into a numbered step also hides it from anyone
                  skimming the procedure.
  Intervention:   Keep step 4 as the happy path. Move failure into its own block, aligned to the
                  48-hour window, ending in a route to a human.
  Example:        "4. Back in Ledgerly, select **Verify**.

                  **If verification fails**
                  DNS changes can take up to 48 hours to spread, so try again later in the day,
                  and again tomorrow. If it still fails after 48 hours, check that each record
                  matches what Ledgerly shows, then [NEEDS: support route — contact link or
                  in-app channel]."
```

```
[P1 · Structure · Argument & hierarchy] "Before you start" omits the prerequisite that disqualifies readers
  Evidence:       "You need access to your domain's DNS settings." (line 7), and the intro's
                  "billing@yourcompany.com" (line 3), which presumes the reader owns a domain
  Why it matters: Owning a domain is assumed, never stated. A small-business owner invoicing
                  from a Gmail or Outlook address cannot complete any of this, and finds out
                  only after reading the whole procedure. For this reader population that is a
                  meaningful share — the prerequisites section is exactly where it should be
                  caught.
  Intervention:   State the domain itself as a prerequisite, and say what to do if the reader
                  doesn't have one.
  Example:        "You need a domain of your own (for example, yourcompany.com) and access to
                  its DNS settings. If you currently send invoices from a Gmail or Outlook
                  address, you'll need to register a domain first." (Confirm whether you want
                  this to link to a "getting a domain" article.)
```

```
[P2 · Language · Specificity] Step 3 is the vaguest line in the article, at the point readers fail
  Evidence:       "add each record exactly as shown" (line 13)
  Why it matters: DNS providers differ on what goes in the host field — some append your domain
                  automatically, so pasting the full name creates a doubled record. That silent
                  mistake produces exactly the failed verification step 4 can't diagnose. "Exactly
                  as shown" is the right instruction only if Ledgerly's display format makes it
                  unambiguous.
  Intervention:   Add one sentence naming the trap. I can't assert your record format, so this
                  is a question to you rather than a rewrite.
  Example:        [NEEDS: confirm whether Ledgerly displays the host as `billing` or as
                  `billing.yourcompany.com`, then add the matching one-line caution — e.g. "Some
                  DNS providers add your domain for you. If yours does, enter only the first part
                  of the record name."]
```

**Open questions for you** (scope calls, not findings): once invoices send from `billing@yourcompany.com`, where do customer replies go, and does the from-name the customer sees change? Both are likely follow-up tickets. They may belong in a sibling article rather than this one — your call.

## Scores

| Layer | Dimension | Tier | Score | Note |
|---|---|---|---|---|
| Strategy | S1 Purpose & reader fit | Critical | 3 | Opens with the reader's benefit and time cost, and knows they may not manage their own DNS; the reader model slips at the domain prerequisite and the step-4 hand-off |
| Strategy | S2 Positioning & differentiation | Secondary | n/a | A procedural help article needs no thesis or differentiation |
| Strategy | S3 Credibility & claim integrity | Critical | 3 | "fewer of them land in spam" and "Invoices you've already sent are not affected" are honestly scoped; not 4 because the article's own 48-hour figure is contradicted at line 14 |
| Structure | T1 Argument & hierarchy | Critical | 3 | Correct task-first order (why → prerequisites → steps → result); loses a point for failure handling tucked inside a numbered step and no terminal path |
| Structure | T2 Persuasive design | n/a | n/a | Informational writing |
| Language | L1 Clarity | Critical | 3 | Short sentences, second person, present tense, exact UI path in bold; the two waiting times collide and "steps 3 and 4" misdirects |
| Language | L2 Specificity | Critical | 3 | "billing@yourcompany.com", "three CNAME records", "Settings > Email > Sending domain" are all concrete; step 3 is the exception |
| Language | L3 Voice fidelity | Secondary | 3 (inferred) | Calm, plain, consistent second person throughout; no BRAND.md to check against |
| Language | L4 Distinctiveness | n/a | n/a | Not a dimension for documentation |

## Not flagged

**CNAME** is left undefined on purpose — it's the literal label the reader will see in their DNS provider's UI, so defining it would add noise; "Ledgerly" and "record" repeat verbatim, which is correct (consistency beats variety in docs); "Invoices you've already sent are not affected" is passive where the actor is irrelevant; the absence of brand voice, benefits language, or a call to action is right for this profile. The hard count in "three CNAME records" will need updating if the record set ever changes, but it helps the reader more than it risks — leaving it.

Linter: 0 hits, 0 confirmed (context 12). Sentence-length variation is healthy (CV 0.36), no em-dash density, no triplets.