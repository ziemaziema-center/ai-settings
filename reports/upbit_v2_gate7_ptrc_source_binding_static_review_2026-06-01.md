# UPBIT V2 GATE_7 PTRC Source-Binding Static Review - 2026-06-01

## Gate
- GATE_7 PTRC SPEC SOURCE-BINDING STATIC REVIEW

## Scope
- Offline static review only.
- No Upbit API, no credentials, no parser, no fixture, no WF08, no scheduler, no runtime execution.

## Analyst Logs
- [Analyst] Bound all 25 required PTRC checks to `ptrc02`, `ptrc03`, `ptrc04` and aligned alert/kill dependencies to `alrt01/alrt02`, `kill01/kill02`.
- [Analyst] Confirmed capital-threshold semantics trace to SEC Rule 15c3-5 language and V2 `ptrc04` with explicit cancel + disable + human re-arm.

## Reviewer Logs
- [Reviewer] Verified every item remains `implementation_status=SPEC_ONLY`, `runtime_status=NOT_IMPLEMENTED`, `live_status=BLOCKED`.
- [Reviewer] Rejection path wording checked for all items: STOP + LOG + ALERT enforced through `ptrc03` and 5-second alert SLA dependency.
- [Reviewer] Live-readiness wording scan completed; no authorization implication found.

## Operator Logs
- [Operator] Produced source-binding report, runtime summary JSON, targeted tests, closing QA, and final verdict under additive-only offline scope.

## PTRC Source-Binding Matrix

