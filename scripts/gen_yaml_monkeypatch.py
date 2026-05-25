#!/usr/bin/env python3
"""
Monkeypatch script to register YAML representers for JsonObj and Annotation types before running the real gen-yaml CLI.

This script ensures that when 'uv run gen-yaml' is called (e.g., from justfile), the representers are registered,
working around the upstream RepresenterError.
"""
from fixp._gen_yaml_shim import main

if __name__ == "__main__":
    main()
