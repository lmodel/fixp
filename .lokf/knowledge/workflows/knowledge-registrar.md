---
type: Service
id: https://w3id.org/lmodel/fixp/knowledge/workflows/knowledge-registrar
genre: reference
title: Knowledge registrar (knowledge-registrar.yaml)
description: "The gate on the bundle: it validates the bundle on each pull request that touches it, and checks who vouched for what."
resource: .github/workflows/knowledge-registrar.yaml
sources:
  - id: contributing.md
    resource: CONTRIBUTING.md
    title: Before opening a pull request
generated:
  by: process:ktl-librarian
  at: "2026-11-06T07:38:52Z"
  revision: 02ca5bbd4a6a7d5343827f52b26fbbdcba94254b
status: draft
---

# Knowledge registrar (knowledge-registrar.yaml)

The workflow runs on any pull request that touches `.lokf/`.[^contributing.md]

[^contributing.md]: CONTRIBUTING.md, Before opening a pull request
