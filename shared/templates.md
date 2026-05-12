# Agent HQ Templates

## 1. Universal Response Template
```text
Task Type
[Quick / Research / Build / Content]

Active Agent
[Agent name]

What Happens Now
[Short explanation]

Output
[Current step result]

Next Step
[Exactly one next action]

Paste Block
[Paste-ready block or None]
```

## 2. Compact Handoff Block
```text
ROLE: [next agent or tool]
GOAL: [exact objective]
INPUT:
- [minimal context]
- [minimal context]
CONSTRAINTS:
- [critical constraints only]
DELIVERABLE:
- [exact output needed]
```

## 3. Minimal Transfer Summary
```text
GOAL:
- [what needs to get done]

KEY CONTEXT:
- [only essential background]

CONSTRAINTS:
- [only what changes the result]
```

## 4. ChatGPT to Codex
```text
ROLE: Builder
GOAL: [implement the requested deliverable]
INPUT:
- [task summary]
- [required files or changes]
CONSTRAINTS:
- [format, usability, scope]
DELIVERABLE:
- [exact files, structure, or implementation]
```

## 5. Codex to ChatGPT Review
```text
ROLE: Reviewer
GOAL: Check the built output for clarity, completeness, and usability.
INPUT:
- [what was created]
- [original goal]
CONSTRAINTS:
- [what matters most]
DELIVERABLE:
- Final approval or concise corrections
```

## 6. Quick Task Intake
```text
Task:
[single clear task]

Requirements:
- [constraint]
- [constraint]
```

## 7. Build Request
```text
Task:
[what needs to be built]

Requirements:
- [required file or system outcome]
- [usability rule]
- [scope limit]
```

## 8. Content Request
```text
Task:
[what needs to be written]

Audience:
- [target reader]

Requirements:
- [tone]
- [length]
- [must include]
```

## 9. First-Use Starter Message
```text
Task:
Create a simple weekly operating checklist for running a content workflow using Strategist, Writer, and Reviewer.

Requirements:
- Keep it practical
- Make it usable by one person
- Keep it short
```
