---
type: Service
id: https://w3id.org/lmodel/fixp/knowledge/workflows/knowledge-release
genre: reference
title: Knowledge release (knowledge-release.yaml)
description: The workflow that attaches the bundle, a Copilot skill and the schema's adapt copy to a GitHub release, each with its `.sha256` and an attestation, when the bundle or the schema changed.
resource: .github/workflows/knowledge-release.yaml
sources:
  - id: security.md
    resource: SECURITY.md
    title: What this repository releases and What executes here
references:
  - https://w3id.org/lmodel/fixp/knowledge/datasets/adapt-copy
generated:
  by: process:ktl-librarian
  at: "2026-11-06T07:38:52Z"
  revision: 02ca5bbd4a6a7d5343827f52b26fbbdcba94254b
status: draft
---

# Knowledge release (knowledge-release.yaml)

The workflow does nothing until it is dispatched, and only its `attach` job, which runs no third-party packages, can write.[^security.md]

[^security.md]: SECURITY.md, What this repository releases and What executes here
