# SESSION_BOOT.md

## HIGH PRIORITY
This file is mandatory session startup control for HQ.

Before any patch, debug, execution, workflow edit, prompt edit, or operational change: read memory first. No exceptions.

## STARTUP CHECKLIST
1. Read required memory files.
2. Identify exact task scope.
3. Confirm additive-only path.
4. Back up before modifying existing files.
5. Validate before reporting success.

## REQUIRED MEMORY READS
- `shared_system/agent_memory/KNOWN_FAILURES.md`
- `shared_system/agent_memory/VALIDATED_PATTERNS.md`
- `shared_system/agent_memory/PATCH_HISTORY.md`

## EXECUTION RULES
- Memory-first.
- Backup-first.
- Validation-first.
- Additive-only unless explicitly approved.
- Exact scope control: modify only named or directly required files.

## PROHIBITED BEHAVIORS
- Do not skip memory reads.
- Do not overwrite existing rules destructively.
- Do not modify production workflows unless explicitly requested.
- Do not broaden scope.
- Do not claim completion without validation.
- Do not append duplicate memory entries; use `memory-key` guards.

## REQUIRED RESULT REPORT
```text
[RESULT]
- backup_path:
- files_modified:
- validation_result:
- side_effects:
- rollback_needed:
- next_action:
```

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
