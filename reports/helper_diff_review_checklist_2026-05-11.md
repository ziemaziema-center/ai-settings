# Helper Change Diff-Review Checklist - 2026-05-11

## Purpose

This checklist must be completed before any future `upbit-helper` patch.

Current state:
- Helper detail endpoint implementation is deferred.
- Helper backup/rollback plan exists.
- Open order remains `wait` / stale.
- No runtime modification is allowed now.

This document is documentation-only. It does not authorize helper patches, workflow patches, Docker changes, service restarts, live API calls, order placement, cancel, activation, cron, or Telegram send.

## 1. Scope Check

A future helper patch may proceed only if all scope checks are true:

- [ ] Patch is additive endpoint only.
- [ ] Patch is read-only only.
- [ ] Existing endpoint behavior is unchanged.
- [ ] Auth/signing/JWT logic is unchanged.
- [ ] Live-order path behavior is unchanged.
- [ ] Order-test behavior is unchanged unless explicitly scoped and separately approved.
- [ ] No cancel, reorder, withdrawal, retry, activation, cron, or Telegram execution path is introduced.
- [ ] No unrelated helper/service files are touched.
- [ ] Open order status has been reviewed before the patch decision.
- [ ] Patch classification is `HELPER_READ_ONLY`.

Reject immediately if any scope check is false or ambiguous.

## 2. Diff Review Check

Reject the helper patch if the diff touches any of the following:

- [ ] Signing function.
- [ ] Query-hash generation.
- [ ] Nonce generation.
- [ ] Auth header creation.
- [ ] API key loading.
- [ ] Credential/env loading behavior.
- [ ] Live-order endpoint.
- [ ] Order-test endpoint, unless explicitly approved.
- [ ] Cancel, reorder, or withdrawal strings.
- [ ] Docker/runtime config.
- [ ] Container/service startup files.
- [ ] Unrelated service files.
- [ ] n8n workflow JSON files.
- [ ] Telegram send path.

Required diff review evidence:
- [ ] Exact files changed listed.
- [ ] Exact functions changed listed.
- [ ] Endpoint inventory before/after compared.
- [ ] Existing endpoint behavior marked unchanged.
- [ ] Reviewer confirms no execution path is reachable from the new code.

## 3. Secret Safety Check

Reject the helper patch if the diff logs, returns, prints, stores, or exposes:

- [ ] API secret.
- [ ] JWT.
- [ ] Authorization header.
- [ ] Raw balances.
- [ ] Raw order payload.
- [ ] Full UUID in general reports.
- [ ] Full API key.
- [ ] Full account identifiers.
- [ ] Telegram bot token.
- [ ] Telegram chat ID unless masked.

Required safe handling:
- [ ] UUID is masked if needed for correlation.
- [ ] Account/order details are summarized and sanitized.
- [ ] Error messages are sanitized.
- [ ] Env var presence is recorded only as present/missing, never value.
- [ ] Reports contain no raw exchange payloads.

## 4. Test Requirement

Future helper patch validation must run in this order:

- [ ] WF05 offline fixture regression passes before helper patch.
- [ ] Mocked helper response test passes.
- [ ] Syntax/static validation passes without live API.
- [ ] Forbidden endpoint scan passes.
- [ ] Secret leak scan passes.
- [ ] Existing endpoint regression scan passes.
- [ ] `/health` pass is checked only after separately approved restart/check.
- [ ] Read-only endpoint test runs only after explicit approval.
- [ ] No workflow execution occurs.
- [ ] No runtime activation occurs.

Hard rule:
- If any offline or mocked test fails, STOP before runtime patch or live telemetry validation.

## 5. Rollback Readiness

Before any helper patch:

- [ ] Backup path exists.
- [ ] Backup path is timestamped.
- [ ] Backup contains `/home/ubuntu/upbit-helper` source files.
- [ ] Backup manifest exists.
- [ ] Restore command is documented.
- [ ] Restore validation is documented.
- [ ] Syntax validation after restore is documented.
- [ ] Endpoint inventory after restore is documented.
- [ ] Restart impact is understood.
- [ ] No restart is planned unless separately approved.

Reject if:
- backup is missing;
- restore command is missing;
- validation after restore is missing;
- service restart impact is unclear.

## 6. Final Rule

No helper patch without clean diff review.

If the diff touches auth, signing, live execution, secrets, Docker/runtime configuration, unrelated services, or unclear behavior, STOP.
