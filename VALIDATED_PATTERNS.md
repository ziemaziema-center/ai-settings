# VALIDATED_PATTERNS

## VP-001: Validation-first trading workflow
- Collect data.
- Select candidate as reference only.
- Precheck blocks by default.
- Test order before live order.
- Live order only after explicit gates.
- Post-execution checks must confirm final state before any next order.

## VP-002: Upbit safe order constraints
- Use Korean Upbit base URL: `https://api.upbit.com`.
- Default markets use `KRW-*`.
- Only `ord_type=limit`.
- Side values must be `bid` or `ask`.
- Market order types `price`, `market`, and `best` are disallowed for now.

## VP-003: Credential handling
- Use n8n environment variables or credential store.
- Required env vars:
  - `UPBIT_ACCESS_KEY`
  - `UPBIT_SECRET_KEY`
  - `KBIA_TELEGRAM_BOT_TOKEN`
  - `KBIA_TELEGRAM_CHAT_ID`
- Do not print tokens or secrets.

## VP-004: Upbit endpoint sequence
- Public market/ticker collection can run without auth.
- Current private read check:
  - `GET /v1/accounts`
- Order-related endpoints are intentionally omitted from this phase.

## VP-005: Post-execution finality
- `state=done`, `remaining_volume=0`, and `executed_volume>0` means fully filled.
- `wait`, `watch`, nonzero `remaining_volume`, missing UUID, or unknown state means STOP.

## VP-006: Upbit accounts JWT helper
- Use HS512.
- Do not base64-decode the Secret Key.
- For `GET /v1/accounts`, payload includes `access_key` and UUID `nonce` only.
- No `query_hash` is used because the request has no params.
- Sanitized telemetry only: timestamp, endpoint, status, success, account count, currencies, error code/message, and Remaining-Req.

## VP-007: Upbit open-order read-only validation
- Endpoint: `GET /v1/orders/open`.
- Query target market only when available, for example `market=KRW-BTC`.
- When query params are used, JWT payload must include SHA512 `query_hash` and `query_hash_alg=SHA512`.
- Do not emit JWT, Authorization header, or raw order payload.
- Sanitized telemetry only: timestamp, endpoint, market, status, success, open order count, open order exists, Remaining-Req, sanitized error.
- PreCheck stops when any open order exists for the target market.

## VP-008: n8n 2.18 Code node compatibility
- `runOnceForEachItem` Code nodes must return a plain object; `runOnceForAllItems` Code nodes may return item arrays.
- JS task runner requires built-in modules to be allowlisted with `NODE_FUNCTION_ALLOW_BUILTIN`.
- WF03 private read checks use built-in `crypto` and `https` only.
- WF03 must route to `Precheck STOP Payload` in this phase regardless of local check results.

## VP-009: Upbit helper microservice boundary
- Upbit signing runs only inside `upbit-helper`.
- n8n calls helper HTTP telemetry endpoints only.
- Helper returns sanitized telemetry fields only and never returns JWT, Authorization headers, balances, or raw orders.
- Bind host publishing to `127.0.0.1:8010` and connect n8n to the helper over a Docker network as `http://upbit-helper:8010`.

## VP-010: One-time manual live order fuse
- WF04 remains inactive and manual-trigger only.
- WF04 must not call Upbit directly; it may call only the helper live telemetry endpoint.
- Live path defaults are `live_order_enabled=false`, `execution_allowed=false`, `execution_mode=dry_run`, and `one_time_live_attempt_allowed=false`.
- A live attempt requires explicit live flags, `all_pass=true`, KRW-BTC bid limit order, 5000-10000 KRW estimate, duplicate lock clear, no open order, system stop off, and passed order-test telemetry.
- WF04 consumes the one-time live attempt fuse before the helper live HTTP call, then emits `live_path_auto_disabled=true` and `LIVE_ATTEMPT_CONSUMED`.
- Any consumed fuse, missing live flag, unsafe order shape, open order, duplicate lock, system stop, or failed order test stops before `/v1/orders`.

## VP-011: Offline trader-committee strategy brain
- Strategy logic can be advanced safely as a dependency-free offline decision engine.
- Use committee scoring, hard guards, position sizing, and exit rules to emit `BUY_CANDIDATE`, `SELL_CANDIDATE`, `HOLD`, or `STOP`.
- Strategy outputs must keep `execution_allowed=false`, `live_order_allowed=false`, `automation_allowed=false`, `order_endpoint_allowed=false`, and `cancel_endpoint_allowed=false`.
- Validate with three loops of py_compile, strategy tests, and WF05 offline regression before storing as ready for shadow-only use.
- Brain v2 uses staged `regime -> setup -> trigger -> risk` gating, 21 committee lenses, optional multi-timeframe inputs, orderbook/account/data-freshness guards, richer exit reasons, and sizing explanation.

