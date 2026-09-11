#!/usr/bin/env python3
"""Pin and re-bless acceptance baselines.

WHY THIS EXISTS. leg and mer are both mid-onboarding, so their baselines are
still moving. When Legrand's build legitimately changes, `products.csv` stops
being 404,798 bytes and the acceptance test goes red FOR A CORRECT REASON. A
gate that false-alarms gets switched off -- that is what happened to B1b
(OPEN_ITEMS G3), and a switched-off gate protects nothing.

So the test has to tell two failures apart:

    the BASELINE moved   -> a human decides: re-bless, or investigate the build
    the MAPPING broke    -> a regression, fix the mapping

It can only do that if it knows what the baseline was WHEN IT LAST PASSED. That
is what `baselines.toml` records: content hash, size, rows, the date it was
pinned, and which build produced it.

RE-BLESSING IS A DELIBERATE, RECORDED ACT. It is this command, with a mandatory
`--reason`, and it appends the superseded pin to a history block rather than
overwriting it. It is not an edit to a number in a test file, because a number
edited in a test file leaves no trace of who decided the new value was right.

    bless.py --list                       show every pin against the live file
    bless.py leg products --reason "..."  re-bless one baseline
    bless.py --all --reason "..."         re-bless everything that moved

Read-only with respect to client data: it hashes files and writes only
`mapping/baselines.toml`.
"""

import datetime
import hashlib
import os
import sys
import tomllib

HERE = os.path.dirname(os.path.abspath(__file__))
BASELINES = os.path.join(HERE, 'baselines.toml')

# client -> (root env label, key -> relative path)
TARGETS = {
    'leg': {'products': 'Build/products.csv',
            'inventory': 'Build/inventory.csv'},
    'mer': {'products': 'Import Files/products.csv'},
}


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b''):
            h.update(chunk)
    return h.hexdigest()


def measure(path):
    with open(path, 'rb') as fh:
        data = fh.read()
    # Data rows: total lines minus the header. Counted, not derived from a
    # separate parse -- a row count that disagrees with the file it describes
    # is worse than no row count.
    lines = data.count(b'\n')
    if data and not data.endswith(b'\n'):
        lines += 1
    return {'sha256': sha256(path), 'bytes': len(data), 'rows': max(lines - 1, 0)}


def load():
    if not os.path.exists(BASELINES):
        return {'baseline': [], 'reference': [], 'history': []}
    with open(BASELINES, 'rb') as fh:
        d = tomllib.load(fh)
    for k in ('baseline', 'reference', 'history'):
        d.setdefault(k, [])
    return d


def esc(s):
    return str(s).replace('\\', '\\\\').replace('"', '\\"')


def save(doc):
    out = [
        '# Acceptance baselines -- pinned by content hash.',
        '#',
        '# Written ONLY by mapping/bless.py. Do not hand-edit: a baseline edited',
        '# by hand records no reason and no date, which is the whole point of',
        '# pinning it. Re-bless with:',
        '#',
        '#     python3 mapping/bless.py <client> <key> --reason "..."',
        '#',
        '# `superseded` below is the audit trail. It is append-only.',
        '',
    ]
    for b in doc['baseline']:
        out.append('[[baseline]]')
        for k in ('client', 'key', 'path', 'sha256'):
            out.append('%s = "%s"' % (k, esc(b[k])))
        for k in ('bytes', 'rows'):
            out.append('%s = %d' % (k, b[k]))
        for k in ('pinned_on', 'produced_by', 'reason'):
            out.append('%s = "%s"' % (k, esc(b.get(k, ''))))
        out.append('')
    if doc.get('reference'):
        out.append('# --- comparison targets: answer keys and scoring references ---')
        out.append('#')
        out.append('# NOT reproduction baselines. These are files a CONCLUSION is')
        out.append('# drawn from. libco\'s stale products.csv sat here unpinned and')
        out.append('# produced two wrong findings before anyone noticed its date.')
        out.append('')
    for r in doc.get('reference', []):
        out.append('[[reference]]')
        for k in ('path', 'sha256'):
            out.append('%s = "%s"' % (k, esc(r[k])))
        for k in ('bytes', 'rows'):
            out.append('%s = %d' % (k, r[k]))
        for k in ('pinned_on', 'role', 'reason'):
            out.append('%s = "%s"' % (k, esc(r.get(k, ''))))
        out.append('')
    if doc['history']:
        out.append('# --- superseded pins, append-only ---')
        out.append('')
    for h in doc['history']:
        out.append('[[history]]')
        for k in ('client', 'key', 'sha256'):
            out.append('%s = "%s"' % (k, esc(h[k])))
        out.append('bytes = %d' % h['bytes'])
        for k in ('pinned_on', 'superseded_on', 'superseded_reason'):
            out.append('%s = "%s"' % (k, esc(h.get(k, ''))))
        out.append('')
    with open(BASELINES, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(out))


