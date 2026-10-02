# Deploy and Host Mealie recipe archive on Railway

Archive imported recipes, retained images, and portable backups

## About Hosting Mealie

A single-node recipe archive with SQLite, controlled schema.org recipe import, retained original/derived images and native portable ZIP backups. No AI provider, PostgreSQL, SMTP, LDAP, OIDC, FlareSolverr or Chromium sidecar. Import only sources you are entitled to archive.

## What gets deployed

One app volume at `/app/data`, 5 GB initial size, attached only to that service. One replica; a mounted volume does not imply HA. The directory includes `mealie.db`, recipes/images/assets, backups, `.secret` and `.session_secret`. A native backup is not a complete session-state archive.

## Operational contract

Signups are disabled. Before listening, the version-bound bootstrap calls upstream migrations/initialization and replaces only an untouched `changeme@example.com` / `MyPassword` administrator, using the upstream password hasher. Existing accounts and restored passwords are not overwritten. Set the admin email before first boot. Upstream recipe media is otherwise public by known ID: `template_app.py` adds native cookie/Bearer authentication and same-group authorization to recipe images/assets and user avatars. Keep this wrapper; bypassing it exposes upstream media routes. Public recipe/asset sharing is deliberately outside this private archive contract. **Groups, not households, are the media isolation boundary**; households in the same group are collaborators, not hostile tenants.

Set a real admin identity before first boot, store generated passwords securely, keep only the app public, and retain encrypted off-volume backups. Follow README.md for variables, source settings, URLs and restore procedures. This is a single-node template, not an HA architecture. Railway plans/volume limits and application workload determine suitability.

Native online ZIP restoration requires an application restart before restored login/access validation; active browser sessions are not a portable-backup guarantee. Restore on the same pinned upstream version and keep other writers disconnected.

## Why Deploy Mealie on Railway

Keep an authenticated recipe archive with retained media on one persistent volume. The recipe adds group-aware media authorization and preserves original owner credentials across restart and native backup restoration. This is a private archive, not a publicly shared recipe gallery or an HA service.

## Common Use Cases

- Archive permitted schema.org recipe content and your own recipe images.
- Organize collaborating households within a group while isolating other groups.
- Export native ZIP backups off-volume and restore to an empty replacement installation.

## Dependencies for Mealie

### Deployment Dependencies

The pinned Mealie application includes SQLite and uses one 5 GB Railway volume at `/app/data`. No external SMTP, AI service or paid provider is required. Choose a Railway plan with enough memory and storage, set the administrator email before initial boot, and protect the generated password and off-volume backups. Only port 9000 receives a public HTTPS domain. Source and license notices remain available at `/api/template-source`.

## Main upstream products

- [Mealie](https://mealie.io/)
- [Mealie source](https://github.com/mealie-recipes/mealie)
