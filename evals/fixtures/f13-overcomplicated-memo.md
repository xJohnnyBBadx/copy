<!-- fixture
{
  "id": "f13-overcomplicated-memo",
  "category": "overcomplicated",
  "profile": "6",
  "commands": [
    "critique",
    "polish"
  ],
  "brief": "Internal email from leadership to the whole sales organization (about 300 people). The consolidation eliminates some roles.",
  "expect_verdict": [
    "Rethink",
    "Revise"
  ],
  "must_flag": [
    {
      "id": "euphemism",
      "desc": "'Certain roles will be impacted' hides that people are losing jobs; misleading to the affected readers"
    },
    {
      "id": "buried-news",
      "desc": "The news is buried under a 60-word preamble"
    },
    {
      "id": "hidden-actor",
      "desc": "'A decision has been made' hides who decided; unsigned 'Leadership Team'"
    },
    {
      "id": "jargon",
      "desc": "Jargon: operational excellence, cross-functional synergies, dynamic environment, journey"
    }
  ],
  "must_not_flag": [
    {
      "id": "invent-numbers",
      "desc": "Must not invent how many roles are affected or severance terms; use placeholders"
    }
  ],
  "preserve": [],
  "polish_min_similarity": null,
  "brand": null
}
-->
Subject: Organizational Alignment Update

Team,

As part of our ongoing commitment to operational excellence and in alignment with our strategic priorities for FY27, we have undertaken a comprehensive review of our go-to-market organizational structure with the objective of optimizing cross-functional synergies and enhancing our ability to deliver value to our customers in an increasingly dynamic environment.

Following this review, a decision has been made to consolidate the Regional Sales Operations function into the Central Revenue Operations team, effective March 1. As a result of this transition, certain roles will be impacted, and affected team members will be contacted directly by their HR business partner in the coming days to discuss next steps and available support resources.

We recognize that change can be challenging, and we remain committed to supporting our people throughout this journey.

Best regards,
Leadership Team
