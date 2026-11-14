<!-- fixture
{
  "id": "f08-technical-unpersuasive-landing",
  "category": "technical-unpersuasive",
  "profile": "3",
  "commands": [
    "critique"
  ],
  "brief": "Landing page for Vaultline, a server backup product. Reader: IT managers at 200-2,000 person companies, most of whom have had a restore fail when they needed it.",
  "expect_verdict": [
    "Revise",
    "Rethink"
  ],
  "must_flag": [
    {
      "id": "buried-differentiator",
      "desc": "The real differentiator (automated nightly restore verification) is buried mid-list"
    },
    {
      "id": "features-no-consequence",
      "desc": "Features listed without consequences for the reader (so-what)"
    },
    {
      "id": "no-problem",
      "desc": "Opens with a spec sentence; doesn't name the reader's problem (restores that fail)"
    }
  ],
  "must_not_flag": [
    {
      "id": "dumb-down",
      "desc": "Must not ask to remove or simplify technical terms (block-level, PXE, RBAC, SAML) for this IT audience"
    },
    {
      "id": "invent-proof",
      "desc": "Must not invent customer counts, restore-success statistics, or testimonials"
    }
  ],
  "preserve": [],
  "polish_min_similarity": null,
  "brand": null
}
-->
# Vaultline

Vaultline is a block-level incremental backup agent for Linux and Windows servers with AES-256 encryption at rest, TLS 1.3 in transit, configurable retention policies, and support for S3-compatible object storage.

## Features

- Block-level deduplication
- Incremental-forever backup chains with synthetic fulls
- Bare-metal restore via PXE boot
- Automated nightly restore verification (boots each backup in a sandbox and checks that services start)
- Application-consistent snapshots for PostgreSQL, MySQL and SQL Server
- RBAC with SAML 2.0 SSO
- Prometheus metrics endpoint
- CLI and REST API

## Pricing

$12 per protected server per month. Volume discounts available.

[Start trial]
