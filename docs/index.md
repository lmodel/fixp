# fixp

This project is a LinkML model of the FIX Performance Session Layer (FIXP) 1.0, the FIX Trading Community's session protocol for fast trading links. It describes each FIXP message by its fields, a run of messages on one session, and the rules of engagement two parties agree on.

- [Schema documentation](elements/index.md), generated from the schema
- [About](about.md): how the schema reads FIXP, where each part comes from and what it leaves out
- [`fixp.yaml`](schema/fixp.yaml): the schema, with its modules merged

## Validating a message or an exchange

A message validates against its own class, and an exchange against `FixpExchange`, the tree root.

```bash
uv run linkml-validate -s src/fixp/schema/fixp.yaml -C FixpNegotiate my-message.yaml
uv run linkml-validate -s src/fixp/schema/fixp.yaml -C FixpExchange my-exchange.yaml
```

`project/jsonschema/fixp.schema.json` is the same schema for anyone without LinkML, and its `$defs` hold each class.

## A record

```yaml
message_kind: FixpNegotiate
session_id: 6513270e-269e-4d37-b2a7-4de452e6b438
request_time: 1793865600000000000
client_flow: Recoverable
```

`tests/data/valid/` has a record of every class, and four whole exchanges.

## What the validator cannot check

`tests/fixp_rules.py` holds the checks that compare one step of an exchange with the steps before it: an answer with its request, a message with the flow types the session agreed, a sequence number with what was sent. [About](about.md#rules-that-span-an-exchange) lists them.
