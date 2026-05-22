# Helper Backup/Rollback Validation Plan - 2026-05-11

## Purpose

This plan defines the backup, rollback, and validation requirements for any future safe helper change, including a possible read-only helper telemetry detail endpoint.

This document is planning-only. It does not authorize helper modification, workflow modification, Docker changes, service restart, live API calls, order placement, cancel, activation, cron, or Telegram send.

Current state:
- Helper detail endpoint implementation is deferred.
- Open order remains `wait` / stale.
- Helper backup and rollback path has not yet been verified.
- No helper modification is allowed now.

## 1. Backup Targets

Future helper work must create a backup before any patch.

Required backup targets:
- `/home/ubuntu/upbit-helper`
- helper application source files, including `app/main.py`
- helper dependency files, including `requirements.txt`
- helper Dockerfile if present
- helper service/container launch metadata if applicable
- any helper-local validation scripts used for the patch

Docker/service configuration:
- Capture helper container name, image/tag, exposed ports, Docker network, mounted paths, and restart policy if applicable.
- Record configuration metadata only.
- Do not modify Docker settings during backup.
- Do not restart containers during backup unless separately approved.

Environment handling:
- Confirm which env var names are required without printing values.
- Do not copy secrets into reports, logs, shell output, or backup manifests.
- Do not print `UPBIT_ACCESS_KEY`, `UPBIT_SECRET_KEY`, Telegram tokens, Authorization headers, JWTs, or raw account/order payloads.
- If env state must be recorded, record only `present=true/false` and masked labels.

Minimum backup artifact requirements:
- timestamped backup directory
- file manifest
- checksum or size metadata for non-secret files
- explicit note that secret values were not captured
- restore instructions tied to the exact backup path

## 2. Rollback Method

Future rollback must restore the previous helper file set exactly and validate that the helper has returned to the known safe state.

Rollback steps:
1. Stop before rollback if the backup path is missing or ambiguous.
2. Restore files from the timestamped backup.
3. Validate Python syntax for changed files without executing live API calls.
4. Confirm endpoint definitions match the backed-up version.
5. Confirm existing endpoint behavior is unchanged by static diff review.
6. Confirm no restart occurs unless separately approved.
7. If a restart is separately approved later, perform only the approved restart and then run read-only health checks.

Post-rollback validation:
- syntax check passes
- `/health` plan is ready for read-only validation
- existing endpoint inventory matches expected state
- no live-order behavior changed
- no signing/auth behavior changed
- no workflow activation changed
- no forbidden endpoint behavior introduced

No restart rule:
- Rollback planning may describe restart validation.
- Actual restart is forbidden unless a future prompt explicitly approves it and restart impact is understood.

## 3. Validation Checks

Future helper patch validation must include:

### Secret leak check

Confirm no output or artifact contains:
- API secret
- JWT
- Authorization header
- raw balances
- raw order payload
- full account identifiers
- full UUID in general reports
- Telegram bot token
- Telegram chat ID unless masked

### Auth/signing path check

Confirm the patch does not modify:
- JWT generation
- query hash generation
- nonce generation
- signing helpers
- Authorization header construction
- Upbit credential loading
- auth middleware or equivalent request-auth logic

### Live-order behavior check

Confirm the patch does not modify:
- live-order endpoint behavior
- order-test endpoint behavior
- execution gates
- fuse behavior
- duplicate-lock interpretation
- order payload construction
- retry behavior

### Existing endpoint regression check

Confirm existing helper endpoints remain unchanged unless explicitly scoped:
- `/health`
- `/upbit/accounts/telemetry`
- `/upbit/open-orders/telemetry`
- `/upbit/order-test/telemetry`
- `/upbit/live-order/telemetry`

For a future read-only detail endpoint, existing endpoint regression validation must be performed by:
- static endpoint inventory comparison
- mocked response validation
- local isolated validation
- manual read-only validation only after explicit approval

## 4. Future Approval Gates

Future helper read-only patch approval must pass these gates in order:

1. backup first
2. isolated diff review
3. offline/mocked test
4. helper syntax validation
5. no secret leak scan
6. no auth/signing path change scan
7. no live-order behavior change scan
8. health check plan review
9. read-only endpoint test plan review
10. explicit human approval for any manual read-only validation

The future helper patch must remain classified as `HELPER_READ_ONLY`.

Any ambiguity upgrades the patch to a higher-risk class and blocks implementation.

## 5. Hard Stop Conditions

Stop immediately if any of the following are true:

- secret exposure
- missing backup
- ambiguous backup path
- unclear service restart impact
- open order unresolved without explicit read-only approval
- auth path touched
- signing path touched
- live-order behavior touched
- order-test behavior touched unexpectedly
- existing endpoint regression detected
- helper instability detected
- workflow modification required
- Docker/runtime modification required
- restart required but not separately approved
- live API call required without explicit read-only approval
- any possible order, cancel, reorder, retry, activation, cron, or Telegram send side effect

## 6. Final Rule

Do not implement helper detail telemetry until the current open order resolves or explicit read-only helper approval is granted, and the helper backup/rollback path is verified first.
