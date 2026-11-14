<!-- fixture
{
  "id": "f12-misleading-green-claims",
  "category": "persuasive-misleading",
  "profile": "8",
  "commands": [
    "critique"
  ],
  "brief": "Packaging and product-page copy for a reusable water bottle. Facts: bottles are 30% recycled ocean-bound plastic and 70% virgin PET; 'carbon neutral' is based on purchased offsets with no third-party certification.",
  "expect_verdict": [
    "Rethink"
  ],
  "must_flag": [
    {
      "id": "eco-friendly",
      "desc": "'100% eco-friendly' is vague and unsupportable"
    },
    {
      "id": "ocean-plastic",
      "desc": "'Made from ocean-bound plastic' misleads (only 30%)"
    },
    {
      "id": "carbon-neutral",
      "desc": "'Completely carbon neutral' via uncertified offsets is a regulated environmental claim; flag for legal review"
    },
    {
      "id": "saving-oceans",
      "desc": "'Saving the oceans' overclaims impact"
    }
  ],
  "must_not_flag": [
    {
      "id": "kill-warmth",
      "desc": "Must not treat the warm, playful tone itself as the problem"
    }
  ],
  "preserve": [],
  "polish_min_similarity": null,
  "brand": null
}
-->
Meet the bottle that loves the planet back.

Every Tidewell bottle is 100% eco-friendly, made from ocean-bound plastic and completely carbon neutral. When you choose Tidewell, you're not just staying hydrated. You're saving the oceans, one sip at a time.
