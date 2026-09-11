#!/usr/bin/env python3
"""A1 — org fingerprint. BUILD_SPEC §3.1, the FATAL tier.

Confirm a built file's keys belong to the org you are about to upload it into,
BEFORE the upload.

    2026-08-18: Legrand's 1,020-row products.csv was imported into 111Mercer,
    soft-deleting all 102 of their products. Second occurrence of this failure
    mode (leg -> mali previously).

F6: every A1 finding is `stage: pre_upload` and severity BLOCKING, not FATAL.
`fatal` is the importer's word for a rejected file; A1 is about a file that has
not been sent yet.

Both times the file was valid, the import was clean, and the org was wrong.
Nothing about the file says which org it belongs to, so the check has to ask the
database.

## What it actually answers

Overlap alone is not the question, because a first import into an empty org
legitimately overlaps nothing. Three questions, and the verdict needs all three:

  1. How much of this file already exists in the target org?
  2. **How many live records would this import DELETE?** - the number that
     matters, and the one that would have screamed on 2026-08-18 (102 of 102).
  3. Does some OTHER org match this file better than the target does?

(3) is what actually names the incident: Legrand's codes match `leg` ~100% and
`mer` 0%. A file that fits another org better is in the wrong place regardless of
what any threshold says.

## Read-only

Emits SQL; it does not connect. Run the emitted statement through the
supercat-postgres-vpn MCP and feed the rows back with --from-results. Same
pattern as collector/rawstate.py, and for the same reason: this environment has
no direct Postgres credentials.
"""

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))

SHORTNAME_RE = re.compile(r'^[a-z0-9_-]{1,32}$')

# What each eCat file is keyed by, and what an import does to records the file
# omits. The delete semantics are the whole reason this check exists.
FILE_KEYS = {
    'products.csv':      ('BaseItemCode', 'products',  'SOFT-DELETE'),
    'inventory.csv':     ('BaseItemCode', 'inventories', 'HARD-DELETE'),
    'stories.csv':       ('BaseItemCode', None,        'sets story=null'),
    'customers.csv':     ('BillToCode',   'customers', 'HARD-DELETE'),
    'options.csv':       ('Code',         None,        'HARD-DELETE'),
    'option_groups.csv': ('Code',         None,        'HARD-DELETE'),
}

# Live table -> (key column, org column, live-row filter)
TABLES = {
    'products':    ('item_number',    'organization_id', 'NOT COALESCE(deleted,false)'),
    'inventories': ('base_item_code', 'organization_id', 'TRUE'),
    'customers':   ('code',           'organization_id', 'TRUE'),
}


def detect_file_type(path, headers):
    """Prefer the filename; fall back to the header set. Both are checked so a
    renamed file cannot quietly be judged as the wrong type."""
    base = os.path.basename(path).lower()
    by_name = next((k for k in FILE_KEYS if k in base), None)
    hset = {h.strip().lower() for h in headers}
    by_header = None
    if 'billtocode' in hset:
        by_header = 'customers.csv'
    elif 'baseitemcode' in hset:
        if 'productstory' in hset:
            by_header = 'stories.csv'
        elif any(h.startswith('qty') for h in hset):
            by_header = 'inventory.csv'
        else:
            by_header = 'products.csv'
    if by_name and by_header and by_name != by_header:
        return by_header, ('filename says %s but headers say %s - trusting the '
                           'headers' % (by_name, by_header))
    return (by_name or by_header), None


def read_keys(path):
    import csv
    import io
    with open(path, 'rb') as fh:
        raw = fh.read()
    for enc in ('utf-8-sig', 'utf-8', 'cp1252', 'latin-1'):
        try:
            txt = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        raise SystemExit('cannot decode %s' % path)
    rows = list(csv.reader(io.StringIO(txt)))
    if not rows:
        raise SystemExit('%s is empty' % path)
    headers = [h.strip() for h in rows[0]]
    ftype, note = detect_file_type(path, headers)
    if not ftype:
        raise SystemExit('cannot tell what eCat file this is: %s' % path)
    keycol = FILE_KEYS[ftype][0]
    idx = next((i for i, h in enumerate(headers) if h.lower() == keycol.lower()), None)
    if idx is None:
        raise SystemExit('%s has no %s column' % (path, keycol))
    keys, blank = [], 0
    for r in rows[1:]:
        v = r[idx].strip() if idx < len(r) else ''
        if v:
            keys.append(v)
        elif any(c.strip() for c in r):
            blank += 1
    return ftype, keycol, keys, blank, note


def sql_literal(s):
    return "'" + s.replace("'", "''") + "'"


