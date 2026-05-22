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

    spec = importlib.util.spec_from_file_location("upbit_helper_main_live_buy_test", MAIN_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def valid_buy_payload(**overrides):
    payload = {
        "market": "KRW-BTC",
        "side": "bid",
        "ord_type": "limit",
        "price": "100000000",
        "volume": "0.0001",
        "estimated_krw_value": "10000",
        "open_order_exists": False,
        "brain_schema_version": "kbia.strategy_brain.v4.1",
        "brain_action": "BUY_CANDIDATE",
        "brain_live_ready": True,
        "brain_candidate_score": "82",
        "news_bias": "BALANCED_REFERENCE",
        "scalping_candidate": True,
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
                "body": [{"currency": "KRW", "balance": "20000"}],
                "remaining_req": "group=default; min=599; sec=9",
            }
        raise AssertionError(f"unexpected private GET {path}")

    def fake_public_get(path, query=None):
        assert path == "/v1/orderbook"
        assert query == {"markets": "KRW-BTC"}
        return {
            "status": 200,
            "body": [
                {
                    "timestamp": int(helper.datetime.now(helper.timezone.utc).timestamp() * 1000),
                    "orderbook_units": [{"bid_price": 100000000, "ask_price": 100050000}],
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


def test_buy_test_blocks_market_order():
    helper = load_helper_module()
    post_calls = []
    install_safe_gate_stubs(helper, post_calls)
    result = helper.buy_test_telemetry(helper.BuyTestRequest(**valid_buy_payload(ord_type="price")))
    assert "LIVE_BUY_LIMIT_ONLY" in result["error_name"]
    assert post_calls == []


def test_buy_test_blocks_ask():
    helper = load_helper_module()
    post_calls = []
    install_safe_gate_stubs(helper, post_calls)
    result = helper.buy_test_telemetry(helper.BuyTestRequest(**valid_buy_payload(side="ask")))
    assert "LIVE_BUY_BID_ONLY" in result["error_name"]
    assert post_calls == []


def test_buy_test_blocks_unapproved_market():
    helper = load_helper_module()
    post_calls = []
    install_safe_gate_stubs(helper, post_calls)
    result = helper.buy_test_telemetry(helper.BuyTestRequest(**valid_buy_payload(market="KRW-DOGE")))
    assert "LIVE_BUY_MARKET_NOT_ALLOWED" in result["error_name"]
    assert post_calls == []


def test_buy_test_blocks_defensive_news():
    helper = load_helper_module()
    post_calls = []
    install_safe_gate_stubs(helper, post_calls)
    result = helper.buy_test_telemetry(helper.BuyTestRequest(**valid_buy_payload(news_bias="DEFENSIVE_REFERENCE")))
    assert "LIVE_BUY_NEWS_DEFENSIVE" in result["error_name"]
    assert post_calls == []


def test_buy_test_blocks_low_brain_score():
    helper = load_helper_module()
    post_calls = []
    install_safe_gate_stubs(helper, post_calls)
    result = helper.buy_test_telemetry(helper.BuyTestRequest(**valid_buy_payload(brain_candidate_score="77.9")))
    assert "LIVE_BUY_BRAIN_SCORE_TOO_LOW" in result["error_name"]
    assert post_calls == []


def test_buy_test_blocks_open_order():
    helper = load_helper_module()
    post_calls = []
    install_safe_gate_stubs(helper, post_calls)

    def fake_open_order_get(path, query=None):
        if path == "/v1/orders/open":
            return {"status": 200, "body": [{"market": "KRW-BTC", "state": "wait"}], "remaining_req": None}
        raise AssertionError(f"unexpected GET {path}")

    helper._upbit_get = fake_open_order_get
    result = helper.buy_test_telemetry(helper.BuyTestRequest(**valid_buy_payload()))
    assert result["error_name"] == "LIVE_BUY_OPEN_ORDER_EXISTS_OR_UNKNOWN"
    assert post_calls == []


def test_buy_test_blocks_insufficient_krw():
    helper = load_helper_module()
    post_calls = []
    install_safe_gate_stubs(helper, post_calls)

    def fake_low_krw_get(path, query=None):
        if path == "/v1/orders/open":
            return {"status": 200, "body": [], "remaining_req": None}
        if path == "/v1/accounts":
            return {"status": 200, "body": [{"currency": "KRW", "balance": "9999"}], "remaining_req": None}
        raise AssertionError(f"unexpected GET {path}")

    helper._upbit_get = fake_low_krw_get
    result = helper.buy_test_telemetry(helper.BuyTestRequest(**valid_buy_payload()))
    assert result["error_name"] == "LIVE_BUY_KRW_BALANCE_NOT_SUFFICIENT"
    assert post_calls == []


def test_buy_test_blocks_crossed_taker_price():
    helper = load_helper_module()
    post_calls = []
    install_safe_gate_stubs(helper, post_calls)
    result = helper.buy_test_telemetry(helper.BuyTestRequest(**valid_buy_payload(price="100050000", volume="0.00009995")))
    assert result["error_name"] == "LIVE_BUY_MAKER_LIMIT_REQUIRED"
    assert post_calls == []


def test_buy_test_success_calls_orders_test_only():
    helper = load_helper_module()
    post_calls = []
    install_safe_gate_stubs(helper, post_calls)
    result = helper.buy_test_telemetry(helper.BuyTestRequest(**valid_buy_payload()))
    assert result["buy_order_test_passed"] is True
    assert result["live_buy_attempted"] is False
    assert post_calls == [
        (
            "/v1/orders/test",
            {"market": "KRW-BTC", "side": "bid", "ord_type": "limit", "price": "100000000", "volume": "0.0001"},
        )
    ]


def test_live_buy_blocks_without_test():
    helper = load_helper_module()
    post_calls = []
    install_safe_gate_stubs(helper, post_calls)
    result = helper.live_buy_telemetry(
        helper.LiveBuyRequest(
            **valid_buy_payload(
                live_buy_enabled=True,
                execution_allowed=True,
                execution_mode="live",
                all_pass=True,
                duplicate_lock_status="clear",
                system_stop_active=False,
                buy_order_test_passed=False,
                one_time_live_buy_attempt_allowed=True,
            )
        )
    )
    assert result["error_name"] == "LIVE_BUY_TEST_NOT_PASSED"
    assert post_calls == []


def test_live_buy_blocks_fingerprint_mismatch():
    helper = load_helper_module()
    post_calls = []
    install_safe_gate_stubs(helper, post_calls)
    result = helper.live_buy_telemetry(
        helper.LiveBuyRequest(
            **valid_buy_payload(
                live_buy_enabled=True,
                execution_allowed=True,
                execution_mode="live",
                all_pass=True,
                duplicate_lock_status="clear",
                system_stop_active=False,
                buy_order_test_passed=True,
                buy_test_fingerprint="wrong",
                one_time_live_buy_attempt_allowed=True,
            )
        )
    )
    assert result["error_name"] == "LIVE_BUY_TEST_FINGERPRINT_MISMATCH"
    assert post_calls == []


def test_live_buy_rechecks_open_order_before_post():
    helper = load_helper_module()
    post_calls = []
    install_safe_gate_stubs(helper, post_calls)
    fingerprint = helper._buy_fingerprint("KRW-BTC", "bid", "limit", helper.Decimal("100000000"), helper.Decimal("0.0001"), helper.Decimal("10000"))

    def fake_open_order_get(path, query=None):
        if path == "/v1/orders/open":
            return {"status": 200, "body": [{"market": "KRW-BTC", "state": "wait"}], "remaining_req": None}
        raise AssertionError(f"unexpected GET {path}")

    helper._upbit_get = fake_open_order_get
    result = helper.live_buy_telemetry(
        helper.LiveBuyRequest(
            **valid_buy_payload(
                live_buy_enabled=True,
                execution_allowed=True,
                execution_mode="live",
                all_pass=True,
                duplicate_lock_status="clear",
                system_stop_active=False,
                buy_order_test_passed=True,
                buy_test_fingerprint=fingerprint,
                one_time_live_buy_attempt_allowed=True,
            )
        )
    )
    assert result["error_name"] == "LIVE_BUY_OPEN_ORDER_EXISTS_OR_UNKNOWN"
    assert post_calls == []


def test_live_buy_success_posts_limit_bid_only():
    helper = load_helper_module()
    post_calls = []
    install_safe_gate_stubs(helper, post_calls)
    fingerprint = helper._buy_fingerprint("KRW-BTC", "bid", "limit", helper.Decimal("100000000"), helper.Decimal("0.0001"), helper.Decimal("10000"))
    result = helper.live_buy_telemetry(
        helper.LiveBuyRequest(
            **valid_buy_payload(
                live_buy_enabled=True,
                execution_allowed=True,
                execution_mode="live",
                all_pass=True,
                duplicate_lock_status="clear",
                system_stop_active=False,
                buy_order_test_passed=True,
                buy_test_fingerprint=fingerprint,
                one_time_live_buy_attempt_allowed=True,
            )
        )
    )
    assert result["live_buy_attempted"] is True
    assert result["live_buy_accepted"] is True
    assert post_calls == [
        (
            "/v1/orders",
            {"market": "KRW-BTC", "side": "bid", "ord_type": "limit", "price": "100000000", "volume": "0.0001"},
        )
    ]


if __name__ == "__main__":
    test_buy_test_blocks_market_order()
    test_buy_test_blocks_ask()
    test_buy_test_blocks_unapproved_market()
    test_buy_test_blocks_defensive_news()
    test_buy_test_blocks_low_brain_score()
    test_buy_test_blocks_open_order()
    test_buy_test_blocks_insufficient_krw()
    test_buy_test_blocks_crossed_taker_price()
    test_buy_test_success_calls_orders_test_only()
    test_live_buy_blocks_without_test()
    test_live_buy_blocks_fingerprint_mismatch()
    test_live_buy_rechecks_open_order_before_post()
    test_live_buy_success_posts_limit_bid_only()
    print("HELPER_LIVE_BUY_ENDPOINT_TESTS_PASS")
