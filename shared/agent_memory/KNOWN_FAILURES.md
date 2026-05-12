# Known Failures

## ROLE
This file records recurring operational failures so future agents can avoid rediscovering them.

## CONTEXT
Append to this file when a task fails, a validation check exposes a repeatable issue, or a rollback is needed.

## TASK
Use this entry format:

```text
## YYYY-MM-DD - Failure Title
- symptom:
- cause:
- affected_files:
- detection_method:
- prevention:
- rollback_or_fix:
```

## CONSTRAINTS
- Keep entries factual.
- Include exact symptoms and validation commands when available.
- Do not store secrets, tokens, or private credentials.
- Prefer append-only updates.

## Initial Baseline
- No known project-specific failures recorded yet.

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

## 2026-05-08 12:04 +09:00ST - Memory Accumulation Rule: Recurring Failure Auto-Capture
- memory-key: recurring-failure-auto-capture-v1
- trigger: Append a new failure entry when the same symptom, validation failure, rollback event, or operational mistake appears more than once.
- duplicate_check: Before appending, search this file for the same symptom plus cause; skip if already recorded.
- root_cause: Failures were previously easy to lose when they stayed only in chat context or one-off execution reports.
- fix_pattern: Write concise Markdown entries with symptom, cause, ffected_files, detection_method, prevention, and ollback_or_fix.
- append_rule: Add only new timestamped entries; never rewrite older failure records.

