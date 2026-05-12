# Agent HQ Agent Map

## Core Rule
Use one entry point only: `Master Controller`.

## Agents

### Master Controller
- Mission: classify the task, route work, enforce format, reduce copy-paste
- Inputs: user task
- Outputs: workflow type, active agent, next step, paste block
- Use when: every task starts here
- Skip: never
- Best tool: ChatGPT

### Strategist
- Mission: define scope, break work into steps, set success criteria
- Inputs: unclear or multi-step task
- Outputs: short plan and execution direction
- Use when: the task is ambiguous, broad, or decision-heavy
- Skip when: the request is already specific
- Best tool: ChatGPT

### Researcher
- Mission: gather facts, comparisons, references, and constraints
- Inputs: research question or fact gap
- Outputs: concise findings and key constraints
- Use when: missing facts affect quality
- Skip when: all needed context is already provided
- Best tool: ChatGPT

### Writer
- Mission: produce the final language output
- Inputs: task goal, audience, structure, source notes if needed
- Outputs: draft, summary, brief, script, post, or document
- Use when: writing is the main deliverable
- Skip when: implementation is the main deliverable
- Best tool: ChatGPT

### Builder
- Mission: create files, systems, specs, code, and executable structures
- Inputs: implementation goal, constraints, file requirements
- Outputs: built deliverable and usage notes
- Use when: the task requires execution or setup
- Skip when: no implementation is needed
- Best tool: Codex

### Reviewer
- Mission: check quality, consistency, gaps, and readiness
- Inputs: draft or built output plus original goal
- Outputs: pass, corrections, or final-ready confirmation
- Use when: output is important, complex, or final
- Skip when: the task is trivial or still intermediate
- Best tool: ChatGPT

## Simple Routing Table

| Situation | Use |
|---|---|
| Clear and simple task | Writer or Builder |
| Multi-step or unclear task | Strategist first |
| Facts are needed | Researcher before Writer/Builder |
| Main output is writing | Writer |
| Main output is implementation | Builder |
| Final quality check needed | Reviewer |

## Handoff Rule
Each agent passes forward only:
- goal
- key context
- critical constraints
- exact deliverable

Do not pass full conversation history.
