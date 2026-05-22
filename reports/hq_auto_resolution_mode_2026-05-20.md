# HQ Auto Resolution Mode - 2026-05-20

## Operating Rule

When a blocker appears, classify it before stopping permanently.

- Safety blocker: keep stopped.
- Technical blocker: call HQ/agents, patch narrowly, validate, deploy, retry the safe precheck once.
- Market-state blocker: keep stopped until state changes.

## Applied To DOT

- Blocker: `LIVE_SELL_ORDERBOOK_STALE`.
- HQ classification: legitimate safety block plus telemetry gap.
- Patch allowed: diagnostics and clock-skew detection only.
- Patch forbidden: stale TTL increase, freshness bypass, market order, retry loop, scheduler activation.

## Patch

- Added orderbook diagnostics to stale/clock-skew blocked responses.
- Added explicit `LIVE_SELL_ORDERBOOK_CLOCK_SKEW`.
- Kept authoritative helper-side orderbook reread.
- Kept stale threshold at `10000 ms`.

## Validation

- helper live sell endpoint tests: `PASS`
- no-journal tests: `PASS`
- portfolio tests: `PASS`
- news tests: `PASS`
- strategy tests: `PASS`
- WF05 regression: `PASS 12/12`
- strategy validation: `PASS loops=3`
- remote helper smoke: `PASS`

## Runtime

- helper-only deployment: `PASS`
- backup: `/home/ubuntu/kbia_backups/upbit-helper-live-sell-20260520_171539`
- rollback image: `upbit-helper:rollback-live-sell-20260520_171539`
- workflow/scheduler activation: `false`
