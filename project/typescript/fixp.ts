/**
* FIX Orchestra codeSet 'ClientFlowCodeSet' (id=3, type=int).
*/
export enum ClientFlowCodeSet {
    
    Recoverable = "RECOVERABLE",
    Idempotent = "IDEMPOTENT",
    Unsequenced = "UNSEQUENCED",
    None = "NONE",
};
/**
* FIX Orchestra codeSet 'NegotiationRejectCodeCodeSet' (id=7, type=int).
*/
export enum NegotiationRejectCodeCodeSet {
    
    Credentials = "CREDENTIALS",
    FlowTypeNotSupported = "FLOW_TYPE_NOT_SUPPORTED",
    DuplicateId = "DUPLICATE_ID",
    Unspecified = "UNSPECIFIED",
};
/**
* FIX Orchestra codeSet 'EstablishmentRejectCodeCodeSet' (id=12, type=int).
*/
export enum EstablishmentRejectCodeCodeSet {
    
    Unnegotiated = "UNNEGOTIATED",
    AlreadyEstablished = "ALREADY_ESTABLISHED",
    SessionBlocked = "SESSION_BLOCKED",
    KeepaliveInterval = "KEEPALIVE_INTERVAL",
    Credentials = "CREDENTIALS",
    Unspecified = "UNSPECIFIED",
};
/**
* FIX Orchestra codeSet 'RetransmitRejectCodeCodeSet' (id=15, type=int).
*/
export enum RetransmitRejectCodeCodeSet {
    
    OutOfRange = "OUT_OF_RANGE",
    InvalidSession = "INVALID_SESSION",
    RequestLimitExceeded = "REQUEST_LIMIT_EXCEEDED",
};
/**
* FIX Orchestra codeSet 'TerminationCodeCodeSet' (id=16, type=int).
*/
export enum TerminationCodeCodeSet {
    
    Finished = "FINISHED",
    UnspecifiedError = "UNSPECIFIED_ERROR",
    ReRequestOutOfBounds = "RE_REQUEST_OUT_OF_BOUNDS",
    ReRequestInProgress = "RE_REQUEST_IN_PROGRESS",
};
/**
* FIX Orchestra codeSet 'FlowCodeSet' (id=18, type=int).
*/
export enum FlowCodeSet {
    
    Recoverable = "RECOVERABLE",
    Idempotent = "IDEMPOTENT",
};
/**
* SBE enum 'FlowType' (encodingType=uint8).
*/
export enum SbeFlowType {
    
    /** Guarantees exactly-once message delivery */
    Recoverable = "RECOVERABLE",
    /** Guarantees at-most-once delivery */
    Idempotent = "IDEMPOTENT",
    /** Best effort delivery */
    Unsequenced = "UNSEQUENCED",
    /** No application messages should be sent in one direction of a session */
    None = "NONE",
};
/**
* SBE enum 'NegotiationRejectCode' (encodingType=uint8).
*/
export enum SbeNegotiationRejectCode {
    
    /** Failed authentication because identity is not recognized, or the user is not authorized to use a particular service */
    Credentials = "CREDENTIALS",
    /** Server does not support requested client flow type */
    FlowTypeNotSupported = "FLOW_TYPE_NOT_SUPPORTED",
    /** Session ID is non-unique */
    DuplicateId = "DUPLICATE_ID",
    Unspecified = "UNSPECIFIED",
};
/**
* SBE enum 'EstablishmentRejectCode' (encodingType=uint8).
*/
export enum SbeEstablishmentRejectCode {
    
    /** Establish request was not preceded by a Negotiation or session was finalized, requiring renegotiation */
    Unnegotiated = "UNNEGOTIATED",
    /** EstablishmentAck was already sent; Establish was redundant */
    AlreadyEstablished = "ALREADY_ESTABLISHED",
    /** User is not authorized */
    SessionBlocked = "SESSION_BLOCKED",
    /** Value is out of accepted range */
    KeepaliveInterval = "KEEPALIVE_INTERVAL",
    /** Failed authentication because identity is not recognized, or the user is not authorized to use a particular service */
    Credentials = "CREDENTIALS",
    Unspecified = "UNSPECIFIED",
};
/**
* SBE enum 'RetransmitRejectCode' (encodingType=uint8).
*/
export enum SbeRetransmitRejectCode {
    
