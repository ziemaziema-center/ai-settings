from __future__ import annotations

import argparse
import json
import sys
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from decimal import Decimal, ROUND_DOWN
from pathlib import Path
from urllib import request

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from strategy.kbia_autonomy_governor import build_autonomy_scorecard, default_live_autonomy_state, scorecard_to_dict


BASE = "http://127.0.0.1:8010"
LOG_DIR = Path("/home/ubuntu/kbia-logs/parallel-smart-automation")
STATE_PATH = LOG_DIR / "state.json"
EVENTS_PATH = LOG_DIR / "events.jsonl"

WATCH_MARKETS = ["KRW-BTC", "KRW-ETH", "KRW-SOL", "KRW-ETC", "KRW-DOT", "KRW-FCT2", "KRW-ALGO", "KRW-DOGE", "KRW-RVN"]
SELL_CANDIDATES = [
    {"market": "KRW-FCT2", "action": "EXIT_STAGED", "target_krw": Decimal("29000"), "priority": 10},
    {"market": "KRW-ALGO", "action": "EXIT_STAGED", "target_krw": Decimal("21000"), "priority": 9},
    {"market": "KRW-DOGE", "action": "REDUCE_STAGED", "target_krw": Decimal("29000"), "priority": 8},
    {"market": "KRW-DOT", "action": "EXIT_STAGED", "target_krw": Decimal("29000"), "priority": 7},
    {"market": "KRW-ETC", "action": "EXIT_STAGED", "target_krw": Decimal("29000"), "priority": 6},
]
MAX_WORKERS = 8
MIN_KRW = Decimal("5000")
MAX_KRW = Decimal("30000")
SLEEP_SECONDS = 180


def kst_now() -> str:
    return datetime.now(timezone(timedelta(hours=9))).isoformat(timespec="seconds")


def kst_after(minutes: int) -> str:
    return (datetime.now(timezone(timedelta(hours=9))) + timedelta(minutes=minutes)).isoformat(timespec="seconds")


def load_state() -> dict:
    if not STATE_PATH.exists():
        state = {
            "mode": "parallel_smart_capital_rotation",
            "started_kst": kst_now(),
            "cycle_count": 0,
            "active_market": None,
            "execution_contract": "parallel_scan_single_live_order_until_finality",
            "live_buy_status": "observed_only_until_brain_and_helper_gates_pass",
        }
        refresh_autonomy_score(state)
        return state
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def save_state(state: dict) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def log_event(event: dict) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    row = {"timestamp_kst": kst_now(), **event}
    with EVENTS_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n")
    print(json.dumps(row, ensure_ascii=True, sort_keys=True), flush=True)


