---
type: FixpExchange
id: https://w3id.org/lmodel/fixp/knowledge/datasets/example-exchange
genre: reference
title: An exchange as a concept
description: The shortest point-to-point start, a Negotiate and its NegotiationResponse, written as a concept of type `FixpExchange`. It shows that the domain schema admits an exchange as a concept.
resource: tests/data/valid/FixpExchange-recoverable-session.yaml
session_kind: point_to_point
exchange_steps:
  - sent_by: client
    fixp_message:
      message_kind: FixpNegotiate
      session_id: 6513270e-269e-4d37-b2a7-4de452e6b438
      request_time: 1793865600000000000
      client_flow: Recoverable
  - sent_by: server
    fixp_message:
      message_kind: FixpNegotiationResponse
      session_id: 6513270e-269e-4d37-b2a7-4de452e6b438
      request_timestamp: 1793865600000000000
      server_flow: Recoverable
derivedFrom:
  - https://w3id.org/lmodel/fixp/knowledge/datasets/example-data
sources:
  - id: test_schema_rules.py
    resource: tests/test_schema_rules.py
    title: test_an_exchange_concept_validates_against_the_copy
generated:
  by: process:ktl-librarian
  at: "2026-11-06T08:48:23Z"
status: draft
---

# An exchange as a concept

This concept shows how a host describes an exchange: its `type` is `FixpExchange`, and its keys are that class's slots beside LOKF's own. Its two steps are the first two of the recoverable session in `tests/data/valid/`.[^test_schema_rules.py]

[^test_schema_rules.py]: tests/test_schema_rules.py, test_an_exchange_concept_validates_against_the_copy
