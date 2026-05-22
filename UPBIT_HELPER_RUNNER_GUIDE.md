# Upbit Helper Runner Guide

## Purpose
Run a separate `upbit-helper` container that owns Upbit JWT signing and returns sanitized telemetry only. n8n must call this helper over HTTP and must not generate JWTs in Code nodes.

## Files
- `upbit-helper/app/main.py`
- `upbit-helper/requirements.txt`
- `upbit-helper/Dockerfile`

## Build
```bash
docker build -t upbit-helper:local ./upbit-helper
```

## Create A Shared Docker Network
Use an existing n8n network if one is already present. Otherwise create a small private network:

```bash
docker network create kbia-internal
docker network connect kbia-internal n8n
```

Do not modify `n8n_data` and do not modify `reel-service`.

## Run Helper
Enter secrets only in the shell environment. Do not write values to files.

```bash
read -rsp 'UPBIT_ACCESS_KEY: ' UPBIT_ACCESS_KEY; echo
read -rsp 'UPBIT_SECRET_KEY: ' UPBIT_SECRET_KEY; echo
export UPBIT_ACCESS_KEY UPBIT_SECRET_KEY
```

```bash
docker run -d \
  --name upbit-helper \
  --restart unless-stopped \
  --network kbia-internal \
  -p 127.0.0.1:8010:8010 \
  -e UPBIT_ACCESS_KEY \
  -e UPBIT_SECRET_KEY \
  upbit-helper:local
```

## Verify Without Printing Secrets
```bash
curl -sS http://127.0.0.1:8010/health
docker exec n8n sh -lc 'node -e "fetch(\"http://upbit-helper:8010/health\").then(r=>r.json()).then(v=>console.log(JSON.stringify(v)))"'
```

Expected health:

```json
{"ok":true,"service":"upbit-helper"}
```

## n8n Helper Base URL
WF03 uses:

```text
http://upbit-helper:8010
```

Only override this if n8n is not on the same Docker network.

## Allowed Helper Endpoints
- `GET /health`
- `POST /upbit/accounts/telemetry`
- `POST /upbit/open-orders/telemetry`

The helper must never return JWT, Authorization headers, balances, or raw orders.
