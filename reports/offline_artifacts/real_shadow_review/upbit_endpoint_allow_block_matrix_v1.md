# UPBIT ENDPOINT ALLOW BLOCK MATRIX V1

| endpoint_class | examples | status | credential_required | side_effect_risk | required_future_gate | allowed_in_this_run | STOP_condition |
| --- | --- | --- | --- | --- | --- | --- | --- |
| public quotation endpoints | /v1/ticker, /v1/candles/*, /v1/orderbook | FUTURE_REVIEW_ONLY | no | low/read-only | HUMAN_ENDPOINT_SCOPE_APPROVAL | NO | STOP if endpoint scope is ambiguous |
| account read endpoints | /v1/accounts | FUTURE_REVIEW_ONLY | yes | medium (sensitive account data) | HUMAN_CREDENTIAL_SCOPE_APPROVAL | NO | STOP if key permission is broader than approved scope |
| order inquiry read-only endpoints | /v1/orders/open, /v1/order read query only | FUTURE_REVIEW_ONLY | yes | medium (position exposure) | HUMAN_READ_ONLY_ORDER_INQUIRY_APPROVAL | NO | STOP if any mutation-capable path is attached |
| wallet/status inquiry | wallet/service status inquiry class only | FUTURE_REVIEW_ONLY | maybe | low to medium | HUMAN_SCOPE_AND_NEED_APPROVAL | NO | STOP if inquiry endpoint can mutate state |
| order create | /v1/orders create | HARD_BLOCKED | yes | critical mutation | SEPARATE_EXECUTION_AUTH_REQUIRED | NO | STOP immediately if referenced for this run |
| order cancel | /v1/order cancel | HARD_BLOCKED | yes | critical mutation | SEPARATE_KILL_VALIDATION_AUTH_REQUIRED | NO | STOP immediately unless separate future approval exists |
| withdrawal | withdrawal family endpoints | HARD_BLOCKED | yes | critical asset movement | FORBIDDEN_IN_REVIEW_SCOPE | NO | STOP immediately |
| transfer | transfer/internal movement endpoints | HARD_BLOCKED | yes | critical asset movement | FORBIDDEN_IN_REVIEW_SCOPE | NO | STOP immediately |
| deposit/withdrawal address | address issuance/query that can affect transfer operations | HARD_BLOCKED | yes | high operational risk | FORBIDDEN_IN_REVIEW_SCOPE | NO | STOP immediately |
| unclear side-effect endpoint | unknown/undocumented endpoint | HARD_BLOCKED | unknown | unknown/high | DOCUMENTED_CLASSIFICATION_REQUIRED | NO | STOP until classified |

Real shadow review score measures review completeness, blocker clarity, and safety coverage only; it does not authorize real shadow execution, Upbit API access, credential use, scheduler activation, live trading, WF08, or production readiness.

This document does not authorize live trading, real shadow mode execution, Upbit API access, credential use, scheduler activation, parser execution, fixture creation, WF08 transition, runtime wiring, implementation, or production-readiness claims.

This document does not authorize live trading, shadow mode, Upbit API access, credential use, scheduler activation, parser execution, fixture creation, WF08 transition, runtime wiring, implementation, or production-readiness claims.
