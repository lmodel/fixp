---
type: Service
id: https://w3id.org/lmodel/fixp/knowledge/services/documentation-site
genre: reference
title: Documentation site
description: The knowledge website in `website/`, an Astro Starlight site that the Knowledge website workflow publishes to GitHub Pages at `https://lmodel.github.io/fixp`, built from the README, `docs/`, the schema's pages and this bundle.
resource: website
sources:
  - id: site.config.mjs
    resource: website/site.config.mjs
    title: REPO, SITE, BASE and REDIRECTS
  - id: website-readme.md
    resource: website/README.md
generated:
  by: process:ktl-librarian
  at: "2026-11-06T08:48:23Z"
status: draft
---

# Documentation site

The site replaces the mkdocs site. Its options redirect the old pages, `/about` and `/elements`, to the new ones, and each old schema page to the page of the same name. A class the schema renamed has no such page.[^site.config.mjs]

`website/README.md` says how to build it.[^website-readme.md]

[^site.config.mjs]: website/site.config.mjs, REPO, SITE, BASE and REDIRECTS
[^website-readme.md]: website/README.md
