# Auto generated from fixp.yaml by pythongen.py version: 0.0.1
# Schema: fixp
#
# id: https://w3id.org/lmodel/fixp
# description: A LinkML model of the FIX Performance Session Layer 1.0, the FIX Trading Community's session protocol for fast trading links. It describes FIXP's session messages, their fields and value lists, exchanges of those messages on one session, and the rules of engagement two parties agree on. A message is described by its fields, so the model works with any encoding.
# license: Apache-2.0

import dataclasses
import re
from dataclasses import dataclass
from datetime import (
    date,
    datetime,
    time
)
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Union
)

from jsonasobj2 import (
    JsonObj,
    as_dict
)
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions
)
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import (
    camelcase,
    sfx,
    underscore
)
from linkml_runtime.utils.metamodelcore import (
    bnode,
    empty_dict,
    empty_list
)
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (
    YAMLRoot,
    extended_float,
    extended_int,
    extended_str
)
from rdflib import (
    Namespace,
    URIRef
)

from linkml_runtime.linkml_model.types import Boolean, Integer, String, Uriorcurie
from linkml_runtime.utils.metamodelcore import Bool, URIorCURIE

metamodel_version = "1.12.0"
version = "1.0"

# Namespaces
FIX_ORCHESTRA = CurieNamespace('fix_orchestra', 'https://w3id.org/lmodel/fix-orchestra/')
FIX_SBE = CurieNamespace('fix_sbe', 'https://w3id.org/lmodel/fix-sbe/')
FIXP = CurieNamespace('fixp', 'https://w3id.org/lmodel/fixp/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = FIXP


# Types
class FixpU8(Integer):
    """ A whole number from 0 to 255, held in eight unsigned bits. """
    type_class_uri = XSD["integer"]
    type_class_curie = "xsd:integer"
    type_name = "fixp_u8"
    type_model_uri = FIXP.FixpU8


class FixpU16(Integer):
    """ A whole number from 0 to 65,535, held in 16 unsigned bits. """
    type_class_uri = XSD["integer"]
    type_class_curie = "xsd:integer"
    type_name = "fixp_u16"
    type_model_uri = FIXP.FixpU16


class FixpU32(Integer):
    """ A whole number from 0 to 4,294,967,295, held in 32 unsigned bits. """
    type_class_uri = XSD["integer"]
    type_class_curie = "xsd:integer"
    type_name = "fixp_u32"
    type_model_uri = FIXP.FixpU32


class FixpU64(Integer):
    """ A whole number from 0 to 18,446,744,073,709,551,615, held in 64 unsigned bits. """
    type_class_uri = XSD["integer"]
    type_class_curie = "xsd:integer"
    type_name = "fixp_u64"
    type_model_uri = FIXP.FixpU64


class FixpUuid(String):
    """ A random UUID of RFC 4122's version 4, written as 32 hexadecimal digits in five groups joined by hyphens. """
    type_class_uri = XSD["string"]
    type_class_curie = "xsd:string"
    type_name = "fixp_uuid"
    type_model_uri = FIXP.FixpUuid


class FixpNanotime(Integer):
    """ A moment, counted in nanoseconds since the Unix epoch and held in 64 unsigned bits. """
    type_class_uri = XSD["integer"]
    type_class_curie = "xsd:integer"
    type_name = "fixp_nanotime"
    type_model_uri = FIXP.FixpNanotime


class FixpDeltaMillisecs(Integer):
    """ A length of time in whole milliseconds, held in 32 unsigned bits. """
    type_class_uri = XSD["integer"]
    type_class_curie = "xsd:integer"
    type_name = "fixp_delta_millisecs"
    type_model_uri = FIXP.FixpDeltaMillisecs


class FixpObject(String):
    """ Octets that FIXP passes through without reading them, written here in base64. """
    type_class_uri = XSD["base64Binary"]
    type_class_curie = "xsd:base64Binary"
    type_name = "fixp_object"
    type_model_uri = FIXP.FixpObject


class FixpString(String):
    """ Text, in UTF-8. """
    type_class_uri = XSD["string"]
    type_class_curie = "xsd:string"
    type_name = "fixp_string"
    type_model_uri = FIXP.FixpString


# Class references
class FixpExchangeId(URIorCURIE):
    pass


class FixpRulesOfEngagementId(URIorCURIE):
    pass


@dataclass(repr=False)
class FixpMessage(YAMLRoot):
    """
    One FIXP message, as its fields would be read from the wire before or after encoding.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIXP["FixpMessage"]
    class_class_curie: ClassVar[str] = "fixp:FixpMessage"
    class_name: ClassVar[str] = "FixpMessage"
    class_model_uri: ClassVar[URIRef] = FIXP.FixpMessage

    message_kind: str = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.message_kind):
            self.MissingRequiredField("message_kind")
        self.message_kind = str(self.class_name)

        super().__post_init__(**kwargs)


    def __new__(cls, *args, **kwargs):

        type_designator = "message_kind"
        if not type_designator in kwargs:
            return super().__new__(cls,*args,**kwargs)
        else:
            type_designator_value = kwargs[type_designator]
            target_cls = cls._class_for("class_name", type_designator_value)


            if target_cls is None:
                raise ValueError(f"Wrong type designator value: class {cls.__name__} "
                                 f"has no subclass with ['class_name']='{kwargs[type_designator]}'")
            return super().__new__(target_cls,*args,**kwargs)



@dataclass(repr=False)
class FixpNegotiate(FixpMessage):
    """
    A client's request to create a session under an identifier it has never used, stating the flow type it will send.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIXP["FixpNegotiate"]
    class_class_curie: ClassVar[str] = "fixp:FixpNegotiate"
    class_name: ClassVar[str] = "FixpNegotiate"
    class_model_uri: ClassVar[URIRef] = FIXP.FixpNegotiate

    message_kind: str = None
    session_id: Union[str, FixpUuid] = None
    request_time: Union[int, FixpNanotime] = None
    client_flow: Union[str, "FixpFlowType"] = None
    credentials: Optional[Union[str, FixpObject]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.session_id):
            self.MissingRequiredField("session_id")
        if not isinstance(self.session_id, FixpUuid):
            self.session_id = FixpUuid(self.session_id)

        if self._is_empty(self.request_time):
            self.MissingRequiredField("request_time")
        if not isinstance(self.request_time, FixpNanotime):
            self.request_time = FixpNanotime(self.request_time)

        if self._is_empty(self.client_flow):
            self.MissingRequiredField("client_flow")
        if not isinstance(self.client_flow, FixpFlowType):
            self.client_flow = FixpFlowType(self.client_flow)

        if self.credentials is not None and not isinstance(self.credentials, FixpObject):
            self.credentials = FixpObject(self.credentials)

        super().__post_init__(**kwargs)
        if self._is_empty(self.message_kind):
            self.MissingRequiredField("message_kind")
        self.message_kind = str(self.class_name)


@dataclass(repr=False)
class FixpNegotiationResponse(FixpMessage):
    """
    A server's acceptance of a new session, stating the flow type it will send back.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIXP["FixpNegotiationResponse"]
    class_class_curie: ClassVar[str] = "fixp:FixpNegotiationResponse"
    class_name: ClassVar[str] = "FixpNegotiationResponse"
    class_model_uri: ClassVar[URIRef] = FIXP.FixpNegotiationResponse

    message_kind: str = None
    session_id: Union[str, FixpUuid] = None
    request_timestamp: Union[int, FixpNanotime] = None
    server_flow: Union[str, "FixpFlowType"] = None
    credentials: Optional[Union[str, FixpObject]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.session_id):
            self.MissingRequiredField("session_id")
        if not isinstance(self.session_id, FixpUuid):
            self.session_id = FixpUuid(self.session_id)

        if self._is_empty(self.request_timestamp):
            self.MissingRequiredField("request_timestamp")
        if not isinstance(self.request_timestamp, FixpNanotime):
            self.request_timestamp = FixpNanotime(self.request_timestamp)

        if self._is_empty(self.server_flow):
            self.MissingRequiredField("server_flow")
        if not isinstance(self.server_flow, FixpFlowType):
            self.server_flow = FixpFlowType(self.server_flow)

        if self.credentials is not None and not isinstance(self.credentials, FixpObject):
            self.credentials = FixpObject(self.credentials)

        super().__post_init__(**kwargs)
        if self._is_empty(self.message_kind):
            self.MissingRequiredField("message_kind")
        self.message_kind = str(self.class_name)


@dataclass(repr=False)
class FixpNegotiationReject(FixpMessage):
    """
    A server's refusal to create a session. The server sends nothing more and closes the transport.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIXP["FixpNegotiationReject"]
    class_class_curie: ClassVar[str] = "fixp:FixpNegotiationReject"
    class_name: ClassVar[str] = "FixpNegotiationReject"
    class_model_uri: ClassVar[URIRef] = FIXP.FixpNegotiationReject

    message_kind: str = None
    session_id: Union[str, FixpUuid] = None
    request_timestamp: Union[int, FixpNanotime] = None
    negotiation_reject_code: Union[str, "FixpNegotiationRejectCode"] = None
    reason_text: Optional[Union[str, FixpString]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.session_id):
            self.MissingRequiredField("session_id")
        if not isinstance(self.session_id, FixpUuid):
            self.session_id = FixpUuid(self.session_id)

        if self._is_empty(self.request_timestamp):
            self.MissingRequiredField("request_timestamp")
        if not isinstance(self.request_timestamp, FixpNanotime):
            self.request_timestamp = FixpNanotime(self.request_timestamp)

        if self._is_empty(self.negotiation_reject_code):
            self.MissingRequiredField("negotiation_reject_code")
        if not isinstance(self.negotiation_reject_code, FixpNegotiationRejectCode):
            self.negotiation_reject_code = FixpNegotiationRejectCode(self.negotiation_reject_code)

        if self.reason_text is not None and not isinstance(self.reason_text, FixpString):
            self.reason_text = FixpString(self.reason_text)

        super().__post_init__(**kwargs)
        if self._is_empty(self.message_kind):
            self.MissingRequiredField("message_kind")
        self.message_kind = str(self.class_name)


@dataclass(repr=False)
class FixpTopic(FixpMessage):
    """
    A multicast publisher's notice that starts a flow and ties the session's short-lived identifier to a lasting
    subject. It is repeated so that late listeners can join.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIXP["FixpTopic"]
    class_class_curie: ClassVar[str] = "fixp:FixpTopic"
    class_name: ClassVar[str] = "FixpTopic"
    class_model_uri: ClassVar[URIRef] = FIXP.FixpTopic

    message_kind: str = None
    session_id: Union[str, FixpUuid] = None
    flow: Union[str, "FixpMulticastFlowType"] = None
    topic_classification: Union[str, FixpObject] = None
    keepalive_interval: Optional[Union[int, FixpDeltaMillisecs]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.session_id):
            self.MissingRequiredField("session_id")
        if not isinstance(self.session_id, FixpUuid):
            self.session_id = FixpUuid(self.session_id)

        if self._is_empty(self.flow):
            self.MissingRequiredField("flow")
        if not isinstance(self.flow, FixpMulticastFlowType):
            self.flow = FixpMulticastFlowType(self.flow)

        if self._is_empty(self.topic_classification):
            self.MissingRequiredField("topic_classification")
        if not isinstance(self.topic_classification, FixpObject):
            self.topic_classification = FixpObject(self.topic_classification)

        if self.keepalive_interval is not None and not isinstance(self.keepalive_interval, FixpDeltaMillisecs):
            self.keepalive_interval = FixpDeltaMillisecs(self.keepalive_interval)

        super().__post_init__(**kwargs)
        if self._is_empty(self.message_kind):
            self.MissingRequiredField("message_kind")
        self.message_kind = str(self.class_name)


@dataclass(repr=False)
class FixpEstablish(FixpMessage):
    """
    A client's request to tie a negotiated session to the very transport this message arrives on. After a
    disconnection it is sent again to re-bind.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIXP["FixpEstablish"]
    class_class_curie: ClassVar[str] = "fixp:FixpEstablish"
    class_name: ClassVar[str] = "FixpEstablish"
    class_model_uri: ClassVar[URIRef] = FIXP.FixpEstablish

    message_kind: str = None
    session_id: Union[str, FixpUuid] = None
    request_time: Union[int, FixpNanotime] = None
    keepalive_interval: Union[int, FixpDeltaMillisecs] = None
    next_seq_no: Optional[Union[int, FixpU64]] = None
    credentials: Optional[Union[str, FixpObject]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.session_id):
            self.MissingRequiredField("session_id")
        if not isinstance(self.session_id, FixpUuid):
            self.session_id = FixpUuid(self.session_id)

        if self._is_empty(self.request_time):
            self.MissingRequiredField("request_time")
        if not isinstance(self.request_time, FixpNanotime):
            self.request_time = FixpNanotime(self.request_time)

        if self._is_empty(self.keepalive_interval):
            self.MissingRequiredField("keepalive_interval")
        if not isinstance(self.keepalive_interval, FixpDeltaMillisecs):
            self.keepalive_interval = FixpDeltaMillisecs(self.keepalive_interval)

        if self.next_seq_no is not None and not isinstance(self.next_seq_no, FixpU64):
            self.next_seq_no = FixpU64(self.next_seq_no)

        if self.credentials is not None and not isinstance(self.credentials, FixpObject):
            self.credentials = FixpObject(self.credentials)

        super().__post_init__(**kwargs)
        if self._is_empty(self.message_kind):
            self.MissingRequiredField("message_kind")
        self.message_kind = str(self.class_name)


@dataclass(repr=False)
class FixpEstablishmentAck(FixpMessage):
    """
    A server's acceptance of the binding. From here, application messages may flow.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIXP["FixpEstablishmentAck"]
    class_class_curie: ClassVar[str] = "fixp:FixpEstablishmentAck"
    class_name: ClassVar[str] = "FixpEstablishmentAck"
    class_model_uri: ClassVar[URIRef] = FIXP.FixpEstablishmentAck

    message_kind: str = None
    session_id: Union[str, FixpUuid] = None
    request_timestamp: Union[int, FixpNanotime] = None
    keepalive_interval: Union[int, FixpDeltaMillisecs] = None
    next_seq_no: Optional[Union[int, FixpU64]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.session_id):
            self.MissingRequiredField("session_id")
        if not isinstance(self.session_id, FixpUuid):
            self.session_id = FixpUuid(self.session_id)

        if self._is_empty(self.request_timestamp):
            self.MissingRequiredField("request_timestamp")
        if not isinstance(self.request_timestamp, FixpNanotime):
            self.request_timestamp = FixpNanotime(self.request_timestamp)

        if self._is_empty(self.keepalive_interval):
            self.MissingRequiredField("keepalive_interval")
        if not isinstance(self.keepalive_interval, FixpDeltaMillisecs):
            self.keepalive_interval = FixpDeltaMillisecs(self.keepalive_interval)

        if self.next_seq_no is not None and not isinstance(self.next_seq_no, FixpU64):
            self.next_seq_no = FixpU64(self.next_seq_no)

        super().__post_init__(**kwargs)
        if self._is_empty(self.message_kind):
            self.MissingRequiredField("message_kind")
        self.message_kind = str(self.class_name)


@dataclass(repr=False)
class FixpEstablishmentReject(FixpMessage):
    """
    A server's refusal of the binding.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIXP["FixpEstablishmentReject"]
    class_class_curie: ClassVar[str] = "fixp:FixpEstablishmentReject"
    class_name: ClassVar[str] = "FixpEstablishmentReject"
    class_model_uri: ClassVar[URIRef] = FIXP.FixpEstablishmentReject

    message_kind: str = None
    session_id: Union[str, FixpUuid] = None
    request_timestamp: Union[int, FixpNanotime] = None
    establishment_reject_code: Union[str, "FixpEstablishmentRejectCode"] = None
    reason_text: Optional[Union[str, FixpString]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.session_id):
            self.MissingRequiredField("session_id")
        if not isinstance(self.session_id, FixpUuid):
            self.session_id = FixpUuid(self.session_id)

        if self._is_empty(self.request_timestamp):
            self.MissingRequiredField("request_timestamp")
        if not isinstance(self.request_timestamp, FixpNanotime):
            self.request_timestamp = FixpNanotime(self.request_timestamp)

        if self._is_empty(self.establishment_reject_code):
            self.MissingRequiredField("establishment_reject_code")
        if not isinstance(self.establishment_reject_code, FixpEstablishmentRejectCode):
            self.establishment_reject_code = FixpEstablishmentRejectCode(self.establishment_reject_code)

        if self.reason_text is not None and not isinstance(self.reason_text, FixpString):
            self.reason_text = FixpString(self.reason_text)

        super().__post_init__(**kwargs)
        if self._is_empty(self.message_kind):
            self.MissingRequiredField("message_kind")
        self.message_kind = str(self.class_name)


@dataclass(repr=False)
class FixpSequence(FixpMessage):
    """
    Starts the numbering of a sequenced flow, so that the application messages after it are numbered by counting up
    from the value it carries. Sent when idle, it is also the heartbeat.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIXP["FixpSequence"]
    class_class_curie: ClassVar[str] = "fixp:FixpSequence"
    class_name: ClassVar[str] = "FixpSequence"
    class_model_uri: ClassVar[URIRef] = FIXP.FixpSequence

    message_kind: str = None
    next_seq_no: Union[int, FixpU64] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.next_seq_no):
            self.MissingRequiredField("next_seq_no")
        if not isinstance(self.next_seq_no, FixpU64):
            self.next_seq_no = FixpU64(self.next_seq_no)

        super().__post_init__(**kwargs)
        if self._is_empty(self.message_kind):
            self.MissingRequiredField("message_kind")
        self.message_kind = str(self.class_name)


@dataclass(repr=False)
class FixpContext(FixpMessage):
    """
    On a transport that several sessions share, names the session the following messages belong to and, when the flow
    is sequenced, where its numbering continues.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIXP["FixpContext"]
    class_class_curie: ClassVar[str] = "fixp:FixpContext"
    class_name: ClassVar[str] = "FixpContext"
    class_model_uri: ClassVar[URIRef] = FIXP.FixpContext

    message_kind: str = None
    session_id: Union[str, FixpUuid] = None
    next_seq_no: Optional[Union[int, FixpU64]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.session_id):
            self.MissingRequiredField("session_id")
        if not isinstance(self.session_id, FixpUuid):
            self.session_id = FixpUuid(self.session_id)

        if self.next_seq_no is not None and not isinstance(self.next_seq_no, FixpU64):
            self.next_seq_no = FixpU64(self.next_seq_no)

        super().__post_init__(**kwargs)
        if self._is_empty(self.message_kind):
            self.MissingRequiredField("message_kind")
        self.message_kind = str(self.class_name)


@dataclass(repr=False)
class FixpUnsequencedHeartbeat(FixpMessage):
    """
    Shows the peer that the session and transport are alive when the sender's flow is unsequenced or empty. It has no
    fields.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIXP["FixpUnsequencedHeartbeat"]
    class_class_curie: ClassVar[str] = "fixp:FixpUnsequencedHeartbeat"
    class_name: ClassVar[str] = "FixpUnsequencedHeartbeat"
    class_model_uri: ClassVar[URIRef] = FIXP.FixpUnsequencedHeartbeat

    message_kind: str = None

    def __post_init__(self, *_: str, **kwargs: Any):

        super().__post_init__(**kwargs)
        if self._is_empty(self.message_kind):
            self.MissingRequiredField("message_kind")
        self.message_kind = str(self.class_name)


@dataclass(repr=False)
class FixpRetransmitRequest(FixpMessage):
    """
    Asks the peer to resend some messages of its recoverable flow. A party has at most one such request open at a time.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIXP["FixpRetransmitRequest"]
    class_class_curie: ClassVar[str] = "fixp:FixpRetransmitRequest"
    class_name: ClassVar[str] = "FixpRetransmitRequest"
    class_model_uri: ClassVar[URIRef] = FIXP.FixpRetransmitRequest

    message_kind: str = None
    session_id: Union[str, FixpUuid] = None
    request_time: Union[int, FixpNanotime] = None
    from_seq_no: Union[int, FixpU64] = None
    message_count: Union[int, FixpU32] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.session_id):
            self.MissingRequiredField("session_id")
        if not isinstance(self.session_id, FixpUuid):
            self.session_id = FixpUuid(self.session_id)

        if self._is_empty(self.request_time):
            self.MissingRequiredField("request_time")
        if not isinstance(self.request_time, FixpNanotime):
            self.request_time = FixpNanotime(self.request_time)

        if self._is_empty(self.from_seq_no):
            self.MissingRequiredField("from_seq_no")
        if not isinstance(self.from_seq_no, FixpU64):
            self.from_seq_no = FixpU64(self.from_seq_no)

        if self._is_empty(self.message_count):
            self.MissingRequiredField("message_count")
        if not isinstance(self.message_count, FixpU32):
            self.message_count = FixpU32(self.message_count)

        super().__post_init__(**kwargs)
        if self._is_empty(self.message_kind):
            self.MissingRequiredField("message_kind")
        self.message_kind = str(self.class_name)


