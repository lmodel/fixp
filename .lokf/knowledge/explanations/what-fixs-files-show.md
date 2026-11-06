---
type: Explanation
id: https://w3id.org/lmodel/fixp/knowledge/explanations/what-fixs-files-show
genre: explanation
title: What FIX's files show
description: "Faults found in FIXP 1.0's own files: the Orchestra file is not well-formed, the SBE schema's field numbers clash and differ from the repository file's, RetransmitReject is misspelt, and section 3 contradicts section 6 on Context."
about:
  - https://w3id.org/lmodel/fixp/knowledge/datasets/upstream-copy
sources:
  - id: about.md
    resource: docs/about.md
    title: What FIX's files show
generated:
  by: process:ktl-librarian
  at: "2026-11-06T07:38:52Z"
  revision: f07e8ed1bf536329aad51980ead6c19e04420365
status: draft
---

# What FIX's files show

The issues are reported to the FIX Trading Community, not mended here.[^about.md]

- The Orchestra file closes the UnsequencedHeartbeat message twice. The tests read it in recovery mode, and it agrees with the repository file.[^about.md]
- The SBE schema numbers Topic's `Flow` 8, which is `Reason`'s number in four other messages, and numbers the four fields of `MessageTemplate` one lower than the repository file does.[^about.md]
- All three files spell RetransmitReject as `RestransmitReject`.[^about.md]
- Section 3 forbids Context where the flow is unsequenced or empty, while section 6's summary allows it. The rules follow section 6.[^about.md]

[^about.md]: docs/about.md, What FIX's files show
