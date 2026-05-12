# Skills

## Purpose

Skills are reusable work patterns that improve routing consistency and output quality across recurring Claude tasks.

Skills do not replace agents. They sharpen how an agent executes.

## Skill Format

Each skill should define:

- trigger signals
- expected output
- guardrails
- common handoff targets

## Reusable Skills

### Opportunity Framing
- Trigger signals: "which direction", "best option", "where should we start", "what is the highest leverage path"
- Expected output: 2-4 options, selection, tradeoff summary, recommended path
- Guardrails: do not fake research; escalate to `Researcher` if facts are missing
- Common handoff targets: `Strategist`, `Monetization Strategist`, `Growth Hacker`

### Build Scoping
- Trigger signals: "build", "set up", "implement", "structure", "system"
- Expected output: architecture, execution stages, constraints, validation checkpoints
- Guardrails: stop for approval before implementation work
- Common handoff targets: `Builder`, `Automation Engineer`, `Reviewer`

### Experiment Design
- Trigger signals: "growth test", "distribution experiment", "what should we test", "optimize reach"
- Expected output: hypothesis, variable, channel, success metric, follow-up decision rule
- Guardrails: avoid vanity metrics without a decision rule
- Common handoff targets: `Growth Hacker`, `Writer`, `Reviewer`

### Monetization Packaging
- Trigger signals: "pricing", "offer", "service package", "how do we make money", "productize"
- Expected output: offer structure, target buyer, price logic, delivery scope, upsell/downsell path
- Guardrails: do not collapse packaging into generic marketing copy
- Common handoff targets: `Monetization Strategist`, `Writer`, `Strategist`

### Risk Review
- Trigger signals: "review", "check", "what could go wrong", "validate"
- Expected output: findings, severity, missing validation, readiness call
- Guardrails: findings first, summary second
- Common handoff targets: `Reviewer`
