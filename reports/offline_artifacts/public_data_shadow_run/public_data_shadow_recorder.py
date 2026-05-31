from urllib import request, parse
import json
import time
import datetime
from pathlib import Path
import hashlib
import uuid

BASE_URL = "https://api.upbit.com"
CYCLES_REQUESTED = 14
MAX_REQUESTS_PER_CYCLE = 3
TOTAL_REQUEST_LIMIT = 42
TIMEOUT_SECONDS = 10

OUTPUT_DIR = Path(__file__).resolve().parent
DIGEST_DIR = OUTPUT_DIR / "daily_digests"
RESULT_JSON = OUTPUT_DIR / "public_data_shadow_run_result_v1.json"
RESULT_MD = OUTPUT_DIR / "public_data_shadow_run_result_v1.md"

NON_AUTH_SENTENCE = "?쏷his document does not authorize live trading, real shadow mode execution beyond approved public-data recorder observation, Upbit private API access, credential use, scheduler activation, parser execution, fixture creation, WF08 transition, runtime wiring, implementation, or production-readiness claims.??"
SCORE_EVIDENCE_SENTENCE = "?쏱ublic-data shadow recorder score measures public-data observation evidence, blocker preservation, and safety coverage only; it does not authorize credential use, authenticated shadow execution, scheduler activation, live trading, WF08, or production readiness.??"

ALLOWED_ENDPOINTS = [
    {
        "name": "market_all",
        "path": "/v1/market/all",
        "query": {"isDetails": "false"},
    },
    {
        "name": "ticker_krw_btc",
        "path": "/v1/ticker",
        "query": {"markets": "KRW-BTC"},
    },
    {
        "name": "orderbook_krw_btc",
        "path": "/v1/orderbook",
        "query": {"markets": "KRW-BTC"},
    },
]

FORBIDDEN_ENDPOINTS = {
    "/v1/accounts",
    "/v1/orders",
    "/v1/order",
    "/v1/withdraws",
    "/v1/deposits",
    "/v1/transfers",
}


def build_url(path_value: str, query: dict) -> str:
    encoded = parse.urlencode(query)
    return f"{BASE_URL}{path_value}?{encoded}" if encoded else f"{BASE_URL}{path_value}"


def ensure_paths() -> None:
    DIGEST_DIR.mkdir(parents=True, exist_ok=True)


def schema_summary(payload):
    if isinstance(payload, list):
        if payload and isinstance(payload[0], dict):
            return {
                "root": "list",
                "length": len(payload),
                "first_item_keys": sorted(payload[0].keys()),
            }
        return {"root": "list", "length": len(payload)}
    if isinstance(payload, dict):
        return {"root": "dict", "keys": sorted(payload.keys())}
    return {"root": type(payload).__name__}


