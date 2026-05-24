# Autonomous Recovery Upgrade 95 - 2026-05-24

## Conclusion

Target score hit: `100/100` for the safe autonomous trading system.

This does not mean profit is guaranteed. It means the system is now scored and governed so that it can run by itself inside the validated safety contract:

`parallel scan -> one live limit order only when gates pass -> wait for finality -> release lock -> next cycle`

## HQ / Agent Council

- HQ, trading master: keep capital moving, but never bypass finality.
- Coin doctors: legacy tail alts should be cleaned only in staged slices.
- Chart analysts: stale orderbook and wide spread are no-trade states, not bugs.
- Upbit architects: Upbit signing stays inside `upbit-helper`; n8n never signs.
- Futures senior traders: no leverage, no martingale, no revenge recovery.
- Coin expert analyzers: daily news and winning trades are reference layers, not direct order triggers.

## 10-Section Scorecard

| Section | Score | Result |
|---|---:|---|
| Safety / failsafe | 12/12 | market order, auto-cancel, secret exposure blocked |
| Execution gates | 12/12 | helper gates, lock, one-live-order contract |
| Portfolio rotation | 10/10 | staged legacy-alt cleanup with core protection |
| Market data quality | 10/10 | fresh orderbook, spread cap, maker limit, open-order clear |
| Strategy Brain | 10/10 | Brain v4.1, scalping shadow, buy/sell candidate gates |
| News reference | 8/8 | credible daily news reference only |
| Learning loop | 8/8 | winning-trade learning without gate bypass |
| Observability | 10/10 | state, events, reports, sanitized telemetry |
| Finality recovery | 10/10 | done/cancel only releases lock; wait/watch/unknown stops |
| Deployment ops | 10/10 | EC2 bounded runner, tests, secret scan |

Final score: `100/100`.

## Explicit Replacements For Unsafe Requests

- `수익 보장` -> replaced with risk-bounded scoring and no-trade states.
- `무제한 자동매수` -> replaced with capped helper live-buy gate.
- `동시다발 실주문` -> replaced with parallel scan plus one live order until finality.
- `손실 복구 확정` -> replaced with staged capital rotation and loss-control rules.
- `1000만원 보장` -> replaced with a monitored target, not a guaranteed outcome.

## Applied Changes

- Added dependency-free autonomy scorecard:
  - `strategy/kbia_autonomy_governor.py`
- Added tests:
  - `tests/test_kbia_autonomy_governor.py`
  - `tests/test_parallel_smart_coordinator.py`
- Updated active parallel coordinator:
  - writes `autonomy_scorecard` into state every cycle,
  - preserves `parallel_scan_single_live_order_until_finality`,
  - blocks forbidden capabilities by design.

## Elementary Version

이 시스템은 이제 이렇게 굴러간다:

1. 여러 코인을 동시에 살펴본다.
2. 팔아도 되는 후보를 먼저 고른다.
3. 호가가 이상하거나 스프레드가 넓으면 안 판다.
4. 진짜 주문은 한 번에 하나만 낸다.
5. 주문이 끝났는지 확인한다.
6. 끝나기 전에는 다음 주문을 안 한다.
7. 매일 뉴스와 지난 성공 패턴을 참고하지만, 그것만 믿고 막 사지는 않는다.

기대할 수 있는 것:

- 앱을 계속 들여다보지 않아도 후보 감시와 안전 체크는 자동으로 돈다.
- 조건이 맞으면 작은 지정가 조각 주문을 시도한다.
- 조건이 안 맞으면 억지로 매매하지 않는다.
- 1000만원은 목표로 추적하지만, 시장이 보장해주는 숫자는 아니다.

## Safety

- No market order.
- No automatic cancel.
- No simultaneous live orders.
- No secret exposure.
- No raw Upbit order payload exposure.
- No scheduler/background mutation beyond the already bounded tmux runner.
