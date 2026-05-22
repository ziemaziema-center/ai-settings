# KBIA IQ170 Trader Committee Strategy - 2026-05-19

## Decision

No trading system can be made to guarantee profit. Crypto markets can move violently and unpredictably, and loss of capital is possible. Therefore this implementation converts the request into a risk-first decision engine:

- strong edge required before a buy candidate;
- hard exits defined before entry;
- no order/cancel endpoint access;
- all outputs remain shadow-only until reconciliation, recovery, logging, alerting, IP allowlist, and live gates are authoritative.

Reference basis:
- FINRA warns that crypto assets can move dramatically and unpredictably, with significant loss risk: https://www.finra.org/investors/investing/investment-products/crypto-assets/risks
- Upbit order documentation defines `bid` for buy, `ask` for sell, and limit order parameters; this strategy remains limit-only and does not call the order endpoint: https://global-docs.upbit.com/reference/order

## Brain v2 Committee

The engine now simulates a stronger HQ + trader committee with 21 independent lenses:

1. regime trend;
2. pullback quality;
3. momentum confirmation;
4. liquidity depth;
5. spread/slippage;
6. volatility window;
7. volume participation;
8. reward/risk;
9. portfolio heat;
10. exit discipline.
11. BTC market regime;
12. relative strength;
13. trend maturity;
14. wick rejection;
15. range position;
16. breakout validation;
17. data freshness;
18. spread/liquidity consistency;
19. drawdown state;
20. cooldown clear;
21. correlation heat.

A buy candidate requires staged agreement:

- regime allows buy;
- at least `14/21` committee votes;
- normalized committee score `>=78`;
- risk sizing returns at least `5000 KRW`;
- all hard guards clear.

Any hard guard overrides the committee and returns `STOP`.

## Buy Conditions

All hard guards must pass:

- no open order;
- system stop off;
- workflow and cron inactive;
- live fuse disabled/consumed;
- daily loss above stop threshold;
- spread within limit;
- liquidity above threshold;
- enough candles;
- valid price.

Then committee consensus must pass:

- `SMA5 > SMA20 > SMA50`;
- pullback from 20-day high is present but not a breakdown;
- RSI is constructive, not euphoric;
- ATR is tradable, not dead or unstable;
- KRW liquidity is sufficient;
- spread is tight;
- volume is not weak;
- reward/risk is acceptable;
- portfolio heat is low.
- BTC or benchmark regime is not bearish;
- candidate has relative strength;
- price is not too extended from SMA20;
- latest candle does not show heavy upper-wick rejection;
- range position is not chase-like unless breakout is confirmed;
- data is fresh, sorted, and non-duplicated;
- spread is consistent with liquidity;
- recent losses/cooldown/correlation heat do not block risk.

## Stop / No-Trade Conditions

Brain v2 stops or holds on:

- stale candle data;
- unsorted or duplicate candles;
- single-candle shock;
- open order exists;
- unresolved previous decision;
- system/manual/news block;
- workflow or cron active;
- live fuse not disabled/consumed;
- daily loss limit hit;
- max consecutive shadow losses;
- recent loss cooldown;
- spread too wide;
- liquidity too low;
- insufficient candles;
- invalid price;
- non-authoritative account state;
- locked balance exists;
- missing/crossed/adverse orderbook when orderbook is required;
- panic, parabolic, bear, chop, or unknown regime.

## Sell Conditions

Sell candidate is produced when a held position triggers any of:

- hard stop loss;
- take profit;
- trailing stop;
- trend break.
- break-even protect;
- time stop;
- volatility expansion exit;
- lower-high exit;
- failed breakout exit;
- regime flip exit;
- exposure reduction;
- liquidity dry-up exit.

The output is still a candidate only. It does not cancel, sell, or call Upbit.

## Risk Policy

- max risk per trade: `0.5%` of equity;
- max position allocation: `10%` of equity;
- max daily loss: `1.5%`;
- hard stop loss: `1.8%`;
- trailing stop: `1.4%`;
- take profit: `3.2%`;
- safe order band: `5000-10000 KRW`;
- order type: limit only.

Brain v2 sizing explains:

- base risk KRW;
- confidence multiplier;
- volatility multiplier;
- drawdown multiplier;
- spread multiplier;
- loss multiplier;
- final shadow KRW.

## Implementation

- strategy kernel: `strategy/kbia_strategy_kernel.py`
- offline tests: `tests/test_kbia_strategy_kernel.py`
- validation runner: `tmp/run_strategy_validation_20260519.py`
- schema: `kbia.strategy_brain.v2`

## Safety Result

- live order submitted: `false`
- cancel attempted: `false`
- reorder attempted: `false`
- workflow activation changed: `false`
- cron enabled: `false`
- helper runtime changed: `false`
- secret exposure: `false`

## Validation Result

- local 3-loop validation: `PASS`
- EC2 bounded workspace 3-loop validation: `PASS`
- Brain v2 local and EC2 3-loop validation: `PASS`
- WF05 offline regression in both environments: `12/12`, `network_used=false`

## Final Status

The strategy layer is complete as a dependency-free offline decision engine. It is not attached to live execution because the project remains in controlled STOP state and Upbit private read authority is still not fully authoritative.
