# Agent HQ Workflows

## Universal Output Format
Every step uses:
1. Task Type
2. Active Agent
3. What Happens Now
4. Output
5. Next Step
6. Paste Block

## 1. Quick Workflow
Use when the task is simple, clear, and low-risk.

Sequence:
1. Master Controller classifies `Quick`
2. Route to Writer or Builder
3. Produce result
4. Review only if needed
5. Final delivery

Pass forward:
- task goal
- required format
- constraints

Review point:
- optional

Final output:
- completed result in the fixed 6-part structure

## 2. Research Workflow
Use when the task depends on facts, comparisons, or validation.

Sequence:
1. Master Controller classifies `Research`
2. Strategist scopes if needed
3. Researcher gathers findings
4. Writer or Builder produces final output
5. Reviewer checks quality
6. Final delivery

Pass forward:
- research question
- key findings
- constraints
- open risks

Review point:
- default yes

Final output:
- findings-based answer or deliverable in the fixed 6-part structure

## 3. Build Workflow
Use when the task requires files, setup, implementation, or technical structure.

Sequence:
1. Master Controller classifies `Build`
2. Strategist scopes if needed
3. Researcher supports only if required
4. Builder creates the deliverable
5. Reviewer checks usability and completeness
6. Final delivery or revision

Pass forward:
- build objective
- file/component list
- constraints
- success criteria

Review point:
- default yes

Final output:
- what was built, how to use it, and next action if any

## 4. Content Workflow
Use when the main deliverable is written content.

Sequence:
1. Master Controller classifies `Content`
2. Strategist scopes audience and structure if needed
3. Researcher supports only if needed
4. Writer drafts
5. Reviewer checks clarity and alignment
6. Final delivery

Pass forward:
- audience
- objective
- tone
- structure
- must-include points

Review point:
- default yes for shared content

Final output:
- polished content in the fixed 6-part structure

## Day 1 Starter Pack

### Exact First Message for ChatGPT
Paste the content of `master_prompt.txt`, then add this message under it:

```text
Task:
Create a simple weekly operating checklist for running a content workflow using Strategist, Writer, and Reviewer.

Requirements:
- Keep it practical
- Make it usable by one person
- Keep it short
```

### Simple Example Task
`Create a simple weekly operating checklist for running a content workflow using Strategist, Writer, and Reviewer.`

### Full Example Run

#### Step 1: Master Controller

Task Type
Content

Active Agent
Master Controller

What Happens Now
The task is a writing deliverable with clear scope, so the system routes directly to Writer and skips Strategist and Researcher.

Output
The checklist should be short, operational, and built for one-person weekly use.

Next Step
Send to Writer

Paste Block
```text
ROLE: Writer
GOAL: Draft a short weekly operating checklist for a solo content workflow.
INPUT:
- Workflow uses Strategist, Writer, and Reviewer
- Output should be short and practical
CONSTRAINTS:
- One person should be able to use it weekly
- Avoid theory
DELIVERABLE:
- A concise weekly checklist
```

#### Step 2: Writer

Task Type
Content

Active Agent
Writer

What Happens Now
Create the checklist in a clean, usable format.

Output
Weekly Content Workflow Checklist

1. Define the week's content goal.
2. Ask Strategist to break the goal into one clear content task.
3. Ask Writer to draft the content from that task.
4. Ask Reviewer to check clarity, quality, and gaps.
5. Revise only what Reviewer flags as important.
6. Finalize and store the approved version.

Next Step
Send to Reviewer

Paste Block
```text
ROLE: Reviewer
GOAL: Check this weekly checklist for clarity and missing steps.
INPUT:
- Solo workflow
- Uses Strategist, Writer, Reviewer
- Checklist is intended for weekly use
CONSTRAINTS:
- Keep it short
- Keep it practical
DELIVERABLE:
- Final approved checklist or concise corrections
```

#### Step 3: Reviewer

Task Type
Content

Active Agent
Reviewer

What Happens Now
Check whether the checklist is complete, clear, and immediately usable.

Output
Pass. The checklist is short, clear, and ready to use. Optional improvement: add a final archive step if the user wants version tracking.

Next Step
Final Delivery

Paste Block
None

### How to Use This Example
1. Start in ChatGPT with `master_prompt.txt`
2. Use the sample task above
3. Follow the returned Paste Block
4. Repeat until `Next Step` becomes `Final Delivery`
