# Contributing to fixp

*This file is a checklist, not a design log. Each rule is a line or two that links to where its reasoning lives. `lint-and-docs.yaml` holds it to a word budget.*

## What this project is

A LinkML schema of the FIX Performance Session Layer (FIXP) 1.0, the FIX Trading Community's session protocol: its messages, exchanges of them, and the rules of engagement two parties agree on.

| Path | Holds |
| --- | --- |
| `src/fixp/schema/` | The LinkML schema: the umbrella and its four modules. |
| `src/fixp/datamodel/`, `project/`, `docs/schema/` | Artefacts generated from the schema. |
| `upstream/` | FIXP 1.0's three resource files and their licence, unchanged. |
| `scripts/check_upstream_release.py`, `scripts/upstream_pins.tsv` | The weekly comparison with FIX's repository, and each file's hash. |
| `docs/` | The website's own pages. |
| `tests/` | Python tests and example data. |
| `.lokf/knowledge/` | This repository's knowledge bundle. |

## Development setup

You need Python 3.10+, [uv](https://docs.astral.sh/uv/) and [just](https://github.com/casey/just).

```bash
git clone https://github.com/lmodel/fixp.git
cd fixp
uv sync --group dev
just --list
```

### Agent skills (optional, only for this repo's `.lokf/` bundle)

The bundle is maintained with the Knowledge Trust Ladder (KTL) skills, **installed, never committed**. Continuous integration (CI) installs the librarian skill at run time, pinned to a release. [The install page](https://w3id.org/ktl/docs/install/) lists every route. With npm:

```bash
npx skills add noelmcloughlin/knowledge-trust-ladder --skill ktl-librarian --yes   # derive concepts
npx skills add noelmcloughlin/knowledge-trust-ladder --skill ktl-curator --yes     # confirm them as a person
```

## Before opening a pull request

- **Edit the schema, then regenerate.** Run `just gen-project`, `just gen-doc` and `just lokf-adapt`, and commit the output. `project/`, `src/fixp/datamodel/`, `docs/schema/` and `.lokf/fixp.yaml` are generated.
- **An element follows FIXP's files.** `tests/test_coverage.py` compares each message with the SBE schema, the repository file and the Orchestra file. A difference goes in `tests/upstream_departures.yaml`, with its reason.
- **A rule says where it comes from.** Each rule names the specification's section. What JSON Schema can hold goes in the schema, the rest in `tests/fixp_rules.py`, with a counter-example.
- **FIX's words stay FIX's.** Write every title, description and comment from what the element does. `tests/test_own_words.py` finds a run of four words shared with FIX's files. Set `FIXP_SPEC_DOCS` to a folder of the specification's chapters to check them too, since that text stays out of this repository.
- **A mapping names a sure match.** `tests/test_mappings.py` lists each one. A term with no sure match stays unmapped.
- **Model the pinned editions.** `tests/test_upstream.py` checks that the schema headers, `scripts/check_upstream_release.py` and `upstream/` agree.
- **Keep names apart.** A host imports this adapt copy beside the Linked Open Knowledge Format (LOKF) schema and the released copies in `tests/neighbours/`. `tests/test_schema_rules.py` checks this.
- **Run the tests**: `just test` (schema generation, `pytest` and the examples under `tests/data/`). Example data goes in `tests/data/valid/` and `tests/data/invalid/`, named `ClassName-suffix.yaml`; an invalid example's first line, `# Fails at: <pointer>`, names where it fails.
- **Follow the schema's conventions**: PascalCase classes with the `Fixp` prefix, snake_case slots whose alias is FIXP's field name, and a short description on every element.
- **Run the pre-commit hooks** on what you staged (`uvx pre-commit run`).
- **Lock files are part of the change.** CI installs with `uv sync --locked`, so an edit without its `uv.lock` (or `.lokf/uv.lock`) fails.
- **Knowledge-bundle changes**: `cd .lokf && just lokf-validate` must pass, and `knowledge-registrar.yaml` runs on any `.lokf/**` change.
- **`lint-and-docs.yaml`** runs ShellCheck, actionlint, markdownlint, lychee and codespell.
- **Actions are pinned to commit hashes**; Dependabot bumps them.
- **The skills pin moves with the sidecar copies.** When moving `TRUST_LADDER_SKILLS_REF` in `.github/workflows/knowledge-librarian.yaml`, copy the other `knowledge-*.yaml` workflows and `.lokf/scripts/` and `.lokf/m365/` from that release's `skills/ktl-sidecar/templates/` in the same pull request.
- **If your change alters behaviour**, add an entry under `## [Unreleased]` in [CHANGELOG.md](CHANGELOG.md).

## Code of conduct

Participation here is covered by the [Contributor Covenant](CODE_OF_CONDUCT.md).

## Using AI tools

Artificial intelligence (AI) assistance is welcome; [AI_COVENANT.md](AI_COVENANT.md) sets the rules, for people and the scheduled `knowledge-librarian` agent alike.

## Reporting issues

Use the [issue tracker](https://github.com/lmodel/fixp/issues) for the schema. Report a problem in FIXP itself to the [FIX Trading Community](https://github.com/FIXTradingCommunity/fixp-specification/issues).

## Releasing (maintainers)

- Write `## [Unreleased]` in [CHANGELOG.md](CHANGELOG.md) as you go. The release job refuses an empty one (`.github/scripts/changelog-release.mjs check`).
- Type the commit ([Conventional Commits](https://www.conventionalcommits.org/)) for what the change *is*. Only `feat:`, `fix:`, `security:` and a breaking `!` start a release. Other types leave their entries for the next release that does. A pull request that would release must carry a releasing type in its title too, since a squash merge takes its subject from it.
- On merge, [`semantic-release.yml`](.github/workflows/semantic-release.yml) retitles the section to `## [X.Y.Z] - YYYY-MM-DD`, commits `CHANGELOG.md`, tags `vX.Y.Z` and publishes the GitHub Release. No file is bumped. Once `KNOWLEDGE_RELEASE_ENABLED` is `true`, it dispatches `.github/workflows/knowledge-release.yaml`, which attaches the schema copy and the bundle when the bundle or the schema changed.
- That step runs behind the `release` GitHub Environment. Configure required reviewers on it in Settings → Environments, or every qualifying merge is released unattended.
- Below 1.0.0: push the `v0.0.0` baseline tag on `main` before the first releasing merge, which then releases 0.1.0. Both release jobs refuse to run without a `v*` tag, because semantic-release would otherwise start at 1.0.0. `.releaserc.json` maps `breaking: true` to `minor`, and reaching 1.0.0 means removing that rule in a pull request of its own.
- A branch rule requiring pull requests, status checks or signed commits would reject the release job's own push to `main`, so leave them off. [SECURITY.md](SECURITY.md) says what holds `main` instead, and the shared design is on [KTL's releasing page](https://github.com/noelmcloughlin/knowledge-trust-ladder/blob/main/docs/releasing.md).

## License

By contributing, you agree that your contributions are licensed under the [Apache License 2.0](LICENSE). The upstream's files are under their own terms; [NOTICE](NOTICE) says what they allow. Update it when you add something from elsewhere.
