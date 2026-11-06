---
type: Dataset
id: https://w3id.org/lmodel/fixp/knowledge/datasets/upstream-departures
genre: reference
title: The departures from FIX's files
description: "`tests/upstream_departures.yaml`: each place the schema differs from a resource file, with its reason, such as Topic's keep-alive interval and Context's next sequence number, and the note that the Orchestra file is not well-formed."
resource: tests/upstream_departures.yaml
about:
  - https://w3id.org/lmodel/fixp/knowledge/datasets/upstream-copy
sources:
  - id: departures
    resource: tests/upstream_departures.yaml
    title: the header
  - id: test_coverage.py
    resource: tests/test_coverage.py
    title: test_every_departure_is_still_needed
generated:
  by: process:ktl-librarian
  at: "2026-11-06T07:38:52Z"
  revision: 2999f6dae0835ad3618643d5af37aeb959d150b9
status: draft
---

# The departures from FIX's files

The coverage test skips exactly the differences the file lists, and fails when one is no longer there, so a mended file is noticed.[^departures]

Each departure in the list names a field that the files do state otherwise.[^test_coverage.py]

[^departures]: tests/upstream_departures.yaml, the header
[^test_coverage.py]: tests/test_coverage.py, test_every_departure_is_still_needed
