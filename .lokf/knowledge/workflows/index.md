# Workflows

* [Build and test (main.yaml)](main.md) - The Build and test workflow: on every pull request and push to `main`, it runs `just test` on Python 3.10 to 3.14, and lints the schema and checks the adapt copy on 3.13.
* [Lint and docs (lint-and-docs.yaml)](lint-and-docs.md) - The static checks on pull requests and on `main`: ShellCheck, actionlint, the governance files' word budgets, markdownlint, lychee and codespell.
* [Semantic release (semantic-release.yml)](semantic-release.md) - The workflow that computes the next version from Conventional Commits on `main`, promotes the changelog, tags and publishes the GitHub Release, and dispatches the knowledge release.
* [Knowledge registrar (knowledge-registrar.yaml)](knowledge-registrar.md) - The gate on the bundle: it validates the bundle on each pull request that touches it, and checks who vouched for what.
* [Knowledge librarian (knowledge-librarian.yaml)](knowledge-librarian.md) - The sidecar's scheduled agent run that keeps the bundle in step with the repository. It stays inert until `KNOWLEDGE_LIBRARIAN_ENABLED` is `true`, and a person merges what it proposes.
* [Knowledge release (knowledge-release.yaml)](knowledge-release.md) - The workflow that attaches the bundle, a Copilot skill and the schema's adapt copy to a GitHub release, each with its `.sha256` and an attestation, when the bundle or the schema changed.
* [Knowledge sync (knowledge-sync.yaml)](knowledge-sync.md) - The weekly workflow that keeps the sidecar's copies and the skills pin at the newest release of Knowledge Trust Ladder, by a pull request a person merges.
* [Knowledge website (knowledge-website.yaml)](knowledge-website.md) - The workflow that builds `website/` on each pull request that touches its inputs, and deploys it from `main` once `KNOWLEDGE_WEBSITE_ENABLED` is `true`.
* [Upstream watch (upstream-watch.yaml)](upstream-watch.md) - The weekly check that `scripts/check_upstream_release.py` runs: a new tag or edition folder of FIXP, a moved tag, a changed or missing pinned file, or a changed licence opens or updates an issue.
