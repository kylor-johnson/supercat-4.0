#!/usr/bin/env python3
"""import_events parser - the substrate for A4, B4, and the error taxonomy.

`import_events.data` is a Ruby-YAML blob. PyYAML is not installed here, and
pulling the blobs out to parse in Python would move megabytes for nothing: leg
alone has 160 events and one inventory event carries 237 warnings.

**So the parse happens in SQL and only structured summaries come back.** That is
not a shortcut - it is what makes the eventual fleet run affordable. Every mode
aggregates server-side and returns small rows.

## The format

    ---
    - - Options
      - - - :error
          - 'Line 27: Code can''t be blank'
        - - :error
          - 'Line 27: Name can''t be blank'
    - - Option Groups
      - []

A top-level list of `[FileType, messages]` pairs; `[]` means clean. Severities
are `information`, `warning`, `error`, `fatal`. YAML escapes a quote by doubling
it (`can''t`).

**One event can carry several file types** - 125 of 1,920 events in the sampled
orgs do. The within-event ordinal is therefore meaningful: it is the order the
importer processed the files, which is what A4 needs.

## Modes

    events      one row per (event, file block): tier + severity counts + seq
    taxonomy    message templates with specifics masked, ranked by frequency
    signatures  per file type, the distinct message-count signatures over time
    feed_pairs  B4's substrate: candidate signature PAIRS with coverage and
                alternation counts. `signatures` cannot decide B4 on its own -
                see sql_feed_pairs.

## Scope

Org-scoped, parameterised by shortname, batched by `organization_id` because
naive full-table aggregates over `import_events` time out at 30s here. The fleet
run is `--org-ids` instead of `--org`, not a rewrite. **Do not run it fleet-wide
yet.**

Read-only: emits SQL, never connects.
"""

import argparse
import json
import re
import sys

SHORTNAME_RE = re.compile(r'^[a-z0-9_-]{1,32}$')

# NOTE on quoting, because getting it wrong fails SILENTLY: every regex below is
# a plain single-quoted SQL string, NOT an E'' string. Postgres consumes the
# backslash itself inside E'', so \s reaches the regex engine as a literal 's'
# and the pattern matches nothing - returning zero rows rather than raising. A
# parser that reports "no messages" when there are 6,115 is worse than one that
# breaks loudly.
#
# Message bodies are captured with [^\n]* rather than .* because Postgres regex
# `.` DOES match a newline, so `.*` swallows every following message into the
# first one.

BLOCKS_CTE = r"""
blocks AS (
  SELECT e.id AS event_id, e.organization_id, e.created_at, b.ord AS seq,
         regexp_replace(split_part(b.blk, chr(10), 1), '^- - ', '') AS file_type,
         b.blk AS blk
  FROM import_events e,
       LATERAL regexp_split_to_table(
         regexp_replace(e.data, '^---\n', ''), '\n(?=- - )')
         WITH ORDINALITY AS b(blk, ord)
  WHERE {org_filter}
)"""

MSG_RE = r"'- - :([a-z_]+)\n\s+- ([^\n]*)'"
SEV_RE = r"'- - :([a-z_]+)'"

# Mask the specifics out of a message so its SHAPE can be counted. Order
# matters: strip line numbers and identifiers before collapsing bare digits, or
# the identifiers stop being recognisable. The third rule truncates messages
# that embed a data value after a colon ("Illegal quoting ... following text:
# Ivory"), which otherwise fragment one template into a dozen.
TEMPLATE_EXPR = r"""
regexp_replace(
 regexp_replace(
  regexp_replace(
   regexp_replace(
    regexp_replace(
     regexp_replace(msg, 'Line [0-9]+', 'Line N'),
    '(BaseItemCode|Code|SKU|ItemNumber)=[^,''[:space:]]+', '\1=X'),
   '(following text|unknown|not found|for product):.*$', '\1: ...'),
  '''[^'']*''', 'Q'),
 '\m[0-9]+([.][0-9]+)?\M', 'N'),
'\s+', ' ', 'g')"""


def org_filter(shortname=None, org_ids=None):
    if org_ids:
        return 'e.organization_id IN (%s)' % ','.join(str(int(i)) for i in org_ids)
    if not SHORTNAME_RE.match(shortname or ''):
        raise SystemExit('unsafe shortname: %r' % shortname)
    return ("e.organization_id = (SELECT id FROM organizations "
            "WHERE shortname = '%s')" % shortname)


