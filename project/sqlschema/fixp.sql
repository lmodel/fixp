-- # Class: FixpSessionExchange Description: Top-level container for a FIXP session exchange - holds an ordered list of session messages plus optional metadata.
--     * Slot: id
--     * Slot: title Description: Title of this exchange document.
--     * Slot: creator Description: Creator of this exchange document.
--     * Slot: publisher Description: Publisher of this exchange document.
--     * Slot: rights Description: Rights statement for this exchange document.
--     * Slot: date Description: Date associated with this exchange document.
-- # Abstract Class: FixpSessionMessage Description: Abstract base class for every FIXP session message.
--     * Slot: id
--     * Slot: FixpSessionExchange_id Description: Autocreated FK slot
-- # Class: SbeObjectComposite Description: Variable length data, also know as octect string
--     * Slot: id
--     * Slot: length Description: SBE member 'length' (primitiveType=uint16, semanticType=Length).
--     * Slot: var_data Description: SBE member 'varData' (primitiveType=uint8, semanticType=data).
-- # Class: SbeCharacterStringComposite Description: Variable length text
--     * Slot: id
--     * Slot: length Description: SBE member 'length' (primitiveType=uint16, semanticType=Length).
--     * Slot: var_data Description: SBE member 'varData' (primitiveType=char, semanticType=String).
-- # Class: SbeMessageHeaderComposite Description: Message identifiers and length of message root
--     * Slot: id
--     * Slot: block_length Description: SBE member 'blockLength' (primitiveType=uint16).
--     * Slot: template_id Description: SBE member 'templateId' (primitiveType=uint16).
--     * Slot: schema_id Description: SBE member 'schemaId' (primitiveType=uint16).
--     * Slot: schema_version Description: SBE member 'version' (primitiveType=uint16).
-- # Class: Negotiate Description: FIXP session message 'Negotiate'.
--     * Slot: id
--     * Slot: session_id Description: FIX field 'SessionId' (tag 1).
--     * Slot: timestamp Description: FIX field 'Timestamp' (tag 2).
--     * Slot: client_flow Description: FIX field 'ClientFlow' (tag 3).
--     * Slot: credentials Description: FIX field 'Credentials' (tag 4).
-- # Class: NegotiationResponse Description: FIXP session message 'NegotiationResponse'.
--     * Slot: id
--     * Slot: session_id Description: FIX field 'SessionId' (tag 1).
--     * Slot: request_timestamp Description: FIX field 'RequestTimestamp' (tag 5).
--     * Slot: server_flow Description: FIX field 'ServerFlow' (tag 6).
--     * Slot: credentials Description: FIX field 'Credentials' (tag 4).
-- # Class: NegotiationReject Description: FIXP session message 'NegotiationReject'.
--     * Slot: id
--     * Slot: session_id Description: FIX field 'SessionId' (tag 1).
--     * Slot: request_timestamp Description: FIX field 'RequestTimestamp' (tag 5).
--     * Slot: negotiation_reject_code Description: FIX field 'NegotiationRejectCode' (tag 7).
--     * Slot: reason Description: FIX field 'Reason' (tag 8).
-- # Class: Topic Description: FIXP session message 'Topic'.
--     * Slot: id
--     * Slot: session_id Description: FIX field 'SessionId' (tag 1).
--     * Slot: flow Description: FIX field 'Flow' (tag 18).
--     * Slot: keepalive_interval Description: FIX field 'KeepaliveInterval' (tag 9).
--     * Slot: classification Description: FIX field 'Classification' (tag 10).
-- # Class: Establish Description: FIXP session message 'Establish'.
--     * Slot: id
--     * Slot: session_id Description: FIX field 'SessionId' (tag 1).
--     * Slot: timestamp Description: FIX field 'Timestamp' (tag 2).
--     * Slot: keepalive_interval Description: FIX field 'KeepaliveInterval' (tag 9).
--     * Slot: next_seq_no Description: FIX field 'NextSeqNo' (tag 11).
--     * Slot: credentials Description: FIX field 'Credentials' (tag 4).
-- # Class: EstablishmentAck Description: FIXP session message 'EstablishmentAck'.
--     * Slot: id
--     * Slot: session_id Description: FIX field 'SessionId' (tag 1).
--     * Slot: request_timestamp Description: FIX field 'RequestTimestamp' (tag 5).
--     * Slot: keepalive_interval Description: FIX field 'KeepaliveInterval' (tag 9).
--     * Slot: next_seq_no Description: FIX field 'NextSeqNo' (tag 11).
-- # Class: EstablishmentReject Description: FIXP session message 'EstablishmentReject'.
--     * Slot: id
--     * Slot: session_id Description: FIX field 'SessionId' (tag 1).
--     * Slot: request_timestamp Description: FIX field 'RequestTimestamp' (tag 5).
--     * Slot: establishment_reject_code Description: FIX field 'EstablishmentRejectCode' (tag 12).
--     * Slot: reason Description: FIX field 'Reason' (tag 8).
-- # Class: Sequence Description: FIXP session message 'Sequence'.
--     * Slot: id
--     * Slot: next_seq_no Description: FIX field 'NextSeqNo' (tag 11).
-- # Class: Context Description: FIXP session message 'Context'.
--     * Slot: id
--     * Slot: session_id Description: FIX field 'SessionId' (tag 1).
--     * Slot: next_seq_no Description: FIX field 'NextSeqNo' (tag 11).
-- # Class: UnsequencedHeartbeat Description: FIXP session message 'UnsequencedHeartbeat'.
--     * Slot: id
-- # Class: RetransmitRequest Description: FIXP session message 'RetransmitRequest'.
--     * Slot: id
--     * Slot: session_id Description: FIX field 'SessionId' (tag 1).
--     * Slot: timestamp Description: FIX field 'Timestamp' (tag 2).
--     * Slot: from_seq_no Description: FIX field 'FromSeqNo' (tag 13).
--     * Slot: count Description: FIX field 'Count' (tag 14).
-- # Class: Retransmission Description: FIXP session message 'Retransmission'.
--     * Slot: id
--     * Slot: session_id Description: FIX field 'SessionId' (tag 1).
--     * Slot: request_timestamp Description: FIX field 'RequestTimestamp' (tag 5).
--     * Slot: next_seq_no Description: FIX field 'NextSeqNo' (tag 11).
--     * Slot: count Description: FIX field 'Count' (tag 14).
-- # Class: RestransmitReject Description: FIXP session message 'RestransmitReject'.
--     * Slot: id
--     * Slot: session_id Description: FIX field 'SessionId' (tag 1).
--     * Slot: request_timestamp Description: FIX field 'RequestTimestamp' (tag 5).
--     * Slot: retransmit_reject_code Description: FIX field 'RetransmitRejectCode' (tag 15).
--     * Slot: reason Description: FIX field 'Reason' (tag 8).
-- # Class: Terminate Description: FIXP session message 'Terminate'.
--     * Slot: id
--     * Slot: session_id Description: FIX field 'SessionId' (tag 1).
--     * Slot: termination_code Description: FIX field 'TerminationCode' (tag 16).
--     * Slot: reason Description: FIX field 'Reason' (tag 8).
-- # Class: FinishedSending Description: FIXP session message 'FinishedSending'.
--     * Slot: id
--     * Slot: session_id Description: FIX field 'SessionId' (tag 1).
--     * Slot: last_seq_no Description: FIX field 'LastSeqNo' (tag 17).
-- # Class: FinishedReceiving Description: FIXP session message 'FinishedReceiving'.
--     * Slot: id
--     * Slot: session_id Description: FIX field 'SessionId' (tag 1).
-- # Class: Applied Description: FIXP session message 'Applied'.
--     * Slot: id
--     * Slot: from_seq_no Description: FIX field 'FromSeqNo' (tag 13).
--     * Slot: count Description: FIX field 'Count' (tag 14).
-- # Class: NotApplied Description: FIXP session message 'NotApplied'.
--     * Slot: id
--     * Slot: from_seq_no Description: FIX field 'FromSeqNo' (tag 13).
--     * Slot: count Description: FIX field 'Count' (tag 14).
-- # Class: MessageTemplate Description: FIXP session message 'MessageTemplate'.
--     * Slot: id
--     * Slot: flow Description: FIX field 'Flow' (tag 18).
--     * Slot: effective_time Description: FIX field 'EffectiveTime' (tag 19).
--     * Slot: version Description: FIX field 'Version' (tag 20).
--     * Slot: template Description: FIX field 'Template' (tag 22).

