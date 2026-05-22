# KB Investment Automation - Upbit Crypto Automation Build Report

## Status
Rewritten for Upbit crypto automation. Prepared only. Not deployed. Not live-tested.

**Last updated:** 2026-05-09  
**Revision:** v2.1-upbit-accounts-jwt  
**Mode:** validation-first, dry-run-first, live-order-blocked-by-default

## Strategic Change
The project was originally designed for KB Securities stock automation. Because a usable securities API is not available, the system has been converted into an Upbit-based crypto automation planning bundle.

The old KakaoPay -> KB stock migration context is no longer part of active automation execution. It remains historical context only.

## Deliverables

| # | File | New Role |
|---|------|----------|
| 1 | `01_WF_News_Data_Collector.json` | Upbit public market data collector |
| 2 | `02_WF_Candidate_Selector.json` | Crypto candidate selector and scoring skeleton |
| 3 | `03_WF_PreCheck_Engine.json` | Upbit read-only accounts JWT validation and hard STOP gate |
| 4 | `04_WF_Execution_Engine.json` | Upbit order-test/live-order execution shell, blocked by default |
| 5 | `05_WF_Post_Execution.json` | Order result verification and audit log builder |
| 6 | `06_WF_Monitoring_Failsafe.json` | Error incident builder and Telegram alert shell |

## Upbit API References Used
- Upbit Korean API base: `https://api.upbit.com`
- Public market/ticker APIs do not require authentication.
- Private Exchange APIs require JWT authentication.
- Account balance: `GET /v1/accounts`
- Order-related endpoints are intentionally omitted from this phase.

## Safety Posture
- No market orders.
- Limit orders only: `ord_type = limit`.
- KRW markets only by default: examples use `KRW-BTC`, `KRW-ETH`, `KRW-XRP`, `KRW-SOL`.
- No live order unless all of these are true:
  - `precheck_passed === true`
  - `live_order_enabled === true`
  - `execution_mode === "live"`
  - `order_test_passed === true`
  - `ord_type === "limit"`
- No automatic retry loop for orders.
- No live execution during diagnostics.
- Stop on unclear state, missing credentials, API error, rate-limit error, or pending order.

## Required Environment Variables
Do not hardcode these values in workflow JSON.

| Variable | Purpose |
|----------|---------|
| `UPBIT_ACCESS_KEY` | Upbit API access key |
| `UPBIT_SECRET_KEY` | Upbit API secret key |
| `KBIA_TELEGRAM_BOT_TOKEN` | KBIA trading alert bot token |
| `KBIA_TELEGRAM_CHAT_ID` | Telegram chat id for alerts |

## Known Placeholders

| Placeholder | Location | Replacement |
|-------------|----------|-------------|
| `YOUR_LOG_ENDPOINT` | WF05 | Real log destination, DB/webhook/Sheets |
| `UPBIT_ACCESS_KEY` env | WF03/WF04 future auth nodes | Set in n8n environment/credentials |
| `UPBIT_SECRET_KEY` env | WF03/WF04 future auth nodes | Set in n8n environment/credentials |
| Telegram env vars | WF06 | Set in n8n environment/credentials |

## Workflow Summary

### WF01 - Market Data Collector
Collects ticker data for configured KRW markets from Upbit public API. Output is normalized to a single payload containing `tickers`.

### WF02 - Candidate Selector
Scores normalized ticker payloads using placeholder momentum/liquidity logic. It preserves full candidate data and keeps `execution_allowed=false`.

### WF03 - PreCheck Engine
Builds an HS512 Upbit JWT for read-only `GET /v1/accounts`, calls only that endpoint when credentials exist, and emits sanitized telemetry. Missing credentials return `CREDENTIAL_MISSING`. Auth or unexpected account responses return `AUTH_FAILED`. Rate-limit responses return `RATE_LIMITED`. The workflow still keeps trading stopped.

### WF04 - Execution Engine
Contains structurally correct branches for test order and live limit order, but default config blocks all order submission. Live path requires explicit pass flags.

### WF05 - Post Execution
Builds an audit log and checks whether an order is fully filled. Any unfilled, partial, cancelled, unknown, or missing UUID state is treated as not final.

### WF06 - Monitoring Failsafe
Builds incident payloads and sends Telegram alerts using environment variables, not embedded tokens.

## Self-Simulation

### Dry Run
- WF01 public ticker collector: structurally valid.
- WF02 candidate scoring: produces selected candidates but blocks execution.
- WF03 precheck: missing-env simulation returns `CREDENTIAL_MISSING`; all paths keep `precheck_status=stop`.
- WF04 execution: returns blocked payload unless all live gates are explicitly true.
- WF05 logging: identifies full fill only when `state=done` and `remaining_volume=0`.
- WF06 monitoring: sends alert only if Telegram env vars are present.

### Expected Default Outcome
No live trade can occur from the saved files as-is.

## Next Prompt Sequence
1. Configure Upbit credentials securely in n8n environment or credential store.
2. Import WF03 and run read-only accounts validation.
3. Review sanitized telemetry only.
4. Add the next private read-only check only in a later explicitly scoped prompt.
5. Keep live trading disabled.

## Sources
- Upbit API Reference: https://docs.upbit.com/kr/reference
- Upbit order creation: https://docs.upbit.com/kr/v1.5.9/reference/%EC%A3%BC%EB%AC%B8%ED%95%98%EA%B8%B0
- Upbit order test: https://docs.upbit.com/kr/reference/order-test
- Upbit account balance: https://docs.upbit.com/kr/reference/get-balance
- Upbit rate limits: https://docs.upbit.com/kr/reference/rate-limits
