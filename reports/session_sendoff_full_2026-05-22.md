# KBIA Upbit Automation Sendoff Packet - 2026-05-22

## Current Status

- Project: KBIA Upbit crypto automation.
- Current mode: gated full automation, sell-cleanup focused.
- Remote tmux session: `kbia-full-auto`.
- Remote runner: `/tmp/kbia_full_automation_coordinator_20260520.py`.
- Remote state: `/home/ubuntu/kbia-logs/full-automation/state.json`.
- Remote events: `/home/ubuntu/kbia-logs/full-automation/events.jsonl`.
- Last observed remote cycle: `54` at `2026-05-22T01:36:19+09:00`.
- Open orders: `0` across BTC, ETC, DOT, FCT2, ALGO, DOGE.
- Completed cleanup sells: `KRW-ETC`, `KRW-DOT`.
- Remaining cleanup candidates: `KRW-FCT2`, `KRW-ALGO`, `KRW-DOGE`.
- Current blockers: FCT2/DOGE spread too wide; ALGO stale or spread too wide.
- Buy branch: blocked until valid Brain candidate and live buy gates exist.

## Safety Contract

- No market orders.
- No automatic cancels.
- No retry or reorder loops.
- One order at a time.
- Any open/wait/watch/partial/unknown state means read-only stop.
- Helper owns Upbit signing.
- n8n must not sign Upbit JWT.
- No secret, JWT, Authorization header, raw account payload, raw order payload, or full UUID exposure.
- Trading capability flags remain false in Brain/news/learning outputs unless a separately validated helper gate explicitly executes.

## Live Sell Helper

Implemented and deployed helper endpoints:

- `POST /upbit/sell-test/telemetry`
- `POST /upbit/live-sell/telemetry`

Helper live sell constraints:

- Allowlist only: `KRW-FCT2`, `KRW-DOT`, `KRW-ALGO`, `KRW-ETC`, `KRW-DOGE`.
- `side=ask` only.
- `ord_type=limit` only.
- Market orders rejected.
- Estimated KRW range: `5000` to `30000`.
- Requires asset balance, no open orders, fresh orderbook, maker price above best bid, spread gate, sell-test fingerprint, and one-time fuse.

Deployment evidence:

- Backup: `/home/ubuntu/kbia_backups/upbit-helper-live-sell-20260520_171539`.
- Rollback image: `upbit-helper:rollback-live-sell-20260520_171539`.
- Smoke tests passed: health ok, market order blocked, wrong side blocked, live sell blocked without flags.

## Completed Live Cleanup Sells

### ETC

- Market: `KRW-ETC`.
- Type: limit ask.
- Price: `13260`.
- Volume: `2.18702865`.
- Estimated value: about `29,000 KRW`.
- Final state: `done`.
- Open orders after finality: `0`.
- Report: `reports/etc_live_sell_finality_done_2026-05-20.md`.

### DOT

- Market: `KRW-DOT`.
- Type: limit ask.
- Price: `1843`.
- Volume: `15.73521432`.
- Estimated value: about `29,000 KRW`.
- Final state: `done`.
- Trades count: `2`.
- Open orders after finality: `0`.
- Report: `reports/dot_live_sell_finality_done_2026-05-20.md`.

## Running Full Automation

Current remote runner behavior:

- Checks helper health.
- Reads open orders for watched markets.
- If any open order exists, stays read-only and checks finality.
- If no open order exists, tries cleanup candidates one by one.
- Runs sell-test first.
- Calls live-sell only if sell-test passes.
- Stops after one accepted live order until finality.

Current limitation:

- The remote coordinator is a standalone sell-cleanup runner.
- It does not import the local Brain v4.1 module yet.
- Brain v4.1 is completed locally as shadow/reference logic, not connected to remote live buy execution.

## Brain v4.1

Current schema:

- `kbia.strategy_brain.v4.1`.

Added layers:

