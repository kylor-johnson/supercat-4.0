#!/usr/bin/env python3
"""Input-class detection — PER FILE, never per client.

    class 1  raw ERP export            -> map it
    class 2  pre-mapped by a human     -> VALIDATE, DO NOT TRANSFORM
    class 3  industry template         -> map, but the template is the contract
    hybrid   eCat headers AND client-domain columns side by side

Per file matters. A client can send one pre-mapped file and one raw one in the
same folder, and drf's "Characteristics ... eCat MAPPED" carries eCat headers
AND client-domain columns in the SAME file. A per-client verdict would re-map
one of them, which means overriding a decision a human already made -- usually
silently, usually wrongly.

The class-2 rule is the load-bearing one. A file whose headers are already
`BaseItemCode` / `BillToCode` has had its mapping done. The job is CHECKING it:
fill rates, value shapes, required fields, and where the human's mapping
disagrees with what eCat will accept.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'profiler'))

import ecat_vocab as vocab  # noqa: E402

# A header is "eCat-shaped" if it matches a known field for the DECLARED target.
# Scoping to the target is deliberate: `Name` is a real eCat field in
# options.csv, but in a NetSuite products export it holds the item code. A
# target-blind match is a false certain, and a false certain is worse than an
# honest moderate.


def _known(target):
    """The field vocabulary for ONE target, scoped deliberately.

    Sourced from `ecat_vocab` (which reads `preflight/limits_generated.py`,
    generated from supercat_server) — never transcribed. Falling back to the
    union of ALL eCat fields would be target-blind, and a target-blind match is
    a false certain: `Name` is a real eCat field in options.csv while in a
    products export it holds the item code.
    """
    known = set(vocab.PRODUCTS['distinctive'] if target == 'products.csv'
                else vocab.ALL_ECAT)
    spec = {'products.csv': vocab.PRODUCTS, 'customers.csv': vocab.CUSTOMERS,
            'inventory.csv': vocab.INVENTORY, 'options.csv': vocab.OPTIONS,
            'option_groups.csv': vocab.OPTION_GROUPS,
            'stories.csv': vocab.STORIES}.get(target)
    if spec:
        known |= {h.lower() for h in spec.get('distinctive', ())}
        if spec.get('key'):
            known.add(spec['key'].lower())
    known |= {h.lower() for h in vocab.REQUIRED_HEADERS.get(target, ())}
    return known


def _patterned(header, target):
    """Price_<code>, OptionSet#, per-division qty — real headers whose NAME is
    per-client. They match by shape, not by a literal."""
    h = header.lower().replace('_', '')
    for pattern, tgt, _label in vocab.PATTERNED:
        if tgt == target and pattern.match(h):
            return True
    return False


def classify(headers, target='products.csv'):
    """Return a verdict dict for one file's header row."""
    known = _known(target)
    hdrs = [(h or '').strip() for h in headers]
    named = [h for h in hdrs if h]
    blank = len(hdrs) - len(named)

    matched = [h for h in named
               if h.lower() in known or _patterned(h, target)]
    unmatched = [h for h in named if h not in matched]
    pct = (100.0 * len(matched) / len(named)) if named else 0.0

    if pct >= 70:
        cls, action = 2, 'VALIDATE, do not transform'
    elif pct >= 20:
        cls, action = 'hybrid', 'validate the eCat half, map the client half'
    else:
        cls, action = 1, 'map it'

    return {
        'class': cls,
        'action': action,
        'target': target,
        'headers': len(hdrs),
        'named': len(named),
        'blank_headers': blank,
        'matched': matched,
        'unmatched': unmatched,
        'pct_matched': round(pct, 1),
        'required_missing': sorted(
            h for h in vocab.REQUIRED_HEADERS.get(target, [])
            if h not in {m.lower() for m in matched}),
    }


def report(verdict, name=''):
    out = ['input class: %s — %s' % (verdict['class'], verdict['action'])]
    out.append('  %s' % name if name else '')
    out.append('  %d headers, %d named, %d BLANK'
               % (verdict['headers'], verdict['named'], verdict['blank_headers']))
    out.append('  %d of %d named headers are eCat fields for %s (%.1f%%)'
               % (len(verdict['matched']), verdict['named'], verdict['target'],
                  verdict['pct_matched']))
    if verdict['blank_headers']:
        out.append('  ! a BLANK header cannot be imported and an unrecognised '
                   'column is a FATAL import error')
    if verdict['required_missing']:
        out.append('  ! required field(s) absent: %s'
                   % ', '.join(verdict['required_missing']))
    if verdict['unmatched']:
        out.append('  client-domain columns (%d): %s'
                   % (len(verdict['unmatched']),
                      ', '.join(verdict['unmatched'][:12])
                      + (' ...' if len(verdict['unmatched']) > 12 else '')))
    return '\n'.join(x for x in out if x.strip())


if __name__ == '__main__':
    import csv
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    with open(sys.argv[1], newline='', encoding='utf-8-sig') as fh:
        hdr = next(csv.reader(fh))
    tgt = sys.argv[2] if len(sys.argv) > 2 else 'products.csv'
    print(report(classify(hdr, tgt), os.path.basename(sys.argv[1])))
