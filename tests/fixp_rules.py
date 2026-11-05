"""The protocol's rules that JSON Schema cannot state.

Each rule compares one step of an exchange with the steps before it: an answer with its
request, a message with the flow types the session negotiated, a sequence number with what
was sent. Most come from the list of protocol violations in section 6 of FIXP 1.0, and each
rule below names its source. They read an exchange as the YAML record the LinkML schema
describes, and read what each message class allows from its annotations.

`rule_errors` returns (place, rule, message) tuples, and tests/test_rules.py holds each rule to
a counter-example.
"""

from __future__ import annotations

from functools import cache

import yaml

from tests.paths import SCHEMA_DIR

SEQUENCED = {"Recoverable", "Idempotent"}
REQUESTS = {
    "FixpNegotiationResponse": "FixpNegotiate",
    "FixpNegotiationReject": "FixpNegotiate",
    "FixpEstablishmentAck": "FixpEstablish",
    "FixpEstablishmentReject": "FixpEstablish",
    "FixpRetransmission": "FixpRetransmitRequest",
    "FixpRetransmitReject": "FixpRetransmitRequest",
}
RETRANSMIT_ANSWERS = {"FixpRetransmission", "FixpRetransmitReject", "FixpTerminate"}
# Applied and NotApplied are application messages: each takes a sequence number.
APPLICATION_MESSAGES = {"FixpApplied", "FixpNotApplied"}


@cache
def message_classes() -> dict[str, dict[str, str]]:
    """Each message class's annotations, read from the schema module."""
    module = yaml.safe_load(
        (SCHEMA_DIR / "fixp_messages.yaml").read_text(encoding="utf-8")
    )
    return {
        name: {key: str(value) for key, value in (cls.get("annotations") or {}).items()}
        for name, cls in module["classes"].items()
    }


class _Session:
    """What the steps so far have shown about the session."""

    def __init__(self, exchange: dict):
        self.kind = exchange.get("session_kind")
        self.multiplexed = bool(exchange.get("multiplexed"))
        self.flows: dict[str, str] = {}
        self.negotiated = False
        self.established = False
        self.terminated: set[str] = set()
        self.finished_sending: set[str] = set()
        self.last_request: dict[tuple[str, str], int] = {}
        self.open_retransmit: set[str] = set()
        self.started: set[str] = set()
        self.next_number: dict[str, int] = {}
        self.highest_sent: dict[str, int] = {}
        self.session_ids: set[str] = set()
        self.topic_seen = False

    def peer(self, party: str) -> str | None:
        return {"client": "server", "server": "client"}.get(party)

    def count_application(
        self, party: str, count: int, place: str, errors: list
    ) -> None:
        if self.flows.get(party) in SEQUENCED and party not in self.started:
            errors.append(
                (
                    place,
                    "sequence-before-sequenced",
                    f"the {party}'s sequenced flow sends an application message before any "
                    "Sequence, Context or Retransmission (section 3)",
                )
            )
        if party in self.next_number:
            first = self.next_number[party]
            self.next_number[party] = first + count
            self.highest_sent[party] = max(
                self.highest_sent.get(party, 0), first + count - 1
            )


def _check_sender(session, name, party, rules, place, errors):
    """sent-by and session-kind: who may send the message, and on which kind of session."""
    allowed = rules.get("fixp_sent_by")
    if session.kind == "multicast":
        if party != "publisher":
            errors.append(
                (
                    place,
                    "sent-by",
                    "only the publisher sends on a multicast (section 5)",
                )
            )
        if rules.get("fixp_multicast") != "true":
            errors.append(
                (
                    place,
                    "session-kind",
                    f"{name} is not used on a multicast (section 6)",
                )
            )
        return
    if party == "publisher":
        errors.append(
            (place, "sent-by", "a point-to-point session has no publisher (section 4)")
        )
    elif allowed in ("client", "server") and party != allowed:
        errors.append(
            (place, "sent-by", f"{name} is sent by the {allowed} (section 4)")
        )
    if "fixp_flow_types" not in rules:
        errors.append(
            (
                place,
                "session-kind",
                f"{name} is not used on a point-to-point session (section 6)",
            )
        )


def _check_flow_type(session, name, party, rules, place, errors):
    """flow-type: a message that concerns one flow suits that flow's type (section 6)."""
    whose = rules.get("fixp_flow_of")
    if not whose or session.kind != "point_to_point":
        return
    owner = party if whose == "own" else session.peer(party)
    flow = session.flows.get(owner)
    if flow and flow not in rules.get("fixp_flow_types", "").split():
        errors.append(
            (
                place,
                "flow-type",
                f"{name} concerns the {owner}'s flow, which is {flow} (section 6)",
            )
        )


def _check_answer(session, name, party, message, place, errors):
    """request-timestamp: an answer repeats the request_time of the request it answers."""
    request = REQUESTS.get(name)
    if not request:
        return
    asked = session.last_request.get((request, session.peer(party) or ""))
    if asked is None:
        errors.append(
            (
                place,
                "request-timestamp",
                f"{name} answers no {request} of the peer (section 4)",
            )
        )
    elif message.get("request_timestamp") != asked:
        errors.append(
            (
                place,
                "request-timestamp",
                f"{name} does not repeat the request_time of the {request} it answers "
                "(section 4)",
            )
        )


