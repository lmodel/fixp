"""The protocol's rules that JSON Schema cannot state.

Each rule compares one step of an exchange with the steps before it: an answer with its
request, a message with the flow types the session negotiated, a sequence number with what
was sent. Most come from the list of protocol violations in section 6 of FIXP 1.0, and each
rule below names its source. Where appendix A shows a step the chapters allow, such as a
session bound again after Terminate, the rules let it pass. They read an exchange as the YAML
record the LinkML schema describes, and read what each message class allows from its
annotations.

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
# The messages that name the flow they concern, which may be another session's: a multicast's
# lost messages are asked for over a separate session (section 5), and InvalidSession answers
# a request for a session the sender does not know (section 4).
RETRANSMIT_MESSAGES = {
    "FixpRetransmitRequest",
    "FixpRetransmission",
    "FixpRetransmitReject",
}
# Applied and NotApplied are application messages: each takes a sequence number.
APPLICATION_MESSAGES = {"FixpApplied", "FixpNotApplied"}
# The messages that keep a session alive when nothing else is sent. Once a party has sent
# FinishedSending, that message takes their place.
HEARTBEATS = {"FixpSequence", "FixpContext", "FixpUnsequencedHeartbeat"}


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
        # A FinishedReceiving has answered a FinishedSending, so the session's identifier is
        # spent.
        self.finalized = False
        self.established = False
        self.terminated: set[str] = set()
        self.finished_sending: set[str] = set()
        self.finished_receiving: set[str] = set()
        self.last_request: dict[tuple[str, str], int] = {}
        # The session_id each party's latest request of each kind named.
        self.request_ids: dict[tuple[str, str], str] = {}
        self.open_retransmit: set[str] = set()
        self.started: set[str] = set()
        # A party in `replaying` has sent a Retransmission and no Sequence or Context since;
        # `replay_left` counts the resent messages its latest batch still owes.
        self.replaying: set[str] = set()
        self.replay_left: dict[str, int] = {}
        self.next_number: dict[str, int] = {}
        # The highest number each flow has reached, counting what a NextSeqNo shows, and the
        # highest an application message in the exchange took.
        self.highest_sent: dict[str, int] = {}
        self.highest_counted: dict[str, int] = {}
        # The session's own identifier: the first the exchange names.
        self.session_id: str | None = None
        self.topic_seen = False
        self.multicast_numbered = False

    def peer(self, party: str) -> str | None:
        return {"client": "server", "server": "client"}.get(party)

    def bind_again(self) -> None:
        """An Establish ties the session to a new transport (section 3), so what each side sent
        before its Terminate no longer silences it, and no earlier request is still open."""
        self.terminated.clear()
        self.established = False
        self.open_retransmit.clear()
        self.replay_left.clear()

    def reached(self, party: str, next_seq_no: int) -> None:
        """A NextSeqNo shows that the numbers below it are behind the party's flow, so its peer
        may ask for any of them (section 4)."""
        self.highest_sent[party] = max(self.highest_sent.get(party, 0), next_seq_no - 1)

    def count_application(
        self, party: str, count: int, place: str, errors: list
    ) -> None:
        flow = self.flows.get(party)
        if flow == "None":
            errors.append(
                (
                    place,
                    "no-application-on-none-flow",
                    f"the {party}'s flow is None, so it sends no application messages "
                    "(section 3)",
                )
            )
        # The first messages after a Retransmission are the batch it announced; the rest are new.
        resent = min(count, self.replay_left.get(party, 0))
        self.replay_left[party] = self.replay_left.get(party, 0) - resent
        new = count - resent
        if flow in SEQUENCED and party not in self.started:
            errors.append(
                (
                    place,
                    "sequence-before-sequenced",
                    f"the {party}'s sequenced flow sends an application message before any "
                    "Sequence, Context or Retransmission (section 3)",
                )
            )
        elif new and party in self.replaying:
            errors.append(
                (
                    place,
                    "sequence-after-retransmission",
                    f"the {party} goes back to new messages after resent ones without "
                    "Sequence or Context first (sections 3 and 4)",
                )
            )
        if new and party in self.finished_sending:
            errors.append(
                (
                    place,
                    "no-application-after-finished-sending",
                    "no new application message follows the sender's FinishedSending "
                    "(section 6)",
                )
            )
        if new and party in self.finished_receiving:
            errors.append(
                (
                    place,
                    "no-application-after-finished-receiving",
                    "no new application message follows the sender's FinishedReceiving "
                    "(section 6)",
                )
            )
        if party in self.next_number:
            first = self.next_number[party]
            self.next_number[party] = first + count
            last = first + count - 1
            self.highest_sent[party] = max(self.highest_sent.get(party, 0), last)
            self.highest_counted[party] = max(self.highest_counted.get(party, 0), last)


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


def _check_sequencing(session, name, party, message, place, errors):
    """topic-first, context-when-multiplexed and multicast-starts-at-one, for the messages
    that start or resume a flow's numbering."""
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
    if "next_seq_no" not in message:
        return
    if session.kind == "multicast" and not session.multicast_numbered:
        session.multicast_numbered = True
        if message["next_seq_no"] != 1:
            errors.append(
                (
                    place,
                    "multicast-starts-at-one",
                    "a new multicast session numbers its first application message 1 "
                    "(section 5)",
                )
            )
    session.started.add(party)
    session.next_number[party] = message["next_seq_no"]
    if name == "FixpRetransmission":
        session.replaying.add(party)
        session.replay_left[party] = message["message_count"]
    else:
        session.replaying.discard(party)
        session.replay_left[party] = 0


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
        named = message["session_id"]
        if session.session_id is None:
            session.session_id = named
        # A reject may repeat the identifier its request named, such as InvalidSession's.
        echoed = named == session.request_ids.get((REQUESTS.get(name, ""), peer or ""))
        if (
            named != session.session_id
            and not session.multiplexed
            and not echoed
            and name not in RETRANSMIT_MESSAGES
        ):
            errors.append(
                (
                    place,
                    "session-id",
                    "a transport that carries one session sees one session_id (section 3)",
                )
            )

    if name in HEARTBEATS and party in session.finished_sending:
        errors.append(
            (
                place,
                "heartbeat-after-finished-sending",
                f"after its FinishedSending, the {party} keeps the session alive with "
                "FinishedSending (section 4)",
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
    elif name == "FixpEstablish" and (not session.negotiated or session.finalized):
        errors.append(
            (
                place,
                "negotiate-first",
                "Establish needs a negotiated session that no FinishedReceiving has closed "
                "(sections 4 and 6)",
            )
        )
    elif name == "FixpEstablishmentAck":
        session.established = True

    if name in ("FixpSequence", "FixpContext", "FixpRetransmission"):
        _check_sequencing(session, name, party, message, place, errors)
    if "next_seq_no" in message:
        session.reached(party, message["next_seq_no"])

    # A request about another session's flow concerns numbers this exchange does not hold.
    own = message.get("session_id") in (None, session.session_id)
    if name == "FixpRetransmitRequest" and own:
        if party in session.open_retransmit or session.replay_left.get(peer, 0) > 0:
            errors.append(
                (
                    place,
                    "one-retransmit-request",
                    "an earlier RetransmitRequest is still being answered (sections 4 and 6)",
                )
            )
        last = message["from_seq_no"] + message["message_count"] - 1
        if last > session.highest_sent.get(peer, 0):
            errors.append(
                (
                    place,
                    "retransmit-in-bounds",
                    "it asks for a number beyond the last the peer has reached (section 6)",
                )
            )
        session.open_retransmit.add(party)
    if name in RETRANSMIT_ANSWERS and peer and own:
        session.open_retransmit.discard(peer)

    if name == "FixpFinishedSending":
        session.finished_sending.add(party)
        last = message.get("last_seq_no")
        if session.flows.get(party) in SEQUENCED and last is None:
            errors.append(
                (
                    place,
                    "last-seq-no",
                    f"the {party}'s flow is sequenced, so FinishedSending gives last_seq_no "
                    "(section 4)",
                )
            )
        elif last is not None and party in session.next_number:
            if not (
                session.highest_counted.get(party, 0)
                <= last
                <= session.highest_sent.get(party, 0)
            ):
                errors.append(
                    (
                        place,
                        "last-seq-no",
                        f"the {party}'s last_seq_no is not the number its flow reached "
                        "(section 4)",
                    )
                )
    if name == "FixpFinishedReceiving":
        if peer not in session.finished_sending:
            errors.append(
                (
                    place,
                    "finished-receiving-after-finished-sending",
                    "FinishedReceiving answers the peer's FinishedSending (section 6)",
                )
            )
        session.finished_receiving.add(party)
        session.finalized = True

    if name in REQUESTS.values():
        session.last_request[(name, party)] = message.get("request_time")
        session.request_ids[(name, party)] = message.get("session_id")
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
    session.count_application(party, count, place, errors)


def rule_errors(exchange: dict) -> list[tuple[str, str, str]]:
    """Every place where the exchange breaks one of the rules above."""
    errors: list[tuple[str, str, str]] = []
    session = _Session(exchange)
    for index, step in enumerate(exchange.get("exchange_steps") or []):
        place = f"/exchange_steps/{index}"
        party = step["sent_by"]
        message = step.get("fixp_message") or {}
        if message.get("message_kind") == "FixpEstablish" and session.terminated:
            session.bind_again()
        if party in session.terminated:
            errors.append(
                (
                    place,
                    "nothing-after-terminate",
                    f"the {party} sends nothing after its own Terminate until an Establish "
                    "ties the session to a transport again (section 4)",
                )
            )
        if "fixp_message" in step:
            _check_message(session, step, place, errors)
        else:
            _check_application(
                session, party, step["application_message_count"], place, errors
            )
    return errors
