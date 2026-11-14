This piece is already publication-ready. I found one substantive issue and no mechanical ones, so the revision below is the original with a single change.

**The one change:** "ask them to do steps 3 and 4" → "ask them to do step 3." Step 4 happens in Ledgerly, not in DNS, so it doesn't require the access the "Before you start" section is gating on — and whoever manages the website may not have a Ledgerly login at all. Narrowing it to step 3 keeps the handoff accurate. If the author intended the DNS person to also verify (because they'd know when the records had propagated), revert this and say so explicitly in the text instead.

**Checked and deliberately left alone:**
- "DNS changes can take time to spread" — "spread" instead of "propagate" is the right call for this audience. Not jargon-corrected.
- "wait an hour and try again" alongside "up to 48 hours" in the intro — reads as a retry cadence within the stated window, not a contradiction.
- The "Steps" heading is generic but conventional for help centres and useful as an anchor target.
- UI bolding, sentence-case headings, list punctuation, and `>` breadcrumbs are already consistent throughout.
- Benefit-plus-time-cost intro and the closing "already sent are not affected" reassurance are both doing real work. No trimming.

<<<REVISED
# Set up a custom sending domain

When you send invoices from your own domain (for example, billing@yourcompany.com), fewer of them land in spam. Setup takes about 15 minutes, plus up to 48 hours for your DNS provider to publish the changes.

## Before you start

You need access to your domain's DNS settings. If someone else manages your website, ask them to do step 3.

## Steps

1. In Ledgerly, go to **Settings > Email > Sending domain**.
2. Enter your domain and select **Generate records**. Ledgerly shows three CNAME records.
3. Sign in to your DNS provider and add each record exactly as shown.
4. Back in Ledgerly, select **Verify**. If verification fails, wait an hour and try again; DNS changes can take time to spread.

When verification succeeds, Ledgerly sends all new invoices from your domain. Invoices you've already sent are not affected.
REVISED>>>