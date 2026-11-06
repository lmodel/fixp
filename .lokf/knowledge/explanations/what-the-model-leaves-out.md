---
type: Explanation
id: https://w3id.org/lmodel/fixp/knowledge/explanations/what-the-model-leaves-out
genre: explanation
title: What the model leaves out
description: "What the schema does not hold: the specification's text, the encoded bytes with SBE's message header and the Simple Open Framing Header, timing, and the content of application messages."
about:
  - https://w3id.org/lmodel/fixp/knowledge/datasets/fixp-linkml-schema
sources:
  - id: about.md
    resource: docs/about.md
    title: What the model leaves out
generated:
  by: process:ktl-librarian
  at: "2026-11-06T08:48:23Z"
status: draft
---

# What the model leaves out

- The specification's text, which is under CC BY-ND 4.0.[^about.md]
- Encoded bytes: the SBE schema's message header and the Simple Open Framing Header are the encoding's frame around a message.[^about.md]
- Timing, which a record of the messages cannot show.[^about.md]
- Application messages, whose content FIXP does not define. An exchange counts them.[^about.md]

[^about.md]: docs/about.md, What the model leaves out
