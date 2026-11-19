#!/usr/bin/env python3
"""One-off: move job titles out of `role` and into `title`.

`role` now means a position within the Bioinformatics Hub (Founder, Coordinator,
Administrator) and belongs only to steering committee members. Every other entry's
`role` value is a job title, so this renames the key for non-steering members.

    python scripts/migrate_roles.py          # show what would change
    python scripts/migrate_roles.py --apply  # rewrite the file
"""
import re
import sys
from pathlib import Path

MEMBERS = Path("_data/members.yml")


def main() -> int:
    apply = "--apply" in sys.argv
    lines = MEMBERS.read_text(encoding="utf-8").split("\n")

    # find each entry's line span
    starts = [i for i, l in enumerate(lines) if re.match(r"^- \w", l)]
    changed = []
    for n, start in enumerate(starts):
        end = starts[n + 1] if n + 1 < len(starts) else len(lines)
        block = lines[start:end]
        steering = any(re.match(r"^\s+team:\s*steering\s*$", l) for l in block)
        if steering:
            continue
        for i, l in enumerate(block):
            m = re.match(r"^(\s+)role:(\s.*)$", l)
            if m:
                name = next((b.split(":", 1)[1].strip() for b in block if b.startswith("- name:")), "?")
                changed.append((name, m.group(2).strip()))
                block[i] = f"{m.group(1)}title:{m.group(2)}"
        lines[start:end] = block

    if not changed:
        print("Nothing to migrate: no non-steering entry has a 'role'.")
        return 0
    for name, value in changed:
        print(f"  {name}: role -> title ({value})")
    if apply:
        MEMBERS.write_text("\n".join(lines), encoding="utf-8")
        print(f"\nRewrote {MEMBERS} -- {len(changed)} entr(ies) changed.")
    else:
        print(f"\n{len(changed)} entr(ies) would change. Re-run with --apply to write them.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
