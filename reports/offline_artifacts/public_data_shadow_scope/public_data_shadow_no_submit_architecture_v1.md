# PUBLIC DATA SHADOW NO SUBMIT ARCHITECTURE V1

## Conceptual Architecture

PUBLIC_DATA_SOURCE -> MARKET_DATA_OBSERVER -> SIGNAL_OBSERVER -> PTRC_OBSERVER -> IDEM_STUB -> OSM_RECORDER -> RECON_SIMULATED_OBSERVER -> KILL_OBSERVER -> ALERT_OBSERVER -> LOCAL_SHADOW_RECORDER -> DAILY_DIGEST

## Invariants

- no credential
- no private endpoint
- no order endpoint
- no exchange submission
- no live order
- no shadow order against exchange
- all hypothetical orders become STUBBED_NOT_SENT
- manual execution only until scheduler separately approved
- PERSISTED BEFORE SUBMITTED preserved by making SUBMITTED impossible
- KILL stops recorder
- RECON drift blocks new candidate observation
- ALERT required for critical anomalies

## Forbidden States

- SUBMITTED
- ACK_RECEIVED
- OPEN
- FILLED
- PARTIAL
- LIVE_ORDER
- SHADOW_ORDER
- PRIVATE_ENDPOINT_CONNECTED

Public-data shadow scope score measures review, scope, blocker clarity, and safety coverage only; it does not authorize real shadow execution, Upbit API access, credential use, scheduler activation, live trading, WF08, or production readiness.

This document does not authorize live trading, real shadow mode execution, Upbit API access, credential use, scheduler activation, parser execution, fixture creation, WF08 transition, runtime wiring, implementation, or production-readiness claims.

This document does not authorize live trading, shadow mode, Upbit API access, credential use, scheduler activation, parser execution, fixture creation, WF08 transition, runtime wiring, implementation, or production-readiness claims.
