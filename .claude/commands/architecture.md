# Architecture Design Skill

Design and document solution architecture aligned to an approved product roadmap. Output is one or more interactive HTML files in `ARCHITECTURE/`.

## Arguments

`$ARGUMENTS` — product name, or path to the product design HTML file. If empty, look for the most recent file in `PRODUCT_DESIGN/`.

---

## Rules

- Architecture must be driven by requirements, not by technology preferences. Every component must justify its existence against a specific user need.
- Apply ruthless mentor mode: challenge over-engineered solutions, unnecessary microservices, premature abstraction.
- If the product design document is missing, vague, or does not contain enough information to make concrete architectural decisions, **call `/requirements` to clarify before proceeding**. Do not invent requirements.
- Do not generate architecture without reading the product design document first.
- Each architectural decision must have an ADR with real alternatives considered — not strawmen.

---

## Flow

### Step 1 — Read the product design

Read the product design HTML in `PRODUCT_DESIGN/`. Extract:
- User personas and their goals
- User stories per stage (MTP / MUP / MVP)
- Non-negotiable constraints (performance, platform, compliance)
- Key screens and the interactions they imply

**If any of these are missing or too vague to make a concrete design decision, stop and run `/requirements` to fill the gap. Say:** "I need more information on [X] before I can design the architecture. Running `/requirements` to clarify."

### Step 2 — Clarifying questions (architecture-specific)

Ask 3–5 targeted questions before designing:

**Scale & Load**
- How many concurrent users at each stage? (MTP: internal testers? MUP: tens? MVP: thousands?)
- Any specific performance SLAs?

**Data & State**
- What data must persist? What can be ephemeral?
- Any data sensitivity / compliance requirements (PII, GDPR, HIPAA)?

**Integration**
- What external systems or APIs must this integrate with?
- Any existing infrastructure that must be reused?

**Team**
- What is the team size and stack familiarity? (directly affects ADR choices)
- Any hard stack constraints?

### Step 3 — High-level design

Identify conceptual components. For each:
- Name
- Responsibility (one sentence)
- Why it must exist (which user need / constraint forces it)
- Which roadmap stages it's needed in (MTP / MUP / MVP)

Present the component list to the user:
> "Here are the components I've identified. Tell me what's missing, wrong, or unnecessary before I design the solutions."

Wait for explicit sign-off.

### Step 4 — Functional workflows

For each user story in the product design, map a step-by-step flow through the components:
- What triggers the workflow (user action or event)
- Which component handles each step and what it does
- What the final outcome is
- Key assumption behind the flow
- Failure mode if any step breaks

Group workflows by roadmap stage (MTP / MUP / MVP).

If a workflow reveals a missing component or a gap in the product design, stop and raise it with the user before continuing.

### Step 5 — Solution architecture per component

For each component, decide the concrete solution (technology / pattern / service) and generate an ADR:
- **Context:** what forces this decision
- **Options considered:** minimum 2 real alternatives (not strawmen), each with a clear rejection reason
- **Decision:** chosen option and why
- **Trade-offs:** concrete pros and cons
- **Consequences:** what becomes easier / harder / locked-in

ADRs must be honest. If the chosen option has a meaningful downside, say it.

### Step 6 — Roadmap alignment

Map components and workflows to stages. Every component or workflow deferred to MUP or MVP must explain why it's not needed earlier.

### Step 7 — Generate the architecture document

Create `ARCHITECTURE/{{kebab-product-name}}-architecture.html` by filling `TEMPLATES/architecture_template.html`.

**System diagram:** generate a text-based ASCII diagram using box-drawing characters:
```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Frontend   │────▶│   API Layer  │────▶│   Database   │
└──────────────┘     └──────────────┘     └──────────────┘
```

**Functional workflows:** for each user story, fill one `WORKFLOW BLOCK` with its steps using `.flow-box` elements. Mark the trigger step `flow-trigger` and the outcome step `flow-end`. Include the key assumption and failure mode.

Fill every `{{PLACEHOLDER}}`. Repeat component and workflow blocks as needed.

If the architecture is complex (>6 components), split into multiple files:
- `{{product}}-architecture-overview.html` — diagram + HLD + workflows
- `{{product}}-architecture-{{component-group}}.html` — solution blocks per group

Open the file and say: **"Review ARCHITECTURE/{{filename}}.html. Once approved, run `/dev` on a specific issue to begin implementation."**

### Step 8 — Trigger review

Run `/skill-review architecture` after output is delivered.

---

## Output

| File | Location | Contains |
|---|---|---|
| `{{product-name}}-architecture.html` | `ARCHITECTURE/` | Diagram, HLD, Functional Workflows, Solution Arch + ADRs |

## Doc Standard

Architecture docs are **HTML** (interactive with sidebar, stage filter, collapsible ADRs, workflow step-flows). Never produce a `.md` architecture file.
