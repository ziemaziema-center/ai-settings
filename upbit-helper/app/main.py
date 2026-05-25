import base64
import hashlib
import hmac
import json
import os
import re
import uuid
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any
from urllib import error, parse, request

from fastapi import FastAPI
from pydantic import BaseModel


UPBIT_BASE_URL = "https://api.upbit.com"
SERVICE_NAME = "upbit-helper"
LOCK_SCHEMA_VERSION = "v2.execution_lock.1"

app = FastAPI(title=SERVICE_NAME, version="1.0.0")


class OpenOrdersRequest(BaseModel):
    market: str


class DetailCorrelationHint(BaseModel):
    market: str | None = None
    side: str | None = None
    ord_type: str | None = None
    created_at: str | None = None


class DetailTelemetryRequest(BaseModel):
    market: str
    run_id: str | None = None
    include_recent_closed: bool = True
    recent_closed_limit: int = 20
    journal_enabled: bool = True
    correlation_hint: DetailCorrelationHint | None = None


class AccountsTelemetryRequest(BaseModel):
    estimated_krw_value: float | int | str | None = None


class OrderTestRequest(BaseModel):
    market: str
    side: str
    ord_type: str
    price: float | int | str
    volume: float | int | str


class LiveOrderRequest(BaseModel):
    live_order_enabled: bool | str | int | None = None
    execution_allowed: bool | str | int | None = None
    execution_mode: str | None = None
    all_pass: bool | str | int | None = None
    market: str | None = None
    side: str | None = None
    ord_type: str | None = None
    price: float | int | str | None = None
    volume: float | int | str | None = None
    estimated_krw_value: float | int | str | None = None
    duplicate_lock_status: str | None = None
    open_order_exists: bool | str | int | None = None
    system_stop_active: bool | str | int | None = None
    order_test_passed: bool | str | int | None = None
    one_time_live_attempt_allowed: bool | str | int | None = None


class SellTestRequest(BaseModel):
    market: str
    side: str
    ord_type: str
    price: float | int | str
    volume: float | int | str
    estimated_krw_value: float | int | str
    open_order_exists: bool | str | int | None = None
    portfolio_plan_valid: bool | str | int | None = None
    cleanup_candidate: bool | str | int | None = None
    cleanup_action: str | None = None
    best_bid: float | int | str | None = None
    best_ask: float | int | str | None = None
    orderbook_timestamp_ms: int | str | None = None
    now_ms: int | str | None = None


class LiveSellRequest(SellTestRequest):
    live_sell_enabled: bool | str | int | None = None
    execution_allowed: bool | str | int | None = None
    execution_mode: str | None = None
    all_pass: bool | str | int | None = None
    duplicate_lock_status: str | None = None
    system_stop_active: bool | str | int | None = None
    sell_order_test_passed: bool | str | int | None = None
    sell_test_fingerprint: str | None = None
    one_time_live_sell_attempt_allowed: bool | str | int | None = None


class CancelStaleOrderRequest(BaseModel):
    market: str
    side: str
    ord_type: str
    cancel_enabled: bool | str | int | None = None
    execution_allowed: bool | str | int | None = None
    execution_mode: str | None = None
    one_time_cancel_allowed: bool | str | int | None = None
    human_approval: bool | str | int | None = None
    min_open_age_minutes: int | str | None = None
    workflow_active: bool | str | int | None = None
    cron_enabled: bool | str | int | None = None
    system_stop_active: bool | str | int | None = None
    now_kst: str | None = None


class BuyTestRequest(BaseModel):
    market: str
    side: str
    ord_type: str
    price: float | int | str
    volume: float | int | str
    estimated_krw_value: float | int | str
    open_order_exists: bool | str | int | None = None
    brain_schema_version: str | None = None
    brain_action: str | None = None
    brain_live_ready: bool | str | int | None = None
    brain_candidate_score: float | int | str | None = None
    news_bias: str | None = None
    scalping_candidate: bool | str | int | None = None
    best_bid: float | int | str | None = None
    best_ask: float | int | str | None = None
    orderbook_timestamp_ms: int | str | None = None
    now_ms: int | str | None = None


class LiveBuyRequest(BuyTestRequest):
    live_buy_enabled: bool | str | int | None = None
    execution_allowed: bool | str | int | None = None
    execution_mode: str | None = None
    all_pass: bool | str | int | None = None
    duplicate_lock_status: str | None = None
    system_stop_active: bool | str | int | None = None
    buy_order_test_passed: bool | str | int | None = None
    buy_test_fingerprint: str | None = None
    one_time_live_buy_attempt_allowed: bool | str | int | None = None


class ExecutionLockStatusRequest(BaseModel):
    now_kst: str | None = None


class ExecutionLockAcquireRequest(BaseModel):
    market: str
    side: str
    ord_type: str
    run_id: str
    approval_id: str
    fuse_id: str
    owner_token: str
    human_approval: bool | str | int | None = None
    lock_reason: str | None = None
    open_order_exists: bool | str | int | None = None
    open_order_count: int | str | None = None
    duplicate_order_exists: bool | str | int | None = None
    reconciliation_classification: str | None = None
    workflow_active: bool | str | int | None = None
    cron_enabled: bool | str | int | None = None
    fuse_state: str | None = None
    order_journal_evidence: bool | str | int | None = None
    expires_at_kst: str | None = None
    now_kst: str | None = None


class ExecutionLockReleaseRequest(BaseModel):
    lock_id: str
    owner_token: str
    release_reason: str
    human_approval: bool | str | int | None = None
    open_order_exists: bool | str | int | None = None
    open_order_count: int | str | None = None
    reconciliation_classification: str | None = None
    workflow_active: bool | str | int | None = None
    cron_enabled: bool | str | int | None = None
    fuse_state: str | None = None
    now_kst: str | None = None


class ExecutionLockRecoverStaleFinalityRequest(BaseModel):
    automated_recovery_allowed: bool | str | int | None = None
    recovery_reason: str | None = None
    workflow_active: bool | str | int | None = None
    cron_enabled: bool | str | int | None = None
    now_kst: str | None = None


LIVE_SELL_ALLOWED_MARKETS = {"KRW-FCT2", "KRW-DOT", "KRW-ALGO", "KRW-ETC", "KRW-DOGE"}
LIVE_SELL_ALLOWED_ACTIONS = {"EXIT_STAGED", "REDUCE_STAGED"}
LIVE_SELL_MIN_KRW = Decimal("5000")
LIVE_SELL_MAX_KRW = Decimal("30000")
LIVE_SELL_MAX_ORDERBOOK_AGE_MS = 10000
LIVE_CANCEL_MIN_OPEN_AGE_MINUTES = 30
LIVE_CANCEL_MAX_OPEN_AGE_MINUTES = 1440
LIVE_BUY_ALLOWED_MARKETS = {"KRW-BTC", "KRW-ETH", "KRW-SOL"}
LIVE_BUY_MIN_KRW = Decimal("5000")
LIVE_BUY_MAX_KRW = Decimal("10000")
LIVE_BUY_MAX_ORDERBOOK_AGE_MS = 10000
LIVE_BUY_MAX_SPREAD_BPS = Decimal("12")
LIVE_BUY_MIN_BRAIN_SCORE = Decimal("78")


def _decimal_or_none(value: Any) -> Decimal | None:
    if value is None:
        return None
    try:
        parsed = Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None
    if not parsed.is_finite():
        return None
    return parsed


def _int_or_none(value: Any) -> int | None:
    if value is None:
        return None
    try:
        return int(str(value))
    except (TypeError, ValueError):
        return None


def _krw_band(value: Decimal | None) -> str | None:
    if value is None:
        return None
    if value <= Decimal("0"):
        return "0"
    if value < Decimal("5000"):
        return "1-4999"
    if value < Decimal("30000"):
        return "5000-29999"
    return "30000+"


def _strict_true(value: Any) -> bool:
    return value is True or value == 1 or value == "1" or value == "true" or value == "TRUE"


def _strict_false(value: Any) -> bool:
    return value is False or value == 0 or value == "0" or value == "false" or value == "FALSE"


def _base64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def _json_b64(payload: dict[str, Any]) -> str:
    return _base64url(json.dumps(payload, separators=(",", ":")).encode("utf-8"))


def _sanitize_message(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value)
    text = re.sub(r"Bearer\s+[A-Za-z0-9._-]+", "Bearer [REDACTED]", text)
    text = re.sub(
        r"[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}",
        "[REDACTED_JWT]",
        text,
    )
    return text[:500]


def _kst_now() -> str:
    return datetime.now(timezone(timedelta(hours=9))).isoformat(timespec="seconds")


def _mask_uuid(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value)
    if len(text) <= 8:
        return "[MASKED]"
    return f"{text[:4]}...{text[-4:]}"


