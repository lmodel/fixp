from __future__ import annotations

import re
import sys
from datetime import (
    date,
    datetime,
    time
)
from decimal import Decimal
from enum import Enum
from typing import (
    Any,
    ClassVar,
    Literal,
    Optional,
    Union
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    SerializationInfo,
    SerializerFunctionWrapHandler,
    field_validator,
    model_serializer
)


metamodel_version = "1.12.0"
version = "1.0"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        serialize_by_alias = True,
        validate_by_name = True,
        validate_assignment = True,
        validate_default = True,
        extra = "forbid",
        arbitrary_types_allowed = True,
        use_enum_values = True,
        strict = False,
    )





class LinkMLMeta(RootModel):
    root: dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key:str):
        return getattr(self.root, key)

    def __getitem__(self, key:str):
        return self.root[key]

    def __setitem__(self, key:str, value):
        self.root[key] = value

    def __contains__(self, key:str) -> bool:
        return key in self.root


linkml_meta = LinkMLMeta({'annotations': {'sbe_byte_order': {'tag': 'sbe_byte_order',
                                        'value': 'littleEndian'},
                     'sbe_package': {'tag': 'sbe_package', 'value': 'FIXP'},
                     'sbe_schema_id': {'tag': 'sbe_schema_id', 'value': '2748'},
                     'sbe_schema_version': {'tag': 'sbe_schema_version',
                                            'value': '0'},
                     'upstream_commit': {'tag': 'upstream_commit',
                                         'value': '6d89f5fa66d544ea6b41e93853c23292505e49c6'},
                     'upstream_tag': {'tag': 'upstream_tag',
                                      'value': 'v1.0-STANDARD'}},
     'comments': ['An exchange starts at FixpExchange, the tree root. A single '
                  'message validates against its own class, such as FixpNegotiate, '
                  'and a rules-of-engagement record against FixpRulesOfEngagement. '
                  "upstream/ holds the specification's resource files unchanged, "
                  'tests/test_coverage.py compares the modules with them, and '
                  'scripts/check_upstream_release.py reports when they change.'],
     'default_prefix': 'fixp',
     'default_range': 'string',
     'description': 'A LinkML model of the FIX Performance Session Layer 1.0, the '
                    "FIX Trading Community's session protocol for fast trading "
                    "links. It describes FIXP's session messages, their fields and "
                    'value lists, exchanges of those messages on one session, and '
                    'the rules of engagement two parties agree on. A message is '
                    'described by its fields, so the model works with any '
                    'encoding.',
     'id': 'https://w3id.org/lmodel/fixp',
     'imports': ['linkml:types',
                 './fixp_core',
                 './fixp_messages',
                 './fixp_exchange',
                 './fixp_engagement'],
     'keywords': ['FIX', 'FIXP', 'session layer', 'trading'],
     'license': 'Apache-2.0',
     'name': 'fixp',
     'prefixes': {'fix_orchestra': {'prefix_prefix': 'fix_orchestra',
                                    'prefix_reference': 'https://w3id.org/lmodel/fix-orchestra/'},
                  'fix_sbe': {'prefix_prefix': 'fix_sbe',
                              'prefix_reference': 'https://w3id.org/lmodel/fix-sbe/'},
                  'fixp': {'prefix_prefix': 'fixp',
                           'prefix_reference': 'https://w3id.org/lmodel/fixp/'},
                  'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'},
                  'schema': {'prefix_prefix': 'schema',
                             'prefix_reference': 'http://schema.org/'}},
     'see_also': ['https://lmodel.github.io/fixp',
                  'https://github.com/FIXTradingCommunity/fixp-specification'],
     'source': 'https://github.com/FIXTradingCommunity/fixp-specification/tree/v1.0-STANDARD/v1-0-STANDARD',
     'source_file': 'src/fixp/schema/fixp.yaml',
     'title': 'FIX Performance Session Layer (FIXP)'} )

class FixpFlowType(str, Enum):
    """
    How surely a flow is delivered. A flow is what one side of a session sends the other, leaving out session messages.
    """
    Recoverable = "Recoverable"
    """
    Every message arrives once and in order; the receiver asks for any gap to be sent again.
    """
    Idempotent = "Idempotent"
    """
    No message takes effect twice; the sender hears of a gap and its application decides what to resend.
    """
    Unsequenced = "Unsequenced"
    """
    Messages carry no sequence number, and none is ever resent.
    """
    None_ = "None"
    """
    This side sends no application messages at all.
    """


class FixpMulticastFlowType(str, Enum):
    """
    The delivery guarantee a multicast topic announces for its flow.
    """
    Recoverable = "Recoverable"
    """
    Sequenced; a listener gets a lost message back over a separate unicast session.
    """
    Idempotent = "Idempotent"
    """
    Sequenced, so a listener can see a loss, but nothing lost comes back.
    """


class FixpNegotiationRejectCode(str, Enum):
    """
    Why a server refused to create a session.
    """
    Credentials = "Credentials"
    """
    The server could not identify the client, or would not let it in.
    """
    FlowTypeNotSupported = "FlowTypeNotSupported"
    """
    The server does not offer the flow type the client asked to send.
    """
    DuplicateId = "DuplicateId"
    """
    The client chose a session identifier that is not new.
    """
    Unspecified = "Unspecified"
    """
    Some reason the other values do not name.
    """


class FixpEstablishmentRejectCode(str, Enum):
    """
    Why a server would not bind the session to this transport.
    """
    Unnegotiated = "Unnegotiated"
    """
    The session was never negotiated, or it has been finalized and needs a new negotiation.
    """
    AlreadyEstablished = "AlreadyEstablished"
    """
    The server had already acknowledged a binding, so this request repeats it.
    """
    SessionBlocked = "SessionBlocked"
    """
    The client may not use this session.
    """
    KeepaliveInterval = "KeepaliveInterval"
    """
    The client's keep-alive interval is outside what the server accepts.
    """
    Credentials = "Credentials"
    """
    The server could not identify the client, or would not let it in.
    """
    Unspecified = "Unspecified"
    """
    Some reason the other values do not name.
    """


class FixpRetransmitRejectCode(str, Enum):
    """
    Why a party will not resend the messages its peer asked for.
    """
    OutOfRange = "OutOfRange"
    """
    The range asked for runs past the sequence numbers sent so far.
    """
    InvalidSession = "InvalidSession"
    """
    The session is unknown, or the one asking may not read it.
    """
    RequestLimitExceeded = "RequestLimitExceeded"
    """
    The request asks for more messages than the sender resends at once.
    """


class FixpTerminationCode(str, Enum):
    """
    Why a party releases a session from its transport.
    """
    Finished = "Finished"
    """
    An ordinary release, with no error.
    """
    UnspecifiedError = "UnspecifiedError"
    """
    An error that the other values do not name.
    """
    ReRequestOutOfBounds = "ReRequestOutOfBounds"
    """
    The peer asked again for messages outside the range sent.
    """
    ReRequestInProgress = "ReRequestInProgress"
    """
    The peer asked again for messages while its earlier request was unanswered.
    """


class FixpSessionKind(str, Enum):
    """
    The two forms of FIXP session.
    """
    point_to_point = "point_to_point"
    """
    A client and a server over a transport that carries messages both ways, with one flow each way.
    """
    multicast = "multicast"
    """
    One publisher, one flow and many listeners, on a transport that only carries messages outward.
    """


class FixpParty(str, Enum):
    """
    The side that sends a step.
    """
    client = "client"
    """
    The party that opens a session with a server.
    """
    server = "server"
    """
    The party that accepts the client's session.
    """
    publisher = "publisher"
    """
    The only party that sends in a multicast.
    """



class FixpMessage(ConfiguredBaseModel):
    """
    One FIXP message, as its fields would be read from the wire before or after encoding.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'comments': ['The FIXP files define each message as an SBE message template, '
                      'which lmodel/fix-sbe models as SbeMessageV1, and as an '
                      'Orchestra message, which lmodel/fix-orchestra models as '
                      'OrchestraMessageV10. A record of those classes defines a kind '
                      'of message; an instance of this class is one message of that '
                      'kind.',
                      'The annotations of each subclass name its template id and its '
                      'name in the SBE schema, the stage the summary in section 6 '
                      'gives it, which side sends it, and the flow types it may appear '
                      'on.'],
         'from_schema': 'https://w3id.org/lmodel/fixp/schema/fixp_core',
         'related_mappings': ['fix_sbe:SbeMessageV1',
                              'fix_orchestra:OrchestraMessageV10']})

    message_kind: Literal["FixpMessage"] = Field(default="FixpMessage", description="""The class of this message, such as FixpNegotiate. It stands for FIXP's MessageType, which every message carries.""", json_schema_extra = { "linkml_meta": {'aliases': ['MessageType'],
         'designates_type': True,
         'domain_of': ['FixpMessage']} })


