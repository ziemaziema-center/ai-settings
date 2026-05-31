# PUBLIC DATA N DAY SHADOW RECORDER RUN PLAN V1

## 1. Status

- run_id: PUBLIC_DATA_N_DAY_SHADOW_RECORDER_RUN
- status: APPROVED_AND_EXECUTING

## 2. Approved Scope

- public-data-only observation run
- public quotation endpoints only
- local/manual one-shot execution only
- no authenticated shadow execution
- no live trading

## 3. N-Cycle Definition

- cycles_requested: 14
- cycle_behavior: each cycle performs up to 3 public GET requests

## 4. Public Endpoint Limits

- allowed endpoints:
  - `https://api.upbit.com/v1/market/all?isDetails=false`
  - `https://api.upbit.com/v1/ticker?markets=KRW-BTC`
  - `https://api.upbit.com/v1/orderbook?markets=KRW-BTC`
- request limit per cycle: 3
- total request limit: 42
- timeout per request: 10 seconds

## 5. Manual Execution Boundary

- manual local script invocation only
- no background process
- no daemon
- no scheduler

## 6. Auth Header Prohibition

- `Authorization` header is prohibited
- authenticated/private API calls are prohibited

## 7. Credential Prohibition

- no credential read
- no `.env` read
- no keyring or credential-manager access
- no environment-secret access

## 8. Private/Order Endpoint Prohibition

- account/private/order/withdraw/transfer endpoints are hard-blocked
- unknown side-effect endpoint class is hard-blocked

## 9. Recorder Behavior

- capture public observation evidence only
- do not produce exchange submission actions
- all hypothetical submissions are `STUBBED_NOT_SENT`

## 10. Daily Digest Behavior

- emit `day_01.md` through `day_14.md`
- include cycle status, endpoint statuses, and stubbed-not-sent state

## 11. STOP Conditions

- wrong working directory
- endpoint class outside allow-list
- non-GET request attempt
- auth header injection attempt
- request limits exceeded
- scheduler/background invocation attempt

## 12. Remaining Blockers

- authenticated shadow execution: BLOCKED
- live trading: BLOCKED
- WF08 transition: BLOCKED
- credentials: BLOCKED

## 13. Final Safety Verdict

This run is a public-data-only observation recorder and is not live trading, not authenticated real shadow mode, and not an authorization expansion for private endpoints, runtime wiring, or production readiness.

?쏷his document does not authorize live trading, real shadow mode execution beyond approved public-data recorder observation, Upbit private API access, credential use, scheduler activation, parser execution, fixture creation, WF08 transition, runtime wiring, implementation, or production-readiness claims.??
