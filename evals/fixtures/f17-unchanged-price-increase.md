<!-- fixture
{
  "id": "f17-unchanged-price-increase",
  "category": "should-remain-unchanged",
  "profile": "6",
  "commands": [
    "critique",
    "polish"
  ],
  "brief": "Email from the founder to all Ledgerly customers announcing a price increase.",
  "expect_verdict": [
    "Ship"
  ],
  "must_flag": [],
  "must_not_flag": [
    {
      "id": "em-dash",
      "desc": "Must not flag the em dash"
    },
    {
      "id": "first-person",
      "desc": "Must not flag the founder's first-person voice"
    },
    {
      "id": "soften",
      "desc": "Must not recommend softening the news or adding marketing language"
    }
  ],
  "preserve": [
    "A person will read it",
    "we'd rather charge more than cut support hours"
  ],
  "polish_min_similarity": 0.95,
  "brand": null
}
-->
Subject: We're raising prices on June 1

Starting June 1, the Team plan will cost $14 per user per month, up from $10. The Solo plan stays at $6.

We're raising the price because our hosting and support costs have gone up by about 40% since we last set prices in 2023, and we'd rather charge more than cut support hours.

If you're on an annual plan, nothing changes until your renewal date. If you're on a monthly plan, your first bill at the new price will be after June 1. You can switch to annual before then and keep $10 per user for a full year.

If the new price doesn't work for you, reply to this email. A person will read it — usually me.

Maya Okafor
Founder, Ledgerly
