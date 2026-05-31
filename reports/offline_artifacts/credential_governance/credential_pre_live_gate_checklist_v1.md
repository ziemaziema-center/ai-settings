# CREDENTIAL PRE-LIVE GATE CHECKLIST V1

## Mandatory Checklist

- key permission READ + TRADE only
- withdrawal forbidden
- transfer forbidden
- IP allowlist mandatory
- all-IP key forbidden
- repo storage forbidden
- .env storage forbidden
- plaintext storage forbidden
- Windows Credential Manager or OS secret manager only
- no credential use in this run

## STOP Rules

- STOP if key has withdrawal permission
- STOP if IP allowlist missing
- STOP if credential appears in repo/env/plaintext

## Future Human Checklist

- approver, timestamp, key-scope evidence, rotation/revocation evidence

Pre-live score measures local dry-run, documentation, governance, and validation completeness only; it does not authorize trading, does not predict profit, and does not indicate runtime, shadow, live, or WF08 readiness.

This document does not authorize live trading, shadow mode, Upbit API access, credential use, scheduler activation, parser execution, fixture creation, WF08 transition, runtime wiring, implementation, or production-readiness claims.
