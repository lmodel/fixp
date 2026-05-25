"""Structural schema tests.

Exercises the generated LinkML schema directly to catch regressions in:
- Schema metadata (id, prefixes, default ranges).
- FIXP session-message class graph (every concrete message inherits from
  ``FixpSessionMessage`` and exposes the right required slots).
- Enum permissible-value sets.
- SBE composite shape (incl. the ``schema_version`` rename that disambiguates
  ``SbeMessageHeaderComposite.version`` from the top-level ``version`` slot).
- SSSOM overlay state — at least one mapping must be present for each
  target vocabulary so we catch broken overlays at test time.
"""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml

SCHEMA_PATH = Path(__file__).parent.parent / "src" / "fixp" / "schema" / "fixp.yaml"

EXPECTED_SESSION_MESSAGES = {
    "Negotiate",
    "NegotiationResponse",
    "NegotiationReject",
    "Topic",
    "Establish",
    "EstablishmentAck",
    "EstablishmentReject",
    "Sequence",
    "Context",
    "UnsequencedHeartbeat",
    "RetransmitRequest",
    "Retransmission",
    "RestransmitReject",
    "Terminate",
    "FinishedSending",
    "FinishedReceiving",
}


@pytest.fixture(scope="module")
def schema() -> dict:
    with SCHEMA_PATH.open() as fh:
        return yaml.safe_load(fh)


# --- Header --------------------------------------------------------------- #

def test_schema_id_and_name(schema: dict) -> None:
    assert schema["id"] == "https://w3id.org/lmodel/fixp"
    assert schema["name"] == "fixp"
    assert schema["default_prefix"] == "fixp"
    assert schema["default_range"] == "string"


def test_own_prefix_iri_matches_id(schema: dict) -> None:
    """Skill rule: the own prefix IRI must equal ``id`` + ``/``."""
    expected = schema["id"].rstrip("/") + "/"
    assert schema["prefixes"]["fixp"] == expected


def test_prefix_keys_are_ncnames(schema: dict) -> None:
    import re

    for key in schema.get("prefixes", {}):
        assert re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key), (
            f"prefix key {key!r} is not a valid NCName (no hyphens allowed)"
        )


# --- Class graph ---------------------------------------------------------- #

def test_all_session_messages_present(schema: dict) -> None:
    classes = schema["classes"]
    missing = EXPECTED_SESSION_MESSAGES - classes.keys()
    assert not missing, f"missing message classes: {missing}"


@pytest.mark.parametrize("cls_name", sorted(EXPECTED_SESSION_MESSAGES))
def test_session_messages_inherit_base(schema: dict, cls_name: str) -> None:
    cls = schema["classes"][cls_name]
    assert cls.get("is_a") == "FixpSessionMessage", (
        f"{cls_name} must inherit from FixpSessionMessage"
    )
    assert "fixp_session_messages" in (cls.get("in_subset") or []), (
        f"{cls_name} must be tagged in_subset: fixp_session_messages"
    )


@pytest.mark.parametrize(
    ("cls_name", "required_slots"),
    [
        ("Negotiate", {"session_id", "timestamp", "client_flow"}),
        ("NegotiationResponse", {"session_id", "request_timestamp", "server_flow"}),
        ("NegotiationReject", {"session_id", "request_timestamp", "negotiation_reject_code"}),
        ("Establish", {"session_id", "timestamp", "keepalive_interval"}),
        ("EstablishmentReject", {"session_id", "request_timestamp", "establishment_reject_code"}),
        ("Sequence", {"next_seq_no"}),
        ("Context", {"session_id", "next_seq_no"}),
        ("Terminate", {"session_id"}),
        ("RetransmitRequest", {"session_id", "timestamp", "from_seq_no", "count"}),
    ],
)
def test_session_message_required_slots(
    schema: dict, cls_name: str, required_slots: set[str]
) -> None:
    cls = schema["classes"][cls_name]
    slot_usage = cls.get("slot_usage") or {}
    actual = {
        name for name, body in slot_usage.items()
        if isinstance(body, dict) and body.get("required") is True
    }
    assert required_slots <= actual, (
        f"{cls_name}: expected required slots {required_slots} "
        f"to be a subset of {actual}"
    )


def test_session_messages_use_slots_not_attributes(schema: dict) -> None:
    """All FIXP session messages must declare fields via the schema-level
    ``slots:`` registry + ``slot_usage:`` refinements, never as class-local
    ``attributes:`` (per linkml-schema skill, and to ensure ``range`` is
    inherited from the top-level slot definition)."""
    for cls_name in EXPECTED_SESSION_MESSAGES:
        cls = schema["classes"][cls_name]
        assert "attributes" not in cls, (
            f"{cls_name} declares attributes:; FIXP session messages must "
            "use slots: + slot_usage: instead"
        )


# --- Enums ---------------------------------------------------------------- #

