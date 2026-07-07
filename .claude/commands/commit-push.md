# Commit Push Skill

Commit and push completed implementation for a single issue. Only run this after `/dev` is fully complete: solution doc approved, code implemented, unit tests passing.

## Arguments

`$ARGUMENTS` — issue number (e.g. `42`).

---

## Pre-flight gates — ALL must pass before committing

Verify each gate explicitly. Do not skip or assume. If any gate fails, stop and state which gate failed and what needs to be done.

**Gate 1 — Solution doc is complete**
Check that `SOLUTIONS/<issue-number>-*-solution.html` exists and the implementation tab is filled in:
- `{{DRIFT_1}}` is replaced with actual drift notes (or "None" if no drift)
- `{{TEST_EVIDENCE}}` is replaced with actual test results

If placeholders remain, stop: "Update the solution doc implementation tab before committing."

**Gate 2 — Tests pass**
Ask the user directly: "Confirm: all unit tests for issue #N pass. Run them now if you haven't."
Do not assume. Wait for explicit confirmation. If tests are failing, stop: "Fix failing tests before committing. Run `/dev <number>` to continue."

**Gate 3 — Correct branch**
Check `git branch --show-current`. The current branch must NOT be `main` or `master`.
If on main/master, stop: "Create a feature branch first: `git checkout -b feat/<issue-number>-<short-description>`."

**Gate 4 — No secrets staged**
Run `git diff --cached --name-only` and `git status --short`. Confirm `.env` is not staged. If it appears, run `git rm --cached .env` before proceeding.

---

## Flow

### Step 1 — Stage only relevant files

Use `git status --short` to see all changed files. Stage only files directly related to the issue — do not use `git add .` blindly. Exclude:
- `.env`, any file matching `*.env`
- `DUMMY_DATA/` (generated test data, not source)
- Any file the user flags as not ready

```bash
git add <specific files>
```

### Step 2 — Commit with structured message

Classify the issue type (feature/bug) and write the commit message:

- Feature: `feat(#{n}): <short imperative description>`
- Bug fix: `fix(#{n}): <short imperative description>`

Body must include:
- One-line summary of what changed
- `Refs #<n>` (do not use `Closes` — the issue closes via PR, not commit)

Format:
```
git commit -m "$(cat <<'EOF'
feat(#42): short description of what was implemented

Summary of key changes made. One or two sentences max.

Refs #42

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
EOF
)"
```

### Step 3 — Push to remote

`gh` CLI is not installed. Push using `GITHUB_TOKEN` from `.env`:

```bash
TOKEN=$(grep GITHUB_TOKEN .env | cut -d= -f2 | tr -d '"' | tr -d "'")
BRANCH=$(git branch --show-current)
REPO=$(git remote get-url origin | sed 's|.*github\.com[:/]||' | sed 's|\.git$||')
git push "https://${TOKEN}@github.com/${REPO}.git" HEAD:"${BRANCH}" --set-upstream 2>&1 \
  | grep -v "github_pat\|github_token\|://.*@github"
```

`sed 's|.*github\.com[:/]||'` strips everything up to and including `github.com/` (or `github.com:` for SSH remotes), leaving `owner/repo`. The `grep -v` strips any output line containing the token so it never appears in the terminal.

### Step 4 — Comment on the GitHub issue

Post a completion comment via GitHub API:

```python
import json, urllib.request

token = open('.env').read()
# parse GITHUB_TOKEN from .env
# POST /repos/{owner}/{repo}/issues/{number}/comments
# body: "Implementation complete. Branch: {branch}. Solution doc: SOLUTIONS/{file}.html"
```

### Step 5 — Trigger review

Run `/skill-review commit-push` after completion.

---

## What this skill does NOT do

- Does not close the issue (closed by PR via `Closes #N` in PR description)
- Does not create a PR (use `/pr` when all milestone issues are done)
- Does not run tests (user confirms tests pass in Gate 2)
