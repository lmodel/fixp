---
type: Playbook
id: https://w3id.org/lmodel/fixp/knowledge/playbooks/release
genre: how-to
title: Cut a release
description: "How a release happens: write `## [Unreleased]`, merge with a releasing commit type, and `semantic-release.yml` tags, writes the changelog and dispatches the knowledge release, which attaches the assets."
references:
  - https://w3id.org/lmodel/fixp/knowledge/workflows/semantic-release
  - https://w3id.org/lmodel/fixp/knowledge/workflows/knowledge-release
sources:
  - id: contributing.md
    resource: CONTRIBUTING.md
    title: Releasing (maintainers)
generated:
  by: process:ktl-librarian
  at: "2026-11-06T08:48:23Z"
status: draft
---

# Cut a release

1. Write `## [Unreleased]` in `CHANGELOG.md` as you go. The release job refuses an empty one.[^contributing.md]
2. Type the commit for what the change is. Only `feat:`, `fix:`, `security:` and a breaking `!` start a release.[^contributing.md]
3. On merge, `semantic-release.yml` retitles the section, commits `CHANGELOG.md`, tags `vX.Y.Z` and publishes the GitHub Release.[^contributing.md]
4. Once `KNOWLEDGE_RELEASE_ENABLED` is `true`, it dispatches `knowledge-release.yaml`, which attaches the schema copy and the bundle when either changed.[^contributing.md]

[^contributing.md]: CONTRIBUTING.md, Releasing (maintainers)
