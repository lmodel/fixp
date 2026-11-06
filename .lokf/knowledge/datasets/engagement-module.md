---
type: Dataset
id: https://w3id.org/lmodel/fixp/knowledge/datasets/engagement-module
genre: reference
title: The engagement module
description: "`fixp_engagement`: `FixpRulesOfEngagement`, the checklist of the specification's appendix B, with a `FixpStackProfile` each for the client and the server."
resource: src/fixp/schema/fixp_engagement.yaml
isPartOf:
  - https://w3id.org/lmodel/fixp/knowledge/datasets/fixp-linkml-schema
sources:
  - id: engagement
    resource: src/fixp/schema/fixp_engagement.yaml
    title: the header and the classes
generated:
  by: process:ktl-librarian
  at: "2026-11-06T08:48:23Z"
status: draft
---

# The engagement module

A stack profile holds one side's choices at the application, presentation, session, security and transport layers, and each field's `stack_layer` annotation names its layer.[^engagement]

[^engagement]: src/fixp/schema/fixp_engagement.yaml, the header and the classes
