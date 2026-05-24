from __future__ import annotations

import importlib.util
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = ROOT / "runners" / "kbia_parallel_smart_coordinator_20260524.py"


def load_runner():
    spec = importlib.util.spec_from_file_location("kbia_parallel_smart_coordinator_test", RUNNER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    temp_root = Path(tempfile.mkdtemp(prefix="kbia_parallel_"))
    module.LOG_DIR = temp_root
    module.STATE_PATH = temp_root / "state.json"
    module.EVENTS_PATH = temp_root / "events.jsonl"
    return module


def test_open_order_blocks_candidate_scan_and_live_sell():
    runner = load_runner()
    calls = []

    def fake_get_json(path):
        assert path == "/health"
        return {"ok": True}

    def fake_post_json(path, payload):
        calls.append((path, payload))
        if path == "/upbit/open-orders/telemetry":
            exists = payload["market"] == "KRW-BTC"
            return {"success": True, "open_order_count": 1 if exists else 0, "open_order_exists": exists}
        if path == "/upbit/open-orders/detail-telemetry-no-journal":
            return {"classification_summary": {"final_classification": "wait", "next_safe_action": "remain_stopped"}, "orders": [{"state": "wait"}]}
        raise AssertionError(f"unexpected path {path}")

    runner.get_json = fake_get_json
    runner.post_json = fake_post_json
    state = {"active_market": "KRW-BTC", "cycle_count": 0}
    result = runner.cycle(state)
    assert result["last_open_orders"]["KRW-BTC"]["open_order_exists"] is True
    assert result["last_finality"]["classification"] == "wait"
    assert not any(path in {"/upbit/sell-test/telemetry", "/upbit/live-sell/telemetry"} for path, _ in calls)


def test_highest_priority_passed_candidate_is_executed_once():
    runner = load_runner()
    calls = []

    def fake_get_json(path):
        assert path == "/health"
        return {"ok": True}

    def fake_post_json(path, payload):
        calls.append((path, payload))
        if path == "/upbit/open-orders/telemetry":
            return {"success": True, "open_order_count": 0, "open_order_exists": False}
        if path == "/upbit/sell-test/telemetry":
            passed = payload["market"] in {"KRW-ALGO", "KRW-DOT"}
            return {
                "success": passed,
                "sell_order_test_passed": passed,
                "sell_test_fingerprint": f"fp-{payload['market']}" if passed else None,
                "error_name": None if passed else "LIVE_SELL_SPREAD_TOO_WIDE",
            }
        if path == "/execution-lock/acquire":
            return {"lock_acquired": True, "lock_id": "lock-1", "blocked_reason": None}
        if path == "/upbit/live-sell/telemetry":
            return {"live_sell_attempted": True, "live_sell_accepted": True, "http_status": 201, "estimated_krw_value": payload["estimated_krw_value"]}
        raise AssertionError(f"unexpected path {path}")

    def fake_orderbook(market):
        return {
            "timestamp": 1,
            "age_ms_at_build": 1,
            "best_bid": runner.Decimal("100"),
            "best_ask": runner.Decimal("100"),
            "spread_bps": runner.Decimal("0"),
        }

    runner.get_json = fake_get_json
    runner.post_json = fake_post_json
    runner.public_orderbook = fake_orderbook
    state = {"active_market": None, "cycle_count": 0}
    result = runner.cycle(state)
    live_calls = [payload for path, payload in calls if path == "/upbit/live-sell/telemetry"]
    assert len(live_calls) == 1
    assert live_calls[0]["market"] == "KRW-ALGO"
    assert result["active_market"] == "KRW-ALGO"
    assert result["autonomy_scorecard"]["target_hit"] is True


def test_live_recheck_reject_releases_lock_and_clears_active_lock():
    runner = load_runner()
    calls = []

    def fake_get_json(path):
        assert path == "/health"
        return {"ok": True}

    def fake_post_json(path, payload):
        calls.append((path, payload))
        if path == "/upbit/open-orders/telemetry":
            return {"success": True, "open_order_count": 0, "open_order_exists": False}
        if path == "/upbit/sell-test/telemetry":
            return {"success": True, "sell_order_test_passed": True, "sell_test_fingerprint": "fp", "error_name": None}
        if path == "/execution-lock/acquire":
            return {"lock_acquired": True, "lock_id": "lock-1", "blocked_reason": None}
        if path == "/upbit/live-sell/telemetry":
            return {"live_sell_attempted": False, "live_sell_accepted": False, "error_name": "LIVE_SELL_SPREAD_TOO_WIDE"}
        if path == "/execution-lock/release":
            return {"lock_released": True, "blocked_reason": None}
        raise AssertionError(f"unexpected path {path}")

    def fake_orderbook(market):
        return {
            "timestamp": 1,
            "age_ms_at_build": 1,
            "best_bid": runner.Decimal("100"),
            "best_ask": runner.Decimal("100"),
            "spread_bps": runner.Decimal("0"),
        }

    runner.get_json = fake_get_json
    runner.post_json = fake_post_json
    runner.public_orderbook = fake_orderbook
    state = {"active_market": None, "cycle_count": 0}
    result = runner.cycle(state)
    assert any(path == "/execution-lock/release" for path, _ in calls)
    assert result.get("active_execution_lock") is None
    assert result.get("active_market") is None


if __name__ == "__main__":
    test_open_order_blocks_candidate_scan_and_live_sell()
    test_highest_priority_passed_candidate_is_executed_once()
    test_live_recheck_reject_releases_lock_and_clears_active_lock()
    print("KBIA_PARALLEL_SMART_COORDINATOR_TESTS_PASS")
