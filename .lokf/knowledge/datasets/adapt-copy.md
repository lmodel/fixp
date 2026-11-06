---
type: Dataset
id: https://w3id.org/lmodel/fixp/knowledge/datasets/adapt-copy
genre: reference
title: The adapt copy
description: "`.lokf/schema/fixp.yaml`, which `just lokf-adapt` writes from the schema so that it can sit beside LOKF's: the file this bundle validates against, and the file a release attaches as `schema-<tag>-fixp.yaml`."
resource: .lokf/schema/fixp.yaml
derivedFrom:
  - https://w3id.org/lmodel/fixp/knowledge/datasets/fixp-linkml-schema
sources:
  - id: readme.md
    resource: README.md
    title: Knowledge Trust Ladder (KTL)
  - id: test_schema_rules.py
    resource: tests/test_schema_rules.py
    title: test_the_copy_keeps_each_class_and_slot and test_copy_roots_the_concept_classes
  - resource: project.justfile
    title: lokf_adapt_roots
generated:
  by: process:ktl-librarian
  at: "2026-11-06T21:20:16Z"
status: draft
---

# The adapt copy

The copy roots an exchange and a rules-of-engagement record on `Concept`, and `just lokf-adapt-check` says when it is stale. It keeps `message_kind` as a plain key, so inside a concept a message is matched by its fields.[^readme.md]

It keeps every class and slot of the source, with two exceptions: it drops `id` for LOKF's, and folds `description` into LOKF's. It renames nothing.[^test_schema_rules.py]

[^readme.md]: README.md, Knowledge Trust Ladder (KTL)
[^test_schema_rules.py]: tests/test_schema_rules.py, test_the_copy_keeps_each_class_and_slot and test_copy_roots_the_concept_classes
