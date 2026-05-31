# PUBLIC DATA SHADOW AUTHORIZATION PACKET TEMPLATE V1

## Template Notice

This template is not approval.

## Required Fields

- human_approver:
- approval_timestamp_utc:
- duration_n_days:
- allowed_public_data_endpoint_class:
- explicitly_blocked_endpoint_classes:
- credential_use: false
- scheduler_use: false
- execution_command:
- local_recorder_path:
- daily_review_owner:
- daily_digest_path:
- alert_channel:
- kill_conditions:
- recon_drift_stop_conditions:
- no_submit_statement:
- no_live_statement:
- proof_artifact_list:
- approval_expiration_utc:
- rollback_stop_procedure:

## Hard Constraints

- any non-public endpoint request invalidates this packet
- any credential requirement invalidates public-data-only mode
- any scheduler activation request invalidates this packet

Public-data shadow scope score measures review, scope, blocker clarity, and safety coverage only; it does not authorize real shadow execution, Upbit API access, credential use, scheduler activation, live trading, WF08, or production readiness.

This document does not authorize live trading, real shadow mode execution, Upbit API access, credential use, scheduler activation, parser execution, fixture creation, WF08 transition, runtime wiring, implementation, or production-readiness claims.

This document does not authorize live trading, shadow mode, Upbit API access, credential use, scheduler activation, parser execution, fixture creation, WF08 transition, runtime wiring, implementation, or production-readiness claims.