class FixpNegotiate(FixpMessage):
    """
    A client's request to create a session under an identifier it has never used, stating the flow type it will send.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'fixp_flow_types': {'tag': 'fixp_flow_types',
                                             'value': 'Recoverable Idempotent '
                                                      'Unsequenced None'},
                         'fixp_multicast': {'tag': 'fixp_multicast', 'value': 'false'},
                         'fixp_sent_by': {'tag': 'fixp_sent_by', 'value': 'client'},
                         'sbe_name': {'tag': 'sbe_name', 'value': 'Negotiate'},
                         'sbe_template_id': {'tag': 'sbe_template_id', 'value': '1'}},
         'from_schema': 'https://w3id.org/lmodel/fixp/schema/fixp_messages',
         'in_subset': ['fixp_initialization'],
         'slot_usage': {'client_flow': {'name': 'client_flow', 'required': True},
                        'credentials': {'description': 'Data that identifies the '
                                                       'client, in a form the two '
                                                       'parties agree on.',
                                        'name': 'credentials'},
                        'request_time': {'name': 'request_time', 'required': True},
                        'session_id': {'name': 'session_id', 'required': True}}})

    session_id: str = Field(default=..., description="""The session's identifier, which the client chooses and never uses again.""", json_schema_extra = { "linkml_meta": {'aliases': ['SessionId'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'String'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '1'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '1'}},
         'domain_of': ['FixpNegotiate',
                       'FixpNegotiationResponse',
                       'FixpNegotiationReject',
                       'FixpTopic',
                       'FixpEstablish',
                       'FixpEstablishmentAck',
                       'FixpEstablishmentReject',
                       'FixpContext',
                       'FixpRetransmitRequest',
                       'FixpRetransmission',
                       'FixpRetransmitReject',
                       'FixpTerminate',
                       'FixpFinishedSending',
                       'FixpFinishedReceiving']} })
    request_time: int = Field(default=..., description="""When the sender made this request. The answer repeats it, to show what it answers.""", json_schema_extra = { "linkml_meta": {'aliases': ['Timestamp'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'int'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '2'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '2'}},
         'domain_of': ['FixpNegotiate', 'FixpEstablish', 'FixpRetransmitRequest']} })
    client_flow: FixpFlowType = Field(default=..., description="""The flow type of the application messages the client will send.""", json_schema_extra = { "linkml_meta": {'aliases': ['ClientFlow'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'int'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '3'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '3'}},
         'domain_of': ['FixpNegotiate']} })
    credentials: Optional[str] = Field(default=None, description="""Data that identifies the client, in a form the two parties agree on.""", json_schema_extra = { "linkml_meta": {'aliases': ['Credentials'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'data'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '4'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '4'}},
         'domain_of': ['FixpNegotiate', 'FixpNegotiationResponse', 'FixpEstablish']} })
    message_kind: Literal["FixpNegotiate"] = Field(default="FixpNegotiate", description="""The class of this message, such as FixpNegotiate. It stands for FIXP's MessageType, which every message carries.""", json_schema_extra = { "linkml_meta": {'aliases': ['MessageType'],
         'designates_type': True,
         'domain_of': ['FixpMessage']} })


class FixpNegotiationResponse(FixpMessage):
    """
    A server's acceptance of a new session, stating the flow type it will send back.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'fixp_flow_types': {'tag': 'fixp_flow_types',
                                             'value': 'Recoverable Idempotent '
                                                      'Unsequenced None'},
                         'fixp_multicast': {'tag': 'fixp_multicast', 'value': 'false'},
                         'fixp_sent_by': {'tag': 'fixp_sent_by', 'value': 'server'},
                         'sbe_name': {'tag': 'sbe_name',
                                      'value': 'NegotiationResponse'},
                         'sbe_template_id': {'tag': 'sbe_template_id', 'value': '2'}},
         'from_schema': 'https://w3id.org/lmodel/fixp/schema/fixp_messages',
         'in_subset': ['fixp_initialization'],
         'slot_usage': {'credentials': {'description': 'Data that identifies the '
                                                       'server to the client, for '
                                                       'mutual authentication.',
                                        'name': 'credentials'},
                        'request_timestamp': {'description': 'The request_time of the '
                                                             'Negotiate this message '
                                                             'accepts.',
                                              'name': 'request_timestamp',
                                              'required': True},
                        'server_flow': {'name': 'server_flow', 'required': True},
                        'session_id': {'name': 'session_id', 'required': True}}})

    session_id: str = Field(default=..., description="""The session's identifier, which the client chooses and never uses again.""", json_schema_extra = { "linkml_meta": {'aliases': ['SessionId'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'String'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '1'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '1'}},
         'domain_of': ['FixpNegotiate',
                       'FixpNegotiationResponse',
                       'FixpNegotiationReject',
                       'FixpTopic',
                       'FixpEstablish',
                       'FixpEstablishmentAck',
                       'FixpEstablishmentReject',
                       'FixpContext',
                       'FixpRetransmitRequest',
                       'FixpRetransmission',
                       'FixpRetransmitReject',
                       'FixpTerminate',
                       'FixpFinishedSending',
                       'FixpFinishedReceiving']} })
    request_timestamp: int = Field(default=..., description="""The request_time of the Negotiate this message accepts.""", json_schema_extra = { "linkml_meta": {'aliases': ['RequestTimestamp'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'int'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '5'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '5'}},
         'domain_of': ['FixpNegotiationResponse',
                       'FixpNegotiationReject',
                       'FixpEstablishmentAck',
                       'FixpEstablishmentReject',
                       'FixpRetransmission',
                       'FixpRetransmitReject']} })
    server_flow: FixpFlowType = Field(default=..., description="""The flow type of the application messages the server will send.""", json_schema_extra = { "linkml_meta": {'aliases': ['ServerFlow'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'int'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '6'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '6'}},
         'domain_of': ['FixpNegotiationResponse']} })
    credentials: Optional[str] = Field(default=None, description="""Data that identifies the server to the client, for mutual authentication.""", json_schema_extra = { "linkml_meta": {'aliases': ['Credentials'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'data'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '4'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '4'}},
         'domain_of': ['FixpNegotiate', 'FixpNegotiationResponse', 'FixpEstablish']} })
    message_kind: Literal["FixpNegotiationResponse"] = Field(default="FixpNegotiationResponse", description="""The class of this message, such as FixpNegotiate. It stands for FIXP's MessageType, which every message carries.""", json_schema_extra = { "linkml_meta": {'aliases': ['MessageType'],
         'designates_type': True,
         'domain_of': ['FixpMessage']} })


class FixpNegotiationReject(FixpMessage):
    """
    A server's refusal to create a session. The server sends nothing more and closes the transport.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'fixp_flow_types': {'tag': 'fixp_flow_types',
                                             'value': 'Recoverable Idempotent '
                                                      'Unsequenced None'},
                         'fixp_multicast': {'tag': 'fixp_multicast', 'value': 'false'},
                         'fixp_sent_by': {'tag': 'fixp_sent_by', 'value': 'server'},
                         'sbe_name': {'tag': 'sbe_name', 'value': 'NegotiationReject'},
                         'sbe_template_id': {'tag': 'sbe_template_id', 'value': '3'}},
         'from_schema': 'https://w3id.org/lmodel/fixp/schema/fixp_messages',
         'in_subset': ['fixp_initialization'],
         'slot_usage': {'negotiation_reject_code': {'name': 'negotiation_reject_code',
                                                    'required': True},
                        'request_timestamp': {'description': 'The request_time of the '
                                                             'Negotiate this message '
                                                             'refuses.',
                                              'name': 'request_timestamp',
                                              'required': True},
                        'session_id': {'name': 'session_id', 'required': True}}})

    session_id: str = Field(default=..., description="""The session's identifier, which the client chooses and never uses again.""", json_schema_extra = { "linkml_meta": {'aliases': ['SessionId'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'String'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '1'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '1'}},
         'domain_of': ['FixpNegotiate',
                       'FixpNegotiationResponse',
                       'FixpNegotiationReject',
                       'FixpTopic',
                       'FixpEstablish',
                       'FixpEstablishmentAck',
                       'FixpEstablishmentReject',
                       'FixpContext',
                       'FixpRetransmitRequest',
                       'FixpRetransmission',
                       'FixpRetransmitReject',
                       'FixpTerminate',
                       'FixpFinishedSending',
                       'FixpFinishedReceiving']} })
    request_timestamp: int = Field(default=..., description="""The request_time of the Negotiate this message refuses.""", json_schema_extra = { "linkml_meta": {'aliases': ['RequestTimestamp'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'int'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '5'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '5'}},
         'domain_of': ['FixpNegotiationResponse',
                       'FixpNegotiationReject',
                       'FixpEstablishmentAck',
                       'FixpEstablishmentReject',
                       'FixpRetransmission',
                       'FixpRetransmitReject']} })
    negotiation_reject_code: FixpNegotiationRejectCode = Field(default=..., description="""Why the server refused to create the session.""", json_schema_extra = { "linkml_meta": {'aliases': ['Code', 'NegotiationRejectCode'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'int'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '7'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '7'}},
         'domain_of': ['FixpNegotiationReject']} })
    reason_text: Optional[str] = Field(default=None, description="""Free text that says more about the code beside it.""", json_schema_extra = { "linkml_meta": {'aliases': ['Reason'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'String'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '8'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '8'}},
         'domain_of': ['FixpNegotiationReject',
                       'FixpEstablishmentReject',
                       'FixpRetransmitReject',
                       'FixpTerminate']} })
    message_kind: Literal["FixpNegotiationReject"] = Field(default="FixpNegotiationReject", description="""The class of this message, such as FixpNegotiate. It stands for FIXP's MessageType, which every message carries.""", json_schema_extra = { "linkml_meta": {'aliases': ['MessageType'],
         'designates_type': True,
         'domain_of': ['FixpMessage']} })


