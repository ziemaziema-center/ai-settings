# V2 Implementation Scope Decision - 2026-05-11

## Current Verified State

- SAFE LIMITED LIVE EXECUTION V1 completed.
- Clean shutdown / controlled stop verification PASS.
- `open_order_exists=false`.
- `duplicate_order_exists=false`.
- Workflows inactive.
- Cron disabled.
- Live fuse disabled.
- V2 safety gate completed.
- V2 runtime architecture review completed.
- V2 implementation readiness checklist completed.
- Automation remains disabled.

This document is documentation-only. It does not approve implementation, workflow modification, helper modification, restart, Docker changes, live API calls, orders, cancels, reorders, activation, cron enablement, or Telegram runtime sends.

## 1. First Implementation Target

Decision:
- First implementation target: documentation-only.

Justification:
- V2 architecture is designed, but runtime scope is not yet human-approved.
- Helper detail telemetry is not implemented.
- Persistent order journal location is only a design decision until the operator approves host/runtime placement.
- Execution lock ownership is only a design decision until journal placement is approved.
- Conservative rule applies: if uncertain, choose documentation-only.

Allowed next implementation-adjacent work:
- refine V2 prompt scope;
- define exact journal schema;
- define exact helper endpoint diff boundaries;
- expand offline regression fixtures;
- prepare approval package for the human operator.

Not allowed now:
- workflow patch;
- helper patch;
- live API call;
- activation;
- cron;
- runtime restart.

## 2. Whether Helper Detail Endpoint Must Be Implemented Before Any V2 Runtime Patch

Decision:
- Yes, helper detail endpoint must be implemented and validated before any V2 runtime workflow patch that depends on detailed order lifecycle fields.

Justification:
- WF05 currently works safely with summary-only telemetry, but production-grade V2 reconciliation requires lifecycle detail.
- Workflow patches that assume missing detail would create ambiguous state handling.
- If helper state is incomplete, block workflow patch.

Boundary:
- The helper endpoint must be additive and read-only.
- Existing endpoints, JWT generation, signing logic, auth header construction, API key loading, live-order behavior, order-test behavior, cancel/reorder/withdrawal behavior must remain untouched.

Exception:
- Documentation-only and offline fixture work may continue before helper detail endpoint implementation.

## 3. Where Order State Journal Should Live

Decision:
- V2 order state journal should live as append-only local JSONL on the n8n host or a dedicated mounted logging path, not inside workflow staticData alone.

Proposed initial path concept:

```text
kbia-logs/order_journal/YYYY-MM-DD.jsonl
```

Required properties:
- append-only;
- sanitized fields only;
- one event per JSON object;
- date partitioned;
- readable by recovery procedures;
- separate from raw exchange payloads and secrets.

Status:
- Design decision made.
- Runtime path not approved.
- Patch prompt not allowed until the human operator approves the exact path and backup/rollback behavior.

## 4. Where Execution Lock Should Live

Decision:
- Execution lock should live primarily in the persistent order journal / lock journal, with workflow staticData allowed only as a non-authoritative runtime cache.

Required lock sources:
- persistent duplicate tuple lock;
- persistent live fuse state;
- open-order exchange state;
- latest reconciliation state;
- workflow inactive/cron state;
- emergency stop state.

Rules:
- StaticData alone is insufficient.
- Missing persistent lock state means STOP.
- Uncertain lock state means STOP.
- Runtime cache may never override persistent STOP state.

Status:
- Design decision made.
- Exact lock schema not yet approved.
- Patch prompt not allowed until schema and persistence location are explicitly approved.

## 5. How Live Fuse Reset Should Be Controlled

Decision:
- Live fuse reset must be controlled manually through a future safety-gated human approval package, not by workflow logic.

Fuse reset requirements:
- `open_order_exists=false`;
- `duplicate_order_exists=false`;
- prior order reconciled as `done` or `cancel`;
- persistent order journal available;
- duplicate lock state clear;
- WF03/WF04/WF05 inactive;
- cron disabled;
- emergency stop clear;
- rollback path ready;
- exact one-time attempt parameters approved by human.

Fuse reset must:
- be one-time;
- be scoped to one market, one side, one order type, one bounded value, one attempt;
- be consumed before any live helper call;
- auto-disable after the attempt;
- never be reset automatically.

## 6. Which Workflow May Be Patched First In V2, If Any

Decision:
- No workflow may be patched yet.

First possible workflow candidate after approval:
- WF05_Reconciliation_ReadOnly.

Why WF05 first:
- It is read-only.
- It is inactive/manual-only.
- It is the lowest-risk place to consume future helper detail telemetry.
- It can be validated with offline regression before runtime testing.

