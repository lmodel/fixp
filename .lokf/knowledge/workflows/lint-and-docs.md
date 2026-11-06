---
type: Service
id: https://w3id.org/lmodel/fixp/knowledge/workflows/lint-and-docs
genre: reference
title: Lint and docs (lint-and-docs.yaml)
description: "The static checks on pull requests and on `main`: ShellCheck, actionlint, the governance files' word budgets, markdownlint, lychee and codespell."
resource: .github/workflows/lint-and-docs.yaml
sources:
  - id: contributing.md
    resource: CONTRIBUTING.md
    title: Before opening a pull request
  - resource: .github/workflows/lint-and-docs.yaml
generated:
  by: process:ktl-librarian
  at: "2026-11-06T08:48:23Z"
status: draft
---

# Lint and docs (lint-and-docs.yaml)

`CONTRIBUTING.md` names what the workflow runs, and the workflow holds `SECURITY.md` and `CONTRIBUTING.md` to their word budgets.[^contributing.md]

[^contributing.md]: CONTRIBUTING.md, Before opening a pull request
