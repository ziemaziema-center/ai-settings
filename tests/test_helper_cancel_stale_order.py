from __future__ import annotations

import importlib.util
import os
import sys
import tempfile
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

    spec = importlib.util.spec_from_file_location("upbit_helper_cancel_stale_test", MAIN_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    temp_root = Path(tempfile.mkdtemp(prefix="kbia_cancel_stale_"))
    os.environ["KBIA_EXECUTION_LOCK_ROOT"] = str(temp_root)
    return module


def acquire_lock(helper):
    result = helper.execution_lock_acquire(
        helper.ExecutionLockAcquireRequest(
            market="KRW-ETC",
            side="ask",
            ord_type="limit",
            run_id="cancel-test-run",
            approval_id="cancel-test-approval",
            fuse_id="cancel-test-fuse",
            owner_token="owner-token",
            human_approval=True,
            lock_reason="cancel_test",
            open_order_exists=False,
            open_order_count=0,
            duplicate_order_exists=False,
            reconciliation_classification="done",
            workflow_active=False,
            cron_enabled=False,
            fuse_state="armed",
            order_journal_evidence=True,
            expires_at_kst="2026-05-25T12:00:00+09:00",
            now_kst="2026-05-25T10:00:00+09:00",
        )
    )
    assert result["lock_acquired"] is True


def cancel_payload(helper, **overrides):
    payload = {
        "market": "KRW-ETC",
        "side": "ask",
        "ord_type": "limit",
        "cancel_enabled": True,
        "execution_allowed": True,
        "execution_mode": "live",
        "one_time_cancel_allowed": True,
        "human_approval": True,
        "min_open_age_minutes": 30,
        "workflow_active": False,
        "cron_enabled": False,
        "system_stop_active": False,
        "now_kst": "2026-05-25T10:00:00+09:00",
    }
    payload.update(overrides)
    return helper.CancelStaleOrderRequest(**payload)


def open_order(**overrides):
    row = {
        "uuid": "12345678-1234-1234-1234-123456789abc",
        "market": "KRW-ETC",
        "side": "ask",
        "ord_type": "limit",
        "state": "wait",
        "created_at": "2026-05-25T09:00:00+09:00",
        "remaining_volume": "2.1",
        "executed_volume": "0",
        "trades_count": 0,
        "price": "13000",
    }
    row.update(overrides)
    return row


def install_open_order_stub(helper, row, delete_calls):
    def fake_upbit_get(path, query=None):
        if path == "/v1/orders/open":
            return {"status": 200, "body": [row], "remaining_req": "group=default; min=599; sec=9"}
        raise AssertionError(f"unexpected GET {path}")

    def fake_upbit_delete(path, query):
        delete_calls.append((path, query))
        return {"status": 200, "body": {"state": "cancel"}, "remaining_req": "group=default; min=599; sec=8"}

    helper._upbit_get = fake_upbit_get
    helper._upbit_delete = fake_upbit_delete


def test_cancel_stale_order_success_deletes_uuid_without_returning_raw_uuid():
    helper = load_helper_module()
    acquire_lock(helper)
    delete_calls = []
    install_open_order_stub(helper, open_order(), delete_calls)

    result = helper.cancel_stale_order_telemetry(cancel_payload(helper))
    assert result["cancel_attempted"] is True
    assert result["cancel_accepted"] is True
    assert result["uuid_masked"] == "1234...9abc"
    assert "12345678-1234-1234-1234-123456789abc" not in str(result)
    assert delete_calls == [("/v1/order", {"uuid": "12345678-1234-1234-1234-123456789abc"})]


def test_cancel_stale_order_blocks_partial_fill():
    helper = load_helper_module()
    acquire_lock(helper)
    delete_calls = []
    install_open_order_stub(helper, open_order(executed_volume="0.1"), delete_calls)

    result = helper.cancel_stale_order_telemetry(cancel_payload(helper))
    assert result["cancel_attempted"] is False
    assert "CANCEL_ZERO_EXECUTION_REQUIRED" in result["blocked_reason"]
    assert delete_calls == []


def test_cancel_stale_order_blocks_young_order():
    helper = load_helper_module()
    acquire_lock(helper)
    delete_calls = []
    install_open_order_stub(helper, open_order(created_at="2026-05-25T09:45:00+09:00"), delete_calls)

    result = helper.cancel_stale_order_telemetry(cancel_payload(helper))
    assert result["cancel_attempted"] is False
    assert "CANCEL_ORDER_NOT_STALE_ENOUGH" in result["blocked_reason"]
    assert delete_calls == []


if __name__ == "__main__":
    test_cancel_stale_order_success_deletes_uuid_without_returning_raw_uuid()
    test_cancel_stale_order_blocks_partial_fill()
    test_cancel_stale_order_blocks_young_order()
    print("HELPER_CANCEL_STALE_ORDER_TESTS_PASS")
