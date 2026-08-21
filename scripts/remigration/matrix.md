# Re-Migration Matrix - Summary

Total page ids compared: **799**

| Status | Count |
|---|---|
| MIGRATED_CORRECTLY | 751 |
| INTENTIONALLY_ADDED | 46 |
| REVIEWED_OK | 2 |

## Flagged pages requiring review (0)

## Manually reviewed - confirmed non-issues (2)

### `extnsbackup/introduction`
- RST 'Features' table is a degenerate single-column grid table; Mintlify converts it to a bullet list with identical content - no data lost.

### `history`
- docs/docs/history.rst only does '.. include:: ../HISTORY.rst', which does not exist in the source tree. The live site's /history.html also renders with <no title> and an empty body (verified via live fetch) - this page is empty on the live site too, so there is nothing to migrate.
