---
type: GlossaryTerm
id: https://w3id.org/lmodel/fixp/knowledge/glossary/session
title: Session
description: "Session: a FIXP dialog under one identifier, a version 4 UUID the client chooses and never uses again. It takes one of two forms, between two parties or multicast, and outlives the transport it is bound to."
relatedTo:
  - https://w3id.org/lmodel/fixp/knowledge/datasets/exchange-module
sources:
  - id: exchange
    resource: src/fixp/schema/fixp_exchange.yaml
    title: FixpSessionKind
generated:
  by: process:ktl-librarian
  at: "2026-11-06T07:38:52Z"
  revision: 2c7c0f68c51ab45e91a9504ae0836e283b8918ef
status: draft
---

# Session

The two forms are a client and a server with one flow each way, and a publisher with one flow and many listeners.[^exchange]

[^exchange]: src/fixp/schema/fixp_exchange.yaml, FixpSessionKind
