# Upgrade and rollback

Template SemVer describes services/variables/storage/authentication; upstream software versions are separate pins. The current contract is recorded in VERSION. Incompatible storage/auth/source changes require a new template major version.

Create a native portable backup and a stopped-writer complete data archive. Test a copy with the new pinned image, update bootstrap/model imports and private-media tests if upstream internals change, run migrations and the full smoke, then upgrade. Rollback needs the old image AND pre-migration data; downgrading the image alone is unsafe.

Before upgrading: stop ingestion/writes, retain encrypted off-volume backups and generated secrets, record image digests, and verify a restore to an isolated clean volume. Preserve one replica and all mount paths. After upgrading: run the full meaningful smoke, examine migration/worker logs, verify anonymous/cross-account denial and retained bytes, and audit the exported template contract. Do not use mutable `latest` tags or automated major updates.

For native online ZIP restoration, keep writers disconnected and restart the application immediately after import before validating the restored owner login, image bytes and group access. A successful import response alone is not a completed restore; upstream authentication may retain the replacement installation's signing settings until restart. Portable ZIPs do not promise active-session preservation.

For publication, create a new verified immutable version/tag and move the existing `release-v1` channel only for compatible changes. Downgrades without pre-migration snapshots are unsupported.