CREATE TABLE "FixpSessionExchange" (
	id INTEGER NOT NULL,
	title TEXT,
	creator TEXT,
	publisher TEXT,
	rights TEXT,
	date TEXT,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_FixpSessionExchange_id" ON "FixpSessionExchange" (id);

CREATE TABLE "SbeObjectComposite" (
	id INTEGER NOT NULL,
	length INTEGER,
	var_data INTEGER,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_SbeObjectComposite_id" ON "SbeObjectComposite" (id);

CREATE TABLE "SbeCharacterStringComposite" (
	id INTEGER NOT NULL,
	length INTEGER,
	var_data TEXT,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_SbeCharacterStringComposite_id" ON "SbeCharacterStringComposite" (id);

CREATE TABLE "SbeMessageHeaderComposite" (
	id INTEGER NOT NULL,
	block_length INTEGER,
	template_id INTEGER,
	schema_id INTEGER,
	schema_version INTEGER,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_SbeMessageHeaderComposite_id" ON "SbeMessageHeaderComposite" (id);

CREATE TABLE "Negotiate" (
	id INTEGER NOT NULL,
	session_id TEXT NOT NULL,
	timestamp TEXT NOT NULL,
	client_flow VARCHAR(11) NOT NULL,
	credentials TEXT,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_Negotiate_id" ON "Negotiate" (id);

CREATE TABLE "NegotiationResponse" (
	id INTEGER NOT NULL,
	session_id TEXT NOT NULL,
	request_timestamp TEXT NOT NULL,
	server_flow VARCHAR(11) NOT NULL,
	credentials TEXT,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_NegotiationResponse_id" ON "NegotiationResponse" (id);

CREATE TABLE "NegotiationReject" (
	id INTEGER NOT NULL,
	session_id TEXT NOT NULL,
	request_timestamp TEXT NOT NULL,
	negotiation_reject_code VARCHAR(23) NOT NULL,
	reason TEXT,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_NegotiationReject_id" ON "NegotiationReject" (id);

CREATE TABLE "Topic" (
	id INTEGER NOT NULL,
	session_id TEXT NOT NULL,
	flow VARCHAR(11) NOT NULL,
	keepalive_interval TEXT NOT NULL,
	classification TEXT NOT NULL,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_Topic_id" ON "Topic" (id);

CREATE TABLE "Establish" (
	id INTEGER NOT NULL,
	session_id TEXT NOT NULL,
	timestamp TEXT NOT NULL,
	keepalive_interval TEXT NOT NULL,
	next_seq_no TEXT,
	credentials TEXT,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_Establish_id" ON "Establish" (id);

CREATE TABLE "EstablishmentAck" (
	id INTEGER NOT NULL,
	session_id TEXT NOT NULL,
	request_timestamp TEXT NOT NULL,
	keepalive_interval TEXT NOT NULL,
	next_seq_no TEXT,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_EstablishmentAck_id" ON "EstablishmentAck" (id);

CREATE TABLE "EstablishmentReject" (
	id INTEGER NOT NULL,
	session_id TEXT NOT NULL,
	request_timestamp TEXT NOT NULL,
	establishment_reject_code VARCHAR(19) NOT NULL,
	reason TEXT,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_EstablishmentReject_id" ON "EstablishmentReject" (id);

CREATE TABLE "Sequence" (
	id INTEGER NOT NULL,
	next_seq_no TEXT NOT NULL,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_Sequence_id" ON "Sequence" (id);

CREATE TABLE "Context" (
	id INTEGER NOT NULL,
	session_id TEXT NOT NULL,
	next_seq_no TEXT NOT NULL,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_Context_id" ON "Context" (id);

CREATE TABLE "UnsequencedHeartbeat" (
	id INTEGER NOT NULL,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_UnsequencedHeartbeat_id" ON "UnsequencedHeartbeat" (id);

CREATE TABLE "RetransmitRequest" (
	id INTEGER NOT NULL,
	session_id TEXT NOT NULL,
	timestamp TEXT NOT NULL,
	from_seq_no TEXT NOT NULL,
	count TEXT NOT NULL,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_RetransmitRequest_id" ON "RetransmitRequest" (id);

CREATE TABLE "Retransmission" (
	id INTEGER NOT NULL,
	session_id TEXT NOT NULL,
	request_timestamp TEXT NOT NULL,
	next_seq_no TEXT NOT NULL,
	count TEXT NOT NULL,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_Retransmission_id" ON "Retransmission" (id);

CREATE TABLE "RestransmitReject" (
	id INTEGER NOT NULL,
	session_id TEXT NOT NULL,
	request_timestamp TEXT NOT NULL,
	retransmit_reject_code VARCHAR(22) NOT NULL,
	reason TEXT,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_RestransmitReject_id" ON "RestransmitReject" (id);

CREATE TABLE "Terminate" (
	id INTEGER NOT NULL,
	session_id TEXT NOT NULL,
	termination_code VARCHAR(24) NOT NULL,
	reason TEXT,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_Terminate_id" ON "Terminate" (id);

CREATE TABLE "FinishedSending" (
	id INTEGER NOT NULL,
	session_id TEXT NOT NULL,
	last_seq_no TEXT NOT NULL,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_FinishedSending_id" ON "FinishedSending" (id);

CREATE TABLE "FinishedReceiving" (
	id INTEGER NOT NULL,
	session_id TEXT NOT NULL,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_FinishedReceiving_id" ON "FinishedReceiving" (id);

CREATE TABLE "Applied" (
	id INTEGER NOT NULL,
	from_seq_no TEXT NOT NULL,
	count TEXT NOT NULL,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_Applied_id" ON "Applied" (id);

CREATE TABLE "NotApplied" (
	id INTEGER NOT NULL,
	from_seq_no TEXT NOT NULL,
	count TEXT NOT NULL,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_NotApplied_id" ON "NotApplied" (id);

CREATE TABLE "MessageTemplate" (
	id INTEGER NOT NULL,
	flow VARCHAR(11) NOT NULL,
	effective_time TEXT NOT NULL,
	version TEXT,
	template TEXT NOT NULL,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_MessageTemplate_id" ON "MessageTemplate" (id);

CREATE TABLE "FixpSessionMessage" (
	id INTEGER NOT NULL,
	"FixpSessionExchange_id" INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY("FixpSessionExchange_id") REFERENCES "FixpSessionExchange" (id)
);
CREATE INDEX "ix_FixpSessionMessage_id" ON "FixpSessionMessage" (id);
