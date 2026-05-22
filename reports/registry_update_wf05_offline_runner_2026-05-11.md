# Registry Update: WF05 Offline Regression Runner - 2026-05-11

## Purpose

This document records the validated status of the offline WF05 reconciliation classifier regression runner and the future registry changes it should drive.

This is documentation only. It does not modify workflows, helper code, runtime configuration, live API behavior, Telegram behavior, cron, activation state, or order lifecycle behavior.

## Future VALIDATED_PATTERNS Revision

Add the following pattern in the next `VALIDATED_PATTERNS` registry revision:

### VP-011: WF05 offline regression runner

- validation_level: `STRONGLY_VALIDATED`
- validation_result: `validated`
- reason: 12 fixture cases passed offline with no network or runtime side effects.
- operational_benefit: Future WF05 classifier changes can be checked before any workflow/runtime patch is considered.
- safe_usage_conditions:
  - run offline only
  - use fixture JSON only
  - no helper calls
  - no Upbit calls
  - no n8n workflow execution
  - no secrets
  - no network
- forbidden_usage_conditions:
  - no live API calls
  - no workflow activation
  - no helper modification
  - no order, cancel, reorder, withdrawal, restart, cron, or Telegram send path
- future_revalidation_needed:
  - run before every future WF05 patch
  - update fixtures only through additive safety-gated review

## Future Rule

Every future WF05 patch must run the offline regression runner first.

If any fixture fails:
- STOP
- do not patch runtime
- do not run live telemetry
- do not execute workflow
- generate failure report
- require human review

## Current Results

- offline runner created: `true`
- fixture_count: `12`
- passed_count: `12`
- failed_count: `0`
- failed_case_ids: `[]`
- network_used: `false`
- live_api_called: `false`
- workflow_modified: `false`
- helper_modified: `false`
- runtime_modified: `false`

## Keep In KNOWN_FAILURES

The following risks remain unresolved and must remain tracked:

- open order still `wait` / stale
- helper summary-only telemetry limitation
- restart recovery not runtime-tested
- Telegram runtime alerts not implemented

## Current Safe State

- system remains controlled STOP
- no new runtime actions allowed
- no second order allowed
- no cancel allowed
- no reorder allowed
- no activation allowed
- no cron allowed
- no restart allowed
- no Telegram live send allowed

## Final Rule

The WF05 offline runner strengthens validation, but it does not permit runtime action. Controlled STOP remains in force until the open order resolves and later safety gates pass.
