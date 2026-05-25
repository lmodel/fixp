"""Shim for the ``gen-yaml`` console-script entry point.

linkml's own ``gen-yaml`` generator uses ``yaml.SafeDumper`` (via
``linkml.generators.yamlgen.as_yaml``), which has no representers for
``jsonasobj2.JsonObj`` or ``linkml_runtime.linkml_model.meta.Annotation`` —
the types that ``annotations:`` blocks are loaded into when the schema is
parsed by linkml-runtime.  Every element with ``annotations:`` triggers:

    yaml.representer.RepresenterError: ('cannot represent an object', JsonObj(...))

This shim registers the missing representers on ``yaml.SafeDumper`` before
delegating to the real generator, so ``uv run gen-yaml`` works without
modification to the upstream library.

Registered as the ``gen-yaml`` console-script in ``pyproject.toml``, this
shim shadows linkml's entry point inside the project venv (the project is
installed last during ``uv sync``, so its scripts take precedence).
"""
from __future__ import annotations

import yaml


def _register_representers() -> None:
    """Add YAML representers for the two problematic types."""
    try:
        from jsonasobj2._jsonobj import JsonObj  # type: ignore[import]
    except ImportError:
        from linkml_runtime.utils.yamlutils import JsonObj  # type: ignore[import]

    from linkml_runtime.linkml_model.meta import Annotation

    def _represent_jsonobj(dumper: yaml.SafeDumper, data: JsonObj) -> yaml.MappingNode:
        """Represent a JsonObj as a plain YAML mapping."""
        return dumper.represent_dict(dict(data._items()))

    def _represent_annotation(
        dumper: yaml.SafeDumper, data: Annotation
    ) -> yaml.Node:
        """Represent an Annotation as its scalar ``value``."""
        return dumper.represent_data(data.value)

    yaml.SafeDumper.add_representer(JsonObj, _represent_jsonobj)
    yaml.SafeDumper.add_representer(Annotation, _represent_annotation)


def main() -> None:
    """Entry point: patch SafeDumper then hand off to the real gen-yaml CLI."""
    _register_representers()
    # Import after patching so the module-level dumper picks up the representers.
    from linkml.generators.yamlgen import cli  # type: ignore[import]

    cli()


if __name__ == "__main__":
    main()
