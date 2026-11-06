"""Holds the counts the docs and the bundle give to the schema and the tests they count."""

import inspect
import re

from linkml_runtime import SchemaView

from tests import fixp_rules
from tests.paths import ROOT, SCHEMA

ABOUT = (ROOT / "docs" / "about.md").read_text(encoding="utf-8")
MESSAGES = " ".join(
    (ROOT / "src" / "fixp" / "schema" / "fixp_messages.yaml")
    .read_text(encoding="utf-8")
    .split()
)
RULES_PAGE = (
    ROOT / ".lokf" / "knowledge" / "explanations" / "rules-that-span-an-exchange.md"
).read_text(encoding="utf-8")


def _messages():
    view = SchemaView(str(SCHEMA))
    return [
        view.get_class(name)
        for name in view.class_descendants("FixpMessage", reflexive=False)
    ]


def test_nineteen_messages_two_of_them_application_messages():
    """The messages module says nineteen, seventeen of them session messages."""
    assert "The nineteen messages of FIXP 1.0" in MESSAGES
    assert "the seventeen session messages and the two application messages" in MESSAGES
    found = _messages()
    assert len(found) == 19
    application = {"FixpApplied", "FixpNotApplied"}
    assert application <= {cls.name for cls in found}


def test_seventeen_rules():
    """The bundle's page on the rules says the module reports seventeen."""
    assert "seventeen rules" in RULES_PAGE
    source = inspect.getsource(fixp_rules)
    assert len(set(re.findall(r'\(\s*place,\s*"([a-z-]+)"', source))) == 17


def test_seven_fields_under_another_key():
    """docs/about.md names seven fields whose key is not FIXP's name in snake_case."""
    assert "Seven take a different word" in ABOUT
    view = SchemaView(str(SCHEMA))
    renamed = set()
    for name, slot in view.all_slots().items():
        if slot.annotations.get("sbe_field_id") is None:
            continue
        # The first alias is the specification's name; the rest are the repository file's.
        if name != re.sub(r"(?<!^)(?=[A-Z])", "_", slot.aliases[0]).lower():
            renamed.add(slot.aliases[0])
    assert renamed == {
        "Timestamp",
        "Reason",
        "Classification",
        "Count",
        "EncodingType",
        "Version",
        "Code",
    }
