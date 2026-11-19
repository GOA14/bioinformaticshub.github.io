#!/usr/bin/env python3
"""Turn a "Join the Bioinformatics Hub" issue form into an entry in _data/members.yml.

Run by .github/workflows/membership.yml. Reads the issue body from the environment,
validates and sanitises every field, then inserts or updates the member block keyed on
the GitHub login of the account that opened the issue -- so nobody can add an entry in
somebody else's name.

Environment
    ISSUE_BODY    raw markdown body of the issue (required)
    ISSUE_AUTHOR  GitHub login of the issue author (required)
    ISSUE_NUMBER  issue number, used in the commit message (optional)
    MEMBERS_FILE  path to the data file (default: _data/members.yml)

Writes `action=added|updated|unchanged`, `name=...` and `login=...` to $GITHUB_OUTPUT.
Exits 1 with a message on $GITHUB_OUTPUT `error=...` when the form cannot be used.
"""
from __future__ import annotations

import os
import re
import sys
import unicodedata
from datetime import date

import yaml

MEMBERS_FILE = os.environ.get("MEMBERS_FILE", "_data/members.yml")
TEMPLATE_MARKER = "# --- Copy the block below"

# Issue-form label (lower-cased) -> members.yml field.
LABEL_TO_FIELD = {
    "full name": "name",
    "institution": "institution",
    "interests": "interests",
    "role or title": "role",
    "career stage": "stage",
    "what do you work on, or what do you want to learn?": "about",
    "location": "location",
    "public email address": "email",
    "website": "website",
    "orcid id": "orcid",
    "orcid": "orcid",
    "x / twitter handle": "twitter",
    "linkedin": "linkedin",
    "bluesky handle": "bluesky",
    "mastodon profile url": "mastodon",
}

# Order fields are written in, so diffs stay readable.
FIELD_ORDER = [
    "name", "github", "institution", "interests", "stage", "about", "team", "role", "location",
    "email", "website", "orcid", "twitter", "linkedin", "bluesky", "mastodon", "joined",
]
REQUIRED = ["name", "github", "institution", "interests", "stage", "about"]

# Stages whose holders must supply an ORCID iD.
ESTABLISHED = {
    "PhD holder", "Postdoctoral researcher", "Faculty / Principal investigator",
    "Research scientist (institute or industry)",
}
STAGES = ESTABLISHED | {"Undergraduate student", "MSc student", "MSc holder", "PhD student", "Other"}
MAX_LEN = {"name": 80, "institution": 120, "interests": 240, "role": 80, "location": 80,
           "stage": 60, "about": 320}

NO_RESPONSE = {"", "_no response_", "none", "n/a", "na", "-"}


def fail(message: str) -> None:
    emit(error=message)
    print(f"::error::{message}")
    sys.exit(1)


def emit(**kwargs: str) -> None:
    path = os.environ.get("GITHUB_OUTPUT")
    if not path:
        return
    with open(path, "a", encoding="utf-8") as fh:
        for key, value in kwargs.items():
            fh.write(f"{key}={value}\n")


def clean(value: str) -> str:
    """Collapse to a single safe line: no control characters, no markdown breakers."""
    value = unicodedata.normalize("NFC", value)
    value = "".join(ch for ch in value if ch == "\t" or not unicodedata.category(ch).startswith("C"))
    value = value.replace("\t", " ").replace("`", "'").replace("<", "(").replace(">", ")")
    return re.sub(r"\s+", " ", value).strip()


def parse_issue_form(body: str) -> dict:
    """Split a GitHub issue-form body ('### Label\n\nvalue') into {label: value}."""
    fields, label, buf = {}, None, []
    for line in body.replace("\r\n", "\n").split("\n"):
        heading = re.match(r"^#{2,4}\s+(.*?)\s*$", line)
        if heading:
            if label is not None:
                fields[label] = "\n".join(buf).strip()
            label = heading.group(1).strip().lower()
            buf = []
        elif label is not None:
            buf.append(line)
    if label is not None:
        fields[label] = "\n".join(buf).strip()
    return fields


