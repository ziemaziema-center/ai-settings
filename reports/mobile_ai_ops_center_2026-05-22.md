# Mobile AI Ops Center - 2026-05-22

## Result

- Status: `PASS`
- EC2 Tailscale IP: `100.87.224.86`
- Main entrypoint from iPhone: `mobile`
- Full tmux workspace: `ai-ops`
- Backup paths:
  - `/home/ubuntu/kbia_backups/mobile-ai-ops-center-20260522_142722`
  - `/home/ubuntu/kbia_backups/mobile-ai-ops-center-20260522_142745`
  - `/home/ubuntu/kbia_backups/mobile-ai-ops-center-20260522_142814`

## Installed / Added

Commands added under `/home/ubuntu/.local/bin`:

- `mobile`
- `center`
- `kbia-ai-ops-center`
- `kbia-status`
- `kbia-auto-watch`
- `auto-watch`
- `kbia-help`
- `n8n-log`
- `reel-log`

Docs added on EC2:

- `/home/ubuntu/.kbia-mobile-ops/AI_OPS_CENTER.md`

## tmux Layout

Created tmux session `ai-ops` with 8 windows:

- `menu`: iPhone-friendly command menu
- `codex`: Codex launch shell
- `claude`: Claude Code launch shell
- `docker`: Docker status / lazydocker entrypoint
- `n8n-log`: n8n log follow
- `auto`: automation state watcher
- `system`: system monitor entrypoint
- `shell`: status and normal shell

## Current Runtime State Observed

- `kbia-full-auto`: running.
- `cycle_count`: `79`.
- `active_market`: `null`.
- Completed markets: `KRW-DOT`, `KRW-ETC`.
- Open orders for watched markets: all `0`.
- Remaining blocked markets:
  - `KRW-FCT2`: `LIVE_SELL_ORDERBOOK_STALE|LIVE_SELL_SPREAD_TOO_WIDE`
  - `KRW-ALGO`: `LIVE_SELL_SPREAD_TOO_WIDE`
  - `KRW-DOGE`: `LIVE_SELL_SPREAD_TOO_WIDE`

## Preserved Services

Docker services remained running:

- `reel-service`
- `upbit-helper`
- `n8n`
- `open-webui`

No containers were removed, recreated, or restarted by this task.

## Use From iPhone

```bash
ssh ubuntu@100.87.224.86
mobile
```

Fast path:

```bash
ssh ubuntu@100.87.224.86
center
```

Useful direct commands:

```bash
kbia-status
codexops
claudeops
kbia-docker-status
lzd
n8n-log
reel-log
auto-watch
full-auto
```

## Safety

- No live order.
- No live sell.
- No cancel.
- No retry/reorder loop.
- No n8n workflow activation.
- No scheduler mutation.
- No helper mutation.
- No Docker mutation.
- No secret/JWT/Auth header/raw payload/full UUID exposure.
