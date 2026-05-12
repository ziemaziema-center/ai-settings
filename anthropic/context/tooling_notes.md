# Tooling Notes

## Operating Assumption

Claude-side tooling may be permission-gated and narrower than a full local shell environment.

## Practical Implications

- Prefer bounded tool usage with a clear purpose.
- When a task depends on external tools or integrations, state that dependency explicitly.
- Do not assume unrestricted automation access.
- Keep system design resilient to partial tool availability.

## Routing Impact

- If the task depends on tool capability or external integration behavior, consider `Automation Engineer`.
- If the task depends on evidence gathering rather than execution, consider `Researcher`.
- If the task is blocked by environment constraints, escalate clearly instead of improvising hidden assumptions.

## Documentation Rule

Describe what tools are for, what limits matter, and what fallback exists. Avoid burying critical operational constraints in generic prose.
