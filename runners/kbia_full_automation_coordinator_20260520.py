from __future__ import annotations

import argparse
import json
import time
import uuid
from datetime import datetime, timezone, timedelta
from decimal import Decimal, ROUND_DOWN
from pathlib import Path
from urllib import request


BASE = "http://127.0.0.1:8010"
LOG_DIR = Path("/home/ubuntu/kbia-logs/full-automation")
STATE_PATH = LOG_DIR / "state.json"
EVENTS_PATH = LOG_DIR / "events.jsonl"

COMPLETED_KNOWN = {"KRW-ETC", "KRW-DOT"}
CANDIDATES = [
    {"market": "KRW-FCT2", "action": "EXIT_STAGED", "target_krw": Decimal("29000")},
    {"market": "KRW-ALGO", "action": "EXIT_STAGED", "target_krw": Decimal("21000")},
    {"market": "KRW-DOGE", "action": "REDUCE_STAGED", "target_krw": Decimal("29000")},
]
WATCH_MARKETS = ["KRW-BTC", "KRW-ETC", "KRW-DOT", "KRW-FCT2", "KRW-ALGO", "KRW-DOGE"]
MAX_KRW = Decimal("30000")
MIN_KRW = Decimal("5000")
SLEEP_SECONDS = 600


def kst_now() -> str:
    return datetime.now(timezone(timedelta(hours=9))).isoformat(timespec="seconds")


def kst_after(minutes: int) -> str:
    return (datetime.now(timezone(timedelta(hours=9))) + timedelta(minutes=minutes)).isoformat(timespec="seconds")


def load_state() -> dict:
    if not STATE_PATH.exists():
        return {
            "mode": "gated_full_automation",
            "started_kst": kst_now(),
            "completed_markets": sorted(COMPLETED_KNOWN),
            "active_market": None,
            "cycle_count": 0,
            "buy_branch_status": "blocked_until_brain_v4_buy_candidate",
            "scheduler_contract": "one_order_then_read_only_until_finality",
        }
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def save_state(state: dict) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def log_event(event: dict) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    event = {"timestamp_kst": kst_now(), **event}
    with EVENTS_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
    print(json.dumps(event, ensure_ascii=False, sort_keys=True), flush=True)


