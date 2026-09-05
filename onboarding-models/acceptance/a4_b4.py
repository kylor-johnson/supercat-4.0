#!/usr/bin/env python3
"""A4 (import order) and B4 (recurring feeds overwriting), over import_log records.

Both read the structured records `import_log.py` produces. Neither re-parses a
formatted string, and neither talks to the database.

## A4 — import order

Canonical order:

    options -> option_groups -> products -> stories -> inventory -> customers

The load-bearing clause is the second one: **importing `options.csv` NULLS group
membership, so `option_groups.csv` must be re-sent afterwards.** An Options
import with no Option Groups import following it leaves every product's option
groups empty, and the import log reads clean either way.

The rule is a running STATE, not a pairing test. An event's net effect is decided
by its last Options/Option Groups block, because the importer processes them in
order: ending on Options leaves membership nulled, ending on Option Groups
restores it.

  FATAL  the standing state is nulled - nothing has restored it
  WARN   membership was nulled for a period and later restored

Only the standing state is a defect. The first version of this rule tested
"is every Options block followed by an Option Groups block before the next
Options block" and reported 17 defects across tcs and pebl where live state has
none - because a remedy arriving in the same event as the next Options import
was not counted. A bare Option Groups import is the remedy and is never flagged.

## B4 — two files feeding one importer

`inventory.csv` and `customers.csv` hard-delete and reload. Two different files
posting into the same importer therefore overwrite each other, and only the last
one's rows survive.

The detector is the message-count signature. One file produces one recurring
signature; two files alternating produce two, interleaved over the same window.
leg's inventory alternates between exactly 237 and exactly 10 warnings.

**This measures the log, not the catalogue.** Two signatures is strong evidence
of two files; it does not by itself prove which rows are currently live. The
verdict says so, and names the query that would settle it.
"""

import argparse
import collections
import json
import sys

CANONICAL = ['Options', 'Option Groups', 'Products', 'Product Stories',
             'Inventory', 'Customers']
ORDER = {name: i for i, name in enumerate(CANONICAL)}

# Files whose importer hard-deletes and reloads: two feeds here destroy data
# rather than merely confusing it.
HARD_DELETE = {'Inventory', 'Customers', 'Options', 'Option Groups'}


def load(path):
    with open(path) as fh:
        payload = json.load(fh)
    return payload['records'] if isinstance(payload, dict) else payload


# ------------------------------------------------------------------ A4

def check_a4(records):
    """Returns (findings, timeline_stats)."""
    recs = sorted(records, key=lambda r: (r['created_at'], r.get('seq', 1)))
    findings = []

    # 1. Within a single event carrying several file types, the sequence the
    #    importer processed them in must respect the canonical order.
    by_event = collections.OrderedDict()
    for r in recs:
        by_event.setdefault(r['event_id'], []).append(r)
    for eid, blocks in by_event.items():
        if len(blocks) < 2:
            continue
        seen = [(b.get('seq', 1), b['file_type']) for b in sorted(
            blocks, key=lambda b: b.get('seq', 1))]
        ranks = [ORDER.get(ft) for _, ft in seen if ft in ORDER]
        if ranks and ranks != sorted(ranks):
            findings.append({
                'rule': 'A4.order',
                'severity': 'FATAL',
                'when': blocks[0]['created_at'],
                'event_id': eid,
                'detail': 'files processed out of canonical order within one '
                          'import: %s' % ' -> '.join(ft for _, ft in seen),
            })

    # 2. Option-group membership.
    #
    # CORRECTED 2026-09-04. The first rule was "every Options block must be
    # followed by an Option Groups block before the next Options block", and it
    # produced a false positive on pebl's most recent import:
    #
    #     09:28  Options -> Option Groups     paired
    #     09:32  Options                      flagged
    #     09:46  Products
    #     09:54  Products
    #     09:56  Options -> Option Groups     the remedy, 24 minutes later
    #
    # 09:32 WAS remedied at 09:56, but the scan for "the next Options block"
    # lands on 09:56 seq 1 - which precedes the remedying Option Groups block at
    # 09:56 seq 2 - and closes the window unremedied. Note that iterating blocks
    # rather than events does NOT fix this on its own: this loop was already
    # block-level. What was wrong was the QUESTION, not the granularity.
    #
    # The importer runs an event's blocks in order, so an event's net effect on
    # membership is decided by its LAST Options/Option Groups block: ending on
    # Options leaves membership nulled, ending on Option Groups restores it.
    # Membership is then a running state over the event stream.
    #
    #   FATAL - the standing state is nulled (nothing restored it since)
    #   WARN  - membership was nulled for a period and later restored
    #
    # Only the standing state is a defect. A transient window is real - reps
    # syncing inside it see no option groups - but it is not the same claim, and
    # conflating them turned 0 live defects into 17 reported ones.
    net = []              # (event_id, created_at, last relevant block type)
    by_event_ordered = collections.OrderedDict()
    for r in recs:
        if r['file_type'] in ('Options', 'Option Groups'):
            by_event_ordered.setdefault(r['event_id'], []).append(r)
    for eid, blocks in by_event_ordered.items():
        last = max(blocks, key=lambda b: b.get('seq', 1))
        net.append((eid, last['created_at'], last['file_type']))
    net.sort(key=lambda t: t[1])

    nulled_since = None
    for eid, when, last_type in net:
        if last_type == 'Options':
            if nulled_since is None:
                nulled_since = (eid, when)
        else:
            if nulled_since is not None:
                findings.append({
                    'rule': 'A4.membership_window',
                    'severity': 'WARN',
                    'when': nulled_since[1],
                    'event_id': nulled_since[0],
                    'detail': 'option group membership was nulled at %s and not '
                              'restored until %s. Reps who synced inside that '
                              'window saw no option groups.'
                              % (nulled_since[1], when),
                })
                nulled_since = None
    if nulled_since is not None:
        findings.append({
            'rule': 'A4.membership_nulled_now',
            'severity': 'FATAL',
            'when': nulled_since[1],
            'event_id': nulled_since[0],
            'detail': 'the most recent Options import (%s) was not followed by an '
                      'Option Groups import. Group membership is nulled RIGHT NOW '
                      '- confirm against option_groups.options before acting.'
                      % nulled_since[1],
        })

    stats = collections.Counter(r['file_type'] for r in recs)
    return findings, stats


