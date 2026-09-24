#!/usr/bin/env python3
"""Preflight — the three environment bugs that kill a container run, checked first.

Every check here exists because a build died on it, or would have. None of them
are about the client's data; they are about whether this machine can read the
client's data at all, and each one has the same failure signature: the file
LOOKS present, the interpreter LOOKS fine, and the build fails somewhere deep
with a message about something else.

1. THE INTERPRETER (bug 3, and the shape of it has moved since it was filed)
   The 09-09 note said "openpyxl is on /usr/bin/python3 and NOT on
   /opt/homebrew/bin/python3.12". Measured 2026-09-09 in this session, that is
   no longer the live shape and the real constraint is tighter:

     /opt/homebrew/bin/python3.12   does not exist any more
     /usr/bin/python3        3.9.6   openpyxl YES   tomllib NO
     /opt/homebrew/bin/python3 3.14.2 openpyxl YES   tomllib YES

   `tomllib` is stdlib only from 3.11, and `mapper.py` imports it at module
   level -- so the interpreter that HAS openpyxl by default is the one that
   cannot import the mapping engine at all. Pinning "the one with openpyxl"
   would have pinned the broken one. The requirement is BOTH, so both are
   checked by import, named, and reported with the interpreter's own path.

2. iCLOUD DATALESS PLACEHOLDERS (bug 2)
   Five of Legrand's eleven source files were dataless on 09-09, including
   `_converted/radiant_us.xlsx`, which the products build reads. `ls` shows
   them at full size. Opening them blocks, or fails. And the check everyone
   reaches for does not see them:

     find -name '*.icloud'   ->  0 hits, on a folder with five placeholders
     stat st_flags & SF_DATALESS (0x40000000)  ->  sees all five

   The `.icloud` sidecar convention is legacy; a modern evicted file keeps its
   real name and gets the SF_DATALESS flag instead. So this is checked by flag,
   never by name. For a cron container it is a HARD BLOCKER: iCloud evicts on
   its own schedule, so a folder that ran yesterday can be half-evicted today
   with nothing in the tree changed.

   Measured now: 0 of 11 Legrand source files are dataless -- they have since
   been hydrated. The hazard is unreproducible today and completely
   undiminished, which is exactly why the check runs every time rather than
   when someone remembers.

3. MISSING INPUTS FAIL LOUDLY (bug 4's class)
   `build_ecat_files.py:39` hardcodes an image list into `~/Downloads` and
   line 535 prints WARNING and returns an empty mapping. Same shape as
   `HIDEABLE_CARRYFORWARD_FILE`, which cost Legrand 19 products' images. So
   every declared input is resolved to an ABSOLUTE path and checked for
   existence, readability and non-zero size BEFORE the build starts, and a
   missing one refuses the run. A warning that scrolls past is not a check.
"""

import os
import subprocess
import sys
import time

# macOS file flag for an evicted iCloud file. The `.icloud` sidecar is the
# legacy representation and is NOT what modern eviction produces.
SF_DATALESS = 0x40000000

MIN_PY = (3, 11)          # tomllib is stdlib from 3.11
REQUIRED_MODULES = ('tomllib',)
XLSX_MODULES = ('openpyxl',)


class PreflightError(RuntimeError):
    """A preflight that failed. The message always names the fix."""


# --- 1. the interpreter -----------------------------------------------------

def check_interpreter(need_xlsx=True):
    """Return (ok, lines). Fails on a missing hard requirement, never warns."""
    lines = []
    problems = []
    lines.append('interpreter : %s' % sys.executable)
    lines.append('version     : %s' % sys.version.split()[0])

    if sys.version_info[:2] < MIN_PY:
        problems.append(
            'Python %d.%d is too old: mapper.py imports tomllib, which is '
            'stdlib only from %d.%d. On this machine use '
            '/opt/homebrew/bin/python3 (3.14.2). NOT /usr/bin/python3 (3.9.6) '
            '-- it has openpyxl but no tomllib, which is the trap.'
            % (sys.version_info[0], sys.version_info[1], MIN_PY[0], MIN_PY[1]))

    need = list(REQUIRED_MODULES) + (list(XLSX_MODULES) if need_xlsx else [])
    for mod in need:
        try:
            __import__(mod)
            lines.append('  %-10s present' % mod)
        except ImportError as exc:
            lines.append('  %-10s MISSING' % mod)
            problems.append(
                '%s is not importable on %s (%s). Pin the interpreter '
                'explicitly; do not rely on `python3` resolving from PATH.'
                % (mod, sys.executable, exc))

    # Reported, never fatal: only --use-db needs it, and the documented path
    # is the MCP. Saying so here stops a container operator concluding the
    # gate is broken when it is merely credential-less.
    try:
        import psycopg2                                        # noqa: F401
        lines.append('  psycopg2   present (--use-db available)')
    except ImportError:
        lines.append('  psycopg2   absent — --use-db unavailable; use '
                     '--emit-sql/--from-results through the MCP')
    return (not problems), lines, problems


