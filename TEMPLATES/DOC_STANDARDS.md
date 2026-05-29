# Documentation Standards

## The Rule

**HTML is for humans. Markdown is for AI.**

| Format | Audience | Priorities |
|---|---|---|
| `.html` | Human readers | Interactive, attractive, scannable UI; use tabs, color, cards, collapsibles |
| `.md` | AI context (Claude, tools) | Short, simple, sufficient; strip all decoration; every word must earn its place |

## Apply This Rule To

- Solution docs (`SOLUTIONS/*.html`) — always HTML, always interactive
- Issue templates (`TEMPLATES/*.md`) — always MD, kept minimal
- This file and CLAUDE.md — MD, for AI consumption

## Violations to Avoid

- Do not create a `.md` solution doc "for simplicity" — it defeats the human readability goal
- Do not bloat `.md` files with headers, tables, or prose beyond what's needed for AI parsing
- Do not create `.html` files intended only for AI reading
