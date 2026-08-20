---
name: longterm-memory
description: "Use when a correction, decision, or preference must persist."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [memory, long-term-memory, wal, context, hygiene, sessions]
---

# Long-Term Memory Discipline

A platform-native memory system for Hermes. No openclaw/clawdbot, no LanceDB, no extra API keys.
It layers **Hermes's built-in `memory` tool** (small durable facts injected every turn)
on top of a **markdown file store** (larger structured context, decisions, lessons, daily logs).

**Rule hierarchy:** Hermes `memory` tool = your "hot RAM" (always in context). The file store = your
"disk" (durable, human-readable, paginated on demand). `session_search` = your "library catalog".

## When to use

- User states a **preference**, **correction**, or personal detail → write it, then respond (**WAL**).
- A **decision with long-term consequences** is made → log it to decisions in the file store.
- You **repeated a mistake** → append to `lessons.md`.
- A session ends / a bounded chunk of work finishes → update today's daily log + SESSION-STATE.md.
- User asks "what did we decide about X" → search the file store, then `session_search` if needed.

## Storage layout (MEMORY_ROOT)

Default root: `$HERMES_HOME/memory` (i.e. `/root/.hermes/memory` here). Override with env
`MEMORY_ROOT` (e.g. a per-project folder). Resolve it at runtime; do not hardcode paths.

```
memory/
├── SESSION-STATE.md      # HOT RAM: current task, key context, pending, recent decisions
├── MEMORY.md             # CURATED long-term: distilled, human-readable, keep it <5KB
├── YYYY-MM-DD.md         # daily logs (rolling)
├── topics/               # topic-specific deep files (project, tech, etc.)
└── lessons.md            # mistakes to avoid + patterns that work
```

Every file starts with a `last-updated` line so staleness is visible.

## WAL Protocol (Critical)

**Write BEFORE responding.** If compaction/crash/restart happens before you save, context is lost.

| Trigger | Action before responding |
|---|---|
| User states a preference | `memory` add → then respond |
| User corrects you | `memory` replace/remove stale → write correction → then respond |
| User makes a decision | append to SESSION-STATE.md "Recent Decisions" → respond |
| User gives a deadline/commitment | write to SESSION-STATE.md "Pending Actions" → respond |

## Mapping to Hermes primitives

| Need | Tool |
|---|---|
| Small durable facts, preferences, corrections | `memory` tool (`target='user'` for who the user is, `target='memory'` for agent notes) |
| Larger structured context, decisions, lessons, logs | read/write files under `memory/` |
| Recall past conversations | `session_search` (query) |
| Session-scoped working memory, survives compaction mid-task | `memory/SESSION-STATE.md` |

Cap rule: if the durable fact is ≤ ~2 short lines, it belongs in the `memory` tool. Longer or
table-like → file store. Don't duplicate the same fact in both.

## Routine

### On session start / when asked "where are we"
1. Read `SESSION-STATE.md` (hot context).
2. Read today's daily log if it exists.
3. Grep `MEMORY.md` + `topics/` for anything matching the task before answering.

### During conversation
1. Concrete detail / correction / preference → **WAL write first**.
2. Meaningful decision → append to SESSION-STATE.md + `topics/decisions.md`.
3. Mistake → append to `lessons.md` silently.

### On session end / bounded milestone
1. Update `SESSION-STATE.md` (current task → done/next).
2. Promote durable items from SESSION-STATE to `MEMORY.md` (curated, keep small) and today's daily log.
3. Preserve the original source lines; never delete a decision without a note.

### Hygiene (weekly, or when MEMORY.md grows)
1. Archive completed work out of `SESSION-STATE.md`.
2. Fold daily logs into `MEMORY.md` / `topics/`; keep logs for history.
3. Prune stale `memory` tool entries in one batch call (remove + add together).
4. Re-scan lessons.md; keep only still-true lessons.

## Commands

```bash
# Scaffold the store (idempotent: never overwrites existing content)
python3 "$(skill_dir)/scripts/init_memory.py"

# Show store health (sizes, staleness, daily-log count)
python3 "$(skill_dir)/scripts/status.py"
```

Resolve scripts relative to this SKILL.md, not the caller's cwd.

## Pitfalls

- **Don't** follow `memory_recall` / `clawdbot` / LanceDB commands — they came from the original
  OpenClaw skill and do not exist in Hermes. Use `memory`, files, and `session_search`.
- **Don't** bloat the `memory` tool with big logs or raw transcripts — char budget is limited;
  that's what the file store and `session_search` are for.
- **Don't** overwrite an existing memory file. Follow the templates; append, never clobber.
- Verify a file actually exists before telling the user it was written.

## Handoff

Return a compact result: file path(s) touched, what changed, and (when asked) the one-line
"where are we" summary. Route to `session_search` for deep recall of older sessions.
