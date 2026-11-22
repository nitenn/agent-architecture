#!/usr/bin/env python3
"""Check relative Markdown links in the Agent knowledge repository."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def main() -> int:
    errors: list[str] = []
    files = [ROOT / "README.md", ROOT / "AGENTS.md"]
    files.extend(sorted((ROOT / "docs").rglob("*.md")))
    for source in files:
        if not source.exists():
            continue
        for href in LINK.findall(source.read_text(encoding="utf-8")):
            parsed = urlsplit(href)
            if parsed.scheme or href.startswith(("#", "mailto:")):
                continue
            target = (source.parent / unquote(parsed.path)).resolve()
            if not target.exists():
                errors.append(f"{source.relative_to(ROOT)} -> {href}")

    if errors:
        print("broken links:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("links ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
