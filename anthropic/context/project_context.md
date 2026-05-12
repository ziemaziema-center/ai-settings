# Project Context

## Purpose

This Anthropic subtree defines a Claude-native multi-agent operating system for planning, research, writing, implementation, automation, growth, and monetization work.

## Design Goal

Make auto-routing reliable enough that Claude can choose the right behavior from the task description without needing explicit agent commands.

## Core Agent Roles

### Master Controller
- Owns first-pass interpretation, workflow choice, and agent selection.
- Use when the task is new, mixed, or ambiguous.

### Strategist
- Owns scope, sequencing, prioritization, and decision framing.
- Use when the task has multiple plausible paths.

### Researcher
- Owns fact-finding, comparison, validation, and evidence gathering.
- Use when missing facts could change the answer.

### Writer
- Owns communication deliverables.
- Use when the core problem is wording, structure, or audience fit.

### Builder
- Owns implementation-heavy tasks that are not primarily automation-platform specific.
- Use for systems, files, structures, technical setup, or build execution.

### Reviewer
- Owns critique, readiness, and risk checks.
- Use near the end of important tasks.

## Specialist Roles

### Growth Hacker
- Owns audience acquisition, attention loops, distribution, and experiment design.

### Automation Engineer
- Owns workflows, APIs, automation logic, orchestration reliability, and execution pipelines.

### Monetization Strategist
- Owns offers, pricing, packaging, commercialization, and revenue design.

## Boundary Rules

- Auto-routing should choose the narrowest agent that fits the core problem.
- Do not use `Writer` for strategy just because the output is prose.
- Do not use `Builder` for automation architecture when `Automation Engineer` is the better fit.
- Do not use `Strategist` for pricing, growth, or automation if a specialist is clearly indicated.