def _check_message(session, step, place, errors):
    party = step["sent_by"]
    message = step["fixp_message"]
    name = message["message_kind"]
    rules = message_classes().get(name, {})
    peer = session.peer(party)

    _check_sender(session, name, party, rules, place, errors)
    _check_flow_type(session, name, party, rules, place, errors)
    _check_answer(session, name, party, message, place, errors)

    if "session_id" in message:
        session.session_ids.add(message["session_id"])
        if not session.multiplexed and len(session.session_ids) > 1:
            errors.append(
                (
                    place,
                    "session-id",
                    "a transport that carries one session sees one session_id (section 3)",
                )
            )

    if name == "FixpNegotiate":
        session.flows["client"] = message.get("client_flow")
    elif name == "FixpNegotiationResponse":
        session.flows["server"] = message.get("server_flow")
        session.negotiated = True
        if session.flows.get("client") == "None" and session.flows["server"] == "None":
            errors.append(
                (place, "one-none-flow", "only one flow may be None (section 3)")
            )
    elif name == "FixpTopic":
        session.flows["publisher"] = message.get("flow")
        session.topic_seen = True
    elif name == "FixpEstablish" and not session.negotiated:
        errors.append(
            (
                place,
                "negotiate-first",
                "Establish comes after a NegotiationResponse (section 6)",
            )
        )
    elif name == "FixpEstablishmentAck":
        session.established = True

    if name in ("FixpSequence", "FixpContext", "FixpRetransmission"):
        if session.kind == "multicast" and not session.topic_seen:
            errors.append(
                (place, "topic-first", "a Topic starts a multicast flow (section 5)")
            )
        if name == "FixpSequence" and session.multiplexed:
            errors.append(
                (
                    place,
                    "context-when-multiplexed",
                    "a shared transport takes Context (section 3)",
                )
            )
        if name == "FixpContext" and not session.multiplexed:
            errors.append(
                (
                    place,
                    "context-when-multiplexed",
                    "a transport that carries one session takes Sequence (section 3)",
                )
            )
        if "next_seq_no" in message:
            session.started.add(party)
            session.next_number[party] = message["next_seq_no"]

    if name == "FixpRetransmitRequest":
        if party in session.open_retransmit:
            errors.append(
                (
                    place,
                    "one-retransmit-request",
                    "an earlier RetransmitRequest is still unanswered (section 4)",
                )
            )
        last = message["from_seq_no"] + message["message_count"] - 1
        if last > session.highest_sent.get(peer, 0):
            errors.append(
                (
                    place,
                    "retransmit-in-bounds",
                    "it asks for a sequence number the peer has not sent (section 6)",
                )
            )
        session.open_retransmit.add(party)
    if name in RETRANSMIT_ANSWERS and peer:
        session.open_retransmit.discard(peer)

    if name == "FixpFinishedSending":
        session.finished_sending.add(party)
        if session.flows.get(party) in SEQUENCED and "last_seq_no" not in message:
            errors.append(
                (
                    place,
                    "last-seq-no",
                    f"the {party}'s flow is sequenced, so FinishedSending gives last_seq_no "
                    "(section 4)",
                )
            )
    if name == "FixpFinishedReceiving" and peer not in session.finished_sending:
        errors.append(
            (
                place,
                "finished-receiving-after-finished-sending",
                "FinishedReceiving answers the peer's FinishedSending (section 6)",
            )
        )

    if name in REQUESTS.values():
        session.last_request[(name, party)] = message.get("request_time")
    if name in APPLICATION_MESSAGES:
        _check_application(session, party, 1, place, errors)
    if name == "FixpTerminate":
        session.terminated.add(party)


def _check_application(session, party, count, place, errors):
    if session.kind == "point_to_point" and not session.established:
        errors.append(
            (
                place,
                "established-first",
                "application messages wait for EstablishmentAck (section 6)",
            )
        )
    if session.kind == "multicast" and not session.topic_seen:
        errors.append(
            (place, "topic-first", "a Topic starts a multicast flow (section 5)")
        )
    if party in session.finished_sending:
        errors.append(
            (
                place,
                "no-application-after-finished-sending",
                "no application message follows the sender's FinishedSending (section 6)",
            )
        )
    session.count_application(party, count, place, errors)


def rule_errors(exchange: dict) -> list[tuple[str, str, str]]:
    """Every place where the exchange breaks one of the rules above."""
    errors: list[tuple[str, str, str]] = []
    session = _Session(exchange)
    for index, step in enumerate(exchange.get("exchange_steps") or []):
        place = f"/exchange_steps/{index}"
        party = step["sent_by"]
        if party in session.terminated:
            errors.append(
                (
                    place,
                    "nothing-after-terminate",
                    f"the {party} sends nothing after its own Terminate (section 4)",
                )
            )
        if "fixp_message" in step:
            _check_message(session, step, place, errors)
        else:
            _check_application(
                session, party, step["application_message_count"], place, errors
            )
    return errors