# --- 2. iCloud dataless placeholders ----------------------------------------

def is_dataless(path):
    """True if this file is an evicted iCloud placeholder.

    Read by FLAG. `find -name '*.icloud'` returned 0 hits on a Legrand Source
    Data folder holding five placeholders, so the name-based check is not a
    weaker version of this one -- it is a check that cannot fire.
    """
    try:
        return bool(getattr(os.lstat(path), 'st_flags', 0) & SF_DATALESS)
    except OSError:
        return False


def hydrate(path, timeout=120.0):
    """Ask iCloud to materialise one file. Returns (ok, detail).

    `brctl download` is the request; the flag clearing is the confirmation.
    Polling the flag rather than trusting the exit code matters because brctl
    returns 0 for "queued" as readily as for "done", and a queued file is
    still unreadable when the build opens it.
    """
    if not is_dataless(path):
        return True, 'already materialised'
    brctl = '/usr/bin/brctl'
    if os.path.exists(brctl):
        try:
            subprocess.run([brctl, 'download', path], capture_output=True,
                           timeout=30)
        except (subprocess.SubprocessError, OSError) as exc:
            return False, 'brctl download failed: %s' % exc
    deadline = time.time() + timeout
    while time.time() < deadline:
        if not is_dataless(path):
            return True, 'materialised'
        # Reading a byte is a second, independent trigger: on a Mac with
        # iCloud running, an open() on a dataless file starts the fetch.
        try:
            with open(path, 'rb') as fh:
                fh.read(1)
        except OSError:
            pass
        time.sleep(1.0)
    return False, ('still dataless after %.0fs. iCloud has not materialised '
                   'it. A cron container cannot wait on this -- stage the '
                   'source folder outside iCloud.' % timeout)


def check_dataless(paths, do_hydrate=False, timeout=120.0):
    """Return (ok, lines, problems) over an explicit list of files."""
    lines, problems = [], []
    dl = [p for p in paths if is_dataless(p)]
    lines.append('dataless scan: %d of %d declared inputs are iCloud '
                 'placeholders (checked by SF_DATALESS, not by name)'
                 % (len(dl), len(paths)))
    for p in dl:
        if do_hydrate:
            ok, detail = hydrate(p, timeout)
            lines.append('  %-9s %s  (%s)' % ('HYDRATED' if ok else 'FAILED',
                                              p, detail))
            if not ok:
                problems.append('dataless and could not be hydrated: %s (%s)'
                                % (p, detail))
        else:
            lines.append('  DATALESS  %s' % p)
            problems.append(
                'iCloud dataless placeholder: %s\n'
                '     `ls` shows it at full size and opening it fails. Re-run '
                'with --hydrate, or stage the folder outside iCloud.' % p)
    if not dl:
        lines.append('  none — every declared input is materialised on disk')
    return (not problems), lines, problems


# --- 3. declared inputs exist, absolutely -----------------------------------

def collect_declared_paths(mapping, client_root):
    """Every client-tree file path a mapping declares, ABSOLUTE.

    Walks the whole parsed TOML for `path` and `source` string values rather
    than enumerating the keys that carry them today. `inputs.*.path`,
    `inputs.*.files[].path` and `carry_forward.source` are the three that
    exist now; a mapping that grows a fourth must not silently escape the
    existence check, because escaping it is indistinguishable from passing it.
    """
    found = []

    def walk(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if k in ('path', 'source') and isinstance(v, str):
                    found.append(v)
                else:
                    walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    walk(mapping)
    out = []
    for rel in found:
        p = rel if os.path.isabs(rel) else os.path.join(client_root, rel)
        out.append((rel, os.path.abspath(p)))
    return out


def check_inputs(declared):
    """declared = [(relative, absolute)]. Missing or empty refuses the run."""
    lines, problems = [], []
    lines.append('declared inputs: %d' % len(declared))
    for rel, absolute in declared:
        if not os.path.exists(absolute):
            lines.append('  MISSING   %s' % absolute)
            problems.append(
                'declared input does not exist: %s\n'
                '     declared as %r. Absolute paths everywhere; a missing '
                'input fails loudly rather than warning and continuing '
                '(build_ecat_files.py:535 is the anti-pattern).' % (absolute, rel))
            continue
        try:
            size = os.path.getsize(absolute)
        except OSError as exc:
            lines.append('  UNREADABLE %s' % absolute)
            problems.append('declared input unreadable: %s (%s)' % (absolute, exc))
            continue
        if size == 0:
            lines.append('  EMPTY     %s' % absolute)
            problems.append('declared input is 0 bytes: %s' % absolute)
            continue
        lines.append('  ok %9d  %s' % (size, absolute))
    return (not problems), lines, problems
