# SHADOW MODE ENTRY CRITERIA V1

## 1. Required Prior Gates

- offline governance confirmed
- offline synthetic tests confirmed
- stress governance confirmed
- stress harness implemented and executed

## 2. Required Test Evidence

- no forbidden state leakage
- no signal-to-order direct transition
- no retry without IDEM-safe evidence

## 3. Required Stress Evidence

- required stress scenarios passed with documented logs
- kill/recon behavior validated in synthetic stress context

## 4. Required Deployment Governance

- version/config hash controls documented
- no manual SSH deploy policy enforced

## 5. Required Credential Governance

- key permissions and storage policy documented
- revocation and rotation checklist available

## 6. Required Alert/KILL Evidence

- alert payload + SLA dry-run evidence
- sticky kill behavior evidence

## 7. Required Shadow Recorder Behavior

- recorder stores decisions and gate outcomes
- recorder does not submit exchange orders
- recorder emits deterministic audit entries

## 8. Prohibited Shadow Shortcuts

- no live API calls
- no credential injection shortcuts
- no scheduler bypass
- no partial gate skip

## 9. N-day Continuous Criteria

- continuous N-day shadow run (value set by human approval)
- zero unresolved drift events
- zero forbidden transitions

## 10. Exit Criteria

- criteria package pass signed by human reviewer
- WF08 review eligibility opened

## 11. Human Approval Format

- approver name
- timestamp
- evidence links
- reversible approval statement

Shadow mode is not authorized by this document.

Readiness score measures documentation, governance, and validation completeness only; it does not authorize trading, does not predict profit, and does not indicate runtime, shadow, live, or WF08 readiness.

This document does not authorize live trading, shadow mode, Upbit API access, credential use, scheduler activation, parser execution, fixture creation, WF08 transition, runtime wiring, implementation, or production-readiness claims.
