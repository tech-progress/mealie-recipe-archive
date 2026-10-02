# Deploy and Host Mealie recipe archive on Railway

Archive imported recipes, retained images, and portable backups

## About hosting

A single-node recipe archive with SQLite, controlled schema.org recipe import, retained original/derived images and native portable ZIP backups. No AI provider, PostgreSQL, SMTP, LDAP, OIDC, FlareSolverr or Chromium sidecar. Import only sources you are entitled to archive.

## What gets deployed

One app volume at `/app/data`, 5 GB initial size, attached only to that service. One replica; a mounted volume does not imply HA. The directory includes `mealie.db`, recipes/images/assets, backups, `.secret` and `.session_secret`. A native backup is not a complete session-state archive.

## Operational contract

Signups are disabled. Before listening, the version-bound bootstrap calls upstream migrations/initialization and replaces only an untouched `changeme@example.com` / `MyPassword` administrator, using the upstream password hasher. Existing accounts and restored passwords are not overwritten. Set the admin email before first boot. Upstream recipe media is otherwise public by known ID: `template_app.py` adds native cookie/Bearer authentication and same-group authorization to recipe images/assets and user avatars. Keep this wrapper; bypassing it exposes upstream media routes. Public recipe/asset sharing is deliberately outside this private archive contract. **Groups, not households, are the media isolation boundary**; households in the same group are collaborators, not hostile tenants.

Set a real admin identity before first boot, store generated passwords securely, keep only the app public, and retain encrypted off-volume backups. Follow README.md for variables, source settings, URLs and restore procedures. This is a single-node template, not an HA architecture. Railway plans/volume limits and application workload determine suitability.

**Unpublished:** no template ID/code or deployment URL is assigned. Source authorization, root metadata sync/audit and approved Railway qualification must pass before offering a deploy button.

## Main upstream products

- [Mealie](https://mealie.io/)
- [Mealie source](https://github.com/mealie-recipes/mealie)