def _safe_int(value: Any, default: int, minimum: int, maximum: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default
    return max(minimum, min(maximum, parsed))


def _detail_classification(row: dict[str, Any]) -> tuple[str, str | None]:
    state = row.get("state")
    remaining_volume = _decimal_or_none(row.get("remaining_volume"))
    executed_volume = _decimal_or_none(row.get("executed_volume"))

    if not state:
        return "unknown_stop", "DETAIL_MISSING_STATE"
    if remaining_volume is None or executed_volume is None:
        return "unknown_stop", "DETAIL_MISSING_OR_MALFORMED_VOLUME"
    if remaining_volume < 0 or executed_volume < 0:
        return "unknown_stop", "DETAIL_NEGATIVE_VOLUME"

    state_text = str(state)
    if state_text == "cancel":
        return "cancel", None
    if state_text == "done" and executed_volume > 0 and remaining_volume == 0:
        return "done", None
    if remaining_volume == 0 and executed_volume > 0:
        return "done", None
    if state_text == "wait" and executed_volume == 0 and remaining_volume > 0:
        return "wait", None
    if state_text == "wait" and executed_volume > 0 and remaining_volume > 0:
        return "partial_fill", None
    return "unknown_stop", "DETAIL_INCONSISTENT_OR_UNSUPPORTED_STATE"


def _sanitize_detail_order(row: Any) -> dict[str, Any]:
    order = row if isinstance(row, dict) else {}
    classification, blocked_reason = _detail_classification(order)
    return {
        "uuid_masked": _mask_uuid(order.get("uuid")),
        "market": _sanitize_message(order.get("market")),
        "side": _sanitize_message(order.get("side")),
        "ord_type": _sanitize_message(order.get("ord_type")),
        "state": _sanitize_message(order.get("state")),
        "created_at": _sanitize_message(order.get("created_at")),
        "remaining_volume": _sanitize_message(order.get("remaining_volume")),
        "executed_volume": _sanitize_message(order.get("executed_volume")),
        "trades_count": order.get("trades_count") if isinstance(order.get("trades_count"), int) else None,
        "paid_fee": _sanitize_message(order.get("paid_fee")),
        "locked": _sanitize_message(order.get("locked")),
        "price": _sanitize_message(order.get("price")),
        "classification": classification,
        "blocked_reason": blocked_reason,
    }


def _order_age_minutes(created_at: Any, now: datetime | None = None) -> int | None:
    if not created_at:
        return None
    created = _parse_kst(str(created_at))
    if created is None:
        return None
    current = now or datetime.now(timezone(timedelta(hours=9)))
    return max(0, int((current - created).total_seconds() // 60))


def _final_detail_classification(orders: list[dict[str, Any]], success: bool, error_name: str | None) -> tuple[str, str | None]:
    if not success:
        return "unknown_stop", error_name or "DETAIL_TELEMETRY_FAILED"
    if not orders:
        return "unknown_stop", "DETAIL_NO_ORDER_DETAIL"
    classifications = {str(order.get("classification")) for order in orders}
    if "unknown_stop" in classifications:
        return "unknown_stop", "DETAIL_ORDER_UNKNOWN_STOP"
    if "partial_fill" in classifications:
        return "partial_fill", None
    if "wait" in classifications:
        return "wait", None
    if "done" in classifications:
        return "done", None
    if classifications == {"cancel"}:
        return "cancel", None
    return "unknown_stop", "DETAIL_CLASSIFICATION_UNCLEAR"


def _journal_path() -> Path | None:
    raw_path = os.getenv("KBIA_ORDER_JOURNAL_DIR")
    if not raw_path:
        return None
    return Path(raw_path) / f"order_journal_{datetime.now(timezone(timedelta(hours=9))).date().isoformat()}.jsonl"


def _append_detail_journal(event: dict[str, Any]) -> dict[str, Any]:
    path = _journal_path()
    if path is None:
        return {
            "attempted": True,
            "success": False,
            "path_masked": None,
            "error_name": "HELPER_DETAIL_JOURNAL_PATH_MISSING",
        }
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, ensure_ascii=True, separators=(",", ":")) + "\n")
        return {
            "attempted": True,
            "success": True,
            "path_masked": path.name,
            "error_name": None,
        }
    except Exception as exc:
        return {
            "attempted": True,
            "success": False,
            "path_masked": path.name,
            "error_name": _sanitize_message(exc.__class__.__name__),
        }


def _parse_kst(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(str(value))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone(timedelta(hours=9)))
    return parsed


def _lock_now(value: str | None = None) -> datetime:
    return _parse_kst(value) or datetime.now(timezone(timedelta(hours=9)))


def _lock_root() -> Path:
    return Path(os.getenv("KBIA_EXECUTION_LOCK_ROOT") or "/home/ubuntu/kbia-logs/upbit-helper")


def _active_lock_path() -> Path:
    return _lock_root() / "execution-locks" / "active_execution_lock.json"


def _lock_journal_path(now: datetime | None = None) -> Path:
    current = now or _lock_now()
    return _lock_root() / "execution-lock-journal" / f"execution_lock_{current.date().isoformat()}.jsonl"


def _owner_token_hash(owner_token: str | None) -> str | None:
    if not owner_token:
        return None
    return hashlib.sha256(str(owner_token).encode("utf-8")).hexdigest()


def _read_json_file(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None, "LOCK_FILE_MISSING"
    except json.JSONDecodeError:
        return None, "LOCK_FILE_MALFORMED"
    except Exception as exc:
        return None, _sanitize_message(exc.__class__.__name__) or "LOCK_FILE_READ_FAILED"
    if not isinstance(data, dict):
        return None, "LOCK_FILE_NOT_OBJECT"
    return data, None


def _partial_lock_writes(path: Path) -> list[str]:
    parent = path.parent
    if not parent.exists():
        return []
    return sorted(item.name for item in parent.glob(f"{path.name}.tmp.*") if item.is_file())


def _validate_lock_payload(lock: dict[str, Any]) -> str | None:
    required = [
        "schema_version",
        "lock_id",
        "created_at_kst",
        "updated_at_kst",
        "market",
        "side",
        "ord_type",
        "lock_state",
        "run_id",
        "approval_id",
        "fuse_id",
        "owner_token_hash",
        "expires_at_kst",
        "forbidden_endpoint_check",
        "secrets_leak_check",
    ]
    for key in required:
        if lock.get(key) in (None, ""):
            return f"LOCK_MISSING_{key.upper()}"
    if lock.get("schema_version") != LOCK_SCHEMA_VERSION:
        return "LOCK_SCHEMA_VERSION_UNSUPPORTED"
    if lock.get("lock_state") not in {"active", "released", "stale_stop", "unknown_stop"}:
        return "LOCK_STATE_UNSUPPORTED"
    if _parse_kst(str(lock.get("created_at_kst"))) is None:
        return "LOCK_CREATED_AT_MALFORMED"
    if _parse_kst(str(lock.get("updated_at_kst"))) is None:
        return "LOCK_UPDATED_AT_MALFORMED"
    if _parse_kst(str(lock.get("expires_at_kst"))) is None:
        return "LOCK_EXPIRES_AT_MALFORMED"
    if lock.get("forbidden_endpoint_check") is not True or lock.get("secrets_leak_check") is not True:
        return "LOCK_SAFETY_CHECK_FAILED"
    return None


def _execution_lock_status(now_kst: str | None = None) -> dict[str, Any]:
    now = _lock_now(now_kst)
    path = _active_lock_path()
    partials = _partial_lock_writes(path)
    if partials:
        return {
            "success": False,
            "lock_state": "unknown_stop",
            "lock_exists": path.exists(),
            "stale_lock": False,
            "human_review_required": True,
            "blocked_reason": "LOCK_PARTIAL_WRITE_PRESENT",
            "active_lock_path": str(path),
            "lock_id": None,
            "partial_files": partials,
        }
    if not path.exists():
        return {
            "success": True,
            "lock_state": "unlocked",
            "lock_exists": False,
            "stale_lock": False,
            "human_review_required": False,
            "blocked_reason": None,
            "active_lock_path": str(path),
            "lock_id": None,
            "partial_files": [],
        }

    lock, error_name = _read_json_file(path)
    if lock is None:
        return {
            "success": False,
            "lock_state": "unknown_stop",
            "lock_exists": True,
            "stale_lock": False,
            "human_review_required": True,
            "blocked_reason": error_name,
            "active_lock_path": str(path),
            "lock_id": None,
            "partial_files": [],
        }
    validation_error = _validate_lock_payload(lock)
    if validation_error:
        return {
            "success": False,
            "lock_state": "unknown_stop",
            "lock_exists": True,
            "stale_lock": False,
            "human_review_required": True,
            "blocked_reason": validation_error,
            "active_lock_path": str(path),
            "lock_id": _sanitize_message(lock.get("lock_id")),
            "partial_files": [],
        }
    expires_at = _parse_kst(str(lock.get("expires_at_kst")))
    if expires_at is None:
        state = "unknown_stop"
        stale = False
        reason = "LOCK_EXPIRES_AT_MALFORMED"
    elif now > expires_at:
        state = "stale_stop"
        stale = True
        reason = "STALE_LOCK_EXISTS"
    else:
        state = str(lock.get("lock_state"))
        stale = False
        reason = "ACTIVE_LOCK_EXISTS" if state == "active" else None
    return {
        "success": state == "released",
        "lock_state": state,
        "lock_exists": True,
        "stale_lock": stale,
        "human_review_required": state in {"active", "stale_stop", "unknown_stop"},
        "blocked_reason": reason,
        "active_lock_path": str(path),
        "lock_id": _sanitize_message(lock.get("lock_id")),
        "partial_files": [],
        "lock": {key: value for key, value in lock.items() if key != "owner_token_hash"},
    }


def _append_lock_journal(event: dict[str, Any], now: datetime | None = None) -> dict[str, Any]:
    path = _lock_journal_path(now)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, ensure_ascii=True, separators=(",", ":")) + "\n")
        return {
            "attempted": True,
            "success": True,
            "path": str(path),
            "path_masked": path.name,
            "error_name": None,
        }
    except Exception as exc:
        return {
            "attempted": True,
            "success": False,
            "path": str(path),
            "path_masked": path.name,
            "error_name": _sanitize_message(exc.__class__.__name__) or "LOCK_JOURNAL_APPEND_FAILED",
        }


def _atomic_write_json(path: Path, payload: dict[str, Any]) -> dict[str, Any]:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = path.with_name(f"{path.name}.tmp.{uuid.uuid4().hex}")
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
        fd = os.open(str(temp_path), flags, 0o600)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(payload, handle, ensure_ascii=True, separators=(",", ":"))
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
        except Exception:
            try:
                os.close(fd)
            except OSError:
                pass
            raise
        os.replace(temp_path, path)
        readback, error_name = _read_json_file(path)
        if readback is None:
            return {"success": False, "error_name": error_name or "LOCK_WRITE_READBACK_FAILED"}
        return {"success": True, "error_name": None}
    except Exception as exc:
        return {"success": False, "error_name": _sanitize_message(exc.__class__.__name__) or "LOCK_WRITE_FAILED"}