@dataclass(repr=False)
class FixpRetransmission(FixpMessage):
    """
    Introduces a batch of resent messages, which are numbered by counting from the number it gives. A request may be
    answered in several batches.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIXP["FixpRetransmission"]
    class_class_curie: ClassVar[str] = "fixp:FixpRetransmission"
    class_name: ClassVar[str] = "FixpRetransmission"
    class_model_uri: ClassVar[URIRef] = FIXP.FixpRetransmission

    message_kind: str = None
    session_id: Union[str, FixpUuid] = None
    request_timestamp: Union[int, FixpNanotime] = None
    next_seq_no: Union[int, FixpU64] = None
    message_count: Union[int, FixpU32] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.session_id):
            self.MissingRequiredField("session_id")
        if not isinstance(self.session_id, FixpUuid):
            self.session_id = FixpUuid(self.session_id)

        if self._is_empty(self.request_timestamp):
            self.MissingRequiredField("request_timestamp")
        if not isinstance(self.request_timestamp, FixpNanotime):
            self.request_timestamp = FixpNanotime(self.request_timestamp)

        if self._is_empty(self.next_seq_no):
            self.MissingRequiredField("next_seq_no")
        if not isinstance(self.next_seq_no, FixpU64):
            self.next_seq_no = FixpU64(self.next_seq_no)

        if self._is_empty(self.message_count):
            self.MissingRequiredField("message_count")
        if not isinstance(self.message_count, FixpU32):
            self.message_count = FixpU32(self.message_count)

        super().__post_init__(**kwargs)
        if self._is_empty(self.message_kind):
            self.MissingRequiredField("message_kind")
        self.message_kind = str(self.class_name)


@dataclass(repr=False)
class FixpRetransmitReject(FixpMessage):
    """
    Refuses a RetransmitRequest, with a code saying why.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIXP["FixpRetransmitReject"]
    class_class_curie: ClassVar[str] = "fixp:FixpRetransmitReject"
    class_name: ClassVar[str] = "FixpRetransmitReject"
    class_model_uri: ClassVar[URIRef] = FIXP.FixpRetransmitReject

    message_kind: str = None
    session_id: Union[str, FixpUuid] = None
    request_timestamp: Union[int, FixpNanotime] = None
    retransmit_reject_code: Union[str, "FixpRetransmitRejectCode"] = None
    reason_text: Optional[Union[str, FixpString]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.session_id):
            self.MissingRequiredField("session_id")
        if not isinstance(self.session_id, FixpUuid):
            self.session_id = FixpUuid(self.session_id)

        if self._is_empty(self.request_timestamp):
            self.MissingRequiredField("request_timestamp")
        if not isinstance(self.request_timestamp, FixpNanotime):
            self.request_timestamp = FixpNanotime(self.request_timestamp)

        if self._is_empty(self.retransmit_reject_code):
            self.MissingRequiredField("retransmit_reject_code")
        if not isinstance(self.retransmit_reject_code, FixpRetransmitRejectCode):
            self.retransmit_reject_code = FixpRetransmitRejectCode(self.retransmit_reject_code)

        if self.reason_text is not None and not isinstance(self.reason_text, FixpString):
            self.reason_text = FixpString(self.reason_text)

        super().__post_init__(**kwargs)
        if self._is_empty(self.message_kind):
            self.MissingRequiredField("message_kind")
        self.message_kind = str(self.class_name)


