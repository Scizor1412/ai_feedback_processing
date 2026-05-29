# Issue Skill

Create or update a GitHub issue using the correct template. Supports single-issue creation and bulk creation from a product design document.

## Arguments

`$ARGUMENTS` — one of:
- Natural language description of a single issue
- An existing issue number to update
- `bulk` — create all issues defined in the product design document (see Bulk Mode below)

---

## Single Issue Mode

### Step 1 — Classify

Decide if this is a **bug** (something isn't working as expected) or a **feature** (new capability or improvement).

- Bug → use `TEMPLATES/bug_issue_template.md`
- Feature → use `TEMPLATES/feature_issue_template.md`

If ambiguous, ask one clarifying question before proceeding.

### Step 2 — Ruthless mentor check

Before drafting, stress-test the issue description:
- Is the problem statement concrete? ("it would be nice" is not a problem)
- For bugs: do we have steps to reproduce?
- For features: is expected behavior defined from the user's POV?

Push back on vague descriptions. Ask clarifying questions until the issue is sharp.

### Step 3 — Draft

Fill the template with the information gathered. Do not add sections not in the template. Do not soften language.

### Step 4 — Check for duplicates and create

Check for duplicates first:
- If `gh` CLI is available: `gh issue list --search "<title>" --state open`
- If not available: use GitHub REST API — `GET /repos/{owner}/{repo}/issues?state=open` and scan titles

Create or update:
- If `gh` available: `gh issue create --title "..." --body "$(cat <<'EOF' ... EOF)"`
- If not available: `POST /repos/{owner}/{repo}/issues` via Python `urllib.request` with `Bearer {GITHUB_TOKEN}` from `.env`

### Step 5 — Report

Output the issue URL and number. Trigger `/skill-review` after completion.

---

## Bulk Mode

Use when creating the **initial issue set from a product design document** (e.g. after `/requirements` produces a product design HTML with a GitHub Issues section). Do not use bulk mode for ongoing individual issues.

### Step 1 — Read the product design

Read the GitHub Issues section of the product design HTML in `PRODUCT_DESIGN/`. Extract all issue titles, descriptions, and roadmap stages (MTP / MUP / MVP).

### Step 2 — Ruthless mentor check (batch)

Review the full issue set before creating anything:
- Are all issues concrete and independently actionable?
- Does each issue have a clear deliverable (not "improve X")?
- Are MTP issues truly the minimum needed to test the core hypothesis?

Raise concerns before proceeding. Do not create issues for vague or overlapping items.

### Step 3 — Write a Python bulk creation script

Write a self-contained Python script (no external dependencies beyond stdlib) that:
1. Reads `GITHUB_TOKEN` from `.env`
2. Defines all issues as a list of dicts with `title` and `body` (filled from `TEMPLATES/feature_issue_template.md` or `bug_issue_template.md`)
3. Creates each issue via `POST https://api.github.com/repos/{owner}/{repo}/issues` using `urllib.request`
4. Sleeps 0.5s between requests to respect GitHub secondary rate limits
5. Prints each created issue number and URL
6. Prints a final summary (created / failed counts)

Title format: `[{STAGE}] {descriptive title}` — e.g. `[MTP] JSON feedback ingestion pipeline`

### Step 4 — Run and clean up

Run the script with `python3 <script>.py`. Confirm all issues were created. Delete the script immediately after — it is a one-off tool, not part of the codebase.

### Step 5 — Report

List all created issue numbers and URLs grouped by stage. Trigger `/skill-review` after completion.

---

## Doc Standard

Issues are created in GitHub (not in local files). Body content follows the MD template exactly — no HTML, no decoration. Bulk creation via Python script is the preferred approach when `gh` CLI is unavailable and more than 3 issues need to be created at once.