    /** NextSeqNo + Count is beyond the range of sequence numbers */
    OutOfRange = "OUT_OF_RANGE",
    /** The specified SessionId is unknown or is not authorized for the requester to access */
    InvalidSession = "INVALID_SESSION",
    /** The message Count exceeds a local rule for maximum retransmission size */
    RequestLimitExceeded = "REQUEST_LIMIT_EXCEEDED",
};
/**
* SBE enum 'TerminationCode' (encodingType=uint8).
*/
export enum SbeTerminationCode {
    
    Finished = "FINISHED",
    UnspecifiedError = "UNSPECIFIED_ERROR",
    ReRequestOutOfBounds = "RE_REQUEST_OUT_OF_BOUNDS",
    ReRequestInProgress = "RE_REQUEST_IN_PROGRESS",
};
/**
* Inline FIX field enumeration for field 'ClientFlow' (id=3).
*/
export enum ClientFlowFieldEnum {
    
    Recoverable = "RECOVERABLE",
    Idempotent = "IDEMPOTENT",
    Unsequenced = "UNSEQUENCED",
    None = "NONE",
};
/**
* Inline FIX field enumeration for field 'NegotiationRejectCode' (id=7).
*/
export enum NegotiationRejectCodeFieldEnum {
    
    Credentials = "CREDENTIALS",
    FlowTypeNotSupported = "FLOW_TYPE_NOT_SUPPORTED",
    DuplicateId = "DUPLICATE_ID",
    Unspecified = "UNSPECIFIED",
};
/**
* Inline FIX field enumeration for field 'EstablishmentRejectCode' (id=12).
*/
export enum EstablishmentRejectCodeFieldEnum {
    
    Unnegotiated = "UNNEGOTIATED",
    AlreadyEstablished = "ALREADY_ESTABLISHED",
    SessionBlocked = "SESSION_BLOCKED",
    KeepaliveInterval = "KEEPALIVE_INTERVAL",
    Credentials = "CREDENTIALS",
    Unspecified = "UNSPECIFIED",
};
/**
* Inline FIX field enumeration for field 'RetransmitRejectCode' (id=15).
*/
export enum RetransmitRejectCodeFieldEnum {
    
    OutOfRange = "OUT_OF_RANGE",
    InvalidSession = "INVALID_SESSION",
    RequestLimitExceeded = "REQUEST_LIMIT_EXCEEDED",
};
/**
* Inline FIX field enumeration for field 'TerminationCode' (id=16).
*/
export enum TerminationCodeFieldEnum {
    
    Finished = "FINISHED",
    UnspecifiedError = "UNSPECIFIED_ERROR",
    ReRequestOutOfBounds = "RE_REQUEST_OUT_OF_BOUNDS",
    ReRequestInProgress = "RE_REQUEST_IN_PROGRESS",
};
/**
* Inline FIX field enumeration for field 'Flow' (id=18).
*/
export enum FlowFieldEnum {
    
    Recoverable = "RECOVERABLE",
    Idempotent = "IDEMPOTENT",
};


/**
 * Top-level container for a FIXP session exchange - holds an ordered list of session messages plus optional metadata.
 */
export interface FixpSessionExchange {
    /** Ordered sequence of FIXP session messages. */
    messages?: FixpSessionMessage[],
    /** Title of this exchange document. */
    title?: string,
    /** Creator of this exchange document. */
    creator?: string,
    /** Publisher of this exchange document. */
    publisher?: string,
    /** Rights statement for this exchange document. */
    rights?: string,
    /** Date associated with this exchange document. */
    date?: string,
}


/**
 * Abstract base class for every FIXP session message.
 */
export interface FixpSessionMessage {
}


/**
 * Variable length data, also know as octect string
 */
