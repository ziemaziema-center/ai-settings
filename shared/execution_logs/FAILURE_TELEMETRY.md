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

## 2026-05-19 14:05 KST - Remote rg Missing
- memory-key: telemetry-failure-remote-rg-missing-v1
- task_category: remote_validation
- symptom: Safety scan command using `rg` failed in the EC2 bounded workspace.
- root_cause: The remote workspace image does not include ripgrep.
- detection_method: SSH scan returned `rg: command not found`.
- affected_scope: Remote safety scan only.
- fix_pattern: Use `grep -R -n -E` with the same pattern set when `rg` is unavailable.
- prevention: Prefer `rg` locally; fall back to `grep` on EC2 until ripgrep is installed.
- validation_after_fix: `grep` scan completed with no matches for risky patterns in newly added files.
- rollback_reference: Not required; no project files were modified by the failed scan.

## 2026-05-20 17:40 KST - Tailscale Auth Pending
- memory-key: telemetry-failure-tailscale-auth-pending-user-approval-v1
- task_category: remote_access_setup
- symptom: EC2 `tailscale up` installed and started `tailscaled` but remained logged out and did not assign a Tailscale IP.
- root_cause: Tailnet enrollment requires user approval through the Tailscale login web flow; no reusable auth key was provided.
- detection_method: `tailscale status` returned `Logged out` and `tailscale ip -4` returned empty.
- affected_scope: SSH-over-Tailscale validation only.
- fix_pattern: On EC2, rerun `sudo tailscale up --ssh=false --accept-dns=false --accept-routes=false --hostname=kbia-ec2-ops`, approve the generated URL from a logged-in Tailscale device, then validate `tailscale ip -4` and SSH to that IP.
- prevention: For future fully unattended EC2 enrollments, provide a short-lived, pre-approved Tailscale auth key.
- validation_after_fix: not_run_with_reason_user_tailnet_auth_required
- rollback_reference: `sudo tailscale down` disables overlay connectivity without touching Docker/n8n runtime; package removal is optional and was not performed.
