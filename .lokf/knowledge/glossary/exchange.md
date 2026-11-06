---
type: GlossaryTerm
id: https://w3id.org/lmodel/fixp/knowledge/glossary/exchange
title: Exchange
description: "Exchange: the messages of one session in the order they were sent, as a test case, a worked example or a captured log. `FixpExchange` is the schema's tree root."
relatedTo:
  - https://w3id.org/lmodel/fixp/knowledge/datasets/exchange-module
  - https://w3id.org/lmodel/fixp/knowledge/glossary/session
sources:
  - id: exchange
    resource: src/fixp/schema/fixp_exchange.yaml
    title: FixpExchange and FixpExchangeStep
generated:
  by: process:ktl-librarian
  at: "2026-11-06T07:38:52Z"
  revision: 2c7c0f68c51ab45e91a9504ae0836e283b8918ef
status: draft
---

# Exchange

Each step is a FIXP message or a run of application messages, with the side that sent it.[^exchange]

[^exchange]: src/fixp/schema/fixp_exchange.yaml, FixpExchange and FixpExchangeStep
