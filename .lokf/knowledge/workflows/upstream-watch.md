---
type: Service
id: https://w3id.org/lmodel/fixp/knowledge/workflows/upstream-watch
genre: reference
title: Upstream watch (upstream-watch.yaml)
description: "The weekly check that `scripts/check_upstream_release.py` runs: a new tag or edition folder of FIXP, a moved tag, a changed or missing pinned file, or a changed licence opens or updates an issue."
resource: .github/workflows/upstream-watch.yaml
sources:
  - id: watch
    resource: .github/workflows/upstream-watch.yaml
    title: the header
  - resource: .github/scripts/report-issue.sh
references:
  - https://w3id.org/lmodel/fixp/knowledge/services/upstream-check
generated:
  by: process:ktl-librarian
  at: "2026-11-06T07:38:52Z"
  revision: 6e3a202185283b3534f6d81939d2f9d5b542d015
status: draft
---

# Upstream watch (upstream-watch.yaml)

A failing check fails the run and opens an issue, or comments on the one already open.[^watch]

[^watch]: .github/workflows/upstream-watch.yaml, the header
