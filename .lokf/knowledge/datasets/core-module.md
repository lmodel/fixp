---
type: Dataset
id: https://w3id.org/lmodel/fixp/knowledge/datasets/core-module
genre: reference
title: The core module
description: "`fixp_core`: FIXP's datatypes, such as `fixp_uuid`, `fixp_nanotime` and `fixp_object`; the value lists, such as `FixpFlowType` and the four reject and termination codes; the fields the messages share; and the abstract `FixpMessage`."
resource: src/fixp/schema/fixp_core.yaml
isPartOf:
  - https://w3id.org/lmodel/fixp/knowledge/datasets/fixp-linkml-schema
sources:
  - id: core
    resource: src/fixp/schema/fixp_core.yaml
    title: the header, the types and the enums
generated:
  by: process:ktl-librarian
  at: "2026-11-06T08:48:23Z"
status: draft
---

# The core module

The datatypes are FIXP's own: unsigned numbers of 8 to 64 bits, a version 4 UUID, nanoseconds since the Unix epoch, milliseconds, octets written in base64, and text.[^core]

Each value keeps FIXP's symbolic name, such as `Recoverable`, and its `sbe_value` annotation gives the number the files assign.[^core]

Each field's aliases give its name in the specification, and its `sbe_field_id` and `repository_field_id` annotations give the numbers the two files assign.[^core]

[^core]: src/fixp/schema/fixp_core.yaml, the header, the types and the enums
