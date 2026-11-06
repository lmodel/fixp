"""Holds each rule of tests/fixp_rules.py to a counter-example of its own.

A change to one of the valid exchanges breaks one rule, and the test asserts the only finding
is that rule at that place. A rule that cannot see its fault fails here, and so does one that
sees more than it should. Other changes make a step the specification allows, often one that
appendix A shows, and those must break no rule.
"""

import copy
import inspect
import re

import pytest
import yaml

from tests import fixp_rules
from tests.fixp_rules import rule_errors
from tests.paths import DATA
from tests.test_data import errors as schema_errors

EXCHANGES = {
    path.stem.removeprefix("FixpExchange-"): yaml.safe_load(
        path.read_text(encoding="utf-8")
    )
    for path in sorted((DATA / "valid").glob("FixpExchange-*.yaml"))
}


def _step(record, kind, sent_by=None, nth=0):
    """The index of the nth step that carries a message of this kind."""
    found = [
        i
        for i, step in enumerate(record["exchange_steps"])
        if step.get("fixp_message", {}).get("message_kind") == kind
        and (sent_by is None or step["sent_by"] == sent_by)
    ]
    return found[nth]


def _message(record, kind, sent_by=None, nth=0):
    return record["exchange_steps"][_step(record, kind, sent_by, nth)]["fixp_message"]


def _insert(record, index, step):
    record["exchange_steps"].insert(index, step)


def _wrong_sender(r):
    _insert(
        r,
        2,
        {
            "sent_by": "server",
            "fixp_message": copy.deepcopy(_message(r, "FixpNegotiate")),
        },
    )


def _topic_on_point_to_point(r):
    _insert(
        r,
        4,
        {
            "sent_by": "server",
            "fixp_message": {
                "message_kind": "FixpTopic",
                "session_id": _message(r, "FixpNegotiate")["session_id"],
                "flow": "Idempotent",
                "topic_classification": "RVMtRlVU",
            },
        },
    )


def _heartbeat_on_recoverable(r):
    _insert(
        r,
        4,
        {
            "sent_by": "client",
            "fixp_message": {"message_kind": "FixpUnsequencedHeartbeat"},
        },
    )


def _response_with_other_timestamp(r):
    _message(r, "FixpNegotiationResponse")["request_timestamp"] += 1


def _ack_without_establish(r):
    del r["exchange_steps"][_step(r, "FixpEstablish")]


def _establish_before_response(r):
    steps = r["exchange_steps"]
    response = steps.pop(_step(r, "FixpNegotiationResponse"))
    steps.insert(_step(r, "FixpEstablishmentAck"), response)


def _application_before_ack(r):
    _insert(
        r,
        _step(r, "FixpEstablishmentAck"),
        {"sent_by": "client", "application_message_count": 1},
    )


def _second_retransmit_request(r):
    index = _step(r, "FixpRetransmitRequest")
    _insert(r, index + 1, copy.deepcopy(r["exchange_steps"][index]))


def _retransmit_out_of_bounds(r):
    _message(r, "FixpRetransmitRequest")["message_count"] = 9


def _message_after_terminate(r):
    r["exchange_steps"].append(
        {
            "sent_by": "client",
            "fixp_message": {"message_kind": "FixpSequence", "next_seq_no": 6},
        }
    )


def _finished_receiving_first(r):
    steps = r["exchange_steps"]
    index = _step(r, "FixpFinishedReceiving", "server")
    steps[index - 1], steps[index] = steps[index], steps[index - 1]


def _application_after_finished_sending(r):
    _insert(
        r,
        _step(r, "FixpFinishedSending", "client") + 1,
        {"sent_by": "client", "application_message_count": 1},
    )


def _no_last_seq_no(r):
    del _message(r, "FixpFinishedSending", "client")["last_seq_no"]


def _two_none_flows(r):
    del r["exchange_steps"][2:]
    _message(r, "FixpNegotiate")["client_flow"] = "None"
    _message(r, "FixpNegotiationResponse")["server_flow"] = "None"


def _second_session_id(r):
    # Only this message is at fault: the ones after it name the session again.
    _message(r, "FixpFinishedSending", "client")["session_id"] = (
        "9531985d-5d9d-49f8-9818-e811892f902b"
    )


