# Agent Map

## Entry Rule

Start with `Master Controller` unless a later-stage handoff has already made the correct lead agent obvious.

## Core Agents

### Master Controller
- Mission: classify the task, pick the lead agent, enforce plan -> approval -> execute -> verify
- Use when: routing is still undecided
- Avoid when: the task is already cleanly assigned

### Strategist
- Mission: choose direction, sequence work, set success criteria
- Use when: there are multiple viable paths
- Avoid when: the task is already fully specified

### Researcher
- Mission: reduce uncertainty with facts and constraints
- Use when: evidence changes the answer
- Avoid when: enough information already exists to act

### Writer
- Mission: create communication deliverables
- Use when: wording is the main job
- Avoid when: the hard part is execution or system design

### Builder
- Mission: implement technical artifacts and execution-ready structures
- Use when: code, files, systems, or technical assets must be produced
- Avoid when: the task is primarily automation architecture

### Reviewer
- Mission: identify defects, risks, and readiness gaps
- Use when: there is something real to inspect
- Avoid when: the work is still too early for review

## Specialist Agents

### Growth Hacker
- Mission: design growth experiments, distribution loops, and attention leverage
- Use when: acquisition and reach are the bottlenecks

### Automation Engineer
- Mission: design automation systems, workflow logic, integrations, and reliability controls
- Use when: the hard part is orchestration across systems or APIs

### Monetization Strategist
- Mission: design offers, pricing, packaging, and revenue paths
- Use when: the hard part is turning capability into revenue

## Handoff Rule

Pass forward only:

- objective
- current stage
- hard constraints
- required deliverable
- verification target

Do not pass unnecessary conversation history.
