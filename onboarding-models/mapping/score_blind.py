#!/usr/bin/env python3
"""Score a blind mapping run against a pinned reference. Refuses if unpinned.

Produces the partition the score has to report — byte-exact / semantically
equivalent / wrong / not produced — at BOTH granularities, because they answer
different questions:

  columns   strict. A column differing on 1 row of 822 counts as a whole miss.
  cells     the honest accuracy measure, and the one to quote.

On libco those two read 26/60 and 97.3%, and the gap is entirely 23 columns
that differ on 1-9 rows each. Reporting only the first would understate the run
by half; reporting only the second would hide that a column can be structurally
wrong in a way no cell records (a renamed header changes no cell at all).

**Refuses to run against an unpinned or stale comparison target.** That is not
process for its own sake: scoring libco against an unpinned, two-months-stale
`products.csv` produced two confident findings that both had to be retracted.
`--allow-unpinned` proceeds but stamps every line of output as untrusted.

**Every section states its coverage** — `evaluated N of M candidates`
(BUILD_SPEC §3.4). This tool was the SIXTH instance of the failure that rule
exists for: its column match was case-sensitive, so five tcs headers spelled
differently scored as "not produced" and the run read 52.2%% when it was 66.2%%.
A check that silently had nothing to measure reported a number anyway. The
coverage line is what makes that visible without anyone happening to look at an
adjacent figure.

`--membership <column>` scores SET EQUALITY on a comma-list column instead of
string equality, and keys on the set rather than the code. That is the only
honest way to score `option_groups.csv`: the group CODE is invented by whoever
built the file, so a mapping can get every membership exactly right and score 0%%
on Code. Grouping and naming are two different questions and they get two
different numbers.

usage: score_blind.py <produced.csv> <reference.csv> [--key BaseItemCode]
                      [--membership Options] [--allow-unpinned]
"""

import csv
import os
import re
import sys
import collections

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import pins  # noqa: E402


def sem(v):
    """Normalise away pure FORMAT, so we can ask whether the VALUE agrees.

    Deliberately narrow: currency decoration, thousands separators and an
    all-zero decimal tail. It does NOT fold case or whitespace, because those
    are the difference between one filter facet and two.
    """
    v = (v or '').strip()
    v = re.sub(r'^\$', '', v).replace(',', '')
    v = re.sub(r'\.0+$', '', v)
    return v


def load(path, key):
    with open(path, newline='', encoding='utf-8-sig') as fh:
        rows = list(csv.DictReader(fh))
    return {(r.get(key) or '').strip(): r for r in rows if (r.get(key) or '').strip()}