class FixpTopic(FixpMessage):
    """
    A multicast publisher's notice that starts a flow and ties the session's short-lived identifier to a lasting subject. It is repeated so that late listeners can join.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'fixp_flow_types': {'tag': 'fixp_flow_types',
                                             'value': 'Recoverable Idempotent'},
                         'fixp_multicast': {'tag': 'fixp_multicast', 'value': 'true'},
                         'fixp_sent_by': {'tag': 'fixp_sent_by', 'value': 'publisher'},
                         'sbe_name': {'tag': 'sbe_name', 'value': 'Topic'},
                         'sbe_template_id': {'tag': 'sbe_template_id', 'value': '4'}},
         'from_schema': 'https://w3id.org/lmodel/fixp/schema/fixp_messages',
         'in_subset': ['fixp_initialization'],
         'slot_usage': {'flow': {'name': 'flow', 'required': True},
                        'keepalive_interval': {'comments': ['The SBE schema and the '
                                                            'repository file give '
                                                            'Topic this field, as a '
                                                            "required one. Section 5's "
                                                            'table leaves it out, so '
                                                            'the schema accepts a '
                                                            'Topic with or without '
                                                            'it.'],
                                               'description': "The publisher's "
                                                              'heartbeat interval, in '
                                                              'milliseconds.',
                                               'name': 'keepalive_interval'},
                        'session_id': {'name': 'session_id', 'required': True},
                        'topic_classification': {'name': 'topic_classification',
                                                 'required': True}}})

    session_id: str = Field(default=..., description="""The session's identifier, which the client chooses and never uses again.""", json_schema_extra = { "linkml_meta": {'aliases': ['SessionId'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'String'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '1'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '1'}},
         'domain_of': ['FixpNegotiate',
                       'FixpNegotiationResponse',
                       'FixpNegotiationReject',
                       'FixpTopic',
                       'FixpEstablish',
                       'FixpEstablishmentAck',
                       'FixpEstablishmentReject',
                       'FixpContext',
                       'FixpRetransmitRequest',
                       'FixpRetransmission',
                       'FixpRetransmitReject',
                       'FixpTerminate',
                       'FixpFinishedSending',
                       'FixpFinishedReceiving']} })
    flow: FixpMulticastFlowType = Field(default=..., description="""The flow type of a multicast topic's messages.""", json_schema_extra = { "linkml_meta": {'aliases': ['Flow'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'int'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '18'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '8'}},
         'domain_of': ['FixpTopic']} })
    keepalive_interval: Optional[int] = Field(default=None, description="""The publisher's heartbeat interval, in milliseconds.""", json_schema_extra = { "linkml_meta": {'aliases': ['KeepaliveInterval'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'int'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '9'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '9'}},
         'comments': ['The SBE schema and the repository file give Topic this field, '
                      "as a required one. Section 5's table leaves it out, so the "
                      'schema accepts a Topic with or without it.'],
         'domain_of': ['FixpTopic', 'FixpEstablish', 'FixpEstablishmentAck']} })
    topic_classification: str = Field(default=..., description="""The lasting subject of a topic's messages, such as a product type or a market symbol.""", json_schema_extra = { "linkml_meta": {'aliases': ['Classification'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'data'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '10'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '10'}},
         'domain_of': ['FixpTopic']} })
    message_kind: Literal["FixpTopic"] = Field(default="FixpTopic", description="""The class of this message, such as FixpNegotiate. It stands for FIXP's MessageType, which every message carries.""", json_schema_extra = { "linkml_meta": {'aliases': ['MessageType'],
         'designates_type': True,
         'domain_of': ['FixpMessage']} })


class FixpEstablish(FixpMessage):
    """
    A client's request to tie a negotiated session to the very transport this message arrives on. After a disconnection it is sent again to re-bind.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'fixp_flow_types': {'tag': 'fixp_flow_types',
                                             'value': 'Recoverable Idempotent '
                                                      'Unsequenced None'},
                         'fixp_multicast': {'tag': 'fixp_multicast', 'value': 'false'},
                         'fixp_sent_by': {'tag': 'fixp_sent_by', 'value': 'client'},
                         'sbe_name': {'tag': 'sbe_name', 'value': 'Establish'},
                         'sbe_template_id': {'tag': 'sbe_template_id', 'value': '5'}},
         'from_schema': 'https://w3id.org/lmodel/fixp/schema/fixp_messages',
         'in_subset': ['fixp_binding'],
         'slot_usage': {'credentials': {'description': 'Data that identifies the '
                                                       'client, in a form the two '
                                                       'parties agree on.',
                                        'name': 'credentials'},
                        'keepalive_interval': {'description': 'The longest the client '
                                                              'stays silent, in '
                                                              'milliseconds, before a '
                                                              'heartbeat.',
                                               'name': 'keepalive_interval',
                                               'required': True},
                        'next_seq_no': {'description': "When the client's recoverable "
                                                       'flow is bound again, the '
                                                       'number its next application '
                                                       'message will carry.',
                                        'name': 'next_seq_no'},
                        'request_time': {'name': 'request_time', 'required': True},
                        'session_id': {'name': 'session_id', 'required': True}}})

    session_id: str = Field(default=..., description="""The session's identifier, which the client chooses and never uses again.""", json_schema_extra = { "linkml_meta": {'aliases': ['SessionId'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'String'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '1'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '1'}},
         'domain_of': ['FixpNegotiate',
                       'FixpNegotiationResponse',
                       'FixpNegotiationReject',
                       'FixpTopic',
                       'FixpEstablish',
                       'FixpEstablishmentAck',
                       'FixpEstablishmentReject',
                       'FixpContext',
                       'FixpRetransmitRequest',
                       'FixpRetransmission',
                       'FixpRetransmitReject',
                       'FixpTerminate',
                       'FixpFinishedSending',
                       'FixpFinishedReceiving']} })
    request_time: int = Field(default=..., description="""When the sender made this request. The answer repeats it, to show what it answers.""", json_schema_extra = { "linkml_meta": {'aliases': ['Timestamp'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'int'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '2'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '2'}},
         'domain_of': ['FixpNegotiate', 'FixpEstablish', 'FixpRetransmitRequest']} })
    keepalive_interval: int = Field(default=..., description="""The longest the client stays silent, in milliseconds, before a heartbeat.""", json_schema_extra = { "linkml_meta": {'aliases': ['KeepaliveInterval'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'int'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '9'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '9'}},
         'domain_of': ['FixpTopic', 'FixpEstablish', 'FixpEstablishmentAck']} })
    next_seq_no: Optional[int] = Field(default=None, description="""When the client's recoverable flow is bound again, the number its next application message will carry.""", json_schema_extra = { "linkml_meta": {'aliases': ['NextSeqNo'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'int'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '11'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '11'}},
         'domain_of': ['FixpEstablish',
                       'FixpEstablishmentAck',
                       'FixpSequence',
                       'FixpContext',
                       'FixpRetransmission']} })
    credentials: Optional[str] = Field(default=None, description="""Data that identifies the client, in a form the two parties agree on.""", json_schema_extra = { "linkml_meta": {'aliases': ['Credentials'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'data'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '4'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '4'}},
         'domain_of': ['FixpNegotiate', 'FixpNegotiationResponse', 'FixpEstablish']} })
    message_kind: Literal["FixpEstablish"] = Field(default="FixpEstablish", description="""The class of this message, such as FixpNegotiate. It stands for FIXP's MessageType, which every message carries.""", json_schema_extra = { "linkml_meta": {'aliases': ['MessageType'],
         'designates_type': True,
         'domain_of': ['FixpMessage']} })