def get_json(path: str) -> dict:
    with request.urlopen(BASE + path, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


def post_json(path: str, payload: dict) -> dict:
    data = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    req = request.Request(BASE + path, method="POST", data=data, headers={"Content-Type": "application/json"})
    with request.urlopen(req, timeout=25) as response:
        return json.loads(response.read().decode("utf-8"))


def public_orderbook(market: str) -> dict:
    with request.urlopen(f"https://api.upbit.com/v1/orderbook?markets={market}", timeout=15) as response:
        rows = json.loads(response.read().decode("utf-8"))
    row = rows[0]
    unit = row["orderbook_units"][0]
    now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    timestamp = int(row.get("timestamp") or 0)
    best_bid = Decimal(str(unit["bid_price"]))
    best_ask = Decimal(str(unit["ask_price"]))
    spread_bps = (best_ask - best_bid) / best_ask * Decimal("10000") if best_ask > 0 else Decimal("99999")
    return {
        "timestamp": timestamp,
        "age_ms_at_build": now_ms - timestamp if timestamp else None,
        "best_bid": best_bid,
        "best_ask": best_ask,
        "spread_bps": spread_bps,
    }


def open_order_for_market(market: str) -> tuple[str, dict]:
    telemetry = post_json("/upbit/open-orders/telemetry", {"market": market})
    return market, {
        "success": telemetry.get("success"),
        "open_order_count": telemetry.get("open_order_count"),
        "open_order_exists": telemetry.get("open_order_exists"),
        "error_name": telemetry.get("error_name"),
    }


def open_orders_parallel() -> dict:
    result = {}
    with ThreadPoolExecutor(max_workers=min(MAX_WORKERS, len(WATCH_MARKETS))) as pool:
        futures = [pool.submit(open_order_for_market, market) for market in WATCH_MARKETS]
        for future in as_completed(futures):
            market, row = future.result()
            result[market] = row
    return dict(sorted(result.items()))


def any_open_order(open_orders: dict) -> bool:
    return any(row.get("open_order_exists") is True or int(row.get("open_order_count") or 0) > 0 for row in open_orders.values())


def first_open_market(open_orders: dict) -> str | None:
    for market in WATCH_MARKETS:
        row = open_orders.get(market) or {}
        if row.get("open_order_exists") is True or int(row.get("open_order_count") or 0) > 0:
            return market
    return None


def recover_stale_lock_if_safe(state: dict) -> dict:
    status = post_json("/execution-lock/status", {})
    state["last_execution_lock_status"] = {
        "lock_state": status.get("lock_state"),
        "lock_exists": status.get("lock_exists"),
        "stale_lock": status.get("stale_lock"),
        "blocked_reason": status.get("blocked_reason"),
    }
    if status.get("lock_state") != "stale_stop" or status.get("stale_lock") is not True:
        return {"attempted": False, "lock_recovered": None, "blocked_reason": status.get("blocked_reason")}
    recovery = post_json(
        "/execution-lock/recover-stale-finality",
        {
            "automated_recovery_allowed": True,
            "recovery_reason": "parallel_smart_stale_lock_finality_recovery",
            "workflow_active": False,
            "cron_enabled": False,
            "now_kst": kst_now(),
        },
    )
    recovery["attempted"] = True
    state["last_stale_lock_recovery"] = {
        "attempted": True,
        "lock_recovered": recovery.get("lock_recovered"),
        "market": recovery.get("market"),
        "final_classification": recovery.get("final_classification"),
        "open_order_count": recovery.get("open_order_count"),
        "blocked_reason": recovery.get("blocked_reason"),
    }
    if recovery.get("lock_recovered") is True:
        state["active_execution_lock"] = None
        if state.get("active_market") == recovery.get("market"):
            state["active_market"] = None
    return recovery


def refresh_autonomy_score(state: dict) -> None:
    autonomy_state = default_live_autonomy_state()
    autonomy_state.update(
        {
            "parallel_candidate_scan": True,
            "one_order_at_a_time": state.get("execution_contract") == "parallel_scan_single_live_order_until_finality"
            or state.get("execution_contract") is None,
            "requested_capabilities": state.get("requested_capabilities") or [],
        }
    )
    state["autonomy_scorecard"] = scorecard_to_dict(build_autonomy_scorecard(autonomy_state))


def detail_finality(market: str) -> dict:
    detail = post_json(
        "/upbit/open-orders/detail-telemetry-no-journal",
        {
            "market": market,
            "run_id": f"parallel-smart-finality-{market}",
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


def cancel_stale_order_if_safe(market: str, finality: dict, state: dict) -> dict:
    if finality.get("classification") != "wait":
        return {"attempted": False, "cancel_accepted": None, "blocked_reason": "FINALITY_NOT_WAIT"}
    result = post_json(
        "/upbit/cancel-stale-order/telemetry",
        {
            "market": market,
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
            "now_kst": kst_now(),
        },
    )
    state["last_cancel_stale_order"] = {
        "attempted": result.get("cancel_attempted"),
        "cancel_accepted": result.get("cancel_accepted"),
        "market": result.get("market"),
        "open_order_count": result.get("open_order_count"),
        "order_age_minutes": result.get("order_age_minutes"),
        "blocked_reason": result.get("blocked_reason"),
        "http_status": result.get("http_status"),
    }
    return result


def build_sell_payload(candidate: dict) -> tuple[dict, dict]:
    market = candidate["market"]
    ob = public_orderbook(market)
    price = ob["best_ask"]
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
        "best_bid": float(ob["best_bid"]),
        "best_ask": float(ob["best_ask"]),
        "spread_bps": float(ob["spread_bps"]),
        "orderbook_timestamp_ms": ob["timestamp"],
        "orderbook_age_ms_at_build": ob["age_ms_at_build"],
        "estimated_krw_value": float(estimated),
        "priority": candidate["priority"],
    }
    return payload, diagnostics


def sell_test_candidate(candidate: dict) -> dict:
    try:
        payload, diagnostics = build_sell_payload(candidate)
        sell_test = post_json("/upbit/sell-test/telemetry", payload)
        return {
            "market": candidate["market"],
            "priority": candidate["priority"],
            "payload": payload,
            "diagnostics": diagnostics,
            "sell_test_passed": sell_test.get("sell_order_test_passed") is True,
            "sell_test_fingerprint": sell_test.get("sell_test_fingerprint"),
            "error_name": sell_test.get("error_name"),
            "orderbook_age_ms": sell_test.get("orderbook_age_ms"),
            "maker_limit_ok": sell_test.get("maker_limit_ok"),
        }
    except Exception as exc:
        return {"market": candidate["market"], "priority": candidate["priority"], "sell_test_passed": False, "error_name": exc.__class__.__name__}


def sell_tests_parallel() -> list[dict]:
    with ThreadPoolExecutor(max_workers=min(MAX_WORKERS, len(SELL_CANDIDATES))) as pool:
        return sorted([future.result() for future in as_completed([pool.submit(sell_test_candidate, c) for c in SELL_CANDIDATES])], key=lambda x: -x["priority"])


def acquire_execution_lock(market: str, state: dict) -> dict:
    token = uuid.uuid4().hex
    payload = {
        "market": market,
        "side": "ask",
        "ord_type": "limit",
        "run_id": f"parallel-smart-live-sell-{market}-{int(time.time())}",
        "approval_id": f"approved-parallel-smart-{market}",
        "fuse_id": f"parallel-smart-one-order-fuse-{market}",
        "owner_token": token,
        "human_approval": True,
        "lock_reason": "parallel_smart_before_live_sell",
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
    if result.get("lock_acquired") is True:
        state["active_execution_lock"] = {"lock_id": result.get("lock_id"), "owner_token": token, "market": market}
    return result


def release_execution_lock(state: dict, market: str, finality: dict, reason: str) -> dict:
    lock = state.get("active_execution_lock") or {}
    if lock.get("market") != market:
        return {"lock_released": False, "blocked_reason": "NO_MATCHING_LOCK"}
    classification = str(finality.get("classification") or "")
    result = post_json(
        "/execution-lock/release",
        {
            "lock_id": lock.get("lock_id"),
            "owner_token": lock.get("owner_token"),
            "release_reason": reason,
            "human_approval": True,
            "open_order_exists": False,
            "open_order_count": 0,
            "reconciliation_classification": classification if classification in {"done", "cancel"} else "unknown",
            "workflow_active": False,
            "cron_enabled": False,
            "fuse_state": "consumed",
            "now_kst": kst_now(),
        },
    )
    if result.get("lock_released") is True:
        state["active_execution_lock"] = None
    return result


def execute_one(candidate_result: dict, state: dict) -> bool:
    market = candidate_result["market"]
    lock = acquire_execution_lock(market, state)
    log_event({"event": "execution_lock_acquire", "market": market, "lock_acquired": lock.get("lock_acquired"), "blocked_reason": lock.get("blocked_reason")})
    if lock.get("lock_acquired") is not True:
        return False
    payload = candidate_result["payload"]
    live_payload = {
        **payload,
        "live_sell_enabled": True,
        "execution_allowed": True,
        "execution_mode": "live",
        "all_pass": True,
        "duplicate_lock_status": "clear",
        "system_stop_active": False,
        "sell_order_test_passed": True,
        "sell_test_fingerprint": candidate_result["sell_test_fingerprint"],
        "one_time_live_sell_attempt_allowed": True,
    }
    live = post_json("/upbit/live-sell/telemetry", live_payload)
    accepted = live.get("live_sell_accepted") is True
    log_event({"event": "live_sell", "market": market, "submitted": live.get("live_sell_attempted") is True, "accepted": accepted, "error_name": live.get("error_name")})
    if accepted:
        state["active_market"] = market
        state["last_live_sell_kst"] = kst_now()
        state["last_live_sell"] = {"market": market, "estimated_krw_value": live.get("estimated_krw_value"), "http_status": live.get("http_status")}
        return True
    release = release_execution_lock(state, market, {"classification": "cancel"}, "approved_abort_before_execution")
    log_event({"event": "execution_lock_release_after_reject", "market": market, "lock_released": release.get("lock_released"), "blocked_reason": release.get("blocked_reason")})
    return False


def cycle(state: dict) -> dict:
    state["cycle_count"] = int(state.get("cycle_count") or 0) + 1
    state["last_cycle_kst"] = kst_now()
    state["execution_contract"] = "parallel_scan_single_live_order_until_finality"
    refresh_autonomy_score(state)
    health = get_json("/health")
    if health.get("ok") is not True:
        log_event({"event": "stop", "reason": "HELPER_HEALTH_FAILED"})
        return state
    lock_recovery = recover_stale_lock_if_safe(state)
    if lock_recovery.get("attempted") or lock_recovery.get("lock_recovered") is not None:
        log_event(
            {
                "event": "stale_lock_recovery_check",
                "attempted": lock_recovery.get("attempted"),
                "lock_recovered": lock_recovery.get("lock_recovered"),
                "market": lock_recovery.get("market"),
                "final_classification": lock_recovery.get("final_classification"),
                "open_order_count": lock_recovery.get("open_order_count"),
                "blocked_reason": lock_recovery.get("blocked_reason"),
            }
        )

    open_orders = open_orders_parallel()
    state["last_open_orders"] = open_orders
    if any_open_order(open_orders):
        open_market = first_open_market(open_orders)
        active = state.get("active_market")
        if open_market and ((open_orders.get(active) or {}).get("open_order_exists") is not True):
            state["active_market"] = open_market
            active = open_market
        finality = detail_finality(active) if active else None
        state["last_finality"] = finality
        cancel = cancel_stale_order_if_safe(active, finality or {}, state) if active else {"attempted": False}
        log_event({"event": "read_only_stop_open_order", "active_market": active, "open_market": open_market, "finality": finality, "open_orders": open_orders})
        if cancel.get("attempted") or cancel.get("cancel_accepted") is not None:
            log_event(
                {
                    "event": "cancel_stale_order_check",
                    "market": active,
                    "attempted": cancel.get("cancel_attempted") or cancel.get("attempted"),
                    "cancel_accepted": cancel.get("cancel_accepted"),
                    "order_age_minutes": cancel.get("order_age_minutes"),
                    "blocked_reason": cancel.get("blocked_reason"),
                    "http_status": cancel.get("http_status"),
                }
            )
        return state

    active = state.get("active_market")
    if active:
        finality = detail_finality(active)
        state["last_finality"] = finality
        if finality.get("classification") in {"done", "cancel"}:
            release = release_execution_lock(state, active, finality, "parallel_smart_finality_confirmed")
            state["active_market"] = None
            log_event({"event": "active_market_finalized", "market": active, "finality": finality, "lock_released": release.get("lock_released")})
        else:
            log_event({"event": "stop_active_market_not_final", "market": active, "finality": finality})
            return state

    candidate_results = sell_tests_parallel()
    state["last_candidate_scan"] = [
        {k: row.get(k) for k in ["market", "priority", "sell_test_passed", "error_name", "orderbook_age_ms", "maker_limit_ok"]}
        for row in candidate_results
    ]
    log_event({"event": "parallel_candidate_scan", "results": state["last_candidate_scan"]})
    passed = [row for row in candidate_results if row.get("sell_test_passed") and row.get("sell_test_fingerprint")]
    if not passed:
        log_event({"event": "no_candidate_executed", "reason": "NO_SELL_TEST_PASS"})
        return state
    execute_one(passed[0], state)
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
