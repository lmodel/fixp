export type FixpExchangeId = string;
export type FixpRulesOfEngagementId = string;
/**
* How surely a flow is delivered. A flow is what one side of a session sends the other, leaving out session messages.
*/
export enum FixpFlowType {
    
    /** Every message arrives once and in order; the receiver asks for any gap to be sent again. */
    Recoverable = "Recoverable",
    /** No message takes effect twice; the sender hears of a gap and its application decides what to resend. */
    Idempotent = "Idempotent",
    /** Messages carry no sequence number, and none is ever resent. */
    Unsequenced = "Unsequenced",
    /** This side sends no application messages at all. */
    None = "None",
};
/**
* The delivery guarantee a multicast topic announces for its flow.
*/
export enum FixpMulticastFlowType {
    
    /** Sequenced; a listener gets a lost message back over a separate unicast session. */
    Recoverable = "Recoverable",
    /** Sequenced, so a listener can see a loss, but nothing lost comes back. */
    Idempotent = "Idempotent",
};
/**
* Why a server refused to create a session.
*/
export enum FixpNegotiationRejectCode {
    
    /** The server could not identify the client, or would not let it in. */
    Credentials = "Credentials",
    /** The server does not offer the flow type the client asked to send. */
    FlowTypeNotSupported = "FlowTypeNotSupported",
    /** The client chose a session identifier that is not new. */
    DuplicateId = "DuplicateId",
    /** Some reason the other values do not name. */
    Unspecified = "Unspecified",
};
/**
* Why a server would not bind the session to this transport.
*/
export enum FixpEstablishmentRejectCode {
    
    /** The session was never negotiated, or it has been finalized and needs a new negotiation. */
    Unnegotiated = "Unnegotiated",
    /** The server had already acknowledged a binding, so this request repeats it. */
    AlreadyEstablished = "AlreadyEstablished",
    /** The client may not use this session. */
    SessionBlocked = "SessionBlocked",
    /** The client's keep-alive interval is outside what the server accepts. */
    KeepaliveInterval = "KeepaliveInterval",
    /** The server could not identify the client, or would not let it in. */
    Credentials = "Credentials",
    /** Some reason the other values do not name. */
    Unspecified = "Unspecified",
};
/**
* Why a party will not resend the messages its peer asked for.
*/
export enum FixpRetransmitRejectCode {
    
    /** The range asked for runs past the sequence numbers sent so far. */
    OutOfRange = "OutOfRange",
    /** The session is unknown, or the one asking may not read it. */
    InvalidSession = "InvalidSession",
    /** The request asks for more messages than the sender resends at once. */
    RequestLimitExceeded = "RequestLimitExceeded",
};
/**
* Why a party releases a session from its transport.
*/
export enum FixpTerminationCode {
    
    /** An ordinary release, with no error. */
    Finished = "Finished",
    /** An error that the other values do not name. */
    UnspecifiedError = "UnspecifiedError",
    /** The peer asked again for messages outside the range sent. */
    ReRequestOutOfBounds = "ReRequestOutOfBounds",
    /** The peer asked again for messages while its earlier request was unanswered. */
    ReRequestInProgress = "ReRequestInProgress",
};
/**
* The two forms of FIXP session.
*/
export enum FixpSessionKind {
    
    /** A client and a server over a transport that carries messages both ways, with one flow each way. */
    point_to_point = "point_to_point",
    /** One publisher, one flow and many listeners, on a transport that only carries messages outward. */
    multicast = "multicast",
};
/**
* The side that sends a step.
*/
export enum FixpParty {
    
    /** The party that opens a session with a server. */
    client = "client",
    /** The party that accepts the client's session. */
    server = "server",
    /** The only party that sends in a multicast. */
    publisher = "publisher",
};


/**
 * One FIXP message, as its fields would be read from the wire before or after encoding.
 */
export interface FixpMessage {
    /** The class of this message, such as FixpNegotiate. It stands for FIXP's MessageType, which every message carries. */
    message_kind: string,
}


/**
 * A client's request to create a session under an identifier it has never used, stating the flow type it will send.
 */
export interface FixpNegotiate extends FixpMessage {
    /** The session's identifier, which the client chooses and never uses again. */
    session_id: string,
    /** When the sender made this request. The answer repeats it, to show what it answers. */
    request_time: string,
    /** The flow type of the application messages the client will send. */
    client_flow: string,
    /** Data that identifies the client, in a form the two parties agree on. */
    credentials?: string,
}


/**
 * A server's acceptance of a new session, stating the flow type it will send back.
 */
export interface FixpNegotiationResponse extends FixpMessage {
    /** The session's identifier, which the client chooses and never uses again. */
    session_id: string,
    /** The request_time of the Negotiate this message accepts. */
    request_timestamp: string,
    /** The flow type of the application messages the server will send. */
    server_flow: string,
    /** Data that identifies the server to the client, for mutual authentication. */
    credentials?: string,
}


/**
 * A server's refusal to create a session. The server sends nothing more and closes the transport.
 */
