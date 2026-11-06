---
type: Dataset
id: https://w3id.org/lmodel/fixp/knowledge/datasets/example-data
genre: reference
title: The example data
description: "`tests/data/`: a valid example of every class, four whole exchanges, and a counter-example per constraint, named `ClassName-suffix.yaml`, each counter-example naming where it fails on its first line."
resource: tests/data
about:
  - https://w3id.org/lmodel/fixp/knowledge/datasets/fixp-linkml-schema
sources:
  - id: contributing.md
    resource: CONTRIBUTING.md
    title: Before opening a pull request
  - id: test_data.py
    resource: tests/test_data.py
    title: test_every_concrete_class_has_an_example
generated:
  by: process:ktl-librarian
  at: "2026-11-06T08:48:23Z"
status: draft
---

# The example data

A counter-example's first line, `# Fails at: <pointer>`, names where it fails.[^contributing.md]

Every class a record can hold has a valid example.[^test_data.py]

The four exchanges are a session with both flows recoverable, an idempotent client flow, a multicast, and a session on a shared transport. `tests/test_rules.py` breaks each rule of `tests/fixp_rules.py` in one of them.

[^contributing.md]: CONTRIBUTING.md, Before opening a pull request
[^test_data.py]: tests/test_data.py, test_every_concrete_class_has_an_example
