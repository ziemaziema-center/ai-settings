# Workflows

## System Flow

Every meaningful task follows:

1. classify
2. choose lead agent
3. plan if required
4. wait for approval
5. execute
6. verify
7. report

## Quick Workflow

Use when the task is clear, low-risk, and can be handled in one pass.

Flow:
1. `Master Controller` classifies `Quick`
2. route directly to `Writer`, `Builder`, or another clear specialist
3. produce the result
4. verify only if risk justifies it

## Research Workflow

Use when facts or comparison materially affect the answer.

Flow:
1. classify `Research`
2. use `Researcher` to gather findings
3. use `Strategist` if a decision must be made from the findings
4. route to the final producing agent
5. verify if the output is important

## Build Workflow

Use when the main deliverable is an implementation artifact or system.

Flow:
1. classify `Build`
2. use `Strategist` only if the path is not already clear
3. stop and present the plan
4. wait for approval
5. route to `Builder` or `Automation Engineer`
6. verify the implementation with `Reviewer` or direct checks
7. report what was changed and how it was checked

## Content Workflow

Use when the main deliverable is communication.

Flow:
1. classify `Content`
2. use `Strategist` or `Researcher` only if needed
3. route to `Writer`
4. verify with `Reviewer` if clarity or risk matters

## Specialist Routing Shortcuts

- use `Growth Hacker` for acquisition, distribution, and experiment design
- use `Automation Engineer` for workflow systems, APIs, n8n, and operational reliability
- use `Monetization Strategist` for pricing, packaging, and revenue model questions

## Verification Standard

Never close a meaningful task without one of these:

- a direct check performed
- a reviewer pass
- an explicit note that verification could not be completed
