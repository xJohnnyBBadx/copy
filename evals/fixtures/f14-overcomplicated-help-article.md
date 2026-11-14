<!-- fixture
{
  "id": "f14-overcomplicated-help-article",
  "category": "overcomplicated",
  "profile": "12",
  "commands": [
    "critique"
  ],
  "brief": "Help-centre article for small-business owners (not technical) who asked 'Why did my invoice email go to spam?'",
  "expect_verdict": [
    "Revise",
    "Rethink"
  ],
  "must_flag": [
    {
      "id": "reader-mismatch",
      "desc": "Written for email engineers, not small-business owners; terms undefined"
    },
    {
      "id": "no-steps",
      "desc": "The fix is buried in a sentence instead of numbered steps"
    },
    {
      "id": "title",
      "desc": "Title doesn't match the reader's question/task"
    }
  ],
  "must_not_flag": [
    {
      "id": "drop-accuracy",
      "desc": "Must not recommend removing the technical cause entirely; the fix should explain it plainly, not delete it"
    }
  ],
  "preserve": [],
  "polish_min_similarity": null,
  "brand": null
}
-->
# Email Deliverability Considerations for Outbound Invoice Transmission

Invoice emails are transmitted via our MTA infrastructure utilizing a shared IP pool, the reputation of which is determined by aggregate sender behavior. Recipient mail servers perform SPF, DKIM, and DMARC alignment verification; in the event that the sending domain's DNS records do not authorize our infrastructure, messages may be subject to heuristic filtering resulting in junk-folder placement. Users are advised to configure custom domain authentication via the Settings > Email > Domain panel, wherein CNAME records are generated for publication at the user's DNS provider.
