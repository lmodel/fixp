---
type: Dataset
id: https://w3id.org/lmodel/fixp/knowledge/datasets/upstream-copy
genre: reference
title: The copy of the upstream
description: "`upstream/`: FIXP 1.0's SBE schema, FIX repository file and Orchestra file, with the repository's CC BY-ND 4.0 licence, unchanged and pinned by git object hash in `scripts/upstream_pins.tsv`."
resource: upstream
derivedFrom:
  - https://w3id.org/lmodel/fixp/knowledge/references/fixp-specification
sources:
  - id: notice
    resource: NOTICE
    title: FIX Performance Session Layer
  - id: test_upstream.py
    resource: tests/test_upstream.py
    title: test_upstream_holds_only_the_pinned_files
  - resource: scripts/upstream_pins.tsv
generated:
  by: process:ktl-librarian
  at: "2026-11-06T08:48:23Z"
status: draft
---

# The copy of the upstream

The files are copied whole and unchanged from the tag `v1.0-STANDARD`, commit `6d89f5f`. They are outside this repository's Apache License.[^notice]

The folder holds exactly the pinned files, four of them, and each matches its pinned hash.[^test_upstream.py]

[^notice]: NOTICE, FIX Performance Session Layer
[^test_upstream.py]: tests/test_upstream.py, test_upstream_holds_only_the_pinned_files
