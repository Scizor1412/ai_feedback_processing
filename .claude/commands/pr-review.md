# PR Review Skill

Review code in a pull request against project standards — Karpathy's 4 rules, architecture decisions, and correctness. If blocking issues are found, trigger `/dev` to fix them before the PR merges.

## Arguments

`$ARGUMENTS` — PR number (e.g. `3`), or omit to review the most recent open PR on the current branch.

---

## Rules

- Findings are classified as **blocking** (must fix before merge) or **advisory** (improvement, not required).
- Only blocking findings trigger `/dev`. Do not reopen issues for advisory items.
- Be a ruthless reviewer. Do not soften criticism. A finding that "might cause issues" is blocking if it can cause a real failure.
- Do not comment on style that has no functional impact.

---

## Review Criteria

### 1. Correctness (blocking if violated)
- Does the code match what the linked issue's acceptance criteria require?
- Are there logic errors, off-by-one mistakes, or incorrect conditionals?
- Are all error paths handled — failed API calls, malformed inputs, empty results?
- Are database writes atomic where they need to be?

### 2. Karpathy's 4 rules (blocking if violated)
- **Start simple:** Is there speculative complexity — abstractions, generalisations, or configurability that no issue asked for?
- **End-to-end first:** Does any component lack a runnable path from input to output?
- **No guessing:** Are there TODO/FIXME comments hiding unverified assumptions? Any `except: pass` swallowing errors silently?
- **Surgical changes:** Does the diff touch code unrelated to the issue? (Formatting changes, unrelated refactors — flag and revert.)

### 3. Architecture alignment (blocking if violated)
- Check `ARCHITECTURE/ai-feedback-process-architecture.html` for the relevant component's ADR.
- Does the implementation match the chosen solution (e.g. FastAPI not Flask, Qdrant not pgvector)?
- Does any new external dependency contradict an architectural decision? If so, it needs a new ADR before merging.

### 4. Security (blocking if violated)
- Is `GITHUB_TOKEN` or any secret hardcoded anywhere in the diff?
- Are there SQL queries built via string concatenation (injection risk)?
- Are there any file paths constructed from user input without sanitisation?

### 5. Tests (blocking if violated)
- Does each changed module have corresponding test coverage?
- Do the tests match the unit tests listed in the GitHub issue?
- Are tests asserting real behaviour or just that the function runs without error?

### 6. Advisory (non-blocking — report but do not block merge)
- Variable or function names that are unclear
- Missing docstring on a non-obvious function
- Opportunity to simplify without changing behaviour

---

## Flow

### Step 1 — Fetch the PR diff

```python
import urllib.request, json

# GET /repos/{owner}/{repo}/pulls/{number}/files
# Returns list of changed files with patch (unified diff)
# Also GET /repos/{owner}/{repo}/pulls/{number} for PR metadata (title, body, linked issues)
```

Read the full diff. Also read each changed file in full from the local working tree for context beyond the diff window.

### Step 2 — Read linked issues and solution docs

From the PR body, extract all `Closes #N` issue references. For each:
- Read the issue (GitHub API: `GET /repos/{owner}/{repo}/issues/{n}`)
- Read the solution doc `SOLUTIONS/<n>-*-solution.html` if it exists

This is the source of truth for what the code must do and what tests are required.

### Step 3 — Run the review

Apply every criterion above to the diff. For each finding, record:
- **Type:** blocking or advisory
- **File and line:** `path/to/file.py:42`
- **Rule violated:** which of the 5 criteria
- **Finding:** what is wrong
- **Fix:** what exactly needs to change (be specific — not "improve error handling")

### Step 4 — Present findings

Output a structured review:

```
## PR Review: #{number} — {title}

### Blocking issues ({count})

**[B1] path/to/file.py:42 — Correctness**
Finding: ...
Fix: ...

**[B2] path/to/file.py:88 — Karpathy / No guessing**
Finding: ...
Fix: ...

### Advisory ({count})

**[A1] path/to/file.py:15 — Simplification**
Finding: ...
Suggestion: ...

### Verdict
{APPROVE / REQUEST CHANGES}
```

If there are **zero blocking issues**, say: "No blocking issues. PR is clear to merge."

### Step 5 — Fix blocking issues

If there are blocking issues, ask:
> "There are {N} blocking issues. Should I fix them now using `/dev`, or do you want to review the list first?"

If the user says to fix:
- Group blocking issues by the issue they belong to (from the linked `Closes #N`)
- Run `/dev <issue_number>` for each affected issue, providing the specific blocking findings as context
- After each fix, re-run the review on that section of the diff to confirm the issue is resolved

### Step 6 — Trigger review

Run `/skill-review pr-review` after the review is delivered.
