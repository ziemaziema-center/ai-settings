# UPBIT V2 Gate Dependency Map - 2026-06-01

| GATE | depends_on | artifacts_required | exit_criteria | status |
|---|---|---|---|---|
| GATE_7 | GATE_6 | PTRC spec freeze artifact + static review evidence | PTRC mandatory checks and reject semantics frozen with no contradiction | SPEC_ONLY |
| GATE_8 | GATE_7 | PTRC implementation spec + static review package | implementation-review evidence without bypass path | SPEC_ONLY |
| GATE_9 | GATE_8 | IDEM spec freeze artifact | UUID and persistence-before-send invariants frozen | SPEC_ONLY |
| GATE_10 | GATE_9 | IDEM implementation spec + static review package | duplicate-prevention and retry semantics review evidence | SPEC_ONLY |
| GATE_11 | GATE_10 | RECON spec freeze artifact | intent/reality reconciliation rules frozen | SPEC_ONLY |
| GATE_12 | GATE_11 | RECON implementation spec + static review package | drift-handling and orphan rules review evidence | SPEC_ONLY |
| GATE_13 | GATE_12 | KILL spec freeze artifact | sticky kill and trigger matrix frozen | SPEC_ONLY |
| GATE_14 | GATE_13 | KILL implementation spec + static review package | kill-sequence review evidence and no auto-clear path | SPEC_ONLY |
| GATE_15 | GATE_14 | HEART+BUDGET+OSM integration artifact | heartbeat/rate/state-machine integration evidence | SPEC_ONLY |
| GATE_16 | GATE_15 | ALERT SLA instrumentation artifact | actionable alert <=5 seconds evidence | SPEC_ONLY |
| GATE_17 | GATE_16 | DEPLOY governance frozen artifact | anti-Knight deployment controls frozen and traceable | SPEC_ONLY |
| GATE_18 | GATE_17 | CRED governance frozen artifact | no-withdraw key policy and rotation governance frozen | SPEC_ONLY |
| GATE_19 | GATE_18 | STRESS report package | annual stress scenarios executed and reported | SPEC_ONLY |
| GATE_20 | GATE_19 | SHADOW N-day evidence package | continuous shadow criteria all pass | SPEC_ONLY |
| GATE_21 | GATE_20 | ASSESS annual self-assessment artifact | assessment issued and approved with sign-off | SPEC_ONLY |
| GATE_22 | GATE_21 | WF08 review artifact | explicit WF08 review decision recorded | BLOCKED |
| GATE_23 | GATE_22 | live authorization packet (human logged scoped reversible) | explicit human live authorization with reversible scope | BLOCKED |

Status note: defaulted to `SPEC_ONLY` unless explicit blocker evidence existed. `GATE_22` and `GATE_23` are `BLOCKED` by source-level blocked/unauthorized statements.
