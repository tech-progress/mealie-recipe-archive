# Mealie — Mealie recipe archive

Template contract **1.0.1**. Pinned upstream **v3.28.0**; image digests are in Dockerfile/Compose, independent of VERSION. Railway authoring dependency is exactly `railway@3.6.0`, with `bun.lock`.

## What this deploys

A single-node recipe archive with SQLite, controlled schema.org recipe import, retained original/derived images and native portable ZIP backups. No AI provider, PostgreSQL, SMTP, LDAP, OIDC, FlareSolverr or Chromium sidecar. Import only sources you are entitled to archive.

## Authentication and first boot

Signups are disabled. Before listening, the version-bound bootstrap calls upstream migrations/initialization and replaces only an untouched `changeme@example.com` / `MyPassword` administrator, using the upstream password hasher. Existing accounts and restored passwords are not overwritten. Set the admin email before first boot. Upstream recipe media is otherwise public by known ID: `template_app.py` adds native cookie/Bearer authentication and same-group authorization to recipe images/assets and user avatars. Keep this wrapper; bypassing it exposes upstream media routes. Public recipe/asset sharing is deliberately outside this private archive contract. **Groups, not households, are the media isolation boundary**; households in the same group are collaborators, not hostile tenants.

## Local use

Requirements: Docker Engine/Compose v2, Bash, OpenSSL, Python 3 standard library, jq and Bun. No Docker socket is mounted into any application. Commands run from this directory:

```sh
export MEALIE_ADMIN_PASSWORD="$(openssl rand -hex 16)"
export MEALIE_ADMIN_EMAIL=admin@example.invalid
export LOCAL_PORT=18550
bash scripts/build.sh
bash scripts/start.sh
# Open http://127.0.0.1:18550 and use the generated administrator.
# Preserve passwords in a password manager; shell variables are not a backup.
docker compose down                 # retains your data
```

`.env.example` documents operator inputs; use `.env` only locally and never commit it. Blank required secrets fail closed. `bash scripts/smoke.sh` generates its own credentials and unique Compose project, builds/starts with bounded waits, exercises real application work, restarts, restores into newly recreated volumes and cleans only its own project. It does not use your existing data. Use an unused LOCAL_PORT within 18500–18559. Runtime logs, recovery artifacts and evidence live in ignored `.local/`; backups there contain secrets/private content and must not be distributed.

## Railway source and networking

`.railway/railway.ts` requires an **actually accessible** `TEMPLATE_SOURCE_REPO` (`owner/repository`) and an **existing** slash-free `TEMPLATE_SOURCE_BRANCH`. The standalone distribution coordinates are `tech-progress/mealie-recipe-archive`, `release-v1`, and root `/`; use those three settings for the maintained release. Fork maintainers must change the repository, create their own release channel and authorize Railway's GitHub App. Set `TEMPLATE_SOURCE_ROOT_DIR` to `/mealie-recipe-archive` only for monorepo authoring. This becomes Railway's `source.rootDirectory`. Source accessibility/GitHub App authorization are checked separately from public visibility.

Install with `bun install --frozen-lockfile`; evaluate locally with `./node_modules/.bin/railway-iac-ts .railway/railway.ts` after supplying the three source settings. Only the app gets an HTTPS domain, targeting **9000**. Native login remains required. Private dependencies have no public domains or TCP proxies. Runtime listeners support Railway IPv6 private networking and local IPv4. Apply/audit the exported template's networking with the offline draft scripts before any authorized publication; see PUBLISHING.md. No paid or remote deployment is performed by verification scripts.

## Required and generated variables

All Railway values, generators and references are in `template-defaults.json`; descriptions in `template-descriptions.json`. Do not paste real secrets into those files. Local Compose uses the required names in `.env.example`; Railway uses generated secrets and references below. PORT values are fixed to the upstream target ports, not arbitrary redirect ports. SMTP, SSO and AI secrets are intentionally absent.

### Mealie

