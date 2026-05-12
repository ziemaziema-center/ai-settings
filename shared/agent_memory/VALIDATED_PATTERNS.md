# Validated Patterns

## ROLE
This file stores reusable execution patterns that have been validated in the workspace.

## CONTEXT
Use it to standardize recurring agent behavior for safe patching, debugging, content generation, and reports.

## TASK
Add patterns using this format:

```text
## Pattern Name
- applies_to:
- procedure:
- validation:
- rollback:
- evidence:
```

## CONSTRAINTS
- Only include patterns that have validation evidence.
- Keep patterns generic enough to reuse.
- Include rollback behavior for every pattern.

## Pattern: Additive Structured File Generation
- applies_to: New prompt, rule, template, and memory files.
- procedure: Create target directories, add files without moving existing content, validate required files and headings.
- validation: Confirm file existence and required section markers.
- rollback: Delete generated files or restore backups for any modified existing files.
- evidence: File existence and required marker validation performed on 2026-05-08; literal `[RESULT]` markers added where validation found omissions.

## RESULT FORMAT
```text
[RESULT]
- backup_path:
- files_modified:
- validation_result:
- side_effects:
- rollback_needed:
- next_action:
```

## Pattern: Lightweight Execution Memory Accumulation
- memory-key: validated-memory-accumulation-v1
- applies_to: Recurring failures, validated successful fixes, and operational patch records.
- procedure: Search for an existing memory key or matching title, append only if absent, keep the summary concise, and include root cause plus fix pattern.
- validation: Confirm target files exist, appended sections contain unique memory-key values, and no existing Markdown content was removed.
- rollback: Restore the timestamped backups from _backups/memory_accumulation_* if the append is rejected.
- root_cause: Operational lessons decay when they are not externalized into shared memory files.
- fix_pattern: Use append-only timestamped Markdown entries in KNOWN_FAILURES.md, VALIDATED_PATTERNS.md, and PATCH_HISTORY.md.
- evidence: Added through a duplicate-aware append script on 2026-05-08 12:04 +09:00ST.

