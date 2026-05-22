# OpenAI Agent HQ

Deliberate routing for ChatGPT-style planning and Codex-style execution.

This folder is an OpenAI-specific operating system for agent-led work. It is designed for people who want explicit control over task classification, approval gates, handoffs, specialist routing, and final verification instead of vague "AI assistant" behavior.

## What This Is

`open_ai/` defines a compact HQ system for OpenAI workflows:

- `Master Controller` routes work
- specialist agents handle distinct bottlenecks
- planning stops for approval before meaningful implementation
- execution is verified before a task is considered done

The result is a controllable workflow for building, researching, writing, automating, and reviewing with less drift and less wasted output.

## Core Design

The system is built around four rules:

1. Classify the task before acting.
2. Route to the narrowest useful agent.
3. Stop for approval on meaningful build or modify work.
4. Verify before closing the task.

This keeps the workflow predictable and makes agent output easier to inspect, reuse, and improve.

## Folder Map

```text
open_ai/
|- AGENTS.md
|- README.md
|- agents/
|  |- master_controller.md
|  |- strategist.md
|  |- researcher.md
|  |- writer.md
|  |- builder.md
|  |- reviewer.md
|  |- growth_hacker.md
|  |- automation_engineer.md
|  `- monetization_strategist.md
`- context/
   |- agent_map.md
   |- master_prompt.md
   |- templates.md
   `- workflows.md
```

## Agent Set

### Core agents

- `Master Controller`: classifies, routes, enforces flow
- `Strategist`: chooses direction, sequencing, success criteria
- `Researcher`: gathers facts and constraints
- `Writer`: produces communication deliverables
- `Builder`: implements technical artifacts
- `Reviewer`: finds defects, risks, and readiness gaps

### Specialist agents

- `Growth Hacker`: acquisition, distribution, experiment design
- `Automation Engineer`: workflow systems, APIs, orchestration, operational reliability
- `Monetization Strategist`: offers, pricing, packaging, revenue logic

## Workflow Modes

The system supports four common modes:

- `Quick`: clear, low-risk tasks
- `Research`: fact-sensitive tasks
- `Build`: implementation-heavy tasks
- `Content`: writing-first tasks

These are documented in [`context/workflows.md`](C:/Users/minho/Documents/02_work/03_AI/04_agent_hq/open_ai/context/workflows.md).

## How To Use

### 1. Start with HQ

Use [`AGENTS.md`](C:/Users/minho/Documents/02_work/03_AI/04_agent_hq/open_ai/AGENTS.md) as the OpenAI-specific root instruction file.

### 2. Route by task type

Use [`context/agent_map.md`](C:/Users/minho/Documents/02_work/03_AI/04_agent_hq/open_ai/context/agent_map.md) to decide who should lead.

### 3. Reuse handoff blocks

Use [`context/templates.md`](C:/Users/minho/Documents/02_work/03_AI/04_agent_hq/open_ai/context/templates.md) for compact handoffs and task intake.

### 4. Keep the flow strict

Meaningful work should follow:

`classify -> plan -> approval -> execute -> verify -> report`

## Best Fit

This setup works best when you want:

- explicit orchestration instead of auto-pilot
- clear planning before implementation
- reusable specialist roles
- strong review and verification habits
- better ChatGPT-to-Codex handoff quality

## Notable Behavior

- OpenAI workflow only
- explicit routing, not hidden auto-routing
- implementation should happen after approval, not before
- verification is part of the workflow, not an optional extra

## Quick Start

1. Load [`AGENTS.md`](C:/Users/minho/Documents/02_work/03_AI/04_agent_hq/open_ai/AGENTS.md).
2. Review [`context/workflows.md`](C:/Users/minho/Documents/02_work/03_AI/04_agent_hq/open_ai/context/workflows.md).
3. Pick the right agent with [`context/agent_map.md`](C:/Users/minho/Documents/02_work/03_AI/04_agent_hq/open_ai/context/agent_map.md).
4. Use [`context/templates.md`](C:/Users/minho/Documents/02_work/03_AI/04_agent_hq/open_ai/context/templates.md) for clean handoffs.
5. Execute only after approval exists.

## Why This Folder Exists

Most agent setups fail because they blur planning, execution, and review into one muddy loop. This folder separates those concerns so you can get sharper decisions, cleaner handoffs, and more reliable output from OpenAI tools.
