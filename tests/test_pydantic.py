"""Pydantic model tests.

Exercise the generated pydantic data models (``fixp.datamodel.fixp_pydantic``)
to lock in:
- Successful construction of representative session messages.
- Required-field omission raises ``ValidationError``.
- Enum coercion: strings are parsed into the right ``Enum`` member.
- Cross-message round-trips via ``model_dump_json`` / ``model_validate_json``.
- The SBE composite header uses ``schema_version`` (the renamed ``version``).
"""
from __future__ import annotations

import pytest
from pydantic import ValidationError

from fixp.datamodel import fixp_pydantic as m

SESSION_ID = "550e8400-e29b-41d4-a716-446655440000"
TIMESTAMP = 1716595200000000000


def test_negotiate_construction() -> None:
    msg = m.Negotiate(
        session_id=SESSION_ID,
        timestamp=TIMESTAMP,
        client_flow="RECOVERABLE",
    )
    assert msg.session_id == SESSION_ID
    assert msg.timestamp == TIMESTAMP
    # str-Enums compare equal to their string value.
    assert msg.client_flow == "RECOVERABLE"
    assert msg.client_flow == m.ClientFlowFieldEnum.Recoverable


def test_negotiate_missing_required_raises() -> None:
    with pytest.raises(ValidationError):
        m.Negotiate(session_id=SESSION_ID, client_flow="RECOVERABLE")


def test_negotiate_bad_enum_value_raises() -> None:
    with pytest.raises(ValidationError):
        m.Negotiate(
            session_id=SESSION_ID,
            timestamp=TIMESTAMP,
            client_flow="FAST",  # not in ClientFlowCodeSet
        )


@pytest.mark.parametrize(
    "code",
    [
        "FINISHED",
        "UNSPECIFIED_ERROR",
        "RE_REQUEST_OUT_OF_BOUNDS",
        "RE_REQUEST_IN_PROGRESS",
    ],
)
def test_terminate_accepts_all_termination_codes(code: str) -> None:
    msg = m.Terminate(session_id=SESSION_ID, termination_code=code)
    assert msg.termination_code == code


def test_terminate_bad_termination_code_raises() -> None:
    with pytest.raises(ValidationError):
        m.Terminate(session_id=SESSION_ID, termination_code="GRACEFUL")


def test_sequence_keepalive() -> None:
    msg = m.Sequence(next_seq_no=42)
    assert msg.next_seq_no == 42


def test_sequence_missing_next_seq_no_raises() -> None:
    with pytest.raises(ValidationError):
        m.Sequence()


def test_context_round_trip_json() -> None:
    msg = m.Context(session_id=SESSION_ID, next_seq_no=7)
    blob = msg.model_dump_json()
    restored = m.Context.model_validate_json(blob)
    assert restored == msg


def test_establish_full() -> None:
    msg = m.Establish(
        session_id=SESSION_ID,
        timestamp=TIMESTAMP,
        keepalive_interval=10,
        next_seq_no=1,
        credentials="dHJhZGVyMTIz",
    )
    assert msg.keepalive_interval == 10
    assert msg.next_seq_no == 1


def test_negotiation_reject_uses_reject_codeset() -> None:
    msg = m.NegotiationReject(
        session_id=SESSION_ID,
        request_timestamp=TIMESTAMP,
        negotiation_reject_code="CREDENTIALS",
        reason="bad token",
    )
    assert msg.negotiation_reject_code == "CREDENTIALS"
    assert msg.negotiation_reject_code == m.NegotiationRejectCodeFieldEnum.Credentials


def test_inheritance_marker() -> None:
    """All concrete session messages must inherit ``FixpSessionMessage``."""
    msg = m.Negotiate(
        session_id=SESSION_ID, timestamp=TIMESTAMP, client_flow="RECOVERABLE"
    )
    assert isinstance(msg, m.FixpSessionMessage)


def test_sbe_message_header_composite_uses_schema_version() -> None:
    """Catches accidental revert of the SBE ``version``→``schema_version``
    rename in the generator."""
    fields = m.SbeMessageHeaderComposite.model_fields
    assert "schema_version" in fields
    assert "version" not in fields
    composite = m.SbeMessageHeaderComposite(
        block_length=0, template_id=1, schema_id=1, schema_version=42
    )
    assert composite.schema_version == 42


def test_session_exchange_aggregates_messages() -> None:
    """``FixpSessionExchange`` is the container; it should accept a list of
    arbitrary session messages and round-trip through pydantic."""
    exchange = m.FixpSessionExchange(
        messages=[
            m.Negotiate(
                session_id=SESSION_ID,
                timestamp=TIMESTAMP,
                client_flow="RECOVERABLE",
            ),
            m.Sequence(next_seq_no=1),
            m.Terminate(session_id=SESSION_ID, termination_code="FINISHED"),
        ]
    )
    assert len(exchange.messages) == 3
