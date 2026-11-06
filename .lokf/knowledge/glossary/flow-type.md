---
type: GlossaryTerm
id: https://w3id.org/lmodel/fixp/knowledge/glossary/flow-type
title: Flow type
description: "Flow type: the delivery guarantee of a flow. `FixpFlowType` lists the four, from Recoverable down to None, and a multicast topic takes only the first two."
relatedTo:
  - https://w3id.org/lmodel/fixp/knowledge/datasets/core-module
  - https://w3id.org/lmodel/fixp/knowledge/glossary/flow
sources:
  - id: core
    resource: src/fixp/schema/fixp_core.yaml
    title: FixpFlowType and FixpMulticastFlowType
generated:
  by: process:ktl-librarian
  at: "2026-11-06T08:48:23Z"
status: draft
---

# Flow type

The values run from the strongest guarantee to none.[^core]

[^core]: src/fixp/schema/fixp_core.yaml, FixpFlowType and FixpMulticastFlowType
