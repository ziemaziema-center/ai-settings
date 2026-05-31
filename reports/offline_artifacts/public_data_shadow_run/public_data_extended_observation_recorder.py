from urllib import request, parse
import json
import time
import datetime
from pathlib import Path
import hashlib
import uuid

BASE_URL = "https://api.upbit.com"
CYCLES_REQUESTED = 56
REQUESTS_PER_CYCLE = 3
TOTAL_REQUEST_LIMIT = 168
TIMEOUT_SECONDS = 10

OUTPUT_DIR = Path(__file__).resolve().parent
DIGEST_DIR = OUTPUT_DIR / "extended_daily_digests"
RESULT_JSON = OUTPUT_DIR / "public_data_extended_observation_result_v1.json"
RESULT_MD = OUTPUT_DIR / "public_data_extended_observation_result_v1.md"

ALLOWED_ENDPOINTS = [
    {"name": "market_all", "path": "/v1/market/all", "query": {"isDetails": "false"}},
    {"name": "ticker_krw_btc", "path": "/v1/ticker", "query": {"markets": "KRW-BTC"}},
    {"name": "orderbook_krw_btc", "path": "/v1/orderbook", "query": {"markets": "KRW-BTC"}},
]
FORBIDDEN_ENDPOINTS = {
    "/v1/accounts", "/v1/orders", "/v1/order", "/v1/withdraws", "/v1/deposits", "/v1/transfers"
}

NON_AUTH = "?쏷his document does not authorize live trading, authenticated real shadow mode execution, Upbit private API access, credential use, scheduler activation, parser execution, fixture creation, WF08 transition, runtime wiring, implementation, or production-readiness claims.??"
SCORE_SENTENCE = "?쏱ublic-data evidence score measures public quotation observation evidence, blocker preservation, and safety coverage only; it does not authorize credential use, authenticated shadow execution, scheduler activation, live trading, WF08, or production readiness.??"


def build_url(path_value: str, query: dict) -> str:
    encoded = parse.urlencode(query)
    return f"{BASE_URL}{path_value}?{encoded}" if encoded else f"{BASE_URL}{path_value}"


