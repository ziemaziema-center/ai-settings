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

    spec = importlib.util.spec_from_file_location("upbit_helper_lock_recovery_test", MAIN_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    temp_root = Path(tempfile.mkdtemp(prefix="kbia_lock_recovery_"))
    os.environ["KBIA_EXECUTION_LOCK_ROOT"] = str(temp_root)
    return module, temp_root


def acquire_lock(helper, expires_at_kst: str):
    return helper.execution_lock_acquire(
        helper.ExecutionLockAcquireRequest(
            market="KRW-ETC",
            side="ask",
            ord_type="limit",
            run_id="test-run",
            approval_id="test-approval",
            fuse_id="test-fuse",
            owner_token="owner-token",
            human_approval=True,
            lock_reason="test",
            open_order_exists=False,
            open_order_count=0,
            duplicate_order_exists=False,
            reconciliation_classification="done",
            workflow_active=False,
            cron_enabled=False,
            fuse_state="armed",
            order_journal_evidence=True,
            expires_at_kst=expires_at_kst,
            now_kst="2026-05-24T10:00:00+09:00",
        )
    )


def recovery_payload(helper):
    return helper.ExecutionLockRecoverStaleFinalityRequest(
        automated_recovery_allowed=True,
        recovery_reason="unit_test_stale_lock_recovery",
        workflow_active=False,
        cron_enabled=False,
        now_kst="2026-05-24T10:00:00+09:00",
    )


def install_done_finality_stubs(helper):
    def fake_upbit_get(path, query=None):
        if path == "/v1/orders/open":
            return {"status": 200, "body": [], "remaining_req": "group=default; min=599; sec=9"}
        if path == "/v1/orders/closed":
            return {
                "status": 200,
                "body": [
                    {
                        "uuid": "12345678-1234-1234-1234-123456789abc",
                        "market": "KRW-ETC",
                        "side": "ask",
                        "ord_type": "limit",
                        "state": "done",
                        "remaining_volume": "0",
                        "executed_volume": "1",
                        "trades_count": 1,
                        "price": "1000",
                    }
                ],
                "remaining_req": "group=default; min=599; sec=9",
            }
        raise AssertionError(f"unexpected GET {path}")

    helper._upbit_get = fake_upbit_get


def test_stale_lock_recovery_releases_when_finality_done_and_no_open_order():
    helper, _ = load_helper_module()
    acquire = acquire_lock(helper, "2026-05-24T09:00:00+09:00")
    assert acquire["lock_acquired"] is True
    install_done_finality_stubs(helper)

    result = helper.execution_lock_recover_stale_finality(recovery_payload(helper))
    assert result["lock_recovered"] is True
    assert result["market"] == "KRW-ETC"
    assert result["final_classification"] == "done"
    assert result["open_order_count"] == 0
    assert helper._active_lock_path().exists() is False


def test_stale_lock_recovery_blocks_when_open_order_exists():
    helper, _ = load_helper_module()
    acquire = acquire_lock(helper, "2026-05-24T09:00:00+09:00")
    assert acquire["lock_acquired"] is True

    def fake_upbit_get(path, query=None):
        if path == "/v1/orders/open":
            return {"status": 200, "body": [{"market": "KRW-ETC", "state": "wait"}], "remaining_req": None}
        raise AssertionError(f"unexpected GET {path}")

    helper._upbit_get = fake_upbit_get
    result = helper.execution_lock_recover_stale_finality(recovery_payload(helper))
    assert result["lock_recovered"] is False
    assert "OPEN_ORDER_EXISTS" in result["blocked_reason"]
    assert helper._active_lock_path().exists() is True


def test_stale_lock_recovery_blocks_when_lock_is_not_stale():
    helper, _ = load_helper_module()
    acquire = acquire_lock(helper, "2026-05-24T11:00:00+09:00")
    assert acquire["lock_acquired"] is True
    install_done_finality_stubs(helper)

    result = helper.execution_lock_recover_stale_finality(recovery_payload(helper))
    assert result["lock_recovered"] is False
    assert "LOCK_NOT_STALE" in result["blocked_reason"]
    assert helper._active_lock_path().exists() is True


if __name__ == "__main__":
    test_stale_lock_recovery_releases_when_finality_done_and_no_open_order()
    test_stale_lock_recovery_blocks_when_open_order_exists()
    test_stale_lock_recovery_blocks_when_lock_is_not_stale()
    print("HELPER_EXECUTION_LOCK_RECOVERY_TESTS_PASS")