# ------------------------------------------------------------------ B4

def check_b4(signatures, min_events=3):
    """`signatures` are rows from import_log --mode signatures."""
    findings = []
    by_type = collections.defaultdict(list)
    for s in signatures:
        by_type[s['file_type']].append(s)

    for ft, sigs in sorted(by_type.items()):
        # A recurring FEED, by definition, recurs over time. Two signatures
        # that both live inside a single day are a batch uploaded in pieces -
        # leg's demo-day image uploads produced 10/0 and 12/0 on 2025-06-13 and
        # were flagged until this filter was added. Require each signature to
        # span more than a day before treating it as a standing feed.
        recurring = [s for s in sigs
                     if int(s['events']) >= min_events
                     and s['signature'] != '0/0'
                     and s['first_seen'] != s['last_seen']]
        if len(recurring) < 2:
            continue
        # Interleaved: the windows overlap rather than following one another.
        spans = [(s['first_seen'], s['last_seen'], s) for s in recurring]
        overlapping = []
        for i in range(len(spans)):
            for j in range(i + 1, len(spans)):
                a, b = spans[i], spans[j]
                if a[0] <= b[1] and b[0] <= a[1]:
                    overlapping.append((a[2], b[2]))
        if not overlapping:
            continue
        for a, b in overlapping:
            findings.append({
                'rule': 'B4.two_feeds',
                'severity': 'FATAL' if ft in HARD_DELETE else 'WARN',
                'file_type': ft,
                'detail': '%s shows two distinct recurring message signatures over '
                          'the same window: %s (%s events, %s..%s) and %s (%s '
                          'events, %s..%s). One file produces one signature; two '
                          'interleaved signatures mean two different files are '
                          'feeding this importer.%s'
                          % (ft, a['signature'], a['events'], a['first_seen'],
                             a['last_seen'], b['signature'], b['events'],
                             b['first_seen'], b['last_seen'],
                             ' %s hard-deletes and reloads, so only one file\'s '
                             'rows survive at a time.' % ft
                             if ft in HARD_DELETE else ''),
                'measured': 'log signatures only',
                'not_established': 'which file\'s rows are live right now. Settle '
                                   'it by comparing the live key set against each '
                                   'candidate source file.',
            })
    return findings


def report(a4, b4, stats, out=sys.stdout):
    w = out.write
    w('=' * 72 + '\n')
    w('A4 IMPORT ORDER / B4 RECURRING FEEDS\n')
    w('=' * 72 + '\n')
    if stats:
        w('blocks seen: %s\n' % ', '.join('%s %d' % (k, v)
                                          for k, v in stats.most_common()))
    w('\n-- A4 ' + '-' * 66 + '\n')
    if not a4:
        w('   no ordering violation found\n')
    for f in a4:
        w('   %-7s %s\n' % (f['severity'], f['rule']))
        w('           %s\n' % f['detail'])
    w('\n-- B4 ' + '-' * 66 + '\n')
    if not b4:
        w('   no interleaved feed signatures found\n')
    for f in b4:
        w('   %-7s %s (%s)\n' % (f['severity'], f['rule'], f['file_type']))
        w('           %s\n' % f['detail'])
        w('           measured: %s\n' % f['measured'])
        w('           NOT established: %s\n' % f['not_established'])
    w('\n')
    return 1 if any(f['severity'] == 'FATAL' for f in a4 + b4) else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--events', help='records from import_log --mode events')
    ap.add_argument('--signatures', help='records from import_log --mode signatures')
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()

    a4, stats = (check_a4(load(args.events)) if args.events else ([], None))
    b4 = check_b4(load(args.signatures)) if args.signatures else []
    if args.json:
        print(json.dumps({'a4': a4, 'b4': b4}, indent=2))
        return 1 if any(f['severity'] == 'FATAL' for f in a4 + b4) else 0
    return report(a4, b4, stats)


if __name__ == '__main__':
    sys.exit(main())