def _request_for_another_session(r):
    """A request that names another session, as a multicast's recovery session sends, or as in
    appendix A's unknown-session dialog, and the reject that repeats its identifier."""
    other = "9531985d-5d9d-49f8-9818-e811892f902b"
    index = _step(r, "FixpRetransmitRequest")
    r["exchange_steps"][index:index] = [
        {
            "sent_by": "client",
            "fixp_message": {
                "message_kind": "FixpRetransmitRequest",
                "session_id": other,
                "request_time": 1793865600900000000,
                "from_seq_no": 1,
                "message_count": 1,
            },
        },
        {
            "sent_by": "server",
            "fixp_message": {
                "message_kind": "FixpRetransmitReject",
                "session_id": other,
                "request_timestamp": 1793865600900000000,
                "retransmit_reject_code": "InvalidSession",
            },
        },
    ]


def _last_seq_no_beyond_the_flow(r):
    _message(r, "FixpFinishedSending", "client")["last_seq_no"] = 9


def _application_before_sequence(r):
    del r["exchange_steps"][_step(r, "FixpSequence", "client")]


def _context_on_one_session(r):
    message = _message(r, "FixpSequence", "client")
    message["message_kind"] = "FixpContext"
    message["session_id"] = _message(r, "FixpNegotiate")["session_id"]


def _sequence_when_multiplexed(r):
    message = _message(r, "FixpContext", "server")
    message["message_kind"] = "FixpSequence"
    del message["session_id"]


def _client_on_multicast(r):
    r["exchange_steps"][_step(r, "FixpMessageTemplate")]["sent_by"] = "client"


def _negotiate_on_multicast(r):
    _insert(
        r,
        1,
        {
            "sent_by": "publisher",
            "fixp_message": {
                "message_kind": "FixpNegotiate",
                "session_id": _message(r, "FixpTopic")["session_id"],
                "request_time": 1793865600000000000,
                "client_flow": "Idempotent",
            },
        },
    )


def _sequence_before_topic(r):
    steps = r["exchange_steps"]
    topic = steps.pop(_step(r, "FixpTopic"))
    steps.insert(_step(r, "FixpSequence") + 1, topic)


def _not_applied_for_recoverable(r):
    del r["exchange_steps"][_step(r, "FixpApplied")]
    _message(r, "FixpNegotiate")["client_flow"] = "Recoverable"


def _new_messages_in_a_resent_batch(r):
    # The Retransmission announces two resent messages; a third is a new one with no Sequence.
    r["exchange_steps"][_step(r, "FixpRetransmission") + 1][
        "application_message_count"
    ] = 3
    _message(r, "FixpFinishedSending", "server")["last_seq_no"] = 5


def _request_during_a_batch(r):
    request = copy.deepcopy(_message(r, "FixpRetransmitRequest"))
    request["request_time"] += 1
    _insert(
        r,
        _step(r, "FixpRetransmission") + 1,
        {"sent_by": "client", "fixp_message": request},
    )


def _application_after_finished_receiving(r):
    # The server's Sequence comes first, so its new message breaks no rule but this one.
    index = _step(r, "FixpFinishedReceiving", "server") + 1
    r["exchange_steps"][index:index] = [
        {
            "sent_by": "server",
            "fixp_message": {"message_kind": "FixpSequence", "next_seq_no": 5},
        },
        {"sent_by": "server", "application_message_count": 1},
    ]
    _message(r, "FixpFinishedSending", "server")["last_seq_no"] = 5


def _sequence_after_finished_sending(r):
    _insert(
        r,
        _step(r, "FixpFinishedSending", "client") + 1,
        {
            "sent_by": "client",
            "fixp_message": {"message_kind": "FixpSequence", "next_seq_no": 4},
        },
    )


def _application_on_a_none_flow(r):
    _message(r, "FixpNegotiate")["client_flow"] = "None"


def _multicast_numbered_from_zero(r):
    _message(r, "FixpSequence")["next_seq_no"] = 0


def _establish_after_finalization(r):
    establish = copy.deepcopy(_message(r, "FixpEstablish"))
    establish["request_time"] = 1793865700000000000
    r["exchange_steps"].append({"sent_by": "client", "fixp_message": establish})


