---
type: Policy
id: https://w3id.org/lmodel/fixp/knowledge/policies/security-policy
genre: reference
title: Security policy
description: How to report a vulnerability, what this repository releases, what executes here and what holds each surface. A report goes through GitHub's private vulnerability reporting, and only the latest release receives fixes.
resource: SECURITY.md
sources:
  - id: security
    resource: SECURITY.md
    title: Reporting a vulnerability, What this repository releases and Not covered
generated:
  by: process:ktl-librarian
  at: "2026-11-06T08:48:23Z"
status: draft
---

# Security policy

Use GitHub's private vulnerability reporting. Only the latest release receives fixes.[^security]

The files under `upstream/` are FIX's, and this repository treats them as data: tests read them with entity resolution and network access off, and nothing executes them.[^security]

Report a problem in FIXP itself to the FIX Trading Community.[^security]

[^security]: SECURITY.md, Reporting a vulnerability, What this repository releases and Not covered
