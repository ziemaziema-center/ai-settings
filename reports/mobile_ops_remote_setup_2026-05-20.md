# Mobile Remote AI Ops Stack - 2026-05-20

## Result

- Overall status: `PARTIAL_PASS_TAILSCALE_AUTH_BLOCKED`.
- EC2 host: `ubuntu@43.201.227.194`.
- Backup roots:
  - `/home/ubuntu/kbia_backups/mobile-ops-20260520_172650`
  - `/home/ubuntu/kbia_backups/mobile-ops-continue-20260520_173828`
- Remote report: `/tmp/mobile_ops_continue_20260520_173828.report`.

## Installed

- `tailscale` 1.98.2.
- `btop` 1.3.0.
- `glances` 3.4.0.3.
- `ncdu`.
- `unzip`.
- `lazydocker` 0.25.2.
- `@openai/codex` / `codex-cli` 0.130.0 under the ubuntu user path.

Already present:

- `tmux` 3.4.
- Docker 29.1.3.
- Claude Code 2.1.139.
- Caddy 2.11.2.
- Node 20.20.2 / npm 10.8.2.

## Configured

- Added `~/.kbia-mobile-ops/mobile-ops.sh`.
- Added `~/.kbia-mobile-ops/README.md`.
- Added wrappers under `~/.local/bin`:
  - `kbia-ops`
  - `kbia-codex`
  - `kbia-claude`
  - `kbia-docker-status`
  - `kbia-tail`
- Added a marked source block to `~/.bashrc`.
- Added a marked mobile tmux block to `~/.tmux.conf`.
- Created persistent tmux session `ops`.
- Enabled and started `tailscaled`.

## Runtime Validation

- Docker containers preserved and still running:
  - `upbit-helper`
  - `n8n`
  - `open-webui`
  - `reel-service`
- Docker volumes preserved:
  - `n8n_data`
  - `open-webui`
- Docker networks preserved:
  - `bridge`
  - `host`
  - `none`
  - `kbia-internal`
- Caddy config validation: `Valid configuration`.
- `upbit-helper` local health: `{"ok":true,"service":"upbit-helper"}`.
- n8n local HTTP HEAD: `HTTP/1.1 200 OK`.
- reel-service local HTTP HEAD: `HTTP/1.1 405 Method Not Allowed`, expected because the service allows GET, not HEAD.
- `tmux has-session -t ops`: pass.

## Tailscale State

- `tailscaled`: active and enabled.
- EC2 tailnet authentication: blocked pending account approval.
- EC2 Tailscale IP: unavailable until approval.
- `tailscale up` generated an authentication URL during the run; regenerate with:
  - `sudo tailscale up --ssh=false --accept-dns=false --accept-routes=false --hostname=kbia-ec2-ops`

## Safety

- No Docker containers were removed, recreated, renamed, or restarted by this mobile ops setup.
- No n8n workflow was modified or activated.
- No n8n volume or bind mount was changed.
- No Caddyfile changes were made.
- No credential rotation or secret inspection was performed.
- No trading order, sell, cancel, retry, scheduler, or workflow activation path was touched.

## Warnings

- `nginx` is not installed. The active proxy is Caddy, not nginx.
- Installing `glances` created and enabled its service; it listens on `127.0.0.1:61209`, not externally.
- Tailscale SSH was intentionally not enabled; normal OpenSSH remains the access method.
