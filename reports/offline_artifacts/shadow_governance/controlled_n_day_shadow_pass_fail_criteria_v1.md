# CONTROLLED N-DAY SHADOW PASS FAIL CRITERIA V1

## Scope

- default N: 14 days (human may change only through signed approval)
- this document defines criteria only and does not execute shadow mode

## Pass Conditions

- zero order submission
- zero live order
- zero unresolved RECON drift
- zero hash-chain break
- alert SLA synthetic evidence pass
- KILL synthetic evidence pass
- no scheduler surprises
- daily digest produced each day
- daily human review completed each day
- no hypothetical overtrade runaway
- no score interpreted as profit guarantee
- no transition to WF08 without human review

## Credential/API Safety Condition

- zero credential read unless separately authorized for non-submission data feed and explicitly blocked from order endpoints

## Fail Conditions

- any forbidden state (SUBMITTED, LIVE_ORDER, EXCHANGE_CONNECTED, CREDENTIAL_READ)
- any unresolved critical alert beyond SLA
- any day missing digest or human review
- any unauthorized scheduler activation or endpoint expansion

## Allowed Pass Result Label Only

SHADOW_RUN_EVIDENCE_READY_FOR_WF08_REVIEW

## Explicit Limit

Pass result does not mean live authorized.

Shadow scope score measures scope, evidence, governance, and blocker completeness only; it does not authorize shadow execution, live trading, Upbit API use, credential use, runtime activation, scheduler activation, WF08, or production readiness.

This document does not authorize live trading, shadow mode execution, Upbit API access, credential use, scheduler activation, parser execution, fixture creation, WF08 transition, runtime wiring, implementation, or production-readiness claims.

This document does not authorize live trading, shadow mode, Upbit API access, credential use, scheduler activation, parser execution, fixture creation, WF08 transition, runtime wiring, implementation, or production-readiness claims.