@dataclass(repr=False)
class FixpTerminate(FixpMessage):
    """
    Releases the session from its transport without ending the session, which can be bound again later. The peer
    answers with a Terminate, and after its own Terminate a party sends nothing more.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIXP["FixpTerminate"]
    class_class_curie: ClassVar[str] = "fixp:FixpTerminate"
    class_name: ClassVar[str] = "FixpTerminate"
    class_model_uri: ClassVar[URIRef] = FIXP.FixpTerminate

    message_kind: str = None
    session_id: Union[str, FixpUuid] = None
    termination_code: Union[str, "FixpTerminationCode"] = None
    reason_text: Optional[Union[str, FixpString]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.session_id):
            self.MissingRequiredField("session_id")
        if not isinstance(self.session_id, FixpUuid):
            self.session_id = FixpUuid(self.session_id)

        if self._is_empty(self.termination_code):
            self.MissingRequiredField("termination_code")
        if not isinstance(self.termination_code, FixpTerminationCode):
            self.termination_code = FixpTerminationCode(self.termination_code)

        if self.reason_text is not None and not isinstance(self.reason_text, FixpString):
            self.reason_text = FixpString(self.reason_text)

        super().__post_init__(**kwargs)
        if self._is_empty(self.message_kind):
            self.MissingRequiredField("message_kind")
        self.message_kind = str(self.class_name)


@dataclass(repr=False)
class FixpFinishedSending(FixpMessage):
    """
    Says that the sender's flow has carried its last application message, which begins finalization. It is repeated as
    the heartbeat until the answer comes.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIXP["FixpFinishedSending"]
    class_class_curie: ClassVar[str] = "fixp:FixpFinishedSending"
    class_name: ClassVar[str] = "FixpFinishedSending"
    class_model_uri: ClassVar[URIRef] = FIXP.FixpFinishedSending

    message_kind: str = None
    session_id: Union[str, FixpUuid] = None
    last_seq_no: Optional[Union[int, FixpU64]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.session_id):
            self.MissingRequiredField("session_id")
        if not isinstance(self.session_id, FixpUuid):
            self.session_id = FixpUuid(self.session_id)

        if self.last_seq_no is not None and not isinstance(self.last_seq_no, FixpU64):
            self.last_seq_no = FixpU64(self.last_seq_no)

        super().__post_init__(**kwargs)
        if self._is_empty(self.message_kind):
            self.MissingRequiredField("message_kind")
        self.message_kind = str(self.class_name)


