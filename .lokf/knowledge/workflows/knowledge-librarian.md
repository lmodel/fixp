---
type: Service
id: https://w3id.org/lmodel/fixp/knowledge/workflows/knowledge-librarian
genre: reference
title: Knowledge librarian (knowledge-librarian.yaml)
description: The sidecar's scheduled agent run that keeps the bundle in step with the repository. It stays inert until `KNOWLEDGE_LIBRARIAN_ENABLED` is `true`, and a person merges what it proposes.
resource: .github/workflows/knowledge-librarian.yaml
sources:
  - id: security.md
    resource: SECURITY.md
    title: What executes here
generated:
  by: process:ktl-librarian
  at: "2026-11-06T07:38:52Z"
  revision: 02ca5bbd4a6a7d5343827f52b26fbbdcba94254b
status: draft
---

# Knowledge librarian (knowledge-librarian.yaml)

The agent's job holds no write token. The `publish` job runs no agent, confines the patch to the bundle and refuses a `human:` claim, and a person merges the pull request.[^security.md]

[^security.md]: SECURITY.md, What executes here
