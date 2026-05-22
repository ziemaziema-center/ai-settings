# WF05 Task-Broker-Safe Runtime Validation Plan

Date: 2026-05-12 KST

Mode: planning/review only

## Result

planning_result: PASS

runtime_validation_status: BLOCKED_PENDING_SEPARATE_APPROVAL

Recommended safest method:

- Use the already running n8n server execution path, preferably the documented workflow run API if the deployed n8n 2.18 instance exposes it.
- Do not use `docker exec n8n n8n execute --id=WF05LockROV2A11 --rawOutput` while the main n8n service is running.

## Additional Execution Hard Limit

Effective 2026-05-12 KST, any future WF05 status-only runtime validation execution method is restricted to exactly one of the following:

1. Existing running n8n instance API execution path:

```text
POST /api/v1/workflows/:id/run
```

2. Single human-driven n8n editor `Execute Workflow` action using the already running n8n server instance.

If the required execution path cannot be confirmed as the already running n8n instance, the validation must STOP and return BLOCKED.

Explicitly forbidden:

- `n8n execute` CLI
- second n8n process
- detached runtime
- task broker restart
- queue restart
- worker restart
- Docker restart
- PM2 restart
- service restart
- multiple executions
- retry execution
- background execution loop
- webhook-triggered execution
- cron-triggered execution

## Problem Statement

The previous WF05 status-only manual runtime validation failed before creating a WF05 execution record because the one-shot `n8n execute` process attempted to start a competing task broker on port `5679`.

This is a launch-method failure, not a WF05 reconciliation logic failure.

## Current Bounds

WF05 runtime workflow:

- workflow name: `WF05_Reconciliation_ReadOnly`
- workflow id: `WF05LockROV2A11`
- inactive: required
- manual-only/read-only: required
- cron disabled: required
- no lock acquire/release: required
- no live order/cancel/reorder/withdrawal: required
- no Telegram runtime send: required

This plan performs no runtime action.

## Option Review

### Option A: Running n8n public workflow run API

Status: RECOMMENDED_IF_ENDPOINT_AVAILABLE

Candidate endpoint:

```text
POST /api/v1/workflows/:id/run
```

Rationale:

- Uses the already running n8n server instead of starting a second `n8n execute` process.
- Avoids the task broker port conflict.
- Does not require workflow activation or cron.
- Can be bounded to one explicit workflow id and one execution attempt.
- Can return an execution id and execution result for audit.

Precondition:

- The deployed n8n 2.18 instance must expose this endpoint in its API reference/playground or accept a read-only preflight request.
- API key/session handling must use existing runtime secret storage or remote env only and must not print headers, JWTs, cookies, or API keys.

Required request shape for the approved future run:

- Fetch or use exact current `WF05LockROV2A11` workflow data without modifying it.
- Execute only `WF05LockROV2A11`.
- Start at `Manual Trigger`.
- Prefer destination node `Build Operator Lock Integration Summary` if supported.
- Do not set `active=true`.
- Do not patch workflow data.
- Do not add webhook, schedule, cron, retry, Telegram, lock acquire/release, or execution endpoints.

Stop if:

- API endpoint is unavailable.
- Endpoint requires activation.
- Endpoint requires modifying WF05.
- Endpoint would create a new trigger or webhook.
- Endpoint cannot prove workflow id, execution id, and execution count delta.
- API response includes sensitive fields that cannot be safely redacted.

### Option B: Human-driven n8n editor manual execution

Status: ACCEPTABLE_FALLBACK_WITH_OPERATOR_APPROVAL

Rationale:

- The editor's Execute Workflow button uses the existing running n8n instance.
- It avoids launching a competing CLI process.
- It preserves inactive/manual-only state.

Limitations:

- Less reproducible than API execution.
- Requires authenticated UI session and careful operator action.
- Evidence capture must be manual or browser-assisted.

Use only if:

- Option A is unavailable in the deployed instance.
- Operator explicitly approves one UI manual execution.
- Preflight gates pass immediately before the click.

### Option C: Internal/private editor execution endpoint

Status: BLOCKED

Rationale:

- Internal endpoints may change across n8n versions and may depend on browser session, CSRF, or editor state.
- Using them directly is riskier than a documented API or human UI action.
- The additional execution hard limit permits only the documented workflow run API path or a single human-driven editor action.

### Option D: Retry `n8n execute` CLI

Status: BLOCKED

Rationale:

- The previous attempt showed the CLI process starts a competing task broker while the main n8n instance is already running.
- A second attempt without changing method is expected to fail the same way.

### Option E: Stop/restart n8n, then run CLI

Status: BLOCKED

Rationale:

