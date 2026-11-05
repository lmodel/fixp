"""Checks that the project's words are its own.

FIX licenses the FIXP specification and its resource files under CC BY-ND 4.0, which lets a
whole copy travel but no adaptation, so no sentence of FIX's belongs in the schema or the docs.
This test looks for a run of four or more words the project's text shares with the text in the
pinned resource files: the SBE schema's descriptions and the Orchestra file's documentation and
examples, the same check NOTICE describes.

The specification's chapters stay out of this repository. Set FIXP_SPEC_DOCS to a folder of
them, such as the v1-0-STANDARD/doc folder of a clone of FIXTradingCommunity/fixp-specification,
and the test compares with them too.
"""

import os
import re
from functools import cache
from pathlib import Path

import pytest
import yaml
from lxml import etree

from tests.paths import ORCHESTRA, REPOSITORY, ROOT, SBE_SCHEMA, SCHEMA_DIR

RUN = 4
WORD = re.compile(r"[a-z0-9]+")
ADDRESS = re.compile(r"https?://\S+")

# Names, not statements: a run inside one of these does not count, and no run crosses one.
NAMES = (
    "fix performance session layer",
    "simple open framing header",
    "simple binary encoding",
    "fix trading community",
    "fix protocol limited",
    "fix protocol ltd",
    "creative commons attribution noderivatives 4 0 international public license",
    "cc by nd 4 0",
)


def _runs(text):
    """Every run of four words in the text, with names and web addresses cut out."""
    words = " ".join(WORD.findall(ADDRESS.sub("|", text.lower())))
    for name in NAMES:
        words = words.replace(name, "|")
    runs = set()
    for part in words.split("|"):
        found = part.split()
        runs |= {" ".join(found[i : i + RUN]) for i in range(len(found) - RUN + 1)}
    return runs


def _file_texts(path):
    """The prose in a resource file: attribute descriptions and element text."""
    parser = etree.XMLParser(
        no_network=True, resolve_entities=False, huge_tree=False, recover=True
    )
    root = etree.parse(str(path), parser).getroot()
    for node in root.iter():
        if node.get("description"):
            yield node.get("description")
        if isinstance(node.tag, str) and node.text and node.text.strip():
            yield node.text


@cache
def fix_runs():
    runs = set()
    for path in (SBE_SCHEMA, ORCHESTRA, REPOSITORY):
        for text in _file_texts(path):
            runs |= _runs(text)
    docs = os.environ.get("FIXP_SPEC_DOCS")
    if docs:
        for path in sorted(Path(docs).glob("*.md")):
            runs |= _runs(path.read_text(encoding="utf-8"))
    return runs


def _schema_texts(node):
    """Every piece of the schema that a reader takes for prose."""
    if isinstance(node, dict):
        for key, value in node.items():
            if key in ("description", "title", "comments", "notes") and isinstance(
                value, (str, list)
            ):
                yield from [value] if isinstance(value, str) else value
            else:
                yield from _schema_texts(value)
    elif isinstance(node, list):
        for item in node:
            yield from _schema_texts(item)


def _documents():
    docs = [ROOT / "README.md", ROOT / "CHANGELOG.md"]
    docs += sorted((ROOT / "docs").glob("*.md"))
    docs += sorted((ROOT / ".lokf" / "knowledge").rglob("*.md"))
    return [path for path in docs if path.exists()]


def test_the_check_has_something_to_compare():
    assert len(fix_runs()) > 1000


@pytest.mark.parametrize(
    "path", sorted(SCHEMA_DIR.glob("*.yaml")), ids=lambda p: p.stem
)
def test_the_schema_shares_no_run_with_fix(path):
    shared = {}
    for text in _schema_texts(yaml.safe_load(path.read_text(encoding="utf-8"))):
        found = _runs(text) & fix_runs()
        if found:
            shared[text[:60]] = sorted(found)
    assert not shared, shared


@pytest.mark.parametrize("path", _documents(), ids=lambda p: p.name)
def test_the_docs_share_no_run_with_fix(path):
    assert not _runs(path.read_text(encoding="utf-8")) & fix_runs()


def test_a_shared_run_is_caught():
    """A sentence taken from a resource file fails, so a pass above means something."""
    text = next(t for t in _file_texts(SBE_SCHEMA) if len(t.split()) >= RUN)
    assert _runs(text) & fix_runs()


def test_a_name_is_not_a_run():
    assert not _runs("the FIX Performance Session Layer (FIXP)") & _runs(
        "FIX Performance Session Layer, version 1.0"
    )