class FixpEstablishmentAck(FixpMessage):
    """
    A server's acceptance of the binding. From here, application messages may flow.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'fixp_flow_types': {'tag': 'fixp_flow_types',
                                             'value': 'Recoverable Idempotent '
                                                      'Unsequenced None'},
                         'fixp_multicast': {'tag': 'fixp_multicast', 'value': 'false'},
                         'fixp_sent_by': {'tag': 'fixp_sent_by', 'value': 'server'},
                         'sbe_name': {'tag': 'sbe_name', 'value': 'EstablishmentAck'},
                         'sbe_template_id': {'tag': 'sbe_template_id', 'value': '6'}},
         'from_schema': 'https://w3id.org/lmodel/fixp/schema/fixp_messages',
         'in_subset': ['fixp_binding'],
         'slot_usage': {'keepalive_interval': {'description': 'The longest the server '
                                                              'stays silent, in '
                                                              'milliseconds, before a '
                                                              'heartbeat.',
                                               'name': 'keepalive_interval',
                                               'required': True},
                        'next_seq_no': {'description': "If the server's flow is "
                                                       'recoverable, the number its '
                                                       'next application message will '
                                                       'carry, so the client can ask '
                                                       'for what it missed.',
                                        'name': 'next_seq_no'},
                        'request_timestamp': {'description': 'The request_time of the '
                                                             'Establish this message '
                                                             'accepts.',
                                              'name': 'request_timestamp',
                                              'required': True},
                        'session_id': {'name': 'session_id', 'required': True}}})

    session_id: str = Field(default=..., description="""The session's identifier, which the client chooses and never uses again.""", json_schema_extra = { "linkml_meta": {'aliases': ['SessionId'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'String'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '1'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '1'}},
         'domain_of': ['FixpNegotiate',
                       'FixpNegotiationResponse',
                       'FixpNegotiationReject',
                       'FixpTopic',
                       'FixpEstablish',
                       'FixpEstablishmentAck',
                       'FixpEstablishmentReject',
                       'FixpContext',
                       'FixpRetransmitRequest',
                       'FixpRetransmission',
                       'FixpRetransmitReject',
                       'FixpTerminate',
                       'FixpFinishedSending',
                       'FixpFinishedReceiving']} })
    request_timestamp: int = Field(default=..., description="""The request_time of the Establish this message accepts.""", json_schema_extra = { "linkml_meta": {'aliases': ['RequestTimestamp'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'int'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '5'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '5'}},
         'domain_of': ['FixpNegotiationResponse',
                       'FixpNegotiationReject',
                       'FixpEstablishmentAck',
                       'FixpEstablishmentReject',
                       'FixpRetransmission',
                       'FixpRetransmitReject']} })
    keepalive_interval: int = Field(default=..., description="""The longest the server stays silent, in milliseconds, before a heartbeat.""", json_schema_extra = { "linkml_meta": {'aliases': ['KeepaliveInterval'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'int'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '9'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '9'}},
         'domain_of': ['FixpTopic', 'FixpEstablish', 'FixpEstablishmentAck']} })
    next_seq_no: Optional[int] = Field(default=None, description="""If the server's flow is recoverable, the number its next application message will carry, so the client can ask for what it missed.""", json_schema_extra = { "linkml_meta": {'aliases': ['NextSeqNo'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'int'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '11'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '11'}},
         'domain_of': ['FixpEstablish',
                       'FixpEstablishmentAck',
                       'FixpSequence',
                       'FixpContext',
                       'FixpRetransmission']} })
    message_kind: Literal["FixpEstablishmentAck"] = Field(default="FixpEstablishmentAck", description="""The class of this message, such as FixpNegotiate. It stands for FIXP's MessageType, which every message carries.""", json_schema_extra = { "linkml_meta": {'aliases': ['MessageType'],
         'designates_type': True,
         'domain_of': ['FixpMessage']} })


class FixpEstablishmentReject(FixpMessage):
    """
    A server's refusal of the binding.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'fixp_flow_types': {'tag': 'fixp_flow_types',
                                             'value': 'Recoverable Idempotent '
                                                      'Unsequenced None'},
                         'fixp_multicast': {'tag': 'fixp_multicast', 'value': 'false'},
                         'fixp_sent_by': {'tag': 'fixp_sent_by', 'value': 'server'},
                         'sbe_name': {'tag': 'sbe_name',
                                      'value': 'EstablishmentReject'},
                         'sbe_template_id': {'tag': 'sbe_template_id', 'value': '7'}},
         'from_schema': 'https://w3id.org/lmodel/fixp/schema/fixp_messages',
         'in_subset': ['fixp_binding'],
         'slot_usage': {'establishment_reject_code': {'name': 'establishment_reject_code',
                                                      'required': True},
                        'request_timestamp': {'description': 'The request_time of the '
                                                             'Establish this message '
                                                             'refuses.',
                                              'name': 'request_timestamp',
                                              'required': True},
                        'session_id': {'name': 'session_id', 'required': True}}})

    session_id: str = Field(default=..., description="""The session's identifier, which the client chooses and never uses again.""", json_schema_extra = { "linkml_meta": {'aliases': ['SessionId'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'String'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '1'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '1'}},
         'domain_of': ['FixpNegotiate',
                       'FixpNegotiationResponse',
                       'FixpNegotiationReject',
                       'FixpTopic',
                       'FixpEstablish',
                       'FixpEstablishmentAck',
                       'FixpEstablishmentReject',
                       'FixpContext',
                       'FixpRetransmitRequest',
                       'FixpRetransmission',
                       'FixpRetransmitReject',
                       'FixpTerminate',
                       'FixpFinishedSending',
                       'FixpFinishedReceiving']} })
    request_timestamp: int = Field(default=..., description="""The request_time of the Establish this message refuses.""", json_schema_extra = { "linkml_meta": {'aliases': ['RequestTimestamp'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'int'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '5'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '5'}},
         'domain_of': ['FixpNegotiationResponse',
                       'FixpNegotiationReject',
                       'FixpEstablishmentAck',
                       'FixpEstablishmentReject',
                       'FixpRetransmission',
                       'FixpRetransmitReject']} })
    establishment_reject_code: FixpEstablishmentRejectCode = Field(default=..., description="""Why the server refused to bind the session.""", json_schema_extra = { "linkml_meta": {'aliases': ['Code', 'EstablishmentRejectCode'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'int'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '12'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '12'}},
         'domain_of': ['FixpEstablishmentReject']} })
    reason_text: Optional[str] = Field(default=None, description="""Free text that says more about the code beside it.""", json_schema_extra = { "linkml_meta": {'aliases': ['Reason'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'String'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '8'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '8'}},
         'domain_of': ['FixpNegotiationReject',
                       'FixpEstablishmentReject',
                       'FixpRetransmitReject',
                       'FixpTerminate']} })
    message_kind: Literal["FixpEstablishmentReject"] = Field(default="FixpEstablishmentReject", description="""The class of this message, such as FixpNegotiate. It stands for FIXP's MessageType, which every message carries.""", json_schema_extra = { "linkml_meta": {'aliases': ['MessageType'],
         'designates_type': True,
         'domain_of': ['FixpMessage']} })


class FixpSequence(FixpMessage):
    """
    Starts the numbering of a sequenced flow, so that the application messages after it are numbered by counting up from the value it carries. Sent when idle, it is also the heartbeat.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'fixp_flow_of': {'tag': 'fixp_flow_of', 'value': 'own'},
                         'fixp_flow_types': {'tag': 'fixp_flow_types',
                                             'value': 'Recoverable Idempotent'},
                         'fixp_multicast': {'tag': 'fixp_multicast', 'value': 'true'},
                         'fixp_sent_by': {'tag': 'fixp_sent_by', 'value': 'any'},
                         'sbe_name': {'tag': 'sbe_name', 'value': 'Sequence'},
                         'sbe_template_id': {'tag': 'sbe_template_id', 'value': '8'}},
         'comments': ['It is used on a transport that carries one session; Context '
                      'replaces it on a shared one.'],
         'from_schema': 'https://w3id.org/lmodel/fixp/schema/fixp_messages',
         'in_subset': ['fixp_transferring'],
         'slot_usage': {'next_seq_no': {'name': 'next_seq_no', 'required': True}}})

    next_seq_no: int = Field(default=..., description="""The number the sender's next application message will carry.""", json_schema_extra = { "linkml_meta": {'aliases': ['NextSeqNo'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'int'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '11'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '11'}},
         'domain_of': ['FixpEstablish',
                       'FixpEstablishmentAck',
                       'FixpSequence',
                       'FixpContext',
                       'FixpRetransmission']} })
    message_kind: Literal["FixpSequence"] = Field(default="FixpSequence", description="""The class of this message, such as FixpNegotiate. It stands for FIXP's MessageType, which every message carries.""", json_schema_extra = { "linkml_meta": {'aliases': ['MessageType'],
         'designates_type': True,
         'domain_of': ['FixpMessage']} })


class FixpContext(FixpMessage):
    """
    On a transport that several sessions share, names the session the following messages belong to and, when the flow is sequenced, where its numbering continues.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'fixp_flow_of': {'tag': 'fixp_flow_of', 'value': 'own'},
                         'fixp_flow_types': {'tag': 'fixp_flow_types',
                                             'value': 'Recoverable Idempotent '
                                                      'Unsequenced None'},
                         'fixp_multicast': {'tag': 'fixp_multicast', 'value': 'true'},
                         'fixp_sent_by': {'tag': 'fixp_sent_by', 'value': 'any'},
                         'sbe_name': {'tag': 'sbe_name', 'value': 'Context'},
                         'sbe_template_id': {'tag': 'sbe_template_id', 'value': '9'}},
         'from_schema': 'https://w3id.org/lmodel/fixp/schema/fixp_messages',
         'in_subset': ['fixp_transferring'],
         'slot_usage': {'next_seq_no': {'comments': ["Section 3's table makes it "
                                                     'optional, and both resource '
                                                     'files make it required, so the '
                                                     'schema accepts a Context with or '
                                                     'without it.'],
                                        'name': 'next_seq_no'},
                        'session_id': {'name': 'session_id', 'required': True}}})

    session_id: str = Field(default=..., description="""The session's identifier, which the client chooses and never uses again.""", json_schema_extra = { "linkml_meta": {'aliases': ['SessionId'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'String'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '1'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '1'}},
         'domain_of': ['FixpNegotiate',
                       'FixpNegotiationResponse',
                       'FixpNegotiationReject',
                       'FixpTopic',
                       'FixpEstablish',
                       'FixpEstablishmentAck',
                       'FixpEstablishmentReject',
                       'FixpContext',
                       'FixpRetransmitRequest',
                       'FixpRetransmission',
                       'FixpRetransmitReject',
                       'FixpTerminate',
                       'FixpFinishedSending',
                       'FixpFinishedReceiving']} })
    next_seq_no: Optional[int] = Field(default=None, description="""The number the sender's next application message will carry.""", json_schema_extra = { "linkml_meta": {'aliases': ['NextSeqNo'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'int'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '11'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '11'}},
         'comments': ["Section 3's table makes it optional, and both resource files "
                      'make it required, so the schema accepts a Context with or '
                      'without it.'],
         'domain_of': ['FixpEstablish',
                       'FixpEstablishmentAck',
                       'FixpSequence',
                       'FixpContext',
                       'FixpRetransmission']} })
    message_kind: Literal["FixpContext"] = Field(default="FixpContext", description="""The class of this message, such as FixpNegotiate. It stands for FIXP's MessageType, which every message carries.""", json_schema_extra = { "linkml_meta": {'aliases': ['MessageType'],
         'designates_type': True,
         'domain_of': ['FixpMessage']} })


