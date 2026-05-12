# Execution Log Schema

## ROLE
This file defines the lightweight telemetry format for HQ execution logs.

## CONTEXT
Use this structure for patch, debug, prompt, documentation, automation, validation, and rollback records.

## TASK CATEGORY
- analysis
- safe_patch
- debug
- generation
- prompt_update
- documentation
- validation
- rollback

## REQUIRED ENTRY
`	ext
## YYYY-MM-DD HH:mm KST - Task Title
- memory-key:
- task_category:
- scope:
- files_touched:
- failure_pattern:
- success_pattern:
- validation_outcome:
- side_effects:
- rollback_needed:
- next_action:
`

## MEMORY-KEY SUPPORT
- Use stable memory-key values for duplicate prevention.
- Format: 	elemetry-<category>-<short-slug>-v1.
- Reuse the same key only for the same recurring pattern.

## DUPLICATE PREVENTION
- Search DAILY_EXECUTION_LOG.md, FAILURE_TELEMETRY.md, and SUCCESS_TELEMETRY.md before appending.
- If the same memory-key already exists, skip the append.
- If the same symptom exists with a different key, update the new entry title for clarity but still append only.

## VALIDATION RULE
- Every entry must state alidation_outcome.
- Use 
ot_run_with_reason when validation is impossible.

## RESULT
`	ext
[RESULT]
- backup_path:
- files_modified:
- validation_result:
- side_effects:
- rollback_needed:
- next_action:
`
"@
    "DAILY_EXECUTION_LOG.md" = @"
# Daily Execution Log

## ROLE
Human-readable daily execution ledger for HQ work.

## CONTEXT
Append concise timestamped entries after execution tasks. Keep this file operational, not narrative.

## ENTRY TEMPLATE
`	ext
## YYYY-MM-DD HH:mm KST - Task Title
- memory-key:
- task_category:
- request:
- exact_scope:
- files_created:
- files_modified:
- backups_created:
- validation_outcome:
- side_effects:
- rollback_needed:
- next_action:
`

## INITIAL ENTRY
## 2026-05-08 12:11 +09:00ST - Execution Telemetry Structure Created
- memory-key: telemetry-generation-execution-log-structure-v1
- task_category: generation
- request: Create reusable execution log structure.
- exact_scope: shared_system/execution_logs/
- files_created: EXECUTION_LOG_SCHEMA.md, DAILY_EXECUTION_LOG.md, FAILURE_TELEMETRY.md, SUCCESS_TELEMETRY.md
- files_modified: none
- backups_created: not_required_new_files_only
- validation_outcome: pending_final_file_validation
- side_effects: additive Markdown files only
- rollback_needed: no
- next_action: Use this log after future patch/debug/execution tasks.

## DUPLICATE PREVENTION
- Before adding an entry, search for the proposed memory-key.
- Skip duplicate entries and record the skip in the final result.

---

## POST-TASK TELEMETRY RULE
- memory-key: post-task-telemetry-rule-v1
- telemetry-key: post-task-telemetry-rule-v1
- added: 2026-05-08 12:18 +09:00ST

After every patch, debug, execution, prompt update, documentation change, validation run, or rollback task, append one concise result entry to:

- shared_system/execution_logs/DAILY_EXECUTION_LOG.md

When applicable, also append:

- recurring failures -> shared_system/execution_logs/FAILURE_TELEMETRY.md
- reusable successful patterns -> shared_system/execution_logs/SUCCESS_TELEMETRY.md
- durable failure patterns -> shared_system/agent_memory/KNOWN_FAILURES.md
- durable validated patterns -> shared_system/agent_memory/VALIDATED_PATTERNS.md
- patch history -> shared_system/agent_memory/PATCH_HISTORY.md

Required telemetry fields:

- timestamp
- memory-key
- 	elemetry-key
- task_category
- exact_scope
- files_touched
- validation_outcome
- failure_pattern or 
one
- success_pattern or 
one
- rollback_needed
- next_action

Duplicate guard:

- Before appending telemetry or memory, search the target file for the same memory-key or 	elemetry-key.
- If the key exists, skip the append and record duplicate_entries_skipped.
- If the key is new but the same symptom/root cause or success pattern already exists, reuse the existing key or skip the duplicate.
- Append only. Do not rewrite, reorder, or delete existing telemetry or memory entries.
