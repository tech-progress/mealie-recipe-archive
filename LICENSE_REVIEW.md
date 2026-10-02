# License review — 2026-10-02

## Owner-approved recipe license

On October 2, 2026 the owner explicitly approved MIT for newly authored recipe, wrapper and application code. `LICENSE` records that scoped grant. It does not relicense any upstream artifact or waive upstream copyleft, notices, corresponding-source or commercial-license obligations. Source-recipe publication and binary redistribution are distinct reviews.

Main product: Mealie v3.28.0. Inspected primary tagged source and license, not a marketplace summary:

- Source: https://github.com/mealie-recipes/mealie/tree/v3.28.0
- License: https://github.com/mealie-recipes/mealie/blob/v3.28.0/LICENSE
- Declared license: **AGPL-3.0-only**. Original text retained in LICENSE.upstream.

Official upstream images are pinned by manifest digest; wrapper source is included here. Preserve upstream notices and dependency licenses when redistributing images. Do not assume a product logo license grants trademark endorsement.

This recipe modifies runtime behavior through an authentication middleware and version-bound offline bootstrap. Before publishing a modified AGPL service/image, provide corresponding source (including this wrapper and build instructions) to network users, preserve notices, choose a compatible license for these additions, and review transitive dependency obligations. Link the exact upstream tag rather than merely the vendor homepage.

This is an engineering review, not legal advice or certification. A full transitive image/SBOM redistribution review remains a publication gate. No product source, image or template was published remotely.
