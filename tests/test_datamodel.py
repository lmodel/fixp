"""Checks what the generated models and the JSON-LD context do with the examples.

The Pydantic models and the dataclasses load every valid example, and the messages of an
exchange keep their classes and their order.
"""

import json

import pytest
import rdflib
import yaml
from linkml_runtime.loaders import yaml_loader

from fixp.datamodel import fixp as dataclasses_module
from fixp.datamodel import fixp_pydantic
from tests.paths import DATA, ROOT

CONTEXT = ROOT / "project" / "jsonld" / "fixp.context.jsonld"
NAMESPACE = "https://w3id.org/lmodel/fixp/"
VALID = sorted((DATA / "valid").glob("*.yaml"))


def _class_of(path):
    return path.stem.split("-")[0]


@pytest.mark.parametrize("path", VALID, ids=lambda p: p.stem)
def test_each_example_loads_into_the_pydantic_models(path):
    record = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert getattr(fixp_pydantic, _class_of(path))(**record)


@pytest.mark.parametrize("path", VALID, ids=lambda p: p.stem)
def test_each_example_loads_into_the_dataclasses(path):
    loaded = yaml_loader.load(
        str(path), target_class=getattr(dataclasses_module, _class_of(path))
    )
    assert loaded


def test_an_exchanges_messages_keep_their_class_and_order():
    """The dataclasses pick each message's class from message_kind, in the exchange's order."""
    loaded = yaml_loader.load(
        str(DATA / "valid" / "FixpExchange-recoverable-session.yaml"),
        target_class=dataclasses_module.FixpExchange,
    )
    kinds = [
        type(step.fixp_message).__name__
        for step in loaded.exchange_steps
        if step.fixp_message
    ]
    assert kinds[:4] == [
        "FixpNegotiate",
        "FixpNegotiationResponse",
        "FixpEstablish",
        "FixpEstablishmentAck",
    ]


def test_json_ld_projects_a_key_under_this_schemas_iri():
    """A record joined with the generated context says its facts under fixp's IRIs."""
    context = json.loads(CONTEXT.read_text(encoding="utf-8"))["@context"]
    document = {
        "@context": context,
        "session_id": "6513270e-269e-4d37-b2a7-4de452e6b438",
        "keepalive_interval": 500,
    }
    graph = rdflib.Graph().parse(
        data=json.dumps(document), format="json-ld", base=NAMESPACE
    )
    predicates = {str(p) for _, p, _ in graph}
    assert f"{NAMESPACE}session_id" in predicates
    assert f"{NAMESPACE}keepalive_interval" in predicates
