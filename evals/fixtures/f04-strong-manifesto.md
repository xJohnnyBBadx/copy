<!-- fixture
{
  "id": "f04-strong-manifesto",
  "category": "strong-unconventional",
  "profile": "2",
  "commands": [
    "critique",
    "polish"
  ],
  "brief": "Brand manifesto for a small custom bicycle frame builder. Appears on the About page.",
  "expect_verdict": [
    "Ship"
  ],
  "must_flag": [],
  "must_not_flag": [
    {
      "id": "fragments",
      "desc": "Must not flag fragments or short sentences ('Good.', 'No more.') as errors"
    },
    {
      "id": "not-because",
      "desc": "Must not flag 'Not because slow is a virtue. Because...' as a formulaic reveal; it is a deliberate correction"
    },
    {
      "id": "no-cta",
      "desc": "Must not ask for a CTA, benefits, or conversion elements"
    },
    {
      "id": "shorten",
      "desc": "Must not recommend shortening or simplifying the piece"
    }
  ],
  "preserve": [
    "We like materials that warn you.",
    "We'd like them to have nothing to say.",
    "Twelve frames a month. No more."
  ],
  "polish_min_similarity": 0.93,
  "brand": null
}
-->
We build bicycles slowly.

Not because slow is a virtue. Because a frame brazed in an afternoon is a frame brazed in a hurry, and hurry shows up eleven years later, at a joint, on a descent.

We use steel. Steel bends before it breaks, and it tells you first. We like materials that warn you.

We don't make a bike for everyone. We make one for you, after we've measured you twice and argued with you once. If you want it next week, we're the wrong shop. Good. There are other shops.

Every frame leaves with the builder's initials under the bottom bracket, where nobody will see them but the next person who fixes it. That person will know who to blame. We'd like them to have nothing to say.

Twelve frames a month. No more.
