## Intent read

- **Piece:** Help-centre how-to, ~145 words: one task article on connecting a custom sending domain in Ledgerly.
- **Profile:** 12 · Technical & explanatory (tiers: S1, S3, T1, L1, L2 Critical; S2, L3 Secondary; T2, L4 n/a).
- **Reader:** A small-business owner already using Ledgerly — product-aware, task-focused, arriving either because invoices are landing in spam or because they saw the setting. Not a DNS administrator.
- **Job:** Get them from "my invoices go to spam" to verified records, and set expectations so a slow DNS update doesn't read as a failure.
- **Constraints:** Help-centre article; no BRAND.md supplied and the brief limits me to piece.md, so L3 is inferred from the piece's own register.
- **Confidence:** High. The only inference that matters is that step 4 needs Ledgerly access, which the piece itself states ("Back in Ledgerly").

## Reader's experience

The first two sentences tell them why to bother and what it will cost them in time, which is exactly the order they'd ask it in. "Before you start" catches the most common real situation — someone else handles the website — and the numbered steps are short enough to follow with the DNS provider open in another tab. The ending answers the question they'd otherwise write into support: already-sent invoices are not affected.

## Verdict: Ship

The piece does its job: task-first order, concrete instructions, honestly hedged claims, and the two likeliest reader questions ("how long?" and "what about invoices I already sent?") answered before they're asked. **Highest-leverage next step:** change "steps 3 and 4" to name only step 3, since step 4 happens inside the reader's own Ledgerly account. One phrase, no restructuring.

## What works (keep these)

- **"fewer of them land in spam"** — hedged to exactly what the mechanism supports. A number here would be stronger-sounding and less honest; resist the temptation to add one.
- **"Setup takes about 15 minutes, plus up to 48 hours for your DNS provider to publish the changes."** — separates the reader's effort from the waiting, in the opening, where it prevents the "is it broken?" support ticket.
- **"If someone else manages your website, ask them to do steps 3 and 4."** — anticipates the delegation case in the reader's own words rather than "your DNS administrator." The scoping is off by one step (below), but the instinct behind the sentence is the best thing in the article.
- **"Invoices you've already sent are not affected."** — ends on the specific thing the reader is quietly worried about.

## Findings

```
[P2 · Language · Clarity] The delegation instruction hands off a step that happens in the reader's own Ledgerly account
  Evidence:       "If someone else manages your website, ask them to do steps 3 and 4." (Before you start)
                  vs. "4. Back in Ledgerly, select **Verify**." (Steps)
  Why it matters: The stated prerequisite is "access to your domain's DNS settings," which only step 3
                  needs. An owner who forwards "steps 3 and 4" is asking their web person for Ledgerly
                  access they probably don't have, and the handoff stalls until the owner works out that
                  step 4 was always theirs. Self-correcting, but it's friction in the one scenario the
                  article went out of its way to support.
  Intervention:   One phrase. Scope the handoff to step 3 and keep step 4 with the reader.
  Example:        "If someone else manages your website, ask them to do step 3; you can finish step 4
                  yourself."
  Note:           If the intent was that a helper with Ledgerly access does both, say so instead — but
                  then the prerequisite line needs to mention Ledgerly access too.
```

**Optional (P3)**

```
[P3 · Structure · Argument & hierarchy] No exit from the retry loop
  Evidence:       "If verification fails, wait an hour and try again; DNS changes can take time to spread."
  Why it matters: A reader on their fourth attempt past the 48-hour mark has no stated next move. In a
                  help centre, the stuck reader is the likeliest reader. Defensible either way: this is an
                  addition, not a defect, and a separate troubleshooting article may already cover it.
  Intervention:   If a troubleshooting page or support route exists, one sentence pointing to it after
                  the retry advice. Nothing to change in the article's shape.
```

## Scores

| Layer | Dimension | Tier | Score | Note |
|---|---|---|---|---|
| Strategy | S1 Purpose & reader fit | Critical | 3 | Right reader at the right awareness level; the delegation path mis-scopes one step |
| Strategy | S2 Positioning & differentiation | Secondary | 2 | No differentiation job here; the implicit promise is deliverability, correctly stated once |
| Strategy | S3 Credibility & claim integrity | Critical | 3 | "fewer", "about 15 minutes", "up to 48 hours" all proportionate; scope limit on sent invoices stated |
| Structure | T1 Argument & hierarchy | Critical | 4 | Order matches the reader's questions; nothing movable or cuttable — "Invoices you've already sent are not affected" is the correct last beat |
| Structure | T2 Persuasive design | n/a | n/a | Informational |
| Language | L1 Clarity | Critical | 3 | Second person, present tense, one action per step; the "steps 3 and 4" slip is the single snag |
| Language | L2 Specificity | Critical | 4 | "three CNAME records", "**Settings > Email > Sending domain**", "billing@yourcompany.com" — every instruction checkable |
| Language | L3 Voice fidelity | Secondary | 3 (inferred) | Consistent plain instructional register; no marketing language leaks into the steps |
| Language | L4 Distinctiveness | n/a | n/a | Documentation |

## Not flagged

"DNS" and "CNAME" are left undefined on purpose — they're the words the reader will see in their DNS provider's interface, so defining them would help less than naming them does. The 48-hour window and "wait an hour and try again" are compatible, not a contradiction. "If someone else manages your website" is the reader's framing of who handles DNS and is better than the technically precise version. "fewer of them land in spam" stays unquantified: a number the article can't source would be worse. Linter: 0 hits, 0 confirmed (sentence-length CV 0.36, no triplets, no em-dash density).

No `polish` needed — the one edit above is targeted, and a polish pass on 145 words this disciplined would mostly find things to change rather than things to fix.