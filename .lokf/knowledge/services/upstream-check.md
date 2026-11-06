---
type: Service
id: https://w3id.org/lmodel/fixp/knowledge/services/upstream-check
genre: reference
title: The upstream check
description: "`scripts/check_upstream_release.py`: lists FIX's FIXP repository through GitHub's API and reports a new tag or edition folder, a moved tag, a changed or missing pinned file, or a changed licence."
resource: scripts/check_upstream_release.py
about:
  - https://w3id.org/lmodel/fixp/knowledge/references/fixp-specification
sources:
  - id: check
    resource: scripts/check_upstream_release.py
    title: the module's description
  - resource: tests/test_watch.py
generated:
  by: process:ktl-librarian
  at: "2026-11-06T07:38:52Z"
  revision: 8fe9853aa70678997c59d582ad8098a43baf2acb
status: draft
---

# The upstream check

The script compares git object hashes and downloads no file. It reads nothing from fixtrading.org, whose terms bar automated copying, and exits 1 on any finding.[^check]

[^check]: scripts/check_upstream_release.py, the module's description
