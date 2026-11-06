# Change Log

## 2026-11-06

* **Changed**: `lokf.yaml` and `fixp.yaml` moved into `.lokf/schema/`, where KTL v0.62.0 keeps a sidecar's schema files, and the concepts that name them follow.
* **Changed**: the licence page says FIX also publishes the SBE schema under the Apache License 2.0.
* **Changed**: the page on what the model leaves out says where a firm's own text goes.
* **Changed**: the engagement module's page names the credentials' form, the keep-alive range and the resend limit a stack profile now holds.
* **Changed**: fix-sbe, fix-orchestra and fix-protocol have released, so their copies are pinned beside the others and the mapping checks no longer skip.
* **Changed**: the rules page counts twenty-two rules, and says steps the specification allows break none of them.
* **Changed**: no concept pins a commit any more. A rebase had left every pin naming a commit GitHub does not hold, and the branch will be squash-merged.
* **Prose**: reworded 8 concept bodies in plain English. No fact, link, number or frontmatter changed.
* **Changed**: What FIX's files show no longer says the faults were reported; docs/about.md now says the project leaves them as they are.
* **Added**: Knowledge sources map, with the bundle's other first concepts, derived from the repository by a bootstrap pass.

## 2026-11-05

* **Initialization**: Scaffolded the LOKF bundle for fixp. Real concepts to follow.
