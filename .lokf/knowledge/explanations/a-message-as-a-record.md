---
type: Explanation
id: https://w3id.org/lmodel/fixp/knowledge/explanations/a-message-as-a-record
genre: explanation
title: A message as a record
description: "How a FIXP message becomes a YAML or JSON record whatever its encoding: a class per message, `message_kind` for FIXP's MessageType, snake_case fields with FIXP's names as aliases, seven fields under another key, and octets in base64."
about:
  - https://w3id.org/lmodel/fixp/knowledge/datasets/messages-module
sources:
  - id: about.md
    resource: docs/about.md
    title: A message as a record
generated:
  by: process:ktl-librarian
  at: "2026-11-06T07:38:52Z"
  revision: f07e8ed1bf536329aad51980ead6c19e04420365
status: draft
---

# A message as a record

FIXP describes a message by its fields and leaves the wire format to the encoding, so a record is the message's fields as YAML or JSON.[^about.md]

Seven fields take a different word, because the plain one is taken elsewhere in the family: `request_time`, `reason_text`, `topic_classification`, `message_count`, `sofh_encoding_type`, `template_version`, and a `*_code` for each `Code`.[^about.md]

The octets are written in base64, which is this schema's choice.[^about.md]

[^about.md]: docs/about.md, A message as a record
