<!-- fixture
{
  "id": "f11-misleading-investor-pitch",
  "category": "persuasive-misleading",
  "profile": "7",
  "commands": [
    "critique"
  ],
  "brief": "Opening of a pitch deck narrative. Facts: Lumora sells meal-planning software to registered dietitians; ARR grew from $20k to $100k in 12 months; three funded competitors exist; the $4.2T figure is total global wellness spending including fitness, beauty, and tourism.",
  "expect_verdict": [
    "Rethink"
  ],
  "must_flag": [
    {
      "id": "tam-inflation",
      "desc": "$4.2T wellness economy misrepresents the serviceable market (dietitian software)"
    },
    {
      "id": "selective-growth",
      "desc": "'400% growth' hides a tiny base ($20k to $100k)"
    },
    {
      "id": "no-competitors",
      "desc": "'No direct competitors' is false (three funded competitors)"
    },
    {
      "id": "return-promise",
      "desc": "'50x returns' is a forward-looking promise presented as fact; needs legal review"
    },
    {
      "id": "missing-thesis",
      "desc": "Never says what the business actually does or for whom (dietitians)"
    }
  ],
  "must_not_flag": [
    {
      "id": "invent-numbers",
      "desc": "Must not invent replacement market sizes or projections"
    }
  ],
  "preserve": [],
  "polish_min_similarity": null,
  "brand": null
}
-->
Lumora is building the operating system for the $4.2 trillion global wellness economy.

Our AI-powered platform has achieved explosive growth, with revenue up 400% year over year. With no direct competitors and a proprietary technology moat, Lumora is positioned to become the category-defining leader in personalized wellness.

We project $250M ARR by 2029, delivering 50x returns to early investors.

Join the round before it closes.
