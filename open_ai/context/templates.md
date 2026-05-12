# Templates

## 1. Universal Status Block
```text
Task Type
[Quick / Research / Build / Content]

Active Agent
[Agent name]

What Happens Now
[one short explanation]

Output
[current result]

Next Step
[exactly one next action]

Paste Block
[paste-ready handoff or None]
```

## 2. Core Handoff Block
```text
ROLE: [next agent]
GOAL: [exact objective]
STAGE: [plan / execute / verify]
INPUT:
- [critical context]
- [critical context]
CONSTRAINTS:
- [hard limit]
- [hard limit]
DELIVERABLE:
- [exact output]
VERIFY:
- [what must be checked]
```

## 3. ChatGPT -> Codex Build Block
```text
ROLE: Builder
GOAL: Implement the approved change.
STAGE: execute
INPUT:
- [approved plan]
- [target files or structure]
CONSTRAINTS:
- do not modify unrelated files
- keep within approved scope
DELIVERABLE:
- completed implementation
VERIFY:
- run or describe the checks performed
```

## 4. Specialist Delegation Block
```text
ROLE: [Growth Hacker / Automation Engineer / Monetization Strategist]
GOAL: [specialist objective]
STAGE: plan
INPUT:
- [current business or system context]
- [specific constraint]
DELIVERABLE:
- [decision, design, or experiment set]
VERIFY:
- [decision rule or quality bar]
```

## 5. Review Block
```text
ROLE: Reviewer
GOAL: Check the output for defects, risk, and readiness.
STAGE: verify
INPUT:
- [artifact produced]
- [original goal]
CONSTRAINTS:
- findings first
- keep line references tight when possible
DELIVERABLE:
- prioritized findings or explicit pass
VERIFY:
- note any missing tests or unresolved risks
```
