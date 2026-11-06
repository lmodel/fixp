---
type: Dataset
id: https://w3id.org/lmodel/fixp/knowledge/datasets/fixp-linkml-schema
genre: reference
title: The fixp LinkML schema
description: The umbrella schema `src/fixp/schema/fixp.yaml`, which imports the core, messages, exchange and engagement modules and is the file the project names. It pins FIXP 1.0 at the tag `v1.0-STANDARD`.
resource: src/fixp/schema/fixp.yaml
hasPart:
  - https://w3id.org/lmodel/fixp/knowledge/datasets/core-module
  - https://w3id.org/lmodel/fixp/knowledge/datasets/messages-module
  - https://w3id.org/lmodel/fixp/knowledge/datasets/exchange-module
  - https://w3id.org/lmodel/fixp/knowledge/datasets/engagement-module
derivedFrom:
  - https://w3id.org/lmodel/fixp/knowledge/references/fixp-specification
sources:
  - id: schema
    resource: src/fixp/schema/fixp.yaml
    title: the header
  - id: test_coverage.py
    resource: tests/test_coverage.py
    title: the module's description
generated:
  by: process:ktl-librarian
  at: "2026-11-06T07:38:52Z"
  revision: dd047e9f1966002a09d4983ab2b8a95f0fe99e58
status: draft
---

# The fixp LinkML schema

The header pins FIXP 1.0 at the tag `v1.0-STANDARD`, commit `6d89f5f`. It also names the SBE schema's package, `FIXP`, its id, 2748, its version, 0, and its byte order, `littleEndian`.[^schema]

An exchange starts at `FixpExchange`, the tree root. A single message validates against its own class, and a rules-of-engagement record against `FixpRulesOfEngagement`.[^schema]

A test holds every message, field, number, type, value and presence to the three resource files in `upstream/`.[^test_coverage.py]

[^schema]: src/fixp/schema/fixp.yaml, the header
[^test_coverage.py]: tests/test_coverage.py, the module's description
