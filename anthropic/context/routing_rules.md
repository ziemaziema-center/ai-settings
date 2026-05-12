# Routing Rules

## Primary Rule

Choose the agent whose core decision load best matches the task.

Route by the real bottleneck, not by the surface format of the output.

## Workflow Classification

### Quick
- Use when the task is clear, low-risk, and answerable in one pass.

### Research
- Use when uncertainty, comparison, or factual validation changes the outcome.

### Build
- Use when the result is a system, artifact, structure, workflow, or implementation.

### Content
- Use when the result is primarily communication for a reader or audience.

## Agent Selection Logic

### Master Controller
Choose when:
- the task contains mixed signals
- more than one agent may apply
- the user asks for an end-to-end outcome

Do not choose when:
- the task cleanly fits one agent already

### Strategist
Choose when:
- there are multiple viable paths
- priorities, scope, or sequencing are unclear
- the user asks what to do first or which direction is best

Do not choose when:
- the main blocker is factual uncertainty
- the task is already fully specified

### Researcher
Choose when:
- the main blocker is missing facts
- the task needs comparison or validation
- risk depends on knowing what is true

Do not choose when:
- the task is mostly prioritization or packaging

### Writer
Choose when:
- quality of wording, structure, tone, or clarity is the main task

Do not choose when:
- the hard part is strategy, system design, or implementation logic

### Builder
Choose when:
- the task is technical and implementation-heavy
- files, structures, specs, or execution artifacts are needed

Do not choose when:
- the task is specifically about automation architecture, APIs, or workflow engines

### Reviewer
Choose when:
- the main need is critique, validation, or readiness

Do not choose when:
- no meaningful artifact exists yet to review

### Growth Hacker
Choose when:
- the task is about acquisition, reach, virality, distribution loops, or growth experiments

Do not choose when:
- the task is general brand writing without an explicit growth goal

### Automation Engineer
Choose when:
- the task is about n8n, APIs, triggers, automations, integrations, workflow logic, or operational reliability

Do not choose when:
- the task is generic coding with no workflow or automation layer

### Monetization Strategist
Choose when:
- the task is about offers, pricing, packaging, monetization paths, or productized service design

Do not choose when:
- the task is pure growth with no revenue model question

## Adjacency Hints

- `Strategist` often hands off to `Growth Hacker`, `Automation Engineer`, `Monetization Strategist`, `Writer`, or `Builder`.
- `Researcher` often feeds `Strategist`, `Writer`, or `Monetization Strategist`.
- `Automation Engineer` may hand off to `Builder` when the design is settled and implementation starts.
- `Growth Hacker` may hand off to `Writer` for messaging or to `Reviewer` for experiment critique.
- `Monetization Strategist` may hand off to `Writer` for offer copy or to `Strategist` for roadmap sequencing.

## Approval Logic

For create, build, design, modify, implement, or planning requests:

1. present the plan
2. stop
3. wait for approval

## Output Rule

For non-trivial tasks, state the chosen route explicitly so the next step is obvious.
