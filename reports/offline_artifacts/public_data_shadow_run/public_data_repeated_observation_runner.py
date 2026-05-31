from urllib import request,parse
import json,time,datetime,uuid,hashlib
from pathlib import Path
BASE_URL="https://api.upbit.com"; WINDOWS=3; CYCLES=56; RPC=3; WLIM=168; TLIM=504; TO=10
OUT=Path(__file__).resolve().parent; DIG=OUT/"repeated_observation_digests"; RJ=OUT/"repeated_observation_result_v1.json"; RM=OUT/"repeated_observation_result_v1.md"
EPS=[{"n":"market_all","p":"/v1/market/all","q":{"isDetails":"false"}},{"n":"ticker_krw_btc","p":"/v1/ticker","q":{"markets":"KRW-BTC"}},{"n":"orderbook_krw_btc","p":"/v1/orderbook","q":{"markets":"KRW-BTC"}}]
FORB={"/v1/accounts","/v1/orders","/v1/order","/v1/withdraws","/v1/deposits","/v1/transfers"}
NON_AUTH='?쏷his document does not authorize live trading, authenticated real shadow mode execution, Upbit private API access, credential use, scheduler activation, parser execution, fixture creation, WF08 transition, runtime wiring, implementation, or production-readiness claims.??'; SCORE='?쏱ublic-data evidence score measures public quotation observation evidence, blocker preservation, and safety coverage only; it does not authorize credential use, authenticated shadow execution, scheduler activation, live trading, WF08, or production readiness.??'
def u(p,q): e=parse.urlencode(q); return f"{BASE_URL}{p}?{e}" if e else f"{BASE_URL}{p}"
def ss(x):
  if isinstance(x,list): f=x[0] if x else {}; return {"root":"list","length":len(x),"first_item_keys":sorted(f.keys()) if isinstance(f,dict) else []}
  if isinstance(x,dict): return {"root":"dict","keys":sorted(x.keys())}
  return {"root":type(x).__name__}
def dig(w,c,s,urls):
  d=DIG/f"window_{w:03d}"; d.mkdir(parents=True,exist_ok=True); t=datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()
  h=hashlib.sha256(json.dumps({"window":w,"cycle":c,"statuses":s},sort_keys=True).encode()).hexdigest()
  lines=[f"# REPEATED OBSERVATION DIGEST WINDOW {w:03d} CYCLE {c:03d}","",f"- window: {w}",f"- cycle: {c}",f"- generated_at_utc: {t}",f"- digest_id: {uuid.uuid4()}",f"- digest_sha256: {h}","- endpoints_attempted:"]+[f"  - {x}" for x in urls]+[f"- response_statuses: {s}","- hypothetical_submission_state: STUBBED_NOT_SENT","",NON_AUTH]
  (d/f"cycle_{c:03d}.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
def run():
  r={"executed_at_utc":datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),"windows_requested":WINDOWS,"windows_completed":0,"cycles_per_window":CYCLES,"total_cycles_completed":0,"total_request_count":0,"response_statuses":[],"endpoints_attempted":[],"methods_used":[],"auth_header_sent":False,"credential_use_in_this_run":False,"env_access_in_this_run":False,"scheduler_use_in_this_run":False,"private_account_endpoint_called":False,"order_endpoint_called":False,"withdraw_transfer_endpoint_called":False,"live_order_count":0,"shadow_order_count":0,"stubbed_not_sent_count":0,"digest_count":0,"window_summaries":[],"schema_samples":[],"run_result":"FAILED","stop_reason":""}
  for w in range(1,WINDOWS+1):
    wc=0; ws=[]
    for c in range(1,CYCLES+1):
      cs=[]; urls=[]
      for ep in EPS[:RPC]:
        if ep["p"] in FORB: r["run_result"]="BLOCKED"; r["stop_reason"]=f"FORBIDDEN_ENDPOINT:{ep['p']}"; return r
        if wc>=WLIM or r["total_request_count"]>=TLIM: r["run_result"]="BLOCKED"; r["stop_reason"]="REQUEST_LIMIT_REACHED"; return r
        url=u(ep["p"],ep["q"]); req=request.Request(url=url,method="GET")
        with request.urlopen(req,timeout=TO) as resp: sc=int(resp.status); payload=json.loads(resp.read().decode("utf-8"))
        if c==1: r["schema_samples"].append({"window":w,"endpoint":ep["n"],"schema":ss(payload)})
        if sc in (401,403): r["run_result"]="BLOCKED"; r["stop_reason"]=f"AUTH_REQUIRED_STATUS:{sc}"; return r
        r["response_statuses"].append(sc); r["endpoints_attempted"].append(url); r["methods_used"].append("GET"); r["total_request_count"]+=1; wc+=1; cs.append(sc); urls.append(url); ws.append(sc)
      dig(w,c,cs,urls); r["digest_count"]+=1; r["stubbed_not_sent_count"]+=1; r["total_cycles_completed"]+=1; time.sleep(0.03)
    r["window_summaries"].append({"window":w,"requests":wc,"unique_statuses":sorted(set(ws))}); r["windows_completed"]+=1
  r["run_result"]="SUCCESS"; return r
r=run(); RJ.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding="utf-8")
RM.write_text("\n".join(["# REPEATED PUBLIC DATA OBSERVATION RESULT V1","",f"- windows_requested: {r['windows_requested']}",f"- windows_completed: {r['windows_completed']}",f"- cycles_per_window: {r['cycles_per_window']}",f"- total_cycles_completed: {r['total_cycles_completed']}",f"- total_request_count: {r['total_request_count']}",f"- response_statuses: {r['response_statuses']}",f"- auth_header_sent: {str(r['auth_header_sent']).lower()}",f"- credential_use_in_this_run: {str(r['credential_use_in_this_run']).lower()}",f"- env_access_in_this_run: {str(r['env_access_in_this_run']).lower()}",f"- scheduler_use_in_this_run: {str(r['scheduler_use_in_this_run']).lower()}",f"- private_account_endpoint_called: {str(r['private_account_endpoint_called']).lower()}",f"- order_endpoint_called: {str(r['order_endpoint_called']).lower()}",f"- withdraw_transfer_endpoint_called: {str(r['withdraw_transfer_endpoint_called']).lower()}",f"- live_order_count: {r['live_order_count']}",f"- shadow_order_count: {r['shadow_order_count']}",f"- stubbed_not_sent_count: {r['stubbed_not_sent_count']}",f"- digest_count: {r['digest_count']}",f"- run_result: {r['run_result']}",f"- stop_reason: {r['stop_reason']}","",NON_AUTH,"",SCORE])+"\n",encoding="utf-8")
