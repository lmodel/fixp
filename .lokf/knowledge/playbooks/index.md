# Playbooks

* [Regenerate and test](regenerate-and-test.md) - How to change the schema: edit a module under `src/fixp/schema/`, run `just lint`, `just gen-project`, `just gen-doc`, `just lokf-adapt` and `just test`, and commit what they write.
* [Cut a release](release.md) - How a release happens: write `## [Unreleased]`, merge with a releasing commit type, and `semantic-release.yml` tags, writes the changelog and dispatches the knowledge release, which attaches the assets.
* [Update the upstream pins](update-upstream-pins.md) - What to do when the watch reports a change in FIX's FIXP repository: read what changed, replace `upstream/`, the pins and the headers together, and let the coverage test show what the schema must follow.
* [Validate a message or an exchange](validate-a-message.md) - How to check a FIXP message or a run of messages against the schema: `linkml-validate` with the message's class, such as `FixpNegotiate`, or with `FixpExchange`, and the JSON Schema in `project/` for anyone without LinkML.
* [Knowledge sources map](knowledge-sources.md) - The librarian's scrape map: every repository location and external source this bundle derives concepts from, how to re-check each, and the tracked paths left out with their reasons.
