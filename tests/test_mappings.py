"""Checks every mapping the schema states, and every name it shares with the FIX siblings.

A mapping names its target by a CURIE whose prefix the module binds, so a projection raises no
warning. Each target's class must exist in the copy of lmodel/fix-sbe or lmodel/fix-orchestra
in tests/neighbours/, which is that repository's released asset. The annotations that name an
SBE primitive type, byte order or FIX datatype must name a value of fix-sbe's lists. Until the
siblings release, the checks that need their copies are skipped.
"""

import pytest
import yaml
from linkml_runtime import SchemaView

from tests.paths import ROOT, SCHEMA, SCHEMA_DIR

NEIGHBOURS = ROOT / "tests" / "neighbours"
KINDS = (
    "exact_mappings",
    "close_mappings",
    "related_mappings",
    "broad_mappings",
    "narrow_mappings",
)
PREFIX_TO_COPY = {"fix_sbe": "fix-sbe.yaml", "fix_orchestra": "fix-orchestra.yaml"}

# The FIXP files define each message as an SBE message template and as an Orchestra message,
# so a message class is related to both, and the same to neither: a record of those classes
# defines a kind of message, while an instance of FixpMessage is one message.
EXPECTED = {
    ("FixpMessage", "related_mappings", "fix_sbe:SbeMessageV1"),
    ("FixpMessage", "related_mappings", "fix_orchestra:OrchestraMessageV10"),
}


def _modules():
    return {
        path.stem: yaml.safe_load(path.read_text(encoding="utf-8"))
        for path in sorted(SCHEMA_DIR.glob("*.yaml"))
    }


def _stated():
    """Every (module, element, kind, target) the schema states, on any kind of element."""
    for name, module in _modules().items():
        for section in ("classes", "slots", "enums", "types"):
            for element_name, element in (module.get(section) or {}).items():
                for kind in KINDS:
                    for target in (element or {}).get(kind) or []:
                        yield name, element_name, kind, target


def _copy(name):
    path = NEIGHBOURS / name
    if not path.exists():
        pytest.skip(f"tests/neighbours/{name} waits for its repository's release")
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _values(copy, enum):
    return set(copy["enums"][enum]["permissible_values"])


def test_every_mapping_has_a_bound_prefix():
    modules = _modules()
    for name, element, _, target in _stated():
        prefix = target.partition(":")[0]
        assert prefix in modules[name]["prefixes"], (element, target)


def test_the_mappings_are_the_ones_listed():
    assert {
        (element, kind, target) for _, element, kind, target in _stated()
    } == EXPECTED


@pytest.mark.parametrize("prefix", sorted(PREFIX_TO_COPY))
def test_every_target_exists_in_its_neighbour(prefix):
    classes = _copy(PREFIX_TO_COPY[prefix])["classes"]
    missing = {
        target
        for *_, target in _stated()
        if target.startswith(f"{prefix}:") and target.partition(":")[2] not in classes
    }
    assert not missing


def test_the_sbe_annotations_name_fix_sbes_values():
    """A type's primitive type, an enum's encoding type and the schema's byte order are values
    of fix-sbe's SbePrimitiveType and SbeByteOrder."""
    copy = _copy("fix-sbe.yaml")
    view = SchemaView(str(SCHEMA))
    primitives = _values(copy, "SbePrimitiveType")
    for element in [*view.all_types().values(), *view.all_enums().values()]:
        for key in ("sbe_primitive_type", "sbe_encoding_type"):
            found = element.annotations.get(key)
            if found:
                assert found.value in primitives, (element.name, found.value)
    byte_order = view.schema.annotations["sbe_byte_order"].value
    assert byte_order in _values(copy, "SbeByteOrder")


def test_the_repository_datatypes_are_fix_datatypes():
    """Each field's datatype in the FIX repository file is a FIX datatype that fix-sbe lists."""
    datatypes = _values(_copy("fix-sbe.yaml"), "SbeFixDatatype")
    for name, slot in (_modules()["fixp_core"].get("slots") or {}).items():
        found = (slot.get("annotations") or {}).get("repository_datatype")
        if found:
            assert found in datatypes, (name, found)
