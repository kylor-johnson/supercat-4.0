#!/usr/bin/env python3
"""A4 (import order) and B4 (recurring feeds overwriting), over import_log records.

Both read the structured records `import_log.py` produces. Neither re-parses a
formatted string, and neither talks to the database.

## A4 — option-group membership

**The canonical-order rule was DELETED 2026-09-04.** It asserted
`options -> option_groups -> products -> stories -> inventory -> customers`
within a single event and emitted FATAL on any deviation. No incident motivated
it, no document described it, and it fired 4,602 times on `ufi`, whose routine
since 2013 is `Products -> Inventory -> Product Stories -> Customers`; also
607/609 events at `swc`, 2,383 at `ih`, 633 at `pf`, 291 at `ta`. File ordering
across unrelated importers is a preference, not correctness.

What is left is the clause with a mechanism behind it: **importing `options.csv`
NULLS group membership, so `option_groups.csv` must be re-sent afterwards.** An Options
import with no Option Groups import following it leaves every product's option
groups empty, and the import log reads clean either way.

The rule is a running STATE, not a pairing test. An event's net effect is decided
by its last Options/Option Groups block, because the importer processes them in
order: ending on Options leaves membership nulled, ending on Option Groups
restores it.

  FATAL  the standing state is nulled - nothing has restored it
  WARN   membership was nulled for a period and later restored
  INFO   Option Groups was processed before Options inside one event

Every A4 finding measures **the import log**. Whether anyone synced inside a
window, or whether membership is empty right now, are separate claims the check
does not make and says it does not make - see OPEN_ITEMS G1 and G2.

Only the standing state is a defect. The first version of this rule tested
"is every Options block followed by an Option Groups block before the next
Options block" and reported 17 defects across tcs and pebl where live state has
none - because a remedy arriving in the same event as the next Options import
was not counted. A bare Option Groups import is the remedy and is never flagged.

## B4 — two files feeding one importer

`inventory.csv` and `customers.csv` hard-delete and reload. Two different files
posting into the same importer therefore overwrite each other, and only the last
one's rows survive.

The detector is the message-count signature, and **overlapping date ranges are
not enough** - see `check_b4`. A pair must additionally cover >=90% of that
importer's runs in the window AND actually alternate (>=5 switches, >=30% of
consecutive runs). Range overlap alone produced 1,711 findings across 13 orgs,
1,262 FATAL, two defensible; the three tests together produce 2.

Input is `import_log --mode feed_pairs`. A `--mode signatures` file is declined
rather than silently downgraded.

**This measures the log, not the catalogue.** It does not prove which rows are
currently live, nor that two signatures are two FILES rather than one file whose
error count moved - message content would settle that and is not wired in. Every
finding says so.
"""

import argparse
import collections
import datetime
import json
import sys

# NOTE: the CANONICAL six-way file order that used to live here is gone on
# purpose (see the module docstring). Do not reintroduce it as a check - the
# ordering of unrelated importers within one event is a client's routine, not a
# correctness property, and asserting it cost 4,602 FATALs on one org.

# Files whose importer hard-deletes and reloads: two feeds here destroy data
# rather than merely confusing it.
HARD_DELETE = {'Inventory', 'Customers', 'Options', 'Option Groups'}


def load(path):
    with open(path) as fh:
        payload = json.load(fh)
    return payload['records'] if isinstance(payload, dict) else payload


def _window_length(start, end):
    """Human duration between two timestamp strings, or '' if unparseable.

    Reported because the severity of a nulled window depends on how long it ran
    - pebl's 276.5h and leg's 2.6h are not the same fact - and the check
    currently gives them the same severity. Stating the length at least lets a
    reader tell them apart until severity is graded properly.
    """
    for fmt in ('%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%dT%H:%M:%S.%f', '%Y-%m-%dT%H:%M:%S'):
        try:
            a = datetime.datetime.strptime(str(start)[:26], fmt)
            b = datetime.datetime.strptime(str(end)[:26], fmt)
        except ValueError:
            continue
        hours = (b - a).total_seconds() / 3600.0
        if hours < 1:
            return '%d min' % round(hours * 60)
        if hours < 48:
            return '%.1f h' % hours
        return '%.1f days' % (hours / 24.0)
    return 'duration unknown'


# ------------------------------------------------------------------ A4