class FixpUnsequencedHeartbeat(FixpMessage):
    """
    Shows the peer that the session and transport are alive when the sender's flow is unsequenced or empty. It has no fields.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'fixp_flow_of': {'tag': 'fixp_flow_of', 'value': 'own'},
                         'fixp_flow_types': {'tag': 'fixp_flow_types',
                                             'value': 'Unsequenced None'},
                         'fixp_multicast': {'tag': 'fixp_multicast', 'value': 'false'},
                         'fixp_sent_by': {'tag': 'fixp_sent_by', 'value': 'any'},
                         'sbe_name': {'tag': 'sbe_name',
                                      'value': 'UnsequencedHeartbeat'},
                         'sbe_template_id': {'tag': 'sbe_template_id', 'value': '10'}},
         'from_schema': 'https://w3id.org/lmodel/fixp/schema/fixp_messages',
         'in_subset': ['fixp_transferring']})

    message_kind: Literal["FixpUnsequencedHeartbeat"] = Field(default="FixpUnsequencedHeartbeat", description="""The class of this message, such as FixpNegotiate. It stands for FIXP's MessageType, which every message carries.""", json_schema_extra = { "linkml_meta": {'aliases': ['MessageType'],
         'designates_type': True,
         'domain_of': ['FixpMessage']} })


class FixpRetransmitRequest(FixpMessage):
    """
    Asks the peer to resend some messages of its recoverable flow. A party has at most one such request open at a time.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'fixp_flow_of': {'tag': 'fixp_flow_of', 'value': 'peer'},
                         'fixp_flow_types': {'tag': 'fixp_flow_types',
                                             'value': 'Recoverable'},
                         'fixp_multicast': {'tag': 'fixp_multicast', 'value': 'false'},
                         'fixp_sent_by': {'tag': 'fixp_sent_by', 'value': 'any'},
                         'sbe_name': {'tag': 'sbe_name', 'value': 'RetransmitRequest'},
                         'sbe_template_id': {'tag': 'sbe_template_id', 'value': '11'}},
         'from_schema': 'https://w3id.org/lmodel/fixp/schema/fixp_messages',
         'in_subset': ['fixp_transferring'],
         'slot_usage': {'from_seq_no': {'description': 'Where the requested run '
                                                       'starts, by sequence number.',
                                        'name': 'from_seq_no',
                                        'required': True},
                        'message_count': {'description': 'How many messages are asked '
                                                         'for.',
                                          'name': 'message_count',
                                          'required': True},
                        'request_time': {'description': 'When the request was made, '
                                                        'which also tells this request '
                                                        'apart from others.',
                                         'name': 'request_time',
                                         'required': True},
                        'session_id': {'name': 'session_id', 'required': True}}})

    session_id: str = Field(default=..., description="""The session's identifier, which the client chooses and never uses again.""", json_schema_extra = { "linkml_meta": {'aliases': ['SessionId'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'String'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '1'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '1'}},
         'domain_of': ['FixpNegotiate',
                       'FixpNegotiationResponse',
                       'FixpNegotiationReject',
                       'FixpTopic',
                       'FixpEstablish',
                       'FixpEstablishmentAck',
                       'FixpEstablishmentReject',
                       'FixpContext',
                       'FixpRetransmitRequest',
                       'FixpRetransmission',
                       'FixpRetransmitReject',
                       'FixpTerminate',
                       'FixpFinishedSending',
                       'FixpFinishedReceiving']} })
    request_time: int = Field(default=..., description="""When the request was made, which also tells this request apart from others.""", json_schema_extra = { "linkml_meta": {'aliases': ['Timestamp'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'int'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '2'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '2'}},
         'domain_of': ['FixpNegotiate', 'FixpEstablish', 'FixpRetransmitRequest']} })
    from_seq_no: int = Field(default=..., description="""Where the requested run starts, by sequence number.""", json_schema_extra = { "linkml_meta": {'aliases': ['FromSeqNo'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'int'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '13'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '13'}},
         'domain_of': ['FixpRetransmitRequest', 'FixpApplied', 'FixpNotApplied']} })
    message_count: int = Field(default=..., description="""How many messages are asked for.""", json_schema_extra = { "linkml_meta": {'aliases': ['Count'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'int'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '14'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '14'}},
         'domain_of': ['FixpRetransmitRequest',
                       'FixpRetransmission',
                       'FixpApplied',
                       'FixpNotApplied']} })
    message_kind: Literal["FixpRetransmitRequest"] = Field(default="FixpRetransmitRequest", description="""The class of this message, such as FixpNegotiate. It stands for FIXP's MessageType, which every message carries.""", json_schema_extra = { "linkml_meta": {'aliases': ['MessageType'],
         'designates_type': True,
         'domain_of': ['FixpMessage']} })


class FixpRetransmission(FixpMessage):
    """
    Introduces a batch of resent messages, which are numbered by counting from the number it gives. A request may be answered in several batches.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'fixp_flow_of': {'tag': 'fixp_flow_of', 'value': 'own'},
                         'fixp_flow_types': {'tag': 'fixp_flow_types',
                                             'value': 'Recoverable'},
                         'fixp_multicast': {'tag': 'fixp_multicast', 'value': 'false'},
                         'fixp_sent_by': {'tag': 'fixp_sent_by', 'value': 'any'},
                         'sbe_name': {'tag': 'sbe_name', 'value': 'Retransmission'},
                         'sbe_template_id': {'tag': 'sbe_template_id', 'value': '12'}},
         'from_schema': 'https://w3id.org/lmodel/fixp/schema/fixp_messages',
         'in_subset': ['fixp_transferring'],
         'slot_usage': {'message_count': {'description': 'How many resent messages the '
                                                         'batch holds.',
                                          'name': 'message_count',
                                          'required': True},
                        'next_seq_no': {'description': "The number the batch's first "
                                                       'message carries.',
                                        'name': 'next_seq_no',
                                        'required': True},
                        'request_timestamp': {'description': 'The request_time of the '
                                                             'RetransmitRequest this '
                                                             'batch answers.',
                                              'name': 'request_timestamp',
                                              'required': True},
                        'session_id': {'name': 'session_id', 'required': True}}})

    session_id: str = Field(default=..., description="""The session's identifier, which the client chooses and never uses again.""", json_schema_extra = { "linkml_meta": {'aliases': ['SessionId'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'String'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '1'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '1'}},
         'domain_of': ['FixpNegotiate',
                       'FixpNegotiationResponse',
                       'FixpNegotiationReject',
                       'FixpTopic',
                       'FixpEstablish',
                       'FixpEstablishmentAck',
                       'FixpEstablishmentReject',
                       'FixpContext',
                       'FixpRetransmitRequest',
                       'FixpRetransmission',
                       'FixpRetransmitReject',
                       'FixpTerminate',
                       'FixpFinishedSending',
                       'FixpFinishedReceiving']} })
    request_timestamp: int = Field(default=..., description="""The request_time of the RetransmitRequest this batch answers.""", json_schema_extra = { "linkml_meta": {'aliases': ['RequestTimestamp'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'int'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '5'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '5'}},
         'domain_of': ['FixpNegotiationResponse',
                       'FixpNegotiationReject',
                       'FixpEstablishmentAck',
                       'FixpEstablishmentReject',
                       'FixpRetransmission',
                       'FixpRetransmitReject']} })
    next_seq_no: int = Field(default=..., description="""The number the batch's first message carries.""", json_schema_extra = { "linkml_meta": {'aliases': ['NextSeqNo'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'int'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '11'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '11'}},
         'domain_of': ['FixpEstablish',
                       'FixpEstablishmentAck',
                       'FixpSequence',
                       'FixpContext',
                       'FixpRetransmission']} })
    message_count: int = Field(default=..., description="""How many resent messages the batch holds.""", json_schema_extra = { "linkml_meta": {'aliases': ['Count'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'int'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '14'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '14'}},
         'domain_of': ['FixpRetransmitRequest',
                       'FixpRetransmission',
                       'FixpApplied',
                       'FixpNotApplied']} })
    message_kind: Literal["FixpRetransmission"] = Field(default="FixpRetransmission", description="""The class of this message, such as FixpNegotiate. It stands for FIXP's MessageType, which every message carries.""", json_schema_extra = { "linkml_meta": {'aliases': ['MessageType'],
         'designates_type': True,
         'domain_of': ['FixpMessage']} })


