<!-- fixture
{
  "id": "f07-voice-mismatch",
  "category": "distinctive-brand",
  "profile": "3",
  "commands": [
    "critique",
    "voice check"
  ],
  "brief": "Draft product page from a new freelancer for the same coffee roaster. Brand profile supplied as BRAND.md.",
  "expect_verdict": [
    "Rethink",
    "Revise"
  ],
  "must_flag": [
    {
      "id": "voice-violation",
      "desc": "Breaks the brand voice: exclamation marks, hype, 'symphony' language the profile explicitly rejects"
    },
    {
      "id": "lost-specifics",
      "desc": "Replaces the brand's specifics (farms, flavour notes, roast day) with generic claims"
    },
    {
      "id": "unsupported-finest",
      "desc": "'Finest farms' and 'very best' are unsupported superlatives"
    }
  ],
  "must_not_flag": [
    {
      "id": "invent-facts",
      "desc": "Must not invent farm names, tasting notes, or awards not in the profile"
    }
  ],
  "preserve": [],
  "polish_min_similarity": null,
  "brand": "dirt-road-coffee.md"
}
-->
## Kitchen Table Blend - Coffee Like You've NEVER Tasted Before!

Elevate your morning ritual with our premium, artisan-crafted Kitchen Table Blend! Sourced from the finest farms in Colombia, this exquisite medium roast delivers a symphony of rich, bold flavors that will awaken your senses!

Perfect for coffee lovers who demand the very best. Order now and experience the difference!
