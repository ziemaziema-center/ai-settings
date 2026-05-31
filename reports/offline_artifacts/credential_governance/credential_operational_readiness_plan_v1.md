# CREDENTIAL OPERATIONAL READINESS PLAN V1

## Future Requirements

- Upbit key permission must be READ + TRADE only
- withdrawal permission forbidden
- transfer permission forbidden
- IP allowlist mandatory and all-IP keys forbidden
- no repo storage
- no .env storage
- no plaintext file storage
- Windows Credential Manager or OS secret manager only
- defined rotation policy and cadence
- incident-triggered revocation playbook
- separate watchdog key only if separately approved
- human checklist required before any credential use

## Human Checklist Before Credential Use (Future)

1. key scope verified (READ+TRADE only)
2. withdraw/transfer toggles confirmed disabled
3. IP allowlist confirmed
4. secret storage mechanism audited
5. rotation schedule set
6. revocation path tested
7. approver and timestamp logged

No credential was created, read, or used in this run.

Readiness score measures documentation, governance, and validation completeness only; it does not authorize trading, does not predict profit, and does not indicate runtime, shadow, live, or WF08 readiness.

This document does not authorize live trading, shadow mode, Upbit API access, credential use, scheduler activation, parser execution, fixture creation, WF08 transition, runtime wiring, implementation, or production-readiness claims.
