# Dev Skill

Implement work tied to an open GitHub issue, following the full planning → approval → implementation flow.

## Arguments

`$ARGUMENTS` — issue number (e.g. `42`) or issue URL.

## Rules

- Never start implementation without an open issue. If no issue exists, stop and say: "Run `/issue` first."
- Never start implementation without explicit user approval of the solution document.
- Never implement on `main` or `master`. Always work on a feature branch.

---

## Flow

### Step 1 — Read the issue

Read every field via GitHub API (gh CLI is not installed):

```python
import json, urllib.request
token = [l.split('=',1)[1].strip().strip('"').strip("'") for l in open('.env') if l.startswith('GITHUB_TOKEN=')][0]
req = urllib.request.Request(f'https://api.github.com/repos/Scizor1412/ai_feedback_processing/issues/<number>')
req.add_header('Authorization', f'Bearer {token}')
req.add_header('Accept', 'application/vnd.github.v3+json')
with urllib.request.urlopen(req) as r:
    print(json.loads(r.read())['body'])
```

If the issue is vague, ask clarifying questions (ruthless mentor mode) before proceeding.

### Step 1b — Create and switch to a feature branch

Check the current branch. If already on a correctly named feature branch for this issue, skip. Otherwise:

```bash
git checkout main && git pull  # ensure branch is from latest main
git checkout -b feat/<issue-number>-<kebab-issue-title>
```

Branch name format: `feat/<number>-<short-kebab-description>` — e.g. `feat/2-ai-extraction-engine`.

If a branch for this issue already exists locally, check it out instead of creating a new one:
```bash
git checkout feat/<issue-number>-*
```

Do not start writing any files until the branch is confirmed.

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

Post a completion comment via GitHub API:

```python
import json, urllib.request
token = [l.split('=',1)[1].strip().strip('"').strip("'") for l in open('.env') if l.startswith('GITHUB_TOKEN=')][0]
body = json.dumps({'body': 'Implementation complete. Branch: feat/<number>-<title>\n\nSolution doc: SOLUTIONS/<file>.html\n\nAll unit tests passing.'})
req = urllib.request.Request('https://api.github.com/repos/Scizor1412/ai_feedback_processing/issues/<number>/comments', data=body.encode())
req.add_header('Authorization', f'Bearer {token}')
req.add_header('Accept', 'application/vnd.github.v3+json')
req.add_header('Content-Type', 'application/json')
with urllib.request.urlopen(req) as r:
    print('Comment:', json.loads(r.read())['html_url'])
```

Trigger `/skill-review` after completion.

## Doc Standard

Solution files are **HTML** (human-readable, interactive). The template in `TEMPLATES/solutions_template.html` is the source of truth. Never create a `.md` solution file.