- Restart is explicitly forbidden unless separately reviewed and approved.
- Restart recovery remains an unresolved known failure.
- Stopping the main runtime could affect unrelated workflows or runtime state.

### Option F: Change task broker port or start a second n8n runtime

Status: BLOCKED

Rationale:

- Two n8n runtimes against the same runtime database and workflow set create execution ownership ambiguity.
- This could introduce queue, credential, staticData, and execution-record ambiguity.

### Option G: Temporary webhook or manager workflow

Status: BLOCKED

Rationale:

- Requires workflow patch/import and likely activation or test-listen behavior.
- Violates the current no workflow modification/no activation planning scope.
- The additional execution hard limit forbids webhook-triggered execution.

## Required Approval Gate

Before any second WF05 runtime validation attempt, require a separate explicit approval prompt containing:

```text
I approve exactly one WF05 status-only runtime validation using the already running n8n server path.
Allowed workflow id: WF05LockROV2A11.
Allowed method: documented n8n workflow run API if available; otherwise one human/UI manual Execute Workflow action after separate confirmation.
Allowed runtime effects: one WF05 execution record and read-only helper calls already present in WF05.
Forbidden: workflow activation, cron, helper patch, workflow patch, restart, n8n execute CLI, second n8n process, detached runtime, task broker restart, queue restart, worker restart, Docker restart, PM2 restart, service restart, webhook-triggered execution, cron-triggered execution, live order, cancel, reorder, withdrawal, Telegram runtime send, lock acquire, lock release, live fuse reset, retry loop, second attempt without review.
Secrets must not be printed or stored.
```

## Future Execution Plan After Approval

1. Preflight read-only gates:
   - Confirm helper health.
   - Confirm `open_order_exists=false` and `open_order_count=0`.
   - Confirm execution lock status is `unlocked`, `lock_exists=false`, and `stale_lock=false`.
   - Confirm WF05 exists exactly once as `WF05LockROV2A11`.
   - Confirm WF05 is inactive.
   - Confirm `triggerCount=0` and no cron/schedule nodes.
   - Confirm WF03/WF04 remain inactive.
   - Confirm WF05 execution count before run.
   - Static-scan current runtime workflow data for forbidden endpoints and Telegram send.

2. Method preflight:
   - Confirm the running n8n server supports `POST /api/v1/workflows/:id/run`, or stop and request UI fallback approval.
   - Confirm no command will start a new n8n process or task broker.
   - Confirm the path is not webhook-triggered, cron-triggered, detached, restarted, queued via a restarted worker, or retried.
   - Confirm API key/session material stays only in env/session and is not logged.

3. Single bounded execution:
   - Execute exactly one WF05 run through the running n8n server.
   - Do not retry automatically.
   - Capture only sanitized execution id prefix, finished status, final node status, and safe output summary.

4. Post-run validation:
   - Confirm WF05 execution count delta is exactly `1`.
   - Confirm WF05 remains inactive.
   - Confirm cron remains disabled.
   - Confirm WF03 and WF04 execution counts did not change.
   - Confirm no workflow activation changed.
   - Confirm no live order/cancel/reorder/withdrawal endpoints were called.
   - Confirm no Telegram runtime send occurred.
   - Confirm no lock acquire/release occurred.
   - Confirm output includes `safe_reconciliation_log_payload` or STOP reason.

5. Failure handling:
   - If execution does not start, record failure and stop.
   - If execution count delta is not exactly `1`, record failure and stop.
   - If any forbidden side effect is detected, record failure and stop.
   - No second attempt without a new reviewed plan.

## Runtime Impact

Allowed future impact after approval:

- One WF05 execution record.
- Read-only helper detail telemetry call.
- Read-only execution lock status call.
- Append-only helper detail journal entry if WF05 sends `journal_enabled=true`.

Forbidden future impact:

- workflow activation
- cron enablement
- helper patch
- workflow patch
- restart
- live order
- cancel
- reorder
- withdrawal
- Telegram runtime send
- lock acquire/release
- live fuse reset
- retry loop

## Rollback

There is no rollback for an append-only execution record or append-only helper journal entry. These should remain as audit evidence.

Rollback is only applicable if an unexpected configuration mutation occurs, in which case stop immediately and use the existing WF05 runtime import backup path under separate approval.

## Final Recommendation

PASS for the bounded plan.

BLOCKED for actual runtime validation until the separate approval gate is satisfied.

Safest method: documented running n8n workflow run API, verified on the deployed instance immediately before use. Fallback: one human-driven editor manual execution. All CLI methods that start a separate n8n process remain blocked.

Under the additional execution hard limit, if neither of those two paths can be confirmed as using the already running n8n instance, the result is BLOCKED.