export interface FixpNegotiationReject extends FixpMessage {
    /** The session's identifier, which the client chooses and never uses again. */
    session_id: string,
    /** The request_time of the Negotiate this message refuses. */
    request_timestamp: string,
    /** Why the server refused to create the session. */
    negotiation_reject_code: string,
    /** Free text that says more about the code beside it. */
    reason_text?: string,
}


/**
 * A multicast publisher's notice that starts a flow and ties the session's short-lived identifier to a lasting subject. It is repeated so that late listeners can join.
 */
export interface FixpTopic extends FixpMessage {
    /** The session's identifier, which the client chooses and never uses again. */
    session_id: string,
    /** The flow type of a multicast topic's messages. */
    flow: string,
    /** The publisher's heartbeat interval, in milliseconds. */
    keepalive_interval?: string,
    /** The lasting subject of a topic's messages, such as a product type or a market symbol. */
    topic_classification: string,
}


/**
 * A client's request to tie a negotiated session to the very transport this message arrives on. After a disconnection it is sent again to re-bind.
 */
export interface FixpEstablish extends FixpMessage {
    /** The session's identifier, which the client chooses and never uses again. */
    session_id: string,
    /** When the sender made this request. The answer repeats it, to show what it answers. */
    request_time: string,
    /** The longest the client stays silent, in milliseconds, before a heartbeat. */
    keepalive_interval: string,
    /** When the client's recoverable flow is bound again, the number its next application message will carry. */
    next_seq_no?: string,
    /** Data that identifies the client, in a form the two parties agree on. */
    credentials?: string,
}


/**
 * A server's acceptance of the binding. From here, application messages may flow.
 */
export interface FixpEstablishmentAck extends FixpMessage {
    /** The session's identifier, which the client chooses and never uses again. */
    session_id: string,
    /** The request_time of the Establish this message accepts. */
    request_timestamp: string,
    /** The longest the server stays silent, in milliseconds, before a heartbeat. */
    keepalive_interval: string,
    /** If the server's flow is recoverable, the number its next application message will carry, so the client can ask for what it missed. */
    next_seq_no?: string,
}


/**
 * A server's refusal of the binding.
 */
export interface FixpEstablishmentReject extends FixpMessage {
    /** The session's identifier, which the client chooses and never uses again. */
    session_id: string,
    /** The request_time of the Establish this message refuses. */
    request_timestamp: string,
    /** Why the server refused to bind the session. */
    establishment_reject_code: string,
    /** Free text that says more about the code beside it. */
    reason_text?: string,
}


/**
 * Starts the numbering of a sequenced flow, so that the application messages after it are numbered by counting up from the value it carries. Sent when idle, it is also the heartbeat.
 */
export interface FixpSequence extends FixpMessage {
    /** The number the sender's next application message will carry. */
    next_seq_no: string,
}


/**
 * On a transport that several sessions share, names the session the following messages belong to and, when the flow is sequenced, where its numbering continues.
 */
export interface FixpContext extends FixpMessage {
    /** The session's identifier, which the client chooses and never uses again. */
    session_id: string,
    /** The number the sender's next application message will carry. */
    next_seq_no?: string,
}


/**
 * Shows the peer that the session and transport are alive when the sender's flow is unsequenced or empty. It has no fields.
 */
export interface FixpUnsequencedHeartbeat extends FixpMessage {
}


/**
 * Asks the peer to resend some messages of its recoverable flow. A party has at most one such request open at a time.
 */
export interface FixpRetransmitRequest extends FixpMessage {
    /** The session's identifier, which the client chooses and never uses again. */
    session_id: string,
    /** When the request was made, which also tells this request apart from others. */
    request_time: string,
    /** Where the requested run starts, by sequence number. */
    from_seq_no: string,
    /** How many messages are asked for. */
    message_count: string,
}


/**
 * Introduces a batch of resent messages, which are numbered by counting from the number it gives. A request may be answered in several batches.
 */
export interface FixpRetransmission extends FixpMessage {
    /** The session's identifier, which the client chooses and never uses again. */
    session_id: string,
    /** The request_time of the RetransmitRequest this batch answers. */
    request_timestamp: string,
    /** The number the batch's first message carries. */
    next_seq_no: string,
    /** How many resent messages the batch holds. */
    message_count: string,
}


/**
 * Refuses a RetransmitRequest, with a code saying why.
 */
export interface FixpRetransmitReject extends FixpMessage {
    /** The session's identifier, which the client chooses and never uses again. */
    session_id: string,
    /** The request_time of the RetransmitRequest this message refuses. */
    request_timestamp: string,
    /** Why the sender will not resend the range. */
    retransmit_reject_code: string,
    /** Free text that says more about the code beside it. */
    reason_text?: string,
}


/**
 * Releases the session from its transport without ending the session, which can be bound again later. The peer answers with a Terminate, and after its own Terminate a party sends nothing more.
 */
