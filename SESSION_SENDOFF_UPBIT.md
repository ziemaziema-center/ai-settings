# SESSION_SENDOFF - KBIA Upbit Crypto Automation

## Current Project State
KB Investment Automation has been migrated from KB Securities stock automation planning to Upbit crypto automation planning.

## Working Directory
`C:\Users\minho\Documents\02_work\03_AI\03_investment_automation\01_planning`

## Current Files
- `KBIA_Workflow_Build_Report.md`
- `SESSION_BOOT.md`
- `KNOWN_FAILURES.md`
- `VALIDATED_PATTERNS.md`
- `PATCH_HISTORY.md`
- `DAILY_EXECUTION_LOG.md`
- `workflows/01_WF_News_Data_Collector.json`
- `workflows/02_WF_Candidate_Selector.json`
- `workflows/03_WF_PreCheck_Engine.json`
- `workflows/04_WF_Execution_Engine.json`
- `workflows/05_WF_Post_Execution.json`
- `workflows/06_WF_Monitoring_Failsafe.json`

## Important Rules
- Do not print or embed API keys/tokens.
- Do not place live Upbit keys inside workflow JSON.
- Use env vars or n8n credentials:
  - `UPBIT_ACCESS_KEY`
  - `UPBIT_SECRET_KEY`
  - `KBIA_TELEGRAM_BOT_TOKEN`
  - `KBIA_TELEGRAM_CHAT_ID`
- No market orders.
- Limit orders only.
- No automatic retry loop.
- Stop on unclear state, pending order, partial fill, API error, rate-limit, or missing credential.
- Do not add any order endpoint until a later explicitly scoped prompt.

## Upbit API Context
- Base URL: `https://api.upbit.com`
- Public endpoints:
  - `GET /v1/market/all?isDetails=true`
  - `GET /v1/ticker?markets=KRW-BTC,KRW-ETH`
- Private endpoints:
  - `GET /v1/accounts`
- Order-related endpoints are intentionally omitted from this phase.
- Private endpoints require JWT auth.
- JWT must include `access_key`, unique `nonce`, and `query_hash` for requests with query/body.

## Workflow Intent
1. WF01 collects public Upbit ticker/market data.
2. WF02 scores KRW crypto candidates but keeps execution blocked.
3. WF03 builds an HS512 JWT and validates read-only Upbit accounts when env credentials exist. It still remains STOP.
4. WF04 contains disabled placeholders for order endpoints in this phase and is blocked by default.
5. WF05 validates order finality and blocks if any order is unfilled.
6. WF06 alerts via Telegram using env vars.

## Next Prompt Recommendation
Start with:

```text
Configure Upbit env vars in n8n and run WF03 read-only accounts validation. Do not add or call order endpoints.
```