def pin_index(doc):
    return {(b['client'], b['key']): b for b in doc['baseline']}


def resolve(client, key, roots):
    rel = TARGETS[client][key]
    return os.path.join(roots[client], rel), rel


def cmd_list(doc, roots):
    pins = pin_index(doc)
    print('%-6s %-10s %-12s %10s  %s' % ('client', 'key', 'state', 'bytes', 'pinned'))
    print('-' * 74)
    moved = []
    for client, keys in TARGETS.items():
        for key in keys:
            path, rel = resolve(client, key, roots)
            pin = pins.get((client, key))
            if not os.path.exists(path):
                print('%-6s %-10s %-12s %10s  %s' % (client, key, 'MISSING', '-', rel))
                continue
            m = measure(path)
            if not pin:
                print('%-6s %-10s %-12s %10d  (unpinned)' % (client, key, 'UNPINNED', m['bytes']))
                moved.append((client, key))
            elif pin['sha256'] == m['sha256']:
                print('%-6s %-10s %-12s %10d  %s' % (client, key, 'pinned', m['bytes'], pin['pinned_on']))
            else:
                print('%-6s %-10s %-12s %10d  %s -> now %d bytes'
                      % (client, key, 'MOVED', pin['bytes'], pin['pinned_on'], m['bytes']))
                moved.append((client, key))
    return moved


def cmd_bless(doc, roots, client, key, reason, produced_by):
    path, rel = resolve(client, key, roots)
    m = measure(path)
    pins = pin_index(doc)
    today = datetime.date.today().isoformat()
    old = pins.get((client, key))
    if old:
        if old['sha256'] == m['sha256']:
            print('  %s/%s unchanged — nothing to bless' % (client, key))
            return False
        doc['history'].append({
            'client': client, 'key': key, 'sha256': old['sha256'],
            'bytes': old['bytes'], 'pinned_on': old.get('pinned_on', ''),
            'superseded_on': today, 'superseded_reason': reason,
        })
        doc['baseline'] = [b for b in doc['baseline']
                           if not (b['client'] == client and b['key'] == key)]
        print('  %s/%s  %d -> %d bytes   superseded pin from %s'
              % (client, key, old['bytes'], m['bytes'], old.get('pinned_on', '?')))
    else:
        print('  %s/%s  pinned at %d bytes (first pin)' % (client, key, m['bytes']))
    doc['baseline'].append({
        'client': client, 'key': key, 'path': rel,
        'sha256': m['sha256'], 'bytes': m['bytes'], 'rows': m['rows'],
        'pinned_on': today, 'produced_by': produced_by, 'reason': reason,
    })
    doc['baseline'].sort(key=lambda b: (b['client'], b['key']))
    return True


PROVENANCE = {
    ('leg', 'products'):
        'build_ecat_files.py (1,537 lines); live in org 273 (leg); file dated 2026-08-25',
    ('leg', 'inventory'):
        'build_ecat_files.py (1,537 lines); live in org 273 (leg); file dated 2026-08-25',
    ('mer', 'products'):
        'hand-built template corrected by mer_fixups.py; imported to org 302 (mer); '
        'file dated 2026-08-27, post-RelatedItems generation',
}


