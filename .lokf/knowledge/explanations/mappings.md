---
type: Explanation
id: https://w3id.org/lmodel/fixp/knowledge/explanations/mappings
genre: explanation
title: Mappings
description: Why `FixpMessage` is only related to lmodel/fix-sbe's `SbeMessageV1` and lmodel/fix-orchestra's `OrchestraMessageV10`, and why the SBE and FIX datatype names are checked against fix-sbe's lists. The five SSSOM sets are gone.
about:
  - https://w3id.org/lmodel/fixp/knowledge/datasets/fixp-linkml-schema
references:
  - https://w3id.org/lmodel/fixp/knowledge/references/lmodel-fix-sbe
  - https://w3id.org/lmodel/fixp/knowledge/references/lmodel-fix-orchestra
sources:
  - id: about.md
    resource: docs/about.md
    title: Mappings
  - id: readme.md
    resource: README.md
    title: Mappings
  - resource: tests/test_mappings.py
generated:
  by: process:ktl-librarian
  at: "2026-11-06T07:38:52Z"
  revision: f07e8ed1bf536329aad51980ead6c19e04420365
status: draft
---

# Mappings

A record of `SbeMessageV1` or `OrchestraMessageV10` defines a kind of message, while an instance of `FixpMessage` is one message, so neither mapping is close.[^about.md]

The five SSSOM sets are gone: their rows were the project's guesses, not FIX's statements.[^readme.md]

[^about.md]: docs/about.md, Mappings
[^readme.md]: README.md, Mappings
