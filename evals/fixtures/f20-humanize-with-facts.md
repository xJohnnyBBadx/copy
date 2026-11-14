<!-- fixture
{
  "id": "f20-humanize-with-facts",
  "category": "generic-ai",
  "profile": "11",
  "commands": [
    "humanize",
    "audit"
  ],
  "brief": "Opening of a blog post for Ledgerly aimed at small-business owners.",
  "expect_verdict": [
    "Revise"
  ],
  "must_flag": [
    {
      "id": "throat",
      "desc": "Throat-clearing: 'In today's fast-paced world', 'It's worth noting', 'here's the thing'"
    },
    {
      "id": "reveal",
      "desc": "'It's not just a filing cabinet. It's a peace of mind machine.' reveal construction"
    },
    {
      "id": "comes-in",
      "desc": "'That's where Ledgerly comes in'"
    }
  ],
  "must_not_flag": [
    {
      "id": "drop-facts",
      "desc": "Humanize must keep the facts: IRS three-year guidance, 'five different places', email/photos/bank feeds"
    },
    {
      "id": "invent",
      "desc": "Must not add new statistics or claims"
    }
  ],
  "preserve": [
    "three years",
    "five different places",
    "email, photos, and bank feeds"
  ],
  "polish_min_similarity": null,
  "brand": null
}
-->
In today's fast-paced world of small business accounting, receipts can feel like a never-ending challenge. It's worth noting that the IRS generally recommends keeping records for three years. But here's the thing: most owners don't lose receipts because they're careless. They lose them because receipts arrive in five different places.

That's where Ledgerly comes in. Ledgerly pulls receipts from email, photos, and bank feeds into one place, so nothing slips through the cracks. It's not just a filing cabinet. It's a peace of mind machine.
