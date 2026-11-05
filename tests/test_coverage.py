"""Checks the schema against FIXP 1.0's resource files, element by element.

The tests read the SBE schema, the FIX repository file and the Orchestra file with lxml, and
share no table with the schema. Each message must have a class that holds exactly its fields,
in the same order, under the alias that names them, with the same number, type and presence.
Each value list must have an enum with the same values and numbers. What the schema states
otherwise is listed in tests/upstream_departures.yaml with its reason.
"""

from functools import cache

import pytest
import yaml
from linkml_runtime import SchemaView
from lxml import etree

from tests.paths import ORCHESTRA, REPOSITORY, ROOT, SBE_SCHEMA, SCHEMA

SBE = "{http://fixprotocol.io/2016/sbe}"
FIXR = "{http://fixprotocol.io/2020/orchestra/repository}"
DEPARTURES = yaml.safe_load(
    (ROOT / "tests" / "upstream_departures.yaml").read_text(encoding="utf-8")
)


def _parse(path, recover=False):
    parser = etree.XMLParser(
        no_network=True, resolve_entities=False, huge_tree=False, recover=recover
    )
    return etree.parse(str(path), parser).getroot()


@cache
def view():
    return SchemaView(str(SCHEMA))


@cache
def sbe():
    return _parse(SBE_SCHEMA)


@cache
def repository():
    return _parse(REPOSITORY).find("fix")


@cache
def orchestra():
    return _parse(ORCHESTRA, recover=True)


def _departure(kind, file, message, field):
    for entry in DEPARTURES[kind]:
        if (entry["file"], entry["message"], entry["field"]) == (file, message, field):
            return entry
    return None


def _messages():
    """Each concrete message class, by its template id."""
    found = {}
    for name in view().class_descendants("FixpMessage", reflexive=False):
        cls = view().get_class(name)
        found[cls.annotations["sbe_template_id"].value] = cls
    return found


def _fields(cls):
    """A message class's fields in order, without the designator."""
    return [
        view().induced_slot(slot, cls.name)
        for slot in view().class_slots(cls.name)
        if slot != "message_kind"
    ]


def _annotation(element, key):
    """An annotation's value, or None. SchemaView hands some annotations over as a dict and
    others as a JSON object, so both are read."""
    annotations = element.annotations
    found = (
        annotations.get(key)
        if isinstance(annotations, dict)
        else getattr(annotations, key, None)
    )
    if found is None:
        return None
    return found.value if hasattr(found, "value") else found


def _sbe_type_of(slot):
    """The SBE schema's name for a slot's range: an enum's sbe_name or a type's sbe_type."""
    if slot.range in view().all_enums():
        return _annotation(view().get_enum(slot.range), "sbe_name")
    return _annotation(view().get_type(slot.range), "sbe_type")


def test_the_schema_header_names_the_sbe_schema():
    header = view().schema.annotations
    assert header["sbe_package"].value == sbe().get("package")
    assert header["sbe_schema_id"].value == sbe().get("id")
    assert header["sbe_schema_version"].value == sbe().get("version")
    assert header["sbe_byte_order"].value == sbe().get("byteOrder")


def test_every_sbe_message_has_its_class_and_no_other():
    ids = {node.get("id"): node.get("name") for node in sbe().iter(f"{SBE}message")}
    classes = _messages()
    assert set(ids) == set(classes)
    for template_id, name in ids.items():
        assert _annotation(classes[template_id], "sbe_name") == name


@pytest.mark.parametrize(
    "node", list(sbe().iter(f"{SBE}message")), ids=lambda n: n.get("name")
)
def test_each_class_holds_its_sbe_messages_fields(node):
    cls = _messages()[node.get("id")]
    fields = [child for child in node if child.tag in ("field", "data")]
    slots = _fields(cls)
    assert [f.get("name") for f in fields] == [
        next(a for a in s.aliases if a in {f.get("name") for f in fields}) for s in slots
    ]
    for field, slot in zip(fields, slots):
        name = field.get("name")
        assert _annotation(slot, "sbe_field_id") == field.get("id"), name
        departure = _departure("range", SBE_SCHEMA.name, node.get("name"), name)
        if departure:
            assert field.get("type") == departure["file_says"]
            assert slot.range == departure["schema_says"]
        else:
            assert _sbe_type_of(slot) == field.get("type"), name
        if field.tag == "data":
            # SBE always sends a data element, though it may be empty, so it says nothing of
            # whether the message needs a value.
            continue
        file_required = field.get("presence", "required") == "required"
        departure = _departure("presence", SBE_SCHEMA.name, node.get("name"), name)
        if departure:
            assert file_required and not slot.required, name
        else:
            assert bool(slot.required) == file_required, name


def test_every_sbe_type_has_its_type():
    types = sbe().find("types")
    simple = {n.get("name"): n for n in types.findall("type")}
    composite = {n.get("name") for n in types.findall("composite")}
    by_sbe_type = {
        _annotation(t, "sbe_type"): t for t in view().all_types().values()
    }
    # messageHeader is SBE's frame around every message, which this schema leaves to the
    # encoding.
    assert set(simple) | composite - {"messageHeader"} == set(by_sbe_type) - {None}
    for name, node in simple.items():
        assert _annotation(by_sbe_type[name], "sbe_primitive_type") == node.get(
            "primitiveType"
        )


