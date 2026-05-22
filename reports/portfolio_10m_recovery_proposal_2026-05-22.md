# Portfolio 10M Recovery Proposal - 2026-05-22

## Current Read

Read-only account snapshot from helper plus public ticker checks:

- available KRW: about `72,244`
- adjusted current portfolio value: about `3,581,773 KRW`
- original buy amount across assets: about `16,455,622 KRW`
- unrealized drawdown: about `-12.87M KRW`
- target: `10,000,000 KRW`
- required gain from current value: about `+6.42M KRW`, roughly `+179%`

Important: this cannot be reached quickly without high risk. The correct objective is not “recover old entry prices”; it is “move today’s remaining capital into the best forward opportunity with strict risk gates.”

## Current Holding View

| Asset | Approx value | Current decision |
| --- | ---: | --- |
| ETH | `896,900` | Keep core |
| SOL | `898,332` | Keep/cap high-beta core |
| BTC | `620,998` | Keep core |
| ETC | `378,977` | Exit staged |
| DOGE | `249,573` | Reduce staged unless tactical signal appears |
| FCT2 | `226,100` | Exit staged when spread/stale gates pass |
| DOT | `112,882` | Exit staged |
| ALGO | `92,419` | Exit staged |
| RVN | `33,326` | Review/tail cleanup |
| KRW | `72,244` | Tactical cash |
| NKN/SXP/SALT/APENFT/EVR/tiny dust | low or unavailable KRW value | Review, do not auto-market dump |

## Decision

Do not dump everything at market. That would convert bad entries into worse execution.

Use this order:

1. Keep BTC/ETH/SOL as the recovery core.
2. Continue staged limit cleanup of FCT2, ALGO, DOT, ETC, and DOGE only when helper gates pass.
3. Do not buy new tail alts.
4. Redeploy cleaned KRW only into BTC/ETH/SOL after Brain/news gates stop blocking.
5. Keep 5-15% KRW tactical cash after cleanup.

Target allocation after cleanup:

- BTC: `35-45%`
- ETH: `20-30%`
- SOL: `15-25%`
- KRW tactical cash: `5-15%`
- all tail/alts combined: `0-10%`

## Why Not Buy Now

Today’s news brain is `DEFENSIVE_REFERENCE`, and the aggressive buy shadow loop produced:

- `loop_count=3`
- `ready_for_buy_test_count=0`
- `live_order_count=0`

So the system is saying:

- Do not add new buy exposure right now.
- Continue watching cleanup windows.
- Do not bypass spread/stale/open-order/maker-limit gates.

## Fastest Practical Route To 10M

The fastest sane route is:

1. Free trapped capital from tail alts without bad execution.
2. Concentrate cleaned capital into liquid high-beta core: BTC/ETH/SOL.
3. Let SOL be the growth lever, but cap it so one bad move does not kill the account.
4. Use Brain v4.1 only when it emits a true `BUY_CANDIDATE`, score >= threshold, non-defensive news, tight spread, and no open order.
5. Stop adding risk if total portfolio falls another `12-15%` from current value.

This is not guaranteed-profit. It is the most rational recovery plan given current capital, liquidity, and automation safety constraints.
