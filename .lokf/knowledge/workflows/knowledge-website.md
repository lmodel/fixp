---
type: Service
id: https://w3id.org/lmodel/fixp/knowledge/workflows/knowledge-website
genre: reference
title: Knowledge website (knowledge-website.yaml)
description: The workflow that builds `website/` on each pull request that touches its inputs, and deploys it from `main` once `KNOWLEDGE_WEBSITE_ENABLED` is `true`.
resource: .github/workflows/knowledge-website.yaml
sources:
  - id: security.md
    resource: SECURITY.md
    title: What executes here
references:
  - https://w3id.org/lmodel/fixp/knowledge/services/documentation-site
generated:
  by: process:ktl-librarian
  at: "2026-11-06T08:48:23Z"
status: draft
---

# Knowledge website (knowledge-website.yaml)

The workflow builds without a write token. Only its deploy job holds `pages: write` and `id-token: write`, and it runs only from `main`.[^security.md]

[^security.md]: SECURITY.md, What executes here
