#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Check the FIX Trading Community's FIXP repository against the edition the schema models.

The schema models FIXP 1.0, the Technical Standard at the tag v1.0-STANDARD. upstream/ holds
that edition's three resource files and the repository's LICENSE unchanged. These things can
change without any change in this repository:

- a new tag appears, or a new edition folder such as v1-1-STANDARD;
- the pinned tag moves, or a pinned file changes or goes, at the tag or on the default branch;
- the licence file on the default branch changes.

The script lists the repository's trees through GitHub's API and compares git object hashes,
so it downloads no file. It reads nothing from fixtrading.org, whose terms bar automated
copying. scripts/upstream_pins.tsv holds each file's hash. The script prints a Markdown report
and exits 1 on any of the above, or when a check could not finish.

Text a server chose is quoted as code on one line in the report, so the issue the workflow
opens from it cannot mention anyone. A redirect is followed only to an https address on
api.github.com. Set ``GITHUB_TOKEN`` to raise the API's rate limit. Usage::

    python scripts/check_upstream_release.py [--report FILE]
"""

from __future__ import annotations

import argparse
import http.client
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PINS = ROOT / "scripts" / "upstream_pins.tsv"
USER_AGENT = "lmodel-fixp-upstream-check"
API = "https://api.github.com/repos/FIXTradingCommunity"
HOST = "api.github.com"

# The most the script reads of one answer. A recursive listing of the repository is small.
MAX_BYTES = 20_000_000

SPEC = "fixp-specification"
BRANCH = "master"

# What the schema models. tests/test_upstream.py holds the schema header and these pins
# equal. Move them together, with upstream/ and scripts/upstream_pins.tsv, for another edition.
EDITION = "1.0"
TAG = "v1.0-STANDARD"
COMMIT = "6d89f5fa66d544ea6b41e93853c23292505e49c6"
FOLDER = "v1-0-STANDARD"

# Everything the repository held when the pins were read, so anything new stands out. The
# folder pattern finds an edition however it is spelled.
KNOWN_TAGS = ("v1.0-RC3", "v1.0-STANDARD", "v1.1-DRAFT")
KNOWN_FOLDERS = (
    "v1-0-DRAFT",
    "v1-0-RC2",
    "v1-0-RC3",
    "v1-0-RC4",
    "v1-0-STANDARD",
    "v1-1",
)
EDITION_FOLDER = re.compile(r"^v\d+-\d+")


class _ApiRedirect(urllib.request.HTTPRedirectHandler):
    """Follow a redirect only to an https address on the API's host."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        parts = urllib.parse.urlsplit(newurl)
        if parts.scheme != "https" or parts.hostname != HOST:
            raise ValueError(f"a redirect leads off {HOST}, to {newurl}")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


# An opener in place of urlopen's, whose redirect handler follows any address.
_open = urllib.request.build_opener(_ApiRedirect).open


def _get(path: str):
    """The JSON answer to one API path, read up to the cap."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(f"{API}{path}", headers=headers)
    with _open(req, timeout=60) as resp:
        body = resp.read(MAX_BYTES + 1)
    if len(body) > MAX_BYTES:
        raise ValueError(f"the answer to {path} is larger than {MAX_BYTES} bytes")
    return json.loads(body)


def _code(text: object) -> str:
    """Text a server chose, as a code span on one line, so it cannot mention a person or add a
    link in the issue. A blank line would end the span, so every run of spaces and line breaks
    is one space."""
    return "`" + " ".join(str(text).replace("`", "'").split()) + "`"


def pins() -> dict[str, str]:
    """Each pinned path, under its repository's name, and its git object hash."""
    rows = (line.split("\t") for line in PINS.read_text(encoding="utf-8").splitlines())
    return {path: sha for path, sha in rows}


def _pins_of(repository: str) -> dict[str, str]:
    """The pins of one repository, by the path inside it."""
    prefix = f"{repository}/"
    return {
        path.removeprefix(prefix): sha
        for path, sha in pins().items()
        if path.startswith(prefix)
    }


def _blobs(repository: str, ref: str) -> dict[str, str]:
    """Each file of a repository at a ref. A listing GitHub cuts short cannot be compared."""
    answer = _get(f"/{repository}/git/trees/{ref}?recursive=1")
    if answer.get("truncated"):
        raise ValueError(f"GitHub cut short the listing of {repository} at {ref}")
    return {e["path"]: e["sha"] for e in answer["tree"] if e["type"] == "blob"}


def _tag_commit(repository: str, tag: str) -> str:
    """The commit a tag names, through its tag object when it has one."""
    target = _get(f"/{repository}/git/ref/tags/{tag}")["object"]
    if target["type"] == "tag":
        target = _get(f"/{repository}/git/tags/{target['sha']}")["object"]
    return target["sha"]


