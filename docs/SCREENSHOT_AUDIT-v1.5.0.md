# Screenshot audit — v1.5.0

This audit is intentionally non-destructive. Existing versioned screenshots are
retained until every documentation reference has been migrated.

| Directory | Status | Action |
| --- | --- | --- |
| `assets/screenshots/v1.4.2/` | Current real Qt captures | Retain until v1.5.0 captures pass review |
| historical versioned images | May still be referenced by release documentation | Retain; do not delete by filename alone |
| `assets/screenshots/archive/` | Not yet created | Use only after reference analysis |

The v1.5.0 screenshot generator must create privacy-safe captures from a real
Qt window and verify non-empty PNG dimensions before README links are updated.
