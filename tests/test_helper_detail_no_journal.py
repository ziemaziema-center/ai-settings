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

    spec = importlib.util.spec_from_file_location("upbit_helper_main_no_journal_test", MAIN_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_detail_no_journal_route_does_not_append_journal():
    helper = load_helper_module()
    journal_calls = []

    def fake_upbit_get(path, query=None):
        assert path == "/v1/orders/open"
        assert query == {"market": "KRW-BTC"}
        return {"status": 200, "body": [], "remaining_req": "group=default; min=599; sec=9"}

    def fake_append_detail_journal(event):
        journal_calls.append(event)
        return {"success": True, "path_masked": "masked", "error_name": None}

    helper._upbit_get = fake_upbit_get
    helper._append_detail_journal = fake_append_detail_journal

    payload = helper.DetailTelemetryRequest(
        market="KRW-BTC",
        run_id="unit-no-journal",
        include_recent_closed=False,
        journal_enabled=True,
    )
    result = helper.open_orders_detail_telemetry_no_journal(payload)

    assert result["endpoint"] == "/upbit/open-orders/detail-telemetry-no-journal"
    assert result["journal_write"]["attempted"] is False
    assert journal_calls == []


def test_detail_route_preserves_journal_enabled_behavior():
    helper = load_helper_module()
    journal_calls = []

    def fake_upbit_get(path, query=None):
        assert path == "/v1/orders/open"
        assert query == {"market": "KRW-BTC"}
        return {"status": 200, "body": [], "remaining_req": "group=default; min=599; sec=9"}

    def fake_append_detail_journal(event):
        journal_calls.append(event)
        return {"success": True, "path_masked": "masked", "error_name": None}

    helper._upbit_get = fake_upbit_get
    helper._append_detail_journal = fake_append_detail_journal

    payload = helper.DetailTelemetryRequest(
        market="KRW-BTC",
        run_id="unit-journal",
        include_recent_closed=False,
        journal_enabled=True,
    )
    result = helper.open_orders_detail_telemetry(payload)

    assert result["endpoint"] == "/upbit/open-orders/detail-telemetry"
    assert result["journal_write"]["success"] is True
    assert len(journal_calls) == 1
    assert journal_calls[0]["endpoint"] == "/upbit/open-orders/detail-telemetry"


if __name__ == "__main__":
    test_detail_no_journal_route_does_not_append_journal()
    test_detail_route_preserves_journal_enabled_behavior()
    print("NO_JOURNAL_UNIT_TESTS_PASS")