- News-aware senior trader council.
- Whale money operator liquidity gate.
- Conservative scalping shadow/reference layer.
- Validated edge-learning reference layer.

Important behavior:

- Brain v4.1 can emit stronger shadow/reference scoring.
- It still keeps `execution_allowed=false`.
- It still keeps `live_order_allowed=false`.
- It still keeps `order_endpoint_allowed=false`.
- It still keeps `cancel_endpoint_allowed=false`.
- It cannot bypass live helper gates.

Report:

- `reports/brain_v4_1_shadow_upgrade_2026-05-22.md`.
- `reports/brain_v4_1_shadow_upgrade_2026-05-22.json`.

## Conservative Scalping Shadow Layer

Purpose:

- Find short-term candidate quality without opening live buy execution.

Gates:

- Tight spread.
- Volume confirmation.
- Bid support.
- Regime alignment.
- Momentum alignment.
- Open-order clear.
- News not defensive.

Hard limits:

- Cannot execute live.
- Cannot increase order frequency.
- Cannot enable simultaneous orders.
- Cannot bypass stale/spread/open-order/maker/fingerprint gates.

## Winning-Trade Learning

New module:

- `strategy/kbia_trade_learning.py`.

New test:

- `tests/test_kbia_trade_learning.py`.

Purpose:

- Record conditions from materially profitable completed trades.
- Detect repeated common patterns.
- Promote only validated patterns into bounded Brain reference weights.

Promotion levels:

- `OBSERVED_WIN`: observed one or more profitable examples; log only.
- `REPEATED_WIN_PATTERN`: repeated examples; can influence commentary/shadow scores.
- `VALIDATED_EDGE_CANDIDATE`: passed loss-case and shadow validation; can add bounded score weight.
- `LIVE_WEIGHT_APPROVED`: only after explicit validation and telemetry update; still cannot bypass gates.

Forbidden:

- One profitable trade as proof of edge.
- Profit logs alone increasing live size.
- Profit logs alone enabling simultaneous orders.
- Profit logs bypassing safety gates.
- Profit guarantees.

Memory added:

- `KNOWN_FAILURES.md`: `KF-014 Profitable-trade overfitting`.
- `VALIDATED_PATTERNS.md`: `VP-014 Winning-trade learning as bounded reference`.

## Self-Improving Skill

Skill path:

- `.agents/skills/self-improving-trading/SKILL.md`.

Current behavior:

- Classifies blockers as safety, technical, market-state, or operator blockers.
- Calls HQ/agents when live trading blocker is nontrivial or requested.
- Allows only safety-preserving patches.
- Allows one safe precheck or sell-test retry after a validated patch.
- Records profitable-trade features and promotes repeated validated patterns.
- Forbids bypassing live safety gates.

## News Brain

Today's digest:

- Date: `2026-05-22`.
- Bias: `DEFENSIVE_REFERENCE`.
- Items scanned: `100`.
- Source failures: `0`.
- Top symbols: BTC, ETH, SOL, DOGE.

Outputs:

- `reports/daily_crypto_news_digest_2026-05-22.md`.
- `reports/daily_crypto_news_digest_2026-05-22.json`.

Effect:

- Brain should treat today as defensive/reference only.
- Buy branch should remain blocked.

## Validation Completed

Commands passed:

- `python tmp/run_daily_news_digest.py`.
- `python -m py_compile strategy/kbia_strategy_kernel.py strategy/kbia_trade_learning.py tests/test_kbia_strategy_kernel.py tests/test_kbia_trade_learning.py tmp/run_daily_news_digest.py`.
- `python tests/test_kbia_trade_learning.py`.
- `python tests/test_kbia_news_brain.py`.
- `python tests/test_kbia_strategy_kernel.py`.
- `python tests/test_kbia_portfolio_liquidation_brain.py`.
- `python tests/wf05_offline_regression_runner_2026-05-11.py` -> `12/12`.
- `python tmp/run_strategy_validation_20260520.py` -> `loops=3`.
- `python tmp/run_brain_v4_1_shadow_upgrade_20260522.py`.