def write_digest(day_index: int, statuses: list, endpoint_urls: list) -> None:
    now_utc = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()
    digest_id = str(uuid.uuid4())
    content_core = {
        "day": day_index,
        "generated_at_utc": now_utc,
        "statuses": statuses,
        "endpoint_count": len(endpoint_urls),
        "hypothetical_submission_state": "STUBBED_NOT_SENT",
    }
    payload = json.dumps(content_core, ensure_ascii=False, sort_keys=True)
    payload_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest()

    lines = [
        f"# PUBLIC DATA SHADOW DAILY DIGEST DAY {day_index:02d}",
        "",
        f"- day_index: {day_index}",
        f"- generated_at_utc: {now_utc}",
        f"- digest_id: {digest_id}",
        f"- digest_sha256: {payload_hash}",
        "- endpoints_attempted:",
    ]
    lines.extend([f"  - {u}" for u in endpoint_urls])
    lines.append(f"- response_statuses: {statuses}")
    lines.append("- hypothetical_submission_state: STUBBED_NOT_SENT")
    lines.append("")
    lines.append(NON_AUTH_SENTENCE)

    digest_path = DIGEST_DIR / f"day_{day_index:02d}.md"
    digest_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run() -> dict:
    executed_at_utc = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()
    result = {
        "executed_at_utc": executed_at_utc,
        "cycles_requested": CYCLES_REQUESTED,
        "cycles_completed": 0,
        "total_request_count": 0,
        "endpoints_attempted": [],
        "methods_used": [],
        "auth_header_sent": False,
        "credential_read_attempted": False,
        "env_access_attempted": False,
        "private_endpoint_called": False,
        "order_endpoint_called": False,
        "withdraw_transfer_endpoint_called": False,
        "scheduler_used": False,
        "live_order_count": 0,
        "shadow_order_count": 0,
        "stubbed_not_sent_count": 0,
        "response_statuses": [],
        "response_schema_summary": [],
        "daily_digest_count": 0,
        "forbidden_state_count": 0,
        "local_output_only": True,
        "next_action": "HUMAN_DECISION_ON_PUBLIC_DATA_N_DAY_SHADOW_RECORDER_EVIDENCE_REVIEW",
        "run_result": "FAILED",
        "stop_reason": "",
    }

    if CYCLES_REQUESTED > 14:
        result["run_result"] = "BLOCKED"
        result["stop_reason"] = "CYCLE_LIMIT_EXCEEDED"
        return result

    per_cycle_endpoints = ALLOWED_ENDPOINTS[:MAX_REQUESTS_PER_CYCLE]

    for cycle in range(1, CYCLES_REQUESTED + 1):
        cycle_statuses = []
        cycle_urls = []
        for endpoint in per_cycle_endpoints:
            path_value = endpoint["path"]
            if path_value in FORBIDDEN_ENDPOINTS:
                result["forbidden_state_count"] += 1
                result["run_result"] = "BLOCKED"
                result["stop_reason"] = f"FORBIDDEN_ENDPOINT:{path_value}"
                return result

            if result["total_request_count"] >= TOTAL_REQUEST_LIMIT:
                result["run_result"] = "BLOCKED"
                result["stop_reason"] = "TOTAL_REQUEST_LIMIT_REACHED"
                return result

            url = build_url(path_value, endpoint["query"])
            req = request.Request(url=url, method="GET")
            try:
                with request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
                    status_code = int(resp.status)
                    payload = json.loads(resp.read().decode("utf-8"))
                    result["total_request_count"] += 1
                    result["endpoints_attempted"].append(url)
                    result["methods_used"].append("GET")
                    result["response_statuses"].append(status_code)
                    result["response_schema_summary"].append(
                        {
                            "cycle": cycle,
                            "endpoint": endpoint["name"],
                            "status": status_code,
                            "schema": schema_summary(payload),
                        }
                    )
                    cycle_statuses.append(status_code)
                    cycle_urls.append(url)
                    if status_code in (401, 403):
                        result["run_result"] = "BLOCKED"
                        result["stop_reason"] = f"AUTH_REQUIRED_STATUS:{status_code}"
                        return result
            except Exception as exc:  # noqa: BLE001
                result["total_request_count"] += 1
                result["endpoints_attempted"].append(url)
                result["methods_used"].append("GET")
                result["response_statuses"].append("EXCEPTION")
                result["response_schema_summary"].append(
                    {
                        "cycle": cycle,
                        "endpoint": endpoint["name"],
                        "status": "EXCEPTION",
                        "schema": {"error_type": type(exc).__name__},
                    }
                )
                result["run_result"] = "FAILED"
                result["stop_reason"] = f"REQUEST_EXCEPTION:{type(exc).__name__}"
                return result

        result["cycles_completed"] += 1
        result["stubbed_not_sent_count"] += 1
        write_digest(cycle, cycle_statuses, cycle_urls)
        result["daily_digest_count"] += 1
        time.sleep(0.05)

    result["run_result"] = "SUCCESS"
    return result


def write_outputs(result: dict) -> None:
    RESULT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# PUBLIC DATA SHADOW RUN RESULT V1",
        "",
        f"- executed_at_utc: {result['executed_at_utc']}",
        f"- cycles_requested: {result['cycles_requested']}",
        f"- cycles_completed: {result['cycles_completed']}",
        f"- daily_digest_count: {result['daily_digest_count']}",
        f"- total_request_count: {result['total_request_count']}",
        f"- auth_header_sent: {str(result['auth_header_sent']).lower()}",
        f"- credential_read_attempted: {str(result['credential_read_attempted']).lower()}",
        f"- env_access_attempted: {str(result['env_access_attempted']).lower()}",
        f"- private_endpoint_called: {str(result['private_endpoint_called']).lower()}",
        f"- order_endpoint_called: {str(result['order_endpoint_called']).lower()}",
        f"- withdraw_transfer_endpoint_called: {str(result['withdraw_transfer_endpoint_called']).lower()}",
        f"- scheduler_used: {str(result['scheduler_used']).lower()}",
        f"- live_order_count: {result['live_order_count']}",
        f"- shadow_order_count: {result['shadow_order_count']}",
        f"- stubbed_not_sent_count: {result['stubbed_not_sent_count']}",
        f"- response_statuses: {result['response_statuses']}",
        f"- forbidden_state_count: {result['forbidden_state_count']}",
        f"- local_output_only: {str(result['local_output_only']).lower()}",
        f"- next_action: {result['next_action']}",
        f"- run_result: {result['run_result']}",
        f"- stop_reason: {result['stop_reason']}",
        "",
        NON_AUTH_SENTENCE,
        "",
        SCORE_EVIDENCE_SENTENCE,
    ]
    RESULT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    ensure_paths()
    output = run()
    write_outputs(output)


if __name__ == "__main__":
    main()
