<!-- fixture
{
  "id": "f03-generic-launch-email",
  "category": "generic-ai",
  "profile": "8",
  "commands": [
    "critique",
    "humanize"
  ],
  "brief": "Launch email to existing customers of Pulse, a data dashboard tool. The 2.0 release adds Salesforce and HubSpot connectors, scheduled PDF reports, and a redesigned chart editor.",
  "expect_verdict": [
    "Revise",
    "Rethink"
  ],
  "must_flag": [
    {
      "id": "vague-whats-new",
      "desc": "Doesn't say what actually changed (the brief names Salesforce/HubSpot connectors, scheduled PDF reports, chart editor); bullets are generic"
    },
    {
      "id": "puffery",
      "desc": "Puffery and inflated significance: game-changer, revolutionize, marks a significant milestone, next-generation"
    },
    {
      "id": "no-reader-benefit",
      "desc": "No consequence for the customer / no clear next step"
    }
  ],
  "must_not_flag": [
    {
      "id": "invent-features",
      "desc": "Must not invent features beyond those in the brief"
    }
  ],
  "preserve": [],
  "polish_min_similarity": null,
  "brand": null
}
-->
Subject: Introducing Pulse 2.0 - A Game-Changer for Your Workflow

Hi there,

We're thrilled to announce the launch of Pulse 2.0, our most powerful release yet! This update marks a significant milestone in our journey to revolutionize how teams manage their data.

With Pulse 2.0, you can now:
- Seamlessly integrate with your favorite tools
- Unlock deeper insights with our next-generation analytics engine
- Enjoy a sleek, intuitive new interface

Pulse 2.0 isn't just an update. It's a whole new experience. We can't wait for you to try it.

As always, we'd love to hear your feedback. Feel free to reach out with any questions!

Best,
The Pulse Team
