# V2 Lock Integration Gate

Date: 2026-05-11 KST

Mode: documentation-only, additive-only

Runtime status: unchanged by this document

## 1. Purpose Of Lock Integration Gate

The lock integration gate defines the minimum safety contract before any workflow may call the deployed execution lock helper endpoints.

The lock exists to prevent duplicate or concurrent live execution attempts. It does not authorize trading. It does not replace reconciliation, duplicate-order checks, live fuse gates, human approval, or STOP behavior.

Primary principle:

```text
STOP > EXECUTE
```

## 2. Why Workflow Patch Is Still Blocked

Workflow patching remains blocked because a deployed lock endpoint is not enough to make workflow execution safe.

Required gaps before workflow patching:

- no reviewed workflow-level integration patch prompt exists;
- no workflow-specific offline regression cases exist for lock branches;
- no dry-run validation has proven workflow lock calls remain non-executing;
- no workflow patch backup/rollback package has been created for lock integration;
- no explicit human approval has been granted for workflow patch implementation;
- live execution remains separately blocked.

Therefore, this document does not permit workflow modification.

## 3. First Candidate Workflow For Future Lock Integration

First candidate workflow:

```text
WF05_Reconciliation_ReadOnly
```

Rationale:

- WF05 is already read-only and manual-only.
- WF05 is closest to reconciliation state and can validate finality before any future execution workflow is considered.
- WF05 can test lock status and report STOP states without adding execution authority.

WF04 must not be the first integration target because it is the live execution workflow. Lock integration must be proven in read-only workflow context before any execution workflow patch is considered.

## 4. Workflows That Must Remain Inactive

The following workflows must remain inactive:

- `KBIA_03_WF_Upbit_PreCheck_Engine`
- duplicate `KBIA_03_WF_Upbit_PreCheck_Engine`
- `KBIA_04_WF_Upbit_Execution_Engine`
- `WF05_Reconciliation_ReadOnly`

Workflow integration patching must not activate workflows and must not enable cron.

## 5. Required Pre-Checks Before Workflow Uses Lock

Before any workflow calls an execution lock endpoint, the workflow must confirm:

- helper health is PASS;
- helper detail endpoint is reachable;
- execution lock status endpoint is reachable;
- `open_order_exists=false`;
- `open_order_count=0`;
- duplicate-order status is clear;
- reconciliation state is final and unambiguous;
- live fuse remains disabled unless a separate future reset gate is approved;
- workflow is inactive before patching;
- cron is disabled;
- automation is disabled;
- persistent logging path is available;
- secrets leak check is PASS;
- forbidden endpoint check is PASS.

If any pre-check is missing, failed, stale, or ambiguous:

```text
STOP
```

## 6. Required Lock Acquisition Point

The lock acquisition point must be after all read-only reconciliation and duplicate-order checks pass, and before any future execution workflow could reach a live-order path.

For the first read-only integration in WF05, acquisition should not occur unless the purpose is a dry-run validation of lock mechanics with no execution authority. A safer first patch may call only `/execution-lock/status` and report lock state.

For any later execution-adjacent workflow, acquisition must occur only after:

- helper detail reconciliation proves no open order;
- duplicate-order check is false;
- workflow active state is known safe;
- cron is known disabled;
- human approval is present;
- live fuse reset is separately approved and logged;
- order journal evidence exists.

## 7. Required Lock Release Point

Lock release must be explicit, human-approved, and bounded.

Allowed release conditions:

- matching lock ID;
- matching owner token;
- human release approval;
- `open_order_exists=false`;
- `open_order_count=0`;
- final reconciliation classification is `done` or `cancel`, or release reason is `approved_abort_before_execution`;
- workflow active state is known safe;
- cron disabled state is known safe.

Release must not happen automatically after timeout, restart, helper recovery, workflow error, or stale lock detection.

## 8. If Lock Exists

If lock exists:

```text
STOP
```

Required behavior:

- do not acquire another lock;
- do not place an order;
- do not cancel;
- do not reorder;
- do not retry;
- do not activate workflows;
- do not reset fuse;
- log/report `ACTIVE_LOCK_EXISTS`;
- require human review.

## 9. If Lock Status Is Unclear

If lock status is unclear:

```text
STOP
```

Unclear states include:

- helper unavailable;
- lock endpoint timeout;
- malformed lock response;
- partial lock write present;
- lock schema mismatch;
- missing active lock file state with conflicting journal evidence;
- permission error;
- journal append failure;
- unknown helper error.

No fallback execution path is allowed.

## 10. If Stale Lock Exists

If stale lock exists:

```text
STOP + human review
```

Required behavior:

- do not auto-unlock;
- do not auto-retry;
- do not acquire a replacement lock;
- do not execute;
- do not cancel;
- write/read a safe report-only state;
- require explicit human-reviewed manual unlock flow under a separate approved prompt.

## 11. Helper Detail Endpoint Before And After Lock

Before lock use:

- call helper detail endpoint in read-only mode;
- confirm `open_order_exists=false`;
- confirm `open_order_count=0`;
- confirm duplicate-order status is false;
- confirm classification is final and unambiguous;
- preserve `next_safe_action=remain_stopped`.

After lock use:

- call helper detail endpoint again before any release decision;
- confirm no open order exists;
- confirm no duplicate/new order appeared;
- confirm final classification remains safe;
- append sanitized journal evidence.