export interface SbeObjectComposite {
    /** SBE member 'length' (primitiveType=uint16, semanticType=Length). */
    length?: number,
    /** SBE member 'varData' (primitiveType=uint8, semanticType=data). */
    var_data?: number,
}


/**
 * Variable length text
 */
export interface SbeCharacterStringComposite {
    /** SBE member 'length' (primitiveType=uint16, semanticType=Length). */
    length?: number,
    /** SBE member 'varData' (primitiveType=char, semanticType=String). */
    var_data?: string,
}


/**
 * Message identifiers and length of message root
 */
export interface SbeMessageHeaderComposite {
    /** SBE member 'blockLength' (primitiveType=uint16). */
    block_length?: number,
    /** SBE member 'templateId' (primitiveType=uint16). */
    template_id?: number,
    /** SBE member 'schemaId' (primitiveType=uint16). */
    schema_id?: number,
    /** SBE member 'version' (primitiveType=uint16). */
    schema_version?: number,
}


/**
 * FIXP session message 'Negotiate'.
 */
export interface Negotiate extends FixpSessionMessage {
    /** FIX field 'SessionId' (tag 1). */
    session_id: string,
    /** FIX field 'Timestamp' (tag 2). */
    timestamp: string,
    /** FIX field 'ClientFlow' (tag 3). */
    client_flow: string,
    /** FIX field 'Credentials' (tag 4). */
    credentials?: string,
}


/**
 * FIXP session message 'NegotiationResponse'.
 */
export interface NegotiationResponse extends FixpSessionMessage {
    /** FIX field 'SessionId' (tag 1). */
    session_id: string,
    /** FIX field 'RequestTimestamp' (tag 5). */
    request_timestamp: string,
    /** FIX field 'ServerFlow' (tag 6). */
    server_flow: string,
    /** FIX field 'Credentials' (tag 4). */
    credentials?: string,
}


/**
 * FIXP session message 'NegotiationReject'.
 */
export interface NegotiationReject extends FixpSessionMessage {
    /** FIX field 'SessionId' (tag 1). */
    session_id: string,
    /** FIX field 'RequestTimestamp' (tag 5). */
    request_timestamp: string,
    /** FIX field 'NegotiationRejectCode' (tag 7). */
    negotiation_reject_code: string,
    /** FIX field 'Reason' (tag 8). */
    reason?: string,
}


/**
 * FIXP session message 'Topic'.
 */
export interface Topic extends FixpSessionMessage {
    /** FIX field 'SessionId' (tag 1). */
    session_id: string,
    /** FIX field 'Flow' (tag 18). */
    flow: string,
    /** FIX field 'KeepaliveInterval' (tag 9). */
    keepalive_interval: string,
    /** FIX field 'Classification' (tag 10). */
    classification: string,
}


/**
 * FIXP session message 'Establish'.
 */
export interface Establish extends FixpSessionMessage {
    /** FIX field 'SessionId' (tag 1). */
    session_id: string,
    /** FIX field 'Timestamp' (tag 2). */
    timestamp: string,
    /** FIX field 'KeepaliveInterval' (tag 9). */
    keepalive_interval: string,
    /** FIX field 'NextSeqNo' (tag 11). */
    next_seq_no?: string,
    /** FIX field 'Credentials' (tag 4). */
    credentials?: string,
}


/**
 * FIXP session message 'EstablishmentAck'.
 */
export interface EstablishmentAck extends FixpSessionMessage {
    /** FIX field 'SessionId' (tag 1). */
    session_id: string,
    /** FIX field 'RequestTimestamp' (tag 5). */
    request_timestamp: string,
    /** FIX field 'KeepaliveInterval' (tag 9). */
    keepalive_interval: string,
    /** FIX field 'NextSeqNo' (tag 11). */
    next_seq_no?: string,
}


/**
 * FIXP session message 'EstablishmentReject'.
 */