def emit_sql(ftype, keys, shortname, candidate_limit=8):
    if not SHORTNAME_RE.match(shortname):
        raise SystemExit('unsafe shortname: %r' % shortname)
    table = FILE_KEYS[ftype][1]
    if table is None:
        return None, ('%s has no directly comparable live table; A1 cannot '
                      'fingerprint it. Fingerprint the products.csv built in the '
                      'same run instead - it shares the key space.' % ftype)
    keycol, orgcol, live = TABLES[table]
    uniq = sorted(set(keys))
    values = ',\n    '.join('(%s)' % sql_literal(k) for k in uniq)

    sql = """
WITH incoming(k) AS (VALUES
    {values}
),
target AS (
  SELECT id, shortname, name FROM organizations WHERE shortname = {sn}
),
live AS (
  SELECT t.{keycol} AS k
  FROM {table} t JOIN target o ON t.{orgcol} = o.id
  WHERE {live}
)
SELECT
  (SELECT shortname FROM target)                                   AS target_shortname,
  (SELECT id FROM target)                                          AS target_org_id,
  (SELECT count(*) FROM incoming)                                  AS file_keys,
  (SELECT count(*) FROM live)                                      AS org_live_keys,
  (SELECT count(*) FROM incoming i WHERE EXISTS
      (SELECT 1 FROM live l WHERE upper(l.k)=upper(i.k)))           AS matched,
  (SELECT count(*) FROM incoming i WHERE NOT EXISTS
      (SELECT 1 FROM live l WHERE upper(l.k)=upper(i.k)))           AS new_to_org,
  (SELECT count(*) FROM live l WHERE NOT EXISTS
      (SELECT 1 FROM incoming i WHERE upper(i.k)=upper(l.k)))       AS would_be_deleted
""".format(values=values, sn=sql_literal(shortname), keycol=keycol,
           table=table, orgcol=orgcol, live=live)

    # Which org does this file ACTUALLY look like? Indexed on
    # products(item_number); customers has no standalone index on code, so the
    # rival scan is products-only and is skipped rather than run slowly.
    rivals = ''
    if table == 'products':
        rivals = """
;
-- rival orgs: which organisations do these keys already live in?
WITH incoming(k) AS (VALUES
    {values}
)
SELECT o.shortname, o.name, count(*) AS matched_keys,
       round(100.0*count(*)/(SELECT count(*) FROM incoming), 1) AS pct_of_file
FROM incoming i
JOIN products p ON upper(p.item_number)=upper(i.k) AND NOT COALESCE(p.deleted,false)
JOIN organizations o ON o.id = p.organization_id
GROUP BY o.shortname, o.name
ORDER BY matched_keys DESC
LIMIT {lim}
""".format(values=values, lim=candidate_limit)
    return (sql.strip() + rivals), None


def verdict(res, ftype, rivals=None):
    """Turn the measured rows into a verdict. Measurements first, then the
    verdict that follows from them - never a verdict without its numbers."""
    out = []
    fk = res['file_keys']
    live = res['org_live_keys']
    matched = res['matched']
    deleted = res['would_be_deleted']
    delete_kind = FILE_KEYS[ftype][2]
    pct_file = (100.0 * matched / fk) if fk else None
    pct_org = (100.0 * matched / live) if live else None

    out.append('file keys                 : %d' % fk)
    out.append('live keys in target org   : %d' % live)
    out.append('matched                   : %d%s' % (
        matched, (' (%.1f%% of file)' % pct_file) if pct_file is not None else ''))
    out.append('new to the org            : %d' % res['new_to_org'])
    out.append('WOULD BE %-16s : %d%s' % (
        delete_kind, deleted,
        (' of %d live records (%.1f%%)' % (live, 100.0 * deleted / live))
        if live else ''))

    fatal, warn = [], []
    if live == 0:
        warn.append('target org has NO live records for this file type, so there is '
                    'nothing to fingerprint against. A1 cannot confirm the target '
                    'is right - it can only confirm it is empty. Verify the org by '
                    'another means before uploading.')
    else:
        if matched == 0:
            fatal.append('ZERO of %d file keys exist in %s, and all %d live records '
                         'would be %s. This is the 2026-08-18 shape exactly.'
                         % (fk, res['target_shortname'], deleted, delete_kind))
        elif pct_org is not None and pct_org < 50:
            fatal.append('only %.1f%% of the org\'s %d live records appear in this '
                         'file; %d would be %s.'
                         % (pct_org, live, deleted, delete_kind))
        elif deleted:
            warn.append('%d live record(s) are absent from the file and would be %s. '
                        'Intended removals are fine - confirm these are intended.'
                        % (deleted, delete_kind))

    if rivals:
        top = rivals[0]
        out.append('')
        out.append('rival orgs holding these keys:')
        for r in rivals:
            out.append('   %-10s %6d keys  %5.1f%% of file  %s'
                       % (r['shortname'], r['matched_keys'], r['pct_of_file'],
                          r['name'][:34]))
        if top['shortname'] != res['target_shortname'] and top['pct_of_file'] >= 50:
            fatal.append('these keys match org %r (%.1f%% of the file) far better '
                         'than the target %r. The file almost certainly belongs to '
                         '%s.' % (top['shortname'], top['pct_of_file'],
                                  res['target_shortname'], top['shortname']))
    return out, fatal, warn




