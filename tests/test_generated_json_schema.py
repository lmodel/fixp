"""Checks the JSON Schema this project commits, as a user of it would read it.

project/jsonschema/fixp.schema.json is what a consumer without LinkML validates with. It is read
here under the draft it declares, and held to the generator's settings in .linkml/generators.yaml.
"""

import json
from functools import cache

import jsonschema
import yaml
from linkml.generators.jsonschemagen import JsonSchemaGenerator

from tests.paths import DATA, ROOT, SCHEMA

COMMITTED = ROOT / "project" / "jsonschema" / "fixp.schema.json"


@cache
def schema():
    return json.loads(COMMITTED.read_text(encoding="utf-8"))


def validator(class_name):
    wrapped = {"$ref": f"#/$defs/{class_name}", "$defs": schema()["$defs"]}
    return jsonschema.validators.validator_for(wrapped)(wrapped)


def _load(name):
    return yaml.safe_load((DATA / "valid" / f"{name}.yaml").read_text(encoding="utf-8"))


def test_the_schema_is_valid_under_the_draft_it_declares():
    jsonschema.validators.validator_for(schema()).check_schema(schema())


def test_the_committed_file_is_the_generators_output():
    """A schema edit without `just gen-project` fails here."""
    settings = yaml.safe_load((ROOT / ".linkml" / "generators.yaml").read_text())
    args = settings["generator_args"]["jsonschema"]
    generated = JsonSchemaGenerator(str(SCHEMA), **args).serialize()
    assert json.loads(generated) == schema()


def test_the_top_of_the_file_is_an_exchange():
    """The root takes an exchange, and refuses any other key."""
    assert schema()["title"] == "fixp"
    assert schema()["additionalProperties"] is False
    assert set(schema()["required"]) == {"id", "session_kind", "exchange_steps"}
    assert not list(
        jsonschema.Draft202012Validator(schema()).iter_errors(
            _load("FixpExchange-recoverable-session")
        )
    )


def test_every_class_is_closed():
    """A key FIXP does not define is refused everywhere."""
    for name, definition in schema()["$defs"].items():
        if definition.get("type") == "object":
            assert definition["additionalProperties"] is False, name


def test_a_message_kind_picks_one_class():
    """Applied and NotApplied hold the same fields, so only message_kind tells them apart."""
    applied = _load("FixpApplied-run")
    assert not list(validator("FixpApplied").iter_errors(applied))
    assert list(validator("FixpNotApplied").iter_errors(applied))


def test_a_fault_deep_in_an_exchange_reaches_the_file():
    """A message's pattern is checked inside an exchange, through the step's message."""
    exchange = _load("FixpExchange-recoverable-session")
    exchange["exchange_steps"][0]["fixp_message"]["session_id"] = "not-a-uuid"
    assert list(validator("FixpExchange").iter_errors(exchange))
