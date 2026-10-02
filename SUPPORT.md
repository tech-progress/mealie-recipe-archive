# Support and security boundary

A single-node recipe archive with SQLite, controlled schema.org recipe import, retained original/derived images and native portable ZIP backups. No AI provider, PostgreSQL, SMTP, LDAP, OIDC, FlareSolverr or Chromium sidecar. Import only sources you are entitled to archive.

Controlled JSON-LD import is tested, not arbitrary live website extraction, paywalls, JavaScript-heavy sources, remote image downloading or video transcription. Optional email/SSO/AI and hostile multi-tenant isolation are excluded. Same-group households intentionally share recipe access. The authentication/media wrapper is maintained by this template, not supported by Mealie upstream. No horizontal scaling or HA; monitor image/backup growth.

Signups are disabled. Before listening, the version-bound bootstrap calls upstream migrations/initialization and replaces only an untouched `changeme@example.com` / `MyPassword` administrator, using the upstream password hasher. Existing accounts and restored passwords are not overwritten. Set the admin email before first boot. Upstream recipe media is otherwise public by known ID: `template_app.py` adds native cookie/Bearer authentication and same-group authorization to recipe images/assets and user avatars. Keep this wrapper; bypassing it exposes upstream media routes. Public recipe/asset sharing is deliberately outside this private archive contract. **Groups, not households, are the media isolation boundary**; households in the same group are collaborators, not hostile tenants.

Operate one replica per durable service. Keep the app public only through Railway HTTPS; no backend public domains or TCP proxies. Do not add Docker sockets, cross-service filesystem assumptions, or unreviewed optional integrations. Treat private DNS as routing, not authentication. Monitor volume capacity and task failures; no backup retention service is included.

Report template bootstrap/wrapper/IaC bugs with upstream version and sanitized logs. Report product bugs to https://github.com/mealie-recipes/mealie; never attach credentials, volume archives, private recipes/notes/documents, SQL dumps or generated graph secrets. `.local/` contains sensitive test recovery artifacts. Generated administrator env values do not reset existing accounts.

## Account/data recovery

Use Admin → Backups to create/download a native ZIP, and separately retain a stopped-writer archive of all `/app/data` for exact recovery. ZIPs contain recipe data, images and `.secret`; they do not promise to preserve active browser sessions (`.session_secret`), and users should log in again. The smoke recreates an empty volume, runs pinned initialization followed by `BackupV2.restore`, and verifies recipe/image hashes and account access. Restore on the same upstream version first. Encrypt backups, retain them off-volume, and test them. For password recovery without configured SMTP, an existing admin can reset an account; do not assume signup or email reset works. Last-admin manual database repair remains an operator-only, unqualified procedure.

## Qualification status

The reproducible tests are `scripts/verify.sh` and `scripts/smoke.sh`; operational/cloud/publication qualification is separate. See the maintainer-only FINDINGS.md for exact evidence. Do not copy FINDINGS.md or `.local/` into a public standalone distribution.
