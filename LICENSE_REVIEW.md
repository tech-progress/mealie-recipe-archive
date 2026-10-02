# License review — 2026-10-02

## Owner-approved recipe license

On October 2, 2026 the owner explicitly approved MIT for newly authored recipe, wrapper and application code. `LICENSE` records that scoped grant. It does not relicense any upstream artifact or waive upstream copyleft, notices, corresponding-source or commercial-license obligations. Source-recipe publication and binary redistribution are distinct reviews.

Main product: Mealie v3.28.0. Inspected primary tagged source and license, not a marketplace summary:

- Source: https://github.com/mealie-recipes/mealie/tree/v3.28.0
- License: https://github.com/mealie-recipes/mealie/blob/v3.28.0/LICENSE
- Declared license: **AGPL-3.0-only**. Original text retained in LICENSE.upstream.

Official upstream images are pinned by manifest digest; wrapper source is included here. Preserve upstream notices and dependency licenses when redistributing images. Do not assume a product logo license grants trademark endorsement.

This recipe modifies runtime behavior through an authentication middleware and version-bound offline bootstrap. Before publishing a modified AGPL service/image, provide corresponding source (including this wrapper and build instructions) to network users, preserve notices, choose a compatible license for these additions, and review transitive dependency obligations. Link the exact upstream tag rather than merely the vendor homepage.

The public distribution contains source recipes, wrapper/build files and lockfiles, not upstream binaries, vendored dependency trees or image layers. The Dockerfile pulls the pinned upstream artifact without removing its component notices. `THIRD_PARTY_NOTICES.md` supplies exact application source, wrapper source and build references. The application offers those links through `/api/template-source` and an HTTP source-notice link. The MIT grant for new files remains compatible with, but does not replace, the upstream combined-work AGPL obligations.

An SPDX inventory of the pinned upstream image identified 480 package records, with 390 declared-license records and 90 missing declarations. Missing declarations included Debian packages, Python packages, executable launcher detections, gosu and the top-level image. These are scanner gaps, not a license grant. Debian copyright files, upstream application source/locks, Python package license metadata and gosu's upstream license are the appropriate provenance sources; retain them. `THIRD_PARTY_NOTICES.md` records those routes. No derived binary is published to a public registry by this recipe. Anyone independently redistributing a built binary must review its complete actual artifact and fulfill exact-version component source/notice duties; this source-recipe review is not blanket binary redistribution clearance.

This is an engineering provenance review, not legal advice or certification. Enterprise add-ons and third-party source content are not granted by this recipe.
