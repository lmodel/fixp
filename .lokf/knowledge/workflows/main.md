---
type: Service
id: https://w3id.org/lmodel/fixp/knowledge/workflows/main
genre: reference
title: Build and test (main.yaml)
description: "The Build and test workflow: on every pull request and push to `main`, it runs `just test` on Python 3.10 to 3.14, and lints the schema and checks the adapt copy on 3.13."
resource: .github/workflows/main.yaml
sources:
  - id: main.yaml
    resource: .github/workflows/main.yaml
references:
  - https://w3id.org/lmodel/fixp/knowledge/playbooks/regenerate-and-test
generated:
  by: process:ktl-librarian
  at: "2026-11-06T08:48:23Z"
status: draft
---

# Build and test (main.yaml)

The `test` job runs on Python 3.10 to 3.14. It installs with `uv sync --locked`, and runs `just test`. On Python 3.13 it also runs `just lint` and `just lokf-adapt-check`.[^main.yaml]

[^main.yaml]: .github/workflows/main.yaml
