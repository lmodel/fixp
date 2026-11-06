---
type: Playbook
id: https://w3id.org/lmodel/fixp/knowledge/playbooks/update-upstream-pins
genre: how-to
title: Update the upstream pins
description: "What to do when the watch reports a change in FIX's FIXP repository: read what changed, replace `upstream/`, the pins and the headers together, and let the coverage test show what the schema must follow."
references:
  - https://w3id.org/lmodel/fixp/knowledge/services/upstream-check
  - https://w3id.org/lmodel/fixp/knowledge/datasets/upstream-copy
sources:
  - id: check
    resource: scripts/check_upstream_release.py
    title: the pins
  - id: test_coverage.py
    resource: tests/test_coverage.py
    title: the module's description
generated:
  by: process:ktl-librarian
  at: "2026-11-06T08:48:23Z"
status: draft
---

# Update the upstream pins

The watch names the new tag, the new edition folder, the moved tag or the changed file.[^check]

To move to another edition:

1. Replace the files under `upstream/`, and rewrite `scripts/upstream_pins.tsv` with their git object hashes.
2. Move the constants at the top of `scripts/check_upstream_release.py`, and the schema headers with them.[^check]
3. Run `tests/test_coverage.py`, which names each message, field, number, type, value and presence that differs from the new files.[^test_coverage.py]
4. Update the schema and `tests/upstream_departures.yaml`, then run the rest of the tests.

[^check]: scripts/check_upstream_release.py, the pins
[^test_coverage.py]: tests/test_coverage.py, the module's description
