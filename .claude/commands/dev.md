# Dev Skill

Implement work tied to an open GitHub issue, following the full planning → approval → implementation flow.

## Arguments

`$ARGUMENTS` — issue number (e.g. `42`) or issue URL.

## Rules

- Never start implementation without an open issue. If no issue exists, stop and say: "Run `/issue` first."
- Never start implementation without explicit user approval of the solution document.

---

## Flow

### Step 1 — Read the issue

```bash
gh issue view <number>
```

Read every field. If the issue is vague, ask clarifying questions (ruthless mentor mode) before proceeding.

### Step 2 — Create the solution document

Create `SOLUTIONS/<issue-number>-<kebab-issue-title>-solution.html` by copying `TEMPLATES/solutions_template.html` and filling in:

| Placeholder | Value |
|---|---|
| `{{ISSUE_NUMBER}}` | issue number |
| `{{ISSUE_TITLE}}` | issue title |
| `{{ISSUE_TYPE}}` | `feature` or `bug` |
| `{{ISSUE_DATE}}` | today's date |
| `{{ISSUE_AUTHOR}}` | your name or "Claude" |
| `{{PROBLEM_STATEMENT}}` | from issue body |
| `{{PROPOSED_SOLUTION}}` | your concrete plan (what, not why) |
| `{{ARCH_FIT}}` | alignment reasoning |
| `{{ARCH_ALIGNMENT}}` | `Aligned` / `Diverges` |
| `{{ALIGN_CLASS}}` | `impact-none` or `impact-major` |
| `{{IMPACT_LEVEL}}` | `None` / `Minor` / `Major` |
| `{{IMPACT_CLASS}}` | `impact-none` / `impact-minor` / `impact-major` |
| `{{EFFECT_DIRECTION}}` | `Beneficial` / `Detrimental` / `Neutral` |

Leave implementation placeholders (`{{DRIFT_1}}`, `{{TEST_EVIDENCE}}`) as empty or as "TBD — pending implementation".

Open the file path for the user and say: **"Review SOLUTIONS/<file>.html. Reply 'approved' to proceed."**

### Step 3 — Wait for approval

Do not write a single line of implementation code until the user explicitly approves.

### Step 4 — Implement

Follow Karpathy's rules:
1. Start simple — implement the minimum that makes the issue's expected behavior true
2. End-to-end first — get something runnable before optimizing
3. Overfit first — make it work on the exact case in the issue
4. Inspect — verify behavior; do not guess

### Step 5 — Update the solution document

Fill in the implementation tab placeholders:
- `{{DRIFT_1}}` and any additional drifts (add timeline items as needed)
- `{{TEST_EVIDENCE}}` — list unit tests run and their results

### Step 6 — Close the loop

```bash
gh issue comment <number> --body "Implementation complete. Solution doc: SOLUTIONS/<file>.html"
```

Trigger `/skill-review` after completion.

## Doc Standard

Solution files are **HTML** (human-readable, interactive). The template in `TEMPLATES/solutions_template.html` is the source of truth. Never create a `.md` solution file.