@dataclass(repr=False)
class FixpFinishedReceiving(FixpMessage):
    """
    Answers FinishedSending once the last message of the peer's flow has been processed. After it the session is
    finalized and its identifier is spent.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIXP["FixpFinishedReceiving"]
    class_class_curie: ClassVar[str] = "fixp:FixpFinishedReceiving"
    class_name: ClassVar[str] = "FixpFinishedReceiving"
    class_model_uri: ClassVar[URIRef] = FIXP.FixpFinishedReceiving

    message_kind: str = None
    session_id: Union[str, FixpUuid] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.session_id):
            self.MissingRequiredField("session_id")
        if not isinstance(self.session_id, FixpUuid):
            self.session_id = FixpUuid(self.session_id)

        super().__post_init__(**kwargs)
        if self._is_empty(self.message_kind):
            self.MissingRequiredField("message_kind")
        self.message_kind = str(self.class_name)


@dataclass(repr=False)
class FixpApplied(FixpMessage):
    """
    An optional application message telling the party that sends an idempotent flow which of its operations took
    effect, where no business message already says so.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIXP["FixpApplied"]
    class_class_curie: ClassVar[str] = "fixp:FixpApplied"
    class_name: ClassVar[str] = "FixpApplied"
    class_model_uri: ClassVar[URIRef] = FIXP.FixpApplied

    message_kind: str = None
    from_seq_no: Union[int, FixpU64] = None
    message_count: Union[int, FixpU32] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.from_seq_no):
            self.MissingRequiredField("from_seq_no")
        if not isinstance(self.from_seq_no, FixpU64):
            self.from_seq_no = FixpU64(self.from_seq_no)

        if self._is_empty(self.message_count):
            self.MissingRequiredField("message_count")
        if not isinstance(self.message_count, FixpU32):
            self.message_count = FixpU32(self.message_count)

        super().__post_init__(**kwargs)
        if self._is_empty(self.message_kind):
            self.MissingRequiredField("message_kind")
        self.message_kind = str(self.class_name)


@dataclass(repr=False)
class FixpNotApplied(FixpMessage):
    """
    An application message telling the party that sends an idempotent flow about a gap: a run of operations that did
    not take effect. That party's application decides what to do.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIXP["FixpNotApplied"]
    class_class_curie: ClassVar[str] = "fixp:FixpNotApplied"
    class_name: ClassVar[str] = "FixpNotApplied"
    class_model_uri: ClassVar[URIRef] = FIXP.FixpNotApplied

    message_kind: str = None
    from_seq_no: Union[int, FixpU64] = None
    message_count: Union[int, FixpU32] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.from_seq_no):
            self.MissingRequiredField("from_seq_no")
        if not isinstance(self.from_seq_no, FixpU64):
            self.from_seq_no = FixpU64(self.from_seq_no)

        if self._is_empty(self.message_count):
            self.MissingRequiredField("message_count")
        if not isinstance(self.message_count, FixpU32):
            self.message_count = FixpU32(self.message_count)

        super().__post_init__(**kwargs)
        if self._is_empty(self.message_kind):
            self.MissingRequiredField("message_kind")
        self.message_kind = str(self.class_name)


@dataclass(repr=False)
class FixpMessageTemplate(FixpMessage):
    """
    Hands the peer a template or schema it needs to read messages in an encoding that templates drive. There is no
    fixed moment for sending it.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIXP["FixpMessageTemplate"]
    class_class_curie: ClassVar[str] = "fixp:FixpMessageTemplate"
    class_name: ClassVar[str] = "FixpMessageTemplate"
    class_model_uri: ClassVar[URIRef] = FIXP.FixpMessageTemplate

    message_kind: str = None
    sofh_encoding_type: Union[int, FixpU32] = None
    template: Union[str, FixpObject] = None
    effective_time: Optional[Union[int, FixpNanotime]] = None
    template_version: Optional[Union[str, FixpObject]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.sofh_encoding_type):
            self.MissingRequiredField("sofh_encoding_type")
        if not isinstance(self.sofh_encoding_type, FixpU32):
            self.sofh_encoding_type = FixpU32(self.sofh_encoding_type)

        if self._is_empty(self.template):
            self.MissingRequiredField("template")
        if not isinstance(self.template, FixpObject):
            self.template = FixpObject(self.template)

        if self.effective_time is not None and not isinstance(self.effective_time, FixpNanotime):
            self.effective_time = FixpNanotime(self.effective_time)

        if self.template_version is not None and not isinstance(self.template_version, FixpObject):
            self.template_version = FixpObject(self.template_version)

        super().__post_init__(**kwargs)
        if self._is_empty(self.message_kind):
            self.MissingRequiredField("message_kind")
        self.message_kind = str(self.class_name)


