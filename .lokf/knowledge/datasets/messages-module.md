---
type: Dataset
id: https://w3id.org/lmodel/fixp/knowledge/datasets/messages-module
genre: reference
title: The messages module
description: "`fixp_messages`: the nineteen FIXP messages as classes with the `Fixp` prefix, from `FixpNegotiate` to `FixpMessageTemplate`, each with its fields in the specification's order and annotations for its template id, sender and flow types."
resource: src/fixp/schema/fixp_messages.yaml
isPartOf:
  - https://w3id.org/lmodel/fixp/knowledge/datasets/fixp-linkml-schema
sources:
  - id: messages
    resource: src/fixp/schema/fixp_messages.yaml
    title: the header and its note
generated:
  by: process:ktl-librarian
  at: "2026-11-06T08:48:23Z"
status: draft
---

# The messages module

The module holds seventeen session messages and the two application messages, `FixpApplied` and `FixpNotApplied`, that answer an idempotent flow.[^messages]

Each class carries these annotations:[^messages]

- `sbe_template_id` and `sbe_name`, the message's id and name in the SBE schema and the repository file;
- `fixp_sent_by`, the side that sends it;
- `fixp_flow_types` and `fixp_multicast`, where the summary in section 6 allows it;
- `fixp_flow_of`, whose flow it concerns, where it concerns one.

Each class is in a subset for its stage: initialization, binding, transferring, unbinding or finalizing.[^messages]

[^messages]: src/fixp/schema/fixp_messages.yaml, the header and its note
