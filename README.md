<a href="https://github.com/linkml/linkml-project-copier"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-teal.json" alt="Copier Badge" style="max-width:100%;"/></a>

# fixp

FIX Performance Session Layer (FIXP) 1.0 (LinkML)

> **Only want to ask?** Install `ktl-docent` into any agent you use, by a route from [the install page](https://w3id.org/ktl/docs/install/), and ask it about this project. It answers from the bundle and says how far each answer has been checked.
>
> **Agents:** if `.lokf/knowledge/index.md` exists, read it first. `llms.txt` says how to weigh it.

## Documentation Website

[https://lmodel.github.io/fixp](https://lmodel.github.io/fixp)

## What it models

The schema renders the [FIX Performance Session Layer](https://github.com/FIXTradingCommunity/fixp-specification) 1.0, the Technical Standard of April 2021. It covers each FIXP message by its fields, whatever the encoding; a run of messages on one session, checked against the protocol's rules; and the rules of engagement two parties agree on.

`upstream/` holds FIXP's three resource files, pinned by hash, and the tests hold the schema to them. [docs/about.md](docs/about.md) says how the schema reads FIXP and what it leaves out.

## Mappings

* **[lmodel/fix-sbe](https://github.com/lmodel/fix-sbe)** and **[lmodel/fix-orchestra](https://github.com/lmodel/fix-orchestra)**: `FixpMessage` is related to `SbeMessageV1` and `OrchestraMessageV10`, the classes of the files that define each message. `tests/test_mappings.py` checks the targets, and the SBE and FIX datatype names, against their released copies.

The five SSSOM sets are gone: their rows were the project's guesses, not FIX's statements, and most named classes that no longer exist.

## Repository Structure

* [docs/](docs/): the website's own pages
* [project/](project/): generated project files (do not edit them)
* [scripts/](scripts/): the upstream watch
* [src/fixp/schema/](src/fixp/schema): the LinkML schema, which you edit
* [src/fixp/datamodel/](src/fixp/datamodel): the generated Python datamodel
* [tests/](tests/): Python tests, with example data in [data/](tests/data) and the neighbours' adapt copies in [neighbours/](tests/neighbours)
* [upstream/](upstream/): FIXP 1.0's resource files and their licence, unchanged
* [website/](website/): the Astro Starlight site built from the README, `docs/`, the schema's pages and the knowledge bundle

## Developer Tools

Run `just` to list the project's [just](https://github.com/casey/just/) recipes.

## Knowledge Trust Ladder (KTL)

`.lokf/` holds this project's [KTL](https://w3id.org/ktl/) knowledge bundle. Its domain schema, `.lokf/fixp.yaml`, is the copy `just lokf-adapt` writes from `src/fixp/schema/fixp.yaml`, and `just lokf-adapt-check` says when it is stale. Edit the source, never the copy.

The copy roots an exchange and a rules-of-engagement record on `Concept`. An exchange's messages stay values inside it. In Obsidian, add these to the KTL plugins' *Known LOKF types* setting:

```text
FixpExchange, FixpRulesOfEngagement
```

The copy drops `id` for LOKF's, folds `description` into LOKF's, and keeps `message_kind` as a plain key, so inside a concept a message is matched by its fields. `tests/test_schema_rules.py` keeps the copy's keys apart from LOKF and the released copies in `tests/neighbours/`.

## License

The schema and the code are under the Apache License 2.0 ([LICENSE](LICENSE)), and the knowledge bundle in [.lokf/knowledge/](.lokf/knowledge) is under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

FIX's files in `upstream/` keep their licence, CC BY-ND 4.0. [NOTICE](NOTICE) states the position, and this project is not endorsed by FIX Protocol Limited.

## Contributing and security

[CONTRIBUTING.md](CONTRIBUTING.md) is the checklist for pull requests and
releases, [AI_COVENANT.md](AI_COVENANT.md) sets the rules for AI-assisted work,
[SECURITY.md](SECURITY.md) says how to report a vulnerability, and
[CHANGELOG.md](CHANGELOG.md) records the changes.

## Credits

Built from the [linkml-project-copier](https://github.com/linkml/linkml-project-copier) template ([doi:10.5281/zenodo.15163584](https://doi.org/10.5281/zenodo.15163584)).