def sql_events(filt, since=None):
    """One row per (event, file block). A few hundred rows per org."""
    where = "\n  AND e.created_at >= '%s'" % since if since else ''
    return """
WITH {blocks}
, sev AS (
  SELECT event_id, organization_id, created_at, seq, file_type,
         count(*) FILTER (WHERE s='fatal')       AS n_fatal,
         count(*) FILTER (WHERE s='error')       AS n_error,
         count(*) FILTER (WHERE s='warning')     AS n_warning,
         count(*) FILTER (WHERE s='information') AS n_info
  FROM blocks b
  LEFT JOIN LATERAL (
    SELECT (regexp_matches(b.blk, {sev}, 'g'))[1] AS s
  ) m ON TRUE
  GROUP BY event_id, organization_id, created_at, seq, file_type
)
SELECT event_id, organization_id, created_at, seq, file_type,
       n_fatal, n_error, n_warning, n_info,
       CASE WHEN n_fatal>0 THEN 'fatal'
            WHEN n_error>0 THEN 'error'
            WHEN n_warning>0 THEN 'warning'
            ELSE 'clean' END AS tier
FROM sev
ORDER BY created_at, seq
""".format(blocks=BLOCKS_CTE.format(org_filter=filt + where), sev=SEV_RE).strip()


def sql_taxonomy(filt, limit=60):
    """Message templates ranked by frequency - the empirical error taxonomy.

    Aggregated in SQL, so it returns `limit` rows however many million messages
    sit behind it. That property is what makes the fleet run cheap.
    """
    return """
WITH {blocks}
, msgs AS (
  SELECT b.file_type, m.sev, m.msg
  FROM blocks b,
       LATERAL (
         SELECT (x)[1] AS sev,
                replace(btrim((x)[2], ''''), '''''', '''') AS msg
         FROM regexp_matches(b.blk, {msg}, 'g') AS x
       ) m
)
SELECT file_type, sev,
       {tmpl} AS template,
       count(*) AS n,
       left(min(msg), 90) AS example
FROM msgs
GROUP BY file_type, sev, template
ORDER BY n DESC
LIMIT {limit}
""".format(blocks=BLOCKS_CTE.format(org_filter=filt), msg=MSG_RE,
           tmpl=TEMPLATE_EXPR, limit=int(limit)).strip()


def sql_signatures(filt):
    """Per file type, the distinct message-count signatures over time.

    ## The signature is three parts, not two (corrected 2026-09-05)

    It used to be `n_warning/n_error`, which ignores `fatal` entirely - so a
    FATAL import, where the whole file is rejected and nothing changes, read as
    `0/0`, byte-identical to a clean one. Specimen: `fal` 2026-01-23,
    `Column shiptoaddress1 is missing and is required`, previously reported as
    a clean customer import.

    Now `n_warning/n_error/n_fatal`. `0/0/0` is clean; `0/0/1` is a rejected
    file. Note the README's leg example accordingly: `237/0` is now `237/0/0`.

    **This is no longer B4's detector** - see sql_feed_pairs, which needs the
    ordered stream and which DROPS fatal blocks rather than distinguishing
    them, because an import that changed nothing cannot have overwritten
    anything.
    """
    return """
WITH {blocks}
, sev AS (
  SELECT event_id, created_at, file_type,
         count(*) FILTER (WHERE s='warning') AS n_warning,
         count(*) FILTER (WHERE s='error')   AS n_error,
         count(*) FILTER (WHERE s='fatal')   AS n_fatal
  FROM blocks b
  LEFT JOIN LATERAL (
    SELECT (regexp_matches(b.blk, {sev}, 'g'))[1] AS s
  ) m ON TRUE
  GROUP BY event_id, created_at, file_type
)
SELECT file_type,
       -- warning/error/fatal. A rejected file used to read as '0/0', identical
       -- to a clean one; it now reads '0/0/1'.
       n_warning || '/' || n_error || '/' || n_fatal AS signature,
       count(*) AS events,
       min(created_at)::date AS first_seen,
       max(created_at)::date AS last_seen
FROM sev
GROUP BY file_type, signature
HAVING count(*) > 1
ORDER BY file_type, events DESC
""".format(blocks=BLOCKS_CTE.format(org_filter=filt), sev=SEV_RE).strip()