class FixpRetransmitReject(FixpMessage):
    """
    Refuses a RetransmitRequest, with a code saying why.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'fixp_flow_of': {'tag': 'fixp_flow_of', 'value': 'own'},
                         'fixp_flow_types': {'tag': 'fixp_flow_types',
                                             'value': 'Recoverable'},
                         'fixp_multicast': {'tag': 'fixp_multicast', 'value': 'false'},
                         'fixp_sent_by': {'tag': 'fixp_sent_by', 'value': 'any'},
                         'sbe_name': {'tag': 'sbe_name', 'value': 'RestransmitReject'},
                         'sbe_template_id': {'tag': 'sbe_template_id', 'value': '13'}},
         'comments': ["The resource files and section 4's table spell its name "
                      'RestransmitReject. The summary in section 6 does not list it; '
                      'it answers a RetransmitRequest, so it belongs to recoverable '
                      'flows.'],
         'from_schema': 'https://w3id.org/lmodel/fixp/schema/fixp_messages',
         'in_subset': ['fixp_transferring'],
         'slot_usage': {'request_timestamp': {'description': 'The request_time of the '
                                                             'RetransmitRequest this '
                                                             'message refuses.',
                                              'name': 'request_timestamp',
                                              'required': True},
                        'retransmit_reject_code': {'name': 'retransmit_reject_code',
                                                   'required': True},
                        'session_id': {'name': 'session_id', 'required': True}}})

    session_id: str = Field(default=..., description="""The session's identifier, which the client chooses and never uses again.""", json_schema_extra = { "linkml_meta": {'aliases': ['SessionId'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'String'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '1'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '1'}},
         'domain_of': ['FixpNegotiate',
                       'FixpNegotiationResponse',
                       'FixpNegotiationReject',
                       'FixpTopic',
                       'FixpEstablish',
                       'FixpEstablishmentAck',
                       'FixpEstablishmentReject',
                       'FixpContext',
                       'FixpRetransmitRequest',
                       'FixpRetransmission',
                       'FixpRetransmitReject',
                       'FixpTerminate',
                       'FixpFinishedSending',
                       'FixpFinishedReceiving']} })
    request_timestamp: int = Field(default=..., description="""The request_time of the RetransmitRequest this message refuses.""", json_schema_extra = { "linkml_meta": {'aliases': ['RequestTimestamp'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'int'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '5'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '5'}},
         'domain_of': ['FixpNegotiationResponse',
                       'FixpNegotiationReject',
                       'FixpEstablishmentAck',
                       'FixpEstablishmentReject',
                       'FixpRetransmission',
                       'FixpRetransmitReject']} })
    retransmit_reject_code: FixpRetransmitRejectCode = Field(default=..., description="""Why the sender will not resend the range.""", json_schema_extra = { "linkml_meta": {'aliases': ['Code', 'RetransmitRejectCode'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'int'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '15'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '15'}},
         'domain_of': ['FixpRetransmitReject']} })
    reason_text: Optional[str] = Field(default=None, description="""Free text that says more about the code beside it.""", json_schema_extra = { "linkml_meta": {'aliases': ['Reason'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'String'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '8'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '8'}},
         'domain_of': ['FixpNegotiationReject',
                       'FixpEstablishmentReject',
                       'FixpRetransmitReject',
                       'FixpTerminate']} })
    message_kind: Literal["FixpRetransmitReject"] = Field(default="FixpRetransmitReject", description="""The class of this message, such as FixpNegotiate. It stands for FIXP's MessageType, which every message carries.""", json_schema_extra = { "linkml_meta": {'aliases': ['MessageType'],
         'designates_type': True,
         'domain_of': ['FixpMessage']} })


class FixpTerminate(FixpMessage):
    """
    Releases the session from its transport without ending the session, which can be bound again later. The peer answers with a Terminate, and after its own Terminate a party sends nothing more.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'fixp_flow_types': {'tag': 'fixp_flow_types',
                                             'value': 'Recoverable Idempotent '
                                                      'Unsequenced None'},
                         'fixp_multicast': {'tag': 'fixp_multicast', 'value': 'false'},
                         'fixp_sent_by': {'tag': 'fixp_sent_by', 'value': 'any'},
                         'sbe_name': {'tag': 'sbe_name', 'value': 'Terminate'},
                         'sbe_template_id': {'tag': 'sbe_template_id', 'value': '14'}},
         'from_schema': 'https://w3id.org/lmodel/fixp/schema/fixp_messages',
         'in_subset': ['fixp_unbinding'],
         'slot_usage': {'session_id': {'name': 'session_id', 'required': True},
                        'termination_code': {'name': 'termination_code',
                                             'required': True}}})

    session_id: str = Field(default=..., description="""The session's identifier, which the client chooses and never uses again.""", json_schema_extra = { "linkml_meta": {'aliases': ['SessionId'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'String'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '1'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '1'}},
         'domain_of': ['FixpNegotiate',
                       'FixpNegotiationResponse',
                       'FixpNegotiationReject',
                       'FixpTopic',
                       'FixpEstablish',
                       'FixpEstablishmentAck',
                       'FixpEstablishmentReject',
                       'FixpContext',
                       'FixpRetransmitRequest',
                       'FixpRetransmission',
                       'FixpRetransmitReject',
                       'FixpTerminate',
                       'FixpFinishedSending',
                       'FixpFinishedReceiving']} })
    termination_code: FixpTerminationCode = Field(default=..., description="""Why the party releases the session from the transport.""", json_schema_extra = { "linkml_meta": {'aliases': ['Code', 'TerminationCode'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'int'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '16'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '16'}},
         'domain_of': ['FixpTerminate']} })
    reason_text: Optional[str] = Field(default=None, description="""Free text that says more about the code beside it.""", json_schema_extra = { "linkml_meta": {'aliases': ['Reason'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'String'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '8'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '8'}},
         'domain_of': ['FixpNegotiationReject',
                       'FixpEstablishmentReject',
                       'FixpRetransmitReject',
                       'FixpTerminate']} })
    message_kind: Literal["FixpTerminate"] = Field(default="FixpTerminate", description="""The class of this message, such as FixpNegotiate. It stands for FIXP's MessageType, which every message carries.""", json_schema_extra = { "linkml_meta": {'aliases': ['MessageType'],
         'designates_type': True,
         'domain_of': ['FixpMessage']} })


class FixpFinishedSending(FixpMessage):
    """
    Says that the sender's flow has carried its last application message, which begins finalization. It is repeated as the heartbeat until the answer comes.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'fixp_flow_of': {'tag': 'fixp_flow_of', 'value': 'own'},
                         'fixp_flow_types': {'tag': 'fixp_flow_types',
                                             'value': 'Recoverable Idempotent '
                                                      'Unsequenced None'},
                         'fixp_multicast': {'tag': 'fixp_multicast', 'value': 'true'},
                         'fixp_sent_by': {'tag': 'fixp_sent_by', 'value': 'any'},
                         'sbe_name': {'tag': 'sbe_name', 'value': 'FinishedSending'},
                         'sbe_template_id': {'tag': 'sbe_template_id', 'value': '15'}},
         'from_schema': 'https://w3id.org/lmodel/fixp/schema/fixp_messages',
         'in_subset': ['fixp_finalizing'],
         'slot_usage': {'last_seq_no': {'comments': ["Optional in section 4's table "
                                                     'and in the SBE schema, required '
                                                     'in the repository file. Section '
                                                     '4 asks for it whenever the flow '
                                                     'is recoverable or idempotent, '
                                                     'which tests/fixp_rules.py checks '
                                                     'in an exchange.'],
                                        'name': 'last_seq_no'},
                        'session_id': {'name': 'session_id', 'required': True}}})

    session_id: str = Field(default=..., description="""The session's identifier, which the client chooses and never uses again.""", json_schema_extra = { "linkml_meta": {'aliases': ['SessionId'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'String'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '1'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '1'}},
         'domain_of': ['FixpNegotiate',
                       'FixpNegotiationResponse',
                       'FixpNegotiationReject',
                       'FixpTopic',
                       'FixpEstablish',
                       'FixpEstablishmentAck',
                       'FixpEstablishmentReject',
                       'FixpContext',
                       'FixpRetransmitRequest',
                       'FixpRetransmission',
                       'FixpRetransmitReject',
                       'FixpTerminate',
                       'FixpFinishedSending',
                       'FixpFinishedReceiving']} })
    last_seq_no: Optional[int] = Field(default=None, description="""The number carried by the flow's final application message.""", json_schema_extra = { "linkml_meta": {'aliases': ['LastSeqNo'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'int'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '17'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '17'}},
         'comments': ["Optional in section 4's table and in the SBE schema, required "
                      'in the repository file. Section 4 asks for it whenever the flow '
                      'is recoverable or idempotent, which tests/fixp_rules.py checks '
                      'in an exchange.'],
         'domain_of': ['FixpFinishedSending']} })
    message_kind: Literal["FixpFinishedSending"] = Field(default="FixpFinishedSending", description="""The class of this message, such as FixpNegotiate. It stands for FIXP's MessageType, which every message carries.""", json_schema_extra = { "linkml_meta": {'aliases': ['MessageType'],
         'designates_type': True,
         'domain_of': ['FixpMessage']} })


