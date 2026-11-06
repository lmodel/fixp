---
type: Dataset
id: https://w3id.org/lmodel/fixp/knowledge/datasets/generated-artefacts
genre: reference
title: The generated artefacts
description: "What the generators write from the schema: `project/`, `src/fixp/datamodel/` and `docs/schema/fixp.yaml`. They are committed and never edited."
resource: project
derivedFrom:
  - https://w3id.org/lmodel/fixp/knowledge/datasets/fixp-linkml-schema
sources:
  - id: contributing.md
    resource: CONTRIBUTING.md
    title: Before opening a pull request
  - id: test_generated_json_schema.py
    resource: tests/test_generated_json_schema.py
    title: test_the_committed_file_is_the_generators_output
  - resource: src/fixp/datamodel
  - resource: docs/schema
  - resource: .linkml/generators.yaml
generated:
  by: process:ktl-librarian
  at: "2026-11-06T08:48:23Z"
status: draft
---

# The generated artefacts

`just gen-project`, `just gen-doc` and `just lokf-adapt` write them, and their output is committed with the schema change.[^contributing.md]

A test fails when the committed JSON Schema is not what the generator writes from the schema today.[^test_generated_json_schema.py]

[^contributing.md]: CONTRIBUTING.md, Before opening a pull request
[^test_generated_json_schema.py]: tests/test_generated_json_schema.py, test_the_committed_file_is_the_generators_output
