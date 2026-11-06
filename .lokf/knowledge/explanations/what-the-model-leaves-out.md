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
  - id: own-text
    resource: docs/about.md
    title: Your own text
generated:
  by: process:ktl-librarian
  at: "2026-11-06T09:00:32Z"
status: draft
---

# What the model leaves out

- The specification's text, which is under CC BY-ND 4.0. A firm's own words about FIXP go in a rules-of-engagement record or in an Orchestra file of its own, and the schema adds no slot for either text.[^own-text]
- Encoded bytes: the SBE schema's message header and the Simple Open Framing Header are the encoding's frame around a message.[^about.md]
- Timing, which a record of the messages cannot show.[^about.md]
- Application messages, whose content FIXP does not define. An exchange counts them.[^about.md]

[^about.md]: docs/about.md, What the model leaves out
[^own-text]: docs/about.md, Your own text
