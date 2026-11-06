---
lokf_version: "0.2"
okf_version: "0.2"
base_iri: https://w3id.org/lmodel/fixp/knowledge/
context: https://w3id.org/lokf/context.jsonld
title: fixp Knowledge Bundle
description: FIX Performance Session Layer (FIXP) 1.0 (LinkML)
license: https://creativecommons.org/licenses/by/4.0/
publisher:
  type: Person
  id: https://w3id.org/lmodel/fixp/knowledge/person/noel-mcloughlin
  name: Noel McLoughlin
---

# fixp Knowledge Bundle

A [LOKF](https://lokf.nolan-nichols.com) knowledge base for fixp. Every Markdown file under `knowledge/` is one concept; together they form a queryable knowledge graph, derived from this repository's code and docs.

# Datasets

* [The fixp LinkML schema](datasets/fixp-linkml-schema.md) - The umbrella schema `src/fixp/schema/fixp.yaml`, which imports the core, messages, exchange and engagement modules and is the file the project names. It pins FIXP 1.0 at the tag `v1.0-STANDARD`.
* [The core module](datasets/core-module.md) - `fixp_core`: FIXP's datatypes, such as `fixp_uuid`, `fixp_nanotime` and `fixp_object`; the value lists, such as `FixpFlowType` and the four reject and termination codes; the fields the messages share; and the abstract `FixpMessage`.
* [The messages module](datasets/messages-module.md) - `fixp_messages`: the nineteen FIXP messages as classes with the `Fixp` prefix, from `FixpNegotiate` to `FixpMessageTemplate`, each with its fields in the specification's order and annotations for its template id, sender and flow types.
* [The exchange module](datasets/exchange-module.md) - `fixp_exchange`: `FixpExchange`, the tree root, a run of messages on one session, and `FixpExchangeStep`, which holds one message or a count of application messages and the side that sent it.
* [The engagement module](datasets/engagement-module.md) - `fixp_engagement`: `FixpRulesOfEngagement`, the checklist of the specification's appendix B, with a `FixpStackProfile` each for the client and the server.
* [The adapt copy](datasets/adapt-copy.md) - `.lokf/fixp.yaml`, which `just lokf-adapt` writes from the schema so that it can sit beside LOKF's: the file this bundle validates against, and the file a release attaches as `schema-<tag>-fixp.yaml`.
* [The neighbours' copies](datasets/neighbour-copies.md) - `tests/neighbours/`: the adapt copies other lmodel repositories release, each the release's schema asset, which tests use to hold this copy's names apart from theirs. fix-sbe, fix-orchestra and fix-protocol join them at their releases.
* [The generated artefacts](datasets/generated-artefacts.md) - What the generators write from the schema: `project/`, `src/fixp/datamodel/` and `docs/schema/fixp.yaml`. They are committed and never edited.
* [The example data](datasets/example-data.md) - `tests/data/`: a valid example of every class, four whole exchanges, and a counter-example per constraint, named `ClassName-suffix.yaml`, each counter-example naming where it fails on its first line.
* [The copy of the upstream](datasets/upstream-copy.md) - `upstream/`: FIXP 1.0's SBE schema, FIX repository file and Orchestra file, with the repository's CC BY-ND 4.0 licence, unchanged and pinned by git object hash in `scripts/upstream_pins.tsv`.
* [The departures from FIX's files](datasets/upstream-departures.md) - `tests/upstream_departures.yaml`: each place the schema differs from a resource file, with its reason, such as Topic's keep-alive interval and Context's next sequence number, and the note that the Orchestra file is not well-formed.
* [An exchange as a concept](datasets/example-exchange.md) - The shortest point-to-point start, a Negotiate and its NegotiationResponse, written as a concept of type `FixpExchange`. It shows that the domain schema admits an exchange as a concept.
* [Rules of engagement as a concept](datasets/example-rules-of-engagement.md) - A client and a server that use SBE over TCP with TLS 1.3, written as a concept of type `FixpRulesOfEngagement`. It shows that the domain schema admits the appendix B checklist as a concept.

# Explanations

* [One edition](explanations/one-edition.md) - Why the schema models FIXP 1.0, the Technical Standard of April 2021, alone: version 1.1 is a Draft Standard whose files differ only in four field numbers, and whose chapters add WebSocket guidance but no message, field or value.
* [A message as a record](explanations/a-message-as-a-record.md) - How a FIXP message becomes a YAML or JSON record whatever its encoding: a class per message, `message_kind` for FIXP's MessageType, snake_case fields with FIXP's names as aliases, seven fields under another key, and octets in base64.
* [Rules that span an exchange](explanations/rules-that-span-an-exchange.md) - What `tests/fixp_rules.py` checks that JSON Schema cannot: who sends each message, the flow types it suits, the order of negotiation and binding, an answer's timestamp, retransmission, the endings, and Sequence against Context.
* [What the model leaves out](explanations/what-the-model-leaves-out.md) - What the schema does not hold: the specification's text, the encoded bytes with SBE's message header and the Simple Open Framing Header, timing, and the content of application messages.
* [What FIX's files show](explanations/what-fixs-files-show.md) - Faults found in FIXP 1.0's own files: the Orchestra file is not well-formed, the SBE schema's field numbers clash and differ from the repository file's, RetransmitReject is misspelt, and section 3 contradicts section 6 on Context.
* [Mappings](explanations/mappings.md) - Why `FixpMessage` is only related to lmodel/fix-sbe's `SbeMessageV1` and lmodel/fix-orchestra's `OrchestraMessageV10`, and why the SBE and FIX datatype names are checked against fix-sbe's lists. The five SSSOM sets are gone.

# Glossary

* [Flow](glossary/flow.md) - Flow: the application messages one side of a FIXP session sends, in one direction. A session between two parties has two flows, and a multicast one.
* [Flow type](glossary/flow-type.md) - Flow type: the delivery guarantee of a flow. `FixpFlowType` lists the four, from Recoverable down to None, and a multicast topic takes only the first two.
* [Session](glossary/session.md) - Session: a FIXP dialog under one identifier, a version 4 UUID the client chooses and never uses again. It takes one of two forms, between two parties or multicast, and outlives the transport it is bound to.
* [Exchange](glossary/exchange.md) - Exchange: the messages of one session in the order they were sent, as a test case, a worked example or a captured log. `FixpExchange` is the schema's tree root.
* [Rules of engagement](glossary/rules-of-engagement.md) - Rules of engagement: what two counterparties agree on for a FIXP service at each layer of the stack, the checklist of the specification's appendix B. `FixpRulesOfEngagement` records it.
* [Adapt copy](glossary/adapt-copy.md) - Adapt copy: the copy of a schema that `lokf adapt` writes so that it can sit beside LOKF's, here `.lokf/fixp.yaml`. Edit the source, never the copy.

# References

* [FIX Performance Session Layer](references/fixp-specification.md) - The FIX Trading Community's repository for FIXP, `FIXTradingCommunity/fixp-specification`, which holds each edition's chapters and resource files under CC BY-ND 4.0. The project pins 1.0 at the tag `v1.0-STANDARD`.
* [lmodel/fix-sbe](references/lmodel-fix-sbe.md) - The sibling LinkML model of FIX Simple Binary Encoding, whose `SbeMessageV1` defines a message template and whose value lists name the SBE primitive types, byte orders and FIX datatypes this schema's annotations use.
* [lmodel/fix-orchestra](references/lmodel-fix-orchestra.md) - The sibling LinkML model of FIX Orchestra, whose `OrchestraMessageV10` defines a message in an Orchestra file such as FIXP's.

# Services

* [Documentation site](services/documentation-site.md) - The knowledge website in `website/`, an Astro Starlight site that the Knowledge website workflow publishes to GitHub Pages at `https://lmodel.github.io/fixp`, built from the README, `docs/`, the schema's pages and this bundle.
* [The upstream check](services/upstream-check.md) - `scripts/check_upstream_release.py`: lists FIX's FIXP repository through GitHub's API and reports a new tag or edition folder, a moved tag, a changed or missing pinned file, or a changed licence.

# Playbooks

* [Regenerate and test](playbooks/regenerate-and-test.md) - How to change the schema: edit a module under `src/fixp/schema/`, run `just lint`, `just gen-project`, `just gen-doc`, `just lokf-adapt` and `just test`, and commit what they write.
* [Cut a release](playbooks/release.md) - How a release happens: write `## [Unreleased]`, merge with a releasing commit type, and `semantic-release.yml` tags, writes the changelog and dispatches the knowledge release, which attaches the assets.
* [Update the upstream pins](playbooks/update-upstream-pins.md) - What to do when the watch reports a change in FIX's FIXP repository: read what changed, replace `upstream/`, the pins and the headers together, and let the coverage test show what the schema must follow.
* [Validate a message or an exchange](playbooks/validate-a-message.md) - How to check a FIXP message or a run of messages against the schema: `linkml-validate` with the message's class, such as `FixpNegotiate`, or with `FixpExchange`, and the JSON Schema in `project/` for anyone without LinkML.
* [Knowledge sources map](playbooks/knowledge-sources.md) - The librarian's scrape map: every repository location and external source this bundle derives concepts from, how to re-check each, and the tracked paths left out with their reasons.

# Policies

* [AI covenant](policies/ai-covenant.md) - The rules for AI-assisted work here: a person owns every contribution, an element says what FIXP's files say, a rule states only what the specification states, a mapping names a sure match or is absent, and FIX's words stay FIX's.
* [Licence and attribution](policies/license-and-attribution.md) - Whose work each part is: the code and the schema under Apache-2.0, the bundle under CC BY 4.0, and FIXP's three resource files whole and unchanged under CC BY-ND 4.0.
* [Security policy](policies/security-policy.md) - How to report a vulnerability, what this repository releases, what executes here and what holds each surface. A report goes through GitHub's private vulnerability reporting, and only the latest release receives fixes.

# Workflows

* [Build and test (main.yaml)](workflows/main.md) - The Build and test workflow: on every pull request and push to `main`, it runs `just test` on Python 3.10 to 3.14, and lints the schema and checks the adapt copy on 3.13.
* [Lint and docs (lint-and-docs.yaml)](workflows/lint-and-docs.md) - The static checks on pull requests and on `main`: ShellCheck, actionlint, the governance files' word budgets, markdownlint, lychee and codespell.
* [Semantic release (semantic-release.yml)](workflows/semantic-release.md) - The workflow that computes the next version from Conventional Commits on `main`, promotes the changelog, tags and publishes the GitHub Release, and dispatches the knowledge release.
* [Knowledge registrar (knowledge-registrar.yaml)](workflows/knowledge-registrar.md) - The gate on the bundle: it validates the bundle on each pull request that touches it, and checks who vouched for what.
* [Knowledge librarian (knowledge-librarian.yaml)](workflows/knowledge-librarian.md) - The sidecar's scheduled agent run that keeps the bundle in step with the repository. It stays inert until `KNOWLEDGE_LIBRARIAN_ENABLED` is `true`, and a person merges what it proposes.
* [Knowledge release (knowledge-release.yaml)](workflows/knowledge-release.md) - The workflow that attaches the bundle, a Copilot skill and the schema's adapt copy to a GitHub release, each with its `.sha256` and an attestation, when the bundle or the schema changed.
* [Knowledge sync (knowledge-sync.yaml)](workflows/knowledge-sync.md) - The weekly workflow that keeps the sidecar's copies and the skills pin at the newest release of Knowledge Trust Ladder, by a pull request a person merges.
* [Knowledge website (knowledge-website.yaml)](workflows/knowledge-website.md) - The workflow that builds `website/` on each pull request that touches its inputs, and deploys it from `main` once `KNOWLEDGE_WEBSITE_ENABLED` is `true`.
* [Upstream watch (upstream-watch.yaml)](workflows/upstream-watch.md) - The weekly check that `scripts/check_upstream_release.py` runs: a new tag or edition folder of FIXP, a moved tag, a changed or missing pinned file, or a changed licence opens or updates an issue.
