"""Checks the upstream watch's decisions against stubbed answers.

scripts/check_upstream_release.py lists the repository through GitHub's API. These tests
replace its one network call, `_get`, with a table of answers, so they run offline. They show
what the report says in each case the watch knows.
"""

import http.client
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
SCRIPT = ROOT / "scripts" / "check_upstream_release.py"


@pytest.fixture
def watch():
    """A fresh copy of the script, so no test sees another's stub."""
    spec = importlib.util.spec_from_file_location("watch_under_test", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _tree(watch, repository, extra=None):
    """A recursive listing of one repository, built from the pins."""
    pinned = {
        path.removeprefix(f"{repository}/"): sha
        for path, sha in watch.pins().items()
        if path.startswith(f"{repository}/")
    }
    pinned.update(extra or {})
    return {"tree": [{"path": p, "type": "blob", "sha": s} for p, s in pinned.items()]}


def _root(watch, repository, folders=()):
    """The top of one repository's default branch, with its licence and any folders."""
    licence = watch.pins()[f"{repository}/LICENSE"]
    entries = [{"path": "LICENSE", "type": "blob", "sha": licence}]
    entries += [
        {"path": name, "type": "tree", "sha": f"tree-{name}"} for name in folders
    ]
    return {"tree": entries}


def _answers(watch):
    """The answers of an unchanged upstream."""
    spec = watch.SPEC
    return {
        f"/{spec}/tags?per_page=100&page=1": [
            {"name": tag} for tag in watch.KNOWN_TAGS
        ],
        f"/{spec}/git/trees/{watch.BRANCH}": _root(watch, spec, watch.KNOWN_FOLDERS),
        f"/{spec}/git/ref/tags/{watch.TAG}": {
            "object": {"type": "commit", "sha": watch.COMMIT}
        },
        f"/{spec}/git/trees/{watch.COMMIT}?recursive=1": _tree(watch, spec),
        f"/{spec}/git/trees/{watch.BRANCH}?recursive=1": _tree(watch, spec),
    }


def _run(watch, answers, capsys, argv=()):
    def fake_get(path):
        answer = answers[path]
        if isinstance(answer, Exception):
            raise answer
        return answer

    watch._get = fake_get
    code = watch.main(list(argv))
    return code, capsys.readouterr().out


def test_an_unchanged_upstream_reports_nothing(watch, capsys):
    code, report = _run(watch, _answers(watch), capsys)
    assert code == 0, report
    assert "**" not in report


def test_a_new_tag_is_reported_and_quoted(watch, capsys):
    answers = _answers(watch)
    answers[f"/{watch.SPEC}/tags?per_page=100&page=1"].append({"name": "v1.1-STANDARD"})
    code, report = _run(watch, answers, capsys)
    assert code == 1
    assert "`v1.1-STANDARD`" in report


def test_a_new_edition_folder_is_reported(watch, capsys):
    answers = _answers(watch)
    answers[f"/{watch.SPEC}/git/trees/{watch.BRANCH}"] = _root(
        watch, watch.SPEC, (*watch.KNOWN_FOLDERS, "v1-1-STANDARD")
    )
    code, report = _run(watch, answers, capsys)
    assert code == 1
    assert "`v1-1-STANDARD`" in report


def test_a_folder_that_names_no_edition_stays_quiet(watch, capsys):
    answers = _answers(watch)
    answers[f"/{watch.SPEC}/git/trees/{watch.BRANCH}"] = _root(
        watch, watch.SPEC, (*watch.KNOWN_FOLDERS, "tools")
    )
    code, report = _run(watch, answers, capsys)
    assert code == 0, report


def test_a_moved_tag_is_reported(watch, capsys):
    answers = _answers(watch)
    moved = "2" * 40
    answers[f"/{watch.SPEC}/git/ref/tags/{watch.TAG}"] = {
        "object": {"type": "commit", "sha": moved}
    }
    answers[f"/{watch.SPEC}/git/trees/{moved}?recursive=1"] = _tree(watch, watch.SPEC)
    code, report = _run(watch, answers, capsys)
    assert code == 1
    assert f"moved to `{moved}`" in report


def test_an_annotated_tag_is_followed(watch, capsys):
    """FIX's tags name commits directly today; an annotated one is read through its object."""
    answers = _answers(watch)
    annotated = "1" * 40
    answers[f"/{watch.SPEC}/git/ref/tags/{watch.TAG}"] = {
        "object": {"type": "tag", "sha": annotated}
    }
    answers[f"/{watch.SPEC}/git/tags/{annotated}"] = {
        "object": {"type": "commit", "sha": watch.COMMIT}
    }
    code, report = _run(watch, answers, capsys)
    assert code == 0, report


def test_a_changed_file_on_the_branch_is_reported_by_path(watch, capsys):
    answers = _answers(watch)
    path = f"{watch.FOLDER}/resources/SBEschemaForFIXP.xml"
    answers[f"/{watch.SPEC}/git/trees/{watch.BRANCH}?recursive=1"] = _tree(
        watch, watch.SPEC, {path: "0" * 40}
    )
    code, report = _run(watch, answers, capsys)
    assert code == 1
    assert f"1 pinned files changed on {watch.BRANCH}" in report
    assert f"`{path}`" in report


def test_a_file_gone_at_the_tag_is_reported_by_path(watch, capsys):
    answers = _answers(watch)
    listing = _tree(watch, watch.SPEC)
    path = f"{watch.FOLDER}/resources/OrchestraForFIXP.xml"
    listing["tree"] = [entry for entry in listing["tree"] if entry["path"] != path]
    answers[f"/{watch.SPEC}/git/trees/{watch.COMMIT}?recursive=1"] = listing
    code, report = _run(watch, answers, capsys)
    assert code == 1
    assert f"1 pinned files gone at {watch.TAG}" in report


def test_a_changed_licence_is_reported(watch, capsys):
    answers = _answers(watch)
    root = answers[f"/{watch.SPEC}/git/trees/{watch.BRANCH}"]
    root["tree"] = [dict(entry) for entry in root["tree"]]
    root["tree"][0]["sha"] = "3" * 40
    code, report = _run(watch, answers, capsys)
    assert code == 1
    assert "The LICENSE changed" in report


def test_a_truncated_listing_cannot_finish(watch, capsys):
    answers = _answers(watch)
    answers[f"/{watch.SPEC}/git/trees/{watch.BRANCH}?recursive=1"]["truncated"] = True
    code, report = _run(watch, answers, capsys)
    assert code == 1
    assert "could not finish" in report


@pytest.mark.parametrize(
    "failure",
    [
        OSError("refused"),
        http.client.RemoteDisconnected("cut"),
        KeyError("tree"),
        ValueError("too large"),
    ],
    ids=lambda e: type(e).__name__,
)
def test_a_failed_request_cannot_finish_and_is_quoted(watch, capsys, failure):
    answers = _answers(watch)
    answers[f"/{watch.SPEC}/tags?per_page=100&page=1"] = failure
    code, report = _run(watch, answers, capsys)
    assert code == 1
    assert "The new editions check could not finish" in report


def test_server_text_cannot_mention_or_link(watch, capsys):
    """A tag's name reaches an issue only as code on one line."""
    answers = _answers(watch)
    answers[f"/{watch.SPEC}/tags?per_page=100&page=1"].append(
        {"name": "@someone\n\n`x`"}
    )
    code, report = _run(watch, answers, capsys)
    assert code == 1
    assert "`@someone 'x'`" in report


def test_a_second_page_of_tags_is_read(watch, capsys):
    answers = _answers(watch)
    first = [{"name": f"v0.0.{n}"} for n in range(100)]
    answers[f"/{watch.SPEC}/tags?per_page=100&page=1"] = first
    answers[f"/{watch.SPEC}/tags?per_page=100&page=2"] = [
        {"name": tag} for tag in watch.KNOWN_TAGS
    ] + [{"name": "v1.1-STANDARD"}]
    code, report = _run(watch, answers, capsys)
    assert code == 1
    assert "`v1.1-STANDARD`" in report


def test_a_redirect_off_the_api_is_refused(watch):
    handler = watch._ApiRedirect()
    with pytest.raises(ValueError, match="leads off"):
        handler.redirect_request(None, None, 302, "Found", {}, "https://example.org/x")
    with pytest.raises(ValueError, match="leads off"):
        handler.redirect_request(
            None, None, 302, "Found", {}, "http://api.github.com/x"
        )


def test_the_report_goes_to_a_file_when_asked(watch, capsys, tmp_path):
    target = tmp_path / "report.md"
    code, report = _run(watch, _answers(watch), capsys, ["--report", str(target)])
    assert code == 0
    assert target.read_text(encoding="utf-8") == report


def test_the_watch_reads_only_github():
    """FIX's site terms bar automated copying, so the watch has no other address."""
    text = SCRIPT.read_text(encoding="utf-8")
    addresses = [part.split('"')[0] for part in text.split("https://")[1:]]
    assert addresses
    assert all(address.startswith("api.github.com") for address in addresses), addresses