def check_a4(records):
    """Returns (findings, timeline_stats)."""
    recs = sorted(records, key=lambda r: (r['created_at'], r.get('seq', 1)))
    findings = []

    # 1. Option Groups processed BEFORE Options inside one event.
    #
    # REPLACED 2026-09-04. The previous rule asserted the full six-way CANONICAL
    # order within an event and emitted FATAL on any deviation. It had no
    # incident behind it, appeared in no document - BUILD_SPEC §3.1 A4 and the
    # harness README both describe only rule 2 - and it fired on ordinary
    # working feeds:
    #
    #   ufi   4,602 FATALs. Its routine since 2013 is
    #         Products -> Inventory -> Product Stories -> Customers, which puts
    #         Inventory (rank 4) ahead of Product Stories (rank 3).
    #   swc   607 of 609 multiblock events.  ih 2,383.  pf 633.  ta 291.
    #
    # "Products before Inventory before Stories" is a preference, not a
    # correctness rule, and a FATAL that fires on every import of a decade-old
    # working routine is how a gate gets switched off.
    #
    # What survives is the one adjacency with a MECHANISM: importing Options
    # nulls option-group membership, so an Option Groups block that the importer
    # processes BEFORE an Options block in the same event has its membership
    # nulled again by that Options block. Rule 2 below already scores the net
    # effect over the event stream, so this is diagnostic rather than a defect
    # in its own right - hence INFO, not FATAL.
    by_event = collections.OrderedDict()
    for r in recs:
        by_event.setdefault(r['event_id'], []).append(r)
    for eid, blocks in by_event.items():
        if len(blocks) < 2:
            continue
        seen = [(b.get('seq', 1), b['file_type']) for b in sorted(
            blocks, key=lambda b: b.get('seq', 1))]
        first_groups = next((s for s, ft in seen if ft == 'Option Groups'), None)
        last_options = max((s for s, ft in seen if ft == 'Options'), default=None)
        if first_groups is not None and last_options is not None \
                and first_groups < last_options:
            findings.append({
                'rule': 'A4.option_order_within_event',
                'severity': 'INFO',
                'when': blocks[0]['created_at'],
                'event_id': eid,
                'detail': 'Option Groups was processed before Options in this import '
                          '(%s), so that Options block nulled the membership the '
                          'Option Groups block had just set. Whether membership is '
                          'nulled NOW is rule 2 below, not this line.'
                          % ' -> '.join(ft for _, ft in seen),
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
                    # The old text read "Reps who synced inside that window saw no
                    # option groups." That is a consequence, not a measurement, and
                    # OPEN_ITEMS G1 settled the wording after doing the work: a
                    # login is not proof of a sync, and a sync is not proof anyone
                    # opened a product with options. Saying it anyway is SCORECARD
                    # §12 R1 in the tool built after R1 was written up.
                    'detail': 'option group membership was nulled at %s and not '
                              'restored until %s (%s).'
                              % (nulled_since[1], when,
                                 _window_length(nulled_since[1], when)),
                    'measured': 'the import log only - the window during which the '
                                'standing state was nulled',
                    'not_established': 'whether any user synced inside the window, '
                                       'and whether anyone opened a product with '
                                       'options if they did. Settle it against '
                                       'login_events for the window and say "at '
                                       'least one user was active during it" - never '
                                       '"reps saw no option groups".',
                })
                nulled_since = None
    if nulled_since is not None:
        findings.append({
            'rule': 'A4.membership_nulled_now',
            'severity': 'FATAL',
            'when': nulled_since[1],
            'event_id': nulled_since[0],
            'detail': 'the most recent Options import (%s) was not followed by an '
                      'Option Groups import, so the standing state is nulled.'
                      % nulled_since[1],
            'measured': 'the import log only',
            'not_established': 'that membership is actually empty right now. '
                               'CONFIRM against option_groups.options for this org '
                               'before this reaches anyone - a harness finding is '
                               'evidence, not a verdict (OPEN_ITEMS G2).',
        })

    stats = collections.Counter(r['file_type'] for r in recs)
    return findings, stats


# ------------------------------------------------------------------ B4

# B4 fires only when all three hold. Each has a meaning; none is a knob.
MIN_PAIR_EVENTS = 10     # enough runs of the importer to see a pattern at all
MIN_COVERAGE = 0.90      # the pair IS this importer's traffic in the window
MIN_ALTERNATIONS = 5     # the pattern returns, rather than swapping once
MIN_ALT_RATE = 0.30      # ...and returns at a rate, not 8 times in 340 events