def validated(field: str, value: str) -> str | None:
    """Return a cleaned value, or None if the field should be dropped."""
    value = clean(value)
    if value.lower() in NO_RESPONSE:
        return None
    limit = MAX_LEN.get(field, 200)
    if len(value) > limit:
        value = value[:limit].rstrip() + "..."

    if field == "stage":
        return value if value in STAGES else None
    if field == "about":
        return value
    if field == "interests":
        parts = [p.strip() for p in re.split(r"[;,]", value) if p.strip()]
        return ", ".join(parts[:8]) or None
    if field == "email":
        return value if re.fullmatch(r"[^@\s]+@[^@\s]+\.[A-Za-z]{2,}", value) else None
    if field in ("website", "mastodon"):
        if not value.startswith(("http://", "https://")):
            value = "https://" + value.lstrip("/")
        return value if re.fullmatch(r"https?://[\w.-]+(?::\d+)?(?:/\S*)?", value) else None
    if field == "orcid":
        digits = re.sub(r"[^0-9X]", "", value.upper().replace("HTTPS://ORCID.ORG/", ""))
        if len(digits) != 16:
            return None
        return "-".join(digits[i:i + 4] for i in range(0, 16, 4))
    if field == "twitter":
        value = value.lstrip("@").rstrip("/").split("/")[-1]
        return value if re.fullmatch(r"[A-Za-z0-9_]{1,15}", value) else None
    if field == "linkedin":
        value = value.rstrip("/").split("/")[-1]
        return value if re.fullmatch(r"[A-Za-z0-9-]{3,100}", value) else None
    if field == "bluesky":
        value = value.lstrip("@")
        return value if re.fullmatch(r"[A-Za-z0-9.-]{3,253}", value) else None
    return value


def scalar(value) -> str:
    """Dump a single YAML scalar, quoting only when necessary."""
    text = yaml.safe_dump(value, allow_unicode=True, default_flow_style=True, width=10 ** 6)
    return text.replace("\n...", "").strip()


def render(entry: dict) -> str:
    lines = []
    for field in FIELD_ORDER:
        if entry.get(field) not in (None, ""):
            prefix = "- " if not lines else "  "
            lines.append(f"{prefix}{field}: {scalar(entry[field])}")
    for field in sorted(set(entry) - set(FIELD_ORDER)):   # keep unknown fields
        lines.append(f"  {field}: {scalar(entry[field])}")
    return "\n".join(lines)


def surname(entry: dict) -> str:
    return str(entry.get("name", "")).split()[-1].lower() if entry.get("name") else ""


def main() -> None:
    body = os.environ.get("ISSUE_BODY", "")
    login = clean(os.environ.get("ISSUE_AUTHOR", ""))
    if not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9]|-(?=[A-Za-z0-9])){0,38}", login):
        fail(f"'{login}' is not a valid GitHub username.")
    if not body.strip():
        fail("The issue body was empty, so there was nothing to read.")

    raw = parse_issue_form(body)
    entry = {"github": login}
    for label, value in raw.items():
        field = LABEL_TO_FIELD.get(label)
        if not field:
            continue
        cleaned = validated(field, value)
        if cleaned:
            entry[field] = cleaned

    missing = [f for f in REQUIRED if not entry.get(f)]
    if missing:
        fail("These required answers were missing or unreadable: " + ", ".join(missing)
             + ". Edit the issue to fill them in and the bot will try again.")

    if entry.get("stage") in ESTABLISHED and not entry.get("orcid"):
        fail(f"Members at the '{entry['stage']}' stage need an ORCID iD, so that the directory "
             "can be verified. It is free and takes two minutes at https://orcid.org/register "
             "-- add it to the issue above and the bot will try again.")

    text = open(MEMBERS_FILE, encoding="utf-8").read() if os.path.exists(MEMBERS_FILE) else ""
    members = yaml.safe_load(text) or []
    if not isinstance(members, list):
        fail(f"{MEMBERS_FILE} does not contain a YAML list.")

    lines = text.split("\n")
    first = next((i for i, l in enumerate(lines) if re.match(r"^-\s+\w", l)), None)
    marker = next((i for i, l in enumerate(lines) if l.startswith(TEMPLATE_MARKER)), None)
    header = "\n".join(lines[:first]).rstrip() if first is not None else text.rstrip()
    trailer = "\n".join(lines[marker:]).rstrip() if marker is not None else ""

    existing = next((m for m in members
                     if str(m.get("github", "")).lower() == login.lower()), None)
    if existing:
        action = "updated"
        original_login = existing.get("github", login)   # keep the capitalisation on file
        for field in list(LABEL_TO_FIELD.values()):      # blanked answers clear the field
            existing.pop(field, None)
        existing.update(entry)
        existing["github"] = original_login
    else:
        action = "added"
        joined = os.environ.get("JOIN_DATE")
        entry["joined"] = date.fromisoformat(joined) if joined else date.today()
        members.append(entry)

    members.sort(key=lambda m: (surname(m), str(m.get("name", "")).lower()))
    rendered = "\n\n".join(render(m) for m in members)
    out = "\n\n".join(part for part in (header, rendered, trailer) if part) + "\n"

    if out == text:
        action = "unchanged"
    else:
        with open(MEMBERS_FILE, "w", encoding="utf-8") as fh:
            fh.write(out)

    emit(action=action, name=entry["name"], login=login)
    print(f"{action}: {entry['name']} (@{login})")


if __name__ == "__main__":
    main()
