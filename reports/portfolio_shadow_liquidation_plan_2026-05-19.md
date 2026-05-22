# Portfolio Shadow Liquidation Plan - 2026-05-19

- mode: `portfolio_shadow_liquidation_plan`
- portfolio_action: `CLEANUP_SHADOW_ONLY`
- schema_version: `kbia.portfolio_liquidation_brain.v3`
- plan_valid: `True`
- validation_errors: `none`
- market_regime: `NEUTRAL`
- total_value_krw: `3583421.0`
- cash_krw: `14272.0`
- cash_pct: `0.004`
- core_pct: `0.6685`
- planned_first_slice_krw: `272922.0`
- planned_total_shadow_sell_krw: `516996.0`
- exit_candidates: `FCT2, DOT, ALGO, ETC`
- reduce_candidates: `DOGE`
- keep_candidates: `SOL, BTC, ETH`

## Position Decisions

| symbol | action | hq_score | exec_profile | first_slice_krw | total_shadow_sell_krw | reason |
| --- | --- | ---: | --- | ---: | ---: | --- |
| `FCT2` | `EXIT_STAGED` | `72.86` | `CAUTIOUS_CLEANUP` | `55588.0` | `77823.0` | `CAPITAL_RECYCLING_FROM_DEAD_ALT` |
| `DOT` | `EXIT_STAGED` | `61.43` | `CAUTIOUS_CLEANUP` | `34029.0` | `47640.0` | `CAPITAL_RECYCLING_FROM_DEAD_ALT` |
| `ALGO` | `EXIT_STAGED` | `55.71` | `CAUTIOUS_CLEANUP` | `21493.0` | `30090.0` | `CAPITAL_RECYCLING_FROM_DEAD_ALT` |
| `ETC` | `EXIT_STAGED` | `91.43` | `CAUTIOUS_CLEANUP` | `99816.0` | `299447.0` | `CAPITAL_RECYCLING_FROM_DEAD_ALT` |
| `DOGE` | `REDUCE_STAGED` | `47.14` | `CAUTIOUS_CLEANUP` | `61996.0` | `61996.0` | `LIMIT_FIRST_SLICE_BECAUSE_LIQUIDITY_WEAK,MEME_EXPOSURE_NOT_CORE_CAPITAL` |
| `SOL` | `KEEP_OR_TRIM_ON_BOUNCE` | `44.29` | `NO_ACTION` | `0.0` | `0.0` | `SOL_HIGH_BETA_CORE_GROWTH_NOT_PANIC_EXIT` |
| `BTC` | `KEEP_CORE` | `35.71` | `NO_ACTION` | `0.0` | `0.0` | `BTC_ETH_CORE_LIQUIDITY_ANCHOR` |
| `ETH` | `KEEP_CORE` | `37.14` | `NO_ACTION` | `0.0` | `0.0` | `BTC_ETH_CORE_LIQUIDITY_ANCHOR` |

## Safety

- execution_allowed: `false`
- live_sell_allowed: `false`
- order_endpoint_allowed: `false`
- cancel_endpoint_allowed: `false`
- market_sell_allowed: `false`
- scheduler_allowed: `false`
- no_profit_guarantee: `true`
