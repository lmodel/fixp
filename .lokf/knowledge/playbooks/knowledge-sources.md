---
type: Playbook
id: https://w3id.org/lmodel/fixp/knowledge/playbooks/knowledge-sources
genre: reference
title: Knowledge sources map
description: "The librarian's scrape map: every repository location and external source this bundle derives concepts from, how to re-check each, and the tracked paths left out with their reasons."
resource: .
references:
  - https://w3id.org/lmodel/fixp/knowledge/datasets/fixp-linkml-schema
  - https://w3id.org/lmodel/fixp/knowledge/references/fixp-specification
exclusions:
  - resource: .github/ISSUE_TEMPLATE
    reason: Issue forms, which are governance text and state nothing about the schema.
  - resource: .github/pull_request_template.md
    reason: The pull request checklist, which repeats CONTRIBUTING.md.
  - resource: .github/PULL_REQUEST_TEMPLATE
    reason: The sidecar sync's pull request template.
  - resource: CODE_OF_CONDUCT.md
    reason: The Contributor Covenant, governance text with nothing about the schema.
  - resource: uv.lock
    reason: The package's lock file, tooling that pins versions.
  - resource: .gitignore
    reason: "Tooling: the files git ignores."
  - resource: .editorconfig
    reason: "Tooling: editor settings."
  - resource: .yamllint.yaml
    reason: "Tooling: the YAML linter's settings."
  - resource: .pre-commit-config.yaml
    reason: "Tooling: the hooks and the files they leave alone."
  - resource: .markdownlint-cli2.jsonc
    reason: "Tooling: the Markdown linter's settings."
  - resource: lychee.toml
    reason: "Tooling: the link checker's settings."
  - resource: config.public.mk
    reason: "Tooling: the variables the justfile loads."
  - resource: .copier-answers.yml
    reason: The copier template's answers, which `just update` reads.
  - resource: src/README.md
    reason: Text from the project template.
  - resource: src/fixp/schema/README.md
    reason: Text from the project template.
  - resource: examples/README.md
    reason: Text from the project template.
  - resource: docs/templates-linkml
    reason: The template's placeholders for gen-doc, not pages.
  - resource: docs/elements
    reason: Generated pages that git ignores, apart from a placeholder.
  - resource: src/fixp/__init__.py
    reason: Package plumbing.
  - resource: src/fixp/_version.py
    reason: Package plumbing.
  - resource: llms.txt
    reason: The pointer that sends agents to this bundle.
  - resource: knowledge_bundle
    reason: The sidecar's link to the bundle.
  - resource: .lokf/lokf.yaml
    reason: LOKF's schema, pinned by the sidecar.
  - resource: .lokf/scripts
    reason: The sidecar's scripts, which the weekly sync replaces.
  - resource: .lokf/m365
    reason: The sidecar's Copilot skill builder and its instructions.
  - resource: .lokf/README.md
    reason: The sidecar's own README.
  - resource: .lokf/queries.http
    reason: The sidecar's sample queries.
  - resource: .lokf/ingest.yaml.sample
    reason: The sidecar's unused example; this host has no outside sources.
  - resource: .lokf/uv.lock
    reason: The sidecar's lock file, tooling that pins versions.
  - resource: .lokf/.gitignore
    reason: "Tooling: what the sidecar keeps out of git."
  - resource: .lokf/.gitattributes
    reason: "Tooling: line endings in the bundle."
sources:
  - resource: README.md
  - resource: docs/about.md
  - resource: docs/index.md
  - resource: src/fixp/schema
  - resource: src/fixp/datamodel
  - resource: project.justfile
  - resource: .lokf/fixp.yaml
  - resource: .lokf/justfile
  - resource: .lokf/pyproject.toml
  - resource: NOTICE
  - resource: LICENSE
  - resource: scripts
  - resource: .github/scripts
  - resource: .github/workflows
  - resource: .github/dependabot.yml
  - resource: .github/release
  - resource: justfile
  - resource: .linkml/generators.yaml
  - resource: .linkmllint.yaml
  - resource: project
  - resource: docs/schema
  - resource: tests
  - resource: upstream
  - resource: CONTRIBUTING.md
  - resource: .releaserc.json
  - resource: CHANGELOG.md
  - resource: website
  - resource: SECURITY.md
  - resource: AI_COVENANT.md
  - resource: pyproject.toml
generated:
  by: process:ktl-librarian
  at: "2026-11-06T07:38:52Z"
  revision: aa85c33978c9c71f0ce3ed3a8a835590423eea41
status: draft
---

# Knowledge sources map

The bundle derives its concepts from the paths under `sources`, each re-read when `knowledge-report.sh worklist` says it changed. Paths under `exclusions` were looked at and left out, each with its reason.

| Source | Yields | Re-check |
| --- | --- | --- |
| `src/fixp/schema/` | the schema and module datasets, the explanations, the glossary | read the file; `just lint` and `just test` |
| `upstream/` | the copy of the upstream and the references | `tests/test_upstream.py`; the watch |
| `tests/` | the example data, the departures, the neighbour copies and the rules | `just test` |
| `scripts/` | the upstream check | its tests |
| `docs/`, `README.md`, `CHANGELOG.md` | the explanations and the playbooks | read the page |
| `NOTICE`, `SECURITY.md`, `AI_COVENANT.md` | the policies | read the file |
| `.github/workflows/`, `justfile`, `project.justfile` | the workflows and the playbooks | read the file |
| `https://github.com/FIXTradingCommunity/fixp-specification`, `https://github.com/lmodel/fix-sbe`, `https://github.com/lmodel/fix-orchestra` | the references | the watch, for the first |