class FixpFinishedReceiving(FixpMessage):
    """
    Answers FinishedSending once the last message of the peer's flow has been processed. After it the session is finalized and its identifier is spent.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'fixp_flow_of': {'tag': 'fixp_flow_of', 'value': 'peer'},
                         'fixp_flow_types': {'tag': 'fixp_flow_types',
                                             'value': 'Recoverable Idempotent '
                                                      'Unsequenced None'},
                         'fixp_multicast': {'tag': 'fixp_multicast', 'value': 'true'},
                         'fixp_sent_by': {'tag': 'fixp_sent_by', 'value': 'any'},
                         'sbe_name': {'tag': 'sbe_name', 'value': 'FinishedReceiving'},
                         'sbe_template_id': {'tag': 'sbe_template_id', 'value': '16'}},
         'from_schema': 'https://w3id.org/lmodel/fixp/schema/fixp_messages',
         'in_subset': ['fixp_finalizing'],
         'slot_usage': {'session_id': {'name': 'session_id', 'required': True}}})

    session_id: str = Field(default=..., description="""The session's identifier, which the client chooses and never uses again.""", json_schema_extra = { "linkml_meta": {'aliases': ['SessionId'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'String'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '1'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '1'}},
         'domain_of': ['FixpNegotiate',
                       'FixpNegotiationResponse',
                       'FixpNegotiationReject',
                       'FixpTopic',
                       'FixpEstablish',
                       'FixpEstablishmentAck',
                       'FixpEstablishmentReject',
                       'FixpContext',
                       'FixpRetransmitRequest',
                       'FixpRetransmission',
                       'FixpRetransmitReject',
                       'FixpTerminate',
                       'FixpFinishedSending',
                       'FixpFinishedReceiving']} })
    message_kind: Literal["FixpFinishedReceiving"] = Field(default="FixpFinishedReceiving", description="""The class of this message, such as FixpNegotiate. It stands for FIXP's MessageType, which every message carries.""", json_schema_extra = { "linkml_meta": {'aliases': ['MessageType'],
         'designates_type': True,
         'domain_of': ['FixpMessage']} })


class FixpApplied(FixpMessage):
    """
    An optional application message telling the party that sends an idempotent flow which of its operations took effect, where no business message already says so.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'fixp_flow_of': {'tag': 'fixp_flow_of', 'value': 'peer'},
                         'fixp_flow_types': {'tag': 'fixp_flow_types',
                                             'value': 'Idempotent'},
                         'fixp_multicast': {'tag': 'fixp_multicast', 'value': 'false'},
                         'fixp_sent_by': {'tag': 'fixp_sent_by', 'value': 'any'},
                         'sbe_name': {'tag': 'sbe_name', 'value': 'Applied'},
                         'sbe_template_id': {'tag': 'sbe_template_id', 'value': '17'}},
         'comments': ['Like any application message, it uses up one number in the '
                      'sequence of the flow it travels on.'],
         'from_schema': 'https://w3id.org/lmodel/fixp/schema/fixp_messages',
         'in_subset': ['fixp_transferring'],
         'slot_usage': {'from_seq_no': {'description': 'Where the run of operations '
                                                       'that took effect starts.',
                                        'name': 'from_seq_no',
                                        'required': True},
                        'message_count': {'description': 'How many operations in a row '
                                                         'took effect.',
                                          'name': 'message_count',
                                          'required': True}}})

    from_seq_no: int = Field(default=..., description="""Where the run of operations that took effect starts.""", json_schema_extra = { "linkml_meta": {'aliases': ['FromSeqNo'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'int'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '13'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '13'}},
         'domain_of': ['FixpRetransmitRequest', 'FixpApplied', 'FixpNotApplied']} })
    message_count: int = Field(default=..., description="""How many operations in a row took effect.""", json_schema_extra = { "linkml_meta": {'aliases': ['Count'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'int'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '14'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '14'}},
         'domain_of': ['FixpRetransmitRequest',
                       'FixpRetransmission',
                       'FixpApplied',
                       'FixpNotApplied']} })
    message_kind: Literal["FixpApplied"] = Field(default="FixpApplied", description="""The class of this message, such as FixpNegotiate. It stands for FIXP's MessageType, which every message carries.""", json_schema_extra = { "linkml_meta": {'aliases': ['MessageType'],
         'designates_type': True,
         'domain_of': ['FixpMessage']} })


class FixpNotApplied(FixpMessage):
    """
    An application message telling the party that sends an idempotent flow about a gap: a run of operations that did not take effect. That party's application decides what to do.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'fixp_flow_of': {'tag': 'fixp_flow_of', 'value': 'peer'},
                         'fixp_flow_types': {'tag': 'fixp_flow_types',
                                             'value': 'Idempotent'},
                         'fixp_multicast': {'tag': 'fixp_multicast', 'value': 'false'},
                         'fixp_sent_by': {'tag': 'fixp_sent_by', 'value': 'any'},
                         'sbe_name': {'tag': 'sbe_name', 'value': 'NotApplied'},
                         'sbe_template_id': {'tag': 'sbe_template_id', 'value': '18'}},
         'comments': ['Like any application message, it uses up one number in the '
                      'sequence of the flow it travels on.'],
         'from_schema': 'https://w3id.org/lmodel/fixp/schema/fixp_messages',
         'in_subset': ['fixp_transferring'],
         'slot_usage': {'from_seq_no': {'description': 'Where the run of operations '
                                                       'that failed to take effect '
                                                       'starts.',
                                        'name': 'from_seq_no',
                                        'required': True},
                        'message_count': {'description': 'How many operations in a row '
                                                         'did not take effect.',
                                          'name': 'message_count',
                                          'required': True}}})

    from_seq_no: int = Field(default=..., description="""Where the run of operations that failed to take effect starts.""", json_schema_extra = { "linkml_meta": {'aliases': ['FromSeqNo'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'int'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '13'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '13'}},
         'domain_of': ['FixpRetransmitRequest', 'FixpApplied', 'FixpNotApplied']} })
    message_count: int = Field(default=..., description="""How many operations in a row did not take effect.""", json_schema_extra = { "linkml_meta": {'aliases': ['Count'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'int'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '14'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '14'}},
         'domain_of': ['FixpRetransmitRequest',
                       'FixpRetransmission',
                       'FixpApplied',
                       'FixpNotApplied']} })
    message_kind: Literal["FixpNotApplied"] = Field(default="FixpNotApplied", description="""The class of this message, such as FixpNegotiate. It stands for FIXP's MessageType, which every message carries.""", json_schema_extra = { "linkml_meta": {'aliases': ['MessageType'],
         'designates_type': True,
         'domain_of': ['FixpMessage']} })


class FixpMessageTemplate(FixpMessage):
    """
    Hands the peer a template or schema it needs to read messages in an encoding that templates drive. There is no fixed moment for sending it.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'fixp_flow_types': {'tag': 'fixp_flow_types',
                                             'value': 'Recoverable Idempotent '
                                                      'Unsequenced None'},
                         'fixp_multicast': {'tag': 'fixp_multicast', 'value': 'true'},
                         'fixp_sent_by': {'tag': 'fixp_sent_by', 'value': 'any'},
                         'sbe_name': {'tag': 'sbe_name', 'value': 'MessageTemplate'},
                         'sbe_template_id': {'tag': 'sbe_template_id', 'value': '19'}},
         'comments': ['A publisher does well to repeat it for late listeners. On a '
                      'shared transport it applies to every session there.'],
         'from_schema': 'https://w3id.org/lmodel/fixp/schema/fixp_messages',
         'in_subset': ['fixp_initialization'],
         'slot_usage': {'sofh_encoding_type': {'name': 'sofh_encoding_type',
                                               'required': True},
                        'template': {'name': 'template', 'required': True}}})

    sofh_encoding_type: int = Field(default=..., description="""The code that the Simple Open Framing Header registers for the encoding a template is written for.""", json_schema_extra = { "linkml_meta": {'aliases': ['EncodingType'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'int'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '19'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '18'}},
         'domain_of': ['FixpMessageTemplate']} })
    effective_time: Optional[int] = Field(default=None, description="""When the template comes into force. Without it, the template applies at once.""", json_schema_extra = { "linkml_meta": {'aliases': ['EffectiveTime'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'int'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '20'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '19'}},
         'domain_of': ['FixpMessageTemplate']} })
    template_version: Optional[str] = Field(default=None, description="""The template's version and format, for an encoding whose templates do not state them.""", json_schema_extra = { "linkml_meta": {'aliases': ['Version'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'data'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '21'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '20'}},
         'domain_of': ['FixpMessageTemplate']} })
    template: str = Field(default=..., description="""The template itself, as octets.""", json_schema_extra = { "linkml_meta": {'aliases': ['Template'],
         'annotations': {'repository_datatype': {'tag': 'repository_datatype',
                                                 'value': 'data'},
                         'repository_field_id': {'tag': 'repository_field_id',
                                                 'value': '22'},
                         'sbe_field_id': {'tag': 'sbe_field_id', 'value': '21'}},
         'domain_of': ['FixpMessageTemplate']} })
    message_kind: Literal["FixpMessageTemplate"] = Field(default="FixpMessageTemplate", description="""The class of this message, such as FixpNegotiate. It stands for FIXP's MessageType, which every message carries.""", json_schema_extra = { "linkml_meta": {'aliases': ['MessageType'],
         'designates_type': True,
         'domain_of': ['FixpMessage']} })