export interface FixpTerminate extends FixpMessage {
    /** The session's identifier, which the client chooses and never uses again. */
    session_id: string,
    /** Why the party releases the session from the transport. */
    termination_code: string,
    /** Free text that says more about the code beside it. */
    reason_text?: string,
}


/**
 * Says that the sender's flow has carried its last application message, which begins finalization. It is repeated as the heartbeat until the answer comes.
 */
export interface FixpFinishedSending extends FixpMessage {
    /** The session's identifier, which the client chooses and never uses again. */
    session_id: string,
    /** The number carried by the flow's final application message. */
    last_seq_no?: string,
}


/**
 * Answers FinishedSending once the last message of the peer's flow has been processed. After it the session is finalized and its identifier is spent.
 */
export interface FixpFinishedReceiving extends FixpMessage {
    /** The session's identifier, which the client chooses and never uses again. */
    session_id: string,
}


/**
 * An optional application message telling the party that sends an idempotent flow which of its operations took effect, where no business message already says so.
 */
export interface FixpApplied extends FixpMessage {
    /** Where the run of operations that took effect starts. */
    from_seq_no: string,
    /** How many operations in a row took effect. */
    message_count: string,
}


/**
 * An application message telling the party that sends an idempotent flow about a gap: a run of operations that did not take effect. That party's application decides what to do.
 */
export interface FixpNotApplied extends FixpMessage {
    /** Where the run of operations that failed to take effect starts. */
    from_seq_no: string,
    /** How many operations in a row did not take effect. */
    message_count: string,
}


/**
 * Hands the peer a template or schema it needs to read messages in an encoding that templates drive. There is no fixed moment for sending it.
 */
export interface FixpMessageTemplate extends FixpMessage {
    /** The code that the Simple Open Framing Header registers for the encoding a template is written for. */
    sofh_encoding_type: string,
    /** When the template comes into force. Without it, the template applies at once. */
    effective_time?: string,
    /** The template's version and format, for an encoding whose templates do not state them. */
    template_version?: string,
    /** The template itself, as octets. */
    template: string,
}


/**
 * The messages of one session in the order they were sent, as a test case, a worked example or a captured log.
 */
export interface FixpExchange {
    /** The identifier of an exchange or a rules-of-engagement record. */
    id: string,
    /** Free text about a record, for the people who read it. */
    description?: string,
    /** Which of the two forms the session takes. */
    session_kind: string,
    /** Whether the transport carries other sessions too, so that Context takes the place of Sequence. */
    multiplexed?: boolean,
    /** Each step of the exchange, in order. */
    exchange_steps: FixpExchangeStep[],
}


/**
 * One step: a FIXP message, or a run of application messages whose content FIXP does not define, and the side that sent it.
 */
export interface FixpExchangeStep {
    /** The side that sent this step. */
    sent_by: string,
    /** The FIXP message sent. */
    fixp_message?: FixpMessage,
    /** How many application messages went out one after another. On a sequenced flow each takes the next sequence number. */
    application_message_count?: string,
}


/**
 * What two counterparties agree on for one FIXP service, layer by layer, for the client and for the server.
 */
export interface FixpRulesOfEngagement {
    /** The identifier of an exchange or a rules-of-engagement record. */
    id: string,
    /** Free text about a record, for the people who read it. */
    description?: string,
    /** What the client side uses. */
    client_stack: FixpStackProfile,
    /** What the server side uses. */
    server_stack: FixpStackProfile,
}


/**
 * One side's choices at each layer of the stack: application, presentation, session, security and transport.
 */
export interface FixpStackProfile {
    /** Whether this side's applications recover lost messages themselves. */
    application_recovery?: boolean,
    /** The FIX version of the application messages, such as FIX.Latest. */
    application_fix_version?: string,
    /** The FIX service pack, where the version has them. */
    service_pack?: string,
    /** The FIX extension packs in use. */
    extension_packs?: string[],
    /** How messages are encoded, such as Simple Binary Encoding. */
    message_encoding?: string,
    /** The version of that encoding. */
    encoding_version?: string,
    /** The message schemas or templates the encoding uses. */
    message_schemas?: string[],
    /** What marks where one message ends and the next begins, such as the Simple Open Framing Header. */
    framing?: string,
    /** The flow types this side accepts or offers. */
    supported_flow_types?: string,
    /** The shortest keep-alive interval, in milliseconds, that this side accepts from its peer. */
    shortest_keepalive_interval?: string,
    /** The longest keep-alive interval, in milliseconds, that this side accepts from its peer. */
    longest_keepalive_interval?: string,
    /** The most messages this side resends in answer to one RetransmitRequest. */
    retransmission_limit?: string,
    /** The TLS version that protects the transport. */
    tls_version?: string,
    /** How the parties prove who they are. */
    authentication_methods?: string[],
    /** The form of the credentials this side sends, and how its peer checks them. */
    credentials_format?: string,
    /** The cipher suites allowed. */
    cipher_suites?: string[],
    /** The transports this side can use, for example TCP, or UDP with multicast. */
    transports?: string[],
    /** Any other network protocols in use. */
    network_protocols?: string[],
}