def _guarded_lock_write(path: Path, payload: dict[str, Any]) -> dict[str, Any]:
    guard_path = path.with_name(f"{path.name}.tmp.acquire")
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        guard_fd = os.open(str(guard_path), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        os.close(guard_fd)
    except FileExistsError:
        return {"success": False, "error_name": "LOCK_CONCURRENT_ACQUIRE_DETECTED"}
    except Exception as exc:
        return {"success": False, "error_name": _sanitize_message(exc.__class__.__name__) or "LOCK_GUARD_CREATE_FAILED"}
    try:
        if path.exists():
            return {"success": False, "error_name": "ACTIVE_LOCK_EXISTS"}
        return _atomic_write_json(path, payload)
    finally:
        try:
            guard_path.unlink()
        except FileNotFoundError:
            pass


def _remove_active_lock(path: Path) -> dict[str, Any]:
    released_path = path.with_name(f"{path.stem}.released.{datetime.now(timezone(timedelta(hours=9))).strftime('%Y%m%d_%H%M%S')}{path.suffix}")
    try:
        os.replace(path, released_path)
        return {"success": True, "released_path": str(released_path), "error_name": None}
    except Exception as exc:
        return {"success": False, "released_path": None, "error_name": _sanitize_message(exc.__class__.__name__) or "LOCK_RELEASE_RENAME_FAILED"}


def _lock_gate_failures(payload: ExecutionLockAcquireRequest) -> list[str]:
    failures: list[str] = []
    if not _strict_true(payload.human_approval):
        failures.append("HUMAN_APPROVAL_REQUIRED")
    if not _strict_false(payload.open_order_exists):
        failures.append("OPEN_ORDER_EXISTS_OR_UNKNOWN")
    if _safe_int(payload.open_order_count, default=-1, minimum=-1, maximum=1000000) != 0:
        failures.append("OPEN_ORDER_COUNT_NOT_ZERO")
    if not _strict_false(payload.duplicate_order_exists):
        failures.append("DUPLICATE_ORDER_EXISTS_OR_UNKNOWN")
    if str(payload.reconciliation_classification or "") not in {"done", "cancel"}:
        failures.append("RECONCILIATION_NOT_FINAL")
    if not _strict_false(payload.workflow_active):
        failures.append("WORKFLOW_ACTIVE_OR_UNKNOWN")
    if not _strict_false(payload.cron_enabled):
        failures.append("CRON_ENABLED_OR_UNKNOWN")
    if str(payload.fuse_state or "") in {"", "unknown", "ambiguous", "consumed"}:
        failures.append("FUSE_STATE_BLOCKED_OR_UNKNOWN")
    if not _strict_true(payload.order_journal_evidence):
        failures.append("ORDER_JOURNAL_EVIDENCE_REQUIRED")
    if not payload.owner_token:
        failures.append("OWNER_TOKEN_REQUIRED")
    return failures


def _release_gate_failures(payload: ExecutionLockReleaseRequest, lock: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    if not _strict_true(payload.human_approval):
        failures.append("HUMAN_RELEASE_APPROVAL_REQUIRED")
    if str(payload.lock_id or "") != str(lock.get("lock_id") or ""):
        failures.append("LOCK_ID_MISMATCH")
    if _owner_token_hash(payload.owner_token) != lock.get("owner_token_hash"):
        failures.append("OWNER_TOKEN_MISMATCH")
    if not _strict_false(payload.open_order_exists):
        failures.append("OPEN_ORDER_EXISTS_OR_UNKNOWN")
    if _safe_int(payload.open_order_count, default=-1, minimum=-1, maximum=1000000) != 0:
        failures.append("OPEN_ORDER_COUNT_NOT_ZERO")
    if str(payload.reconciliation_classification or "") not in {"done", "cancel"} and str(payload.release_reason or "") != "approved_abort_before_execution":
        failures.append("RECONCILIATION_NOT_FINAL")
    if not _strict_false(payload.workflow_active):
        failures.append("WORKFLOW_ACTIVE_OR_UNKNOWN")
    if not _strict_false(payload.cron_enabled):
        failures.append("CRON_ENABLED_OR_UNKNOWN")
    if not payload.release_reason:
        failures.append("RELEASE_REASON_REQUIRED")
    return failures


def _stale_lock_recovery_blocked(
    payload: ExecutionLockRecoverStaleFinalityRequest,
    status: dict[str, Any],
    lock: dict[str, Any],
) -> list[str]:
    failures: list[str] = []
    if not _strict_true(payload.automated_recovery_allowed):
        failures.append("AUTOMATED_RECOVERY_ALLOWED_REQUIRED")
    if not payload.recovery_reason:
        failures.append("RECOVERY_REASON_REQUIRED")
    if not _strict_false(payload.workflow_active):
        failures.append("WORKFLOW_ACTIVE_OR_UNKNOWN")
    if not _strict_false(payload.cron_enabled):
        failures.append("CRON_ENABLED_OR_UNKNOWN")
    if status.get("lock_state") != "stale_stop" or status.get("stale_lock") is not True:
        failures.append("LOCK_NOT_STALE")
    if status.get("partial_files"):
        failures.append("LOCK_PARTIAL_WRITE_PRESENT")
    if str(lock.get("lock_state") or "") != "active":
        failures.append("LOCK_STATE_NOT_ACTIVE")
    if str(lock.get("market") or "") not in LIVE_SELL_ALLOWED_MARKETS | LIVE_BUY_ALLOWED_MARKETS:
        failures.append("LOCK_MARKET_UNSUPPORTED")
    if str(lock.get("side") or "") not in {"ask", "bid"}:
        failures.append("LOCK_SIDE_UNSUPPORTED")
    if str(lock.get("ord_type") or "") != "limit":
        failures.append("LOCK_LIMIT_ONLY")
    return failures


def _stale_lock_finality_evidence(market: str, side: str, ord_type: str) -> dict[str, Any]:
    open_result = _upbit_get("/v1/orders/open", {"market": market})
    open_status = open_result["status"]
    open_body = open_result["body"]
    open_classification = _classify(open_status, open_body)
    open_orders = open_body if isinstance(open_body, list) else []
    open_success = open_classification["stop_code"] is None and isinstance(open_body, list)
    if not open_success:
        return {
            "success": False,
            "blocked_reason": open_classification["error_name"] or "OPEN_ORDER_TELEMETRY_FAILED",
            "open_order_count": None,
            "open_order_exists": None,
            "final_classification": "unknown_stop",
            "order": None,
        }
    if len(open_orders) > 0:
        return {
            "success": False,
            "blocked_reason": "OPEN_ORDER_EXISTS",
            "open_order_count": len(open_orders),
            "open_order_exists": True,
            "final_classification": "wait",
            "order": None,
        }

    closed_result = _upbit_get(
        "/v1/orders/closed",
        {"market": market, "limit": "10", "order_by": "desc"},
    )
    closed_body = closed_result["body"]
    closed_orders = closed_body if isinstance(closed_body, list) else []
    sanitized_orders = [_sanitize_detail_order(row) for row in closed_orders if isinstance(row, dict)]
    matching = [
        order
        for order in sanitized_orders
        if order.get("market") == market and order.get("side") == side and order.get("ord_type") == ord_type
    ]
    selected = matching[:1]
    final_classification, blocked_reason = _final_detail_classification(selected, True, None)
    if final_classification not in {"done", "cancel"}:
        return {
            "success": False,
            "blocked_reason": blocked_reason or "STALE_LOCK_RECENT_ORDER_NOT_FINAL",
            "open_order_count": 0,
            "open_order_exists": False,
            "final_classification": final_classification,
            "order": selected[0] if selected else None,
        }
    return {
        "success": True,
        "blocked_reason": None,
        "open_order_count": 0,
        "open_order_exists": False,
        "final_classification": final_classification,
        "order": selected[0] if selected else None,
    }


def _credentials() -> tuple[str | None, str | None]:
    return os.getenv("UPBIT_ACCESS_KEY"), os.getenv("UPBIT_SECRET_KEY")


def _create_jwt(query_string: str = "") -> str | None:
    access_key, secret_key = _credentials()
    if not access_key or not secret_key:
        return None

    payload: dict[str, Any] = {
        "access_key": access_key,
        "nonce": str(uuid.uuid4()),
    }
    if query_string:
        payload["query_hash"] = hashlib.sha512(query_string.encode("utf-8")).hexdigest()
        payload["query_hash_alg"] = "SHA512"

    signing_input = f"{_json_b64({'alg': 'HS512', 'typ': 'JWT'})}.{_json_b64(payload)}"
    signature = hmac.new(
        secret_key.encode("utf-8"),
        signing_input.encode("utf-8"),
        hashlib.sha512,
    ).digest()
    return f"{signing_input}.{_base64url(signature)}"


def _classify(status: int | None, body: Any) -> dict[str, str | None]:
    error_object = body.get("error") if isinstance(body, dict) else None
    if status in (418, 429):
        return {
            "stop_code": "RATE_LIMITED",
            "error_name": _sanitize_message((error_object or {}).get("name") or "RATE_LIMITED"),
            "error_message": "RATE_LIMITED",
        }
    if status in (401, 403):
        return {
            "stop_code": "AUTH_FAILED",
            "error_name": _sanitize_message((error_object or {}).get("name") or "AUTH_FAILED"),
            "error_message": "AUTH_FAILED",
        }
    if status is None or status < 200 or status >= 300:
        return {
            "stop_code": "AUTH_FAILED",
            "error_name": _sanitize_message((error_object or {}).get("name") or "UNEXPECTED_RESPONSE"),
            "error_message": _sanitize_message((error_object or {}).get("message") or "UNEXPECTED_RESPONSE"),
        }
    return {
        "stop_code": None,
        "error_name": _sanitize_message((error_object or {}).get("name")),
        "error_message": _sanitize_message((error_object or {}).get("message")),
    }


def _upbit_get(path: str, query: dict[str, str] | None = None) -> dict[str, Any]:
    query_string = parse.urlencode(query or {})
    jwt = _create_jwt(query_string)
    if jwt is None:
        return {
            "status": None,
            "remaining_req": None,
            "body": {"error": {"name": "CREDENTIAL_MISSING", "message": "CREDENTIAL_MISSING"}},
        }

    endpoint = f"{UPBIT_BASE_URL}{path}"
    if query_string:
        endpoint = f"{endpoint}?{query_string}"

    req = request.Request(endpoint, method="GET", headers={"Authorization": f"Bearer {jwt}"})
    try:
        with request.urlopen(req, timeout=10) as response:
            raw_body = response.read().decode("utf-8", errors="replace")
            body = json.loads(raw_body) if raw_body else None
            return {
                "status": response.status,
                "remaining_req": response.headers.get("Remaining-Req"),
                "body": body,
            }
    except error.HTTPError as exc:
        raw_body = exc.read().decode("utf-8", errors="replace")
        try:
            body = json.loads(raw_body) if raw_body else None
        except json.JSONDecodeError:
            body = {"error": {"name": "HTTP_ERROR", "message": "HTTP_ERROR"}}
        return {
            "status": exc.code,
            "remaining_req": exc.headers.get("Remaining-Req"),
            "body": body,
        }
    except Exception as exc:
        return {
            "status": None,
            "remaining_req": None,
            "body": {"error": {"name": exc.__class__.__name__, "message": str(exc)}},
        }


def _upbit_public_get(path: str, query: dict[str, str] | None = None) -> dict[str, Any]:
    query_string = parse.urlencode(query or {})
    endpoint = f"{UPBIT_BASE_URL}{path}"
    if query_string:
        endpoint = f"{endpoint}?{query_string}"

    req = request.Request(endpoint, method="GET")
    try:
        with request.urlopen(req, timeout=10) as response:
            raw_body = response.read().decode("utf-8", errors="replace")
            body = json.loads(raw_body) if raw_body else None
            return {
                "status": response.status,
                "remaining_req": response.headers.get("Remaining-Req"),
                "body": body,
            }
    except error.HTTPError as exc:
        raw_body = exc.read().decode("utf-8", errors="replace")
        try:
            body = json.loads(raw_body) if raw_body else None
        except json.JSONDecodeError:
            body = {"error": {"name": "HTTP_ERROR", "message": "HTTP_ERROR"}}
        return {
            "status": exc.code,
            "remaining_req": exc.headers.get("Remaining-Req"),
            "body": body,
        }
    except Exception as exc:
        return {
            "status": None,
            "remaining_req": None,
            "body": {"error": {"name": exc.__class__.__name__, "message": str(exc)}},
        }


def _upbit_post(path: str, payload: dict[str, str]) -> dict[str, Any]:
    query_string = parse.urlencode(payload)
    jwt = _create_jwt(query_string)
    if jwt is None:
        return {
            "status": None,
            "remaining_req": None,
            "body": {"error": {"name": "CREDENTIAL_MISSING", "message": "CREDENTIAL_MISSING"}},
        }

    data = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    req = request.Request(
        f"{UPBIT_BASE_URL}{path}",
        method="POST",
        data=data,
        headers={
            "Authorization": f"Bearer {jwt}",
            "Content-Type": "application/json",
        },
    )
    try:
        with request.urlopen(req, timeout=10) as response:
            raw_body = response.read().decode("utf-8", errors="replace")
            body = json.loads(raw_body) if raw_body else None
            return {
                "status": response.status,
                "remaining_req": response.headers.get("Remaining-Req"),
                "body": body,
            }
    except error.HTTPError as exc:
        raw_body = exc.read().decode("utf-8", errors="replace")
        try:
            body = json.loads(raw_body) if raw_body else None
        except json.JSONDecodeError:
            body = {"error": {"name": "HTTP_ERROR", "message": "HTTP_ERROR"}}
        return {
            "status": exc.code,
            "remaining_req": exc.headers.get("Remaining-Req"),
            "body": body,
        }
    except Exception as exc:
        return {
            "status": None,
            "remaining_req": None,
            "body": {"error": {"name": exc.__class__.__name__, "message": str(exc)}},
        }


def _upbit_delete(path: str, query: dict[str, str]) -> dict[str, Any]:
    query_string = parse.urlencode(query)
    jwt = _create_jwt(query_string)
    if jwt is None:
        return {
            "status": None,
            "remaining_req": None,
            "body": {"error": {"name": "CREDENTIAL_MISSING", "message": "CREDENTIAL_MISSING"}},
        }

    endpoint = f"{UPBIT_BASE_URL}{path}"
    if query_string:
        endpoint = f"{endpoint}?{query_string}"
    req = request.Request(endpoint, method="DELETE", headers={"Authorization": f"Bearer {jwt}"})
    try:
        with request.urlopen(req, timeout=10) as response:
            raw_body = response.read().decode("utf-8", errors="replace")
            body = json.loads(raw_body) if raw_body else None
            return {
                "status": response.status,
                "remaining_req": response.headers.get("Remaining-Req"),
                "body": body,
            }
    except error.HTTPError as exc:
        raw_body = exc.read().decode("utf-8", errors="replace")
        try:
            body = json.loads(raw_body) if raw_body else None
        except json.JSONDecodeError:
            body = {"error": {"name": "HTTP_ERROR", "message": "HTTP_ERROR"}}
        return {
            "status": exc.code,
            "remaining_req": exc.headers.get("Remaining-Req"),
            "body": body,
        }
    except Exception as exc:
        return {
            "status": None,
            "remaining_req": None,
            "body": {"error": {"name": exc.__class__.__name__, "message": str(exc)}},
        }


@app.get("/health")
def health() -> dict[str, bool | str]:
    return {"ok": True, "service": SERVICE_NAME}


@app.post("/execution-lock/status")
def execution_lock_status(payload: ExecutionLockStatusRequest | None = None) -> dict[str, Any]:
    status = _execution_lock_status(payload.now_kst if payload else None)
    return {
        "success": status["success"],
        "mode": "execution_lock_status_only",
        "lock_state": status["lock_state"],
        "lock_exists": status["lock_exists"],
        "stale_lock": status["stale_lock"],
        "human_review_required": status["human_review_required"],
        "blocked_reason": status["blocked_reason"],
        "active_lock_path": status["active_lock_path"],
        "lock_id": status["lock_id"],
        "partial_files": status["partial_files"],
        "forbidden_endpoint_check": True,
        "secrets_leak_check": True,
        "next_safe_action": "remain_stopped",
    }


@app.post("/execution-lock/acquire")
def execution_lock_acquire(payload: ExecutionLockAcquireRequest) -> dict[str, Any]:
    now = _lock_now(payload.now_kst)
    status = _execution_lock_status(payload.now_kst)
    path = _active_lock_path()

    def blocked(reason: str, extra: dict[str, Any] | None = None) -> dict[str, Any]:
        event = {
            "timestamp_kst": now.isoformat(timespec="seconds"),
            "event_type": "lock_acquire_attempt",
            "result": "blocked",
            "lock_id": None,
            "market": _sanitize_message(payload.market),
            "side": _sanitize_message(payload.side),
            "ord_type": _sanitize_message(payload.ord_type),
            "run_id": _sanitize_message(payload.run_id),
            "approval_id": _sanitize_message(payload.approval_id),
            "fuse_state": _sanitize_message(payload.fuse_state),
            "open_order_exists": _strict_true(payload.open_order_exists),
            "open_order_count": _safe_int(payload.open_order_count, default=-1, minimum=-1, maximum=1000000),
            "reconciliation_classification": _sanitize_message(payload.reconciliation_classification),
            "blocked_reason": reason,
            "next_safe_action": "remain_stopped",
            "forbidden_endpoint_check": True,
            "secrets_leak_check": True,
        }
        journal = _append_lock_journal(event, now)
        response = {
            "success": False,
            "mode": "execution_lock_acquire_only",
            "lock_acquired": False,
            "lock_id": None,
            "lock_state": "blocked",
            "blocked_reason": reason,
            "human_review_required": reason in {"STALE_LOCK_EXISTS", "LOCK_STATUS_UNCLEAR", "LOCK_PARTIAL_WRITE_PRESENT"},
            "journal_write": journal,
            "active_lock_path": str(path),
            "forbidden_endpoint_check": True,
            "secrets_leak_check": True,
            "next_safe_action": "remain_stopped",
        }
        if extra:
            response.update(extra)
        return response

    if status["lock_state"] != "unlocked":
        reason = status["blocked_reason"] or "LOCK_STATUS_UNCLEAR"
        return blocked(reason, {"current_lock_state": status["lock_state"]})

    failures = _lock_gate_failures(payload)
    if failures:
        return blocked("|".join(failures))

    lock_id = f"lock-{uuid.uuid4().hex}"
    expires_at = _parse_kst(payload.expires_at_kst) or (now + timedelta(minutes=10))
    lock_payload = {
        "schema_version": LOCK_SCHEMA_VERSION,
        "lock_id": lock_id,
        "created_at_kst": now.isoformat(timespec="seconds"),
        "updated_at_kst": now.isoformat(timespec="seconds"),
        "created_by": "human_approved_runtime",
        "market": _sanitize_message(payload.market),
        "side": _sanitize_message(payload.side),
        "ord_type": _sanitize_message(payload.ord_type),
        "lock_state": "active",
        "lock_reason": _sanitize_message(payload.lock_reason) or "LIVE_EXECUTION_APPROVAL_PENDING_OR_IN_PROGRESS",
        "run_id": _sanitize_message(payload.run_id),
        "approval_id": _sanitize_message(payload.approval_id),
        "fuse_id": _sanitize_message(payload.fuse_id),
        "owner_token_hash": _owner_token_hash(payload.owner_token),
        "journal_ref": "execution_lock_journal",
        "open_order_exists_at_acquire": False,
        "open_order_count_at_acquire": 0,
        "reconciliation_classification_at_acquire": _sanitize_message(payload.reconciliation_classification),
        "workflow_active_at_acquire": False,
        "cron_enabled_at_acquire": False,
        "expires_at_kst": expires_at.isoformat(timespec="seconds"),
        "release_required_by_human": True,
        "forbidden_endpoint_check": True,
        "secrets_leak_check": True,
    }
    validation_error = _validate_lock_payload(lock_payload)
    if validation_error:
        return blocked(validation_error)

    attempt_journal = _append_lock_journal(
        {
            "timestamp_kst": now.isoformat(timespec="seconds"),
            "event_type": "lock_acquire_attempt",
            "result": "attempting",
            "lock_id": lock_id,
            "market": lock_payload["market"],
            "side": lock_payload["side"],
            "ord_type": lock_payload["ord_type"],
            "run_id": lock_payload["run_id"],
            "approval_id": lock_payload["approval_id"],
            "fuse_state": _sanitize_message(payload.fuse_state),
            "open_order_exists": False,
            "open_order_count": 0,
            "reconciliation_classification": lock_payload["reconciliation_classification_at_acquire"],
            "blocked_reason": None,
            "next_safe_action": "remain_stopped",
            "forbidden_endpoint_check": True,
            "secrets_leak_check": True,
        },
        now,
    )
    if not attempt_journal["success"]:
        return blocked(attempt_journal["error_name"] or "LOCK_JOURNAL_APPEND_FAILED")

    write_result = _guarded_lock_write(path, lock_payload)
    if not write_result["success"]:
        return blocked(write_result["error_name"] or "LOCK_WRITE_FAILED")

    acquired_journal = _append_lock_journal(
        {
            "timestamp_kst": now.isoformat(timespec="seconds"),
            "event_type": "lock_acquired",
            "result": "acquired",
            "lock_id": lock_id,
            "market": lock_payload["market"],
            "side": lock_payload["side"],
            "ord_type": lock_payload["ord_type"],
            "run_id": lock_payload["run_id"],
            "approval_id": lock_payload["approval_id"],
            "fuse_state": _sanitize_message(payload.fuse_state),
            "open_order_exists": False,
            "open_order_count": 0,
            "reconciliation_classification": lock_payload["reconciliation_classification_at_acquire"],
            "blocked_reason": None,
            "next_safe_action": "remain_stopped",
            "forbidden_endpoint_check": True,
            "secrets_leak_check": True,
        },
        now,
    )
    if not acquired_journal["success"]:
        return {
            "success": False,
            "mode": "execution_lock_acquire_only",
            "lock_acquired": True,
            "lock_id": lock_id,
            "lock_state": "active",
            "blocked_reason": acquired_journal["error_name"] or "LOCK_JOURNAL_APPEND_FAILED_AFTER_ACQUIRE",
            "human_review_required": True,
            "journal_write": acquired_journal,
            "active_lock_path": str(path),
            "forbidden_endpoint_check": True,
            "secrets_leak_check": True,
            "next_safe_action": "remain_stopped",
        }

    return {
        "success": True,
        "mode": "execution_lock_acquire_only",
        "lock_acquired": True,
        "lock_id": lock_id,
        "lock_state": "active",
        "blocked_reason": None,
        "human_review_required": False,
        "journal_write": acquired_journal,
        "active_lock_path": str(path),
        "forbidden_endpoint_check": True,
        "secrets_leak_check": True,
        "next_safe_action": "remain_stopped",
    }


@app.post("/execution-lock/release")
def execution_lock_release(payload: ExecutionLockReleaseRequest) -> dict[str, Any]:
    now = _lock_now(payload.now_kst)
    path = _active_lock_path()
    status = _execution_lock_status(payload.now_kst)
    if status["lock_state"] not in {"active", "stale_stop"}:
        journal = _append_lock_journal(
            {
                "timestamp_kst": now.isoformat(timespec="seconds"),
                "event_type": "lock_release_attempt",
                "result": "blocked",
                "lock_id": _sanitize_message(payload.lock_id),
                "market": None,
                "side": None,
                "ord_type": None,
                "run_id": None,
                "approval_id": None,
                "fuse_state": _sanitize_message(payload.fuse_state),
                "open_order_exists": _strict_true(payload.open_order_exists),
                "open_order_count": _safe_int(payload.open_order_count, default=-1, minimum=-1, maximum=1000000),
                "reconciliation_classification": _sanitize_message(payload.reconciliation_classification),
                "blocked_reason": status["blocked_reason"] or "NO_ACTIVE_LOCK_TO_RELEASE",
                "next_safe_action": "remain_stopped",
                "forbidden_endpoint_check": True,
                "secrets_leak_check": True,
            },
            now,
        )
        return {
            "success": False,
            "mode": "execution_lock_release_only",
            "lock_released": False,
            "lock_id": _sanitize_message(payload.lock_id),
            "lock_state": status["lock_state"],
            "blocked_reason": status["blocked_reason"] or "NO_ACTIVE_LOCK_TO_RELEASE",
            "human_review_required": True,
            "journal_write": journal,
            "active_lock_path": str(path),
            "forbidden_endpoint_check": True,
            "secrets_leak_check": True,
            "next_safe_action": "remain_stopped",
        }

    lock = (status.get("lock") or {}).copy()
    lock_with_hash, read_error = _read_json_file(path)
    if lock_with_hash is None:
        return {
            "success": False,
            "mode": "execution_lock_release_only",
            "lock_released": False,
            "lock_id": _sanitize_message(payload.lock_id),
            "lock_state": "unknown_stop",
            "blocked_reason": read_error,
            "human_review_required": True,
            "journal_write": {"attempted": False, "success": None, "path_masked": None, "error_name": None},
            "active_lock_path": str(path),
            "forbidden_endpoint_check": True,
            "secrets_leak_check": True,
            "next_safe_action": "remain_stopped",
        }
    failures = _release_gate_failures(payload, lock_with_hash)
    if failures:
        journal = _append_lock_journal(
            {
                "timestamp_kst": now.isoformat(timespec="seconds"),
                "event_type": "lock_release_attempt",
                "result": "blocked",
                "lock_id": _sanitize_message(payload.lock_id),
                "market": lock.get("market"),
                "side": lock.get("side"),
                "ord_type": lock.get("ord_type"),
                "run_id": lock.get("run_id"),
                "approval_id": lock.get("approval_id"),
                "fuse_state": _sanitize_message(payload.fuse_state),
                "open_order_exists": _strict_true(payload.open_order_exists),
                "open_order_count": _safe_int(payload.open_order_count, default=-1, minimum=-1, maximum=1000000),
                "reconciliation_classification": _sanitize_message(payload.reconciliation_classification),
                "blocked_reason": "|".join(failures),
                "next_safe_action": "remain_stopped",
                "forbidden_endpoint_check": True,
                "secrets_leak_check": True,
            },
            now,
        )
        return {
            "success": False,
            "mode": "execution_lock_release_only",
            "lock_released": False,
            "lock_id": _sanitize_message(payload.lock_id),
            "lock_state": status["lock_state"],
            "blocked_reason": "|".join(failures),
            "human_review_required": True,
            "journal_write": journal,
            "active_lock_path": str(path),
            "forbidden_endpoint_check": True,
            "secrets_leak_check": True,
            "next_safe_action": "remain_stopped",
        }

    journal = _append_lock_journal(
        {
            "timestamp_kst": now.isoformat(timespec="seconds"),
            "event_type": "lock_release",
            "result": "released",
            "lock_id": lock.get("lock_id"),
            "market": lock.get("market"),
            "side": lock.get("side"),
            "ord_type": lock.get("ord_type"),
            "run_id": lock.get("run_id"),
            "approval_id": lock.get("approval_id"),
            "fuse_state": _sanitize_message(payload.fuse_state),
            "open_order_exists": False,
            "open_order_count": 0,
            "reconciliation_classification": _sanitize_message(payload.reconciliation_classification),
            "blocked_reason": None,
            "next_safe_action": "remain_stopped",
            "forbidden_endpoint_check": True,
            "secrets_leak_check": True,
        },
        now,
    )
    if not journal["success"]:
        return {
            "success": False,
            "mode": "execution_lock_release_only",
            "lock_released": False,
            "lock_id": lock.get("lock_id"),
            "lock_state": status["lock_state"],
            "blocked_reason": journal["error_name"] or "LOCK_JOURNAL_APPEND_FAILED",
            "human_review_required": True,
            "journal_write": journal,
            "active_lock_path": str(path),
            "forbidden_endpoint_check": True,
            "secrets_leak_check": True,
            "next_safe_action": "remain_stopped",
        }

    release_result = _remove_active_lock(path)
    return {
        "success": release_result["success"],
        "mode": "execution_lock_release_only",
        "lock_released": release_result["success"],
        "lock_id": lock.get("lock_id"),
        "lock_state": "released" if release_result["success"] else status["lock_state"],
        "blocked_reason": None if release_result["success"] else release_result["error_name"],
        "human_review_required": not release_result["success"],
        "journal_write": journal,
        "released_path": release_result["released_path"],
        "active_lock_path": str(path),
        "forbidden_endpoint_check": True,
        "secrets_leak_check": True,
        "next_safe_action": "remain_stopped",
    }


@app.post("/execution-lock/recover-stale-finality")
def execution_lock_recover_stale_finality(payload: ExecutionLockRecoverStaleFinalityRequest) -> dict[str, Any]:
    now = _lock_now(payload.now_kst)
    path = _active_lock_path()
    status = _execution_lock_status(payload.now_kst)
    lock = (status.get("lock") or {}).copy()
    lock_with_hash, read_error = _read_json_file(path)
    if lock_with_hash is None:
        journal = _append_lock_journal(
            {
                "timestamp_kst": now.isoformat(timespec="seconds"),
                "event_type": "lock_stale_recovery_attempt",
                "result": "blocked",
                "lock_id": None,
                "market": None,
                "side": None,
                "ord_type": None,
                "run_id": None,
                "approval_id": None,
                "open_order_exists": None,
                "open_order_count": None,
                "reconciliation_classification": "unknown_stop",
                "blocked_reason": read_error or status.get("blocked_reason") or "NO_LOCK_TO_RECOVER",
                "next_safe_action": "remain_stopped",
                "forbidden_endpoint_check": True,
                "secrets_leak_check": True,
            },
            now,
        )
        return {
            "success": False,
            "mode": "execution_lock_stale_finality_recovery",
            "lock_recovered": False,
            "lock_id": None,
            "market": None,
            "lock_state": status["lock_state"],
            "blocked_reason": read_error or status.get("blocked_reason") or "NO_LOCK_TO_RECOVER",
            "human_review_required": True,
            "journal_write": journal,
            "active_lock_path": str(path),
            "forbidden_endpoint_check": True,
            "secrets_leak_check": True,
            "next_safe_action": "remain_stopped",
        }

    failures = _stale_lock_recovery_blocked(payload, status, lock_with_hash)
    market = str(lock_with_hash.get("market") or "")
    side = str(lock_with_hash.get("side") or "")
    ord_type = str(lock_with_hash.get("ord_type") or "")
    evidence = None
    if not failures:
        evidence = _stale_lock_finality_evidence(market, side, ord_type)
        if not evidence.get("success"):
            failures.append(str(evidence.get("blocked_reason") or "STALE_LOCK_FINALITY_NOT_PROVEN"))

    if failures:
        journal = _append_lock_journal(
            {
                "timestamp_kst": now.isoformat(timespec="seconds"),
                "event_type": "lock_stale_recovery_attempt",
                "result": "blocked",
                "lock_id": _sanitize_message(lock_with_hash.get("lock_id")),
                "market": market,
                "side": side,
                "ord_type": ord_type,
                "run_id": _sanitize_message(lock_with_hash.get("run_id")),
                "approval_id": _sanitize_message(lock_with_hash.get("approval_id")),
                "open_order_exists": evidence.get("open_order_exists") if evidence else None,
                "open_order_count": evidence.get("open_order_count") if evidence else None,
                "reconciliation_classification": evidence.get("final_classification") if evidence else "unknown_stop",
                "blocked_reason": "|".join(failures),
                "next_safe_action": "remain_stopped",
                "forbidden_endpoint_check": True,
                "secrets_leak_check": True,
            },
            now,
        )
        return {
            "success": False,
            "mode": "execution_lock_stale_finality_recovery",
            "lock_recovered": False,
            "lock_id": _sanitize_message(lock_with_hash.get("lock_id")),
            "market": market,
            "lock_state": status["lock_state"],
            "blocked_reason": "|".join(failures),
            "human_review_required": True,
            "journal_write": journal,
            "open_order_count": evidence.get("open_order_count") if evidence else None,
            "final_classification": evidence.get("final_classification") if evidence else "unknown_stop",
            "active_lock_path": str(path),
            "forbidden_endpoint_check": True,
            "secrets_leak_check": True,
            "next_safe_action": "remain_stopped",
        }

    order = (evidence or {}).get("order") or {}
    journal = _append_lock_journal(
        {
            "timestamp_kst": now.isoformat(timespec="seconds"),
            "event_type": "lock_stale_recovery",
            "result": "released",
            "lock_id": _sanitize_message(lock_with_hash.get("lock_id")),
            "market": market,
            "side": side,
            "ord_type": ord_type,
            "run_id": _sanitize_message(lock_with_hash.get("run_id")),
            "approval_id": _sanitize_message(lock_with_hash.get("approval_id")),
            "open_order_exists": False,
            "open_order_count": 0,
            "reconciliation_classification": evidence["final_classification"],
            "blocked_reason": None,
            "next_safe_action": "remain_stopped",
            "forbidden_endpoint_check": True,
            "secrets_leak_check": True,
        },
        now,
    )
    if not journal["success"]:
        return {
            "success": False,
            "mode": "execution_lock_stale_finality_recovery",
            "lock_recovered": False,
            "lock_id": _sanitize_message(lock_with_hash.get("lock_id")),
            "market": market,
            "lock_state": status["lock_state"],
            "blocked_reason": journal["error_name"] or "LOCK_JOURNAL_APPEND_FAILED",
            "human_review_required": True,
            "journal_write": journal,
            "open_order_count": 0,
            "final_classification": evidence["final_classification"],
            "active_lock_path": str(path),
            "forbidden_endpoint_check": True,
            "secrets_leak_check": True,
            "next_safe_action": "remain_stopped",
        }

    release_result = _remove_active_lock(path)
    return {
        "success": release_result["success"],
        "mode": "execution_lock_stale_finality_recovery",
        "lock_recovered": release_result["success"],
        "lock_id": _sanitize_message(lock_with_hash.get("lock_id")),
        "market": market,
        "side": side,
        "ord_type": ord_type,
        "lock_state": "released" if release_result["success"] else status["lock_state"],
        "blocked_reason": None if release_result["success"] else release_result["error_name"],
        "human_review_required": not release_result["success"],
        "journal_write": journal,
        "released_path": release_result["released_path"],
        "open_order_count": 0,
        "open_order_exists": False,
        "final_classification": evidence["final_classification"],
        "order_state": order.get("state"),
        "executed_volume": order.get("executed_volume"),
        "remaining_volume": order.get("remaining_volume"),
        "uuid_masked": order.get("uuid_masked"),
        "active_lock_path": str(path),
        "forbidden_endpoint_check": True,
        "secrets_leak_check": True,
        "next_safe_action": "remain_stopped",
    }


@app.post("/upbit/accounts/telemetry")
def accounts_telemetry(payload: AccountsTelemetryRequest | None = None) -> dict[str, Any]:
    result = _upbit_get("/v1/accounts")
    status = result["status"]
    body = result["body"]
    classification = _classify(status, body)
    accounts = body if isinstance(body, list) else []
    success = classification["stop_code"] is None and isinstance(body, list)
    requested_krw = _decimal_or_none(payload.estimated_krw_value if payload else None)
    krw_available = None
    for row in accounts:
        if isinstance(row, dict) and str(row.get("currency")) == "KRW":
            krw_available = _decimal_or_none(row.get("balance"))
            break
    krw_balance_sufficient = None
    if success and requested_krw is not None and krw_available is not None:
        krw_balance_sufficient = krw_available >= requested_krw

    return {
        "http_status": status,
        "success": success,
        "account_count": len(accounts),
        "currencies_present": sorted({str(row.get("currency")) for row in accounts if isinstance(row, dict) and row.get("currency")}),
        "krw_balance_sufficient": krw_balance_sufficient,
        "krw_available_band": _krw_band(krw_available) if success else None,
        "remaining_req": result["remaining_req"],
        "error_name": classification["error_name"],
        "error_message": classification["error_message"],
    }


@app.post("/upbit/open-orders/telemetry")
def open_orders_telemetry(payload: OpenOrdersRequest) -> dict[str, Any]:
    market = str(payload.market or "KRW-BTC")
    result = _upbit_get("/v1/orders/open", {"market": market})
    status = result["status"]
    body = result["body"]
    classification = _classify(status, body)
    open_orders = body if isinstance(body, list) else []
    success = classification["stop_code"] is None and isinstance(body, list)

    return {
        "http_status": status,
        "success": success,
        "market": market,
        "open_order_count": len(open_orders),
        "open_order_exists": len(open_orders) > 0,
        "remaining_req": result["remaining_req"],
        "error_name": classification["error_name"],
        "error_message": classification["error_message"],
    }


def _open_orders_detail_telemetry(
    payload: DetailTelemetryRequest,
    endpoint_path: str,
    journal_enabled: bool,
) -> dict[str, Any]:
    market = str(payload.market or "KRW-BTC")
    timestamp_kst = _kst_now()
    open_result = _upbit_get("/v1/orders/open", {"market": market})
    open_status = open_result["status"]
    open_body = open_result["body"]
    open_classification = _classify(open_status, open_body)
    open_orders_raw = open_body if isinstance(open_body, list) else []
    open_success = open_classification["stop_code"] is None and isinstance(open_body, list)

    recent_closed_orders_raw: list[Any] = []
    if open_success and not open_orders_raw and payload.include_recent_closed:
        closed_limit = _safe_int(payload.recent_closed_limit, default=20, minimum=1, maximum=50)
        closed_result = _upbit_get(
            "/v1/orders/closed",
            {"market": market, "limit": str(closed_limit), "order_by": "desc"},
        )
        closed_body = closed_result["body"]
        if isinstance(closed_body, list):
            recent_closed_orders_raw = closed_body

    selected_orders_raw = open_orders_raw if open_orders_raw else recent_closed_orders_raw[:1]
    sanitized_orders = [_sanitize_detail_order(row) for row in selected_orders_raw if isinstance(row, dict)]
    duplicate_order_exists = len(open_orders_raw) > 1
    new_order_created_detected = duplicate_order_exists
    final_classification, blocked_reason = _final_detail_classification(
        sanitized_orders if selected_orders_raw else [],
        open_success,
        open_classification["error_name"],
    )

    response_success = open_success
    if blocked_reason is not None and final_classification == "unknown_stop":
        response_success = False

    response: dict[str, Any] = {
        "success": response_success,
        "endpoint": endpoint_path,
        "mode": "read_only_detail_telemetry",
        "market": market,
        "open_order_exists": len(open_orders_raw) > 0,
        "open_order_count": len(open_orders_raw),
        "duplicate_order_exists": duplicate_order_exists,
        "new_order_created_detected": new_order_created_detected,
        "orders": sanitized_orders,
        "classification_summary": {
            "final_classification": final_classification,
            "blocked_reason": blocked_reason,
            "next_safe_action": "remain_stopped",
        },
        "journal_write": {
            "attempted": False,
            "success": None,
            "path_masked": None,
            "error_name": None,
        },
        "forbidden_endpoint_check": True,
        "secrets_leak_check": True,
        "remaining_req": open_result["remaining_req"],
        "error_name": open_classification["error_name"],
        "error_message": open_classification["error_message"],
    }

    if journal_enabled:
        journal_event = {
            "timestamp_kst": timestamp_kst,
            "run_id": _sanitize_message(payload.run_id),
            "source": SERVICE_NAME,
            "endpoint": endpoint_path,
            "market": market,
            "open_order_exists": response["open_order_exists"],
            "open_order_count": response["open_order_count"],
            "duplicate_order_exists": duplicate_order_exists,
            "new_order_created_detected": new_order_created_detected,
            "state": sanitized_orders[0].get("state") if sanitized_orders else None,
            "remaining_volume": sanitized_orders[0].get("remaining_volume") if sanitized_orders else None,
            "executed_volume": sanitized_orders[0].get("executed_volume") if sanitized_orders else None,
            "classification": final_classification,
            "blocked_reason": blocked_reason,
            "forbidden_endpoint_check": True,
            "secrets_leak_check": True,
            "next_safe_action": "remain_stopped",
        }
        journal_result = _append_detail_journal(journal_event)
        response["journal_write"] = journal_result
        if not journal_result["success"]:
            response["success"] = False
            response["classification_summary"] = {
                "final_classification": "unknown_stop",
                "blocked_reason": journal_result["error_name"],
                "next_safe_action": "remain_stopped",
            }
            response["error_name"] = journal_result["error_name"]
            response["error_message"] = journal_result["error_name"]

    return response


@app.post("/upbit/open-orders/detail-telemetry")
def open_orders_detail_telemetry(payload: DetailTelemetryRequest) -> dict[str, Any]:
    return _open_orders_detail_telemetry(
        payload,
        "/upbit/open-orders/detail-telemetry",
        payload.journal_enabled,
    )


@app.post("/upbit/open-orders/detail-telemetry-no-journal")
def open_orders_detail_telemetry_no_journal(payload: DetailTelemetryRequest) -> dict[str, Any]:
    return _open_orders_detail_telemetry(
        payload,
        "/upbit/open-orders/detail-telemetry-no-journal",
        False,
    )


def _cancel_stale_order_failures(
    payload: CancelStaleOrderRequest,
    open_orders: list[Any],
    lock_status: dict[str, Any],
    now: datetime,
) -> tuple[list[str], dict[str, Any] | None, int | None]:
    failures: list[str] = []
    market = str(payload.market or "")
    side = str(payload.side or "")
    ord_type = str(payload.ord_type or "")
    min_age = _safe_int(
        payload.min_open_age_minutes,
        default=LIVE_CANCEL_MIN_OPEN_AGE_MINUTES,
        minimum=LIVE_CANCEL_MIN_OPEN_AGE_MINUTES,
        maximum=LIVE_CANCEL_MAX_OPEN_AGE_MINUTES,
    )

    if not _strict_true(payload.cancel_enabled):
        failures.append("CANCEL_ENABLED_REQUIRED")
    if not _strict_true(payload.execution_allowed):
        failures.append("EXECUTION_ALLOWED_REQUIRED")
    if str(payload.execution_mode or "") != "live":
        failures.append("LIVE_MODE_REQUIRED")
    if not _strict_true(payload.one_time_cancel_allowed):
        failures.append("ONE_TIME_CANCEL_REQUIRED")
    if not _strict_true(payload.human_approval):
        failures.append("HUMAN_APPROVAL_REQUIRED")
    if not _strict_false(payload.workflow_active):
        failures.append("WORKFLOW_ACTIVE_OR_UNKNOWN")
    if not _strict_false(payload.cron_enabled):
        failures.append("CRON_ENABLED_OR_UNKNOWN")
    if _strict_true(payload.system_stop_active):
        failures.append("SYSTEM_STOP_ACTIVE")
    if market not in LIVE_SELL_ALLOWED_MARKETS:
        failures.append("CANCEL_MARKET_NOT_ALLOWED")
    if side != "ask":
        failures.append("CANCEL_ASK_ONLY")
    if ord_type != "limit":
        failures.append("CANCEL_LIMIT_ONLY")
    if len(open_orders) != 1:
        failures.append("CANCEL_REQUIRES_EXACTLY_ONE_OPEN_ORDER")

    order = open_orders[0] if len(open_orders) == 1 and isinstance(open_orders[0], dict) else None
    age_minutes: int | None = None
    if order is None:
        return failures, None, age_minutes

    remaining = _decimal_or_none(order.get("remaining_volume"))
    executed = _decimal_or_none(order.get("executed_volume"))
    age_minutes = _order_age_minutes(order.get("created_at"), now)
    if order.get("uuid") in (None, ""):
        failures.append("CANCEL_UUID_MISSING")
    if str(order.get("market") or "") != market:
        failures.append("CANCEL_MARKET_MISMATCH")
    if str(order.get("side") or "") != side:
        failures.append("CANCEL_SIDE_MISMATCH")
    if str(order.get("ord_type") or "") != ord_type:
        failures.append("CANCEL_ORD_TYPE_MISMATCH")
    if str(order.get("state") or "") != "wait":
        failures.append("CANCEL_WAIT_STATE_REQUIRED")
    if executed is None or executed != 0:
        failures.append("CANCEL_ZERO_EXECUTION_REQUIRED")
    if remaining is None or remaining <= 0:
        failures.append("CANCEL_REMAINING_VOLUME_REQUIRED")
    if age_minutes is None:
        failures.append("CANCEL_CREATED_AT_REQUIRED")
    elif age_minutes < min_age:
        failures.append("CANCEL_ORDER_NOT_STALE_ENOUGH")

    lock = lock_status.get("lock") or {}
    if lock_status.get("lock_state") not in {"active", "stale_stop"}:
        failures.append("CANCEL_LOCK_ACTIVE_OR_STALE_REQUIRED")
    if str(lock.get("market") or "") != market:
        failures.append("CANCEL_LOCK_MARKET_MISMATCH")
    if str(lock.get("side") or "") != side:
        failures.append("CANCEL_LOCK_SIDE_MISMATCH")
    if str(lock.get("ord_type") or "") != ord_type:
        failures.append("CANCEL_LOCK_ORD_TYPE_MISMATCH")
    return failures, order, age_minutes


@app.post("/upbit/cancel-stale-order/telemetry")
def cancel_stale_order_telemetry(payload: CancelStaleOrderRequest) -> dict[str, Any]:
    now = _lock_now(payload.now_kst)
    market = str(payload.market or "")
    side = str(payload.side or "")
    ord_type = str(payload.ord_type or "")
    open_result = _upbit_get("/v1/orders/open", {"market": market})
    open_body = open_result["body"]
    open_classification = _classify(open_result["status"], open_body)
    open_success = open_classification["stop_code"] is None and isinstance(open_body, list)
    open_orders = open_body if isinstance(open_body, list) else []
    lock_status = _execution_lock_status(payload.now_kst)

    if not open_success:
        failures = [open_classification["error_name"] or "OPEN_ORDER_TELEMETRY_FAILED"]
        order = None
        age_minutes = None
    else:
        failures, order, age_minutes = _cancel_stale_order_failures(payload, open_orders, lock_status, now)

    response_base = {
        "mode": "cancel_stale_order_telemetry",
        "market": market,
        "side": side,
        "ord_type": ord_type,
        "open_order_count": len(open_orders),
        "open_order_exists": len(open_orders) > 0,
        "order_age_minutes": age_minutes,
        "lock_state": lock_status.get("lock_state"),
        "stale_lock": lock_status.get("stale_lock"),
        "uuid_masked": _mask_uuid(order.get("uuid")) if order else None,
        "forbidden_endpoint_check": True,
        "secrets_leak_check": True,
        "next_safe_action": "remain_stopped",
    }
    if failures:
        journal = _append_lock_journal(
            {
                "timestamp_kst": now.isoformat(timespec="seconds"),
                "event_type": "cancel_stale_order_attempt",
                "result": "blocked",
                "lock_id": _sanitize_message((lock_status.get("lock") or {}).get("lock_id")),
                "market": market,
                "side": side,
                "ord_type": ord_type,
                "run_id": _sanitize_message((lock_status.get("lock") or {}).get("run_id")),
                "approval_id": _sanitize_message((lock_status.get("lock") or {}).get("approval_id")),
                "open_order_exists": len(open_orders) > 0,
                "open_order_count": len(open_orders),
                "reconciliation_classification": "wait",
                "blocked_reason": "|".join(failures),
                "next_safe_action": "remain_stopped",
                "forbidden_endpoint_check": True,
                "secrets_leak_check": True,
            },
            now,
        )
        return {
            "success": False,
            **response_base,
            "cancel_attempted": False,
            "cancel_accepted": False,
            "blocked_reason": "|".join(failures),
            "human_review_required": True,
            "journal_write": journal,
            "remaining_req": open_result["remaining_req"],
            "error_name": "|".join(failures),
            "error_message": "|".join(failures),
        }

    cancel_result = _upbit_delete("/v1/order", {"uuid": str(order.get("uuid"))})
    cancel_classification = _classify(cancel_result["status"], cancel_result["body"])
    accepted = cancel_classification["stop_code"] is None and cancel_result["status"] in {200, 201}
    journal = _append_lock_journal(
        {
            "timestamp_kst": now.isoformat(timespec="seconds"),
            "event_type": "cancel_stale_order",
            "result": "accepted" if accepted else "rejected",
            "lock_id": _sanitize_message((lock_status.get("lock") or {}).get("lock_id")),
            "market": market,
            "side": side,
            "ord_type": ord_type,
            "run_id": _sanitize_message((lock_status.get("lock") or {}).get("run_id")),
            "approval_id": _sanitize_message((lock_status.get("lock") or {}).get("approval_id")),
            "open_order_exists": True,
            "open_order_count": 1,
            "reconciliation_classification": "wait",
            "blocked_reason": None if accepted else cancel_classification["error_name"],
            "next_safe_action": "remain_stopped",
            "forbidden_endpoint_check": True,
            "secrets_leak_check": True,
        },
        now,
    )
    body = cancel_result["body"] if isinstance(cancel_result["body"], dict) else {}
    return {
        "success": accepted,
        **response_base,
        "cancel_attempted": True,
        "cancel_accepted": accepted,
        "http_status": cancel_result["status"],
        "cancel_state": _sanitize_message(body.get("state")),
        "blocked_reason": None if accepted else cancel_classification["error_name"],
        "human_review_required": not accepted,
        "journal_write": journal,
        "remaining_req": cancel_result["remaining_req"],
        "error_name": None if accepted else cancel_classification["error_name"],
        "error_message": None if accepted else cancel_classification["error_message"],
    }


def _sell_fingerprint(market: str, side: str, ord_type: str, price: Decimal, volume: Decimal, estimated: Decimal) -> str:
    raw = "|".join([market, side, ord_type, format(price, "f"), format(volume, "f"), format(estimated, "f")])
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _live_sell_shape_failures(payload: SellTestRequest) -> tuple[list[str], str, str, str, Decimal | None, Decimal | None, Decimal | None]:
    market = str(payload.market or "")
    side = str(payload.side or "")
    ord_type = str(payload.ord_type or "")
    cleanup_action = str(payload.cleanup_action or "")
    price = _decimal_or_none(payload.price)
    volume = _decimal_or_none(payload.volume)
    estimated = _decimal_or_none(payload.estimated_krw_value)
    calculated = price * volume if price is not None and volume is not None else None
    failures: list[str] = []

    if market not in LIVE_SELL_ALLOWED_MARKETS:
        failures.append("LIVE_SELL_MARKET_NOT_ALLOWED")
    if side != "ask":
        failures.append("LIVE_SELL_ASK_ONLY")
    if ord_type != "limit":
        failures.append("LIVE_SELL_LIMIT_ONLY")
    if price is None or volume is None or price <= 0 or volume <= 0:
        failures.append("LIVE_SELL_INVALID_PRICE_VOLUME")
    if estimated is None or estimated < LIVE_SELL_MIN_KRW:
        failures.append("LIVE_SELL_MIN_KRW_NOT_MET")
    if estimated is not None and estimated > LIVE_SELL_MAX_KRW:
        failures.append("LIVE_SELL_MAX_KRW_EXCEEDED")
    if calculated is None or estimated is None or abs(calculated - estimated) > Decimal("1"):
        failures.append("LIVE_SELL_ESTIMATE_MISMATCH")
    if not _strict_false(payload.open_order_exists):
        failures.append("LIVE_SELL_OPEN_ORDER_EXISTS_OR_UNKNOWN")
    if not _strict_true(payload.portfolio_plan_valid):
        failures.append("LIVE_SELL_PORTFOLIO_PLAN_NOT_VALID")
    if not _strict_true(payload.cleanup_candidate):
        failures.append("LIVE_SELL_CLEANUP_CANDIDATE_REQUIRED")
    if cleanup_action not in LIVE_SELL_ALLOWED_ACTIONS:
        failures.append("LIVE_SELL_CLEANUP_ACTION_NOT_ALLOWED")

    return failures, market, side, ord_type, price, volume, estimated


def _blocked_sell_response(
    error_name: str,
    market: str,
    side: str,
    ord_type: str,
    estimated: Decimal | None,
    live_attempt: bool = False,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    response = {
        "http_status": None,
        "success": False,
        "market": market,
        "side": side,
        "ord_type": ord_type,
        "estimated_krw_value": float(estimated) if estimated is not None else None,
        "sell_order_test_passed": False,
        "live_sell_attempted": live_attempt,
        "live_sell_accepted": False,
        "remaining_req": None,
        "error_name": error_name,
        "error_message": error_name,
    }
    if extra:
        response.update(extra)
    return response


def _all_open_orders_clear_for_sell() -> dict[str, Any]:
    result = _upbit_get("/v1/orders/open")
    status = result["status"]
    body = result["body"]
    classification = _classify(status, body)
    open_orders = body if isinstance(body, list) else []
    success = classification["stop_code"] is None and isinstance(body, list)
    return {
        "http_status": status,
        "success": success,
        "open_order_count": len(open_orders),
        "open_order_exists": len(open_orders) > 0,
        "remaining_req": result["remaining_req"],
        "error_name": classification["error_name"],
        "error_message": classification["error_message"],
    }


def _asset_balance_gate_for_sell(market: str, volume: Decimal) -> dict[str, Any]:
    currency = market.split("-", 1)[1] if "-" in market else market
    result = _upbit_get("/v1/accounts")
    status = result["status"]
    body = result["body"]
    classification = _classify(status, body)
    accounts = body if isinstance(body, list) else []
    success = classification["stop_code"] is None and isinstance(body, list)
    available = None
    for row in accounts:
        if isinstance(row, dict) and str(row.get("currency")) == currency:
            available = _decimal_or_none(row.get("balance"))
            break
    sufficient = success and available is not None and available >= volume
    if not success:
        band = None
    elif available is None or available <= 0:
        band = "0"
    elif sufficient:
        band = "sufficient"
    else:
        band = "positive_below_order"
    return {
        "http_status": status,
        "success": success,
        "currency": currency,
        "asset_balance_sufficient": sufficient if success else None,
        "asset_available_band": band,
        "remaining_req": result["remaining_req"],
        "error_name": classification["error_name"],
        "error_message": classification["error_message"],
    }


def _orderbook_gate_for_sell(market: str, price: Decimal) -> dict[str, Any]:
    result = _upbit_public_get("/v1/orderbook", {"markets": market})
    status = result["status"]
    body = result["body"]
    classification = _classify(status, body)
    rows = body if isinstance(body, list) else []
    row = rows[0] if rows and isinstance(rows[0], dict) else {}
    units = row.get("orderbook_units") if isinstance(row, dict) else None
    unit = units[0] if isinstance(units, list) and units and isinstance(units[0], dict) else {}
    best_bid = _decimal_or_none(unit.get("bid_price"))
    best_ask = _decimal_or_none(unit.get("ask_price"))
    timestamp_ms = _int_or_none(row.get("timestamp")) if isinstance(row, dict) else None
    now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    clock_skew_ms = None
    if timestamp_ms is None:
        age_ms = None
    elif timestamp_ms > now_ms:
        clock_skew_ms = timestamp_ms - now_ms
        age_ms = 0
    else:
        age_ms = now_ms - timestamp_ms
    spread_bps = None
    if best_bid is not None and best_ask is not None and best_ask > 0:
        spread_bps = (best_ask - best_bid) / best_ask * Decimal("10000")

    failures: list[str] = []
    if classification["stop_code"] is not None or not rows:
        failures.append("LIVE_SELL_ORDERBOOK_UNAVAILABLE")
    if best_bid is None or best_ask is None or best_bid <= 0 or best_ask <= 0:
        failures.append("LIVE_SELL_ORDERBOOK_INVALID")
    elif best_bid >= best_ask:
        failures.append("LIVE_SELL_ORDERBOOK_CROSSED")
    elif price <= best_bid:
        failures.append("LIVE_SELL_MAKER_LIMIT_REQUIRED")
    if clock_skew_ms is not None and clock_skew_ms > 2000:
        failures.append("LIVE_SELL_ORDERBOOK_CLOCK_SKEW")
    if age_ms is None or age_ms > LIVE_SELL_MAX_ORDERBOOK_AGE_MS:
        failures.append("LIVE_SELL_ORDERBOOK_STALE")
    if spread_bps is None or spread_bps > Decimal("35"):
        failures.append("LIVE_SELL_SPREAD_TOO_WIDE")

    return {
        "http_status": status,
        "success": not failures,
        "best_bid": float(best_bid) if best_bid is not None else None,
        "best_ask": float(best_ask) if best_ask is not None else None,
        "spread_bps": float(spread_bps) if spread_bps is not None else None,
        "orderbook_timestamp_ms": timestamp_ms,
        "helper_now_ms": now_ms,
        "age_ms": age_ms,
        "clock_skew_ms": clock_skew_ms,
        "maker_limit_ok": not failures,
        "failures": failures,
        "remaining_req": result["remaining_req"],
        "error_name": "|".join(failures) if failures else classification["error_name"],
        "error_message": "|".join(failures) if failures else classification["error_message"],
    }


def _buy_fingerprint(market: str, side: str, ord_type: str, price: Decimal, volume: Decimal, estimated: Decimal) -> str:
    raw = "|".join([market, side, ord_type, format(price, "f"), format(volume, "f"), format(estimated, "f")])
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _live_buy_shape_failures(payload: BuyTestRequest) -> tuple[list[str], str, str, str, Decimal | None, Decimal | None, Decimal | None]:
    market = str(payload.market or "")
    side = str(payload.side or "")
    ord_type = str(payload.ord_type or "")
    price = _decimal_or_none(payload.price)
    volume = _decimal_or_none(payload.volume)
    estimated = _decimal_or_none(payload.estimated_krw_value)
    calculated = price * volume if price is not None and volume is not None else None
    score = _decimal_or_none(payload.brain_candidate_score)
    schema = str(payload.brain_schema_version or "")
    news_bias = str(payload.news_bias or "")
    failures: list[str] = []

    if market not in LIVE_BUY_ALLOWED_MARKETS:
        failures.append("LIVE_BUY_MARKET_NOT_ALLOWED")
    if side != "bid":
        failures.append("LIVE_BUY_BID_ONLY")
    if ord_type != "limit":
        failures.append("LIVE_BUY_LIMIT_ONLY")
    if price is None or volume is None or price <= 0 or volume <= 0:
        failures.append("LIVE_BUY_INVALID_PRICE_VOLUME")
    if estimated is None or estimated < LIVE_BUY_MIN_KRW:
        failures.append("LIVE_BUY_MIN_KRW_NOT_MET")
    if estimated is not None and estimated > LIVE_BUY_MAX_KRW:
        failures.append("LIVE_BUY_MAX_KRW_EXCEEDED")
    if calculated is None or estimated is None or abs(calculated - estimated) > Decimal("1"):
        failures.append("LIVE_BUY_ESTIMATE_MISMATCH")
    if not _strict_false(payload.open_order_exists):
        failures.append("LIVE_BUY_OPEN_ORDER_EXISTS_OR_UNKNOWN")
    if not schema.startswith("kbia.strategy_brain.v4"):
        failures.append("LIVE_BUY_BRAIN_SCHEMA_NOT_ALLOWED")
    if str(payload.brain_action or "") != "BUY_CANDIDATE":
        failures.append("LIVE_BUY_CANDIDATE_REQUIRED")
    if not _strict_true(payload.brain_live_ready):
        failures.append("LIVE_BUY_BRAIN_LIVE_READY_REQUIRED")
    if score is None or score < LIVE_BUY_MIN_BRAIN_SCORE:
        failures.append("LIVE_BUY_BRAIN_SCORE_TOO_LOW")
    if news_bias == "DEFENSIVE_REFERENCE":
        failures.append("LIVE_BUY_NEWS_DEFENSIVE")
    if not _strict_true(payload.scalping_candidate):
        failures.append("LIVE_BUY_SCALPING_CANDIDATE_REQUIRED")

    return failures, market, side, ord_type, price, volume, estimated


def _blocked_buy_response(
    error_name: str,
    market: str,
    side: str,
    ord_type: str,
    estimated: Decimal | None,
    live_attempt: bool = False,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    response = {
        "http_status": None,
        "success": False,
        "market": market,
        "side": side,
        "ord_type": ord_type,
        "estimated_krw_value": float(estimated) if estimated is not None else None,
        "buy_order_test_passed": False,
        "live_buy_attempted": live_attempt,
        "live_buy_accepted": False,
        "remaining_req": None,
        "error_name": error_name,
        "error_message": error_name,
    }
    if extra:
        response.update(extra)
    return response


def _all_open_orders_clear_for_buy() -> dict[str, Any]:
    result = _upbit_get("/v1/orders/open")
    status = result["status"]
    body = result["body"]
    classification = _classify(status, body)
    open_orders = body if isinstance(body, list) else []
    success = classification["stop_code"] is None and isinstance(body, list)
    return {
        "http_status": status,
        "success": success,
        "open_order_count": len(open_orders),
        "open_order_exists": len(open_orders) > 0,
        "remaining_req": result["remaining_req"],
        "error_name": classification["error_name"],
        "error_message": classification["error_message"],
    }


def _krw_balance_gate_for_buy(estimated: Decimal) -> dict[str, Any]:
    result = _upbit_get("/v1/accounts")
    status = result["status"]
    body = result["body"]
    classification = _classify(status, body)
    accounts = body if isinstance(body, list) else []
    success = classification["stop_code"] is None and isinstance(body, list)
    available = None
    for row in accounts:
        if isinstance(row, dict) and str(row.get("currency")) == "KRW":
            available = _decimal_or_none(row.get("balance"))
            break
    sufficient = success and available is not None and available >= estimated
    if not success:
        band = None
    elif available is None or available <= 0:
        band = "0"
    elif sufficient:
        band = "sufficient"
    else:
        band = "positive_below_order"
    return {
        "http_status": status,
        "success": success,
        "currency": "KRW",
        "krw_balance_sufficient": sufficient if success else None,
        "krw_available_band": band,
        "remaining_req": result["remaining_req"],
        "error_name": classification["error_name"],
        "error_message": classification["error_message"],
    }


def _orderbook_gate_for_buy(market: str, price: Decimal) -> dict[str, Any]:
    result = _upbit_public_get("/v1/orderbook", {"markets": market})
    status = result["status"]
    body = result["body"]
    classification = _classify(status, body)
    rows = body if isinstance(body, list) else []
    row = rows[0] if rows and isinstance(rows[0], dict) else {}
    units = row.get("orderbook_units") if isinstance(row, dict) else None
    unit = units[0] if isinstance(units, list) and units and isinstance(units[0], dict) else {}
    best_bid = _decimal_or_none(unit.get("bid_price"))
    best_ask = _decimal_or_none(unit.get("ask_price"))
    timestamp_ms = _int_or_none(row.get("timestamp")) if isinstance(row, dict) else None
    now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    clock_skew_ms = None
    if timestamp_ms is None:
        age_ms = None
    elif timestamp_ms > now_ms:
        clock_skew_ms = timestamp_ms - now_ms
        age_ms = 0
    else:
        age_ms = now_ms - timestamp_ms
    spread_bps = None
    if best_bid is not None and best_ask is not None and best_ask > 0:
        spread_bps = (best_ask - best_bid) / best_ask * Decimal("10000")

    failures: list[str] = []
    if classification["stop_code"] is not None or not rows:
        failures.append("LIVE_BUY_ORDERBOOK_UNAVAILABLE")
    if best_bid is None or best_ask is None or best_bid <= 0 or best_ask <= 0:
        failures.append("LIVE_BUY_ORDERBOOK_INVALID")
    elif best_bid >= best_ask:
        failures.append("LIVE_BUY_ORDERBOOK_CROSSED")
    elif price >= best_ask:
        failures.append("LIVE_BUY_MAKER_LIMIT_REQUIRED")
    if clock_skew_ms is not None and clock_skew_ms > 2000:
        failures.append("LIVE_BUY_ORDERBOOK_CLOCK_SKEW")
    if age_ms is None or age_ms > LIVE_BUY_MAX_ORDERBOOK_AGE_MS:
        failures.append("LIVE_BUY_ORDERBOOK_STALE")
    if spread_bps is None or spread_bps > LIVE_BUY_MAX_SPREAD_BPS:
        failures.append("LIVE_BUY_SPREAD_TOO_WIDE")

    return {
        "http_status": status,
        "success": not failures,
        "best_bid": float(best_bid) if best_bid is not None else None,
        "best_ask": float(best_ask) if best_ask is not None else None,
        "spread_bps": float(spread_bps) if spread_bps is not None else None,
        "orderbook_timestamp_ms": timestamp_ms,
        "helper_now_ms": now_ms,
        "age_ms": age_ms,
        "clock_skew_ms": clock_skew_ms,
        "maker_limit_ok": not failures,
        "failures": failures,
        "remaining_req": result["remaining_req"],
        "error_name": "|".join(failures) if failures else classification["error_name"],
        "error_message": "|".join(failures) if failures else classification["error_message"],
    }


@app.post("/upbit/order-test/telemetry")
def order_test_telemetry(payload: OrderTestRequest) -> dict[str, Any]:
    market = str(payload.market or "")
    side = str(payload.side or "")
    ord_type = str(payload.ord_type or "")
    price = _decimal_or_none(payload.price)
    volume = _decimal_or_none(payload.volume)
    estimated = price * volume if price is not None and volume is not None else None

    def blocked(error_name: str) -> dict[str, Any]:
        return {
            "http_status": None,
            "success": False,
            "market": market,
            "side": side,
            "ord_type": ord_type,
            "estimated_krw_value": float(estimated) if estimated is not None else None,
            "order_test_passed": False,
            "remaining_req": None,
            "error_name": error_name,
            "error_message": error_name,
        }

    if market != "KRW-BTC":
        return blocked("ORDER_TEST_MARKET_NOT_ALLOWED")
    if side != "bid":
        return blocked("ORDER_TEST_SIDE_NOT_ALLOWED")
    if ord_type != "limit":
        return blocked("ORDER_TEST_LIMIT_ONLY")
    if price is None or volume is None or price <= 0 or volume <= 0:
        return blocked("ORDER_TEST_INVALID_PRICE_VOLUME")
    if estimated is None or estimated > Decimal("10000"):
        return blocked("ORDER_TEST_MAX_KRW_EXCEEDED")

    result = _upbit_post(
        "/v1/orders/test",
        {
            "market": market,
            "side": side,
            "ord_type": ord_type,
            "price": format(price, "f"),
            "volume": format(volume, "f"),
        },
    )
    status = result["status"]
    body = result["body"]
    classification = _classify(status, body)
    success = classification["stop_code"] is None and status is not None and 200 <= status < 300

    return {
        "http_status": status,
        "success": success,
        "market": market,
        "side": side,
        "ord_type": ord_type,
        "estimated_krw_value": float(estimated),
        "order_test_passed": success,
        "remaining_req": result["remaining_req"],
        "error_name": classification["error_name"],
        "error_message": classification["error_message"],
    }


@app.post("/upbit/live-order/telemetry")
def live_order_telemetry(payload: LiveOrderRequest) -> dict[str, Any]:
    market = str(payload.market or "")
    side = str(payload.side or "")
    ord_type = str(payload.ord_type or "")
    price = _decimal_or_none(payload.price)
    volume = _decimal_or_none(payload.volume)
    estimated = _decimal_or_none(payload.estimated_krw_value)
    calculated = price * volume if price is not None and volume is not None else None

    def blocked(error_name: str) -> dict[str, Any]:
        return {
            "http_status": None,
            "success": False,
            "market": market,
            "side": side,
            "ord_type": ord_type,
            "estimated_krw_value": float(estimated) if estimated is not None else None,
            "live_order_attempted": False,
            "live_order_accepted": False,
            "remaining_req": None,
            "error_name": error_name,
            "error_message": error_name,
        }

    if not _strict_true(payload.live_order_enabled):
        return blocked("LIVE_ORDER_NOT_ENABLED")
    if not _strict_true(payload.execution_allowed):
        return blocked("LIVE_EXECUTION_NOT_ALLOWED")
    if str(payload.execution_mode or "") != "live":
        return blocked("LIVE_EXECUTION_MODE_REQUIRED")
    if not _strict_true(payload.all_pass):
        return blocked("LIVE_ALL_PASS_REQUIRED")
    if market != "KRW-BTC":
        return blocked("LIVE_MARKET_NOT_ALLOWED")
    if side != "bid":
        return blocked("LIVE_SIDE_NOT_ALLOWED")
    if ord_type != "limit":
        return blocked("LIVE_LIMIT_ONLY")
    if price is None or volume is None or price <= 0 or volume <= 0:
        return blocked("LIVE_INVALID_PRICE_VOLUME")
    if estimated is None or estimated < Decimal("5000"):
        return blocked("LIVE_MIN_KRW_NOT_MET")
    if estimated > Decimal("10000"):
        return blocked("LIVE_MAX_KRW_EXCEEDED")
    if calculated is None or abs(calculated - estimated) > Decimal("1"):
        return blocked("LIVE_ESTIMATE_MISMATCH")
    if str(payload.duplicate_lock_status or "") != "clear":
        return blocked("LIVE_DUPLICATE_LOCK_NOT_CLEAR")
    if not _strict_false(payload.open_order_exists):
        return blocked("LIVE_OPEN_ORDER_EXISTS_OR_UNKNOWN")
    if not _strict_false(payload.system_stop_active):
        return blocked("LIVE_SYSTEM_STOP_ACTIVE_OR_UNKNOWN")
    if not _strict_true(payload.order_test_passed):
        return blocked("LIVE_ORDER_TEST_NOT_PASSED")
    if not _strict_true(payload.one_time_live_attempt_allowed):
        return blocked("LIVE_ONE_TIME_ATTEMPT_NOT_ALLOWED")

    result = _upbit_post(
        "/v1/orders",
        {
            "market": market,
            "side": side,
            "ord_type": ord_type,
            "price": format(price, "f"),
            "volume": format(volume, "f"),
        },
    )
    status = result["status"]
    body = result["body"]
    classification = _classify(status, body)
    success = classification["stop_code"] is None and status is not None and 200 <= status < 300

    return {
        "http_status": status,
        "success": success,
        "market": market,
        "side": side,
        "ord_type": ord_type,
        "estimated_krw_value": float(estimated),
        "live_order_attempted": True,
        "live_order_accepted": success,
        "remaining_req": result["remaining_req"],
        "error_name": classification["error_name"],
        "error_message": classification["error_message"],
    }


@app.post("/upbit/buy-test/telemetry")
def buy_test_telemetry(payload: BuyTestRequest) -> dict[str, Any]:
    failures, market, side, ord_type, price, volume, estimated = _live_buy_shape_failures(payload)
    if failures or price is None or volume is None or estimated is None:
        return _blocked_buy_response("|".join(failures) if failures else "LIVE_BUY_INVALID_SHAPE", market, side, ord_type, estimated)

    open_gate = _all_open_orders_clear_for_buy()
    if not open_gate["success"] or open_gate["open_order_exists"]:
        return _blocked_buy_response("LIVE_BUY_OPEN_ORDER_EXISTS_OR_UNKNOWN", market, side, ord_type, estimated)

    balance_gate = _krw_balance_gate_for_buy(estimated)
    if balance_gate["krw_balance_sufficient"] is not True:
        return _blocked_buy_response("LIVE_BUY_KRW_BALANCE_NOT_SUFFICIENT", market, side, ord_type, estimated)

    orderbook_gate = _orderbook_gate_for_buy(market, price)
    if not orderbook_gate["success"]:
        return _blocked_buy_response(
            str(orderbook_gate["error_name"] or "LIVE_BUY_ORDERBOOK_GATE_FAILED"),
            market,
            side,
            ord_type,
            estimated,
            extra={
                "orderbook_age_ms": orderbook_gate["age_ms"],
                "orderbook_timestamp_ms": orderbook_gate["orderbook_timestamp_ms"],
                "helper_now_ms": orderbook_gate["helper_now_ms"],
                "clock_skew_ms": orderbook_gate["clock_skew_ms"],
                "best_bid": orderbook_gate["best_bid"],
                "best_ask": orderbook_gate["best_ask"],
                "spread_bps": orderbook_gate["spread_bps"],
                "maker_limit_ok": orderbook_gate["maker_limit_ok"],
                "orderbook_failures": orderbook_gate["failures"],
            },
        )

    result = _upbit_post(
        "/v1/orders/test",
        {
            "market": market,
            "side": side,
            "ord_type": ord_type,
            "price": format(price, "f"),
            "volume": format(volume, "f"),
        },
    )
    status = result["status"]
    body = result["body"]
    classification = _classify(status, body)
    success = classification["stop_code"] is None and status is not None and 200 <= status < 300

    return {
        "http_status": status,
        "success": success,
        "market": market,
        "side": side,
        "ord_type": ord_type,
        "estimated_krw_value": float(estimated),
        "buy_order_test_passed": success,
        "buy_test_fingerprint": _buy_fingerprint(market, side, ord_type, price, volume, estimated) if success else None,
        "live_buy_attempted": False,
        "live_buy_accepted": False,
        "open_order_count": open_gate["open_order_count"],
        "krw_balance_sufficient": balance_gate["krw_balance_sufficient"],
        "krw_available_band": balance_gate["krw_available_band"],
        "orderbook_age_ms": orderbook_gate["age_ms"],
        "maker_limit_ok": orderbook_gate["maker_limit_ok"],
        "remaining_req": result["remaining_req"],
        "error_name": classification["error_name"],
        "error_message": classification["error_message"],
    }


@app.post("/upbit/live-buy/telemetry")
def live_buy_telemetry(payload: LiveBuyRequest) -> dict[str, Any]:
    failures, market, side, ord_type, price, volume, estimated = _live_buy_shape_failures(payload)
    if failures or price is None or volume is None or estimated is None:
        return _blocked_buy_response("|".join(failures) if failures else "LIVE_BUY_INVALID_SHAPE", market, side, ord_type, estimated)
    if not _strict_true(payload.live_buy_enabled):
        return _blocked_buy_response("LIVE_BUY_NOT_ENABLED", market, side, ord_type, estimated)
    if not _strict_true(payload.execution_allowed):
        return _blocked_buy_response("LIVE_BUY_EXECUTION_NOT_ALLOWED", market, side, ord_type, estimated)
    if str(payload.execution_mode or "") != "live":
        return _blocked_buy_response("LIVE_BUY_EXECUTION_MODE_REQUIRED", market, side, ord_type, estimated)
    if not _strict_true(payload.all_pass):
        return _blocked_buy_response("LIVE_BUY_ALL_PASS_REQUIRED", market, side, ord_type, estimated)
    if str(payload.duplicate_lock_status or "") != "clear":
        return _blocked_buy_response("LIVE_BUY_DUPLICATE_LOCK_NOT_CLEAR", market, side, ord_type, estimated)
    if not _strict_false(payload.system_stop_active):
        return _blocked_buy_response("LIVE_BUY_SYSTEM_STOP_ACTIVE_OR_UNKNOWN", market, side, ord_type, estimated)
    if not _strict_true(payload.buy_order_test_passed):
        return _blocked_buy_response("LIVE_BUY_TEST_NOT_PASSED", market, side, ord_type, estimated)
    expected_fingerprint = _buy_fingerprint(market, side, ord_type, price, volume, estimated)
    if str(payload.buy_test_fingerprint or "") != expected_fingerprint:
        return _blocked_buy_response("LIVE_BUY_TEST_FINGERPRINT_MISMATCH", market, side, ord_type, estimated)
    if not _strict_true(payload.one_time_live_buy_attempt_allowed):
        return _blocked_buy_response("LIVE_BUY_ONE_TIME_ATTEMPT_NOT_ALLOWED", market, side, ord_type, estimated)

    open_gate = _all_open_orders_clear_for_buy()
    if not open_gate["success"] or open_gate["open_order_exists"]:
        return _blocked_buy_response("LIVE_BUY_OPEN_ORDER_EXISTS_OR_UNKNOWN", market, side, ord_type, estimated)

    balance_gate = _krw_balance_gate_for_buy(estimated)
    if balance_gate["krw_balance_sufficient"] is not True:
        return _blocked_buy_response("LIVE_BUY_KRW_BALANCE_NOT_SUFFICIENT", market, side, ord_type, estimated)

    orderbook_gate = _orderbook_gate_for_buy(market, price)
    if not orderbook_gate["success"]:
        return _blocked_buy_response(
            str(orderbook_gate["error_name"] or "LIVE_BUY_ORDERBOOK_GATE_FAILED"),
            market,
            side,
            ord_type,
            estimated,
            extra={
                "orderbook_age_ms": orderbook_gate["age_ms"],
                "orderbook_timestamp_ms": orderbook_gate["orderbook_timestamp_ms"],
                "helper_now_ms": orderbook_gate["helper_now_ms"],
                "clock_skew_ms": orderbook_gate["clock_skew_ms"],
                "best_bid": orderbook_gate["best_bid"],
                "best_ask": orderbook_gate["best_ask"],
                "spread_bps": orderbook_gate["spread_bps"],
                "maker_limit_ok": orderbook_gate["maker_limit_ok"],
                "orderbook_failures": orderbook_gate["failures"],
            },
        )

    result = _upbit_post(
        "/v1/orders",
        {
            "market": market,
            "side": side,
            "ord_type": ord_type,
            "price": format(price, "f"),
            "volume": format(volume, "f"),
        },
    )
    status = result["status"]
    body = result["body"]
    classification = _classify(status, body)
    success = classification["stop_code"] is None and status is not None and 200 <= status < 300

    return {
        "http_status": status,
        "success": success,
        "market": market,
        "side": side,
        "ord_type": ord_type,
        "estimated_krw_value": float(estimated),
        "buy_order_test_passed": True,
        "live_buy_attempted": True,
        "live_buy_accepted": success,
        "open_order_count": open_gate["open_order_count"],
        "krw_balance_sufficient": balance_gate["krw_balance_sufficient"],
        "krw_available_band": balance_gate["krw_available_band"],
        "orderbook_age_ms": orderbook_gate["age_ms"],
        "maker_limit_ok": orderbook_gate["maker_limit_ok"],
        "remaining_req": result["remaining_req"],
        "error_name": classification["error_name"],
        "error_message": classification["error_message"],
    }


@app.post("/upbit/sell-test/telemetry")
def sell_test_telemetry(payload: SellTestRequest) -> dict[str, Any]:
    failures, market, side, ord_type, price, volume, estimated = _live_sell_shape_failures(payload)
    if failures or price is None or volume is None or estimated is None:
        return _blocked_sell_response("|".join(failures) if failures else "LIVE_SELL_INVALID_SHAPE", market, side, ord_type, estimated)

    open_gate = _all_open_orders_clear_for_sell()
    if not open_gate["success"] or open_gate["open_order_exists"]:
        return _blocked_sell_response("LIVE_SELL_OPEN_ORDER_EXISTS_OR_UNKNOWN", market, side, ord_type, estimated)

    balance_gate = _asset_balance_gate_for_sell(market, volume)
    if balance_gate["asset_balance_sufficient"] is not True:
        return _blocked_sell_response("LIVE_SELL_ASSET_BALANCE_NOT_SUFFICIENT", market, side, ord_type, estimated)

    orderbook_gate = _orderbook_gate_for_sell(market, price)
    if not orderbook_gate["success"]:
        return _blocked_sell_response(
            str(orderbook_gate["error_name"] or "LIVE_SELL_ORDERBOOK_GATE_FAILED"),
            market,
            side,
            ord_type,
            estimated,
            extra={
                "orderbook_age_ms": orderbook_gate["age_ms"],
                "orderbook_timestamp_ms": orderbook_gate["orderbook_timestamp_ms"],
                "helper_now_ms": orderbook_gate["helper_now_ms"],
                "clock_skew_ms": orderbook_gate["clock_skew_ms"],
                "best_bid": orderbook_gate["best_bid"],
                "best_ask": orderbook_gate["best_ask"],
                "spread_bps": orderbook_gate["spread_bps"],
                "maker_limit_ok": orderbook_gate["maker_limit_ok"],
                "orderbook_failures": orderbook_gate["failures"],
            },
        )

    result = _upbit_post(
        "/v1/orders/test",
        {
            "market": market,
            "side": side,
            "ord_type": ord_type,
            "price": format(price, "f"),
            "volume": format(volume, "f"),
        },
    )
    status = result["status"]
    body = result["body"]
    classification = _classify(status, body)
    success = classification["stop_code"] is None and status is not None and 200 <= status < 300

    return {
        "http_status": status,
        "success": success,
        "market": market,
        "side": side,
        "ord_type": ord_type,
        "estimated_krw_value": float(estimated),
        "sell_order_test_passed": success,
        "sell_test_fingerprint": _sell_fingerprint(market, side, ord_type, price, volume, estimated) if success else None,
        "live_sell_attempted": False,
        "live_sell_accepted": False,
        "open_order_count": open_gate["open_order_count"],
        "asset_balance_sufficient": balance_gate["asset_balance_sufficient"],
        "asset_available_band": balance_gate["asset_available_band"],
        "orderbook_age_ms": orderbook_gate["age_ms"],
        "maker_limit_ok": orderbook_gate["maker_limit_ok"],
        "remaining_req": result["remaining_req"],
        "error_name": classification["error_name"],
        "error_message": classification["error_message"],
    }


@app.post("/upbit/live-sell/telemetry")
def live_sell_telemetry(payload: LiveSellRequest) -> dict[str, Any]:
    failures, market, side, ord_type, price, volume, estimated = _live_sell_shape_failures(payload)
    if failures or price is None or volume is None or estimated is None:
        return _blocked_sell_response("|".join(failures) if failures else "LIVE_SELL_INVALID_SHAPE", market, side, ord_type, estimated)
    if not _strict_true(payload.live_sell_enabled):
        return _blocked_sell_response("LIVE_SELL_NOT_ENABLED", market, side, ord_type, estimated)
    if not _strict_true(payload.execution_allowed):
        return _blocked_sell_response("LIVE_SELL_EXECUTION_NOT_ALLOWED", market, side, ord_type, estimated)
    if str(payload.execution_mode or "") != "live":
        return _blocked_sell_response("LIVE_SELL_EXECUTION_MODE_REQUIRED", market, side, ord_type, estimated)
    if not _strict_true(payload.all_pass):
        return _blocked_sell_response("LIVE_SELL_ALL_PASS_REQUIRED", market, side, ord_type, estimated)
    if str(payload.duplicate_lock_status or "") != "clear":
        return _blocked_sell_response("LIVE_SELL_DUPLICATE_LOCK_NOT_CLEAR", market, side, ord_type, estimated)
    if not _strict_false(payload.system_stop_active):
        return _blocked_sell_response("LIVE_SELL_SYSTEM_STOP_ACTIVE_OR_UNKNOWN", market, side, ord_type, estimated)
    if not _strict_true(payload.sell_order_test_passed):
        return _blocked_sell_response("LIVE_SELL_TEST_NOT_PASSED", market, side, ord_type, estimated)
    expected_fingerprint = _sell_fingerprint(market, side, ord_type, price, volume, estimated)
    if str(payload.sell_test_fingerprint or "") != expected_fingerprint:
        return _blocked_sell_response("LIVE_SELL_TEST_FINGERPRINT_MISMATCH", market, side, ord_type, estimated)
    if not _strict_true(payload.one_time_live_sell_attempt_allowed):
        return _blocked_sell_response("LIVE_SELL_ONE_TIME_ATTEMPT_NOT_ALLOWED", market, side, ord_type, estimated)

    open_gate = _all_open_orders_clear_for_sell()
    if not open_gate["success"] or open_gate["open_order_exists"]:
        return _blocked_sell_response("LIVE_SELL_OPEN_ORDER_EXISTS_OR_UNKNOWN", market, side, ord_type, estimated)

    balance_gate = _asset_balance_gate_for_sell(market, volume)
    if balance_gate["asset_balance_sufficient"] is not True:
        return _blocked_sell_response("LIVE_SELL_ASSET_BALANCE_NOT_SUFFICIENT", market, side, ord_type, estimated)

    orderbook_gate = _orderbook_gate_for_sell(market, price)
    if not orderbook_gate["success"]:
        return _blocked_sell_response(
            str(orderbook_gate["error_name"] or "LIVE_SELL_ORDERBOOK_GATE_FAILED"),
            market,
            side,
            ord_type,
            estimated,
            extra={
                "orderbook_age_ms": orderbook_gate["age_ms"],
                "orderbook_timestamp_ms": orderbook_gate["orderbook_timestamp_ms"],
                "helper_now_ms": orderbook_gate["helper_now_ms"],
                "clock_skew_ms": orderbook_gate["clock_skew_ms"],
                "best_bid": orderbook_gate["best_bid"],
                "best_ask": orderbook_gate["best_ask"],
                "spread_bps": orderbook_gate["spread_bps"],
                "maker_limit_ok": orderbook_gate["maker_limit_ok"],
                "orderbook_failures": orderbook_gate["failures"],
            },
        )

    result = _upbit_post(
        "/v1/orders",
        {
            "market": market,
            "side": side,
            "ord_type": ord_type,
            "price": format(price, "f"),
            "volume": format(volume, "f"),
        },
    )
    status = result["status"]
    body = result["body"]
    classification = _classify(status, body)
    success = classification["stop_code"] is None and status is not None and 200 <= status < 300

    return {
        "http_status": status,
        "success": success,
        "market": market,
        "side": side,
        "ord_type": ord_type,
        "estimated_krw_value": float(estimated),
        "sell_order_test_passed": True,
        "live_sell_attempted": True,
        "live_sell_accepted": success,
        "open_order_count": open_gate["open_order_count"],
        "asset_balance_sufficient": balance_gate["asset_balance_sufficient"],
        "asset_available_band": balance_gate["asset_available_band"],
        "orderbook_age_ms": orderbook_gate["age_ms"],
        "maker_limit_ok": orderbook_gate["maker_limit_ok"],
        "remaining_req": result["remaining_req"],
        "error_name": classification["error_name"],
        "error_message": classification["error_message"],
    }
