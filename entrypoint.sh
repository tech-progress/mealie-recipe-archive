#!/bin/bash
set -euo pipefail
: "${MEALIE_ADMIN_EMAIL:?Set MEALIE_ADMIN_EMAIL}" "${MEALIE_ADMIN_PASSWORD:?Set MEALIE_ADMIN_PASSWORD}"
[[ ${#MEALIE_ADMIN_PASSWORD} -ge 16 ]] || exit 64
export API_PORT=9000 ALLOW_SIGNUP=false DATA_DIR=/app/data
mkdir -p /app/data
chown -R "${PUID:-911}:${PGID:-911}" /app/data
cd /app
gosu "${PUID:-911}:${PGID:-911}" /opt/mealie/bin/python /template-bootstrap.py
exec gosu "${PUID:-911}:${PGID:-911}" /opt/mealie/bin/python /app/template_app.py
