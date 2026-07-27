#!/usr/bin/env python3
"""Shared primitives for the pre-import gate.

Three tiers, matching the existing validators so a phase gate can branch on the
exit code, plus a fourth that exists purely so a skipped check stays visible:

    FAIL    exit 1  blocks the import
    WARNING exit 0  advisory
    SKIP    exit 0  inapplicable for this client, with the flag that caused it
    ERROR   exit 2  the check could not run at all (unreadable file, missing input)

SKIP is not cosmetic. An unexplained absence is how "we don't do options for this
client" gets forgotten and re-litigated a quarter later, so every skipped check
prints its reason.
"""
import csv
import re

FAIL = "FAIL"
WARNING = "WARNING"
SKIP = "SKIP"
ERROR = "ERROR"

EXIT_OK = 0
EXIT_FAIL = 1
EXIT_ERROR = 2

BOM_BYTES = b"\xef\xbb\xbf"


class Finding:
    """One thing a check found. `where` is a row number, filename, or code."""

    __slots__ = ("severity", "check", "message", "where")

    def __init__(self, severity, check, message, where=None):
        self.severity = severity
        self.check = check
        self.message = message
        self.where = where

    def render(self):
        prefix = f"{self.where}: " if self.where else ""
        return f"{prefix}{self.message}"

    def __repr__(self):
        return f"Finding({self.severity}, {self.check}, {self.message!r})"


def fail(check, message, where=None):
    return Finding(FAIL, check, message, where)


def warn(check, message, where=None):
    return Finding(WARNING, check, message, where)


def skip(check, message):
    return Finding(SKIP, check, message)


def error(check, message, where=None):
    return Finding(ERROR, check, message, where)


class Report:
    """Collects findings across checks and renders the gate output."""

    def __init__(self, title=""):
        self.title = title
        self.findings = []
        self.notes = []
        self.ran = []

    def add(self, findings):
        if findings is None:
            return self
        if isinstance(findings, Finding):
            findings = [findings]
        self.findings.extend(findings)
        return self

    def note(self, text):
        self.notes.append(text)
        return self

    def record(self, check_name):
        if check_name not in self.ran:
            self.ran.append(check_name)
        return self

    def of(self, severity):
        return [f for f in self.findings if f.severity == severity]

    @property
    def exit_code(self):
        if self.of(ERROR):
            return EXIT_ERROR
        return EXIT_FAIL if self.of(FAIL) else EXIT_OK

    def render(self):
        out = []
        if self.title:
            out.append(self.title)
            out.append("")
        for text in self.notes:
            out.append(text)
        if self.notes:
            out.append("")

        for severity, label, bullet in (
            (SKIP, "SKIPPED", "~"),
            (WARNING, "WARNINGS", "?"),
            (ERROR, "ERRORS", "!"),
            (FAIL, "FAILURES", "-"),
        ):
            group = self.of(severity)
            if not group:
                continue
            if severity == SKIP:
                out.append(f"{label} ({len(group)}) — not applicable to this client:")
            elif severity == WARNING:
                out.append(f"{label} ({len(group)}) — advisory, do not block import:")
            elif severity == ERROR:
                out.append(f"{label} ({len(group)}) — check could not run:")
            else:
                out.append(f"{label} ({len(group)}) — these block the import:")
            for f in group:
                out.append(f"  {bullet} [{f.check}] {f.render()}")
            out.append("")

        checks = len(self.ran)
        if self.of(FAIL):
            out.append(f"FAIL: {len(self.of(FAIL))} blocking issue(s) across {checks} check(s)")
        elif self.of(ERROR):
            out.append(f"ERROR: {len(self.of(ERROR))} check(s) could not run")
        else:
            tail = f" ({len(self.of(WARNING))} advisory)" if self.of(WARNING) else ""
            out.append(f"PASS: no blocking issues across {checks} check(s){tail}")
        return "\n".join(out)


# --- CSV primitives -------------------------------------------------------------
# The importer downcases every header, so all lookups here are case-insensitive.
# Reading with utf-8-sig means a BOM never breaks *our* parse; the BOM check reads
# the raw bytes separately, because the importer's header validator does not.


def load_rows(path):
    """Return (rows, header_lookup). header_lookup maps lowercase -> actual name."""
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            return [], {}
        lookup = {name.strip().lower(): name for name in reader.fieldnames}
        return list(reader), lookup


def get(row, lookup, field):
    actual = lookup.get(field.lower())
    return (row.get(actual) or "").strip() if actual else ""


def split_codes(value, sep=","):
    return [c.strip() for c in value.split(sep) if c.strip()]


def has_bom(path):
    """True if the file starts with the three bytes EF BB BF."""
    with open(path, "rb") as f:
        return f.read(3) == BOM_BYTES


def first_header_name(path):
    """The first header cell as the importer's header validator would see it."""
    with open(path, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            return row[0] if row else ""
    return ""


def column_values(rows, lookup, field):
    return [get(r, lookup, field) for r in rows]


def is_url(value):
    return bool(re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", value.strip()))