@dataclass(repr=False)
class FixpExchange(YAMLRoot):
    """
    The messages of one session in the order they were sent, as a test case, a worked example or a captured log.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIXP["FixpExchange"]
    class_class_curie: ClassVar[str] = "fixp:FixpExchange"
    class_name: ClassVar[str] = "FixpExchange"
    class_model_uri: ClassVar[URIRef] = FIXP.FixpExchange

    id: Union[str, FixpExchangeId] = None
    session_kind: Union[str, "FixpSessionKind"] = None
    exchange_steps: Union[Union[dict, "FixpExchangeStep"], list[Union[dict, "FixpExchangeStep"]]] = None
    description: Optional[str] = None
    multiplexed: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, FixpExchangeId):
            self.id = FixpExchangeId(self.id)

        if self._is_empty(self.session_kind):
            self.MissingRequiredField("session_kind")
        if not isinstance(self.session_kind, FixpSessionKind):
            self.session_kind = FixpSessionKind(self.session_kind)

        if self._is_empty(self.exchange_steps):
            self.MissingRequiredField("exchange_steps")
        self._normalize_inlined_as_list(slot_name="exchange_steps", slot_type=FixpExchangeStep, key_name="sent_by", keyed=False)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.multiplexed is not None and not isinstance(self.multiplexed, Bool):
            self.multiplexed = Bool(self.multiplexed)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class FixpExchangeStep(YAMLRoot):
    """
    One step: a FIXP message, or a run of application messages whose content FIXP does not define, and the side that
    sent it.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIXP["FixpExchangeStep"]
    class_class_curie: ClassVar[str] = "fixp:FixpExchangeStep"
    class_name: ClassVar[str] = "FixpExchangeStep"
    class_model_uri: ClassVar[URIRef] = FIXP.FixpExchangeStep

    sent_by: Union[str, "FixpParty"] = None
    fixp_message: Optional[Union[dict, FixpMessage]] = None
    application_message_count: Optional[Union[int, FixpU32]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.sent_by):
            self.MissingRequiredField("sent_by")
        if not isinstance(self.sent_by, FixpParty):
            self.sent_by = FixpParty(self.sent_by)

        if self.fixp_message is not None and not isinstance(self.fixp_message, FixpMessage):
            self.fixp_message = FixpMessage(**as_dict(self.fixp_message))

        if self.application_message_count is not None and not isinstance(self.application_message_count, FixpU32):
            self.application_message_count = FixpU32(self.application_message_count)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class FixpRulesOfEngagement(YAMLRoot):
    """
    What two counterparties agree on for one FIXP service, layer by layer, for the client and for the server.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIXP["FixpRulesOfEngagement"]
    class_class_curie: ClassVar[str] = "fixp:FixpRulesOfEngagement"
    class_name: ClassVar[str] = "FixpRulesOfEngagement"
    class_model_uri: ClassVar[URIRef] = FIXP.FixpRulesOfEngagement

    id: Union[str, FixpRulesOfEngagementId] = None
    client_stack: Union[dict, "FixpStackProfile"] = None
    server_stack: Union[dict, "FixpStackProfile"] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, FixpRulesOfEngagementId):
            self.id = FixpRulesOfEngagementId(self.id)

        if self._is_empty(self.client_stack):
            self.MissingRequiredField("client_stack")
        if not isinstance(self.client_stack, FixpStackProfile):
            self.client_stack = FixpStackProfile(**as_dict(self.client_stack))

        if self._is_empty(self.server_stack):
            self.MissingRequiredField("server_stack")
        if not isinstance(self.server_stack, FixpStackProfile):
            self.server_stack = FixpStackProfile(**as_dict(self.server_stack))

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class FixpStackProfile(YAMLRoot):
    """
    One side's choices at each layer of the stack: application, presentation, session, security and transport.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIXP["FixpStackProfile"]
    class_class_curie: ClassVar[str] = "fixp:FixpStackProfile"
    class_name: ClassVar[str] = "FixpStackProfile"
    class_model_uri: ClassVar[URIRef] = FIXP.FixpStackProfile

    application_recovery: Optional[Union[bool, Bool]] = None
    application_fix_version: Optional[str] = None
    service_pack: Optional[str] = None
    extension_packs: Optional[Union[str, list[str]]] = empty_list()
    message_encoding: Optional[str] = None
    encoding_version: Optional[str] = None
    message_schemas: Optional[Union[str, list[str]]] = empty_list()
    framing: Optional[str] = None
    supported_flow_types: Optional[Union[Union[str, "FixpFlowType"], list[Union[str, "FixpFlowType"]]]] = empty_list()
    tls_version: Optional[str] = None
    authentication_methods: Optional[Union[str, list[str]]] = empty_list()
    cipher_suites: Optional[Union[str, list[str]]] = empty_list()
    transports: Optional[Union[str, list[str]]] = empty_list()
    network_protocols: Optional[Union[str, list[str]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.application_recovery is not None and not isinstance(self.application_recovery, Bool):
            self.application_recovery = Bool(self.application_recovery)

        if self.application_fix_version is not None and not isinstance(self.application_fix_version, str):
            self.application_fix_version = str(self.application_fix_version)

        if self.service_pack is not None and not isinstance(self.service_pack, str):
            self.service_pack = str(self.service_pack)

        if not isinstance(self.extension_packs, list):
            self.extension_packs = [self.extension_packs] if self.extension_packs is not None else []
        self.extension_packs = [v if isinstance(v, str) else str(v) for v in self.extension_packs]

        if self.message_encoding is not None and not isinstance(self.message_encoding, str):
            self.message_encoding = str(self.message_encoding)

        if self.encoding_version is not None and not isinstance(self.encoding_version, str):
            self.encoding_version = str(self.encoding_version)

        if not isinstance(self.message_schemas, list):
            self.message_schemas = [self.message_schemas] if self.message_schemas is not None else []
        self.message_schemas = [v if isinstance(v, str) else str(v) for v in self.message_schemas]

        if self.framing is not None and not isinstance(self.framing, str):
            self.framing = str(self.framing)

        if not isinstance(self.supported_flow_types, list):
            self.supported_flow_types = [self.supported_flow_types] if self.supported_flow_types is not None else []
        self.supported_flow_types = [v if isinstance(v, FixpFlowType) else FixpFlowType(v) for v in self.supported_flow_types]

        if self.tls_version is not None and not isinstance(self.tls_version, str):
            self.tls_version = str(self.tls_version)

        if not isinstance(self.authentication_methods, list):
            self.authentication_methods = [self.authentication_methods] if self.authentication_methods is not None else []
        self.authentication_methods = [v if isinstance(v, str) else str(v) for v in self.authentication_methods]

        if not isinstance(self.cipher_suites, list):
            self.cipher_suites = [self.cipher_suites] if self.cipher_suites is not None else []
        self.cipher_suites = [v if isinstance(v, str) else str(v) for v in self.cipher_suites]

        if not isinstance(self.transports, list):
            self.transports = [self.transports] if self.transports is not None else []
        self.transports = [v if isinstance(v, str) else str(v) for v in self.transports]

        if not isinstance(self.network_protocols, list):
            self.network_protocols = [self.network_protocols] if self.network_protocols is not None else []
        self.network_protocols = [v if isinstance(v, str) else str(v) for v in self.network_protocols]

        super().__post_init__(**kwargs)


# Enumerations
class FixpFlowType(EnumDefinitionImpl):
    """
    How surely a flow is delivered. A flow is what one side of a session sends the other, leaving out session messages.
    """
    Recoverable = PermissibleValue(
        text="Recoverable",
        description="Every message arrives once and in order; the receiver asks for any gap to be sent again.")
    Idempotent = PermissibleValue(
        text="Idempotent",
        description="""No message takes effect twice; the sender hears of a gap and its application decides what to resend.""")
    Unsequenced = PermissibleValue(
        text="Unsequenced",
        description="Messages carry no sequence number, and none is ever resent.")

    _defn = EnumDefinition(
        name="FixpFlowType",
        description="""How surely a flow is delivered. A flow is what one side of a session sends the other, leaving out session messages.""",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "None",
            PermissibleValue(
                text="None",
                description="This side sends no application messages at all."))

class FixpMulticastFlowType(EnumDefinitionImpl):
    """
    The delivery guarantee a multicast topic announces for its flow.
    """
    Recoverable = PermissibleValue(
        text="Recoverable",
        description="Sequenced; a listener gets a lost message back over a separate unicast session.")
    Idempotent = PermissibleValue(
        text="Idempotent",
        description="Sequenced, so a listener can see a loss, but nothing lost comes back.")

    _defn = EnumDefinition(
        name="FixpMulticastFlowType",
        description="The delivery guarantee a multicast topic announces for its flow.",
    )

class FixpNegotiationRejectCode(EnumDefinitionImpl):
    """
    Why a server refused to create a session.
    """
    Credentials = PermissibleValue(
        text="Credentials",
        description="The server could not identify the client, or would not let it in.")
    FlowTypeNotSupported = PermissibleValue(
        text="FlowTypeNotSupported",
        description="The server does not offer the flow type the client asked to send.")
    DuplicateId = PermissibleValue(
        text="DuplicateId",
        description="The client chose a session identifier that is not new.")
    Unspecified = PermissibleValue(
        text="Unspecified",
        description="Some reason the other values do not name.")

    _defn = EnumDefinition(
        name="FixpNegotiationRejectCode",
        description="Why a server refused to create a session.",
    )

class FixpEstablishmentRejectCode(EnumDefinitionImpl):
    """
    Why a server would not bind the session to this transport.
    """
    Unnegotiated = PermissibleValue(
        text="Unnegotiated",
        description="The session was never negotiated, or it has been finalized and needs a new negotiation.")
    AlreadyEstablished = PermissibleValue(
        text="AlreadyEstablished",
        description="The server had already acknowledged a binding, so this request repeats it.")
    SessionBlocked = PermissibleValue(
        text="SessionBlocked",
        description="The client may not use this session.")
    KeepaliveInterval = PermissibleValue(
        text="KeepaliveInterval",
        description="The client's keep-alive interval is outside what the server accepts.")
    Credentials = PermissibleValue(
        text="Credentials",
        description="The server could not identify the client, or would not let it in.")
    Unspecified = PermissibleValue(
        text="Unspecified",
        description="Some reason the other values do not name.")

    _defn = EnumDefinition(
        name="FixpEstablishmentRejectCode",
        description="Why a server would not bind the session to this transport.",
    )

class FixpRetransmitRejectCode(EnumDefinitionImpl):
    """
    Why a party will not resend the messages its peer asked for.
    """
    OutOfRange = PermissibleValue(
        text="OutOfRange",
        description="The range asked for runs past the sequence numbers sent so far.")
    InvalidSession = PermissibleValue(
        text="InvalidSession",
        description="The session is unknown, or the one asking may not read it.")
    RequestLimitExceeded = PermissibleValue(
        text="RequestLimitExceeded",
        description="The request asks for more messages than the sender resends at once.")

    _defn = EnumDefinition(
        name="FixpRetransmitRejectCode",
        description="Why a party will not resend the messages its peer asked for.",
    )

class FixpTerminationCode(EnumDefinitionImpl):
    """
    Why a party releases a session from its transport.
    """
    Finished = PermissibleValue(
        text="Finished",
        description="An ordinary release, with no error.")
    UnspecifiedError = PermissibleValue(
        text="UnspecifiedError",
        description="An error that the other values do not name.")
    ReRequestOutOfBounds = PermissibleValue(
        text="ReRequestOutOfBounds",
        description="The peer asked again for messages outside the range sent.")
    ReRequestInProgress = PermissibleValue(
        text="ReRequestInProgress",
        description="The peer asked again for messages while its earlier request was unanswered.")

    _defn = EnumDefinition(
        name="FixpTerminationCode",
        description="Why a party releases a session from its transport.",
    )

class FixpSessionKind(EnumDefinitionImpl):
    """
    The two forms of FIXP session.
    """
    point_to_point = PermissibleValue(
        text="point_to_point",
        description="""A client and a server over a transport that carries messages both ways, with one flow each way.""")
    multicast = PermissibleValue(
        text="multicast",
        description="One publisher, one flow and many listeners, on a transport that only carries messages outward.")

    _defn = EnumDefinition(
        name="FixpSessionKind",
        description="The two forms of FIXP session.",
    )

class FixpParty(EnumDefinitionImpl):
    """
    The side that sends a step.
    """
    client = PermissibleValue(
        text="client",
        description="The party that opens a session with a server.")
    server = PermissibleValue(
        text="server",
        description="The party that accepts the client's session.")
    publisher = PermissibleValue(
        text="publisher",
        description="The only party that sends in a multicast.")

    _defn = EnumDefinition(
        name="FixpParty",
        description="The side that sends a step.",
    )

# Slots
class slots:
    pass

slots.id = Slot(uri=FIXP.id, name="id", curie=FIXP.curie('id'),
                   model_uri=FIXP.id, domain=None, range=URIRef)

slots.description = Slot(uri=SCHEMA.description, name="description", curie=SCHEMA.curie('description'),
                   model_uri=FIXP.description, domain=None, range=Optional[str])

slots.message_kind = Slot(uri=FIXP.message_kind, name="message_kind", curie=FIXP.curie('message_kind'),
                   model_uri=FIXP.message_kind, domain=None, range=str)

slots.session_id = Slot(uri=FIXP.session_id, name="session_id", curie=FIXP.curie('session_id'),
                   model_uri=FIXP.session_id, domain=None, range=Optional[Union[str, FixpUuid]])

slots.request_time = Slot(uri=FIXP.request_time, name="request_time", curie=FIXP.curie('request_time'),
                   model_uri=FIXP.request_time, domain=None, range=Optional[Union[int, FixpNanotime]])

slots.client_flow = Slot(uri=FIXP.client_flow, name="client_flow", curie=FIXP.curie('client_flow'),
                   model_uri=FIXP.client_flow, domain=None, range=Optional[Union[str, "FixpFlowType"]])

slots.credentials = Slot(uri=FIXP.credentials, name="credentials", curie=FIXP.curie('credentials'),
                   model_uri=FIXP.credentials, domain=None, range=Optional[Union[str, FixpObject]])

slots.request_timestamp = Slot(uri=FIXP.request_timestamp, name="request_timestamp", curie=FIXP.curie('request_timestamp'),
                   model_uri=FIXP.request_timestamp, domain=None, range=Optional[Union[int, FixpNanotime]])

slots.server_flow = Slot(uri=FIXP.server_flow, name="server_flow", curie=FIXP.curie('server_flow'),
                   model_uri=FIXP.server_flow, domain=None, range=Optional[Union[str, "FixpFlowType"]])

slots.negotiation_reject_code = Slot(uri=FIXP.negotiation_reject_code, name="negotiation_reject_code", curie=FIXP.curie('negotiation_reject_code'),
                   model_uri=FIXP.negotiation_reject_code, domain=None, range=Optional[Union[str, "FixpNegotiationRejectCode"]])

slots.reason_text = Slot(uri=FIXP.reason_text, name="reason_text", curie=FIXP.curie('reason_text'),
                   model_uri=FIXP.reason_text, domain=None, range=Optional[Union[str, FixpString]])

slots.keepalive_interval = Slot(uri=FIXP.keepalive_interval, name="keepalive_interval", curie=FIXP.curie('keepalive_interval'),
                   model_uri=FIXP.keepalive_interval, domain=None, range=Optional[Union[int, FixpDeltaMillisecs]])

slots.topic_classification = Slot(uri=FIXP.topic_classification, name="topic_classification", curie=FIXP.curie('topic_classification'),
                   model_uri=FIXP.topic_classification, domain=None, range=Optional[Union[str, FixpObject]])

slots.next_seq_no = Slot(uri=FIXP.next_seq_no, name="next_seq_no", curie=FIXP.curie('next_seq_no'),
                   model_uri=FIXP.next_seq_no, domain=None, range=Optional[Union[int, FixpU64]])

slots.establishment_reject_code = Slot(uri=FIXP.establishment_reject_code, name="establishment_reject_code", curie=FIXP.curie('establishment_reject_code'),
                   model_uri=FIXP.establishment_reject_code, domain=None, range=Optional[Union[str, "FixpEstablishmentRejectCode"]])

slots.from_seq_no = Slot(uri=FIXP.from_seq_no, name="from_seq_no", curie=FIXP.curie('from_seq_no'),
                   model_uri=FIXP.from_seq_no, domain=None, range=Optional[Union[int, FixpU64]])

slots.message_count = Slot(uri=FIXP.message_count, name="message_count", curie=FIXP.curie('message_count'),
                   model_uri=FIXP.message_count, domain=None, range=Optional[Union[int, FixpU32]])

slots.retransmit_reject_code = Slot(uri=FIXP.retransmit_reject_code, name="retransmit_reject_code", curie=FIXP.curie('retransmit_reject_code'),
                   model_uri=FIXP.retransmit_reject_code, domain=None, range=Optional[Union[str, "FixpRetransmitRejectCode"]])

slots.termination_code = Slot(uri=FIXP.termination_code, name="termination_code", curie=FIXP.curie('termination_code'),
                   model_uri=FIXP.termination_code, domain=None, range=Optional[Union[str, "FixpTerminationCode"]])

slots.last_seq_no = Slot(uri=FIXP.last_seq_no, name="last_seq_no", curie=FIXP.curie('last_seq_no'),
                   model_uri=FIXP.last_seq_no, domain=None, range=Optional[Union[int, FixpU64]])

slots.flow = Slot(uri=FIXP.flow, name="flow", curie=FIXP.curie('flow'),
                   model_uri=FIXP.flow, domain=None, range=Optional[Union[str, "FixpMulticastFlowType"]])

slots.sofh_encoding_type = Slot(uri=FIXP.sofh_encoding_type, name="sofh_encoding_type", curie=FIXP.curie('sofh_encoding_type'),
                   model_uri=FIXP.sofh_encoding_type, domain=None, range=Optional[Union[int, FixpU32]])

slots.effective_time = Slot(uri=FIXP.effective_time, name="effective_time", curie=FIXP.curie('effective_time'),
                   model_uri=FIXP.effective_time, domain=None, range=Optional[Union[int, FixpNanotime]])

slots.template_version = Slot(uri=FIXP.template_version, name="template_version", curie=FIXP.curie('template_version'),
                   model_uri=FIXP.template_version, domain=None, range=Optional[Union[str, FixpObject]])

slots.template = Slot(uri=FIXP.template, name="template", curie=FIXP.curie('template'),
                   model_uri=FIXP.template, domain=None, range=Optional[Union[str, FixpObject]])

slots.fixpExchange__session_kind = Slot(uri=FIXP.session_kind, name="fixpExchange__session_kind", curie=FIXP.curie('session_kind'),
                   model_uri=FIXP.fixpExchange__session_kind, domain=None, range=Union[str, "FixpSessionKind"])

slots.fixpExchange__multiplexed = Slot(uri=FIXP.multiplexed, name="fixpExchange__multiplexed", curie=FIXP.curie('multiplexed'),
                   model_uri=FIXP.fixpExchange__multiplexed, domain=None, range=Optional[Union[bool, Bool]])

slots.fixpExchange__exchange_steps = Slot(uri=FIXP.exchange_steps, name="fixpExchange__exchange_steps", curie=FIXP.curie('exchange_steps'),
                   model_uri=FIXP.fixpExchange__exchange_steps, domain=None, range=Union[Union[dict, FixpExchangeStep], list[Union[dict, FixpExchangeStep]]])

slots.fixpExchangeStep__sent_by = Slot(uri=FIXP.sent_by, name="fixpExchangeStep__sent_by", curie=FIXP.curie('sent_by'),
                   model_uri=FIXP.fixpExchangeStep__sent_by, domain=None, range=Union[str, "FixpParty"])

slots.fixpExchangeStep__fixp_message = Slot(uri=FIXP.fixp_message, name="fixpExchangeStep__fixp_message", curie=FIXP.curie('fixp_message'),
                   model_uri=FIXP.fixpExchangeStep__fixp_message, domain=None, range=Optional[Union[dict, FixpMessage]])

slots.fixpExchangeStep__application_message_count = Slot(uri=FIXP.application_message_count, name="fixpExchangeStep__application_message_count", curie=FIXP.curie('application_message_count'),
                   model_uri=FIXP.fixpExchangeStep__application_message_count, domain=None, range=Optional[Union[int, FixpU32]])

slots.fixpRulesOfEngagement__client_stack = Slot(uri=FIXP.client_stack, name="fixpRulesOfEngagement__client_stack", curie=FIXP.curie('client_stack'),
                   model_uri=FIXP.fixpRulesOfEngagement__client_stack, domain=None, range=Union[dict, FixpStackProfile])

slots.fixpRulesOfEngagement__server_stack = Slot(uri=FIXP.server_stack, name="fixpRulesOfEngagement__server_stack", curie=FIXP.curie('server_stack'),
                   model_uri=FIXP.fixpRulesOfEngagement__server_stack, domain=None, range=Union[dict, FixpStackProfile])

slots.fixpStackProfile__application_recovery = Slot(uri=FIXP.application_recovery, name="fixpStackProfile__application_recovery", curie=FIXP.curie('application_recovery'),
                   model_uri=FIXP.fixpStackProfile__application_recovery, domain=None, range=Optional[Union[bool, Bool]])

slots.fixpStackProfile__application_fix_version = Slot(uri=FIXP.application_fix_version, name="fixpStackProfile__application_fix_version", curie=FIXP.curie('application_fix_version'),
                   model_uri=FIXP.fixpStackProfile__application_fix_version, domain=None, range=Optional[str])

slots.fixpStackProfile__service_pack = Slot(uri=FIXP.service_pack, name="fixpStackProfile__service_pack", curie=FIXP.curie('service_pack'),
                   model_uri=FIXP.fixpStackProfile__service_pack, domain=None, range=Optional[str])

slots.fixpStackProfile__extension_packs = Slot(uri=FIXP.extension_packs, name="fixpStackProfile__extension_packs", curie=FIXP.curie('extension_packs'),
                   model_uri=FIXP.fixpStackProfile__extension_packs, domain=None, range=Optional[Union[str, list[str]]])

slots.fixpStackProfile__message_encoding = Slot(uri=FIXP.message_encoding, name="fixpStackProfile__message_encoding", curie=FIXP.curie('message_encoding'),
                   model_uri=FIXP.fixpStackProfile__message_encoding, domain=None, range=Optional[str])

slots.fixpStackProfile__encoding_version = Slot(uri=FIXP.encoding_version, name="fixpStackProfile__encoding_version", curie=FIXP.curie('encoding_version'),
                   model_uri=FIXP.fixpStackProfile__encoding_version, domain=None, range=Optional[str])

slots.fixpStackProfile__message_schemas = Slot(uri=FIXP.message_schemas, name="fixpStackProfile__message_schemas", curie=FIXP.curie('message_schemas'),
                   model_uri=FIXP.fixpStackProfile__message_schemas, domain=None, range=Optional[Union[str, list[str]]])

slots.fixpStackProfile__framing = Slot(uri=FIXP.framing, name="fixpStackProfile__framing", curie=FIXP.curie('framing'),
                   model_uri=FIXP.fixpStackProfile__framing, domain=None, range=Optional[str])

slots.fixpStackProfile__supported_flow_types = Slot(uri=FIXP.supported_flow_types, name="fixpStackProfile__supported_flow_types", curie=FIXP.curie('supported_flow_types'),
                   model_uri=FIXP.fixpStackProfile__supported_flow_types, domain=None, range=Optional[Union[Union[str, "FixpFlowType"], list[Union[str, "FixpFlowType"]]]])

slots.fixpStackProfile__tls_version = Slot(uri=FIXP.tls_version, name="fixpStackProfile__tls_version", curie=FIXP.curie('tls_version'),
                   model_uri=FIXP.fixpStackProfile__tls_version, domain=None, range=Optional[str])

slots.fixpStackProfile__authentication_methods = Slot(uri=FIXP.authentication_methods, name="fixpStackProfile__authentication_methods", curie=FIXP.curie('authentication_methods'),
                   model_uri=FIXP.fixpStackProfile__authentication_methods, domain=None, range=Optional[Union[str, list[str]]])

slots.fixpStackProfile__cipher_suites = Slot(uri=FIXP.cipher_suites, name="fixpStackProfile__cipher_suites", curie=FIXP.curie('cipher_suites'),
                   model_uri=FIXP.fixpStackProfile__cipher_suites, domain=None, range=Optional[Union[str, list[str]]])

slots.fixpStackProfile__transports = Slot(uri=FIXP.transports, name="fixpStackProfile__transports", curie=FIXP.curie('transports'),
                   model_uri=FIXP.fixpStackProfile__transports, domain=None, range=Optional[Union[str, list[str]]])

slots.fixpStackProfile__network_protocols = Slot(uri=FIXP.network_protocols, name="fixpStackProfile__network_protocols", curie=FIXP.curie('network_protocols'),
                   model_uri=FIXP.fixpStackProfile__network_protocols, domain=None, range=Optional[Union[str, list[str]]])

slots.FixpNegotiate_session_id = Slot(uri=FIXP.session_id, name="FixpNegotiate_session_id", curie=FIXP.curie('session_id'),
                   model_uri=FIXP.FixpNegotiate_session_id, domain=FixpNegotiate, range=Union[str, FixpUuid])

slots.FixpNegotiate_request_time = Slot(uri=FIXP.request_time, name="FixpNegotiate_request_time", curie=FIXP.curie('request_time'),
                   model_uri=FIXP.FixpNegotiate_request_time, domain=FixpNegotiate, range=Union[int, FixpNanotime])

slots.FixpNegotiate_client_flow = Slot(uri=FIXP.client_flow, name="FixpNegotiate_client_flow", curie=FIXP.curie('client_flow'),
                   model_uri=FIXP.FixpNegotiate_client_flow, domain=FixpNegotiate, range=Union[str, "FixpFlowType"])

slots.FixpNegotiate_credentials = Slot(uri=FIXP.credentials, name="FixpNegotiate_credentials", curie=FIXP.curie('credentials'),
                   model_uri=FIXP.FixpNegotiate_credentials, domain=FixpNegotiate, range=Optional[Union[str, FixpObject]])

slots.FixpNegotiationResponse_session_id = Slot(uri=FIXP.session_id, name="FixpNegotiationResponse_session_id", curie=FIXP.curie('session_id'),
                   model_uri=FIXP.FixpNegotiationResponse_session_id, domain=FixpNegotiationResponse, range=Union[str, FixpUuid])

slots.FixpNegotiationResponse_request_timestamp = Slot(uri=FIXP.request_timestamp, name="FixpNegotiationResponse_request_timestamp", curie=FIXP.curie('request_timestamp'),
                   model_uri=FIXP.FixpNegotiationResponse_request_timestamp, domain=FixpNegotiationResponse, range=Union[int, FixpNanotime])

slots.FixpNegotiationResponse_server_flow = Slot(uri=FIXP.server_flow, name="FixpNegotiationResponse_server_flow", curie=FIXP.curie('server_flow'),
                   model_uri=FIXP.FixpNegotiationResponse_server_flow, domain=FixpNegotiationResponse, range=Union[str, "FixpFlowType"])

slots.FixpNegotiationResponse_credentials = Slot(uri=FIXP.credentials, name="FixpNegotiationResponse_credentials", curie=FIXP.curie('credentials'),
                   model_uri=FIXP.FixpNegotiationResponse_credentials, domain=FixpNegotiationResponse, range=Optional[Union[str, FixpObject]])

slots.FixpNegotiationReject_session_id = Slot(uri=FIXP.session_id, name="FixpNegotiationReject_session_id", curie=FIXP.curie('session_id'),
                   model_uri=FIXP.FixpNegotiationReject_session_id, domain=FixpNegotiationReject, range=Union[str, FixpUuid])

slots.FixpNegotiationReject_request_timestamp = Slot(uri=FIXP.request_timestamp, name="FixpNegotiationReject_request_timestamp", curie=FIXP.curie('request_timestamp'),
                   model_uri=FIXP.FixpNegotiationReject_request_timestamp, domain=FixpNegotiationReject, range=Union[int, FixpNanotime])

slots.FixpNegotiationReject_negotiation_reject_code = Slot(uri=FIXP.negotiation_reject_code, name="FixpNegotiationReject_negotiation_reject_code", curie=FIXP.curie('negotiation_reject_code'),
                   model_uri=FIXP.FixpNegotiationReject_negotiation_reject_code, domain=FixpNegotiationReject, range=Union[str, "FixpNegotiationRejectCode"])

slots.FixpTopic_session_id = Slot(uri=FIXP.session_id, name="FixpTopic_session_id", curie=FIXP.curie('session_id'),
                   model_uri=FIXP.FixpTopic_session_id, domain=FixpTopic, range=Union[str, FixpUuid])

slots.FixpTopic_flow = Slot(uri=FIXP.flow, name="FixpTopic_flow", curie=FIXP.curie('flow'),
                   model_uri=FIXP.FixpTopic_flow, domain=FixpTopic, range=Union[str, "FixpMulticastFlowType"])

slots.FixpTopic_keepalive_interval = Slot(uri=FIXP.keepalive_interval, name="FixpTopic_keepalive_interval", curie=FIXP.curie('keepalive_interval'),
                   model_uri=FIXP.FixpTopic_keepalive_interval, domain=FixpTopic, range=Optional[Union[int, FixpDeltaMillisecs]])

slots.FixpTopic_topic_classification = Slot(uri=FIXP.topic_classification, name="FixpTopic_topic_classification", curie=FIXP.curie('topic_classification'),
                   model_uri=FIXP.FixpTopic_topic_classification, domain=FixpTopic, range=Union[str, FixpObject])

slots.FixpEstablish_session_id = Slot(uri=FIXP.session_id, name="FixpEstablish_session_id", curie=FIXP.curie('session_id'),
                   model_uri=FIXP.FixpEstablish_session_id, domain=FixpEstablish, range=Union[str, FixpUuid])

slots.FixpEstablish_request_time = Slot(uri=FIXP.request_time, name="FixpEstablish_request_time", curie=FIXP.curie('request_time'),
                   model_uri=FIXP.FixpEstablish_request_time, domain=FixpEstablish, range=Union[int, FixpNanotime])

slots.FixpEstablish_keepalive_interval = Slot(uri=FIXP.keepalive_interval, name="FixpEstablish_keepalive_interval", curie=FIXP.curie('keepalive_interval'),
                   model_uri=FIXP.FixpEstablish_keepalive_interval, domain=FixpEstablish, range=Union[int, FixpDeltaMillisecs])

slots.FixpEstablish_next_seq_no = Slot(uri=FIXP.next_seq_no, name="FixpEstablish_next_seq_no", curie=FIXP.curie('next_seq_no'),
                   model_uri=FIXP.FixpEstablish_next_seq_no, domain=FixpEstablish, range=Optional[Union[int, FixpU64]])

slots.FixpEstablish_credentials = Slot(uri=FIXP.credentials, name="FixpEstablish_credentials", curie=FIXP.curie('credentials'),
                   model_uri=FIXP.FixpEstablish_credentials, domain=FixpEstablish, range=Optional[Union[str, FixpObject]])

slots.FixpEstablishmentAck_session_id = Slot(uri=FIXP.session_id, name="FixpEstablishmentAck_session_id", curie=FIXP.curie('session_id'),
                   model_uri=FIXP.FixpEstablishmentAck_session_id, domain=FixpEstablishmentAck, range=Union[str, FixpUuid])

slots.FixpEstablishmentAck_request_timestamp = Slot(uri=FIXP.request_timestamp, name="FixpEstablishmentAck_request_timestamp", curie=FIXP.curie('request_timestamp'),
                   model_uri=FIXP.FixpEstablishmentAck_request_timestamp, domain=FixpEstablishmentAck, range=Union[int, FixpNanotime])

slots.FixpEstablishmentAck_keepalive_interval = Slot(uri=FIXP.keepalive_interval, name="FixpEstablishmentAck_keepalive_interval", curie=FIXP.curie('keepalive_interval'),
                   model_uri=FIXP.FixpEstablishmentAck_keepalive_interval, domain=FixpEstablishmentAck, range=Union[int, FixpDeltaMillisecs])

slots.FixpEstablishmentAck_next_seq_no = Slot(uri=FIXP.next_seq_no, name="FixpEstablishmentAck_next_seq_no", curie=FIXP.curie('next_seq_no'),
                   model_uri=FIXP.FixpEstablishmentAck_next_seq_no, domain=FixpEstablishmentAck, range=Optional[Union[int, FixpU64]])

slots.FixpEstablishmentReject_session_id = Slot(uri=FIXP.session_id, name="FixpEstablishmentReject_session_id", curie=FIXP.curie('session_id'),
                   model_uri=FIXP.FixpEstablishmentReject_session_id, domain=FixpEstablishmentReject, range=Union[str, FixpUuid])

slots.FixpEstablishmentReject_request_timestamp = Slot(uri=FIXP.request_timestamp, name="FixpEstablishmentReject_request_timestamp", curie=FIXP.curie('request_timestamp'),
                   model_uri=FIXP.FixpEstablishmentReject_request_timestamp, domain=FixpEstablishmentReject, range=Union[int, FixpNanotime])

slots.FixpEstablishmentReject_establishment_reject_code = Slot(uri=FIXP.establishment_reject_code, name="FixpEstablishmentReject_establishment_reject_code", curie=FIXP.curie('establishment_reject_code'),
                   model_uri=FIXP.FixpEstablishmentReject_establishment_reject_code, domain=FixpEstablishmentReject, range=Union[str, "FixpEstablishmentRejectCode"])

slots.FixpSequence_next_seq_no = Slot(uri=FIXP.next_seq_no, name="FixpSequence_next_seq_no", curie=FIXP.curie('next_seq_no'),
                   model_uri=FIXP.FixpSequence_next_seq_no, domain=FixpSequence, range=Union[int, FixpU64])

slots.FixpContext_session_id = Slot(uri=FIXP.session_id, name="FixpContext_session_id", curie=FIXP.curie('session_id'),
                   model_uri=FIXP.FixpContext_session_id, domain=FixpContext, range=Union[str, FixpUuid])

slots.FixpContext_next_seq_no = Slot(uri=FIXP.next_seq_no, name="FixpContext_next_seq_no", curie=FIXP.curie('next_seq_no'),
                   model_uri=FIXP.FixpContext_next_seq_no, domain=FixpContext, range=Optional[Union[int, FixpU64]])

slots.FixpRetransmitRequest_session_id = Slot(uri=FIXP.session_id, name="FixpRetransmitRequest_session_id", curie=FIXP.curie('session_id'),
                   model_uri=FIXP.FixpRetransmitRequest_session_id, domain=FixpRetransmitRequest, range=Union[str, FixpUuid])

slots.FixpRetransmitRequest_request_time = Slot(uri=FIXP.request_time, name="FixpRetransmitRequest_request_time", curie=FIXP.curie('request_time'),
                   model_uri=FIXP.FixpRetransmitRequest_request_time, domain=FixpRetransmitRequest, range=Union[int, FixpNanotime])

slots.FixpRetransmitRequest_from_seq_no = Slot(uri=FIXP.from_seq_no, name="FixpRetransmitRequest_from_seq_no", curie=FIXP.curie('from_seq_no'),
                   model_uri=FIXP.FixpRetransmitRequest_from_seq_no, domain=FixpRetransmitRequest, range=Union[int, FixpU64])

slots.FixpRetransmitRequest_message_count = Slot(uri=FIXP.message_count, name="FixpRetransmitRequest_message_count", curie=FIXP.curie('message_count'),
                   model_uri=FIXP.FixpRetransmitRequest_message_count, domain=FixpRetransmitRequest, range=Union[int, FixpU32])

slots.FixpRetransmission_session_id = Slot(uri=FIXP.session_id, name="FixpRetransmission_session_id", curie=FIXP.curie('session_id'),
                   model_uri=FIXP.FixpRetransmission_session_id, domain=FixpRetransmission, range=Union[str, FixpUuid])

slots.FixpRetransmission_request_timestamp = Slot(uri=FIXP.request_timestamp, name="FixpRetransmission_request_timestamp", curie=FIXP.curie('request_timestamp'),
                   model_uri=FIXP.FixpRetransmission_request_timestamp, domain=FixpRetransmission, range=Union[int, FixpNanotime])

slots.FixpRetransmission_next_seq_no = Slot(uri=FIXP.next_seq_no, name="FixpRetransmission_next_seq_no", curie=FIXP.curie('next_seq_no'),
                   model_uri=FIXP.FixpRetransmission_next_seq_no, domain=FixpRetransmission, range=Union[int, FixpU64])

slots.FixpRetransmission_message_count = Slot(uri=FIXP.message_count, name="FixpRetransmission_message_count", curie=FIXP.curie('message_count'),
                   model_uri=FIXP.FixpRetransmission_message_count, domain=FixpRetransmission, range=Union[int, FixpU32])

slots.FixpRetransmitReject_session_id = Slot(uri=FIXP.session_id, name="FixpRetransmitReject_session_id", curie=FIXP.curie('session_id'),
                   model_uri=FIXP.FixpRetransmitReject_session_id, domain=FixpRetransmitReject, range=Union[str, FixpUuid])

slots.FixpRetransmitReject_request_timestamp = Slot(uri=FIXP.request_timestamp, name="FixpRetransmitReject_request_timestamp", curie=FIXP.curie('request_timestamp'),
                   model_uri=FIXP.FixpRetransmitReject_request_timestamp, domain=FixpRetransmitReject, range=Union[int, FixpNanotime])

slots.FixpRetransmitReject_retransmit_reject_code = Slot(uri=FIXP.retransmit_reject_code, name="FixpRetransmitReject_retransmit_reject_code", curie=FIXP.curie('retransmit_reject_code'),
                   model_uri=FIXP.FixpRetransmitReject_retransmit_reject_code, domain=FixpRetransmitReject, range=Union[str, "FixpRetransmitRejectCode"])

slots.FixpTerminate_session_id = Slot(uri=FIXP.session_id, name="FixpTerminate_session_id", curie=FIXP.curie('session_id'),
                   model_uri=FIXP.FixpTerminate_session_id, domain=FixpTerminate, range=Union[str, FixpUuid])

slots.FixpTerminate_termination_code = Slot(uri=FIXP.termination_code, name="FixpTerminate_termination_code", curie=FIXP.curie('termination_code'),
                   model_uri=FIXP.FixpTerminate_termination_code, domain=FixpTerminate, range=Union[str, "FixpTerminationCode"])

slots.FixpFinishedSending_session_id = Slot(uri=FIXP.session_id, name="FixpFinishedSending_session_id", curie=FIXP.curie('session_id'),
                   model_uri=FIXP.FixpFinishedSending_session_id, domain=FixpFinishedSending, range=Union[str, FixpUuid])

slots.FixpFinishedSending_last_seq_no = Slot(uri=FIXP.last_seq_no, name="FixpFinishedSending_last_seq_no", curie=FIXP.curie('last_seq_no'),
                   model_uri=FIXP.FixpFinishedSending_last_seq_no, domain=FixpFinishedSending, range=Optional[Union[int, FixpU64]])

slots.FixpFinishedReceiving_session_id = Slot(uri=FIXP.session_id, name="FixpFinishedReceiving_session_id", curie=FIXP.curie('session_id'),
                   model_uri=FIXP.FixpFinishedReceiving_session_id, domain=FixpFinishedReceiving, range=Union[str, FixpUuid])

slots.FixpApplied_from_seq_no = Slot(uri=FIXP.from_seq_no, name="FixpApplied_from_seq_no", curie=FIXP.curie('from_seq_no'),
                   model_uri=FIXP.FixpApplied_from_seq_no, domain=FixpApplied, range=Union[int, FixpU64])

slots.FixpApplied_message_count = Slot(uri=FIXP.message_count, name="FixpApplied_message_count", curie=FIXP.curie('message_count'),
                   model_uri=FIXP.FixpApplied_message_count, domain=FixpApplied, range=Union[int, FixpU32])

slots.FixpNotApplied_from_seq_no = Slot(uri=FIXP.from_seq_no, name="FixpNotApplied_from_seq_no", curie=FIXP.curie('from_seq_no'),
                   model_uri=FIXP.FixpNotApplied_from_seq_no, domain=FixpNotApplied, range=Union[int, FixpU64])

slots.FixpNotApplied_message_count = Slot(uri=FIXP.message_count, name="FixpNotApplied_message_count", curie=FIXP.curie('message_count'),
                   model_uri=FIXP.FixpNotApplied_message_count, domain=FixpNotApplied, range=Union[int, FixpU32])

slots.FixpMessageTemplate_sofh_encoding_type = Slot(uri=FIXP.sofh_encoding_type, name="FixpMessageTemplate_sofh_encoding_type", curie=FIXP.curie('sofh_encoding_type'),
                   model_uri=FIXP.FixpMessageTemplate_sofh_encoding_type, domain=FixpMessageTemplate, range=Union[int, FixpU32])

slots.FixpMessageTemplate_template = Slot(uri=FIXP.template, name="FixpMessageTemplate_template", curie=FIXP.curie('template'),
                   model_uri=FIXP.FixpMessageTemplate_template, domain=FixpMessageTemplate, range=Union[str, FixpObject])