def _compare(found: dict[str, str], expected: dict[str, str], place: str) -> list[str]:
    """One line for each kind of difference between the pins and a listing."""
    lines = []
    gone = sorted(path for path in expected if path not in found)
    changed = sorted(
        path for path, sha in expected.items() if path in found and found[path] != sha
    )
    for label, paths in (("gone", gone), ("changed", changed)):
        if paths:
            shown = ", ".join(_code(path) for path in paths)
            lines.append(f"- **{len(paths)} pinned files {label} {place}:** {shown}.")
    return lines


def _tags(repository: str) -> set[str]:
    """Every tag of a repository, page by page, so none past the first hundred is missed."""
    tags: set[str] = set()
    for page in range(1, 11):
        found = _get(f"/{repository}/tags?per_page=100&page={page}")
        tags |= {entry["name"] for entry in found}
        if len(found) < 100:
            return tags
    raise ValueError(f"{repository} has over 1000 tags, more than the watch reads")


def check_editions() -> tuple[list[str], bool]:
    """Report any tag or edition folder the pins did not know."""
    tags = _tags(SPEC)
    root = _get(f"/{SPEC}/git/trees/{BRANCH}")["tree"]
    folders = {
        entry["path"]
        for entry in root
        if entry["type"] == "tree" and EDITION_FOLDER.match(entry["path"])
    }
    lines = []
    new_tags = sorted(tags - set(KNOWN_TAGS))
    new_folders = sorted(folders - set(KNOWN_FOLDERS))
    if new_tags:
        shown = ", ".join(_code(tag) for tag in new_tags)
        lines.append(f"- **New tags in the specification's repository:** {shown}.")
    if new_folders:
        shown = ", ".join(_code(folder) for folder in new_folders)
        lines.append(f"- **New edition folders:** {shown}.")
    if lines:
        lines.append(
            "- Read what changed, decide whether the schema moves to it, and move upstream/, "
            "the pins and the schema header together."
        )
        return lines, True
    return ["- No new tag or edition folder in the specification's repository."], False


def check_edition() -> tuple[list[str], bool]:
    """Report whether the edition's tag still names the pinned commit and files."""
    commit = _tag_commit(SPEC, TAG)
    lines = []
    if commit != COMMIT:
        lines.append(
            f"- **The tag {TAG} moved to {_code(commit)}.** Find out why a published "
            "edition moved before trusting the copy in upstream/."
        )
    expected = {
        path: sha for path, sha in _pins_of(SPEC).items() if path.startswith(f"{FOLDER}/")
    }
    lines += _compare(_blobs(SPEC, commit), expected, f"at {TAG}")
    lines += _compare(_blobs(SPEC, BRANCH), expected, f"on {BRANCH}")
    if lines:
        return lines, True
    return [f"- FIXP {EDITION}'s {len(expected)} pinned files are unchanged."], False


def check_licence() -> tuple[list[str], bool]:
    """Report whether the licence on the default branch is the pinned file."""
    root = {e["path"]: e["sha"] for e in _get(f"/{SPEC}/git/trees/{BRANCH}")["tree"]}
    if root.get("LICENSE") != pins()[f"{SPEC}/LICENSE"]:
        return [
            "- **The LICENSE changed on the default branch.** Read what changed, and update "
            "NOTICE if the licence moved."
        ], True
    return ["- The licence on the default branch is the pinned file."], False


# Each check, by the name the report gives it when it cannot finish.
CHECKS = (
    ("new editions", check_editions),
    (f"FIXP {EDITION}", check_edition),
    ("licence", check_licence),
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--report", type=Path, help="Also write the Markdown report to this file"
    )
    args = parser.parse_args(argv)
    lines = [f"- Pinned edition: FIXP {EDITION} at {TAG}."]
    attention = False
    for label, check in CHECKS:
        try:
            found, needs = check()
        # OSError covers a refused or failed request and a timeout, HTTPException and EOFError
        # a connection cut off mid-answer, LookupError and ValueError an answer of another
        # shape or too large.
        except (
            OSError,
            http.client.HTTPException,
            EOFError,
            LookupError,
            ValueError,
        ) as err:
            found = [f"- **The {label} check could not finish: {_code(err)}.**"]
            needs = True
        lines += found
        attention = attention or needs
    text = "\n".join(lines) + "\n"
    print(text, end="")
    if args.report:
        args.report.write_text(text, encoding="utf-8")
    return 1 if attention else 0


if __name__ == "__main__":
    sys.exit(main())
