---
type: FixpRulesOfEngagement
id: https://w3id.org/lmodel/fixp/knowledge/datasets/example-rules-of-engagement
genre: reference
title: Rules of engagement as a concept
description: A client and a server that use SBE over TCP with TLS 1.3, written as a concept of type `FixpRulesOfEngagement`. It shows that the domain schema admits the appendix B checklist as a concept.
resource: tests/data/valid/FixpRulesOfEngagement-venue.yaml
client_stack:
  message_encoding: Simple Binary Encoding
  framing: Simple Open Framing Header
  supported_flow_types:
    - Idempotent
  tls_version: "1.3"
  transports:
    - TCP
server_stack:
  message_encoding: Simple Binary Encoding
  framing: Simple Open Framing Header
  supported_flow_types:
    - Recoverable
  tls_version: "1.3"
  transports:
    - TCP
derivedFrom:
  - https://w3id.org/lmodel/fixp/knowledge/datasets/example-data
sources:
  - id: test_schema_rules.py
    resource: tests/test_schema_rules.py
    title: test_a_rules_of_engagement_concept_validates_against_the_copy
generated:
  by: process:ktl-librarian
  at: "2026-11-06T08:48:23Z"
status: draft
---

# Rules of engagement as a concept

This concept shows how a host records what it agreed with a counterparty: its `type` is `FixpRulesOfEngagement`, and each side's choices sit under `client_stack` and `server_stack`.[^test_schema_rules.py]

[^test_schema_rules.py]: tests/test_schema_rules.py, test_a_rules_of_engagement_concept_validates_against_the_copy
