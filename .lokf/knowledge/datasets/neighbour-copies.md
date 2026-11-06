---
type: Dataset
id: https://w3id.org/lmodel/fixp/knowledge/datasets/neighbour-copies
genre: reference
title: The neighbours' copies
description: "`tests/neighbours/`: the adapt copies other lmodel repositories release, each the release's schema asset, which tests use to hold this copy's names apart from theirs, fix-sbe's, fix-orchestra's and fix-protocol's among them."
resource: tests/neighbours
references:
  - https://w3id.org/lmodel/fixp/knowledge/datasets/adapt-copy
sources:
  - id: test_schema_rules.py
    resource: tests/test_schema_rules.py
    title: NEIGHBOURS
generated:
  by: process:ktl-librarian
  at: "2026-11-06T08:52:39Z"
status: draft
---

# The neighbours' copies

Each copy is pinned by its SHA-256 checksum. No neighbour declares a class, enum, type or subset of this copy, and a key the copy shares with a neighbour has the same IRI in both.[^test_schema_rules.py]

lmodel/fix-orchestra, fix-sbe and fix-protocol joined the pinned list at their v0.1.0 releases.[^test_schema_rules.py]

[^test_schema_rules.py]: tests/test_schema_rules.py, NEIGHBOURS
