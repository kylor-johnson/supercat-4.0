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

    B4's detector. Two files feeding one importer alternately produce two
    recurring signatures rather than one.
    """
    return """
WITH {blocks}
, sev AS (
  SELECT event_id, created_at, file_type,
         count(*) FILTER (WHERE s='warning') AS n_warning,
         count(*) FILTER (WHERE s='error')   AS n_error
  FROM blocks b
  LEFT JOIN LATERAL (
    SELECT (regexp_matches(b.blk, {sev}, 'g'))[1] AS s
  ) m ON TRUE
  GROUP BY event_id, created_at, file_type
)
SELECT file_type,
       n_warning || '/' || n_error AS signature,
       count(*) AS events,
       min(created_at)::date AS first_seen,
       max(created_at)::date AS last_seen
FROM sev
GROUP BY file_type, signature
HAVING count(*) > 1
ORDER BY file_type, events DESC
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
                  'events', 'event_id', 'organization_id'):
            if rec.get(k) is not None:
                rec[k] = int(rec[k])
        out.append(rec)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--org', help='org shortname')
    ap.add_argument('--org-ids', help='comma-separated org ids (fleet mode; batch these)')
    ap.add_argument('--mode', choices=('events', 'taxonomy', 'signatures'),
                    default='events')
    ap.add_argument('--since', help='YYYY-MM-DD lower bound (events mode)')
    ap.add_argument('--limit', type=int, default=60)
    ap.add_argument('--emit-sql', action='store_true')
    ap.add_argument('--from-results', help='JSON list of rows from the MCP')
    ap.add_argument('--out', help='write structured records here')
    args = ap.parse_args()

    if not args.org and not args.org_ids:
        ap.error('need --org or --org-ids')
    ids = [int(x) for x in args.org_ids.split(',')] if args.org_ids else None
    filt = org_filter(args.org, ids)

    if args.emit_sql:
        if args.mode == 'events':
            print(sql_events(filt, args.since))
        elif args.mode == 'taxonomy':
            print(sql_taxonomy(filt, args.limit))
        else:
            print(sql_signatures(filt))
        return 0

    if not args.from_results:
        ap.error('need --emit-sql or --from-results')
    with open(args.from_results) as fh:
        recs = to_records(json.load(fh))
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