@pytest.mark.parametrize(
    ("enum_name", "expected_values"),
    [
        ("ClientFlowCodeSet", {"RECOVERABLE", "IDEMPOTENT", "UNSEQUENCED", "NONE"}),
        ("FlowCodeSet", {"RECOVERABLE", "IDEMPOTENT"}),
        (
            "TerminationCodeCodeSet",
            {
                "FINISHED",
                "UNSPECIFIED_ERROR",
                "RE_REQUEST_OUT_OF_BOUNDS",
                "RE_REQUEST_IN_PROGRESS",
            },
        ),
        (
            "EstablishmentRejectCodeCodeSet",
            {
                "UNNEGOTIATED",
                "ALREADY_ESTABLISHED",
                "SESSION_BLOCKED",
                "KEEPALIVE_INTERVAL",
                "CREDENTIALS",
                "UNSPECIFIED",
            },
        ),
    ],
)
def test_enum_permissible_values(
    schema: dict, enum_name: str, expected_values: set[str]
) -> None:
    enum = schema["enums"][enum_name]
    actual = set((enum.get("permissible_values") or {}).keys())
    assert actual == expected_values, (
        f"{enum_name}: permissible_values mismatch; "
        f"missing={expected_values - actual} extra={actual - expected_values}"
    )


# --- SBE composite rename ------------------------------------------------- #

def test_sbe_message_header_uses_schema_version(schema: dict) -> None:
    """The SBE ``messageHeader.version`` member would shadow the top-level
    ``version`` slot if emitted verbatim (different range, breaks
    inheritance). The generator renames it to ``schema_version`` and
    preserves the wire name in an annotation."""
    cls = schema["classes"]["SbeMessageHeaderComposite"]
    attrs = cls["attributes"]
    assert "schema_version" in attrs, (
        "SbeMessageHeaderComposite must expose 'schema_version' (the renamed "
        "SBE 'version' member)"
    )
    assert "version" not in attrs, (
        "SbeMessageHeaderComposite must NOT expose 'version' (would shadow "
        "the top-level 'version' slot)"
    )
    annos = attrs["schema_version"].get("annotations") or {}
    assert annos.get("sbe_member_name") == "version", (
        "schema_version must carry sbe_member_name: version to preserve the "
        "on-wire SBE field identity"
    )
    assert attrs["schema_version"].get("range") == "integer"


# --- SSSOM overlay state -------------------------------------------------- #

KNOWN_MAPPING_PREFIXES = (
    "common_domain_model:",
    "fix_orchestra:",
    "fix_sbe:",
    "fluxnova_bpm_platform:",
    "gist_linkml:",
)


def _walk_mapping_curies(node):
    """Yield every CURIE found under *_mappings keys anywhere in the schema."""
    if isinstance(node, dict):
        for k, v in node.items():
            if isinstance(k, str) and k.endswith("_mappings") and isinstance(v, list):
                for item in v:
                    if isinstance(item, str):
                        yield item
            else:
                yield from _walk_mapping_curies(v)
    elif isinstance(node, list):
        for item in node:
            yield from _walk_mapping_curies(item)


@pytest.mark.parametrize("prefix", KNOWN_MAPPING_PREFIXES)
def test_sssom_overlay_present(schema: dict, prefix: str) -> None:
    """After ``just apply-sssom-overlay`` runs, the schema must contain at
    least one mapping for each curated target vocabulary; otherwise the
    overlay is silently broken."""
    found = [c for c in _walk_mapping_curies(schema) if c.startswith(prefix)]
    assert found, f"no SSSOM mappings found with prefix {prefix!r}"


# --- URI resolvability ---------------------------------------------------- #

ALLOWED_IDENTITY_PREFIXES = ("fixp:", "dcterms:", "dc:", "rdfs:", "schema:", "skos:")


def test_class_uris_use_own_or_known_prefix(schema: dict) -> None:
    bad = []
    for name, body in schema["classes"].items():
        uri = body.get("class_uri")
        if uri and not uri.startswith(ALLOWED_IDENTITY_PREFIXES):
            bad.append((name, uri))
    assert not bad, f"class_uri must use own or known prefix: {bad}"


def test_slot_uris_use_own_or_known_prefix(schema: dict) -> None:
    bad = []
    for name, body in (schema.get("slots") or {}).items():
        uri = (body or {}).get("slot_uri")
        if uri and not uri.startswith(ALLOWED_IDENTITY_PREFIXES):
            bad.append((name, uri))
    assert not bad, f"slot_uri must use own or known prefix: {bad}"


def test_enum_uris_use_own_prefix(schema: dict) -> None:
    bad = []
    for name, body in schema["enums"].items():
        uri = body.get("enum_uri")
        if uri and not uri.startswith("fixp:"):
            bad.append((name, uri))
    assert not bad, f"enum_uri must use own prefix: {bad}"
