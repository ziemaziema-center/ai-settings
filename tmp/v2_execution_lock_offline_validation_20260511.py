import importlib.util
import json
import os
import shutil
import sys
import types
from pathlib import Path


class FakeRoute:
    def __init__(self, path):
        self.path = path


class FakeFastAPI:
    def __init__(self, *args, **kwargs):
        self.routes = []

    def get(self, path):
        def decorator(fn):
            self.routes.append(FakeRoute(path))
            return fn
        return decorator

    def post(self, path):
        def decorator(fn):
            self.routes.append(FakeRoute(path))
            return fn
        return decorator


class FakeBaseModel:
    def __init__(self, **kwargs):
        for cls in reversed(self.__class__.mro()):
            annotations = getattr(cls, "__annotations__", {})
            for name in annotations:
                if hasattr(cls, name):
                    setattr(self, name, getattr(cls, name))
                else:
                    setattr(self, name, None)
        for key, value in kwargs.items():
            setattr(self, key, value)


def load_helper(root: Path):
    fastapi = types.ModuleType("fastapi")
    fastapi.FastAPI = FakeFastAPI
    pydantic = types.ModuleType("pydantic")
    pydantic.BaseModel = FakeBaseModel
    sys.modules["fastapi"] = fastapi
    sys.modules["pydantic"] = pydantic

    module_path = root / "upbit-helper" / "app" / "main.py"
    spec = importlib.util.spec_from_file_location("upbit_helper_main", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def acquire_payload(module, **overrides):
    data = {
        "market": "KRW-BTC",
        "side": "bid",
        "ord_type": "limit",
        "run_id": "offline-run",
        "approval_id": "offline-approval",
        "fuse_id": "offline-fuse",
        "owner_token": "owner-token-1",
        "human_approval": True,
        "lock_reason": "OFFLINE_VALIDATION",
        "open_order_exists": False,
        "open_order_count": 0,
        "duplicate_order_exists": False,
        "reconciliation_classification": "cancel",
        "workflow_active": False,
        "cron_enabled": False,
        "fuse_state": "disabled",
        "order_journal_evidence": True,
        "expires_at_kst": "2026-05-11T22:30:00+09:00",
        "now_kst": "2026-05-11T22:20:00+09:00",
    }
    data.update(overrides)
    return module.ExecutionLockAcquireRequest(**data)


def release_payload(module, lock_id, **overrides):
    data = {
        "lock_id": lock_id,
        "owner_token": "owner-token-1",
        "release_reason": "offline_release_validation",
        "human_approval": True,
        "open_order_exists": False,
        "open_order_count": 0,
        "reconciliation_classification": "cancel",
        "workflow_active": False,
        "cron_enabled": False,
        "fuse_state": "disabled",
        "now_kst": "2026-05-11T22:21:00+09:00",
    }
    data.update(overrides)
    return module.ExecutionLockReleaseRequest(**data)


def reset_fixture(fixture_root: Path):
    if fixture_root.exists():
        shutil.rmtree(fixture_root)
    fixture_root.mkdir(parents=True, exist_ok=True)


def assert_true(condition, name, detail=None):
    if not condition:
        raise AssertionError(f"{name}: {detail}")


def main():
    root = Path(r"C:\Users\minho\Documents\02_work\03_AI\03_investment_automation\01_planning")
    fixture_root = root / "tests" / "execution_lock_runtime_fixture"
    report_json = root / "reports" / "V2_execution_lock_offline_validation_2026-05-11.json"
    report_md = root / "reports" / "V2_execution_lock_offline_validation_2026-05-11.md"

    reset_fixture(fixture_root)
    os.environ["KBIA_EXECUTION_LOCK_ROOT"] = str(fixture_root)
    module = load_helper(root)

    network_called = {"get": False, "post": False}

    def fake_get(*args, **kwargs):
        network_called["get"] = True
        raise AssertionError("live API GET called")

    def fake_post(*args, **kwargs):
        network_called["post"] = True
        raise AssertionError("live API POST called")

    module._upbit_get = fake_get
    module._upbit_post = fake_post

    results = {}

    # 1. no active lock -> acquire succeeds
    acquire = module.execution_lock_acquire(acquire_payload(module))
    results["acquire_no_lock"] = acquire
    assert_true(acquire["success"] is True and acquire["lock_acquired"] is True, "acquire_no_lock", acquire)
    lock_id = acquire["lock_id"]

    # 2. active lock exists -> acquire blocked
    existing = module.execution_lock_acquire(acquire_payload(module, run_id="second-run"))
    results["acquire_existing_lock_blocked"] = existing
    assert_true(existing["success"] is False and existing["lock_acquired"] is False, "acquire_existing_lock_blocked", existing)
    assert_true(existing["blocked_reason"] == "ACTIVE_LOCK_EXISTS", "existing_lock_reason", existing)

    # 5. release with mismatched owner/token blocked
    mismatch = module.execution_lock_release(release_payload(module, lock_id, owner_token="wrong-token"))
    results["mismatched_release_blocked"] = mismatch
    assert_true(mismatch["success"] is False and mismatch["lock_released"] is False, "mismatched_release_blocked", mismatch)
    assert_true("OWNER_TOKEN_MISMATCH" in mismatch["blocked_reason"], "mismatched_reason", mismatch)

    # 4. release with matching owner/token succeeds
    release = module.execution_lock_release(release_payload(module, lock_id))
    results["matching_release"] = release
    assert_true(release["success"] is True and release["lock_released"] is True, "matching_release", release)

    # 3. stale lock exists -> blocked + human review required
    reset_fixture(fixture_root)
    stale_acquire = module.execution_lock_acquire(
        acquire_payload(
            module,
            run_id="stale-run",
            expires_at_kst="2026-05-11T22:00:00+09:00",
            now_kst="2026-05-11T21:59:00+09:00",
        )
    )
    assert_true(stale_acquire["success"] is True, "stale_setup_acquire", stale_acquire)
    stale = module.execution_lock_acquire(acquire_payload(module, run_id="after-stale", now_kst="2026-05-11T22:10:00+09:00"))
    results["stale_lock_blocked"] = stale
    assert_true(stale["success"] is False and stale["human_review_required"] is True, "stale_lock_blocked", stale)
    assert_true(stale["current_lock_state"] == "stale_stop", "stale_state", stale)

    # 7. partial write safety
    reset_fixture(fixture_root)
    active_path = module._active_lock_path()
    active_path.parent.mkdir(parents=True, exist_ok=True)
    partial_path = active_path.with_name(f"{active_path.name}.tmp.partial-validation")
    partial_path.write_text("{", encoding="utf-8")
    partial = module.execution_lock_acquire(acquire_payload(module, run_id="partial-run"))
    results["partial_write_safety"] = partial
    assert_true(partial["success"] is False, "partial_write_safety", partial)
    assert_true(partial["blocked_reason"] == "LOCK_PARTIAL_WRITE_PRESENT", "partial_reason", partial)
    partial_path.unlink()

    # 6. journal append works
    journal_files = sorted((fixture_root / "execution-lock-journal").glob("*.jsonl"))
    journal_line_count = 0
    for path in journal_files:
        journal_line_count += len(path.read_text(encoding="utf-8").splitlines())
    results["journal_append"] = {
        "journal_files": [str(path) for path in journal_files],
        "journal_line_count": journal_line_count,
    }
    assert_true(journal_files and journal_line_count >= 1, "journal_append", results["journal_append"])

    # 8. existing helper endpoints remain preserved with mocked reads.
    assert_true(module.health()["ok"] is True, "health")
    module._upbit_get = lambda path, query=None: {
        "status": 200,
        "remaining_req": "mock",
        "body": [] if path == "/v1/orders/open" else [{"currency": "KRW", "balance": "10000"}],
    }
    accounts = module.accounts_telemetry(module.AccountsTelemetryRequest(estimated_krw_value="5000"))
    open_orders = module.open_orders_telemetry(module.OpenOrdersRequest(market="KRW-BTC"))
    order_test = module.order_test_telemetry(module.OrderTestRequest(market="KRW-ETH", side="bid", ord_type="limit", price="1", volume="1"))
    live_order = module.live_order_telemetry(module.LiveOrderRequest())
    results["existing_helper_endpoints_offline"] = {
        "health": "PASS",
        "accounts_success": accounts.get("success"),
        "open_orders_success": open_orders.get("success"),
        "order_test_blocked": order_test.get("order_test_passed") is False,
        "live_order_blocked": live_order.get("live_order_attempted") is False,
    }
    assert_true(results["existing_helper_endpoints_offline"]["accounts_success"] is True, "accounts")
    assert_true(results["existing_helper_endpoints_offline"]["open_orders_success"] is True, "open_orders")
    assert_true(results["existing_helper_endpoints_offline"]["order_test_blocked"], "order_test_blocked")
    assert_true(results["existing_helper_endpoints_offline"]["live_order_blocked"], "live_order_blocked")

    # 9-10. no workflow interaction, no live API/order/cancel/reorder path called by lock code.
    routes = sorted(getattr(route, "path", "") for route in module.app.routes)
    lock_routes = [route for route in routes if route.startswith("/execution-lock/")]
    output = {
        "overall_status": "PASS",
        "lock_routes": lock_routes,
        "results": {
            "offline_lock_tests": "PASS",
            "acquire_no_lock": "PASS",
            "acquire_existing_lock_blocked": "PASS",
            "stale_lock_blocked": "PASS",
            "matching_release": "PASS",
            "mismatched_release_blocked": "PASS",
            "journal_append": "PASS",
            "partial_write_safety": "PASS",
            "existing_helper_endpoints_offline": "PASS",
            "workflow_interaction_added": False,
            "live_api_called": False,
            "network_called_before_existing_endpoint_mock": network_called,
        },
        "fixture_root": str(fixture_root),
        "lock_journal_validation_path": str(journal_files[-1]) if journal_files else None,
    }

    report_json.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    report_md.write_text(
        "\n".join(
            [
                "# V2 Execution Lock Offline Validation",
                "",
                "Result: PASS",
                "",
                "- Offline lock tests: PASS",
                "- Acquire with no active lock: PASS",
                "- Existing active lock blocks acquire: PASS",
                "- Stale lock blocks acquire and requires human review: PASS",
                "- Matching release succeeds: PASS",
                "- Mismatched release is blocked: PASS",
                "- Append-only lock journal works: PASS",
                "- Partial write safety blocks acquire: PASS",
                "- Existing helper endpoints preserved offline: PASS",
                "- Workflow interaction added: false",
                "- Live API called: false",
                "",
                f"Fixture root: `{fixture_root}`",
                f"Lock journal validation path: `{output['lock_journal_validation_path']}`",
            ]
        ),
        encoding="utf-8",
    )
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
