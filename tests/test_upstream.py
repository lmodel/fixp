"""Checks that upstream/ holds the edition the schema models.

upstream/ holds FIXP 1.0's three resource files and the repository's licence, as they are
published. scripts/check_upstream_release.py compares them with GitHub. These tests make the
same comparison offline, and hold the schema's headers and NOTICE to the same pins.
"""

import hashlib
import importlib.util
from functools import cache

import yaml

from tests.paths import ROOT, SCHEMA_DIR, UPSTREAM

WATCH = ROOT / "scripts" / "check_upstream_release.py"


@cache
def _watch():
    spec = importlib.util.spec_from_file_location("watch_pins", WATCH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def _header(path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_upstream_holds_only_the_pinned_files():
    found = {
        path.relative_to(UPSTREAM).as_posix()
        for path in UPSTREAM.rglob("*")
        if path.is_file()
    }
    assert found == set(_watch().pins())
    assert len(found) == 4


def test_copies_match_the_pinned_blobs():
    """Each file has the git object hash the watch pins."""
    wrong = [
        path for path, sha in _watch().pins().items() if _blob(UPSTREAM / path) != sha
    ]
    assert not wrong


def test_every_module_names_the_pinned_edition():
    watch = _watch()
    for path in SCHEMA_DIR.glob("*.yaml"):
        header = _header(path)
        assert header["version"] == watch.EDITION, path.name
        assert header["source"].endswith(f"/tree/{watch.TAG}/{watch.FOLDER}"), path.name
        assert header["license"] == "Apache-2.0", path.name


def test_the_umbrella_names_the_pinned_commit():
    watch = _watch()
    annotations = _header(SCHEMA_DIR / "fixp.yaml")["annotations"]
    assert annotations["upstream_tag"] == watch.TAG
    assert annotations["upstream_commit"] == watch.COMMIT


def test_the_notice_carries_what_the_licences_ask():
    """CC BY-ND asks for attribution and a link to the licence, and Apache-2.0 for its notice,
    and FIX's marks stay FIX's."""
    notice = (ROOT / "NOTICE").read_text(encoding="utf-8")
    for needed in (
        "FIX Protocol Limited",
        "Creative Commons Attribution-NoDerivatives 4.0",
        "https://creativecommons.org/licenses/by-nd/4.0/legalcode",
        "fixp-specification",
        f"at the tag {_watch().TAG}, commit {_watch().COMMIT[:7]}",
        "Infopaq",
        "does not imply endorsement",
    ):
        assert needed in notice, needed
    for path in _watch().pins():
        assert path.removeprefix("fixp-specification/") in notice, path


def test_the_notice_names_the_apache_copy_of_the_sbe_schema():
    """FIX also publishes the SBE schema under Apache-2.0 in conga, as the same git object. NOTICE
    names it by that hash, so a new pin fails here until the claim is checked again."""
    notice = (ROOT / "NOTICE").read_text(encoding="utf-8")
    sbe = _watch().pins()[
        "fixp-specification/v1-0-STANDARD/resources/SBEschemaForFIXP.xml"
    ]
    assert "https://github.com/FIXTradingCommunity/conga" in notice
    assert f"same git object hash as the pinned file, {sbe[:7]}" in notice.replace(
        "\n", " "
    )
