---
type: GlossaryTerm
id: https://w3id.org/lmodel/fixp/knowledge/glossary/flow
title: Flow
description: "Flow: the application messages one side of a FIXP session sends, in one direction. A session between two parties has two flows, and a multicast one."
relatedTo:
  - https://w3id.org/lmodel/fixp/knowledge/datasets/core-module
sources:
  - id: core
    resource: src/fixp/schema/fixp_core.yaml
    title: FixpFlowType
generated:
  by: process:ktl-librarian
  at: "2026-11-06T07:38:52Z"
  revision: dd047e9f1966002a09d4983ab2b8a95f0fe99e58
status: draft
---

# Flow

Each flow has a type, which says how surely it is delivered.[^core]

[^core]: src/fixp/schema/fixp_core.yaml, FixpFlowType
