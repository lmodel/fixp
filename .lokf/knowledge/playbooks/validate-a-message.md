---
type: Playbook
id: https://w3id.org/lmodel/fixp/knowledge/playbooks/validate-a-message
genre: how-to
title: Validate a message or an exchange
description: "How to check a FIXP message or a run of messages against the schema: `linkml-validate` with the message's class, such as `FixpNegotiate`, or with `FixpExchange`, and the JSON Schema in `project/` for anyone without LinkML."
references:
  - https://w3id.org/lmodel/fixp/knowledge/datasets/fixp-linkml-schema
sources:
  - id: index.md
    resource: docs/index.md
    title: Validating a message or an exchange
generated:
  by: process:ktl-librarian
  at: "2026-11-06T08:48:23Z"
status: draft
---

# Validate a message or an exchange

1. Write the message as YAML or JSON, with `message_kind` naming its class.[^index.md]
2. Run `uv run linkml-validate -s src/fixp/schema/fixp.yaml -C FixpNegotiate my-message.yaml`, naming the message's class, or `-C FixpExchange` for an exchange.[^index.md]
3. Without LinkML, validate with `project/jsonschema/fixp.schema.json`, whose `$defs` hold each class.[^index.md]

The rules that compare one step with another are in `tests/fixp_rules.py`, which no validator runs.[^index.md]

[^index.md]: docs/index.md, Validating a message or an exchange
