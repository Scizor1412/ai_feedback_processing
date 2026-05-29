# Skill Review

Triggered automatically after any skill completes. Reviews what happened and surfaces improvements.

## Arguments

`$ARGUMENTS` — name of the skill that just ran (e.g. `issue`, `dev`). If omitted, review the most recent skill in this session.

## Behavior

### Step 1 — Read the log

Look at what the skill actually did in this conversation:
- Did it follow its documented flow exactly?
- Did any step get skipped, combined, or silently changed?
- Were there any tool errors, retries, or workarounds?
- Did it produce the correct output format (HTML vs MD, correct file path, correct GitHub command)?

### Step 2 — Identify improvements

Check against these axes:
- **Correctness** — did the skill do what it promised?
- **Completeness** — were all steps executed?
- **Efficiency** — were there unnecessary steps or redundant calls?
- **Robustness** — what edge cases weren't handled?
- **Doc standard** — was the HTML/MD rule followed?

### Step 3 — Present findings

Output a compact review:

```
## Skill Review: <skill-name>

**What went well:**
- ...

**Issues found:**
- ...

**Suggested improvements to the skill definition:**
- ...
```

Keep it honest and direct. This is a ruthless review, not a praise session.

### Step 4 — Ask the user

Ask: "Any feedback on how this skill ran? Anything you'd change?"

If the user provides feedback, offer to update the skill file immediately.

### Step 5 — Apply updates (if agreed)

Edit `.claude/commands/<skill-name>.md` with the agreed changes. Do not rewrite the whole file — make surgical edits only.
