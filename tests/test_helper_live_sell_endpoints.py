import importlib.util
import sys
import types
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAIN_PATH = ROOT / "upbit-helper" / "app" / "main.py"


def load_helper_module():
    if "fastapi" not in sys.modules:
        fastapi_stub = types.ModuleType("fastapi")

        class FastAPI:
            def __init__(self, *args, **kwargs):
                pass

            def post(self, *args, **kwargs):
                def decorator(func):
                    return func

                return decorator

            def get(self, *args, **kwargs):
                def decorator(func):
                    return func

                return decorator

        fastapi_stub.FastAPI = FastAPI
        sys.modules["fastapi"] = fastapi_stub

    if "pydantic" not in sys.modules:
        pydantic_stub = types.ModuleType("pydantic")

        class BaseModel:
            def __init__(self, **kwargs):
                annotations = {}
                for cls in reversed(type(self).mro()):
                    annotations.update(getattr(cls, "__annotations__", {}))
                for key in annotations:
                    setattr(self, key, getattr(type(self), key, None))
                for key, value in kwargs.items():
                    setattr(self, key, value)

        pydantic_stub.BaseModel = BaseModel
        sys.modules["pydantic"] = pydantic_stub

    spec = importlib.util.spec_from_file_location("upbit_helper_main_live_sell_test", MAIN_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def valid_sell_payload(**overrides):
    payload = {
        "market": "KRW-ETC",
        "side": "ask",
        "ord_type": "limit",
        "price": "30000",
        "volume": "0.5",
        "estimated_krw_value": "15000",
        "open_order_exists": False,
        "portfolio_plan_valid": True,
        "cleanup_candidate": True,
        "cleanup_action": "EXIT_STAGED",
    }
    payload.update(overrides)
    return payload


def install_safe_gate_stubs(helper, post_calls):
    def fake_upbit_get(path, query=None):
        if path == "/v1/orders/open":
            return {"status": 200, "body": [], "remaining_req": "group=default; min=599; sec=9"}
        if path == "/v1/accounts":
            return {
                "status": 200,
                "body": [{"currency": "ETC", "balance": "10"}],
                "remaining_req": "group=default; min=599; sec=9",
            }
        raise AssertionError(f"unexpected private GET {path}")

    def fake_public_get(path, query=None):
        assert path == "/v1/orderbook"
        assert query == {"markets": "KRW-ETC"}
        return {
            "status": 200,
            "body": [
                {
                    "timestamp": int(helper.datetime.now(helper.timezone.utc).timestamp() * 1000),
                    "orderbook_units": [{"bid_price": 29900, "ask_price": 30000}],
                }
            ],
            "remaining_req": "group=orderbook; min=599; sec=9",
        }

    def fake_upbit_post(path, payload):
        post_calls.append((path, payload))
        return {"status": 201, "body": {"ok": True}, "remaining_req": "group=default; min=599; sec=9"}

    helper._upbit_get = fake_upbit_get
    helper._upbit_public_get = fake_public_get
    helper._upbit_post = fake_upbit_post


def install_stale_orderbook_stubs(helper, post_calls, stale_ms=10001, future_ms=None):
    def fake_upbit_get(path, query=None):
        if path == "/v1/orders/open":
            return {"status": 200, "body": [], "remaining_req": "group=default; min=599; sec=9"}
        if path == "/v1/accounts":
            return {
                "status": 200,
                "body": [{"currency": "ETC", "balance": "10"}],
                "remaining_req": "group=default; min=599; sec=9",
            }
        raise AssertionError(f"unexpected private GET {path}")

    def fake_public_get(path, query=None):
        assert path == "/v1/orderbook"
        now_ms = int(helper.datetime.now(helper.timezone.utc).timestamp() * 1000)
        timestamp = now_ms + future_ms if future_ms is not None else now_ms - stale_ms
        return {
            "status": 200,
            "body": [
                {
                    "timestamp": timestamp,
                    "orderbook_units": [{"bid_price": 29900, "ask_price": 30000}],
                }
            ],
            "remaining_req": "group=orderbook; min=599; sec=9",
        }

    def fake_upbit_post(path, payload):
        post_calls.append((path, payload))
        return {"status": 201, "body": {"ok": True}, "remaining_req": "group=default; min=599; sec=9"}

    helper._upbit_get = fake_upbit_get
    helper._upbit_public_get = fake_public_get
    helper._upbit_post = fake_upbit_post


def test_sell_test_blocks_market_order():
    helper = load_helper_module()
    post_calls = []
    install_safe_gate_stubs(helper, post_calls)
    result = helper.sell_test_telemetry(helper.SellTestRequest(**valid_sell_payload(ord_type="market")))
    assert "LIVE_SELL_LIMIT_ONLY" in result["error_name"]
    assert post_calls == []


def test_sell_test_blocks_bid():
    helper = load_helper_module()
    post_calls = []
    install_safe_gate_stubs(helper, post_calls)
    result = helper.sell_test_telemetry(helper.SellTestRequest(**valid_sell_payload(side="bid")))
    assert "LIVE_SELL_ASK_ONLY" in result["error_name"]
    assert post_calls == []


def test_sell_test_blocks_unapproved_market():
    helper = load_helper_module()
    post_calls = []
    install_safe_gate_stubs(helper, post_calls)
    result = helper.sell_test_telemetry(helper.SellTestRequest(**valid_sell_payload(market="KRW-BTC")))
    assert "LIVE_SELL_MARKET_NOT_ALLOWED" in result["error_name"]
    assert post_calls == []


def test_sell_test_blocks_large_slice():
    helper = load_helper_module()
    post_calls = []
    install_safe_gate_stubs(helper, post_calls)
    result = helper.sell_test_telemetry(
        helper.SellTestRequest(**valid_sell_payload(price="30001", volume="1", estimated_krw_value="30001"))
    )
    assert "LIVE_SELL_MAX_KRW_EXCEEDED" in result["error_name"]
    assert post_calls == []


def test_sell_test_blocks_open_order():
    helper = load_helper_module()
    post_calls = []
    install_safe_gate_stubs(helper, post_calls)

    def fake_open_order_get(path, query=None):
        if path == "/v1/orders/open":
            return {"status": 200, "body": [{"market": "KRW-BTC", "state": "wait"}], "remaining_req": None}
        raise AssertionError(f"unexpected GET {path}")

    helper._upbit_get = fake_open_order_get
    result = helper.sell_test_telemetry(helper.SellTestRequest(**valid_sell_payload()))
    assert result["error_name"] == "LIVE_SELL_OPEN_ORDER_EXISTS_OR_UNKNOWN"
    assert post_calls == []


def test_sell_test_success_calls_orders_test_only():
    helper = load_helper_module()
    post_calls = []
    install_safe_gate_stubs(helper, post_calls)
    result = helper.sell_test_telemetry(helper.SellTestRequest(**valid_sell_payload()))
    assert result["sell_order_test_passed"] is True
    assert result["live_sell_attempted"] is False
    assert post_calls == [
        (
            "/v1/orders/test",
            {"market": "KRW-ETC", "side": "ask", "ord_type": "limit", "price": "30000", "volume": "0.5"},
        )
    ]


def test_sell_test_blocks_stale_orderbook_with_diagnostics():
    helper = load_helper_module()
    post_calls = []
    install_stale_orderbook_stubs(helper, post_calls, stale_ms=20000)
    result = helper.sell_test_telemetry(helper.SellTestRequest(**valid_sell_payload()))
    assert result["error_name"] == "LIVE_SELL_ORDERBOOK_STALE"
    assert result["orderbook_age_ms"] >= 10000
    assert result["orderbook_timestamp_ms"] is not None
    assert result["helper_now_ms"] is not None
    assert result["best_bid"] == 29900.0
    assert result["best_ask"] == 30000.0
    assert "LIVE_SELL_ORDERBOOK_STALE" in result["orderbook_failures"]
    assert post_calls == []


def test_sell_test_blocks_future_orderbook_clock_skew():
    helper = load_helper_module()
    post_calls = []
    install_stale_orderbook_stubs(helper, post_calls, future_ms=5000)
    result = helper.sell_test_telemetry(helper.SellTestRequest(**valid_sell_payload()))
    assert result["error_name"] == "LIVE_SELL_ORDERBOOK_CLOCK_SKEW"
    assert result["clock_skew_ms"] >= 2000
    assert "LIVE_SELL_ORDERBOOK_CLOCK_SKEW" in result["orderbook_failures"]
    assert post_calls == []


def test_live_sell_blocks_without_test():
    helper = load_helper_module()
    post_calls = []
    install_safe_gate_stubs(helper, post_calls)
    result = helper.live_sell_telemetry(
        helper.LiveSellRequest(
            **valid_sell_payload(
                live_sell_enabled=True,
                execution_allowed=True,
                execution_mode="live",
                all_pass=True,
                duplicate_lock_status="clear",
                system_stop_active=False,
                sell_order_test_passed=False,
                one_time_live_sell_attempt_allowed=True,
            )
        )
    )
    assert result["error_name"] == "LIVE_SELL_TEST_NOT_PASSED"
    assert post_calls == []


def test_live_sell_blocks_fingerprint_mismatch():
    helper = load_helper_module()
    post_calls = []
    install_safe_gate_stubs(helper, post_calls)
    result = helper.live_sell_telemetry(
        helper.LiveSellRequest(
            **valid_sell_payload(
                live_sell_enabled=True,
                execution_allowed=True,
                execution_mode="live",
                all_pass=True,
                duplicate_lock_status="clear",
                system_stop_active=False,
                sell_order_test_passed=True,
                sell_test_fingerprint="wrong",
                one_time_live_sell_attempt_allowed=True,
            )
        )
    )
    assert result["error_name"] == "LIVE_SELL_TEST_FINGERPRINT_MISMATCH"
    assert post_calls == []


def test_live_sell_rechecks_open_order_before_post():
    helper = load_helper_module()
    post_calls = []
    install_safe_gate_stubs(helper, post_calls)
    fingerprint = helper._sell_fingerprint("KRW-ETC", "ask", "limit", helper.Decimal("30000"), helper.Decimal("0.5"), helper.Decimal("15000"))

    def fake_open_order_get(path, query=None):
        if path == "/v1/orders/open":
            return {"status": 200, "body": [{"market": "KRW-ETC", "state": "wait"}], "remaining_req": None}
        raise AssertionError(f"unexpected GET {path}")

    helper._upbit_get = fake_open_order_get
    result = helper.live_sell_telemetry(
        helper.LiveSellRequest(
            **valid_sell_payload(
                live_sell_enabled=True,
                execution_allowed=True,
                execution_mode="live",
                all_pass=True,
                duplicate_lock_status="clear",
                system_stop_active=False,
                sell_order_test_passed=True,
                sell_test_fingerprint=fingerprint,
                one_time_live_sell_attempt_allowed=True,
            )
        )
    )
    assert result["error_name"] == "LIVE_SELL_OPEN_ORDER_EXISTS_OR_UNKNOWN"
    assert post_calls == []


def test_live_sell_success_posts_limit_ask_only():
    helper = load_helper_module()
    post_calls = []
    install_safe_gate_stubs(helper, post_calls)
    fingerprint = helper._sell_fingerprint("KRW-ETC", "ask", "limit", helper.Decimal("30000"), helper.Decimal("0.5"), helper.Decimal("15000"))
    result = helper.live_sell_telemetry(
        helper.LiveSellRequest(
            **valid_sell_payload(
                live_sell_enabled=True,
                execution_allowed=True,
                execution_mode="live",
                all_pass=True,
                duplicate_lock_status="clear",
                system_stop_active=False,
                sell_order_test_passed=True,
                sell_test_fingerprint=fingerprint,
                one_time_live_sell_attempt_allowed=True,
            )
        )
    )
    assert result["live_sell_attempted"] is True
    assert result["live_sell_accepted"] is True
    assert post_calls == [
        (
            "/v1/orders",
            {"market": "KRW-ETC", "side": "ask", "ord_type": "limit", "price": "30000", "volume": "0.5"},
        )
    ]


if __name__ == "__main__":
    test_sell_test_blocks_market_order()
    test_sell_test_blocks_bid()
    test_sell_test_blocks_unapproved_market()
    test_sell_test_blocks_large_slice()
    test_sell_test_blocks_open_order()
    test_sell_test_success_calls_orders_test_only()
    test_sell_test_blocks_stale_orderbook_with_diagnostics()
    test_sell_test_blocks_future_orderbook_clock_skew()
    test_live_sell_blocks_without_test()
    test_live_sell_blocks_fingerprint_mismatch()
    test_live_sell_rechecks_open_order_before_post()
    test_live_sell_success_posts_limit_ask_only()
    print("HELPER_LIVE_SELL_ENDPOINT_TESTS_PASS")
