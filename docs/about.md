# About fixp

This page says how the schema reads FIXP, where each part comes from, and what the model leaves out.

## One edition

The schema models FIXP 1.0, the Technical Standard the FIX Trading Community approved in April 2021, at the tag `v1.0-STANDARD` of [fixp-specification](https://github.com/FIXTradingCommunity/fixp-specification). Version 1.1 is a Draft Standard. Its resource files differ from 1.0's only in four field numbers of `MessageTemplate`, and it lacks an Orchestra file. Its chapters add guidance for WebSocket and mend three spellings, but no message, field or value. So one edition is modelled, and the upstream watch reports a new tag or edition folder.

## A message as a record

FIXP describes a message by its fields and leaves the wire format to the encoding, so a record is those fields as YAML or JSON. Each message is a class with the `Fixp` prefix, and its fields keep the specification's order. `message_kind` names the class, as FIXP's MessageType names the message.

Each field is a snake_case slot, and the slot's aliases give FIXP's name. Seven take a different word, because the plain one is taken elsewhere in the family: `Timestamp` is `request_time`, `Reason` is `reason_text`, `Classification` is `topic_classification`, `Count` is `message_count`, `EncodingType` is `sofh_encoding_type`, `Version` is `template_version`, and each `Code` is named for its list, such as `termination_code`.

The datatypes are FIXP's own: unsigned numbers of 8 to 64 bits, a version 4 UUID, nanoseconds since the Unix epoch, milliseconds, opaque octets and text. The octets are written in base64, which is this schema's choice.

Two records that are not messages hold what a session needs around them. `FixpExchange` is a run of steps on one session, each a message or a count of application messages, and the specification's appendix A describes many such runs. `FixpRulesOfEngagement` is the checklist of appendix B: what the client and the server each use at each layer of the stack.

## Where each part comes from

`upstream/` holds FIXP 1.0's three resource files, pinned by git object hash: the SBE message schema, the FIX repository file and the Orchestra file. `tests/test_coverage.py` holds every message, field, number, type, value and presence in the schema to them. The annotations on each element give the names and numbers the files use: `sbe_template_id`, `sbe_field_id`, `repository_field_id` and `sbe_value`.

Where the files and the specification's tables disagree, the schema accepts both, and `tests/upstream_departures.yaml` lists each case with its reason:

- Topic's `keepalive_interval` is required in both files and missing from section 5's table, so it is optional.
- Context's `next_seq_no` is required in both files and optional in section 3's table, so it is optional.
- FinishedSending's `last_seq_no` is required in the repository file and optional in the SBE schema and section 4, so it is optional, and a rule asks for it on a sequenced flow.
- Topic's `flow` takes Recoverable or Idempotent, as section 5 and the repository file say. The SBE schema allows all four flow types.

## Rules that span an exchange

JSON Schema checks each message by itself. `tests/fixp_rules.py` checks what the specification states about one step against the steps before it, and each rule has a counter-example in `tests/test_rules.py`.

- **Who sends what.** A message comes from the side its class names: Negotiate and Establish from the client, their answers from the server, Topic from a publisher. Only the publisher sends on a multicast, and a message section 6 leaves off a multicast, or off a session between two parties, is refused there.
- **Flow types.** A message that concerns one flow suits that flow's type, by the summary in section 6: Sequence only on a sequenced flow, UnsequencedHeartbeat only where the flow is unsequenced or empty, RetransmitRequest only towards a recoverable one, Applied and NotApplied only back to an idempotent one. A session's two flows cannot both be None.
- **Order.** Establish follows a NegotiationResponse, application messages wait for EstablishmentAck, a multicast flow starts with Topic, and a sequenced flow starts with Sequence, Context or Retransmission.
- **Answers.** An answer repeats the request_time of the request it answers. A party keeps at most one RetransmitRequest open, and asks only for numbers already sent.
- **Endings.** FinishedReceiving answers the peer's FinishedSending, no application message follows the sender's own FinishedSending, FinishedSending gives `last_seq_no` on a sequenced flow, and a party sends nothing after its own Terminate.
- **Transport.** A transport that carries one session sees one session identifier and takes Sequence, and a shared one takes Context.

## What the model leaves out

- The specification's text. It is under CC BY-ND 4.0, so every description here is this project's own, and [NOTICE](https://github.com/lmodel/fixp/blob/main/NOTICE) states the position.
- Encoded bytes. The SBE schema's message header and the Simple Open Framing Header are the encoding's frame around a message, which other standards define.
- Timing. Keep-alive intervals, timeouts and retries are about when a message is sent, which a record of the messages cannot show.
- Application messages, whose content FIXP does not define. An exchange counts them, so that the sequence numbers add up.

## What FIX's files show

The project leaves these faults in FIX's files as they are.

- The Orchestra file is not well-formed XML: line 733 closes the UnsequencedHeartbeat message, and line 735 closes it again. The tests read it in recovery mode, and it agrees with the repository file.
- The SBE schema numbers Topic's `Flow` 8, which is `Reason`'s number in four other messages, and numbers the four fields of `MessageTemplate` one lower than the repository file does.
- All three files spell RetransmitReject as `RestransmitReject`, and section 4's tables spell RetransmitRequest and Retransmission with the same extra letter. Version 1.1's tables mend all three, and its files do not.
- Section 3 says that sending Context or Sequence when the flow is unsequenced or empty breaks the protocol, while its own table makes Context's `NextSeqNo` optional, and section 6's summary allows Context on those flows. The rules follow section 6, which the list of violations points to.

## Mappings

The FIXP files define each message as an SBE message template and as an Orchestra message, so `FixpMessage` has `related_mappings` to lmodel/fix-sbe's `SbeMessageV1` and lmodel/fix-orchestra's `OrchestraMessageV10`. A record of those classes defines a kind of message, while an instance of `FixpMessage` is one message, so neither mapping is close. The annotations that name an SBE primitive type, a byte order or a FIX datatype use the values of fix-sbe's lists. `tests/test_mappings.py` checks the targets and the values against those repositories' released copies.
