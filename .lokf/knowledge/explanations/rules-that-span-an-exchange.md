---
type: Explanation
id: https://w3id.org/lmodel/fixp/knowledge/explanations/rules-that-span-an-exchange
genre: explanation
title: Rules that span an exchange
description: "What `tests/fixp_rules.py` checks that JSON Schema cannot: who sends each message, the flow types it suits, the order of negotiation and binding, an answer's timestamp, retransmission, the endings, and Sequence against Context."
about:
  - https://w3id.org/lmodel/fixp/knowledge/datasets/exchange-module
sources:
  - id: about.md
    resource: docs/about.md
    title: Rules that span an exchange
  - id: test_rules.py
    resource: tests/test_rules.py
    title: test_every_rule_has_a_case
  - resource: tests/fixp_rules.py
generated:
  by: process:ktl-librarian
  at: "2026-11-06T08:48:23Z"
status: draft
---

# Rules that span an exchange

JSON Schema checks each message by itself. The rules compare one step of an exchange with the steps before it, and each has a counter-example.[^about.md]

`tests/fixp_rules.py` reports seventeen rules, and each has a test case that breaks that rule and no other.[^test_rules.py]

[^about.md]: docs/about.md, Rules that span an exchange
[^test_rules.py]: tests/test_rules.py, test_every_rule_has_a_case