export interface EstablishmentReject extends FixpSessionMessage {
    /** FIX field 'SessionId' (tag 1). */
    session_id: string,
    /** FIX field 'RequestTimestamp' (tag 5). */
    request_timestamp: string,
    /** FIX field 'EstablishmentRejectCode' (tag 12). */
    establishment_reject_code: string,
    /** FIX field 'Reason' (tag 8). */
    reason?: string,
}


/**
 * FIXP session message 'Sequence'.
 */
export interface Sequence extends FixpSessionMessage {
    /** FIX field 'NextSeqNo' (tag 11). */
    next_seq_no: string,
}


/**
 * FIXP session message 'Context'.
 */
export interface Context extends FixpSessionMessage {
    /** FIX field 'SessionId' (tag 1). */
    session_id: string,
    /** FIX field 'NextSeqNo' (tag 11). */
    next_seq_no: string,
}


/**
 * FIXP session message 'UnsequencedHeartbeat'.
 */
export interface UnsequencedHeartbeat extends FixpSessionMessage {
}


/**
 * FIXP session message 'RetransmitRequest'.
 */
export interface RetransmitRequest extends FixpSessionMessage {
    /** FIX field 'SessionId' (tag 1). */
    session_id: string,
    /** FIX field 'Timestamp' (tag 2). */
    timestamp: string,
    /** FIX field 'FromSeqNo' (tag 13). */
    from_seq_no: string,
    /** FIX field 'Count' (tag 14). */
    count: string,
}


/**
 * FIXP session message 'Retransmission'.
 */
export interface Retransmission extends FixpSessionMessage {
    /** FIX field 'SessionId' (tag 1). */
    session_id: string,
    /** FIX field 'RequestTimestamp' (tag 5). */
    request_timestamp: string,
    /** FIX field 'NextSeqNo' (tag 11). */
    next_seq_no: string,
    /** FIX field 'Count' (tag 14). */
    count: string,
}


/**
 * FIXP session message 'RestransmitReject'.
 */
export interface RestransmitReject extends FixpSessionMessage {
    /** FIX field 'SessionId' (tag 1). */
    session_id: string,
    /** FIX field 'RequestTimestamp' (tag 5). */
    request_timestamp: string,
    /** FIX field 'RetransmitRejectCode' (tag 15). */
    retransmit_reject_code: string,
    /** FIX field 'Reason' (tag 8). */
    reason?: string,
}


/**
 * FIXP session message 'Terminate'.
 */
export interface Terminate extends FixpSessionMessage {
    /** FIX field 'SessionId' (tag 1). */
    session_id: string,
    /** FIX field 'TerminationCode' (tag 16). */
    termination_code: string,
    /** FIX field 'Reason' (tag 8). */
    reason?: string,
}


/**
 * FIXP session message 'FinishedSending'.
 */
export interface FinishedSending extends FixpSessionMessage {
    /** FIX field 'SessionId' (tag 1). */
    session_id: string,
    /** FIX field 'LastSeqNo' (tag 17). */
    last_seq_no: string,
}


/**
 * FIXP session message 'FinishedReceiving'.
 */
export interface FinishedReceiving extends FixpSessionMessage {
    /** FIX field 'SessionId' (tag 1). */
    session_id: string,
}


/**
 * FIXP session message 'Applied'.
 */
export interface Applied extends FixpSessionMessage {
    /** FIX field 'FromSeqNo' (tag 13). */
    from_seq_no: string,
    /** FIX field 'Count' (tag 14). */
    count: string,
}


/**
 * FIXP session message 'NotApplied'.
 */
export interface NotApplied extends FixpSessionMessage {
    /** FIX field 'FromSeqNo' (tag 13). */
    from_seq_no: string,
    /** FIX field 'Count' (tag 14). */
    count: string,
}


/**
 * FIXP session message 'MessageTemplate'.
 */
export interface MessageTemplate extends FixpSessionMessage {
    /** FIX field 'Flow' (tag 18). */
    flow: string,
    /** FIX field 'EffectiveTime' (tag 19). */
    effective_time: string,
    /** FIX field 'Version' (tag 20). */
    version?: string,
    /** FIX field 'Template' (tag 22). */
    template: string,
}



