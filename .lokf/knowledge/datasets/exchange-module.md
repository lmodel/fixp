---
type: Dataset
id: https://w3id.org/lmodel/fixp/knowledge/datasets/exchange-module
genre: reference
title: The exchange module
description: "`fixp_exchange`: `FixpExchange`, the tree root, a run of messages on one session, and `FixpExchangeStep`, which holds one message or a count of application messages and the side that sent it."
resource: src/fixp/schema/fixp_exchange.yaml
isPartOf:
  - https://w3id.org/lmodel/fixp/knowledge/datasets/fixp-linkml-schema
sources:
  - id: exchange
    resource: src/fixp/schema/fixp_exchange.yaml
    title: the header and the classes
generated:
  by: process:ktl-librarian
  at: "2026-11-06T08:48:23Z"
status: draft
---

# The exchange module

An exchange names which of the two forms of session it belongs to, and whether its transport carries other sessions too.[^exchange]

A step holds exactly one of a message or a count of application messages, and names the client, the server or the publisher as its sender.[^exchange]

[^exchange]: src/fixp/schema/fixp_exchange.yaml, the header and the classes
