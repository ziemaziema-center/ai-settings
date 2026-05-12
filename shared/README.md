# Shared System

## ROLE
This folder is the shared execution standard layer for the HQ environment.

## CONTEXT
It centralizes reusable rules, prompts, templates, and agent memory without moving or replacing existing HQ instruction systems.

## TASK
Use these files as common references from root and provider-specific instruction files:

- `system_rules/`: structured execution and platform-specific rule patches.
- `agent_memory/`: durable operational memory and validated patterns.
- `templates/`: reusable patch, debug, content, and report formats.
- `prompts/`: Codex, Claude, and GPT execution prompts.

## CONSTRAINTS
- Additive only.
- Backup before modifying existing files.
- Preserve production workflows and user documents.
- Prefer minimal scope changes and rollback-aware execution.

## RESULT
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

## MEMORY-FIRST EXECUTION RULE
- memory-key: memory-first-execution-rule-v1
- added: 2026-05-08 12:06 +09:00ST

Before any patch, debug, execution, automation change, prompt change, or operational modification, read these shared memory files first:

1. shared_system/agent_memory/KNOWN_FAILURES.md
2. shared_system/agent_memory/VALIDATED_PATTERNS.md
3. shared_system/agent_memory/PATCH_HISTORY.md

Execution behavior:

- Check known failures before diagnosing or patching.
- Prefer validated patterns when they match the current task.
- Review patch history to avoid repeating rejected or risky approaches.
- Preserve all existing rules and apply the memory review as an additive preflight step.

Duplicate guard:

- Use memory-key values as stable duplicate identifiers.
- Before appending any new memory entry, search the target memory file for the same memory-key.
- If the same memory-key exists, skip the append and record duplicate_entries_skipped.
- If no key exists, append a concise timestamped entry with root cause, fix pattern, validation evidence, and rollback notes.

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