class FixpExchange(ConfiguredBaseModel):
    """
    The messages of one session in the order they were sent, as a test case, a worked example or a captured log.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/lmodel/fixp/schema/fixp_exchange',
         'tree_root': True})

    id: str = Field(default=..., description="""The identifier of an exchange or a rules-of-engagement record.""", json_schema_extra = { "linkml_meta": {'domain_of': ['FixpExchange', 'FixpRulesOfEngagement']} })
    description: Optional[str] = Field(default=None, description="""Free text about a record, for the people who read it.""", json_schema_extra = { "linkml_meta": {'domain_of': ['FixpExchange', 'FixpRulesOfEngagement'],
         'slot_uri': 'schema:description'} })
    session_kind: FixpSessionKind = Field(default=..., description="""Which of the two forms the session takes.""", json_schema_extra = { "linkml_meta": {'domain_of': ['FixpExchange']} })
    multiplexed: Optional[bool] = Field(default=None, description="""Whether the transport carries other sessions too, so that Context takes the place of Sequence.""", json_schema_extra = { "linkml_meta": {'domain_of': ['FixpExchange']} })
    exchange_steps: list[FixpExchangeStep] = Field(default=..., description="""Each step of the exchange, in order.""", min_length=1, json_schema_extra = { "linkml_meta": {'domain_of': ['FixpExchange']} })


class FixpExchangeStep(ConfiguredBaseModel):
    """
    One step: a FIXP message, or a run of application messages whose content FIXP does not define, and the side that sent it.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'exactly_one_of': [{'slot_conditions': {'fixp_message': {'name': 'fixp_message',
                                                                  'value_presence': 'PRESENT'}}},
                            {'slot_conditions': {'application_message_count': {'name': 'application_message_count',
                                                                               'value_presence': 'PRESENT'}}}],
         'from_schema': 'https://w3id.org/lmodel/fixp/schema/fixp_exchange'})

    sent_by: FixpParty = Field(default=..., description="""The side that sent this step.""", json_schema_extra = { "linkml_meta": {'domain_of': ['FixpExchangeStep']} })
    fixp_message: Optional[Union[FixpNegotiate,FixpNegotiationResponse,FixpNegotiationReject,FixpTopic,FixpEstablish,FixpEstablishmentAck,FixpEstablishmentReject,FixpSequence,FixpContext,FixpUnsequencedHeartbeat,FixpRetransmitRequest,FixpRetransmission,FixpRetransmitReject,FixpTerminate,FixpFinishedSending,FixpFinishedReceiving,FixpApplied,FixpNotApplied,FixpMessageTemplate]] = Field(default=None, description="""The FIXP message sent.""", json_schema_extra = { "linkml_meta": {'domain_of': ['FixpExchangeStep']} })
    application_message_count: Optional[int] = Field(default=None, description="""How many application messages went out one after another. On a sequenced flow each takes the next sequence number.""", ge=1, json_schema_extra = { "linkml_meta": {'domain_of': ['FixpExchangeStep']} })


class FixpRulesOfEngagement(ConfiguredBaseModel):
    """
    What two counterparties agree on for one FIXP service, layer by layer, for the client and for the server.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'comments': ['Appendix B calls its checklist an aid, and FIXP leaves each of '
                      'these choices to the counterparties.'],
         'from_schema': 'https://w3id.org/lmodel/fixp/schema/fixp_engagement'})

    id: str = Field(default=..., description="""The identifier of an exchange or a rules-of-engagement record.""", json_schema_extra = { "linkml_meta": {'domain_of': ['FixpExchange', 'FixpRulesOfEngagement']} })
    description: Optional[str] = Field(default=None, description="""Free text about a record, for the people who read it.""", json_schema_extra = { "linkml_meta": {'domain_of': ['FixpExchange', 'FixpRulesOfEngagement'],
         'slot_uri': 'schema:description'} })
    client_stack: FixpStackProfile = Field(default=..., description="""What the client side uses.""", json_schema_extra = { "linkml_meta": {'domain_of': ['FixpRulesOfEngagement']} })
    server_stack: FixpStackProfile = Field(default=..., description="""What the server side uses.""", json_schema_extra = { "linkml_meta": {'domain_of': ['FixpRulesOfEngagement']} })


class FixpStackProfile(ConfiguredBaseModel):
    """
    One side's choices at each layer of the stack: application, presentation, session, security and transport.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/lmodel/fixp/schema/fixp_engagement'})

    application_recovery: Optional[bool] = Field(default=None, description="""Whether this side's applications recover lost messages themselves.""", json_schema_extra = { "linkml_meta": {'annotations': {'stack_layer': {'tag': 'stack_layer', 'value': 'application'}},
         'domain_of': ['FixpStackProfile']} })
    application_fix_version: Optional[str] = Field(default=None, description="""The FIX version of the application messages, such as FIX.Latest.""", json_schema_extra = { "linkml_meta": {'annotations': {'stack_layer': {'tag': 'stack_layer', 'value': 'application'}},
         'domain_of': ['FixpStackProfile']} })
    service_pack: Optional[str] = Field(default=None, description="""The FIX service pack, where the version has them.""", json_schema_extra = { "linkml_meta": {'annotations': {'stack_layer': {'tag': 'stack_layer', 'value': 'application'}},
         'domain_of': ['FixpStackProfile']} })
    extension_packs: Optional[list[str]] = Field(default=None, description="""The FIX extension packs in use.""", json_schema_extra = { "linkml_meta": {'annotations': {'stack_layer': {'tag': 'stack_layer', 'value': 'application'}},
         'domain_of': ['FixpStackProfile']} })
    message_encoding: Optional[str] = Field(default=None, description="""How messages are encoded, such as Simple Binary Encoding.""", json_schema_extra = { "linkml_meta": {'annotations': {'stack_layer': {'tag': 'stack_layer',
                                         'value': 'presentation'}},
         'domain_of': ['FixpStackProfile']} })
    encoding_version: Optional[str] = Field(default=None, description="""The version of that encoding.""", json_schema_extra = { "linkml_meta": {'annotations': {'stack_layer': {'tag': 'stack_layer',
                                         'value': 'presentation'}},
         'domain_of': ['FixpStackProfile']} })
    message_schemas: Optional[list[str]] = Field(default=None, description="""The message schemas or templates the encoding uses.""", json_schema_extra = { "linkml_meta": {'annotations': {'stack_layer': {'tag': 'stack_layer',
                                         'value': 'presentation'}},
         'domain_of': ['FixpStackProfile']} })
    framing: Optional[str] = Field(default=None, description="""What marks where one message ends and the next begins, such as the Simple Open Framing Header.""", json_schema_extra = { "linkml_meta": {'annotations': {'stack_layer': {'tag': 'stack_layer',
                                         'value': 'presentation'}},
         'domain_of': ['FixpStackProfile']} })
    supported_flow_types: Optional[list[FixpFlowType]] = Field(default=None, description="""The flow types this side accepts or offers.""", json_schema_extra = { "linkml_meta": {'annotations': {'stack_layer': {'tag': 'stack_layer', 'value': 'session'}},
         'domain_of': ['FixpStackProfile']} })
    tls_version: Optional[str] = Field(default=None, description="""The TLS version that protects the transport.""", json_schema_extra = { "linkml_meta": {'annotations': {'stack_layer': {'tag': 'stack_layer', 'value': 'security'}},
         'domain_of': ['FixpStackProfile']} })
    authentication_methods: Optional[list[str]] = Field(default=None, description="""How the parties prove who they are.""", json_schema_extra = { "linkml_meta": {'annotations': {'stack_layer': {'tag': 'stack_layer', 'value': 'security'}},
         'domain_of': ['FixpStackProfile']} })
    cipher_suites: Optional[list[str]] = Field(default=None, description="""The cipher suites allowed.""", json_schema_extra = { "linkml_meta": {'annotations': {'stack_layer': {'tag': 'stack_layer', 'value': 'security'}},
         'domain_of': ['FixpStackProfile']} })
    transports: Optional[list[str]] = Field(default=None, description="""The transports this side can use, for example TCP, or UDP with multicast.""", json_schema_extra = { "linkml_meta": {'annotations': {'stack_layer': {'tag': 'stack_layer', 'value': 'transport'}},
         'domain_of': ['FixpStackProfile']} })
    network_protocols: Optional[list[str]] = Field(default=None, description="""Any other network protocols in use.""", json_schema_extra = { "linkml_meta": {'annotations': {'stack_layer': {'tag': 'stack_layer', 'value': 'transport'}},
         'domain_of': ['FixpStackProfile']} })


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
FixpMessage.model_rebuild()
FixpNegotiate.model_rebuild()
FixpNegotiationResponse.model_rebuild()
FixpNegotiationReject.model_rebuild()
FixpTopic.model_rebuild()
FixpEstablish.model_rebuild()
FixpEstablishmentAck.model_rebuild()
FixpEstablishmentReject.model_rebuild()
FixpSequence.model_rebuild()
FixpContext.model_rebuild()
FixpUnsequencedHeartbeat.model_rebuild()
FixpRetransmitRequest.model_rebuild()
FixpRetransmission.model_rebuild()
FixpRetransmitReject.model_rebuild()
FixpTerminate.model_rebuild()
FixpFinishedSending.model_rebuild()
FixpFinishedReceiving.model_rebuild()
FixpApplied.model_rebuild()
FixpNotApplied.model_rebuild()
FixpMessageTemplate.model_rebuild()
FixpExchange.model_rebuild()
FixpExchangeStep.model_rebuild()
FixpRulesOfEngagement.model_rebuild()
FixpStackProfile.model_rebuild()