Known validation caveat:

- Skill `quick_validate.py` failed earlier because local Python is missing `yaml` module.
- Manual skill validation passed.

## Important Files

Core memory:

- `KNOWN_FAILURES.md`.
- `VALIDATED_PATTERNS.md`.
- `PATCH_HISTORY.md`.
- `DAILY_EXECUTION_LOG.md`.
- `SESSION_BOOT.md` is stale for current runtime and should not override latest remote state.

Strategy:

- `strategy/kbia_strategy_kernel.py`.
- `strategy/kbia_trade_learning.py`.
- `strategy/kbia_news_brain.py`.
- `strategy/kbia_portfolio_liquidation_brain.py`.

Tests:

- `tests/test_kbia_strategy_kernel.py`.
- `tests/test_kbia_trade_learning.py`.
- `tests/test_kbia_news_brain.py`.
- `tests/test_kbia_portfolio_liquidation_brain.py`.
- `tests/wf05_offline_regression_runner_2026-05-11.py`.

Runners:

- `tmp/kbia_full_automation_coordinator_20260520.py`.
- `tmp/run_daily_news_digest.py`.
- `tmp/run_brain_v4_1_shadow_upgrade_20260522.py`.
- `tmp/run_strategy_validation_20260520.py`.

Reports:

- `reports/full_automation_gated_start_2026-05-20.md`.
- `reports/etc_live_sell_finality_done_2026-05-20.md`.
- `reports/dot_live_sell_finality_done_2026-05-20.md`.
- `reports/daily_crypto_news_digest_2026-05-22.md`.
- `reports/brain_v4_1_shadow_upgrade_2026-05-22.md`.

## Remote Commands

Check full automation:

```powershell
ssh -i "C:\Users\minho\Downloads\n8n-key.pem" ubuntu@43.201.227.194 "tmux has-session -t kbia-full-auto && echo RUNNING || echo NOT_RUNNING; cat /home/ubuntu/kbia-logs/full-automation/state.json; tail -n 20 /home/ubuntu/kbia-logs/full-automation/events.jsonl"
```

Check helper health:

```powershell
ssh -i "C:\Users\minho\Downloads\n8n-key.pem" ubuntu@43.201.227.194 "curl -sS http://127.0.0.1:8010/health"
```

Stop full automation only if explicitly requested:

```powershell
ssh -i "C:\Users\minho\Downloads\n8n-key.pem" ubuntu@43.201.227.194 "tmux kill-session -t kbia-full-auto"
```

## GitHub Status

- Main project folder is not a git repository.
- Existing git repo found only under `ai-settings`.
- `ai-settings` was previously pushed to `ziemaziema-center/ai-settings`, branch `main`, commit `448a60b`.
- The full trading project has not been pushed because it is not initialized/connected to a remote repository.

## Next Work

Recommended next steps:

1. Keep current full automation running while FCT2/ALGO/DOGE wait for better spread/fresh orderbook.
2. Add a remote read-only Brain v4.1 shadow observer that writes signals without executing orders.
3. Only after shadow observer is stable, wire Brain v4.1 candidate output into the coordinator as read-only telemetry.
4. Design live buy helper gates separately; do not reuse sell helper blindly.
5. Do not enable simultaneous orders until per-market finality, exposure locks, and shadow validation exist.

## Final Operating Posture

- Live cleanup automation is running.
- DOT and ETC cleanup sells are done.
- Remaining cleanup is gated by market quality.
- Brain v4.1 is locally upgraded and validated as shadow/reference.
- Winning-trade learning is implemented as bounded reference memory.
- Buy branch remains intentionally locked.
- System is safe, but not yet a fully autonomous buy/sell trading bot.