Blocker:
- WF05 patch must wait until helper detail endpoint scope and persistent journal decisions are approved, if the patch depends on those capabilities.

## 7. Which Workflow Must Remain Inactive

Decision:
- WF03 must remain inactive.
- WF04 must remain inactive.
- WF05 must remain inactive/manual-only/read-only.

Rationale:
- WF03 can influence execution eligibility.
- WF04 contains the live execution path.
- WF05 must remain observation-only and must not become an automation bridge.

No workflow activation is allowed by this document.

## 8. Runtime Actions That Remain Forbidden

Forbidden actions:
- live order;
- second order;
- cancel;
- reorder;
- retry loop;
- workflow activation;
- cron enablement;
- helper patch;
- workflow patch;
- Docker/runtime change;
- restart;
- Telegram runtime send;
- Telegram trade/cancel/retry/activate/cron buttons;
- raw balance logging;
- raw order payload logging;
- JWT or Authorization header logging.

Manual user actions outside Codex automation must still be reconciled as external operator actions and must not become automation precedent.

## 9. Minimum Patch Scope For The First V2 Implementation Prompt

Decision:
- Minimum first patch prompt should be a documentation/offline-only package unless the human operator explicitly approves runtime scope.

Preferred first patch prompt scope:
- expand WF05 offline regression fixtures;
- define order journal schema;
- define lock journal schema;
- define helper detail endpoint fixture contract;
- no helper changes;
- no workflow changes;
- no runtime calls.

If the operator approves runtime implementation later, the smallest acceptable runtime patch should be:
- one helper read-only detail endpoint only;
- additive code only;
- no existing endpoint behavior changes;
- no JWT/signing/auth changes;
- no live-order/order-test/cancel/reorder changes;
- mocked tests first;
- no workflow patch in the same prompt.

## 10. Absolute Blockers Before Any V2 Runtime Patch

Runtime patch is blocked if any are true:

- helper detail endpoint scope not approved;
- order journal exact path not approved;
- execution lock schema not approved;
- live fuse reset rules not approved;
- rollback path missing;
- backup path missing;
- persistent logging unavailable;
- open order exists;
- duplicate state uncertain;
- workflow active state uncertain;
- cron state uncertain;
- emergency stop uncertain;
- helper health unavailable;
- auth telemetry failing;
- WF05 offline regression failing;
- patch touches JWT/signing/auth unexpectedly;
- patch touches live-order behavior unexpectedly;
- patch could cancel, reorder, retry, activate, enable cron, restart, or send Telegram runtime messages;
- human approval is missing or ambiguous.

## 11. Required Approval Gate Before Patch Prompt Creation

Before any runtime patch prompt is written, the human operator must explicitly approve:

- patch class;
- target component;
- exact files in scope;
- exact files out of scope;
- runtime calls allowed or forbidden;
- backup path;
- rollback method;
- validation plan;
- forbidden endpoint scan;
- secret leak scan;
- final output format.

For the first V2 runtime patch, approval must also state whether the target is:
- helper read-only endpoint only;
- WF05 read-only workflow only;
- offline fixtures only;
- documentation-only.

Without this approval, patch_prompt_allowed_now is false.

## 12. Required Validation Before Any Future Live Execution Discussion

Before future live execution can even be discussed:

- `open_order_exists=false`;
- `duplicate_order_exists=false`;
- prior order reconciled as `done` or `cancel`;
- no `wait`, `partial_fill`, `stale_wait`, or `unknown_stop` remains;
- helper health PASS;
- auth telemetry PASS;
- open-order telemetry PASS;
- detailed reconciliation PASS if detail endpoint exists;
- persistent order journal available;
- execution lock state clear;
- live fuse disabled until one-time approval;
- WF03/WF04/WF05 inactive;
- cron disabled;
- WF05 offline regression PASS;
- rollback path ready;
- emergency stop clear;
- human approval explicit and one-time.

Discussion is not implementation approval. Implementation approval is not live execution approval.

## Final Decision Summary

- First implementation target: documentation-only.
- Helper detail endpoint required before dependent workflow runtime patch: yes.
- Order journal location: design decision is local append-only JSONL on n8n host or mounted logging path; exact runtime path requires human approval.
- Execution lock location: design decision is persistent journal/lock journal as authority, staticData cache only; exact schema requires human approval.
- Patch prompt allowed now: no.

NO PATCH PROMPT MAY BE WRITTEN UNTIL V2 IMPLEMENTATION SCOPE IS EXPLICITLY APPROVED BY THE HUMAN OPERATOR.
