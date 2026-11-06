---
type: Policy
id: https://w3id.org/lmodel/fixp/knowledge/policies/license-and-attribution
genre: reference
title: Licence and attribution
description: "Whose work each part is: the code and the schema under Apache-2.0, the bundle under CC BY 4.0, and FIXP's three resource files whole and unchanged under CC BY-ND 4.0."
resource: NOTICE
sources:
  - id: readme.md
    resource: README.md
    title: License
  - id: notice
    resource: NOTICE
    title: FIX Performance Session Layer
  - id: test_own_words.py
    resource: tests/test_own_words.py
    title: the module's description
  - resource: LICENSE
generated:
  by: process:ktl-librarian
  at: "2026-11-06T08:48:23Z"
status: draft
---

# Licence and attribution

The schema and the code are under the Apache License 2.0, and the knowledge bundle is under CC BY 4.0.[^readme.md]

CC BY-ND 4.0 lets anyone share a whole, unchanged copy of FIX's files, and does not let anyone share an adapted version. So `upstream/` holds those files unchanged, and every title, description and comment here was written from what the element does.[^notice]

A test finds any run of four words shared with the text in the resource files, and with the specification's chapters when `FIXP_SPEC_DOCS` names them.[^test_own_words.py]

This project is not endorsed by FIX Protocol Limited, and it takes nothing from fixtrading.org, whose terms bar automated copying.[^notice]

[^readme.md]: README.md, License
[^notice]: NOTICE, FIX Performance Session Layer
[^test_own_words.py]: tests/test_own_words.py, the module's description