If helper detail telemetry is missing, malformed, inconsistent, rate-limited, or unknown:

```text
STOP
```

## 12. Live Fuse Interaction With Lock

The lock does not reset the live fuse.

Rules:

- lock acquisition does not authorize live execution;
- lock acquisition does not consume or reset fuse state;
- live fuse reset requires a separate design, review, approval, and validation gate;
- if fuse state is unknown or ambiguous, STOP;
- if fuse is disabled and no separate reset approval exists, live execution remains blocked.

## 13. Duplicate Order Prevention Interaction With Lock

Duplicate-order prevention remains mandatory and independent.

Rules:

- duplicate-order check must run before any lock acquisition;
- duplicate-order check must run after any lock release;
- `duplicate_order_exists=true` means STOP;
- unknown duplicate-order status means STOP;
- lock presence does not prove duplicate-order absence;
- duplicate-order absence does not authorize execution.

## 14. Required Offline Regression Cases

Future workflow lock integration must add and pass offline cases for:

- helper health failure -> STOP;
- lock status unlocked -> continue read-only branch only;
- active lock exists -> STOP;
- stale lock exists -> STOP + human review;
- lock status timeout -> STOP;
- lock status malformed -> STOP;
- lock journal unavailable -> STOP;
- helper detail says open order exists -> STOP;
- helper detail duplicate order exists -> STOP;
- reconciliation unclear -> STOP;
- fuse disabled without reset approval -> STOP;
- cron enabled -> STOP;
- workflow active ambiguity -> STOP;
- no execution path reachable from lock status branch;
- no auto-unlock branch exists;
- no auto-retry branch exists.

## 15. Required Dry-Run Validation Cases

Before any runtime workflow patch can be considered safe, dry-run validation must prove:

- workflow remains inactive;
- manual trigger only;
- no cron/schedule added;
- only helper read/lock endpoints are called;
- no `/upbit/live-order/telemetry` call is reachable;
- no cancel/reorder/withdrawal endpoint is reachable;
- active lock blocks;
- stale lock blocks and reports human review required;
- helper unavailable blocks;
- malformed telemetry blocks;
- lock acquisition dry-run cannot place order;
- lock release dry-run cannot trigger execution;
- reports/logs are sanitized;
- no JWT, Authorization header, API secret, raw balances, raw order payload, or full UUID is logged.

## 16. Forbidden Integration Behaviors

The following behaviors are forbidden:

- workflow activation from integration patch;
- cron enablement;
- live execution from integration patch;
- live-order endpoint call;
- cancel endpoint call;
- reorder endpoint call;
- withdrawal endpoint call;
- retry loop;
- auto-unlock;
- auto-retry after helper failure;
- auto-retry after stale lock;
- automatic cancel/reprice;
- second order before reconciliation;
- live fuse reset;
- Telegram execution buttons;
- Telegram runtime send unless separately approved for read-only alerts;
- investment decision logic;
- hidden fallback execution path.

## 17. Minimum Bounded Workflow Patch Scope

Minimum future workflow patch scope should be:

- one workflow only;
- preferably `WF05_Reconciliation_ReadOnly` first;
- inactive/manual-only preserved;
- read-only lock status node first;
- report-only lock state summary;
- append-only sanitized log/report;
- no lock acquisition unless separately approved for dry-run validation;
- no execution node changes;
- no live-order path changes;
- no workflow activation;
- no cron/schedule.

WF03 and WF04 must not be patched in the same prompt as initial lock integration.

## 18. Required Review Before Patch Prompt

Before a workflow patch prompt may be written:

- this lock integration gate must be reviewed;
- review decision must be PASS;
- missing/ambiguous items must be resolved;
- target workflow must be explicitly selected;
- bounded patch scope must be approved;
- rollback plan must be documented;
- offline regression plan must be approved;
- live execution must remain explicitly excluded.

## 19. Explicit Human Approval Before Implementation

Implementation requires explicit human approval after review.

Approval must name:

- target workflow;
- allowed nodes/endpoints;
- allowed files;
- forbidden workflows/files;
- validation steps;
- rollback path;
- confirmation that workflow activation and cron remain forbidden.

No approval is implied by this document.

## 20. Conditions Before Any Live Execution Discussion

Live execution may not be discussed until all of the following are true:

- helper health PASS;
- helper detail endpoint PASS;
- execution lock runtime PASS;
- lock final state unlocked;
- no stale lock;
- `open_order_exists=false`;
- `open_order_count=0`;
- duplicate-order status false;
- reconciliation final and unambiguous;
- persistent order journal present;
- live fuse reset design reviewed and approved;
- workflow lock integration implemented and validated read-only;
- workflow remains inactive/manual-only after patch;
- cron disabled;
- Telegram runtime execution controls absent;
- offline regression PASS;
- dry-run validation PASS;
- rollback validated;
- explicit human approval granted for a separate live execution planning gate.

## Decision

workflow_patch_allowed_now: false

first_candidate_workflow: `WF05_Reconciliation_ReadOnly`

live_execution_allowed_now: false

## Final Rule

NO WORKFLOW PATCH MAY BE WRITTEN UNTIL THIS LOCK INTEGRATION GATE IS REVIEWED AND EXPLICITLY APPROVED.