def main():
    args = sys.argv[1:]
    if len(args) < 2:
        print(__doc__)
        return 2
    produced, reference = args[0], args[1]
    key = args[args.index('--key') + 1] if '--key' in args else 'BaseItemCode'
    allow = '--allow-unpinned' in args

    ok, lines = pins.require([reference], allow_unpinned=allow)
    print('=' * 74)
    print('COMPARISON TARGETS')
    print('=' * 74)
    for ln in lines:
        print(ln)
    if not ok:
        return 2
    prefix = '[UNTRUSTED] ' if allow and any('!!' in l for l in lines) else ''

    ref, mine = load(reference, key), load(produced, key)

    if '--membership' in args:
        return membership(ref, mine, args[args.index('--membership') + 1],
                          key, produced, reference)

    shared = sorted(set(ref) & set(mine))
    if not shared:
        # A column is "byte-exact" over an empty row set, which is how a score
        # of 0/0 reads as a pass. Same vacuity as a test that cannot go red, and
        # the drf run hit it: 72 pattern codes against 1,627 SKU codes share
        # nothing, and the tool cheerfully reported 21 byte-exact columns.
        print()
        print('=' * 74)
        print('CANNOT SCORE — the two files share ZERO keys on %r.' % key)
        print('=' * 74)
        print('  reference : %d rows, %d columns' % (len(ref), len(list(ref[next(iter(ref))].keys()))))
        print('  produced  : %d rows, %d columns' % (len(mine), len(list(mine[next(iter(mine))].keys()))))
        print()
        print('  A per-column score over an empty intersection is vacuous: every')
        print('  column is trivially "exact" on no rows. Refusing to print one.')
        print()
        print('  This is a finding, not a tooling failure. Two files claiming the')
        print('  same target with no key overlap means they are keyed on different')
        print('  THINGS -- and that is the question to answer before any mapping')
        print('  is scored at all.')
        print('  reference specimens: %s' % ', '.join(sorted(ref)[:4]))
        print('  produced  specimens: %s' % ', '.join(sorted(mine)[:4]))
        return 3
    ref_cols = list(ref[next(iter(ref))].keys())
    my_cols = list(mine[next(iter(mine))].keys())

    # Column names match CASE-INSENSITIVELY, and casing differences are reported
    # rather than scored as misses. tcs's build spells four headers lowercase
    # (`materials`, `dimensions`, `shipweight`, `Price_MAP`); a case-sensitive
    # match scored all four as "not produced" and put the run at 52.2% when it
    # was 66.2%. Third defect of this shape found by a blind run: a check that
    # reads as a failure when it is really a naming difference.
    ref_by_lower = {h.lower(): h for h in ref_cols}
    casing = []

    exact_cols, sem_cols, diff_cols = [], [], []
    tot = ex = so = df = 0
    per = collections.Counter()
    for h in my_cols:
        ref_h = ref_by_lower.get(h.lower())
        if ref_h is None:
            continue
        if ref_h != h:
            casing.append('%s -> %s' % (h, ref_h))
        e = s2 = 0
        for k in shared:
            a = (ref[k].get(ref_h) or '').strip()
            b = (mine[k].get(h) or '').strip()
            tot += 1
            if a == b:
                e += 1; s2 += 1; ex += 1
            elif sem(a) == sem(b):
                s2 += 1; so += 1
            else:
                df += 1; per[h] += 1
        n = len(shared)
        (exact_cols if e == n else sem_cols if s2 == n else diff_cols).append(h)

    my_lower = {h.lower() for h in my_cols}
    not_produced = [h for h in ref_cols if h.lower() not in my_lower]

    print()
    print('%s%s' % (prefix, '=' * 74))
    print('%sPARTITION' % prefix)
    print('%s%s' % (prefix, '=' * 74))
    print('%sreference : %s (%d rows, %d cols)'
          % (prefix, os.path.basename(reference), len(ref), len(ref_cols)))
    print('%sproduced  : %s (%d rows, %d cols)'
          % (prefix, os.path.basename(produced), len(mine), len(my_cols)))
    print('%sshared rows: %d   rows only in reference: %d   only in mine: %d'
          % (prefix, len(shared), len(set(ref) - set(mine)), len(set(mine) - set(ref))))
    print()
    denom = len(ref_cols)
    print('%sCOLUMNS (denominator %d = the reference\'s column set)' % (prefix, denom))
    print('%s  byte-exact             %3d' % (prefix, len(exact_cols)))
    print('%s  semantically equal     %3d  %s' % (prefix, len(sem_cols), sem_cols or ''))
    print('%s  differ                 %3d' % (prefix, len(diff_cols)))
    print('%s  not produced           %3d  %s' % (prefix, len(not_produced), not_produced or ''))
    if casing:
        print('%s  (name matched but CASED differently, not counted as misses: %s)'
              % (prefix, '; '.join(casing)))
    print('%s  %s' % (prefix, '-' * 34))
    print('%s  sum                    %3d' % (prefix,
          len(exact_cols) + len(sem_cols) + len(diff_cols) + len(not_produced)))
    print('%s  COVERAGE — evaluated %d of %d reference columns (%d produced '
          'columns had no counterpart and are NOT in this denominator)'
          % (prefix, len(exact_cols) + len(sem_cols) + len(diff_cols), denom,
             len([h for h in my_cols if h.lower() not in ref_by_lower])))
    print()
    print('%sCELLS (%d compared)' % (prefix, tot))
    if tot:
        print('%s  byte-exact             %6d  (%.1f%%)' % (prefix, ex, 100 * ex / tot))
        print('%s  semantically equal     %6d  (%.1f%%)' % (prefix, so, 100 * so / tot))
        print('%s  differ                 %6d  (%.1f%%)' % (prefix, df, 100 * df / tot))
        print('%s  %s' % (prefix, '-' * 34))
        print('%s  sum                    %6d' % (prefix, ex + so + df))
        print()
        print('%s  semantic accuracy      %.1f%%' % (prefix, 100 * (ex + so) / tot))
        print('%s  COVERAGE — evaluated %d of %d candidate cells '
              '(%d matched columns x %d shared rows). %d reference rows and %d '
              'produced rows were outside the shared key set and contributed '
              'NOTHING to this number.'
              % (prefix, tot, len(ref_cols) * len(ref), tot // max(len(shared), 1),
                 len(shared), len(set(ref) - set(mine)), len(set(mine) - set(ref))))
    else:
        print('%s  COVERAGE — evaluated 0 of %d candidate cells. NO column name '
              'matched between the two files; this is not a pass.'
              % (prefix, len(ref_cols) * len(ref)))
    if per:
        print()
        print('%sdiffering cells, per column (the tail is what makes the column'
              % prefix)
        print('%smetric look worse than the run was):' % prefix)
        run = 0
        for h, n in per.most_common():
            run += n
            print('%s  %-24s %5d   cumulative %.0f%%' % (prefix, h, n, 100 * run / df))
    return 0


