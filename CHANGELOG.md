# Changelog

All notable changes to this project are documented here. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

The `v0.0.0` tag is a baseline, not a release: it marks where versioning starts so the first real release is `0.1.0` rather than `1.0.0`. The schema stays below 1.0.0 until its shape settles, so a breaking change raises the minor version.

## [Unreleased]

### Added

- **`upstream/`**, holding FIXP 1.0's SBE schema, FIX repository file and Orchestra file with their licence, at the tag `v1.0-STANDARD`, pinned by git object hash, with a weekly watch.
- **`FixpExchange`, the tree root**: a run of messages on one session, each step a message or a count of application messages. Four worked exchanges cover a recoverable session, an idempotent flow, a multicast and a shared transport.
- **`FixpRulesOfEngagement`**, the checklist of the specification's appendix B: what the client and the server each use at each layer.
- **Rules a validator cannot state** in `tests/fixp_rules.py`: who sends each message, the flow types it suits, the order of negotiation, binding and finalization, an answer's timestamp, retransmission bounds, and Sequence against Context.
- **Tests** that hold every message, field, number, type, value and presence to the three resource files, with each difference listed in `tests/upstream_departures.yaml`. They hold an example per class and a counter-example per constraint, and find any run of four words shared with FIX's files.
- **`.lokf/fixp.yaml`, the schema's `lokf adapt` copy.** The knowledge release attaches it as `schema-<tag>-fixp.yaml`.
- **The repository's Knowledge Trust Ladder (KTL) knowledge bundle and its sidecar automation**, from the KTL v0.61.0 templates with the lokf floor at 0.9.0, and a knowledge website that replaces the mkdocs site.
- **The governance files**: SECURITY.md, AI_COVENANT.md, the CONTRIBUTING checklist, and a NOTICE that states the licence position.

### Changed

- **The schema models FIXP 1.0, the Technical Standard**, where it named FIX.5.0SP2 and read the 1.1 draft's files.
- **Every message, value list and type takes the `Fixp` prefix**, such as `FixpNegotiate` for `Negotiate`, and every value list appears once, where each appeared up to three times.
- **Each message holds `message_kind`**, which names its class, so an exchange can hold any message.
- **The datatypes are FIXP's own**: unsigned numbers, a version 4 UUID, nanoseconds, milliseconds, octets in base64 and text, each with its range or pattern.
- **Seven fields take another key**: `request_time`, `reason_text`, `topic_classification`, `message_count`, `sofh_encoding_type`, `template_version`, and a `*_code` for each `Code`.
- **Topic's flow takes only Recoverable or Idempotent**, and Topic's `keepalive_interval`, Context's `next_seq_no` and FinishedSending's `last_seq_no` are optional, where the specification and the files disagree.
- **Every description is this project's own**, in place of text copied from FIX's files, whose licence forbids sharing an adaptation.
- **The template settings** turn PyPI publishing and the docs preview off, linkml and linkml-runtime are locked at 1.12.1, and the Python project is named `fixp-linkml`.

### Removed

- **The five SSSOM sets and their overlay.** Their rows were this project's guesses, not FIX's statements, and their targets named classes that no longer exist.
- **The 38 FIX datatypes as types**, of which FIXP's repository file names three, now annotations. Also the class for SBE's message header, and the guessed mappings to gist, the Common Domain Model and Fluxnova.
- **`upstream-releases/`**, with every draft and release candidate and the 1.1 draft's documents, and **`scripts/schema_to_linkml.py`**. The schema is written by hand, and `tests/test_coverage.py` compares it with the files.
- **The mkdocs site.**