def _bound_again(r):
    """Appendix A's graceful termination: the client binds the session to a new transport and
    both flows go on from where they were."""
    session_id = _message(r, "FixpNegotiate")["session_id"]
    r["exchange_steps"] += [
        {
            "sent_by": "client",
            "fixp_message": {
                "message_kind": "FixpEstablish",
                "session_id": session_id,
                "request_time": 1793869200000000000,
                "keepalive_interval": 1000,
            },
        },
        {
            "sent_by": "server",
            "fixp_message": {
                "message_kind": "FixpEstablishmentAck",
                "session_id": session_id,
                "request_timestamp": 1793869200000000000,
                "keepalive_interval": 1000,
                "next_seq_no": 3,
            },
        },
        {
            "sent_by": "client",
            "fixp_message": {"message_kind": "FixpSequence", "next_seq_no": 6},
        },
        {"sent_by": "client", "application_message_count": 1},
        {
            "sent_by": "server",
            "fixp_message": {"message_kind": "FixpSequence", "next_seq_no": 3},
        },
        {
            "sent_by": "server",
            "fixp_message": {
                "message_kind": "FixpApplied",
                "from_seq_no": 6,
                "message_count": 1,
            },
        },
    ]


def _request_below_next_seq_no(r):
    """Appendix A's request-limit dialog: the server's flow resumes at 1000, and the client asks
    for numbers below it before any message of the server's arrives."""
    session_id = _message(r, "FixpNegotiate")["session_id"]
    _message(r, "FixpEstablishmentAck")["next_seq_no"] = 1000
    _message(r, "FixpSequence", "server")["next_seq_no"] = 1000
    index = _step(r, "FixpSequence", "server") + 1
    _insert(
        r,
        index,
        {
            "sent_by": "server",
            "fixp_message": {
                "message_kind": "FixpRetransmitReject",
                "session_id": session_id,
                "request_timestamp": 1793865601000000000,
                "retransmit_reject_code": "RequestLimitExceeded",
            },
        },
    )
    _insert(
        r,
        index,
        {
            "sent_by": "client",
            "fixp_message": {
                "message_kind": "FixpRetransmitRequest",
                "session_id": session_id,
                "request_time": 1793865601000000000,
                "from_seq_no": 1,
                "message_count": 999,
            },
        },
    )


def _resent_after_finished_sending(r):
    """Appendix A's finishing on a recoverable flow: the server finds a gap from last_seq_no
    and gets the message back before it answers with FinishedReceiving."""
    session_id = _message(r, "FixpNegotiate")["session_id"]
    index = _step(r, "FixpFinishedSending", "client") + 1
    r["exchange_steps"][index:index] = [
        {
            "sent_by": "server",
            "fixp_message": {
                "message_kind": "FixpRetransmitRequest",
                "session_id": session_id,
                "request_time": 1793865602000000000,
                "from_seq_no": 3,
                "message_count": 1,
            },
        },
        {
            "sent_by": "client",
            "fixp_message": {
                "message_kind": "FixpRetransmission",
                "session_id": session_id,
                "request_timestamp": 1793865602000000000,
                "next_seq_no": 3,
                "message_count": 1,
            },
        },
        {"sent_by": "client", "application_message_count": 1},
    ]


def _new_messages_behind_a_sequence(r):
    """Section 4's interleaving: after the resent batch, a Sequence brings the flow back to new
    messages."""
    index = _step(r, "FixpRetransmission") + 2
    r["exchange_steps"][index:index] = [
        {
            "sent_by": "server",
            "fixp_message": {"message_kind": "FixpSequence", "next_seq_no": 5},
        },
        {"sent_by": "server", "application_message_count": 1},
    ]
    _message(r, "FixpFinishedSending", "server")["last_seq_no"] = 5