| check_id | source_text_reference | standard_reference | required_behavior | rejection_behavior | alert_dependency | kill_dependency | implementation_status | runtime_status | live_status | ambiguity_status | pass/block_decision |
|---|---|---|---|---|---|---|---|---|---|---|---|
| max_order_notional_krw | v2:ptrc02 financial checks | SEC Rule 15c3-5 max order size / capital limits | enforce single-order notional ceiling pre-trade | STOP + LOG(`REJECTED_BY_PTRC`) + ALERT within 5 seconds | alrt01/alrt02 + MiFID II RTS 6 Art 17(1) | kill02 rejection-rate / burst escalation | SPEC_ONLY | NOT_IMPLEMENTED | BLOCKED | CLEAR | PASS |
| max_position_notional_krw | v2:ptrc02 financial checks | SEC Rule 15c3-5 capital limit controls | enforce per-market position notional cap pre-trade | STOP + LOG + ALERT | alrt01/alrt02 | kill02 | SPEC_ONLY | NOT_IMPLEMENTED | BLOCKED | CLEAR | PASS |
| max_aggregate_exposure_krw | v2:ptrc02 financial checks | SEC Rule 15c3-5 credit/capital controls | enforce account-wide exposure cap pre-trade | STOP + LOG + ALERT | alrt01/alrt02 | kill02 | SPEC_ONLY | NOT_IMPLEMENTED | BLOCKED | CLEAR | PASS |
| pre_held_krw_balance_required | v2:ptrc02 financial checks | SEC Rule 15c3-5 pre-trade risk control model | require pre-held KRW balance before intent progression | STOP + LOG + ALERT | alrt01/alrt02 | kill02 | SPEC_ONLY | NOT_IMPLEMENTED | BLOCKED | CLEAR | PASS |
| daily_loss_cap | v2:ptrc02 + ptrc04 | SEC Rule 15c3-5 pre-set capital threshold | enforce daily realized-loss hard cap | CAPITAL_BREACH => cancel outstanding orders + disable new entry + human re-arm | alrt01/alrt02 | kill01/kill02/kill03 | SPEC_ONLY | NOT_IMPLEMENTED | BLOCKED | CLEAR | PASS |
| intraday_drawdown_cap | v2:ptrc02 + ptrc04 | SEC Rule 15c3-5 pre-set capital threshold | enforce intraday drawdown hard cap | CAPITAL_BREACH => cancel outstanding orders + disable new entry + human re-arm | alrt01/alrt02 | kill01/kill02/kill03 | SPEC_ONLY | NOT_IMPLEMENTED | BLOCKED | CLEAR | PASS |
| max_price_deviation_pct_vs_last_trade | v2:ptrc02 price sanity checks | SEC Rule 15c3-5 price parameter controls | reject fat-finger deviation versus last trade | STOP + LOG + ALERT | alrt01/alrt02 | kill02 anomaly escalation | SPEC_ONLY | NOT_IMPLEMENTED | BLOCKED | CLEAR | PASS |
| max_price_deviation_pct_vs_orderbook_mid | v2:ptrc02 price sanity checks | SEC Rule 15c3-5 price parameter controls | reject fat-finger deviation versus orderbook mid | STOP + LOG + ALERT | alrt01/alrt02 | kill02 anomaly escalation | SPEC_ONLY | NOT_IMPLEMENTED | BLOCKED | CLEAR | PASS |
| min_tick_size_compliance | v2:ptrc02 price sanity checks | SEC Rule 15c3-5 erroneous order prevention | enforce tick-size compliance pre-trade | STOP + LOG + ALERT | alrt01/alrt02 | kill02 | SPEC_ONLY | NOT_IMPLEMENTED | BLOCKED | CLEAR | PASS |
| min_order_size_compliance | v2:ptrc02 price sanity checks | SEC Rule 15c3-5 erroneous order prevention | enforce minimum order-size compliance pre-trade | STOP + LOG + ALERT | alrt01/alrt02 | kill02 | SPEC_ONLY | NOT_IMPLEMENTED | BLOCKED | CLEAR | PASS |
| ord_type == limit | v2:ptrc02 order type checks | V2 governance hard constraint | hard-allow only limit order type | STOP + LOG + ALERT on non-limit | alrt01/alrt02 | kill02 | SPEC_ONLY | NOT_IMPLEMENTED | BLOCKED | CLEAR | PASS |
| ord_type != market | v2:ptrc02 order type checks | V2 governance hard reject | hard-reject market order type | STOP + LOG + ALERT | alrt01/alrt02 | kill02 | SPEC_ONLY | NOT_IMPLEMENTED | BLOCKED | CLEAR | PASS |
| no_leverage | v2:ptrc02 order type checks | V2 governance risk boundary | leverage exposure forbidden in PTRC gate | STOP + LOG + ALERT | alrt01/alrt02 | kill02 | SPEC_ONLY | NOT_IMPLEMENTED | BLOCKED | CLEAR | PASS |
| no_margin | v2:ptrc02 order type checks | V2 governance risk boundary | margin exposure forbidden in PTRC gate | STOP + LOG + ALERT | alrt01/alrt02 | kill02 | SPEC_ONLY | NOT_IMPLEMENTED | BLOCKED | CLEAR | PASS |
| per_second_budget_remaining | v2:ptrc02 rate checks + bdgt02 | Upbit Open API rate limit policy | enforce pre-trade per-second budget threshold | STOP + LOG + ALERT on budget breach | alrt01/alrt02 | kill02 + budget 429/418 escalation path | SPEC_ONLY | NOT_IMPLEMENTED | BLOCKED | CLEAR | PASS |
| per_market_order_burst_limit | v2:ptrc02 rate checks | Upbit rate-limit discipline reference | enforce per-market burst cap | STOP + LOG + ALERT | alrt01/alrt02 | kill02 volume-based triggers | SPEC_ONLY | NOT_IMPLEMENTED | BLOCKED | CLEAR | PASS |
| per_minute_max_orders | v2:ptrc02 rate checks | Upbit rate-limit discipline reference | enforce per-minute order cap | STOP + LOG + ALERT | alrt01/alrt02 | kill02 volume-based triggers | SPEC_ONLY | NOT_IMPLEMENTED | BLOCKED | CLEAR | PASS |
| client_order_id_unique_in_window | v2:ptrc02 duplicate checks | IDEM pattern references | reject duplicate client order ID within guard window | STOP + LOG + ALERT | alrt01/alrt02 | kill02 integrity-based trigger | SPEC_ONLY | NOT_IMPLEMENTED | BLOCKED | CLEAR | PASS |
| no_identical_order_within_N_seconds | v2:ptrc02 duplicate checks | V2 anti-duplicate execution rule | reject identical order replay in lock window | STOP + LOG + ALERT | alrt01/alrt02 | kill02 integrity/volume anomaly | SPEC_ONLY | NOT_IMPLEMENTED | BLOCKED | CLEAR | PASS |
| market_in_allowlist | v2:ptrc02 instrument checks | V2 governance allowlist requirement | allow only approved market list | STOP + LOG + ALERT | alrt01/alrt02 | kill02 integrity checks | SPEC_ONLY | NOT_IMPLEMENTED | BLOCKED | CLEAR | PASS |
| market_warning_status == NONE | v2:ptrc02 instrument checks | Upbit market warning semantics (referenced in V2 text) | block warning-marked market intents | STOP + LOG + ALERT | alrt01/alrt02 | kill02 | SPEC_ONLY | NOT_IMPLEMENTED | BLOCKED | CLEAR | PASS |
| wallet_state == working | v2:ptrc02 instrument checks | V2 instrument availability requirement | require working wallet state before progression | STOP + LOG + ALERT | alrt01/alrt02 | kill02 + kill connectivity/integrity escalation | SPEC_ONLY | NOT_IMPLEMENTED | BLOCKED | CLEAR | PASS |
| can_trade flag verified | v2:ptrc02 instrument checks | V2 tradability flag requirement | require can_trade verification before progression | STOP + LOG + ALERT | alrt01/alrt02 | kill02 | SPEC_ONLY | NOT_IMPLEMENTED | BLOCKED | MINOR_NOTE (`can_withdraw / can_trade` combined phrase) | PASS |
| not restricted | v2:ptrc02 regulatory checks | SEC Rule 15c3-5 regulatory risk controls | block restricted-list intents | STOP + LOG + ALERT | alrt01/alrt02 | kill02 integrity/regulatory trigger | SPEC_ONLY | NOT_IMPLEMENTED | BLOCKED | CLEAR | PASS |
| not scheduled maintenance | v2:ptrc02 regulatory checks | SEC Rule 15c3-5 pre-trade control intent | block intents during scheduled exchange maintenance windows | STOP + LOG + ALERT | alrt01/alrt02 | kill02 + heart/connectivity trigger chain | SPEC_ONLY | NOT_IMPLEMENTED | BLOCKED | CLEAR | PASS |

## Static Review Result
- ptrc_required_items_count: 25
- ptrc_items_passed: 25
- ptrc_items_blocked: 0
- implementation_status_uniform: SPEC_ONLY
- runtime_status_uniform: NOT_IMPLEMENTED
- live_status_uniform: BLOCKED

## Scope Safety
- live_trading_authorization: false
- credential_authorization: false
- wf08_authorization: false
- scheduler_authorization: false
- upbit_api_access: false
- parser_execution: false
- fixture_creation: false

This document does not authorize live trading, shadow mode, Upbit API access, credential use, scheduler activation, parser execution, fixture creation, WF08 transition, runtime wiring, implementation, or production-readiness claims.
