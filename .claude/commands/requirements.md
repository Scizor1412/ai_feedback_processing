# Requirements Clarification Skill

Elicit and document product requirements through structured questioning, then produce an interactive product design document aligned to the MTP → MUP → MVP roadmap.

## Arguments

`$ARGUMENTS` — product name or one-line description. If empty, ask for it first.

---

## Rules

- Never generate requirements or design decisions for the user. Your job is to ask, challenge, and clarify — not invent.
- Apply ruthless mentor mode: push back on vague goals, assumptions, and "nice-to-haves" presented as core needs.
- Do not proceed to output generation until you have concrete answers to every required question.

---

## Flow

### Step 1 — Anchoring question

Ask one focused question to establish the core problem:

> "What is the specific problem this product solves, and who experiences it? Describe a real situation where this problem happens."

Wait for answer. If vague, push back before continuing.

### Step 2 — Structured elicitation

Ask questions in batches of 3–4. Do not dump all questions at once. Cover:

**User & Problem**
- Who is the primary user? Describe them concretely (role, context, pain).
- What does the user do today without this product? Why is that insufficient?
- What does success look like for the user after using this product?

**Scope & Boundaries**
- What is the one thing this product must do to be worth building at all? (MTP hypothesis)
- What makes this product minimally usable by a real user? (MUP threshold)
- What would make this a product you'd actually ship to the public? (MVP bar)
- What is explicitly out of scope?

**Behavior & Experience**
- What are the 3–5 core user actions the product must support?
- Are there any non-negotiable UX requirements (offline, mobile, speed)?
- What does the product look like at a high level? (key screens)

**Constraints**
- Any hard technical constraints (platform, stack, integrations)?
- Timeline or resource constraints that affect scope?

### Step 3 — Roadmap alignment

Confirm the MTP → MUP → MVP breakdown with the user:

> "Based on what you've told me, here's how I'd divide the roadmap:
> - **MTP:** [hypothesis + minimum feature set to test it]
> - **MUP:** [minimum for a real user to get value]
> - **MVP:** [minimum for public release]
>
> Does this match your thinking? What would you change?"

Do not proceed without explicit sign-off on the roadmap.

### Step 4 — Generate the product design document

Create `PRODUCT_DESIGN/{{kebab-product-name}}-product-design.html` by filling `TEMPLATES/product_design_template.html` with all gathered information.

Fill every `{{PLACEHOLDER}}` with real content. For wireframes, build HTML wireframe blocks using `.wf-block` elements to represent actual screen layouts described by the user — do not leave placeholder text.

For GitHub issues section: generate a concrete issue title and one-line description for each user story per stage. These are to be created with `/issue` separately; here just list them.

Open the file and say: **"Review PRODUCT_DESIGN/{{filename}}.html. When you're happy with it, run `/architecture` to design the solution."**

### Step 5 — Trigger review

Run `/skill-review requirements` after output is delivered.

---

## Output

| File | Location |
|---|---|
| `{{product-name}}-product-design.html` | `PRODUCT_DESIGN/` |

## Doc Standard

Product design docs are **HTML** (human-readable, interactive with sidebar, stage tabs, persona cards, wireframes). Never produce a `.md` product design file.
