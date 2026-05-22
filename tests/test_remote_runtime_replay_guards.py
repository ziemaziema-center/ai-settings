from __future__ import annotations

import importlib.util
import sys
import types
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = ROOT / "runners" / "kbia_full_automation_coordinator_20260520.py"


def load_runner():
    spec = importlib.util.spec_from_file_location("kbia_full_automation_coordinator_replay_test", RUNNER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    temp_root = Path(tempfile.mkdtemp(prefix="kbia_replay_"))
    module.LOG_DIR = temp_root
    module.STATE_PATH = temp_root / "state.json"
    module.EVENTS_PATH = temp_root / "events.jsonl"
    return module


def test_cycle_stops_when_any_open_order_exists():
    runner = load_runner()
    calls = []

    def fake_get_json(path):
        assert path == "/health"
        return {"ok": True}

    def fake_post_json(path, payload):
        calls.append((path, payload))
        if path == "/upbit/open-orders/telemetry":
            exists = payload["market"] == "KRW-BTC"
            return {"success": True, "open_order_count": 1 if exists else 0, "open_order_exists": exists, "error_name": None}
        if path == "/upbit/open-orders/detail-telemetry-no-journal":
            return {"classification_summary": {"final_classification": "wait", "next_safe_action": "remain_stopped"}, "orders": [{"state": "wait"}]}
        raise AssertionError(f"unexpected path {path}")

    runner.get_json = fake_get_json
    runner.post_json = fake_post_json
    state = {"completed_markets": [], "active_market": "KRW-BTC", "cycle_count": 0}
    result = runner.cycle(state)
    assert result["last_open_orders"]["KRW-BTC"]["open_order_exists"] is True
    assert result["last_finality"]["classification"] == "wait"
    assert not any(path in {"/upbit/sell-test/telemetry", "/upbit/live-sell/telemetry"} for path, _ in calls)


def test_cycle_does_not_attempt_live_sell_when_sell_test_blocks():
    runner = load_runner()
    calls = []

    def fake_get_json(path):
        assert path == "/health"
        return {"ok": True}

    def fake_post_json(path, payload):
        calls.append((path, payload))
        if path == "/upbit/open-orders/telemetry":
            return {"success": True, "open_order_count": 0, "open_order_exists": False, "error_name": None}
        if path == "/upbit/sell-test/telemetry":
            return {"success": False, "sell_order_test_passed": False, "error_name": "LIVE_SELL_SPREAD_TOO_WIDE"}
        raise AssertionError(f"unexpected path {path}")

    def fake_orderbook(market):
        return {"timestamp": 1, "age_ms_at_build": 1, "best_bid": runner.Decimal("17.9"), "best_ask": runner.Decimal("18.1")}

    runner.get_json = fake_get_json
    runner.post_json = fake_post_json
    runner.public_orderbook = fake_orderbook
    state = {"completed_markets": ["KRW-DOT", "KRW-ETC"], "active_market": None, "cycle_count": 0}
    result = runner.cycle(state)
    assert result["blocked_markets"]["KRW-FCT2"]["error_name"] == "LIVE_SELL_SPREAD_TOO_WIDE"
    assert not any(path == "/upbit/live-sell/telemetry" for path, _ in calls)


def test_helper_health_failure_blocks_all_trading_calls():
    runner = load_runner()
    calls = []

    def fake_get_json(path):
        calls.append((path, None))
        return {"ok": False}

    runner.get_json = fake_get_json
    runner.post_json = lambda path, payload: (_ for _ in ()).throw(AssertionError(path))
    state = {"completed_markets": [], "active_market": None, "cycle_count": 0}
    result = runner.cycle(state)
    assert result["cycle_count"] == 1
    assert calls == [("/health", None)]


def test_live_sell_path_acquires_server_lock_first():
    runner = load_runner()
    calls = []

    def fake_get_json(path):
        assert path == "/health"
        return {"ok": True}

    def fake_post_json(path, payload):
        calls.append((path, payload))
        if path == "/upbit/open-orders/telemetry":
            return {"success": True, "open_order_count": 0, "open_order_exists": False, "error_name": None}
        if path == "/upbit/sell-test/telemetry":
            return {"success": True, "sell_order_test_passed": True, "sell_test_fingerprint": "fp", "error_name": None}
        if path == "/execution-lock/acquire":
            return {"lock_acquired": True, "lock_id": "lock-1", "lock_state": "active", "blocked_reason": None}
        if path == "/upbit/live-sell/telemetry":
            return {"live_sell_attempted": True, "live_sell_accepted": True, "http_status": 201, "estimated_krw_value": 29000, "error_name": None}
        raise AssertionError(f"unexpected path {path}")

    def fake_orderbook(market):
        return {"timestamp": 1, "age_ms_at_build": 1, "best_bid": runner.Decimal("17.9"), "best_ask": runner.Decimal("18.1")}

    runner.get_json = fake_get_json
    runner.post_json = fake_post_json
    runner.public_orderbook = fake_orderbook
    state = {"completed_markets": ["KRW-DOT", "KRW-ETC"], "active_market": None, "cycle_count": 0}
    result = runner.cycle(state)
    paths = [path for path, _ in calls]
    assert paths.index("/execution-lock/acquire") < paths.index("/upbit/live-sell/telemetry")
    assert result["active_market"] == "KRW-FCT2"
    assert result["active_execution_lock"]["lock_id"] == "lock-1"


if __name__ == "__main__":
    test_cycle_stops_when_any_open_order_exists()
    test_cycle_does_not_attempt_live_sell_when_sell_test_blocks()
    test_helper_health_failure_blocks_all_trading_calls()
    test_live_sell_path_acquires_server_lock_first()
    print("REMOTE_RUNTIME_REPLAY_GUARDS_PASS")
