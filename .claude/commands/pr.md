# PR Skill

Create a pull request when all issues in a GitHub milestone are complete. One PR per milestone (MTP / MUP / MVP).

## Arguments

`$ARGUMENTS` — milestone title or number (e.g. `MTP` or `1`).

---

## Rules

- Never create a PR with open issues in the milestone. Every issue must be closed first.
- Never create a PR directly from `main` or `master` to itself.
- PR description must reference every issue in the milestone with `Closes #N` so GitHub auto-closes them on merge.

---

## Flow

### Step 1 — Verify all milestone issues are closed

Fetch milestone issues via GitHub API:

```python
import json, urllib.request

# GET /repos/{owner}/{repo}/issues?milestone={id}&state=all
# Separate into open vs closed
# If any are open: stop and list them
```

If any issues are still open, stop and say:
> "The following issues are still open in milestone {name}: #N, #M. Complete them with `/dev` and `/commit-push` before creating a PR."

### Step 2 — Ruthless mentor check

Before drafting, stress-test readiness:
- Are all solution docs updated with drift and test evidence?
- Is there at least one commit per closed issue on this branch?
- Does `git log origin/main..HEAD --oneline` show commits for every issue?

If anything is missing, raise it. Do not create a PR for incomplete work.

### Step 3 — Collect change summary

For each closed issue in the milestone:
- Read its title and description
- Read its solution doc in `SOLUTIONS/` if it exists (check drift and test evidence)
- Summarise what was built in 1–2 sentences

### Step 4 — Create the PR via GitHub API

Use a Python script (same pattern as bulk issue creation — stdlib only, token from `.env`):

```python
import json, urllib.request

# POST /repos/{owner}/{repo}/pulls
# {
#   "title": "[{MILESTONE}] {short summary}",
#   "head": "{feature-branch}",
#   "base": "main",
#   "body": pr_body,
#   "draft": False
# }
```

**PR title format:** `[MTP] Ingestion pipeline, AI extraction, CSV generation and review UI`

**PR body must include:**

```markdown
## Summary
{2–4 bullet points summarising what this milestone delivers}

## Issues closed
- Closes #{n} — {issue title}
- Closes #{n} — {issue title}
(one line per issue in the milestone)

## Architecture alignment
Links to relevant sections of ARCHITECTURE/ai-feedback-process-architecture.html

## Test coverage
Summary of what unit tests cover across all issues in this milestone.

## How to review
Step-by-step instructions for a reviewer to verify the changes work end-to-end.

🤖 Generated with Claude Code
```

### Step 5 — Report

Output the PR URL. Trigger `/skill-review pr` after completion.

---

## Milestone setup note

GitHub milestones must exist before this skill can check them. Create milestones in GitHub:
- **MTP** — issues #1–4
- **MUP** — issues #5–9
- **MVP** — issues #10–14

Assign issues to milestones via:
```python
# PATCH /repos/{owner}/{repo}/issues/{number}
# {"milestone": <milestone_id>}
```
Or do it manually in the GitHub UI. This skill cannot create milestones — only read them.