# Each case: the exchange, the change, the rule it breaks and the step where it shows.
CASES = {
    "sent-by": ("recoverable-session", _wrong_sender, 2),
    "sent-by on a multicast": ("multicast", _client_on_multicast, 1),
    "session-kind": ("recoverable-session", _topic_on_point_to_point, 4),
    "session-kind on a multicast": ("multicast", _negotiate_on_multicast, 1),
    "flow-type": ("recoverable-session", _heartbeat_on_recoverable, 4),
    "flow-type of the peer": ("idempotent-orders", _not_applied_for_recoverable, 7),
    "request-timestamp": ("recoverable-session", _response_with_other_timestamp, 1),
    "request-timestamp with no request": (
        "recoverable-session",
        _ack_without_establish,
        2,
    ),
    "negotiate-first": ("recoverable-session", _establish_before_response, 1),
    "negotiate-first after finalization": (
        "recoverable-session",
        _establish_after_finalization,
        17,
    ),
    "established-first": ("multiplexed", _application_before_ack, 3),
    "one-retransmit-request": ("recoverable-session", _second_retransmit_request, 9),
    "one-retransmit-request during a batch": (
        "recoverable-session",
        _request_during_a_batch,
        10,
    ),
    "retransmit-in-bounds": ("recoverable-session", _retransmit_out_of_bounds, 8),
    "nothing-after-terminate": ("idempotent-orders", _message_after_terminate, 11),
    "finished-receiving-after-finished-sending": (
        "recoverable-session",
        _finished_receiving_first,
        11,
    ),
    "no-application-after-finished-sending": (
        "recoverable-session",
        _application_after_finished_sending,
        12,
    ),
    "no-application-after-finished-receiving": (
        "recoverable-session",
        _application_after_finished_receiving,
        14,
    ),
    "heartbeat-after-finished-sending": (
        "recoverable-session",
        _sequence_after_finished_sending,
        12,
    ),
    "last-seq-no": ("recoverable-session", _no_last_seq_no, 11),
    "last-seq-no beyond the flow": (
        "recoverable-session",
        _last_seq_no_beyond_the_flow,
        11,
    ),
    "one-none-flow": ("recoverable-session", _two_none_flows, 1),
    "no-application-on-none-flow": ("multiplexed", _application_on_a_none_flow, 5),
    "session-id": ("recoverable-session", _second_session_id, 11),
    "sequence-before-sequenced": (
        "recoverable-session",
        _application_before_sequence,
        4,
    ),
    "sequence-after-retransmission": (
        "recoverable-session",
        _new_messages_in_a_resent_batch,
        10,
    ),
    "context-when-multiplexed": ("recoverable-session", _context_on_one_session, 4),
    "context-when-multiplexed on a shared transport": (
        "multiplexed",
        _sequence_when_multiplexed,
        6,
    ),
    "topic-first": ("multicast", _sequence_before_topic, 1),
    "multicast-starts-at-one": ("multicast", _multicast_numbered_from_zero, 2),
}

# Each case: the exchange, and a change to it that the specification allows.
KEPT = {
    "a session bound again after Terminate": ("idempotent-orders", _bound_again),
    "a request below the peer's NextSeqNo": (
        "idempotent-orders",
        _request_below_next_seq_no,
    ),
    "messages resent after FinishedSending": (
        "recoverable-session",
        _resent_after_finished_sending,
    ),
    "new messages behind a Sequence after resent ones": (
        "recoverable-session",
        _new_messages_behind_a_sequence,
    ),
    "a request for another session's messages": (
        "recoverable-session",
        _request_for_another_session,
    ),
}


@pytest.mark.parametrize("name", sorted(EXCHANGES))
def test_the_valid_exchanges_keep_every_rule(name):
    assert rule_errors(EXCHANGES[name]) == []


@pytest.mark.parametrize("case", sorted(CASES))
def test_each_rule_catches_its_fault(case):
    name, change, step = CASES[case]
    record = copy.deepcopy(EXCHANGES[name])
    change(record)
    rule = case.split(" ")[0]
    found = [(place, found_rule) for place, found_rule, _ in rule_errors(record)]
    assert found == [(f"/exchange_steps/{step}", rule)], found


@pytest.mark.parametrize("case", sorted(KEPT))
def test_what_the_specification_allows_keeps_every_rule(case):
    """A rule that sees a fault in a step the specification allows fails here. The changed
    exchange must still validate, so the case tests the rules and not a malformed record."""
    name, change = KEPT[case]
    record = copy.deepcopy(EXCHANGES[name])
    change(record)
    assert not schema_errors(record, "FixpExchange")
    assert rule_errors(record) == []


def test_every_rule_has_a_case():
    """A rule the module can report but no case breaks would go untested."""
    source = inspect.getsource(fixp_rules)
    named = set(re.findall(r'\(\s*place,\s*"([a-z-]+)"', source))
    assert len(named) == 22, sorted(named)
    assert named == {case.split(" ")[0] for case in CASES}