def write_digest(cycle: int, statuses: list, endpoints: list) -> None:
    DIGEST_DIR.mkdir(parents=True, exist_ok=True)
    generated_at = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()
    digest_id = str(uuid.uuid4())
    core = {
        "cycle": cycle,
        "generated_at_utc": generated_at,
        "statuses": statuses,
        "hypothetical_submission_state": "STUBBED_NOT_SENT",
    }
    digest_sha = hashlib.sha256(json.dumps(core, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
    lines = [
        f"# EXTENDED PUBLIC DATA OBSERVATION DIGEST CYCLE {cycle:03d}",
        "",
        f"- cycle: {cycle}",
        f"- generated_at_utc: {generated_at}",
        f"- digest_id: {digest_id}",
        f"- digest_sha256: {digest_sha}",
        "- endpoints_attempted:",
    ]
    lines.extend([f"  - {u}" for u in endpoints])
    lines.append(f"- response_statuses: {statuses}")
    lines.append("- hypothetical_submission_state: STUBBED_NOT_SENT")
    lines.append("")
    lines.append(NON_AUTH)
    (DIGEST_DIR / f"cycle_{cycle:03d}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run() -> dict:
    result = {
        "executed_at_utc": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
        "cycles_requested": CYCLES_REQUESTED,
        "cycles_completed": 0,
        "total_request_count": 0,
        "endpoints_attempted": [],
        "methods_used": [],
        "auth_header_sent": False,
        "credential_use_in_this_run": False,
        "env_access_in_this_run": False,
        "scheduler_use_in_this_run": False,
        "private_account_endpoint_called": False,
        "order_endpoint_called": False,
        "withdraw_transfer_endpoint_called": False,
        "live_order_count": 0,
        "shadow_order_count": 0,
        "stubbed_not_sent_count": 0,
        "response_statuses": [],
        "daily_digest_count": 0,
        "local_output_only": True,
        "run_result": "FAILED",
        "stop_reason": "",
    }

    if CYCLES_REQUESTED > 56:
        result["run_result"] = "BLOCKED"
        result["stop_reason"] = "CYCLE_LIMIT_EXCEEDED"
        return result

    for cycle in range(1, CYCLES_REQUESTED + 1):
        cycle_statuses = []
        cycle_urls = []
        for endpoint in ALLOWED_ENDPOINTS[:REQUESTS_PER_CYCLE]:
            if endpoint["path"] in FORBIDDEN_ENDPOINTS:
                result["run_result"] = "BLOCKED"
                result["stop_reason"] = f"FORBIDDEN_ENDPOINT:{endpoint['path']}"
                return result
            if result["total_request_count"] >= TOTAL_REQUEST_LIMIT:
                result["run_result"] = "BLOCKED"
                result["stop_reason"] = "TOTAL_REQUEST_LIMIT_REACHED"
                return result

            url = build_url(endpoint["path"], endpoint["query"])
            req = request.Request(url=url, method="GET")
            try:
                with request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
                    status_code = int(resp.status)
                    _ = resp.read()
                result["response_statuses"].append(status_code)
                result["endpoints_attempted"].append(url)
                result["methods_used"].append("GET")
                result["total_request_count"] += 1
                cycle_statuses.append(status_code)
                cycle_urls.append(url)
                if status_code in (401, 403):
                    result["run_result"] = "BLOCKED"
                    result["stop_reason"] = f"AUTH_REQUIRED_STATUS:{status_code}"
                    return result
            except Exception as exc:  # noqa: BLE001
                result["response_statuses"].append("EXCEPTION")
                result["endpoints_attempted"].append(url)
                result["methods_used"].append("GET")
                result["total_request_count"] += 1
                result["run_result"] = "FAILED"
                result["stop_reason"] = f"REQUEST_EXCEPTION:{type(exc).__name__}"
                return result

        write_digest(cycle, cycle_statuses, cycle_urls)
        result["daily_digest_count"] += 1
        result["stubbed_not_sent_count"] += 1
        result["cycles_completed"] += 1
        time.sleep(0.03)

    result["run_result"] = "SUCCESS"
    return result


def write_results(result: dict) -> None:
    RESULT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# PUBLIC DATA EXTENDED OBSERVATION RESULT V1",
        "",
        f"- cycles_requested: {result['cycles_requested']}",
        f"- cycles_completed: {result['cycles_completed']}",
        f"- total_request_count: {result['total_request_count']}",
        f"- auth_header_sent: {str(result['auth_header_sent']).lower()}",
        f"- credential_use_in_this_run: {str(result['credential_use_in_this_run']).lower()}",
        f"- env_access_in_this_run: {str(result['env_access_in_this_run']).lower()}",
        f"- scheduler_use_in_this_run: {str(result['scheduler_use_in_this_run']).lower()}",
        f"- private_account_endpoint_called: {str(result['private_account_endpoint_called']).lower()}",
        f"- order_endpoint_called: {str(result['order_endpoint_called']).lower()}",
        f"- withdraw_transfer_endpoint_called: {str(result['withdraw_transfer_endpoint_called']).lower()}",
        f"- live_order_count: {result['live_order_count']}",
        f"- shadow_order_count: {result['shadow_order_count']}",
        f"- stubbed_not_sent_count: {result['stubbed_not_sent_count']}",
        f"- daily_digest_count: {result['daily_digest_count']}",
        f"- response_statuses: {result['response_statuses']}",
        f"- run_result: {result['run_result']}",
        f"- stop_reason: {result['stop_reason']}",
        "",
        NON_AUTH,
        "",
        SCORE_SENTENCE,
    ]
    RESULT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    result = run()
    write_results(result)


if __name__ == "__main__":
    main()