def membership(ref, mine, col, key, produced, reference):
    """Score SET EQUALITY on a comma-list column, keyed on the set.

    `option_groups.csv` cannot be scored on Code. The code is invented by
    whoever built the file -- `MNT47` here, something else there -- so a mapping
    that partitions the catalogue exactly right scores 0% byte-exact on Code and
    the number means nothing. What is actually being asked is: for each group in
    the reference, did I produce a group with the IDENTICAL option set?

    Reported both ways round, because they are different failures:
      recall     reference sets I reproduced      -> grouping I missed
      precision  my sets that exist in reference  -> grouping I invented
    """
    def sets(d):
        out = {}
        for k, r in d.items():
            members = tuple(sorted(x for x in (r.get(col) or '').split(',') if x))
            out.setdefault(members, []).append(k)
        return out

    rs, ms = sets(ref), sets(mine)
    if not rs or all(not m for m in rs):
        print()
        print('CANNOT SCORE — the reference has no %r values to compare.' % col)
        return 3
    matched = [m for m in rs if m in ms]
    print()
    print('=' * 74)
    print('MEMBERSHIP — set equality on %r, code spelling IGNORED' % col)
    print('=' * 74)
    print('  reference : %s   %d rows, %d distinct member sets'
          % (os.path.basename(reference), len(ref), len(rs)))
    print('  produced  : %s   %d rows, %d distinct member sets'
          % (os.path.basename(produced), len(mine), len(ms)))
    print()
    print('  reference sets I reproduced exactly   %4d of %4d   recall    %.1f%%'
          % (len(matched), len(rs), 100 * len(matched) / len(rs)))
    inv = [m for m in ms if m not in rs]
    print('  my sets that exist in the reference   %4d of %4d   precision %.1f%%'
          % (len(ms) - len(inv), len(ms),
             100 * (len(ms) - len(inv)) / max(len(ms), 1)))
    print()
    print('  COVERAGE — evaluated %d of %d reference member sets and %d of %d '
          'produced sets. Rows whose %r is empty form the single empty set and '
          'are counted once, not per row.'
          % (len(rs), len(rs), len(ms), len(ms), col))

    # Partial credit: how close are the misses?
    if len(matched) < len(rs):
        best = []
        mine_sets = [set(m) for m in ms]
        for m in rs:
            if m in ms:
                continue
            sm = set(m)
            if not sm:
                continue
            j = max((len(sm & x) / len(sm | x) for x in mine_sets if x), default=0.0)
            best.append(j)
        if best:
            exactish = sum(1 for j in best if j >= 0.9)
            print()
            print('  of the %d reference sets I did NOT reproduce exactly, the '
                  'closest produced set overlaps by Jaccard:' % len(best))
            print('     >= 0.90   %4d      mean %.2f      = 0.00 (no overlap)  %d'
                  % (exactish, sum(best) / len(best), sum(1 for j in best if j == 0)))
    print()
    print('  Code spelling is a SEPARATE question and is not scored here. Run')
    print('  without --membership to see it, and read the two numbers together:')
    print('  right grouping with invented codes is a rename; wrong grouping is a')
    print('  different catalogue.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
