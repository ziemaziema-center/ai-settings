# PUBLIC DATA EXTENDED OBSERVATION PLAN V1

## Scope

- cycles_requested: 56
- requests_per_cycle: 3
- total_request_limit: 168
- market: KRW-BTC
- endpoints:
  - https://api.upbit.com/v1/market/all?isDetails=false
  - https://api.upbit.com/v1/ticker?markets=KRW-BTC
  - https://api.upbit.com/v1/orderbook?markets=KRW-BTC

## Safety Rules

- public quotation GET only
- no auth header
- no credentials / no .env
- no private/account/order endpoints
- no scheduler
- manual/local execution only
- timeout <= 10 seconds
- no retry storm
- local output only

## Output Targets

- public_data_extended_observation_result_v1.json
- public_data_extended_observation_result_v1.md
- extended_daily_digests/cycle_001.md ... cycle_056.md

?쏷his document does not authorize live trading, authenticated real shadow mode execution, Upbit private API access, credential use, scheduler activation, parser execution, fixture creation, WF08 transition, runtime wiring, implementation, or production-readiness claims.??