def sql_feed_pairs(filt):
    """B4's substrate: one row per candidate signature PAIR, with the three
    numbers the alternation test needs. Aggregated server-side.

    ## Why a pair-level mode exists at all

    B4 used to be decided from `--mode signatures` alone, which carries only
    (file_type, signature, events, first_seen, last_seen). From that the only
    testable relation is "do the two date ranges overlap", and for any
    long-running feed they always do. That produced **1,711 findings across 13
    orgs, 1,262 of them FATAL, of which two were defensible** - `cl` alone was
    1,033 FATALs on an Inventory feed that ran clean 5,641 times out of 5,865.

    Deciding whether two signatures ALTERNATE needs the ordered event stream,
    and streaming every block to Python is unaffordable (`cl` has 39k blocks,
    `clli` 64k). So the alternation is computed in SQL and only the pair
    summaries come back - the same principle that makes every other mode here
    cheap enough to eventually run fleet-wide.

    ## The three numbers, and what each means

        n_win    every block of this file_type inside the pair's overlap window
        n_pair   those blocks whose signature is one of the two
        alts     transitions between the two signatures, in time order,
                 restricted to the window

    `n_pair / n_win` is **coverage**. Two files feeding one importer means
    nearly every run of that importer is one file or the other, so coverage is
    the definitional test - `leg` is 37 of 37, 100%.

    `alts / (n_pair - 1)` is the **alternation rate**. `A...A B...B` is one file
    replaced by another, and scores near zero however many events it has;
    `ABABAB` is two files competing. `sp`'s Kit Items pair is 340 events at 96.6%
    coverage with **8** alternations - drift wearing coverage's clothing, and the
    reason the rate is needed as well as the count.

    ## Two-stage, and it has to stay that way

    Coverage is computed first and filtered in a `HAVING`, then `alts` is
    computed only for survivors. The one-stage form times out at 30s on `cl`
    (1,025 candidate pairs x 39k blocks); this form returns in a few seconds
    because only 246 pairs reach the window function. Do not flatten it.
    """
    return """
WITH {blocks}
, sev AS MATERIALIZED (
  SELECT event_id, created_at, seq, file_type,
         (count(*) FILTER (WHERE s='warning'))||'/'||
         (count(*) FILTER (WHERE s='error')) AS sig
  FROM blocks b
  LEFT JOIN LATERAL (
    SELECT (regexp_matches(b.blk, {sev}, 'g'))[1] AS s
  ) m ON TRUE
  GROUP BY 1,2,3,4
  -- FATAL blocks are DROPPED, not distinguished (2026-09-05). A fatal import
  -- means the whole file was rejected and nothing changed - it hard-deleted
  -- nothing and reloaded nothing, so it cannot be one side of two files
  -- overwriting each other. Giving it its own signature would count a no-op as
  -- a file switch; leaving it in inflates n_win, the coverage denominator.
  --
  -- This is NOT the same edit as adding fatal to sql_signatures, and doing
  -- that one here would be wrong. Note also that a fatal block is often NOT
  -- '0/0': across the 13-org cohort 1,292 of 1,594 fatal blocks carry warnings
  -- or errors too, and some of those signatures ARE candidate pair members
  -- (cl Inventory '1/0', sp Products '1001/0'). So this filter can change
  -- n_pair and the alternation counts, not only coverage.
  HAVING count(*) FILTER (WHERE s='fatal') = 0
)
, agg AS (
  SELECT file_type, sig, count(*) AS events,
         min(created_at) AS fs, max(created_at) AS ls
  FROM sev GROUP BY 1,2
)
-- A recurring FEED recurs over more than one day, and a clean block carries no
-- signature to compare. Both filters predate the alternation test and both
-- still earn their place.
, q AS (
  SELECT * FROM agg
  WHERE events >= 3 AND sig <> '0/0' AND fs::date <> ls::date
)
, pairs AS (
  SELECT a.file_type, a.sig AS sig_a, b.sig AS sig_b,
         a.events AS events_a, b.events AS events_b,
         greatest(a.fs, b.fs) AS win_start, least(a.ls, b.ls) AS win_end,
         greatest(a.ls, b.ls) AS pair_last_seen
  FROM q a JOIN q b ON a.file_type = b.file_type AND a.sig < b.sig
  WHERE a.fs <= b.ls AND b.fs <= a.ls
)
-- Stage 1: coverage and volume, filtered in HAVING so stage 2 stays small.
, cov AS MATERIALIZED (
  SELECT p.*, count(*) AS n_win,
         count(*) FILTER (WHERE s.sig IN (p.sig_a, p.sig_b)) AS n_pair
  FROM pairs p
  JOIN sev s ON s.file_type = p.file_type
            AND s.created_at BETWEEN p.win_start AND p.win_end
  GROUP BY p.file_type, p.sig_a, p.sig_b, p.events_a, p.events_b,
           p.win_start, p.win_end, p.pair_last_seen
  HAVING count(*) FILTER (WHERE s.sig IN (p.sig_a, p.sig_b)) >= 10
     AND count(*) FILTER (WHERE s.sig IN (p.sig_a, p.sig_b))::numeric
         / count(*) >= 0.90
)
-- Stage 2: alternations, only for pairs that survived stage 1.
SELECT c.file_type, c.sig_a, c.sig_b, c.events_a, c.events_b,
       c.win_start::date AS win_start, c.win_end::date AS win_end,
       -- F6 Decision 3. The overlap WINDOW ends at the earlier of the two
       -- signatures' last events; the PAIR is still active until the later of
       -- them. Demotion must key on the pair, not the window: leg's window ends
       -- 2026-09-03 but 237/0 ran on 09-04, which is also the last Inventory
       -- import - so the pair is STANDING and must not demote. Keying off
       -- win_end would drop A8 to WARN, which is the regression this guards.
       c.pair_last_seen::date AS pair_last_seen,
       (SELECT max(s2.created_at)::date FROM sev s2
         WHERE s2.file_type = c.file_type)      AS last_import_of_type,
       c.n_win, c.n_pair,
       (SELECT count(*) FROM (
          SELECT s.sig, lag(s.sig) OVER (ORDER BY s.created_at, s.seq) AS prev
          FROM sev s
          WHERE s.file_type = c.file_type
            AND s.created_at BETWEEN c.win_start AND c.win_end
            AND s.sig IN (c.sig_a, c.sig_b)
        ) t WHERE prev IS NOT NULL AND sig <> prev) AS alts
FROM cov c
ORDER BY c.file_type, c.n_pair DESC
""".format(blocks=BLOCKS_CTE.format(org_filter=filt), sev=SEV_RE).strip()


