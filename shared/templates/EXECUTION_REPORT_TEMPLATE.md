# Execution Report Template

Use this exact report shape for operational tasks.

```text
[RESULT]
- backup_path:
- files_modified:
- validation_result:
- side_effects:
- rollback_needed:
- next_action:
```

## Field Rules
- `backup_path`: Use a concrete path, `not_required_new_files_only`, or `not_created_explain_why`.
- `files_modified`: List created, modified, or deleted files separately when useful.
- `validation_result`: Include command/check and outcome.
- `side_effects`: State known side effects or `none_detected`.
- `rollback_needed`: Use `yes`, `no`, or `conditional`.
- `next_action`: One practical next step.

## Expanded Format
```text
[RESULT]
- backup_path:
- files_created:
- files_modified:
- validation_result:
- side_effects:
- rollback_needed:
- rollback_plan:
- next_action:
```