def check_b4(rows, min_events=3):
    """`rows` are from `import_log --mode feed_pairs`.

    ## What changed, and why the old test could not work

    The previous test was "do the two signatures' [first_seen, last_seen] ranges
    overlap". For any long-running feed they always do, so it fired on drift:
    **1,711 findings across 13 orgs, 1,262 FATAL, two defensible.** `cl` alone
    contributed 1,033 FATALs on an Inventory feed that ran clean 5,641 times out
    of 5,865, whose three "competing files" were one feed whose warning count
    drifted 1 -> 14 -> 17 over six months.

    `fal` is the case that shows what the signature actually is. Its seven
    Customers FATALs came from a ten-day window in January 2025 where the same
    file was re-uploaded after each fix: `0/1001` is "still lots of billing
    errors", `0/8` is "down to the last eight", and the eight are byte-identical
    across 01-20, 01-24, 01-28 and 01-29 x3 - `Line 1927: Shipping post code
    can't be blank: Customer # = 851825`. One file being iterated reads as two
    files alternating if all you compare is a count.

    ## The three tests

    Two files feeding one importer implies all of:

      coverage      n_pair / n_win >= 0.90
                    If two files alternate into an importer, nearly every run of
                    it is one of them. leg: 37 of 37, 100%.

      alternation   alts >= 5 AND alts / (n_pair - 1) >= 0.30
                    `A...A B...B` is one file REPLACED by another and scores near
                    zero at any volume. The rate is needed as well as the count:
                    sp's Kit Items pair is 340 events at 96.6% coverage with 8
                    alternations - 2.4%, drift wearing coverage's clothing.

      volume        n_pair >= 10

    Validated against the four cases whose answer is known independently:

        leg   Inventory 237/0 vs 10/0   100% cov, 19 alts, 52.8%  -> FIRES
        cl    Inventory, 246 pairs      max alt rate 16.7%        -> silent
        fal   Customers, 7 pairs        max 2 alts at >=90% cov   -> silent
        pebl  Option Groups             0 alts; 423/423 groups OK -> silent

    Across the same 13 orgs: **1,711 -> 2** (leg's FATAL, and one sp Products
    WARN from a genuinely alternating 10-day window in 2021).

    ## What this still does not establish

    The signature is a COUNT of warnings and errors. Two files produce different
    message CONTENT, not merely different counts, and comparing content is what
    would settle this definitively - `--mode taxonomy` is the substrate for that
    and it is not wired in. Every finding says so.
    """
    findings = []
    if not rows:
        return findings

    # Legacy `--mode signatures` rows cannot answer the question. Decline
    # loudly rather than falling back to range-overlap, which is the behaviour
    # that produced 1,262 FATALs.
    if 'alts' not in rows[0]:
        return [{
            'rule': 'B4.not_evaluated', 'severity': 'INFO',
            'file_type': '(all)',
            'detail': 'NOT EVALUATED - B4 needs `import_log --mode feed_pairs`. The '
                      'rows supplied are `--mode signatures`, which carry only per-'
                      'signature date ranges; whether two signatures ALTERNATE '
                      'cannot be decided from those, and testing range overlap '
                      'instead is what produced 1,262 FATALs of which two were '
                      'defensible.',
            'measured': 'nothing - the check did not run',
            'not_established': 'anything about this org\'s feeds. Re-run with '
                               '--mode feed_pairs.',
        }]

    for r in rows:
        n_pair = int(r.get('n_pair') or 0)
        n_win = int(r.get('n_win') or 0)
        alts = int(r.get('alts') or 0)
        if n_pair < MIN_PAIR_EVENTS or n_win <= 0:
            continue
        coverage = n_pair / float(n_win)
        alt_rate = alts / float(n_pair - 1) if n_pair > 1 else 0.0
        if coverage < MIN_COVERAGE:
            continue
        if alts < MIN_ALTERNATIONS or alt_rate < MIN_ALT_RATE:
            continue
        ft = r['file_type']
        findings.append({
            'rule': 'B4.two_feeds',
            'severity': 'FATAL' if ft in HARD_DELETE else 'WARN',
            'file_type': ft,
            'detail': '%s alternates between two distinct message signatures over '
                      '%s..%s: %s (%s events) and %s (%s events). Across that window '
                      'they are %d of %d runs of this importer (%.0f%% coverage) and '
                      'they alternate %d times (%.0f%% of consecutive runs switch). '
                      'One file produces one signature; a pair that both dominates '
                      'the importer and keeps swapping is two different files feeding '
                      'it.%s'
                      % (ft, r.get('win_start'), r.get('win_end'),
                         r.get('sig_a'), r.get('events_a'),
                         r.get('sig_b'), r.get('events_b'),
                         n_pair, n_win, 100.0 * coverage,
                         alts, 100.0 * alt_rate,
                         ' %s hard-deletes and reloads, so only one file\'s rows '
                         'survive at a time.' % ft if ft in HARD_DELETE else ''),
            'measured': 'the import log only - signature counts, their coverage of '
                        'this importer, and how often they alternate',
            'not_established': 'which file\'s rows are live right now, and that the '
                               'two signatures are different FILES rather than one '
                               'file whose error count moves. Settle it by comparing '
                               'the live key set against each candidate source file; '
                               'message CONTENT (--mode taxonomy) would settle the '
                               'second question and is not wired in.',
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
        if f.get('measured'):
            w('           measured: %s\n' % f['measured'])
        if f.get('not_established'):
            w('           NOT established: %s\n' % f['not_established'])
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
    ap.add_argument('--signatures',
                    help='records from import_log --mode feed_pairs (a --mode '
                         'signatures file is accepted and declined, loudly)')
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