def to_records(rows):
    """Normalise MCP rows into structured records.

    Structured, not printed: A4, B4 and the taxonomy consume these. Nothing
    downstream should ever re-parse a formatted string.
    """
    out = []
    for r in rows:
        rec = dict(r)
        if rec.get('created_at') is not None and not isinstance(rec['created_at'], str):
            rec['created_at'] = str(rec['created_at'])
        for k in ('n_fatal', 'n_error', 'n_warning', 'n_info', 'seq', 'n',
                  'events', 'event_id', 'organization_id',
                  'n_win', 'n_pair', 'alts', 'events_a', 'events_b'):
            if rec.get(k) is not None:
                rec[k] = int(rec[k])
        out.append(rec)
    return out




# --- DATABASE_URL path (added 2026-09-09) -----------------------------------
# Before this, import_log offered --emit-sql and --from-results only, so running it
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

def _statement(args, filt):
    """The one statement for this mode.

    Factored out of main() so --emit-sql and --use-db cannot select different
    SQL for the same arguments. That divergence is not hypothetical: it is the
    class of defect where a gate reports on a query nobody ran.
    """
    if args.mode == 'events':
        return sql_events(filt, args.since)
    if args.mode == 'taxonomy':
        return sql_taxonomy(filt, args.limit)
    if args.mode == 'feed_pairs':
        return sql_feed_pairs(filt)
    return sql_signatures(filt)



def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--org', help='org shortname')
    ap.add_argument('--org-ids', help='comma-separated org ids (fleet mode; batch these)')
    ap.add_argument('--mode',
                    choices=('events', 'taxonomy', 'signatures', 'feed_pairs'),
                    default='events')
    ap.add_argument('--since', help='YYYY-MM-DD lower bound (events mode)')
    ap.add_argument('--limit', type=int, default=60)
    ap.add_argument('--emit-sql', action='store_true')
    ap.add_argument('--from-results', help='JSON list of rows from the MCP')
    ap.add_argument('--use-db', action='store_true',
                    help='run the statement directly against DATABASE_URL, '
                         'read-only. For a container; needs psycopg2.')
    ap.add_argument('--out', help='write structured records here')
    args = ap.parse_args()

    if not args.org and not args.org_ids:
        ap.error('need --org or --org-ids')
    ids = [int(x) for x in args.org_ids.split(',')] if args.org_ids else None
    filt = org_filter(args.org, ids)

    if args.emit_sql:
        print(_statement(args, filt))
        return 0

    if args.use_db:
        try:
            dbexec, sess = _session()
            with sess:
                rows = sess.rows(_statement(args, filt))
        except Exception as exc:                              # noqa: BLE001
            print('import_log NOT CHECKED - %s' % exc)
            return 2
        recs = to_records(rows)
    elif args.from_results:
        with open(args.from_results) as fh:
            recs = to_records(json.load(fh))
    else:
        ap.error('need --emit-sql, --from-results or --use-db')
    payload = {'mode': args.mode, 'org': args.org or args.org_ids,
               'record_count': len(recs), 'records': recs}
    if args.out:
        with open(args.out, 'w') as fh:
            json.dump(payload, fh, indent=2)
        print('%d records -> %s' % (len(recs), args.out))
    else:
        print(json.dumps(payload, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
