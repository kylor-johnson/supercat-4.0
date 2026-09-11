#!/usr/bin/env python3
"""Content pins for ANY file the mapping layer compares against.

## Why this is not just for baselines

Task 1 pinned the three reproduction baselines. It did not pin the ANSWER KEY,
which was read straight off disk — and that is the file that caused damage.

libco's `products.csv` is dated 2026-07-13 and is superseded by a September
patch. Scoring the blind run against it produced two confident, wrong findings:
that the build had deliberately excluded 75 SKUs (it had not — the file was
stale) and that libco hard-cuts LongDesc at 50 characters like Legrand (it does
not — that was a defect, since fixed; the script's constant is 255). Both
retractions came from an unpinned comparison target.

So the rule is: **any file whose content a conclusion depends on gets a hash and
a date.** Three roles, one mechanism:

    baseline    a file the mapping must REPRODUCE
    reference   an answer key or scoring target the mapping is COMPARED to
    input       a client source file whose content a finding cites

A scoring run against an unpinned or stale reference must refuse, or stamp every
line of its output with the staleness. Silence is the failure mode that already
cost two findings.
"""

import datetime
import hashlib
import os
import tomllib

HERE = os.path.dirname(os.path.abspath(__file__))
BASELINES = os.path.join(HERE, 'baselines.toml')

OK, STALE, UNPINNED, MISSING = 'pinned', 'STALE', 'UNPINNED', 'MISSING'


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b''):
            h.update(chunk)
    return h.hexdigest()


def measure(path):
    with open(path, 'rb') as fh:
        data = fh.read()
    lines = data.count(b'\n')
    if data and not data.endswith(b'\n'):
        lines += 1
    return {'sha256': hashlib.sha256(data).hexdigest(),
            'bytes': len(data), 'rows': max(lines - 1, 0)}


def load(path=BASELINES):
    if not os.path.exists(path):
        return {'baseline': [], 'reference': [], 'history': []}
    with open(path, 'rb') as fh:
        doc = tomllib.load(fh)
    for k in ('baseline', 'reference', 'history'):
        doc.setdefault(k, [])
    return doc


def _index(doc):
    """Pins addressable by basename AND by (client, key)."""
    by_name = {}
    for kind in ('baseline', 'reference'):
        for p in doc[kind]:
            p = dict(p, kind=kind)
            by_name.setdefault(os.path.basename(p['path']), []).append(p)
    return by_name


def verify(file_path, doc=None):
    """Return (status, pin_or_None, measured_or_None)."""
    doc = doc or load()
    if not os.path.exists(file_path):
        return MISSING, None, None
    m = measure(file_path)
    candidates = _index(doc).get(os.path.basename(file_path), [])
    for pin in candidates:
        if pin['sha256'] == m['sha256']:
            return OK, pin, m
    if candidates:
        return STALE, candidates[0], m
    return UNPINNED, None, m


def stamp(file_path, doc=None):
    """One line describing the trust status of a comparison target."""
    status, pin, m = verify(file_path, doc)
    name = os.path.basename(file_path)
    if status == MISSING:
        return '!! MISSING        %s' % name
    if status == OK:
        return '   pinned %s  %s (%d bytes) — %s' % (
            pin['pinned_on'], name, m['bytes'], pin.get('role') or pin.get('produced_by', ''))
    if status == STALE:
        return ('!! STALE          %s is %d bytes; the pin from %s was %d. '
                'Conclusions drawn from it are unattributable.'
                % (name, m['bytes'], pin['pinned_on'], pin['bytes']))
    return ('!! UNPINNED       %s (%d bytes, %d rows) — no hash, no date. '
            'Pin it before drawing a conclusion from it.'
            % (name, m['bytes'], m['rows']))


def require(paths, allow_unpinned=False):
    """Gate a scoring run. Returns (ok, lines).

    ok=False means REFUSE. With allow_unpinned=True it never refuses, but the
    caller must print every returned line alongside its output -- that is the
    "or at minimum stamp every line" half of the rule.
    """
    doc = load()
    lines, bad = [], []
    for p in paths:
        lines.append(stamp(p, doc))
        status, _, _ = verify(p, doc)
        if status != OK:
            bad.append((p, status))
    if bad and not allow_unpinned:
        lines.append('')
        lines.append('REFUSING to score: %d comparison target(s) are not pinned '
                     'to a known content hash.' % len(bad))
        lines.append('Pin them, with a reason:')
        for p, status in bad:
            lines.append('   python3 mapping/bless.py --reference %r \\' % p)
            lines.append('       --role "..." --reason "..."')
        lines.append('Or re-run with --allow-unpinned, which stamps every line '
                     'of output as untrusted.')
        return False, lines
    return True, lines
