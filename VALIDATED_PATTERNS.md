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

## VP-016: Autonomous scorecard governor

- A 95+ readiness score must be calculated from explicit safety, execution, portfolio, data, strategy, news, learning, observability, finality, and deployment sections.
- The scorecard may approve bounded autonomy only when market orders, auto-cancel, secret exposure, gate bypass, simultaneous live orders, and profit guarantees remain blocked.
- Valid automation pattern is parallel scanning with single live limit order sequencing until finality.
- Runtime state should record the current `autonomy_scorecard` so the operator can see whether the system is ready, blocked, or degraded.
- Forbidden capability requests must be documented as blockers or converted into safe equivalents before runtime activation.

## VP-017: Self-running stale lock recovery

- A stale execution lock may be recovered automatically only through `POST /execution-lock/recover-stale-finality`.
- Recovery requires:
  - stale lock state,
  - no partial lock writes,
  - supported KRW market,
  - `ord_type=limit`,
  - open-order telemetry for the locked market returning `open_order_count=0`,
  - latest matching closed order classified as `done` or `cancel`,
  - workflow and cron flags false.
- If the locked market still has an open order, recovery is blocked and the coordinator must update `active_market` to the open market and keep read-only monitoring.
- The recovery path must not submit orders, cancel orders, expose owner tokens, expose raw Upbit payloads, or bypass finality.

## VP-018: Bounded stale limit cancel/reprice

- A stale open order may be cancelled only through `POST /upbit/cancel-stale-order/telemetry`.
- Cancel gate requires:
  - supported cleanup market,
  - `side=ask`,
  - `ord_type=limit`,
  - exactly one open order,
  - order state `wait`,
  - executed volume `0`,
  - remaining volume positive,
  - created_at parsed and older than the configured minimum age,
  - matching active or stale execution lock,
  - workflow/cron/system stop safe flags,
  - one-time cancel flag.
- Helper may use the raw Upbit UUID only internally for `DELETE /v1/order`; responses must expose only `uuid_masked`.
- After a cancel attempt, the coordinator must re-read finality before any next live order.
- Reprice is not market order chasing: the next order still goes through sell-test, fresh orderbook, spread, maker-limit, balance, lock, and live-sell gates.

## VP-019: CI-portable validation scripts

- CI-covered Python validation scripts should derive the repository root from the script location, not from a local workstation path.
- Use `Path(__file__).resolve().parents[n]` when the script lives inside the repository and all target files are repo-relative.
- When a validation script writes evidence files, rerun it locally and in GitHub Actions after path portability changes.

## VP-020: Opportunity-cost aware autonomy

- `time = money` is a permanent operating rule for the trading system.
- No-trade is not automatically success; repeated no-candidate cycles must be recorded as opportunity-cost pressure.
- Opportunity-cost pressure may:
  - prioritize legacy-capital cleanup candidates,
  - increase monitoring attention,
  - trigger bounded strategy review,
  - require a clear reason for continued idle state.
- Opportunity-cost pressure must not:
  - force market orders,
  - loosen spread/freshness gates without a tested code change,
  - bypass helper live gates,
  - allow simultaneous live orders,
  - treat profit as guaranteed.
- When opportunity-cost pressure is high, the validated runtime action is scan acceleration only:
  - set `opportunity_cost_pressure.level=HIGH`,
  - set `recommended_sleep_seconds=60`,
  - keep `bypass_gates_allowed=false`,
  - keep live execution limited to the existing helper-gated single-order path.

## VP-020: Static local SEO generation and validation

- For Korean local SEO sites, generate pages from structured route/content data instead of editing dozens of pages manually.
- Preserve the prior static site with a timestamped backup before overwriting public entry files.
- Generate canonical URLs, robots.txt, sitemap.xml, llms.txt, LocalBusiness/FAQ/Breadcrumb/BlogPosting JSON-LD, and internal links in one build step.
- Validate all generated HTML for UTF-8 mojibake markers, canonical tags, parseable JSON-LD, sitemap coverage, and at least one rendered smoke test across desktop and mobile routes.
- Review/trust sections must summarize real review themes without inventing fake review bodies.

## VP-021: GitHub Pages custom-domain HTTPS recovery

- If DNS points correctly to GitHub Pages but HTTPS returns certificate subject mismatch, inspect `GET /repos/{owner}/{repo}/pages`.
- If `https_enforced=false` and enabling HTTPS fails with `The certificate does not exist yet`, re-save the custom domain and source first.
- If no certificate appears, perform a controlled custom-domain reset/re-add in Pages settings.
- Wait for `https_certificate.state=approved`, then enable `https_enforced=true`.
- Verify with:
  - Pages API `html_url=https://...`,
  - `https_enforced=true`,
  - HTTPS sitemap `200 OK`,
  - HTTP sitemap `301` to HTTPS,
  - robots.txt includes the HTTPS sitemap directive.
