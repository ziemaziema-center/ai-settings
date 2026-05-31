# OFFLINE TEST HARNESS README

Use all relevant installed plugins and skills before making assumptions.

운영모드.

memory-first + SESSION_BOOT + validation-first + additive-only + post-task telemetry 기준으로 진행.

## Scope

Local-only synthetic harness for contract-layer governance validation.

## Files

- `synthetic_market_data_generator.py`
- `offline_strategy_candidate_engine.py`
- `offline_backtest_runner.py`
- `offline_safety_scoring.py`

## Run

```bash
python reports/offline_artifacts/offline_test_harness/offline_backtest_runner.py
python -m unittest discover -s tests/offline_strategy_research -p "test_*.py"
```

This document does not authorize live trading, shadow mode, Upbit API access, credential use, scheduler activation, parser execution, fixture creation, WF08 transition, runtime wiring, implementation, or production-readiness claims.
