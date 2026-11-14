<!-- fixture
{
  "id": "f15-unchanged-docs",
  "category": "should-remain-unchanged",
  "profile": "12",
  "commands": [
    "critique",
    "polish"
  ],
  "brief": "Help-centre article for small-business owners using Ledgerly, an invoicing app.",
  "expect_verdict": [
    "Ship"
  ],
  "must_flag": [],
  "must_not_flag": [
    {
      "id": "passive",
      "desc": "Must not flag 'Invoices you've already sent are not affected' passive voice"
    },
    {
      "id": "repetition",
      "desc": "Must not flag repetition of 'Ledgerly' (consistency)"
    },
    {
      "id": "add-persuasion",
      "desc": "Must not suggest adding benefits, CTAs, or brand voice"
    },
    {
      "id": "restructure",
      "desc": "Must not recommend restructuring the steps"
    }
  ],
  "preserve": [
    "Invoices you've already sent are not affected.",
    "If someone else manages your website, ask them to do steps 3 and 4."
  ],
  "polish_min_similarity": 0.95,
  "brand": null
}
-->
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
