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
  at: "2026-11-06T08:48:23Z"
status: draft
---

# Upstream watch (upstream-watch.yaml)

A failing check fails the run and opens an issue, or comments on the one already open.[^watch]

[^watch]: .github/workflows/upstream-watch.yaml, the header
