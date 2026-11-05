-- # Abstract Class: FixpMessage Description: One FIXP message, as its fields would be read from the wire before or after encoding.
--     * Slot: id
--     * Slot: message_kind Description: The class of this message, such as FixpNegotiate. It stands for FIXP's MessageType, which every message carries.
-- # Class: FixpNegotiate Description: A client's request to create a session under an identifier it has never used, stating the flow type it will send.
--     * Slot: id
--     * Slot: session_id Description: The session's identifier, which the client chooses and never uses again.
--     * Slot: request_time Description: When the sender made this request. The answer repeats it, to show what it answers.
--     * Slot: client_flow Description: The flow type of the application messages the client will send.
--     * Slot: credentials Description: Data that identifies the client, in a form the two parties agree on.
--     * Slot: message_kind Description: The class of this message, such as FixpNegotiate. It stands for FIXP's MessageType, which every message carries.
-- # Class: FixpNegotiationResponse Description: A server's acceptance of a new session, stating the flow type it will send back.
--     * Slot: id
--     * Slot: session_id Description: The session's identifier, which the client chooses and never uses again.
--     * Slot: request_timestamp Description: The request_time of the Negotiate this message accepts.
--     * Slot: server_flow Description: The flow type of the application messages the server will send.
--     * Slot: credentials Description: Data that identifies the server to the client, for mutual authentication.
--     * Slot: message_kind Description: The class of this message, such as FixpNegotiate. It stands for FIXP's MessageType, which every message carries.
-- # Class: FixpNegotiationReject Description: A server's refusal to create a session. The server sends nothing more and closes the transport.
--     * Slot: id
--     * Slot: session_id Description: The session's identifier, which the client chooses and never uses again.
--     * Slot: request_timestamp Description: The request_time of the Negotiate this message refuses.
--     * Slot: negotiation_reject_code Description: Why the server refused to create the session.
--     * Slot: reason_text Description: Free text that says more about the code beside it.
--     * Slot: message_kind Description: The class of this message, such as FixpNegotiate. It stands for FIXP's MessageType, which every message carries.
-- # Class: FixpTopic Description: A multicast publisher's notice that starts a flow and ties the session's short-lived identifier to a lasting subject. It is repeated so that late listeners can join.
--     * Slot: id
--     * Slot: session_id Description: The session's identifier, which the client chooses and never uses again.
--     * Slot: flow Description: The flow type of a multicast topic's messages.
--     * Slot: keepalive_interval Description: The publisher's heartbeat interval, in milliseconds.
--     * Slot: topic_classification Description: The lasting subject of a topic's messages, such as a product type or a market symbol.
--     * Slot: message_kind Description: The class of this message, such as FixpNegotiate. It stands for FIXP's MessageType, which every message carries.
-- # Class: FixpEstablish Description: A client's request to tie a negotiated session to the very transport this message arrives on. After a disconnection it is sent again to re-bind.
--     * Slot: id
--     * Slot: session_id Description: The session's identifier, which the client chooses and never uses again.
--     * Slot: request_time Description: When the sender made this request. The answer repeats it, to show what it answers.
--     * Slot: keepalive_interval Description: The longest the client stays silent, in milliseconds, before a heartbeat.
--     * Slot: next_seq_no Description: When the client's recoverable flow is bound again, the number its next application message will carry.
--     * Slot: credentials Description: Data that identifies the client, in a form the two parties agree on.
--     * Slot: message_kind Description: The class of this message, such as FixpNegotiate. It stands for FIXP's MessageType, which every message carries.
-- # Class: FixpEstablishmentAck Description: A server's acceptance of the binding. From here, application messages may flow.
--     * Slot: id
--     * Slot: session_id Description: The session's identifier, which the client chooses and never uses again.
--     * Slot: request_timestamp Description: The request_time of the Establish this message accepts.
--     * Slot: keepalive_interval Description: The longest the server stays silent, in milliseconds, before a heartbeat.
--     * Slot: next_seq_no Description: If the server's flow is recoverable, the number its next application message will carry, so the client can ask for what it missed.
--     * Slot: message_kind Description: The class of this message, such as FixpNegotiate. It stands for FIXP's MessageType, which every message carries.
-- # Class: FixpEstablishmentReject Description: A server's refusal of the binding.
--     * Slot: id
--     * Slot: session_id Description: The session's identifier, which the client chooses and never uses again.
--     * Slot: request_timestamp Description: The request_time of the Establish this message refuses.
--     * Slot: establishment_reject_code Description: Why the server refused to bind the session.
--     * Slot: reason_text Description: Free text that says more about the code beside it.
--     * Slot: message_kind Description: The class of this message, such as FixpNegotiate. It stands for FIXP's MessageType, which every message carries.
-- # Class: FixpSequence Description: Starts the numbering of a sequenced flow, so that the application messages after it are numbered by counting up from the value it carries. Sent when idle, it is also the heartbeat.
--     * Slot: id
--     * Slot: next_seq_no Description: The number the sender's next application message will carry.
--     * Slot: message_kind Description: The class of this message, such as FixpNegotiate. It stands for FIXP's MessageType, which every message carries.
-- # Class: FixpContext Description: On a transport that several sessions share, names the session the following messages belong to and, when the flow is sequenced, where its numbering continues.
--     * Slot: id
--     * Slot: session_id Description: The session's identifier, which the client chooses and never uses again.
--     * Slot: next_seq_no Description: The number the sender's next application message will carry.
--     * Slot: message_kind Description: The class of this message, such as FixpNegotiate. It stands for FIXP's MessageType, which every message carries.
-- # Class: FixpUnsequencedHeartbeat Description: Shows the peer that the session and transport are alive when the sender's flow is unsequenced or empty. It has no fields.
--     * Slot: id
--     * Slot: message_kind Description: The class of this message, such as FixpNegotiate. It stands for FIXP's MessageType, which every message carries.
-- # Class: FixpRetransmitRequest Description: Asks the peer to resend some messages of its recoverable flow. A party has at most one such request open at a time.
--     * Slot: id
--     * Slot: session_id Description: The session's identifier, which the client chooses and never uses again.
--     * Slot: request_time Description: When the request was made, which also tells this request apart from others.
--     * Slot: from_seq_no Description: Where the requested run starts, by sequence number.
--     * Slot: message_count Description: How many messages are asked for.
--     * Slot: message_kind Description: The class of this message, such as FixpNegotiate. It stands for FIXP's MessageType, which every message carries.
-- # Class: FixpRetransmission Description: Introduces a batch of resent messages, which are numbered by counting from the number it gives. A request may be answered in several batches.
--     * Slot: id
--     * Slot: session_id Description: The session's identifier, which the client chooses and never uses again.
--     * Slot: request_timestamp Description: The request_time of the RetransmitRequest this batch answers.
--     * Slot: next_seq_no Description: The number the batch's first message carries.
--     * Slot: message_count Description: How many resent messages the batch holds.
--     * Slot: message_kind Description: The class of this message, such as FixpNegotiate. It stands for FIXP's MessageType, which every message carries.
-- # Class: FixpRetransmitReject Description: Refuses a RetransmitRequest, with a code saying why.
--     * Slot: id
--     * Slot: session_id Description: The session's identifier, which the client chooses and never uses again.
--     * Slot: request_timestamp Description: The request_time of the RetransmitRequest this message refuses.
--     * Slot: retransmit_reject_code Description: Why the sender will not resend the range.
--     * Slot: reason_text Description: Free text that says more about the code beside it.
--     * Slot: message_kind Description: The class of this message, such as FixpNegotiate. It stands for FIXP's MessageType, which every message carries.
-- # Class: FixpTerminate Description: Releases the session from its transport without ending the session, which can be bound again later. The peer answers with a Terminate, and after its own Terminate a party sends nothing more.
--     * Slot: id
--     * Slot: session_id Description: The session's identifier, which the client chooses and never uses again.
--     * Slot: termination_code Description: Why the party releases the session from the transport.
--     * Slot: reason_text Description: Free text that says more about the code beside it.
--     * Slot: message_kind Description: The class of this message, such as FixpNegotiate. It stands for FIXP's MessageType, which every message carries.
-- # Class: FixpFinishedSending Description: Says that the sender's flow has carried its last application message, which begins finalization. It is repeated as the heartbeat until the answer comes.
--     * Slot: id
--     * Slot: session_id Description: The session's identifier, which the client chooses and never uses again.
--     * Slot: last_seq_no Description: The number carried by the flow's final application message.
--     * Slot: message_kind Description: The class of this message, such as FixpNegotiate. It stands for FIXP's MessageType, which every message carries.
-- # Class: FixpFinishedReceiving Description: Answers FinishedSending once the last message of the peer's flow has been processed. After it the session is finalized and its identifier is spent.
--     * Slot: id
--     * Slot: session_id Description: The session's identifier, which the client chooses and never uses again.
--     * Slot: message_kind Description: The class of this message, such as FixpNegotiate. It stands for FIXP's MessageType, which every message carries.
-- # Class: FixpApplied Description: An optional application message telling the party that sends an idempotent flow which of its operations took effect, where no business message already says so.
--     * Slot: id
--     * Slot: from_seq_no Description: Where the run of operations that took effect starts.
--     * Slot: message_count Description: How many operations in a row took effect.
--     * Slot: message_kind Description: The class of this message, such as FixpNegotiate. It stands for FIXP's MessageType, which every message carries.
-- # Class: FixpNotApplied Description: An application message telling the party that sends an idempotent flow about a gap: a run of operations that did not take effect. That party's application decides what to do.
--     * Slot: id
--     * Slot: from_seq_no Description: Where the run of operations that failed to take effect starts.
--     * Slot: message_count Description: How many operations in a row did not take effect.
--     * Slot: message_kind Description: The class of this message, such as FixpNegotiate. It stands for FIXP's MessageType, which every message carries.
-- # Class: FixpMessageTemplate Description: Hands the peer a template or schema it needs to read messages in an encoding that templates drive. There is no fixed moment for sending it.
--     * Slot: id
--     * Slot: sofh_encoding_type Description: The code that the Simple Open Framing Header registers for the encoding a template is written for.
--     * Slot: effective_time Description: When the template comes into force. Without it, the template applies at once.
--     * Slot: template_version Description: The template's version and format, for an encoding whose templates do not state them.
--     * Slot: template Description: The template itself, as octets.
--     * Slot: message_kind Description: The class of this message, such as FixpNegotiate. It stands for FIXP's MessageType, which every message carries.
-- # Class: FixpExchange Description: The messages of one session in the order they were sent, as a test case, a worked example or a captured log.
--     * Slot: id Description: The identifier of an exchange or a rules-of-engagement record.
--     * Slot: description Description: Free text about a record, for the people who read it.
--     * Slot: session_kind Description: Which of the two forms the session takes.
--     * Slot: multiplexed Description: Whether the transport carries other sessions too, so that Context takes the place of Sequence.
-- # Class: FixpExchangeStep Description: One step: a FIXP message, or a run of application messages whose content FIXP does not define, and the side that sent it.
--     * Slot: id
--     * Slot: sent_by Description: The side that sent this step.
--     * Slot: application_message_count Description: How many application messages went out one after another. On a sequenced flow each takes the next sequence number.
--     * Slot: FixpExchange_id Description: Autocreated FK slot
--     * Slot: fixp_message_id Description: The FIXP message sent.
-- # Class: FixpRulesOfEngagement Description: What two counterparties agree on for one FIXP service, layer by layer, for the client and for the server.
--     * Slot: id Description: The identifier of an exchange or a rules-of-engagement record.
--     * Slot: description Description: Free text about a record, for the people who read it.
--     * Slot: client_stack_id Description: What the client side uses.
--     * Slot: server_stack_id Description: What the server side uses.
-- # Class: FixpStackProfile Description: One side's choices at each layer of the stack: application, presentation, session, security and transport.
--     * Slot: id
--     * Slot: application_recovery Description: Whether this side's applications recover lost messages themselves.
--     * Slot: application_fix_version Description: The FIX version of the application messages, such as FIX.Latest.
--     * Slot: service_pack Description: The FIX service pack, where the version has them.
--     * Slot: message_encoding Description: How messages are encoded, such as Simple Binary Encoding.
--     * Slot: encoding_version Description: The version of that encoding.
--     * Slot: framing Description: What marks where one message ends and the next begins, such as the Simple Open Framing Header.
--     * Slot: tls_version Description: The TLS version that protects the transport.
-- # Class: FixpStackProfile_extension_packs
--     * Slot: FixpStackProfile_id Description: Autocreated FK slot
--     * Slot: extension_packs Description: The FIX extension packs in use.
-- # Class: FixpStackProfile_message_schemas
--     * Slot: FixpStackProfile_id Description: Autocreated FK slot
--     * Slot: message_schemas Description: The message schemas or templates the encoding uses.
-- # Class: FixpStackProfile_supported_flow_types
--     * Slot: FixpStackProfile_id Description: Autocreated FK slot
--     * Slot: supported_flow_types Description: The flow types this side accepts or offers.
-- # Class: FixpStackProfile_authentication_methods
--     * Slot: FixpStackProfile_id Description: Autocreated FK slot
--     * Slot: authentication_methods Description: How the parties prove who they are.
-- # Class: FixpStackProfile_cipher_suites
--     * Slot: FixpStackProfile_id Description: Autocreated FK slot
--     * Slot: cipher_suites Description: The cipher suites allowed.
-- # Class: FixpStackProfile_transports
--     * Slot: FixpStackProfile_id Description: Autocreated FK slot
--     * Slot: transports Description: The transports this side can use, for example TCP, or UDP with multicast.
-- # Class: FixpStackProfile_network_protocols
--     * Slot: FixpStackProfile_id Description: Autocreated FK slot
--     * Slot: network_protocols Description: Any other network protocols in use.