def main():
    args = sys.argv[1:]
    if not args or '--help' in args or '-h' in args:
        print(__doc__)
        return 2
    if '--reference' not in args and ('--legrand' not in args or '--mercer' not in args):
        print(__doc__)
        print('ERROR: pass --legrand <dir> --mercer <dir>')
        return 2
    roots = {}
    if '--legrand' in args:
        roots['leg'] = os.path.abspath(args[args.index('--legrand') + 1])
    if '--mercer' in args:
        roots['mer'] = os.path.abspath(args[args.index('--mercer') + 1])
    doc = load()

    if '--reference' in args:
        ref = os.path.abspath(args[args.index('--reference') + 1])
        if '--reason' not in args:
            print('ERROR: --reason is mandatory for a reference pin too.')
            return 2
        reason = args[args.index('--reason') + 1]
        role = args[args.index('--role') + 1] if '--role' in args else 'comparison target'
        if not os.path.exists(ref):
            print('ERROR: no such file: %s' % ref)
            return 2
        m = measure(ref)
        today = datetime.date.today().isoformat()
        prev = [r for r in doc['reference'] if r['path'] == ref]
        if prev and prev[0]['sha256'] == m['sha256']:
            print('  %s unchanged — already pinned %s' % (os.path.basename(ref), prev[0]['pinned_on']))
            return 0
        if prev:
            doc['history'].append({
                'client': 'reference', 'key': os.path.basename(ref),
                'sha256': prev[0]['sha256'], 'bytes': prev[0]['bytes'],
                'pinned_on': prev[0].get('pinned_on', ''),
                'superseded_on': today, 'superseded_reason': reason})
            doc['reference'] = [r for r in doc['reference'] if r['path'] != ref]
        doc['reference'].append({
            'path': ref, 'sha256': m['sha256'], 'bytes': m['bytes'],
            'rows': m['rows'], 'pinned_on': today, 'role': role, 'reason': reason})
        doc['reference'].sort(key=lambda r: r['path'])
        save(doc)
        print('  pinned reference %s (%d bytes, %d rows)'
              % (os.path.basename(ref), m['bytes'], m['rows']))
        print('    role: %s' % role)
        return 0

    if '--list' in args:
        moved = cmd_list(doc, roots)
        if moved:
            print()
            print('%d baseline(s) need a decision. Re-bless with a reason, or' % len(moved))
            print('investigate the build that moved them:')
            for c, k in moved:
                print('   python3 mapping/bless.py %s %s --reason "..." \\' % (c, k))
                print('       --legrand <dir> --mercer <dir>')
        return 0

    if '--reason' not in args:
        print('ERROR: --reason is mandatory. A re-bless without a recorded reason')
        print('is an edit to a number, which is what pinning exists to prevent.')
        return 2
    reason = args[args.index('--reason') + 1]

    if '--all' in args:
        changed = False
        for client, keys in TARGETS.items():
            for key in keys:
                pb = PROVENANCE.get((client, key), 'unrecorded')
                changed |= cmd_bless(doc, roots, client, key, reason, pb)
        if changed:
            save(doc)
            print('\nwrote %s' % os.path.basename(BASELINES))
        return 0

    positional = [a for a in args if not a.startswith('--')
                  and a not in (roots['leg'], roots['mer'], reason)]
    if len(positional) != 2:
        print('ERROR: need <client> <key>, e.g. `bless.py leg products`')
        return 2
    client, key = positional
    if client not in TARGETS or key not in TARGETS[client]:
        print('ERROR: unknown target %s/%s' % (client, key))
        return 2
    pb = PROVENANCE.get((client, key), 'unrecorded')
    if cmd_bless(doc, roots, client, key, reason, pb):
        save(doc)
        print('\nwrote %s' % os.path.basename(BASELINES))
    return 0


if __name__ == '__main__':
    sys.exit(main())
