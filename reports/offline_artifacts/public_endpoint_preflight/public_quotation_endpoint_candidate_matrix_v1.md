# PUBLIC QUOTATION ENDPOINT CANDIDATE MATRIX V1

| endpoint_class | future_status | credential_required | side_effect_risk | allowed_in_this_run | allowed_in_future_public_data_only_preflight | required_future_gate | STOP_condition |
| --- | --- | --- | --- | --- | --- | --- | --- |
| market list / market metadata | FUTURE_PREFLIGHT_CANDIDATE | no | low/read-only | NO | YES | HUMAN_PUBLIC_PREFLIGHT_SCOPE_APPROVAL | STOP if response implies auth requirement |
| ticker / current price quotation | FUTURE_PREFLIGHT_CANDIDATE | no | low/read-only | NO | YES | HUMAN_PUBLIC_PREFLIGHT_SCOPE_APPROVAL | STOP if response implies auth requirement |
| orderbook quotation | FUTURE_PREFLIGHT_CANDIDATE | no | low/read-only | NO | YES | HUMAN_PUBLIC_PREFLIGHT_SCOPE_APPROVAL | STOP if response implies auth requirement |
| candle quotation | FUTURE_PREFLIGHT_CANDIDATE | no | low/read-only | NO | YES | HUMAN_PUBLIC_PREFLIGHT_SCOPE_APPROVAL | STOP if response implies auth requirement |
| trades/ticks quotation | FUTURE_PREFLIGHT_CANDIDATE | no | low/read-only | NO | YES | HUMAN_PUBLIC_PREFLIGHT_SCOPE_APPROVAL | STOP if response implies auth requirement |
| websocket public quotation if considered | HUMAN_REVIEW_REQUIRED | unknown | medium/streaming control risk | NO | HUMAN_REVIEW | HUMAN_WS_PREFLIGHT_SCOPE_APPROVAL | STOP until websocket safety scope is approved |
| authenticated/private endpoint | HARD_BLOCKED | yes | high/private access risk | NO | NO | OUT_OF_SCOPE_GATE | STOP immediately |
| order create endpoint | HARD_BLOCKED | yes | critical mutation | NO | NO | FORBIDDEN_MUTATION_GATE | STOP immediately |
| order cancel endpoint | HARD_BLOCKED | yes | critical mutation | NO | NO | FORBIDDEN_MUTATION_GATE | STOP immediately |
| account/balance endpoint | HARD_BLOCKED | yes | high private account risk | NO | NO | OUT_OF_SCOPE_GATE | STOP immediately |
| withdrawal/transfer endpoint | HARD_BLOCKED | yes | critical asset movement | NO | NO | FORBIDDEN_ASSET_MOVEMENT_GATE | STOP immediately |
| unknown side-effect endpoint | HARD_BLOCKED | unknown | unknown/high | NO | NO | CLASSIFICATION_REQUIRED_GATE | STOP until classified |

Public endpoint preflight review score measures review, scope, blocker clarity, and safety coverage only; it does not authorize Upbit API calls, credential use, public-data shadow execution, scheduler activation, live trading, WF08, or production readiness.

This document does not authorize live trading, real shadow mode execution, Upbit API access, credential use, scheduler activation, parser execution, fixture creation, WF08 transition, runtime wiring, implementation, or production-readiness claims.

This document does not authorize live trading, shadow mode, Upbit API access, credential use, scheduler activation, parser execution, fixture creation, WF08 transition, runtime wiring, implementation, or production-readiness claims.
