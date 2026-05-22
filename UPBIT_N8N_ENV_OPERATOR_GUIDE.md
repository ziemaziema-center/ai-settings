# Upbit n8n Environment Operator Guide

## Purpose
Safely set `UPBIT_ACCESS_KEY` and `UPBIT_SECRET_KEY` for the current n8n Docker deployment and validate only the read-only Upbit accounts flow in WF03.

## Non-Negotiable Rules
- Do not paste secrets into chat, docs, workflow JSON, git, logs, screenshots, or tickets.
- Do not put secret values into `.env`, Compose files, markdown files, or scripts.
- Do not call order, cancel, reorder, or withdrawal endpoints.
- Do not modify `live_order_enabled=false`.
- Do not activate cron/live execution.
- Confirm success only from sanitized `accounts_telemetry`.

## Current Local Finding
This planning folder does not contain the live n8n Docker Compose file. Run the commands below on the server that hosts n8n.

## Step 1 - Identify the n8n container

```bash
docker ps --format 'table {{.ID}}\t{{.Names}}\t{{.Image}}\t{{.Mounts}}' | grep -i n8n
```

Set the container name without printing env values:

```bash
export N8N_CONTAINER='<container_name_from_previous_command>'
```

Check whether the container was created by Docker Compose:

```bash
docker inspect -f '{{ index .Config.Labels "com.docker.compose.project.working_dir" }}' "$N8N_CONTAINER"
```

If this prints a directory, use Method A. If it prints `<no value>` or blank, use Method B.

## Method A - Docker Compose Deployment

Go to the Compose working directory printed above:

```bash
cd '<compose_working_dir>'
```

Backup Compose config without secrets:

```bash
cp docker-compose.yml "docker-compose.yml.backup.$(date +%Y%m%d_%H%M%S)"
```

Add only variable references to the n8n service. Do not write actual secret values.

```yaml
services:
  n8n:
    environment:
      - UPBIT_ACCESS_KEY=${UPBIT_ACCESS_KEY:?UPBIT_ACCESS_KEY_missing}
      - UPBIT_SECRET_KEY=${UPBIT_SECRET_KEY:?UPBIT_SECRET_KEY_missing}
```

If the `environment:` block already exists, append only the two lines above.

Enter secret values silently in the terminal:

```bash
read -rsp 'UPBIT_ACCESS_KEY: ' UPBIT_ACCESS_KEY; echo
read -rsp 'UPBIT_SECRET_KEY: ' UPBIT_SECRET_KEY; echo
export UPBIT_ACCESS_KEY UPBIT_SECRET_KEY
```

Recreate only the n8n container. This preserves Docker named volumes and bind mounts.

```bash
docker compose up -d --no-deps --force-recreate n8n
```

If the service name is not `n8n`, list service names and use the matching one:

```bash
docker compose config --services
```

## Method B - Standalone Docker Container

Use this only if the container is not Compose-managed.

Record the image and mount summary without secrets:

```bash
docker inspect -f 'IMAGE={{.Config.Image}}' "$N8N_CONTAINER"
docker inspect -f 'MOUNTS={{range .Mounts}}{{printf "%s:%s " .Source .Destination}}{{end}}' "$N8N_CONTAINER"
```

Preferred action: migrate this container to a Compose file that preserves the same image, ports, and mounts. Add only variable references as shown in Method A. Do not use `docker commit`.

If you must recreate manually, use the original run command from your deployment notes and add:

```bash
-e UPBIT_ACCESS_KEY -e UPBIT_SECRET_KEY
```

Then enter values silently before running it:

```bash
read -rsp 'UPBIT_ACCESS_KEY: ' UPBIT_ACCESS_KEY; echo
read -rsp 'UPBIT_SECRET_KEY: ' UPBIT_SECRET_KEY; echo
export UPBIT_ACCESS_KEY UPBIT_SECRET_KEY
```

Do not remove the old container until the new container is healthy and the same volume is mounted.

## Step 2 - Verify env vars without printing values

```bash
docker exec "$N8N_CONTAINER" sh -lc 'node -e "console.log(JSON.stringify({UPBIT_ACCESS_KEY: Boolean(process.env.UPBIT_ACCESS_KEY), UPBIT_SECRET_KEY: Boolean(process.env.UPBIT_SECRET_KEY)}))"'
```

Expected:

```json
{"UPBIT_ACCESS_KEY":true,"UPBIT_SECRET_KEY":true}
```

Do not run `printenv`, `env`, `docker inspect` env dumps, or any command that displays actual values.

## Step 3 - Import or update WF03

Use the n8n UI:

1. Open n8n.
2. Import or update `workflows/03_WF_PreCheck_Engine.json`.
3. Keep the workflow inactive unless you intentionally need a manual test.
4. Confirm there are no active schedules.
5. Confirm `Set Upbit Trade Request` still contains `live_order_enabled: false`.

## Step 4 - Run read-only accounts validation

Manual execution only:

1. Open `KBIA_03_WF_Upbit_PreCheck_Engine`.
2. Click `Execute workflow`.
3. Inspect only the final `Precheck STOP Payload` or `Validate Upbit Safety Conditions` output.
4. Confirm `accounts_telemetry` only:
   - `timestamp`
   - `endpoint`
   - `http_status`
   - `success`
   - `account_count`
   - `currencies_present`
   - `error_name`
   - `error_message`
   - `remaining_req`

Expected pass shape:

```json
{
  "accounts_telemetry": {
    "endpoint": "https://api.upbit.com/v1/accounts",
    "http_status": 200,
    "success": true,
    "account_count": 1,
    "currencies_present": ["KRW"],
    "error_name": null,
    "error_message": "",
    "remaining_req": "group=default; min=1800; sec=29"
  },
  "precheck_status": "stop",
  "precheck_passed": false,
  "execution_allowed": false
}
```

`account_count`, `currencies_present`, and `remaining_req` may differ. Do not copy raw account balances.

## Stop Codes

| stop_code | Meaning | Action |
|-----------|---------|--------|
| `CREDENTIAL_MISSING` | n8n process cannot see one or both env vars | Recheck Docker env injection and restart |
| `AUTH_FAILED` | Upbit rejected JWT/key/permission/IP allowlist | Check Upbit key permission and allowed IP |
| `RATE_LIMITED` | Upbit returned 429 or 418 | Stop immediately and wait |

## Success Criteria
- Env visibility check returns both booleans as true.
- WF03 manual execution returns `accounts_telemetry.success=true`.
- `http_status=200`.
- `currencies_present` contains only currency codes, not balances.
- `precheck_status` remains `stop`.
- `live_order_enabled` remains false.
