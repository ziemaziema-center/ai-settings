# PUBLIC DATA LONG OBSERVATION PLAN V1

## Objective
- Continue public-data-only evidence gathering without crossing hard authorization gates.

## Requested Window
- default_target_cycles: 112
- selected_cycles_for_this_run: 56
- selection_reason: Keep request budget conservative (168 requests) to avoid rate-discipline overreach while preserving comparability with prior successful extended observation.

## Execution Constraints
- requests_per_cycle: 3
- total_max_requests_this_run: 168
- endpoints: /v1/market/all?isDetails=false, /v1/ticker?markets=KRW-BTC, /v1/orderbook?markets=KRW-BTC
- method: GET only
- no credentials / no auth header / no private endpoints
- no scheduler / no background process / local outputs only
- timeout_seconds: <=10

?쏷his document does not authorize live trading, authenticated real shadow mode execution, Upbit private API access, credential use, scheduler activation, parser execution, fixture creation, WF08 transition, runtime wiring, implementation, or production-readiness claims.??