# --- DATABASE_URL path (added 2026-09-09) -----------------------------------
# Before this, A1 offered --emit-sql and --from-results only, so running it
# meant a human carrying rows between two commands. That is workable at a desk
# and impossible on a cron: the gate could not run in the same container that
# produced the file it was meant to gate. `collector.py:197-217` had had a
# working DATABASE_URL path since August; the four modules that actually gate
# an upload had none, so a read-only replica credential on its own would still
# have left the gate unrunnable.
#
# It runs the SAME statements --emit-sql prints and assembles the SAME dict
# --from-results loads, so the two paths cannot drift into disagreeing about
# what was measured. Read-only is enforced per statement in dbexec.

def _session():
    import os as _os
    import sys as _sys
    _sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
    import dbexec
    return dbexec, dbexec.ReadOnlySession()

def _results_from_db(sql):
    """Run A1's one or two statements and return the --from-results shape.

    emit_sql() concatenates the summary and the rival-org scan into one string
    separated by `;` and a comment. Splitting on that comment rather than on
    `;` is deliberate: the VALUES lists contain no semicolons today, but a
    quoted key could, and a split that is right by luck in a gate this file
    exists to provide is not right.
    """
    dbexec, sess = _session()
    with sess:
        head, sep, tail = sql.partition('-- rival orgs:')
        res = {'summary': sess.rows(head)}
        if sep:
            res['rivals'] = sess.rows(sep + tail)
    return res



def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('file')
    ap.add_argument('--org', required=True, help='target org shortname')
    ap.add_argument('--emit-sql', action='store_true')
    ap.add_argument('--from-results', help='JSON {"summary": {...}, "rivals": [...]}')
    ap.add_argument('--use-db', action='store_true',
                    help='run the statements directly against DATABASE_URL, '
                         'read-only. For a container; needs psycopg2.')
    args = ap.parse_args()

    ftype, keycol, keys, blank, note = read_keys(args.file)
    uniq = sorted(set(keys))

    if args.emit_sql:
        sql, err = emit_sql(ftype, keys, args.org)
        meta = {
            'file': args.file, 'file_type': ftype, 'key_column': keycol,
            'key_rows': len(keys), 'distinct_keys': len(uniq),
            'blank_key_rows': blank, 'target_org': args.org,
            'omitted_records': FILE_KEYS[ftype][2],
        }
        if note:
            meta['note'] = note
        if err:
            meta['error'] = err
        print(json.dumps(meta, indent=2))
        if sql:
            print('\n-- run through supercat-postgres-vpn, read-only --')
            print(sql)
        return 0 if sql else 2

    if args.use_db:
        sql, err = emit_sql(ftype, keys, args.org)
        if err:
            print('NOT CHECKED - %s' % err)
            return 2
        try:
            res = _results_from_db(sql)
        except Exception as exc:                              # noqa: BLE001
            print('A1 NOT CHECKED - %s' % exc)
            return 2
    elif args.from_results:
        with open(args.from_results) as fh:
            res = json.load(fh)
    else:
        ap.error('need --emit-sql, --from-results or --use-db')
    if not res.get('summary'):
        print('A1 NOT CHECKED - the results carry no `summary` rows. An empty '
              'result is not a clean fingerprint.')
        return 2
    summary = res['summary'][0] if isinstance(res['summary'], list) else res['summary']

    print('=' * 70)
    print('A1 ORG FINGERPRINT')
    print('=' * 70)
    print('file      : %s' % args.file)
    print('type      : %s (keyed by %s)' % (ftype, keycol))
    if note:
        print('NOTE      : %s' % note)
    if blank:
        print('NOTE      : %d row(s) have a blank %s and were not counted'
              % (blank, keycol))
    if len(keys) != len(uniq):
        print('NOTE      : %d key rows, %d distinct - %s'
              % (len(keys), len(uniq),
                 'expected for customers.csv (ship-to rows repeat BillToCode)'
                 if ftype == 'customers.csv' else 'DUPLICATE KEYS, investigate'))
    print('target org: %s (id %s)' % (summary['target_shortname'],
                                      summary['target_org_id']))
    print('-' * 70)
    lines, fatal, warn = verdict(summary, ftype, res.get('rivals'))
    for l in lines:
        print(l)
    print('-' * 70)
    # F6 Decision 1+2. A1 used to print its own FATAL/WARN shape. The ladder is
    # now BLOCKING/WARN/INFO like every other module, and the thing FATAL was
    # really carrying here - "this has not happened yet, you can still stop" -
    # is the `stage` field. Every A1 finding is pre_upload by construction:
    # A1 runs against a FILE, before the upload that would make it true.
    for f in fatal:
        print('BLOCKING [pre_upload] : %s' % f)
    for w in warn:
        print('WARN     [pre_upload] : %s' % w)
    print('\nstage    : pre_upload - nothing here has been applied to the org yet.')
    print('repair   : none - A1 is a gate, not a defect report. The repair is to')
    print('           upload the right file to the right org.')
    if fatal:
        print('\nVERDICT: DO NOT UPLOAD')
        return 1
    if warn:
        print('\nVERDICT: PROCEED ONLY AFTER CONFIRMING THE ABOVE')
        return 0
    print('\nVERDICT: PASS - the file belongs to this org')
    return 0


if __name__ == '__main__':
    sys.exit(main())