| Variable | Railway default | Meaning |
| --- | --- | --- |
| `PORT` | `9000` | PORT: pinned deployment setting; see README for scope and recovery requirements. |
| `API_PORT` | `9000` | API_PORT: pinned deployment setting; see README for scope and recovery requirements. |
| `DATA_DIR` | `/app/data` | DATA_DIR: pinned deployment setting; see README for scope and recovery requirements. |
| `DB_ENGINE` | `sqlite` | DB_ENGINE: pinned deployment setting; see README for scope and recovery requirements. |
| `ALLOW_SIGNUP` | `false` | ALLOW_SIGNUP: pinned deployment setting; see README for scope and recovery requirements. |
| `MEALIE_ADMIN_EMAIL` | `admin@example.invalid` | Initial administrator email. Change to your actual address before first deployment; no mail service is included. |
| `MEALIE_ADMIN_PASSWORD` | `Generated 32-character secret` | Generated password replacing the upstream default before listening; only seeds untouched default accounts. |
| `BASE_URL` | `https://${{Mealie.RAILWAY_PUBLIC_DOMAIN}}` | Canonical HTTPS public URL; update when adding a custom domain. |
| `PUID` | `911` | PUID: pinned deployment setting; see README for scope and recovery requirements. |
| `PGID` | `911` | PGID: pinned deployment setting; see README for scope and recovery requirements. |
| `TZ` | `UTC` | TZ: pinned deployment setting; see README for scope and recovery requirements. |

Canonical public URL variables must match your HTTPS domain, including any custom domain. Private DNS must not be replaced with localhost. Password/reference rotation requires coordinated server/client changes; resetting an environment variable is not account recovery. Keep generated settings with backups.

## Storage and recovery

One app volume at `/app/data`, 5 GB initial size, attached only to that service. One replica; a mounted volume does not imply HA. The directory includes `mealie.db`, recipes/images/assets, backups, `.secret` and `.session_secret`. A native backup is not a complete session-state archive.

Use Admin → Backups to create/download a native ZIP, and separately retain a stopped-writer archive of all `/app/data` for exact recovery. ZIPs contain recipe data, images and `.secret`; they do not promise to preserve active browser sessions (`.session_secret`), and users should log in again. The smoke recreates an empty volume, runs pinned initialization followed by `BackupV2.restore`, and verifies recipe/image hashes and account access. Restore on the same upstream version first. Encrypt backups, retain them off-volume, and test them. For password recovery without configured SMTP, an existing admin can reset an account; do not assume signup or email reset works. Last-admin manual database repair remains an operator-only, unqualified procedure.

## Verification and limits

`bash scripts/verify.sh` checks structure, version, JSON, dependency lock, Compose and offline IaC/draft contracts. `bash scripts/smoke.sh` is the destructive **isolated test** gate, not a production restoration command. See SUPPORT.md and UPGRADE.md.

Controlled JSON-LD import is tested, not arbitrary live website extraction, paywalls, JavaScript-heavy sources, remote image downloading or video transcription. Optional email/SSO/AI and hostile multi-tenant isolation are excluded. Same-group households intentionally share recipe access. The authentication/media wrapper is maintained by this template, not supported by Mealie upstream. No horizontal scaling or HA; monitor image/backup growth.

Local qualification does **not** complete marketplace publication. A maintainer must perform the root metadata synchronization/audit, a sanitized-source audit, source authorization, and an explicitly approved Railway validation/cleanup. Those gates are unrun in this implementation-only task.

## Main upstream products

- [Mealie](https://mealie.io/)
- [Mealie source](https://github.com/mealie-recipes/mealie)

Configuration/license reviewed at the pinned source: [v3.28.0](https://github.com/mealie-recipes/mealie/tree/v3.28.0), [AGPL-3.0-only license](https://github.com/mealie-recipes/mealie/blob/v3.28.0/LICENSE). LICENSE.upstream retains the tagged upstream license; LICENSE_REVIEW.md describes distribution obligations.
