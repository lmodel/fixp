---
type: Playbook
id: https://w3id.org/lmodel/fixp/knowledge/playbooks/regenerate-and-test
genre: how-to
title: Regenerate and test
description: "How to change the schema: edit a module under `src/fixp/schema/`, run `just lint`, `just gen-project`, `just gen-doc`, `just lokf-adapt` and `just test`, and commit what they write."
references:
  - https://w3id.org/lmodel/fixp/knowledge/datasets/generated-artefacts
sources:
  - id: contributing.md
    resource: CONTRIBUTING.md
    title: Before opening a pull request
  - id: justfile
    resource: justfile
    title: the test recipe
  - id: main.yaml
    resource: .github/workflows/main.yaml
    title: the lint step
generated:
  by: process:ktl-librarian
  at: "2026-11-06T08:48:23Z"
status: draft
---

# Regenerate and test

1. Edit a module under `src/fixp/schema/`.[^contributing.md]
2. Run `just lint`, `just gen-project`, `just gen-doc` and `just lokf-adapt`.[^contributing.md]
3. Run `just test`, which generates the schema into `tmp/`, runs `pytest`, and runs the example runner.[^justfile]
4. Commit the output. CI runs `just lint` and `just lokf-adapt-check` on Python 3.13, and `just test` on each version.[^main.yaml]

[^contributing.md]: CONTRIBUTING.md, Before opening a pull request
[^justfile]: justfile, the test recipe
[^main.yaml]: .github/workflows/main.yaml, the lint step
