## Add your own just recipes here. This is imported by the main justfile.

# Overriding recipes from the root justfile by adding a recipe with the same
# name in this file is not possible until a known issue in just is fixed,
# https://github.com/casey/just/issues/2540

# Apply curated SSSOM mapping TSVs to the generated LinkML schema YAMLs.
# Merges SKOS exact/close/broad/narrow/related matches into the matching
# class / enum / type bodies and declares any referenced object-side prefixes.
# Idempotent: re-running on a clean tree produces no further changes. Run
# after `schema_to_linkml.py` regenerates the YAMLs and before `gen-project`.
[group('model development')]
apply-sssom-overlay:
  uv run python scripts/apply_sssom_overlay.py \
    --schema-dir src/fixp/schema \
    --mappings-dir src/fixp/mappings

# Regenerate the LinkML schemas from the upstream artifacts, then overlay the
# curated SSSOM mappings. This is the canonical "rebuild the model" recipe;
# run it whenever the upstream release or the SSSOM TSVs change. Outputs:
#   src/fixp/schema/fixp/.yaml
[group('model development')]
gen-linkml: && apply-sssom-overlay
  uv run python scripts/schema_to_linkml.py