## VP-012: Portfolio shadow liquidation brain
- Long-held losing portfolios should be converted into a shadow-only cleanup plan before any live sell decision.
- Do not panic liquidate core liquid assets. Treat BTC and ETH as core anchors and SOL as high-beta core-growth unless a separate live exit gate is passed.
- Recycle capital from severe drawdown legacy/tail alts through staged cleanup candidates, not market dumps.
- The output must classify each asset as `KEEP_CORE`, `KEEP_OR_TRIM_ON_BOUNCE`, `REDUCE_STAGED`, `EXIT_STAGED`, or `REVIEW`, with first-slice and total shadow values.
- Portfolio cleanup outputs must keep `execution_allowed=false`, `live_sell_allowed=false`, `automation_allowed=false`, `order_endpoint_allowed=false`, `cancel_endpoint_allowed=false`, `market_sell_allowed=false`, and `scheduler_allowed=false`.
- Validate with three loops of py_compile, strategy tests, portfolio liquidation tests, and WF05 offline regression before storing evidence or using in bounded shadow runs.
- Brain v3 adds three HQ upgrade layers: market-regime overlay, HQ/agent committee asset scoring, and execution-quality slice scheduling.
- Unknown assets must route to classification review, not automatic liquidation.
- First cleanup slices must be capped by bid-side orderbook depth and blocked when orderbook data is missing.
- Portfolio outputs should include `plan_valid` and `validation_errors` for duplicate markets, negative values, total mismatch, core-floor breach, daily-cap breach, and unknown-asset planned slices.

## VP-013: Daily credible crypto news brain
- The trading brain can consume a daily news context layer, but it must be reference-only and never directly trigger execution.
- Use multiple public RSS sources, source credibility weights, dedupe, watch-symbol extraction, risk tags, and daily brain bias.
- Track at least BTC, ETH, SOL, ETC, DOGE, DOT, ALGO, and FCT2.
- Output `daily_brain_bias` such as `NORMAL_REFERENCE`, `EVENT_RISK_REFERENCE`, or `DEFENSIVE_REFERENCE`.
- News outputs must keep `execution_allowed=false`, `live_order_allowed=false`, `live_sell_allowed=false`, `automation_allowed=false`, `order_endpoint_allowed=false`, `cancel_endpoint_allowed=false`, `market_sell_allowed=false`, and project `scheduler_allowed=false`.
- Validate parser/scoring/digest logic offline before running a bounded public RSS digest.

## VP-014: Winning-trade learning as bounded reference
- Completed profitable trades may be converted into sanitized feature observations.
- Repeated winning patterns may influence Brain scoring only after loss-case review, fee/slippage checks, shadow validation, and HQ review.
- Promotion levels are `OBSERVED_WIN`, `REPEATED_WIN_PATTERN`, `VALIDATED_EDGE_CANDIDATE`, and `LIVE_WEIGHT_APPROVED`.
- Pattern reinforcement must remain a bounded reference score bonus and must keep all execution/order/cancel/scheduler capability flags false.
- Winning-trade learning must never bypass live gates, increase live size from profit alone, enable simultaneous orders from profit alone, or continue trading after non-final order states.
# VP-015 - Bounded live buy helper gate

- Status: validated locally and remotely on 2026-05-22.
- Live buy support must be split into:
  1. `buy-test` endpoint for Upbit test order validation.
  2. `live-buy` endpoint for the final live order attempt.
- The live-buy endpoint must require all of the following:
  - allowlisted major KRW market only,
  - `side=bid`,
  - `ord_type=limit`,
  - KRW value between the minimum order size and the hard max slice,
  - open order count clear,
  - KRW balance sufficient,
  - Brain v4 `BUY_CANDIDATE`,
  - Brain live-ready,
  - score threshold,
  - non-defensive news,
  - scalping candidate,
  - fresh orderbook,
  - spread cap,
  - maker-limit price,
  - prior buy-test pass with matching fingerprint,
  - duplicate lock clear,
  - system stop false,
  - one-time live fuse.
- Profit logs, user urgency, or opportunity cost must not bypass this helper gate.