CREATE TABLE "FixpMessage" (
	id INTEGER NOT NULL,
	message_kind TEXT NOT NULL,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_FixpMessage_id" ON "FixpMessage" (id);

CREATE TABLE "FixpNegotiate" (
	id INTEGER NOT NULL,
	session_id TEXT NOT NULL,
	request_time TEXT NOT NULL,
	client_flow VARCHAR(11) NOT NULL,
	credentials TEXT,
	message_kind TEXT NOT NULL,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_FixpNegotiate_id" ON "FixpNegotiate" (id);

CREATE TABLE "FixpNegotiationResponse" (
	id INTEGER NOT NULL,
	session_id TEXT NOT NULL,
	request_timestamp TEXT NOT NULL,
	server_flow VARCHAR(11) NOT NULL,
	credentials TEXT,
	message_kind TEXT NOT NULL,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_FixpNegotiationResponse_id" ON "FixpNegotiationResponse" (id);

CREATE TABLE "FixpNegotiationReject" (
	id INTEGER NOT NULL,
	session_id TEXT NOT NULL,
	request_timestamp TEXT NOT NULL,
	negotiation_reject_code VARCHAR(20) NOT NULL,
	reason_text TEXT,
	message_kind TEXT NOT NULL,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_FixpNegotiationReject_id" ON "FixpNegotiationReject" (id);

CREATE TABLE "FixpTopic" (
	id INTEGER NOT NULL,
	session_id TEXT NOT NULL,
	flow VARCHAR(11) NOT NULL,
	keepalive_interval TEXT,
	topic_classification TEXT NOT NULL,
	message_kind TEXT NOT NULL,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_FixpTopic_id" ON "FixpTopic" (id);

CREATE TABLE "FixpEstablish" (
	id INTEGER NOT NULL,
	session_id TEXT NOT NULL,
	request_time TEXT NOT NULL,
	keepalive_interval TEXT NOT NULL,
	next_seq_no TEXT,
	credentials TEXT,
	message_kind TEXT NOT NULL,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_FixpEstablish_id" ON "FixpEstablish" (id);

CREATE TABLE "FixpEstablishmentAck" (
	id INTEGER NOT NULL,
	session_id TEXT NOT NULL,
	request_timestamp TEXT NOT NULL,
	keepalive_interval TEXT NOT NULL,
	next_seq_no TEXT,
	message_kind TEXT NOT NULL,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_FixpEstablishmentAck_id" ON "FixpEstablishmentAck" (id);

CREATE TABLE "FixpEstablishmentReject" (
	id INTEGER NOT NULL,
	session_id TEXT NOT NULL,
	request_timestamp TEXT NOT NULL,
	establishment_reject_code VARCHAR(18) NOT NULL,
	reason_text TEXT,
	message_kind TEXT NOT NULL,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_FixpEstablishmentReject_id" ON "FixpEstablishmentReject" (id);

CREATE TABLE "FixpSequence" (
	id INTEGER NOT NULL,
	next_seq_no TEXT NOT NULL,
	message_kind TEXT NOT NULL,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_FixpSequence_id" ON "FixpSequence" (id);

CREATE TABLE "FixpContext" (
	id INTEGER NOT NULL,
	session_id TEXT NOT NULL,
	next_seq_no TEXT,
	message_kind TEXT NOT NULL,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_FixpContext_id" ON "FixpContext" (id);

CREATE TABLE "FixpUnsequencedHeartbeat" (
	id INTEGER NOT NULL,
	message_kind TEXT NOT NULL,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_FixpUnsequencedHeartbeat_id" ON "FixpUnsequencedHeartbeat" (id);

CREATE TABLE "FixpRetransmitRequest" (
	id INTEGER NOT NULL,
	session_id TEXT NOT NULL,
	request_time TEXT NOT NULL,
	from_seq_no TEXT NOT NULL,
	message_count TEXT NOT NULL,
	message_kind TEXT NOT NULL,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_FixpRetransmitRequest_id" ON "FixpRetransmitRequest" (id);

CREATE TABLE "FixpRetransmission" (
	id INTEGER NOT NULL,
	session_id TEXT NOT NULL,
	request_timestamp TEXT NOT NULL,
	next_seq_no TEXT NOT NULL,
	message_count TEXT NOT NULL,
	message_kind TEXT NOT NULL,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_FixpRetransmission_id" ON "FixpRetransmission" (id);

CREATE TABLE "FixpRetransmitReject" (
	id INTEGER NOT NULL,
	session_id TEXT NOT NULL,
	request_timestamp TEXT NOT NULL,
	retransmit_reject_code VARCHAR(20) NOT NULL,
	reason_text TEXT,
	message_kind TEXT NOT NULL,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_FixpRetransmitReject_id" ON "FixpRetransmitReject" (id);

CREATE TABLE "FixpTerminate" (
	id INTEGER NOT NULL,
	session_id TEXT NOT NULL,
	termination_code VARCHAR(20) NOT NULL,
	reason_text TEXT,
	message_kind TEXT NOT NULL,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_FixpTerminate_id" ON "FixpTerminate" (id);

CREATE TABLE "FixpFinishedSending" (
	id INTEGER NOT NULL,
	session_id TEXT NOT NULL,
	last_seq_no TEXT,
	message_kind TEXT NOT NULL,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_FixpFinishedSending_id" ON "FixpFinishedSending" (id);

CREATE TABLE "FixpFinishedReceiving" (
	id INTEGER NOT NULL,
	session_id TEXT NOT NULL,
	message_kind TEXT NOT NULL,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_FixpFinishedReceiving_id" ON "FixpFinishedReceiving" (id);

CREATE TABLE "FixpApplied" (
	id INTEGER NOT NULL,
	from_seq_no TEXT NOT NULL,
	message_count TEXT NOT NULL,
	message_kind TEXT NOT NULL,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_FixpApplied_id" ON "FixpApplied" (id);

CREATE TABLE "FixpNotApplied" (
	id INTEGER NOT NULL,
	from_seq_no TEXT NOT NULL,
	message_count TEXT NOT NULL,
	message_kind TEXT NOT NULL,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_FixpNotApplied_id" ON "FixpNotApplied" (id);

CREATE TABLE "FixpMessageTemplate" (
	id INTEGER NOT NULL,
	sofh_encoding_type TEXT NOT NULL,
	effective_time TEXT,
	template_version TEXT,
	template TEXT NOT NULL,
	message_kind TEXT NOT NULL,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_FixpMessageTemplate_id" ON "FixpMessageTemplate" (id);

CREATE TABLE "FixpExchange" (
	id TEXT NOT NULL,
	description TEXT,
	session_kind VARCHAR(14) NOT NULL,
	multiplexed BOOLEAN,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_FixpExchange_id" ON "FixpExchange" (id);

CREATE TABLE "FixpStackProfile" (
	id INTEGER NOT NULL,
	application_recovery BOOLEAN,
	application_fix_version TEXT,
	service_pack TEXT,
	message_encoding TEXT,
	encoding_version TEXT,
	framing TEXT,
	tls_version TEXT,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_FixpStackProfile_id" ON "FixpStackProfile" (id);

CREATE TABLE "FixpExchangeStep" (
	id INTEGER NOT NULL,
	sent_by VARCHAR(9) NOT NULL,
	application_message_count TEXT,
	"FixpExchange_id" TEXT,
	fixp_message_id INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY("FixpExchange_id") REFERENCES "FixpExchange" (id),
	FOREIGN KEY(fixp_message_id) REFERENCES "FixpMessage" (id)
);
CREATE INDEX "ix_FixpExchangeStep_id" ON "FixpExchangeStep" (id);

CREATE TABLE "FixpRulesOfEngagement" (
	id TEXT NOT NULL,
	description TEXT,
	client_stack_id INTEGER NOT NULL,
	server_stack_id INTEGER NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(client_stack_id) REFERENCES "FixpStackProfile" (id),
	FOREIGN KEY(server_stack_id) REFERENCES "FixpStackProfile" (id)
);
CREATE INDEX "ix_FixpRulesOfEngagement_id" ON "FixpRulesOfEngagement" (id);

CREATE TABLE "FixpStackProfile_extension_packs" (
	"FixpStackProfile_id" INTEGER,
	extension_packs TEXT,
	PRIMARY KEY ("FixpStackProfile_id", extension_packs),
	FOREIGN KEY("FixpStackProfile_id") REFERENCES "FixpStackProfile" (id)
);
CREATE INDEX "ix_FixpStackProfile_extension_packs_FixpStackProfile_id" ON "FixpStackProfile_extension_packs" ("FixpStackProfile_id");
CREATE INDEX "ix_FixpStackProfile_extension_packs_extension_packs" ON "FixpStackProfile_extension_packs" (extension_packs);

CREATE TABLE "FixpStackProfile_message_schemas" (
	"FixpStackProfile_id" INTEGER,
	message_schemas TEXT,
	PRIMARY KEY ("FixpStackProfile_id", message_schemas),
	FOREIGN KEY("FixpStackProfile_id") REFERENCES "FixpStackProfile" (id)
);
CREATE INDEX "ix_FixpStackProfile_message_schemas_message_schemas" ON "FixpStackProfile_message_schemas" (message_schemas);
CREATE INDEX "ix_FixpStackProfile_message_schemas_FixpStackProfile_id" ON "FixpStackProfile_message_schemas" ("FixpStackProfile_id");

CREATE TABLE "FixpStackProfile_supported_flow_types" (
	"FixpStackProfile_id" INTEGER,
	supported_flow_types VARCHAR(11),
	PRIMARY KEY ("FixpStackProfile_id", supported_flow_types),
	FOREIGN KEY("FixpStackProfile_id") REFERENCES "FixpStackProfile" (id)
);
CREATE INDEX "ix_FixpStackProfile_supported_flow_types_supported_flow_types" ON "FixpStackProfile_supported_flow_types" (supported_flow_types);
CREATE INDEX "ix_FixpStackProfile_supported_flow_types_FixpStackProfile_id" ON "FixpStackProfile_supported_flow_types" ("FixpStackProfile_id");

CREATE TABLE "FixpStackProfile_authentication_methods" (
	"FixpStackProfile_id" INTEGER,
	authentication_methods TEXT,
	PRIMARY KEY ("FixpStackProfile_id", authentication_methods),
	FOREIGN KEY("FixpStackProfile_id") REFERENCES "FixpStackProfile" (id)
);
CREATE INDEX "ix_FixpStackProfile_authentication_methods_FixpStackProfile_id" ON "FixpStackProfile_authentication_methods" ("FixpStackProfile_id");
CREATE INDEX "ix_FixpStackProfile_authentication_methods_authentication_methods" ON "FixpStackProfile_authentication_methods" (authentication_methods);

CREATE TABLE "FixpStackProfile_cipher_suites" (
	"FixpStackProfile_id" INTEGER,
	cipher_suites TEXT,
	PRIMARY KEY ("FixpStackProfile_id", cipher_suites),
	FOREIGN KEY("FixpStackProfile_id") REFERENCES "FixpStackProfile" (id)
);
CREATE INDEX "ix_FixpStackProfile_cipher_suites_cipher_suites" ON "FixpStackProfile_cipher_suites" (cipher_suites);
CREATE INDEX "ix_FixpStackProfile_cipher_suites_FixpStackProfile_id" ON "FixpStackProfile_cipher_suites" ("FixpStackProfile_id");

CREATE TABLE "FixpStackProfile_transports" (
	"FixpStackProfile_id" INTEGER,
	transports TEXT,
	PRIMARY KEY ("FixpStackProfile_id", transports),
	FOREIGN KEY("FixpStackProfile_id") REFERENCES "FixpStackProfile" (id)
);
CREATE INDEX "ix_FixpStackProfile_transports_transports" ON "FixpStackProfile_transports" (transports);
CREATE INDEX "ix_FixpStackProfile_transports_FixpStackProfile_id" ON "FixpStackProfile_transports" ("FixpStackProfile_id");

CREATE TABLE "FixpStackProfile_network_protocols" (
	"FixpStackProfile_id" INTEGER,
	network_protocols TEXT,
	PRIMARY KEY ("FixpStackProfile_id", network_protocols),
	FOREIGN KEY("FixpStackProfile_id") REFERENCES "FixpStackProfile" (id)
);
CREATE INDEX "ix_FixpStackProfile_network_protocols_network_protocols" ON "FixpStackProfile_network_protocols" (network_protocols);
CREATE INDEX "ix_FixpStackProfile_network_protocols_FixpStackProfile_id" ON "FixpStackProfile_network_protocols" ("FixpStackProfile_id");
