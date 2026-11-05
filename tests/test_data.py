"""Data tests: every example against the JSON Schema the validator generates."""

import json
from functools import cache

import jsonschema
import pytest
import yaml
from linkml.generators.jsonschemagen import JsonSchemaGenerator
from linkml.validator import validate
from linkml_runtime import SchemaView

from tests.paths import DATA, SCHEMA

VALID = sorted((DATA / "valid").glob("*.yaml"))
INVALID = sorted((DATA / "invalid").glob("*.yaml"))


@cache
def definitions():
    """The class definitions of the JSON Schema that linkml-validate generates. Generating it
    once keeps the run short; test_validator_agrees checks that linkml-validate gives the same
    answers."""
    generator = JsonSchemaGenerator(
        str(SCHEMA), mergeimports=True, include_range_class_descendants=True
    )
    return json.loads(generator.serialize())["$defs"]


def errors(instance, class_name):
    schema = {"$ref": f"#/$defs/{class_name}", "$defs": definitions()}
    validator = jsonschema.validators.validator_for(schema)(schema)
    return list(validator.iter_errors(instance))


def pointer(error):
    return "/" + "/".join(str(part) for part in error.absolute_path)


def class_of(path):
    return path.stem.split("-")[0]


def fails_at(path):
    first = path.read_text(encoding="utf-8").splitlines()[0]
    assert first.startswith("# Fails at: "), (
        f"{path.name}: the first line names where it fails"
    )
    return first.removeprefix("# Fails at: ").strip()


def places(error):
    """Where an error points: its own place or, for an anyOf that no branch met, the places
    inside the one branch that is not null. A choice among real alternatives stays where it is."""
    if error.validator != "anyOf" or not error.context:
        return {pointer(error)}
    branches = {}
    for sub in error.context:
        branches.setdefault(sub.relative_schema_path[0], []).append(sub)
    real = [
        subs
        for subs in branches.values()
        if not any(s.validator == "type" and s.validator_value == "null" for s in subs)
    ]
    if len(real) != 1:
        return {pointer(error)}
    found = set()
    for sub in real[0]:
        found |= places(sub)
    return found or {pointer(error)}


def test_the_example_folders_hold_examples():
    """The parametrized tests below pass on an empty folder, so this one does not."""
    assert len(VALID) >= 26, len(VALID)
    assert len(INVALID) >= 47, len(INVALID)


@pytest.mark.parametrize("path", VALID, ids=lambda p: p.stem)
def test_valid_examples_validate(path):
    instance = yaml.safe_load(path.read_text(encoding="utf-8"))
    found = errors(instance, class_of(path))
    assert not found, [f"{pointer(e)}: {e.message[:200]}" for e in found]


@pytest.mark.parametrize("path", INVALID, ids=lambda p: p.stem)
def test_counter_examples_fail_where_they_say(path):
    """Each counter-example fails at the place its first line names, and nowhere else but on
    the way to it, so a file that starts failing for another reason fails this test."""
    where = fails_at(path)
    found = errors(yaml.safe_load(path.read_text(encoding="utf-8")), class_of(path))
    assert found, "it validates"
    reached = set().union(*(places(e) for e in found))
    report = [f"{pointer(e)}: {e.message[:200]}" for e in found]
    assert where in reached, (sorted(reached), report)
    on_the_way = {
        p for p in reached if where == p or where.startswith(p.rstrip("/") + "/")
    }
    assert reached == on_the_way, (sorted(reached - on_the_way), report)


def test_validator_agrees():
    """linkml-validate, which the README tells a user to run, accepts a valid example and
    rejects a counter-example at the same place."""
    good = DATA / "valid" / "FixpExchange-recoverable-session.yaml"
    report = validate(yaml.safe_load(good.read_text()), SCHEMA, "FixpExchange")
    assert not report.results, [r.message for r in report.results]
    bad = DATA / "invalid" / "FixpTopic-unsequenced-flow.yaml"
    report = validate(yaml.safe_load(bad.read_text()), SCHEMA, "FixpTopic")
    assert report.results


def test_every_concrete_class_has_an_example():
    """Each class a record can hold has a valid example."""
    view = SchemaView(str(SCHEMA))
    concrete = {
        name
        for name, cls in view.all_classes().items()
        if not cls.abstract and not cls.mixin
    }
    assert concrete == {class_of(path) for path in VALID}
