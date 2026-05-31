from urllib import request, parse
import json
import datetime
from pathlib import Path

BASE_URL = "https://api.upbit.com"
MAX_REQUESTS = 3
TIMEOUT_SECONDS = 10

OUTPUT_DIR = Path(__file__).resolve().parent
RESULT_JSON_PATH = OUTPUT_DIR / "one_shot_public_quotation_preflight_result_v1.json"
RESULT_MD_PATH = OUTPUT_DIR / "one_shot_public_quotation_preflight_result_v1.md"

ENDPOINTS = [
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


def _is_forbidden_path(path_value: str) -> bool:
    forbidden_exact_paths = {
        "/v1/accounts",
        "/v1/orders",
        "/v1/order",
        "/v1/withdraws",
        "/v1/deposits",
        "/v1/transfers",
    }
    return path_value in forbidden_exact_paths


def _build_url(path_value: str, query: dict) -> str:
    encoded = parse.urlencode(query)
    return f"{BASE_URL}{path_value}?{encoded}" if encoded else f"{BASE_URL}{path_value}"


def _summarize_schema(payload):
    if isinstance(payload, list):
        if not payload:
            return {"root": "list", "length": 0, "first_item_keys": []}
        first = payload[0]
        if isinstance(first, dict):
            return {"root": "list", "length": len(payload), "first_item_keys": sorted(list(first.keys()))}
        return {"root": "list", "length": len(payload), "first_item_type": type(first).__name__}
    if isinstance(payload, dict):
        return {"root": "dict", "keys": sorted(list(payload.keys()))}
    return {"root": type(payload).__name__}


def run_preflight() -> dict:
    executed_at_utc = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

    result = {
        "executed_at_utc": executed_at_utc,
        "request_count": 0,
        "endpoints_attempted": [],
        "methods_used": [],
        "auth_header_sent": False,
        "credential_read_attempted": False,
        "env_access_attempted": False,
        "private_endpoint_called": False,
        "order_endpoint_called": False,
        "scheduler_used": False,
        "response_statuses": [],
        "response_schema_summary": [],
        "local_output_only": True,
        "preflight_result": "FAILED",
        "stop_reason": "",
    }

    if len(ENDPOINTS) > MAX_REQUESTS:
        result["preflight_result"] = "BLOCKED"
        result["stop_reason"] = "REQUEST_SET_EXCEEDS_MAX"
        return result

    for endpoint in ENDPOINTS:
        path_value = endpoint["path"]
        if _is_forbidden_path(path_value):
            result["preflight_result"] = "BLOCKED"
            result["stop_reason"] = f"FORBIDDEN_ENDPOINT_PATH:{path_value}"
            return result

        url = _build_url(path_value, endpoint["query"])
        req = request.Request(url=url, method="GET")

        result["request_count"] += 1
        result["endpoints_attempted"].append(url)
        result["methods_used"].append("GET")

        try:
            with request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
                status_code = int(resp.status)
                body = resp.read().decode("utf-8")
                payload = json.loads(body)
                result["response_statuses"].append(status_code)
                result["response_schema_summary"].append(
                    {
                        "endpoint": endpoint["name"],
                        "status": status_code,
                        "schema": _summarize_schema(payload),
                    }
                )

                if status_code in (401, 403):
                    result["preflight_result"] = "BLOCKED"
                    result["stop_reason"] = f"AUTH_REQUIRED_STATUS:{status_code}"
                    return result
        except Exception as exc:  # noqa: BLE001
            result["response_statuses"].append("EXCEPTION")
            result["response_schema_summary"].append(
                {
                    "endpoint": endpoint["name"],
                    "status": "EXCEPTION",
                    "schema": {"error_type": type(exc).__name__},
                }
            )
            result["preflight_result"] = "FAILED"
            result["stop_reason"] = f"REQUEST_EXCEPTION:{type(exc).__name__}"
            return result

    result["preflight_result"] = "SUCCESS"
    result["stop_reason"] = ""
    return result


def write_outputs(result: dict) -> None:
    RESULT_JSON_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# ONE SHOT PUBLIC QUOTATION PREFLIGHT RESULT V1",
        "",
        f"- executed_at_utc: {result['executed_at_utc']}",
        f"- request_count: {result['request_count']}",
        "- endpoints_attempted:",
    ]
    lines.extend([f"  - {item}" for item in result["endpoints_attempted"]])
    lines.append("- methods_used:")
    lines.extend([f"  - {item}" for item in result["methods_used"]])
    lines.extend(
        [
            f"- auth_header_sent: {str(result['auth_header_sent']).lower()}",
            f"- credential_read_attempted: {str(result['credential_read_attempted']).lower()}",
            f"- env_access_attempted: {str(result['env_access_attempted']).lower()}",
            f"- private_endpoint_called: {str(result['private_endpoint_called']).lower()}",
            f"- order_endpoint_called: {str(result['order_endpoint_called']).lower()}",
            f"- scheduler_used: {str(result['scheduler_used']).lower()}",
            f"- response_statuses: {result['response_statuses']}",
            f"- local_output_only: {str(result['local_output_only']).lower()}",
            f"- preflight_result: {result['preflight_result']}",
            f"- stop_reason: {result['stop_reason']}",
            "",
            "?쏷his document does not authorize live trading, real shadow mode execution, Upbit API access beyond the approved public quotation preflight, credential use, scheduler activation, parser execution, fixture creation, WF08 transition, runtime wiring, implementation, or production-readiness claims.??",
            "",
            "?쏰ne-shot public quotation preflight score measures public endpoint evidence, blocker preservation, and safety coverage only; it does not authorize credential use, shadow execution, scheduler activation, live trading, WF08, or production readiness.??",
        ]
    )
    RESULT_MD_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    result = run_preflight()
    write_outputs(result)


if __name__ == "__main__":
    main()