def test_every_sbe_enum_has_its_enum():
    enums = {n.get("name"): n for n in sbe().find("types").findall("enum")}
    by_sbe_name = {
        _annotation(e, "sbe_name"): e
        for e in view().all_enums().values()
        if _annotation(e, "sbe_name")
    }
    assert set(enums) == set(by_sbe_name)
    for name, node in enums.items():
        enum = by_sbe_name[name]
        assert _annotation(enum, "sbe_encoding_type") == node.get("encodingType")
        assert {
            v.get("name"): v.text.strip() for v in node.findall("validValue")
        } == {
            value: _annotation(pv, "sbe_value")
            for value, pv in enum.permissible_values.items()
        }


def _repository_fields(root):
    return {node.get("id"): node for node in root.find("fields").findall("field")}


def _field_values(fields, node):
    """A repository field's values and numbers, through enumDatatype when it borrows them."""
    source = fields[node.get("enumDatatype")] if node.get("enumDatatype") else node
    return {e.get("name"): e.get("value") for e in source.findall("enum")}


def test_every_repository_field_has_its_slot():
    fields = _repository_fields(repository())
    by_id = {}
    for slot in view().all_slots().values():
        found = _annotation(slot, "repository_field_id")
        if found:
            by_id[found] = slot
    assert set(fields) == set(by_id)
    for field_id, node in fields.items():
        slot = by_id[field_id]
        assert node.get("name") in slot.aliases
        assert _annotation(slot, "repository_datatype") == node.get("type")
        values = _field_values(fields, node)
        if values:
            enum = view().get_enum(slot.range)
            assert values == {
                value: _annotation(pv, "sbe_value")
                for value, pv in enum.permissible_values.items()
            }


@pytest.mark.parametrize(
    "node",
    list(repository().find("messages").findall("message")),
    ids=lambda n: n.get("name"),
)
def test_each_class_holds_its_repository_messages_fields(node):
    cls = _messages()[node.get("id")]
    assert _annotation(cls, "sbe_name") == node.get("name")
    refs = node.findall("fieldRef")
    slots = _fields(cls)
    assert [r.get("id") for r in refs] == [
        _annotation(s, "repository_field_id") for s in slots
    ]
    for ref, slot in zip(refs, slots):
        name = ref.get("name")
        assert name in slot.aliases
        file_required = ref.get("required") == "1"
        departure = _departure("presence", REPOSITORY.name, node.get("name"), name)
        if departure:
            assert file_required and not slot.required, name
        else:
            assert bool(slot.required) == file_required, name


def test_the_orchestra_file_is_still_not_well_formed():
    """A mended file fails here, so its coverage below can be read again without recovery."""
    assert DEPARTURES["orchestra_not_well_formed"]
    with pytest.raises(etree.XMLSyntaxError):
        _parse(ORCHESTRA)


def test_the_orchestra_file_agrees_with_the_repository_file():
    """Read in recovery mode, the Orchestra file gives the same fields, code sets, messages
    and presence as the repository file, so the tests above cover it too."""
    fields = _repository_fields(repository())
    orchestra_fields = {
        n.get("id"): n for n in orchestra().find(f"{FIXR}fields").findall(f"{FIXR}field")
    }
    assert set(fields) == set(orchestra_fields)
    code_sets = {
        n.get("name"): n
        for n in orchestra().find(f"{FIXR}codeSets").findall(f"{FIXR}codeSet")
    }
    for field_id, node in fields.items():
        other = orchestra_fields[field_id]
        assert other.get("name") == node.get("name")
        values = _field_values(fields, node)
        if values:
            code_set = code_sets[other.get("type")]
            assert {
                c.get("name"): c.get("value") for c in code_set.findall(f"{FIXR}code")
            } == values
        else:
            assert other.get("type") == node.get("type")
    # Recovery ends the messages element at the stray closing tag, so the later messages are
    # found wherever the parser put them.
    messages = {n.get("id"): n for n in orchestra().iter(f"{FIXR}message")}
    for node in repository().find("messages").findall("message"):
        other = messages[node.get("id")]
        assert other.get("name") == node.get("name")
        assert [
            (r.get("id"), r.get("presence") == "required")
            for r in other.iter(f"{FIXR}fieldRef")
        ] == [(r.get("id"), r.get("required") == "1") for r in node.findall("fieldRef")]


def test_every_departure_is_still_needed():
    """Each listed departure names a field the files really state otherwise; the tests above
    would pass on a stale entry, so this one does not."""
    files = {SBE_SCHEMA.name: sbe(), REPOSITORY.name: repository()}
    for entry in DEPARTURES["presence"] + DEPARTURES["range"]:
        root = files[entry["file"]]
        if entry["file"] == SBE_SCHEMA.name:
            message = next(
                n for n in root.iter(f"{SBE}message") if n.get("name") == entry["message"]
            )
            field = next(n for n in message if n.get("name") == entry["field"])
            said = (
                field.get("presence", "required")
                if entry in DEPARTURES["presence"]
                else field.get("type")
            )
        else:
            message = next(
                n
                for n in root.find("messages").findall("message")
                if n.get("name") == entry["message"]
            )
            field = next(
                n for n in message.findall("fieldRef") if n.get("name") == entry["field"]
            )
            said = "required" if field.get("required") == "1" else "optional"
        assert said == entry["file_says"], entry