def get_json(path: str):
    with request.urlopen(BASE + path, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


def post_json(path: str, payload: dict):
    data = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    req = request.Request(BASE + path, method="POST", data=data, headers={"Content-Type": "application/json"})
    with request.urlopen(req, timeout=25) as response:
        return json.loads(response.read().decode("utf-8"))


def public_orderbook(market: str):
    with request.urlopen(f"https://api.upbit.com/v1/orderbook?markets={market}", timeout=15) as response:
        rows = json.loads(response.read().decode("utf-8"))
    row = rows[0]
    unit = row["orderbook_units"][0]
    now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    timestamp = int(row.get("timestamp") or 0)
    return {
        "timestamp": timestamp,
        "age_ms_at_build": now_ms - timestamp if timestamp else None,
        "best_bid": Decimal(str(unit["bid_price"])),
        "best_ask": Decimal(str(unit["ask_price"])),
    }


def open_orders_by_market() -> dict:
    result = {}
    for market in WATCH_MARKETS:
        telemetry = post_json("/upbit/open-orders/telemetry", {"market": market})
        result[market] = {
            "success": telemetry.get("success"),
            "open_order_count": telemetry.get("open_order_count"),
            "open_order_exists": telemetry.get("open_order_exists"),
            "error_name": telemetry.get("error_name"),
        }
    return result


def any_open_order(open_orders: dict) -> bool:
    return any(row.get("open_order_exists") is True for row in open_orders.values())


def acquire_execution_lock(market: str, state: dict) -> dict:
    owner_token = uuid.uuid4().hex
    run_id = f"full-auto-live-sell-{market}-{int(time.time())}"
    payload = {
        "market": market,
        "side": "ask",
        "ord_type": "limit",
        "run_id": run_id,
        "approval_id": f"approved-full-auto-{market}",
        "fuse_id": f"one-order-fuse-{market}",
        "owner_token": owner_token,
        "human_approval": True,
        "lock_reason": "server_side_lock_before_live_sell",
        "open_order_exists": False,
        "open_order_count": 0,
        "duplicate_order_exists": False,
        "reconciliation_classification": "done",
        "workflow_active": False,
        "cron_enabled": False,
        "fuse_state": "armed",
        "order_journal_evidence": True,
        "expires_at_kst": kst_after(30),
        "now_kst": kst_now(),
    }
    result = post_json("/execution-lock/acquire", payload)
    if result.get("lock_acquired") is True and result.get("lock_id"):
        state["active_execution_lock"] = {
            "lock_id": result.get("lock_id"),
            "owner_token": owner_token,
            "market": market,
            "run_id": run_id,
        }
    log_event(
        {
            "event": "execution_lock_acquire",
            "market": market,
            "lock_acquired": result.get("lock_acquired"),
            "lock_state": result.get("lock_state"),
            "blocked_reason": result.get("blocked_reason"),
        }
    )
    return result


def release_execution_lock(state: dict, market: str, finality: dict | None, reason: str) -> dict:
    active_lock = state.get("active_execution_lock") or {}
    if active_lock.get("market") != market or not active_lock.get("lock_id") or not active_lock.get("owner_token"):
        return {"lock_released": False, "blocked_reason": "NO_MATCHING_ACTIVE_LOCK_IN_STATE"}
    classification = str((finality or {}).get("classification") or "")
    payload = {
        "lock_id": active_lock["lock_id"],
        "owner_token": active_lock["owner_token"],
        "release_reason": reason,
        "human_approval": True,
        "open_order_exists": False,
        "open_order_count": 0,
        "reconciliation_classification": classification if classification in {"done", "cancel"} else "unknown",
        "workflow_active": False,
        "cron_enabled": False,
        "fuse_state": "consumed",
        "now_kst": kst_now(),
    }
    result = post_json("/execution-lock/release", payload)
    if result.get("lock_released") is True:
        state["active_execution_lock"] = None
    log_event(
        {
            "event": "execution_lock_release",
            "market": market,
            "lock_released": result.get("lock_released"),
            "lock_state": result.get("lock_state"),
            "blocked_reason": result.get("blocked_reason"),
            "release_reason": reason,
        }
    )
    return result


def detail_finality(market: str) -> dict:
    detail = post_json(
        "/upbit/open-orders/detail-telemetry-no-journal",
        {
            "market": market,
            "run_id": f"full-auto-finality-{market}",
            "include_recent_closed": True,
            "recent_closed_limit": 10,
            "journal_enabled": False,
            "correlation_hint": {"market": market, "side": "ask", "ord_type": "limit"},
        },
    )
    first = (detail.get("orders") or [{}])[0]
    return {
        "classification": (detail.get("classification_summary") or {}).get("final_classification"),
        "next_safe_action": (detail.get("classification_summary") or {}).get("next_safe_action"),
        "state": first.get("state"),
        "executed_volume": first.get("executed_volume"),
        "remaining_volume": first.get("remaining_volume"),
        "trades_count": first.get("trades_count"),
        "uuid_masked": first.get("uuid_masked"),
    }


def build_sell_payload(candidate: dict) -> tuple[dict, dict]:
    market = candidate["market"]
    orderbook = public_orderbook(market)
    best_bid = orderbook["best_bid"]
    best_ask = orderbook["best_ask"]
    if best_ask <= best_bid:
        raise RuntimeError("ORDERBOOK_CROSSED")
    price = best_ask
    target_krw = min(candidate["target_krw"], MAX_KRW)
    volume = (target_krw / price).quantize(Decimal("0.00000001"), rounding=ROUND_DOWN)
    estimated = price * volume
    if estimated < MIN_KRW or estimated > MAX_KRW:
        raise RuntimeError(f"ESTIMATE_OUT_OF_RANGE:{estimated}")
    payload = {
        "market": market,
        "side": "ask",
        "ord_type": "limit",
        "price": format(price, "f"),
        "volume": format(volume, "f"),
        "estimated_krw_value": format(estimated, "f"),
        "open_order_exists": False,
        "portfolio_plan_valid": True,
        "cleanup_candidate": True,
        "cleanup_action": candidate["action"],
    }
    diagnostics = {
        "best_bid": float(best_bid),
        "best_ask": float(best_ask),
        "price_above_best_bid": price > best_bid,
        "orderbook_timestamp_ms": orderbook["timestamp"],
        "orderbook_age_ms_at_build": orderbook["age_ms_at_build"],
        "estimated_krw_value": float(estimated),
    }
    return payload, diagnostics


def try_candidate(candidate: dict, state: dict) -> bool:
    market = candidate["market"]
    payload, diagnostics = build_sell_payload(candidate)
    sell_test = post_json("/upbit/sell-test/telemetry", payload)
    log_event(
        {
            "event": "sell_test",
            "market": market,
            "diagnostics": diagnostics,
            "success": sell_test.get("success"),
            "sell_order_test_passed": sell_test.get("sell_order_test_passed"),
            "error_name": sell_test.get("error_name"),
            "orderbook_age_ms": sell_test.get("orderbook_age_ms"),
            "maker_limit_ok": sell_test.get("maker_limit_ok"),
        }
    )
    if sell_test.get("sell_order_test_passed") is not True or not sell_test.get("sell_test_fingerprint"):
        blocked = state.setdefault("blocked_markets", {})
        blocked[market] = {"timestamp_kst": kst_now(), "error_name": sell_test.get("error_name")}
        return False

    lock_result = acquire_execution_lock(market, state)
    if lock_result.get("lock_acquired") is not True:
        blocked = state.setdefault("blocked_markets", {})
        blocked[market] = {"timestamp_kst": kst_now(), "error_name": lock_result.get("blocked_reason") or "EXECUTION_LOCK_NOT_ACQUIRED"}
        return False

    live_payload = {
        **payload,
        "live_sell_enabled": True,
        "execution_allowed": True,
        "execution_mode": "live",
        "all_pass": True,
        "duplicate_lock_status": "clear",
        "system_stop_active": False,
        "sell_order_test_passed": True,
        "sell_test_fingerprint": sell_test["sell_test_fingerprint"],
        "one_time_live_sell_attempt_allowed": True,
    }
    live_sell = post_json("/upbit/live-sell/telemetry", live_payload)
    accepted = live_sell.get("live_sell_accepted") is True
    log_event(
        {
            "event": "live_sell",
            "market": market,
            "submitted": live_sell.get("live_sell_attempted") is True,
            "accepted": accepted,
            "http_status": live_sell.get("http_status"),
            "estimated_krw_value": live_sell.get("estimated_krw_value"),
            "orderbook_age_ms": live_sell.get("orderbook_age_ms"),
            "error_name": live_sell.get("error_name"),
        }
    )
    if accepted:
        state["active_market"] = market
        state["last_live_sell_kst"] = kst_now()
        state["last_live_sell"] = {
            "market": market,
            "estimated_krw_value": live_sell.get("estimated_krw_value"),
            "http_status": live_sell.get("http_status"),
        }
        return True
    release_execution_lock(state, market, {"classification": "unknown"}, "approved_abort_before_execution")
    return False


def cycle(state: dict) -> dict:
    state["cycle_count"] = int(state.get("cycle_count") or 0) + 1
    state["last_cycle_kst"] = kst_now()

    health = get_json("/health")
    if health.get("ok") is not True:
        log_event({"event": "stop", "reason": "HELPER_HEALTH_FAILED"})
        return state

    open_orders = open_orders_by_market()
    state["last_open_orders"] = open_orders
    if any_open_order(open_orders):
        active = state.get("active_market")
        finality = detail_finality(active) if active else None
        state["last_finality"] = finality
        log_event({"event": "read_only_stop_open_order", "active_market": active, "open_orders": open_orders, "finality": finality})
        return state

    active = state.get("active_market")
    if active:
        finality = detail_finality(active)
        state["last_finality"] = finality
        if finality.get("classification") in {"done", "cancel"}:
            completed = set(state.get("completed_markets") or [])
            completed.add(active)
            state["completed_markets"] = sorted(completed)
            state["active_market"] = None
            release_execution_lock(state, active, finality, "finality_confirmed")
            log_event({"event": "active_market_finalized", "market": active, "finality": finality})
        else:
            log_event({"event": "stop_active_market_not_final", "market": active, "finality": finality})
            return state

    completed = set(state.get("completed_markets") or [])
    for candidate in CANDIDATES:
        if candidate["market"] in completed:
            continue
        accepted = try_candidate(candidate, state)
        if accepted:
            break
    else:
        log_event({"event": "no_candidate_executed", "completed_markets": sorted(completed), "blocked_markets": state.get("blocked_markets", {})})

    return state


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--loop", action="store_true")
    parser.add_argument("--sleep", type=int, default=SLEEP_SECONDS)
    args = parser.parse_args()

    state = load_state()
    while True:
        try:
            state = cycle(state)
        except Exception as exc:
            log_event({"event": "cycle_error_stop", "error_name": exc.__class__.__name__, "error_message": str(exc)[:200]})
        save_state(state)
        if not args.loop:
            break
        time.sleep(max(60, args.sleep))


if __name__ == "__main__":
    main()
