## Add your own just recipes here. This is imported by the main justfile.

# Overriding recipes from the root justfile by adding a recipe with the same
# name in this file is not possible until a known issue in just is fixed,
# https://github.com/casey/just/issues/2540

# ============ Knowledge bundle: the adapted domain schema ============

# `.lokf/fixp.yaml` is the copy `lokf adapt` writes from the schema so that it can sit beside
# `.lokf/lokf.yaml` (`lokf adapt --help` lists the moves). The roots are the two records a
# person documents: an exchange of messages, and the rules of engagement two parties agree on.
# A concept names one of them as its `type`. The messages stay values inside an exchange. The
# recipes run the `lokf` the sidecar's floor pins (0.9.0 or later); LOKF_CMD runs another,
# such as a checkout: LOKF_CMD="uv run --project ../lokf lokf" just lokf-adapt
lokf_cmd := env_var_or_default("LOKF_CMD", "uv run --project .lokf lokf")
lokf_adapt_roots := "--root FixpExchange --root FixpRulesOfEngagement"

# Rewrite .lokf/fixp.yaml from the schema (run after every schema change)
[group('knowledge bundle')]
lokf-adapt:
  {{lokf_cmd}} adapt {{source_schema_path}} {{lokf_adapt_roots}} --lokf .lokf/lokf.yaml -o .lokf/fixp.yaml

# Fail when .lokf/fixp.yaml is stale against the schema or .lokf/lokf.yaml
[group('knowledge bundle')]
lokf-adapt-check:
  {{lokf_cmd}} adapt {{source_schema_path}} {{lokf_adapt_roots}} --lokf .lokf/lokf.yaml -o .lokf/fixp.yaml --check
