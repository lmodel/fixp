---
type: Service
id: https://w3id.org/lmodel/fixp/knowledge/workflows/semantic-release
genre: reference
title: Semantic release (semantic-release.yml)
description: The workflow that computes the next version from Conventional Commits on `main`, promotes the changelog, tags and publishes the GitHub Release, and dispatches the knowledge release.
resource: .github/workflows/semantic-release.yml
sources:
  - id: security.md
    resource: SECURITY.md
    title: What executes here
  - resource: .releaserc.json
  - resource: .github/release
  - resource: .github/scripts/changelog-release.mjs
references:
  - https://w3id.org/lmodel/fixp/knowledge/playbooks/release
generated:
  by: process:ktl-librarian
  at: "2026-11-06T07:38:52Z"
  revision: 3e7087cbcf1f1e5140bc509800888c2bf3a3347d
status: draft
---

# Semantic release (semantic-release.yml)

The workflow runs on a push to `main`, in the `release` Environment, and installs its pinned tools with `--ignore-scripts`.[^security.md]

[^security.md]: SECURITY.md, What executes here
