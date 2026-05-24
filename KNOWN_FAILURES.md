# KNOWN_FAILURES

## 2026-05-09 - Upbit Migration Known Failure Modes

### KF-001: Securities API dependency removed
- Previous KB Securities stock automation cannot proceed because there is no available broker API.
- Resolution: Project rewritten to Upbit crypto automation.
- Rule: Do not reuse KB Securities order schema, stock symbols, or account-transfer rules in active workflows.

### KF-002: Hardcoded credentials in workflow JSON
- Prior WF06 contained a hardcoded Telegram bot token.
- Resolution: Upbit v2 workflows use environment variables for Telegram and Upbit credentials.
- Rule: Do not print, log, or embed API keys/tokens in workflow JSON, reports, or telemetry.

### KF-003: Live order risk
- Upbit live order endpoints create real orders.
- Resolution: WF04 is blocked by default and routes only when explicit precheck/test/live gates are satisfied.
- Rule: Do not add order endpoints in the current accounts-validation phase. No market orders. No retry loop.

### KF-004: Pending order ambiguity
- Any unfilled order can distort available balance and create duplicate exposure.
- Resolution: WF03 requires open-order validation; WF05 marks non-final states as STOP.
- Rule: Do not execute if any prior order is unfilled, partial, watch, wait, or unknown.

### KF-005: Upbit rate limit or temporary ban
- Excessive requests can return 429 or 418.
- Resolution: WF06 treats rate-limit patterns as critical and no-retry.
- Rule: Stop immediately on rate-limit signal. Do not retry repeatedly.

### KF-006: JWT query hash mismatch
- Upbit private APIs require JWT with query_hash matching request query/body.
- Resolution: accounts-only JWT helper is wired for no-param `GET /v1/accounts`; no query_hash is used there.
- Rule: Do not reuse the accounts helper unchanged for parameterized private requests.

### KF-007: Credential missing in local environment
- Local validation cannot call Upbit private APIs without `UPBIT_ACCESS_KEY` and `UPBIT_SECRET_KEY`.
- Resolution: helper stops with `CREDENTIAL_MISSING` before any HTTP call.
- Rule: Set credentials only in n8n env/credential store; do not write them into files.

### KF-008: Open order exposure
- Any `GET /v1/orders/open` result for the target market means existing exposure or pending state.
- Resolution: WF03 emits only `open_order_count` and `open_order_exists`; raw order payload is discarded.
- Rule: If `open_order_exists=true`, STOP and do not proceed to the next validation layer.

### KF-009: n8n Code node runner compatibility
- n8n 2.18 task runner does not expose `fetch` in Code nodes and blocks built-in modules unless explicitly allowlisted.
- Resolution: WF03 uses Node built-in `https` instead of `fetch`; manual CLI validation uses `NODE_FUNCTION_ALLOW_BUILTIN=crypto,https`.
- Rule: For `runOnceForEachItem`, return the JSON object directly, not `[{ json: ... }]`.

### KF-010: Upbit invalid access key
- Live n8n execution reached Upbit and returned `401 invalid_access_key` for `GET /v1/accounts`.
- Resolution: Treat as `AUTH_FAILED`; do not continue to open-order or execution layers.
- Rule: Validate the n8n `UPBIT_ACCESS_KEY`, matching secret key, permissions, and IP allowlist without printing or storing secret values.

### KF-011: n8n must not sign Upbit JWT
- n8n Code node sandbox blocks or destabilizes required signing primitives.
- Resolution: Upbit signing moved to the dedicated `upbit-helper` FastAPI service.
- Rule: WF03 n8n Code nodes may normalize telemetry only; no `crypto`, WebCrypto, JWT creation, Authorization header creation, or secret env reads.

### KF-012: Local Docker daemon unavailable
- Local Docker commands fail when Docker Desktop Linux engine is not running.
- Resolution: Docker build/run/health validation must be rerun after starting Docker Desktop or on the n8n host.
- Rule: Do not modify existing `n8n_data` or `reel-service` while starting the separate `upbit-helper` container.

### KF-013: Profit guarantee is impossible
- Any strategy described as guaranteed to profit is unsafe and must be rejected or converted into risk-bounded shadow logic.
- Resolution: Strategy work must define loss limits, no-trade states, STOP guards, and offline validation before any runtime attachment.
- Rule: Never present a trading strategy as risk-free or guaranteed. Keep new strategy logic shadow-only until reconciliation, recovery, logging, alerts, IP allowlist, and live gates are authoritative.

### KF-014: Profitable-trade overfitting
- One or a few profitable trades can be luck, broad market beta, or survivorship bias.
- Resolution: Winning-trade conditions may be recorded only as sanitized features and promoted only after repeated independent examples, loss-case checks, fee/slippage checks, shadow validation, and HQ review.
- Rule: Profit logs alone must never increase live size, order frequency, simultaneous orders, or bypass open-order, stale, spread, maker-limit, asset-balance, cap, fingerprint, or finality gates.

### KF-015: Unsafe autonomy wording
- Requests for profit guarantee, unlimited auto-buy, simultaneous live orders, or guaranteed loss recovery can sound like product requirements but are unsafe trading promises.
- Resolution: Convert those requests into bounded autonomy capabilities: parallel read-only scan, capped staged sizing, helper-gated limit orders, finality-based sequencing, and explicit no-trade states.
- Rule: A 95+ system score may mean automation readiness, not profit certainty. Forbidden capabilities must reduce or block readiness if they are requested as literal runtime behavior.

### KF-016: Stale lock requiring human release
- A live order can outlive the lock expiry window, leaving the helper in `stale_stop` while the order is still open or after it later reaches finality.
- Resolution: The helper may recover a stale lock without an owner token only after read-only evidence proves `open_order_count=0` and the latest matching order is `done` or `cancel`.
- Rule: If any open order exists for the locked market, stale-lock recovery must stay blocked and the coordinator must monitor that open market as the active market.
