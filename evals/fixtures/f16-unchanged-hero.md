<!-- fixture
{
  "id": "f16-unchanged-hero",
  "category": "should-remain-unchanged",
  "profile": "3",
  "commands": [
    "critique",
    "polish"
  ],
  "brief": "Homepage hero for Ledgerly's receipt-matching feature. Reader: freelancers and small-business owners whose accountant chases them for receipts.",
  "expect_verdict": [
    "Ship"
  ],
  "must_flag": [],
  "must_not_flag": [
    {
      "id": "triplet",
      "desc": "Must not flag 'reads..., matches..., and files...' as a reflexive triplet; it describes three real steps"
    },
    {
      "id": "headline-rewrite",
      "desc": "Must not present a replacement headline as a correction (alternatives must be labelled as options)"
    }
  ],
  "preserve": [
    "Your accountant will stop emailing you for receipts.",
    "You don't forward anything."
  ],
  "polish_min_similarity": 0.95,
  "brand": null
}
-->
# Your accountant will stop emailing you for receipts.

Ledgerly reads the receipts in your inbox, matches them to bank transactions, and files them where your accountant can find them. You don't forward anything.

[Connect your inbox - free for 30 days]
