# REAL SHADOW CREDENTIAL DATA ACCESS GATE REVIEW V1

## Scope Boundary

- no credential use in this run
- no credential read in this run

## Future Credential Principles

- future credential should be READ-only for data access if possible
- if trade permission is required later, application-layer order submission remains hard blocked
- withdrawal permission is forbidden
- transfer permission is forbidden

## Mandatory Storage and Access Rules

- IP allowlist mandatory
- no all-IP keys
- no repository storage
- no .env storage
- no plaintext storage
- Windows Credential Manager or OS secret manager only

## Human Key Inspection Checklist

- human approver name and timestamp
- key permission snapshot
- withdrawal=false, transfer=false confirmation
- IP allowlist evidence
- storage location evidence (secret manager only)
- revocation/rotation plan evidence

## Dry-Run Requirement Before Any Real Shadow Execution

- credential dry-run validation required before any real-data shadow request
- dry-run must prove no submit path and no scheduler activation

## STOP Conditions

- STOP if key has withdrawal or transfer permission
- STOP if IP allowlist is missing
- STOP if credential appears in repository, .env, or plaintext
- STOP if endpoint scope cannot be mapped to reviewed allow/block matrix

Real shadow review score measures review completeness, blocker clarity, and safety coverage only; it does not authorize real shadow execution, Upbit API access, credential use, scheduler activation, live trading, WF08, or production readiness.

This document does not authorize live trading, real shadow mode execution, Upbit API access, credential use, scheduler activation, parser execution, fixture creation, WF08 transition, runtime wiring, implementation, or production-readiness claims.

This document does not authorize live trading, shadow mode, Upbit API access, credential use, scheduler activation, parser execution, fixture creation, WF08 transition, runtime wiring, implementation, or production-readiness claims.
