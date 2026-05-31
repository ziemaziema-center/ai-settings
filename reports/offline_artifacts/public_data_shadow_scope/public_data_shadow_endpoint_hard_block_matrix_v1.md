# PUBLIC DATA SHADOW ENDPOINT HARD BLOCK MATRIX V1

| endpoint_class | future_status | credential_required | allowed_in_this_run | allowed_in_future_public_data_only_shadow | side_effect_risk | required_gate | STOP_condition |
| --- | --- | --- | --- | --- | --- | --- | --- |
| public quotation/market endpoint class | FUTURE_REVIEW_ONLY | no | NO | HUMAN_REVIEW | low/read-only | HUMAN_PUBLIC_ENDPOINT_SCOPE_APPROVAL | STOP if endpoint not clearly public/read-only |
| account read endpoint class | HARD_BLOCKED | yes | NO | NO | medium-sensitive | OUT_OF_SCOPE_GATE | STOP immediately |
| order inquiry endpoint class | HARD_BLOCKED | yes | NO | NO | medium position-leak | OUT_OF_SCOPE_GATE | STOP immediately |
| order create endpoint class | HARD_BLOCKED | yes | NO | NO | critical mutation | FORBIDDEN_MUTATION_GATE | STOP immediately |
| order cancel endpoint class | HARD_BLOCKED | yes | NO | NO | critical mutation | FORBIDDEN_MUTATION_GATE | STOP immediately |
| wallet/status private endpoint class | HARD_BLOCKED | yes | NO | NO | medium/private | OUT_OF_SCOPE_GATE | STOP immediately |
| withdrawal endpoint class | HARD_BLOCKED | yes | NO | NO | critical asset movement | FORBIDDEN_ASSET_MOVEMENT_GATE | STOP immediately |
| transfer endpoint class | HARD_BLOCKED | yes | NO | NO | critical asset movement | FORBIDDEN_ASSET_MOVEMENT_GATE | STOP immediately |
| deposit/withdrawal address endpoint class | HARD_BLOCKED | yes | NO | NO | high operational risk | FORBIDDEN_ASSET_MOVEMENT_GATE | STOP immediately |
| unknown side-effect endpoint class | HARD_BLOCKED | unknown | NO | NO | unknown/high | CLASSIFICATION_REQUIRED_GATE | STOP until classified |

Public-data shadow scope score measures review, scope, blocker clarity, and safety coverage only; it does not authorize real shadow execution, Upbit API access, credential use, scheduler activation, live trading, WF08, or production readiness.

This document does not authorize live trading, real shadow mode execution, Upbit API access, credential use, scheduler activation, parser execution, fixture creation, WF08 transition, runtime wiring, implementation, or production-readiness claims.

This document does not authorize live trading, shadow mode, Upbit API access, credential use, scheduler activation, parser execution, fixture creation, WF08 transition, runtime wiring, implementation, or production-readiness claims.
