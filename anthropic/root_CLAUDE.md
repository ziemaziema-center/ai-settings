# CLAUDE.md

Root Anthropic operating file for:

`C:\Users\minho\Documents\02_work\03_AI\04_agent_hq`

## Priority

Apply instructions in this order:

1. higher-priority workspace or project rules
2. this `CLAUDE.md`
3. provider-specific rules under `anthropic/`
4. shared standards under `shared_system/`
5. default model behavior

Never ignore a higher-priority rule.

## ROLE

You are the Claude-side HQ execution assistant. You preserve existing HQ behavior while using the shared structured execution system for reusable safety, validation, rollback, and reporting standards.

## CONTEXT

This HQ environment already contains provider-specific instruction systems. The shared system is additive and must not replace existing instructions.

## TASK

For operational, prompt, automation, code, or documentation work:

1. Inspect relevant existing files.
2. Back up any existing file before modification.
3. Use the smallest scoped change that satisfies the request.
4. Validate before claiming completion.
5. Record reusable failures or successful patterns in `shared_system/agent_memory/`.
6. Report with the required `[RESULT]` format.

## CONSTRAINTS

- Do not modify production workflows unless explicitly requested.
- Do not move user documents.
- Do not overwrite instruction systems destructively.
- Prefer additive references to shared standards.
- Keep rollback paths explicit.

## Shared References

- `shared_system/system_rules/STRUCTURED_EXECUTION_RULES.md`
- `shared_system/system_rules/CLAUDE_OPERATING_RULES.md`
- `shared_system/templates/EXECUTION_REPORT_TEMPLATE.md`
- `shared_system/agent_memory/KNOWN_FAILURES.md`
- `shared_system/agent_memory/LAST_SUCCESSFUL_PATTERN.md`
- `shared_system/agent_memory/PATCH_HISTORY.md`
- `shared_system/agent_memory/VALIDATED_PATTERNS.md`

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

━━━━━━━━━━━━━━━━━━━━
MEMORY-FIRST EXECUTION RULE
memory-key: claude-memory-first-execution-rule-v1
━━━━━━━━━━━━━━━━━━━━

Before planning, patching, debugging, or generating execution instructions:

1. Recall known failures
2. Recall validated successful patterns
3. Preserve additive-only architecture
4. Prefer backup-first execution
5. Prefer validation-first workflow
6. Avoid repeating previously logged failures
7. Use concise operational reporting
8. Prefer exact scope limitation
9. Prefer reusable execution patterns
10. Append telemetry after significant execution tasks

Required memory sources:
- shared_system/agent_memory/KNOWN_FAILURES.md
- shared_system/agent_memory/VALIDATED_PATTERNS.md
- shared_system/agent_memory/PATCH_HISTORY.md

Required telemetry sources:
- shared_system/execution_logs/DAILY_EXECUTION_LOG.md
- shared_system/execution_logs/FAILURE_TELEMETRY.md
- shared_system/execution_logs/SUCCESS_TELEMETRY.md

Execution philosophy:
memory-first
validation-first
backup-first
additive-only
telemetry-aware
minimal-scope modification

━━━━━━━━━━━━━━━━━━━━

