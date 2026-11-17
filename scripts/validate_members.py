#!/usr/bin/env python3
"""Check _data/members.yml before it is merged.

Run by .github/workflows/validate.yml on every pull request that touches the file,
and usable locally:  python scripts/validate_members.py
"""
from __future__ import annotations

import re
import sys

import yaml

MEMBERS_FILE = "_data/members.yml"
REQUIRED = ["name", "github", "institution", "interests"]
ALLOWED = set(REQUIRED) | {
    "team", "role", "location", "email", "website", "orcid",
    "twitter", "linkedin", "bluesky", "mastodon", "joined",
}
PATTERNS = {
    "github": r"[A-Za-z0-9](?:[A-Za-z0-9]|-(?=[A-Za-z0-9])){0,38}",
    "email": r"[^@\s]+@[^@\s]+\.[A-Za-z]{2,}",
    "website": r"https?://\S+",
    "mastodon": r"https?://\S+",
    "orcid": r"\d{4}-\d{4}-\d{4}-\d{3}[\dX]",
    "twitter": r"[A-Za-z0-9_]{1,15}",
    "joined": r"\d{4}-\d{2}-\d{2}",
    "team": r"steering|member",
}


def main() -> int:
    with open(MEMBERS_FILE, encoding="utf-8") as fh:
        members = yaml.safe_load(fh)

    problems: list[str] = []
    if not isinstance(members, list):
        print(f"{MEMBERS_FILE} must contain a YAML list of members.")
        return 1

    seen: dict[str, str] = {}
    for i, m in enumerate(members, 1):
        where = f"entry {i}"
        if not isinstance(m, dict):
            problems.append(f"{where}: not a mapping (check the indentation).")
            continue
        where = f"entry {i} ({m.get('name') or m.get('github') or 'unnamed'})"

        for field in REQUIRED:
            if not str(m.get(field, "")).strip():
                problems.append(f"{where}: missing required field '{field}'.")
        for field in set(m) - ALLOWED:
            problems.append(f"{where}: unknown field '{field}'. Allowed: {', '.join(sorted(ALLOWED))}.")
        for field, pattern in PATTERNS.items():
            value = m.get(field)
            if value not in (None, "") and not re.fullmatch(pattern, str(value)):
                problems.append(f"{where}: '{field}' value {value!r} does not look right.")

        login = str(m.get("github", "")).lower()
        if login:
            if login in seen:
                problems.append(f"{where}: duplicate GitHub username, already used by {seen[login]}.")
            seen[login] = where

    if problems:
        print(f"{len(problems)} problem(s) in {MEMBERS_FILE}:\n")
        for p in problems:
            print(" -", p)
            print(f"::error file={MEMBERS_FILE}::{p}")
        return 1

    print(f"{MEMBERS_FILE}: {len(members)} member(s), all valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
