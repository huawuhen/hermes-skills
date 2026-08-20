#!/usr/bin/env python3
"""Report health of the Hermes long-term memory store."""
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


def fmt_size(n: int) -> str:
    return f"{n/1024:.1f}KB"


def main() -> int:
    root = memory_root()
    print(f"🧠 Memory store: {root}\n")
    if not root.exists():
        print("✗ store missing — run scripts/init_memory.py first")
        return 1

    now = dt.datetime.now().astimezone()
    today = dt.date.today().isoformat()
    checks = []

    for name in ("SESSION-STATE.md", "MEMORY.md"):
        p = root / name
        if p.exists():
            size = p.stat().st_size
            age = dt.datetime.fromtimestamp(p.stat().st_mtime, tz=now.tzinfo)
            days = (now - age).days
            warn = "  ⚠ stale" if days > 14 else ""
            checks.append(f"✓ {name:<16} {fmt_size(size):>8}  {days}d ago{warn}")
        else:
            checks.append(f"✗ {name:<16} missing")

    log_dir = root
    dailies = sorted(p for p in log_dir.glob("????-??-??.md") if p.name.startswith("2"))
    if dailies:
        latest = dailies[-1]
        checks.append(f"✓ daily logs      {len(dailies)} (latest {latest.name})")
    else:
        checks.append("• no daily logs yet")

    topics = root / "topics"
    if topics.exists():
        n = len([p for p in topics.iterdir() if p.is_file()])
        checks.append(f"✓ topics/         {n} file(s)")
    else:
        checks.append("• topics/ not created yet")

    if (root / "lessons.md").exists():
        checks.append("✓ lessons.md      present")
    else:
        checks.append("• lessons.md missing")

    print("\n".join(checks))

    memory_md = root / "MEMORY.md"
    if memory_md.exists() and memory_md.stat().st_size > 5 * 1024:
        print("\n⚠ MEMORY.md exceeds 5KB — consider folding detail into topics/ or daily logs.")
    if today and (root / f"{today}.md").exists() is False:
        print("\n• Today's daily log not created yet — run: python3 scripts/init_memory.py")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
