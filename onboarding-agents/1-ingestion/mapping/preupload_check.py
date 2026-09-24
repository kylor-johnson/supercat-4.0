#!/usr/bin/env python3
"""Pre-upload gate for a mapped file: B6 regeneration diff, B7, then A1.

Phase 2 produces files; a HUMAN decides what is uploaded. This is what that
human should have in front of them, and it runs in the order the risk runs in:

  B6  Diff the regenerated file against the one that produced current live
      state. `blanked` is reported separately and first, because blanking is
      the dangerous direction -- a regenerated products.csv that silently
      empties a column still imports CLEAN, and products.csv soft-deletes
      omitted rows. That is how Legrand lost 19 products' live images.

  B7  Is the file POORER than the live rows it will replace? B6 only fires
      when a previous file exists; B7 is the case where one does not, and it
      compares against LIVE STATE instead. `mali`'s customers.csv regenerated
      from the available export carries BillToAddress1 on 21.3% of rows where
      live holds 100%, and puts every customer on a LIST price code where live
      has them on dealer-net. Owned by acceptance/ (it is an A1-family check
      that reads the database); called from here because the file it inspects
      is the mapping layer's output.

  A1  Confirm the file belongs to the target org. Emits SQL only; this runs
      read-only and has no Postgres credentials, so the statement goes through
      the supercat-postgres-vpn MCP and the rows come back via --from-results.
      2026-08-18: Legrand's 1,020-row file went into 111Mercer and soft-deleted
      all 102 of their products. The file was valid and the import was clean.

Read-only. Writes nothing, uploads nothing.

EMITTED IS NOT EVALUATED — added 2026-09-09
-------------------------------------------
Until now this exited 0 once B6 had diffed and an --org was given, having only
PRINTED the SQL for B7 and A1. That is the same defect the gate exists to
catch, turned on the gate: a check that measured nothing reporting a pass. An
operator reading `exit 0` had no way to tell "B7 ran clean" from "B7 printed a
query nobody ran", and those are the two states that matter most.

So the three checks now land in one of three states, and the exit code says
which:

    RAN           measured against the thing it names
    EMITTED ONLY  SQL produced, nothing measured        -> exit 3
    NOT CHECKED   could not even be attempted           -> exit 2

`--use-db` runs B7 and A1 in-process against a read-only DATABASE_URL, which
is what makes the gate runnable in a container. Without it they emit SQL, the
run exits 3, and the report says the credential is what is missing.

usage: preupload_check.py <produced.csv> <previous.csv> [--org <shortname>]
                          [--use-db]
exit:  0 all three RAN · 2 something NOT CHECKED · 3 something EMITTED ONLY
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

import ecatlib as lib  # noqa: E402

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), 'acceptance'))
import b7_lossy  # noqa: E402
import a1_fingerprint  # noqa: E402


def _run_b7(produced, org):
    """Call B7 for real rather than printing its command line.

    Returns (meta, statements). Raises if the file is unreadable or is not a
    recognised eCat type - the caller reports that as NOT CHECKED, because a
    file B7 could not classify is precisely where a lossy regeneration hides.
    """
    headers, body = b7_lossy.read_file(produced)
    ftype, _note = b7_lossy.detect_file_type(produced, headers)
    if not ftype:
        raise RuntimeError('not a recognised eCat file type: %s'
                           % os.path.basename(produced))
    return b7_lossy.emit_sql(produced, ftype, headers, body, org, 50)


def _verdict(not_checked, emitted_only=(), blocking=()):
    """Say which of the three RAN, which only EMITTED, which could not run.

    A gate that skipped a check must never exit 0: the operator reads the exit
    code, and "B6 could not run" and "B6 ran clean" are different states that
    used to produce the same silence. Nor may a gate that only PRINTED a query
    exit 0 — that was this file's own version of the same defect, and it is
    the reason `emitted_only` exists as a third state rather than being folded
    into either of the other two.
    """
    print()
    print('=' * 70)
    print('GATE COVERAGE — BUILD_SPEC §3.4')
    print('=' * 70)
    blocked = list(not_checked) + list(emitted_only)
    ran = [c for c in ('B6', 'B7', 'A1')
           if not any(n.startswith(c) for n in blocked)]
    if blocking:
        print('  BLOCKING     : %d' % len(blocking))
        for b in blocking:
            print('     %s' % b)
    print('  RAN          : %s' % (', '.join(ran) or 'none'))
    print('  EMITTED ONLY : %s' % ('%d of 3' % len(emitted_only)
                                   if emitted_only else 'none'))
    for n in emitted_only:
        print('     %s' % n)
    print('  NOT CHECKED  : %s' % ('%d of 3' % len(not_checked)
                                   if not_checked else 'none'))
    for n in not_checked:
        print('     %s' % n)
    # A check that RAN and FOUND something outranks a check that could not
    # run: the first is certain and actionable, the second is an absence.
    # Before 2026-09-09 this returned 0 with `BLANKED LongDesc 1020 of 1020
    # rows` printed three lines above it. B6 reported the exact shape that
    # cost Legrand 19 products' images -- under a heading that says "read this
    # first" -- and the gate exited clean. On leg the regression byte-check
    # caught it; no new client has one.
    if blocking:
        print()
        print('  A check RAN and found a BLOCKING problem. DO NOT UPLOAD.')
        return 4
    if not_checked:
        print()
        print('  A skipped check is not a passed check. Do not upload on this run.')
        return 2
    if emitted_only:
        print()
        print('  SQL was produced and nothing was measured. Either re-run with')
        print('  --use-db and a read-only DATABASE_URL, or run the emitted')
        print('  statements through the supercat-postgres-vpn MCP and feed the')
        print('  rows back with --from-results. Do not upload on this run.')
        return 3
    print()
    print('  All three RAN against the thing each of them names: B6 the '
          'previous file,')
    print('  B7 live state, A1 the org.')
    return 0


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    produced, previous = sys.argv[1], sys.argv[2]
    org = None
    if '--org' in sys.argv:
        org = sys.argv[sys.argv.index('--org') + 1]
    use_db = '--use-db' in sys.argv

    # Each check records itself here rather than returning early. Before
    # 2026-09-09 a NOT CHECKED B6 did `return 2`, which skipped B7 and A1
    # entirely - so the two strongest checks were dropped exactly when the file
    # was least understood, and the exit code said "gate failed" when it meant
    # "gate stopped". A check that could not run must say so and let the others
    # run; that is BUILD_SPEC §3.4 applied to the gate itself, not just to the
    # checks inside it.
    not_checked = []
    # Third state, separate from not_checked on purpose: see _verdict.
    emitted_only = []
    # Fourth: a check that ran and FOUND something. This is what makes the
    # file refuse rather than merely be described.
    blocking = []

    new_rows = lib.read_rows(produced)
    prev_rows = lib.read_rows(previous)
    key = lib.diff_key_for(produced)
    d = lib.diff_against_previous(prev_rows, new_rows, key_column=key)

    print('=' * 70)
    print('B6 — regeneration diff')
    print('=' * 70)
    print('  previous : %s (%d rows)' % (os.path.basename(previous), len(prev_rows)))
    print('  produced : %s (%d rows)' % (os.path.basename(produced), len(new_rows)))
    print('  keyed on : %s' % key)
    if d.get('key_missing'):
        print()
        print('  NOT CHECKED — %s' % d['key_missing'])
        print('  B6 reports nothing below. That is a missing key, NOT a clean diff.')
        print('  B7 and A1 still run — they do not need this key.')
        print()
        not_checked.append('B6 — %s' % d['key_missing'])
        d = None
    if d is not None:
      print('  compared : %d rows present on both sides' % d.get('compared', 0))
      print()
      print('  BLANKED columns (had a value, now empty) — read this first:')
      if not d['blanked']:
          print('     none')
      for col, n in sorted(d['blanked'].items(), key=lambda x: -x[1]):
          ex = d['blanked_examples'].get(col, [])
          print('     %-24s %5d of %d rows   e.g. %s'
                % (col, n, len(new_rows), ', '.join(ex[:3])))
      print()
      print('  dropped keys : %d%s' % (len(d['dropped']),
            ('   e.g. ' + ', '.join(d['dropped'][:3])) if d['dropped'] else ''))
      print('  added keys   : %d%s' % (len(d['added']),
            ('   e.g. ' + ', '.join(d['added'][:3])) if d['added'] else ''))
      if d['dropped']:
        # Delete semantics are per file type, and they set the severity: a
        # soft-delete leaves `deleted=true` to reverse, a hard-delete leaves
        # nothing at all.
        semantics = {'BillToCode': 'customers.csv HARD-DELETES',
                     'Code': 'this file HARD-DELETES',
                     'BaseItemCode': 'products.csv SOFT-DELETES (inventory.csv HARD-DELETES)'}
        print('     ! %s omitted rows on a clean import.'
              % semantics.get(key, 'this file removes'))
      print()
      print('  changed columns:')
      if not d['changed']:
        print('     none — output is identical to the previous build')
      for col, n in sorted(d['changed'].items(), key=lambda x: -x[1]):
        print('     %-24s %5d of %d rows' % (col, n, len(new_rows)))

      # --- B6 now REFUSES rather than merely reporting -------------------
      # Blanking is the dangerous direction and it is BLOCKING for every file
      # type: a regenerated file that empties a column imports CLEAN, so
      # nothing downstream objects. Row loss is severity-by-file-type -- a
      # soft-delete leaves `deleted=true` to reverse, a hard-delete leaves
      # nothing -- so it is graded rather than uniform.
      for col, n in sorted(d['blanked'].items(), key=lambda x: -x[1]):
        blocking.append(
            'B6 - BLANKED: %s had a value on %d of %d rows and is now empty. '
            'A file that blanks a column imports CLEAN; this is the shape that '
            'cost Legrand 19 products their live images.'
            % (col, n, len(new_rows)))
      if d['dropped']:
        hard = key in ('BillToCode', 'Code') or 'inventory' in os.path.basename(
            produced).lower()
        pct = (100.0 * len(d['dropped']) / len(prev_rows)) if prev_rows else 0.0
        msg = ('B6 - %d of %d key(s) in the previous file (%.1f%%) are absent '
               'from this one and would be %s on a clean import (e.g. %s)'
               % (len(d['dropped']), len(prev_rows), pct,
                  'HARD-DELETED, with nothing left to reverse'
                  if hard else 'SOFT-DELETED (reversible via deleted=true)',
                  ', '.join(d['dropped'][:3])))
        # SCALE, not just delete semantics. Grading purely on soft-vs-hard put
        # drf at WARN for dropping 1,627 of 1,627 keys -- a file that would
        # soft-delete the ENTIRE previous catalogue -- because products.csv
        # happens to be reversible. Reversible is not the same as intended, and
        # a 100% drop is not a large version of a small one: it means the two
        # files do not share a key space. drf's build is keyed pattern x
        # colourway and its source carries only the pattern, which is exactly
        # what a 0%-overlap diff looks like.
        #
        # The 50% threshold is A1's, deliberately: A1 already calls
        # `pct_org < 50` fatal. Two checks reading the same shape should not
        # disagree about whether it is serious.
        if hard or pct >= 50.0:
          blocking.append(msg + (
              '  -- and the two files share NO keys at all, so this is not a '
              'deletion, it is a different key space'
              if d.get('compared') == 0 and not d['blanked'] else ''))
        else:
          print('     WARN: %s' % msg)

    print()
    print('=' * 70)
    print('B7 — lossy regeneration gate')
    print('=' * 70)
    if not org:
        print('  NOT CHECKED — no --org given. Do not upload without it.')
        not_checked.append('B7 — no --org given')
    else:
        print('  B6 above compared this file to the PREVIOUS FILE. B7 compares it to')
        print('  LIVE STATE, which is the only thing that catches a first regeneration')
        print('  from a lossy export.')
        print()
        # Wired 2026-09-09. This section used to PRINT the command to run B7 and
        # then move on, which is a suggestion, not a gate - the operator could
        # skip it and preupload_check would still exit 0. It now calls B7 and
        # emits the SQL itself.
        try:
            b7_meta, b7_stmts = _run_b7(produced, org)
        except Exception as exc:                      # noqa: BLE001
            print('  NOT CHECKED — %s' % exc)
            not_checked.append('B7 — %s' % exc)
            print('  Treat that as NOT CHECKED, not as a pass: an unrecognised or')
            print('  unreadable file is exactly the case a lossy regeneration hides in.')
            b7_meta = None
        if b7_meta:
            print('  file type   : %s (keyed by %s, %d rows)'
                  % (b7_meta['file_type'], b7_meta['key_column'], b7_meta['file_rows']))
            print('  omitted rows: %s  ->  %s on a material fill drop'
                  % (b7_meta['omitted_records'],
                     'BLOCKING' if b7_meta['omitted_records'].startswith('HARD')
                     else 'WARN'))
            print('  columns     : %d evaluated, %d with no live counterpart%s'
                  % (len(b7_meta['evaluated_columns']),
                     len(b7_meta['not_checked_columns']),
                     (' (%s)' % ', '.join(b7_meta['not_checked_columns'][:6]))
                     if b7_meta['not_checked_columns'] else ''))
            if use_db:
                # Run it here. This is the difference between a gate and a
                # suggestion, and it is the only reason the gate can run on a
                # cron next to the database.
                try:
                    b7_res = b7_lossy._results_from_db(b7_meta, b7_stmts)
                    lines, b7_blocking, warn, nc, spot, evaluated, compared = \
                        b7_lossy.report(b7_meta, b7_res, 10.0, 20.0)
                    print()
                    for l in lines:
                        print('  ' + l)
                    for l in spot:
                        print('  ' + l)
                    print('  evaluated %d of %d file columns for density'
                          % (evaluated,
                             len(b7_meta['evaluated_columns'])
                             + len(b7_meta['not_checked_columns'])))
                    print('  value spot-check: %s'
                          % ('ran' if compared else
                             'NOT CHECKED - nothing comparable'))
                    for n in nc:
                        print('  NOT CHECKED  %s' % n)
                    for b in b7_blocking:
                        print('  BLOCKING [pre_upload] : %s' % b)
                    for w in warn:
                        print('  WARN     [pre_upload] : %s' % w)
                    if b7_blocking:
                        blocking.extend('B7 - %s' % b for b in b7_blocking)
                except Exception as exc:                      # noqa: BLE001
                    print('  NOT CHECKED - DATABASE_URL path failed: %s' % exc)
                    not_checked.append('B7 - --use-db failed: %s' % exc)
            else:
                # Named per FILE TYPE, not just per org. A single gate run
                # over products.csv and inventory.csv wrote both to
                # `b7_leg.sql` and the second silently replaced the first, so
                # the operator ran inventory's SQL believing it covered
                # products. Found 2026-09-09 by gating two files in one run.
                out = os.path.join(
                    os.path.dirname(os.path.abspath(produced)),
                    'b7_%s_%s.sql' % (org, b7_meta['file_type'].replace('.csv', '')))
                with open(out, 'w') as fh:
                    fh.write('-- B7 lossy-regeneration gate, %s -> org %s\n'
                             '-- read-only. Run through supercat-postgres-vpn.\n\n'
                             % (os.path.basename(produced), org))
                    for st in b7_stmts:
                        fh.write(st + ';\n\n')
                print('  SQL written : %s' % out)
                print()
                print('  EMITTED ONLY - nothing was measured. Run it read-only, then:')
                print('     python3 acceptance/b7_lossy.py %s --org %s --from-results <json>'
                      % (produced, org))
                print('  or re-run this gate with --use-db and a read-only DATABASE_URL.')
                emitted_only.append(
                    'B7 - SQL emitted to %s, not evaluated. Needs Postgres.'
                    % os.path.basename(out))
        print()
        print('  A1 counts KEYS, so a file with every key present and half its columns')
        print('  empty passes A1 at 100%. The hazard is column blanking, not row')
        print('  deletion, and every eCat file type is exposed to it.')

    print()
    print('=' * 70)
    print('A1 — org fingerprint')
    print('=' * 70)
    if not org:
        print('  NOT CHECKED — no --org given. Do not upload without it.')
        not_checked.append('A1 — no --org given')
        return _verdict(not_checked, emitted_only, blocking)
    if use_db:
        try:
            ftype, keycol, keys, blank, note = a1_fingerprint.read_keys(produced)
            sql, err = a1_fingerprint.emit_sql(ftype, keys, org)
            if err:
                print('  NOT CHECKED - %s' % err)
                not_checked.append('A1 - %s' % err)
            else:
                res = a1_fingerprint._results_from_db(sql)
                if not res.get('summary'):
                    print('  NOT CHECKED - the query returned no summary row. '
                          'An empty result is not a clean fingerprint.')
                    not_checked.append('A1 - empty summary row')
                else:
                    summary = (res['summary'][0]
                               if isinstance(res['summary'], list)
                               else res['summary'])
                    print('  file      : %s (%s, keyed by %s)'
                          % (os.path.basename(produced), ftype, keycol))
                    print('  target org: %s (id %s)'
                          % (summary['target_shortname'],
                             summary['target_org_id']))
                    lines, fatal, warn = a1_fingerprint.verdict(
                        summary, ftype, res.get('rivals'))
                    for l in lines:
                        print('  ' + l)
                    for f in fatal:
                        print('  BLOCKING [pre_upload] : %s' % f)
                    for w in warn:
                        print('  WARN     [pre_upload] : %s' % w)
                    if fatal:
                        blocking.extend('A1 - %s' % f for f in fatal)
        except Exception as exc:                              # noqa: BLE001
            print('  NOT CHECKED - DATABASE_URL path failed: %s' % exc)
            not_checked.append('A1 - --use-db failed: %s' % exc)
    else:
        print('  EMITTED ONLY - nothing was measured. Run it read-only through')
        print('  supercat-postgres-vpn:')
        print('     python3 acceptance/a1_fingerprint.py %s --org %s --emit-sql'
              % (produced, org))
        print('  then feed the rows back with --from-results, or re-run this')
        print('  gate with --use-db and a read-only DATABASE_URL.')
        emitted_only.append('A1 - not evaluated. Needs Postgres.')
    print()
    print('  A clean import proves the file parsed. It proves nothing about')
    print('  whether it was right, and nothing about whether it was the right org.')
    return _verdict(not_checked, emitted_only, blocking)


if __name__ == '__main__':
    sys.exit(main())
