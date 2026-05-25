# About fixp

FIX Performance (FIXP) protocol - LinkML Schema

## Project Design

This project maintains a canonical LinkML schema for FIXP and generates all
derived artifacts (Python datamodels, docs pages, examples, and language
bindings) from that source.

Design goals:

- Keep a single source of truth: `src/fixp/schema/fixp.yaml`.
- Regenerate deterministically from upstream FIXP artifacts under
	`upstream-releases/fixp-specification/`.
- Keep curated semantic mappings (SSSOM) in dedicated TSV files under
	`src/fixp/mappings/` and apply them as an overlay step.
- Validate with both structural schema tests and runtime pydantic behavior tests.

Generation flow:

1. `scripts/schema_to_linkml.py` parses upstream FIX Repository, SBE schema, and
	 Orchestra resources and emits LinkML.
2. `scripts/apply_sssom_overlay.py` merges curated SSSOM mappings into the
	 generated schema.
3. `just` recipes generate downstream artifacts (project outputs and docs).

Key implementation notes:

- FIXP session messages are modeled as classes with `slots` and `slot_usage`
	refinements.
- SBE composite members are modeled as class attributes.
- `SbeMessageHeaderComposite.schema_version` is intentionally named to avoid
	shadowing the top-level `version` slot; original SBE member name is preserved
	in annotations.

## Current Status

As of May 2026, the model and tooling are in a healthy state:

- Test suite passes: `just test` reports all tests passing.
- Documentation generation path works via `just setup` and `just _gen-yaml`.
- Schema linting passes (`linkml-lint` clean).
- Provenance audits confirm emitted classes, enums, types, and slots are mapped
	to upstream FIXP inputs.
- SSSOM overlay includes mappings across all configured target vocabularies,
	including slot-level mappings.

Recent hardening work:

- Fixed missing slot overlay application in `apply_sssom_overlay.py`.
- Added broader schema and pydantic coverage tests.
- Added a local `gen-yaml` shim to handle LinkML YAML serialization of
	annotation objects.

Known caveats:

- LinkML `gen-yaml` currently requires the local shim in this project because of
	upstream serializer behavior with annotation object types.
- `just` recipe override behavior across imported justfiles is limited in the
	currently used `just` version, so command behavior is adjusted in project
	scripts instead of by redefining imported recipes.
