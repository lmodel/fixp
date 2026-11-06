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
  at: "2026-11-06T08:48:23Z"
status: draft
---

# Knowledge registrar (knowledge-registrar.yaml)

The workflow runs on any pull request that touches `.lokf/`.[^contributing.md]

[^contributing.md]: CONTRIBUTING.md, Before opening a pull request
