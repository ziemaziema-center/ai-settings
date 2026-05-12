# Failure Telemetry

## ROLE
Track recurring failure patterns that should influence future execution.

## CONTEXT
Use this file when a task fails, validation fails, rollback is required, or a repeated operational mistake appears.

## FAILURE ENTRY TEMPLATE
`	ext
## YYYY-MM-DD HH:mm KST - Failure Pattern
- memory-key:
- task_category:
- symptom:
- root_cause:
- detection_method:
- affected_scope:
- fix_pattern:
- prevention:
- validation_after_fix:
- rollback_reference:
`

## DUPLICATE PREVENTION
- Search for the same memory-key first.
- If no key exists, search for the same symptom plus oot_cause.
- Append only when the pattern is new or materially different.

## CURRENT STATUS
- No telemetry-specific failure patterns recorded yet.

## VALIDATION OUTCOME FIELD
- memory-key: telemetry-failure-validation-outcome-field-v1
- required_field: `validation_outcome`
- usage: Record the validation result after a fix attempt, or `not_run_with_reason` when validation cannot run.
- duplicate_prevention: Do not append this section again if the same `memory-key` exists.
