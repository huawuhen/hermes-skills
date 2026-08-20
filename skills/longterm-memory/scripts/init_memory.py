#!/usr/bin/env python3
"""Scaffold the Hermes long-term memory store (idempotent, never clobbers)."""
from __future__ import annotations

import datetime as dt
import os
import sys
from pathlib import Path


def memory_root() -> Path:
    configured = os.environ.get("MEMORY_ROOT")
    if configured:
        return Path(configured).expanduser().resolve()
    home = os.environ.get("HERMES_HOME")
    base = Path(home).expanduser() if home else Path.home()
    return (base / "memory").resolve()


TEMPLATES = {
    "SESSION-STATE.md": """# SESSION-STATE.md — Active Working Memory (HOT RAM)

> last-updated: {now}
> This file is the agent's RAM — survives compaction, restart, distraction.

## Current Task
[None]

## Key Context
- 

## Pending Actions
- [ ] None

## Recent Decisions
- 

---
*Write here BEFORE responding (WAL). Promote durable items to MEMORY.md.*
""",
    "MEMORY.md": """# MEMORY.md — Curated Long-Term Memory

> last-updated: {now}
> Keep this file < 5KB. Distill insights from daily logs and topics here.

## About the User
- 

## Active Projects
- 

## Decisions Log
- 

## Lessons Learned
- 

## Preferences
- 

---
*Curated archive — the "good stuff". Detailed notes live in topics/ and daily logs.*
""",
    "lessons.md": """# lessons.md — Mistakes to Avoid & Patterns That Work

> last-updated: {now}

## Mistakes (cost us before)
- 

## Patterns that work
- 
""",
    "topics/decisions.md": """# Decisions Log

> last-updated: {now}

| Date | Decision | Why | Status |
|---|---|---|---|
| {today} |  |  | active |
""",
}


def write_if_missing(path: Path, content: str) -> str:
    if path.exists():
        return f"• exists           {path}"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return f"✓ created          {path}"


def main() -> int:
    root = memory_root()
    now = dt.datetime.now().astimezone().isoformat(timespec="minutes")
    today = dt.date.today().isoformat()
    today_log = root / f"{today}.md"

    print(f"🧠 Long-Term Memory store: {root}\n")
    lines = [write_if_missing(root / rel, tpl.format(now=now, today=today))
             for rel, tpl in TEMPLATES.items()]
    lines.append(write_if_missing(
        today_log,
        f"# {today} — Daily Log\n\n> last-updated: {now}\n\n"
        "## Tasks Completed\n- \n\n## Decisions Made\n- \n\n"
        "## Lessons Learned\n- \n\n## Tomorrow\n- \n"))
    print("\n".join(lines))

    print("\nDone. Resolve scripts/skill at runtime via $HERMES_HOME/skills/note-taking/longterm-memory")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
