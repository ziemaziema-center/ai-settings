# KBIA Strategy Validation - 2026-05-19

- overall_passed: `True`
- loops_requested: `3`
- runtime_modified: `false`
- workflow_changed: `false`
- live_order_submitted: `false`
- cancel_attempted: `false`
- cron_enabled: `false`

## Loop Results
- loop 1: `PASS`
  - `C:\Python314\python.exe -m py_compile strategy/kbia_strategy_kernel.py tests/test_kbia_strategy_kernel.py` -> `0`
  - `C:\Python314\python.exe tests/test_kbia_strategy_kernel.py` -> `0`
  - `C:\Python314\python.exe tests/wf05_offline_regression_runner_2026-05-11.py` -> `0`
- loop 2: `PASS`
  - `C:\Python314\python.exe -m py_compile strategy/kbia_strategy_kernel.py tests/test_kbia_strategy_kernel.py` -> `0`
  - `C:\Python314\python.exe tests/test_kbia_strategy_kernel.py` -> `0`
  - `C:\Python314\python.exe tests/wf05_offline_regression_runner_2026-05-11.py` -> `0`
- loop 3: `PASS`
  - `C:\Python314\python.exe -m py_compile strategy/kbia_strategy_kernel.py tests/test_kbia_strategy_kernel.py` -> `0`
  - `C:\Python314\python.exe tests/test_kbia_strategy_kernel.py` -> `0`
  - `C:\Python314\python.exe tests/wf05_offline_regression_runner_2026-05-11.py` -> `0`

## Safety

This validation is offline only. It does not call Upbit, n8n, helper runtime, order, cancel, Telegram, or scheduler endpoints.
