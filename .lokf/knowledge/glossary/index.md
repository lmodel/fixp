# Glossary

* [Flow](flow.md) - Flow: the application messages one side of a FIXP session sends, in one direction. A session between two parties has two flows, and a multicast one.
* [Flow type](flow-type.md) - Flow type: the delivery guarantee of a flow. `FixpFlowType` lists the four, from Recoverable down to None, and a multicast topic takes only the first two.
* [Session](session.md) - Session: a FIXP dialog under one identifier, a version 4 UUID the client chooses and never uses again. It takes one of two forms, between two parties or multicast, and outlives the transport it is bound to.
* [Exchange](exchange.md) - Exchange: the messages of one session in the order they were sent, as a test case, a worked example or a captured log. `FixpExchange` is the schema's tree root.
* [Rules of engagement](rules-of-engagement.md) - Rules of engagement: what two counterparties agree on for a FIXP service at each layer of the stack, the checklist of the specification's appendix B. `FixpRulesOfEngagement` records it.
* [Adapt copy](adapt-copy.md) - Adapt copy: the copy of a schema that `lokf adapt` writes so that it can sit beside LOKF's, here `.lokf/schema/fixp.yaml`. Edit the source, never the copy.
