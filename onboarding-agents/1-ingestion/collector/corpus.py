#!/usr/bin/env python3
"""
Build CORPUS_<sn>.md — the raw, deduplicated, chronological record of everything
said to or about one client: every Fathom call transcript and every HelpScout
thread, in time order.

This is L2 of the ground-truth method. It is RAW DATA ONLY. Nothing in here
interprets, summarises, or assigns a phase — that is the reading agent's job,
and it must do it blind.

VERIFIED MECHANICS (2026-08-18) — get these wrong and the corpus lies:

  1. Fathom summaries and transcripts join on `Recording Share URL`, NEVER `ID`.
     The ID columns are unrelated: 0 of 933 match. The URL matches 921 of 933.
     A join on ID silently yields zero transcripts and looks like missing data.

  2. The same call is recorded by several Fathom users under different
     recording_ids. Dedupe on (meeting_title, meeting_start) or you read the
     same call up to 4 times. Raw -> unique: drf 17->11, mali 30->18,
     tcd 7->5, pebl 2->1.

  3. Domain matching is PRIMARY; title regex is secondary. Title search found
     fewer calls than the domain join for every client, and zero for pebl
     (its only call is titled "Discovery Call").

  4. HelpScout tickets that never touch a client domain still carry the client's
     story: mali has 56 tickets on supercatsolutions.com that mention Magic Lite,
     and tcd has 4 on gmail.com. Those are tiers B and C — included, but labeled,
     because a mention is not proof of relevance.

Usage:
    ./corpus.py --client tcd --manifest          # counts only, no dump
    ./corpus.py --client tcd --out CORPUS_tcd.md
    ./corpus.py --client mali --before 2026-04-01 --out CORPUS_mali_part1.md
    ./corpus.py --client mali --since  2026-04-01 --out CORPUS_mali_part2.md
"""

from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime, timezone

BQ_PROJECT = "supercat-data-pipeline"
DEFAULT_SA_KEY = os.path.expanduser(
    "~/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/integrations/"
    "bigquery/service-account/supercat-data-pipeline-ac0671b8d44a.json"
)

STAFF_DOMAIN = "supercatsolutions.com"

# Domain sets confirmed 2026-08-18. `partner` domains are third parties who are
# genuinely part of the client's journey (ERP integrators), not noise.
# `token_rx` finds mentions in threads that never touch a client domain.
CLIENTS = {
    "tcd": {
        "name": "Terracotta Designs",
        "org_id": 282,
        "domains": ["terracottalighting.com"],
        "partners": [],
        "token_rx": r"terracotta",
        "note": ("admin-email fallback yields 12 domains, 11 of them rep agencies "
                 "(carolinafixturesales, rickylights, finelightsales, markneal, "
                 "vincehall, vackaragency, prairielakes, lmlightinggroup) — "
                 "deliberately NOT in tier A; they may still surface in tier C"),
    },
    "pebl": {
        "name": "Skyard Furniture Co Ltd. (Pebl)",
        "org_id": 275,
        "domains": ["peblfurniture.com", "skyard-outdoor.com"],
        "partners": [],
        "token_rx": r"pebl|skyard",
        "note": ("brand 'Pebl' != legal name 'Skyard Furniture Co Ltd.'. "
                 "Email-only journey: 1 call, ~94 threads. "
                 "CORRECTED 2026-08-25: ica.com.tr and sezondekor.com are DISTRIBUTORS, not "
                 "suppliers — each has its own Admin user group ('ICA', 'Albania-Sezon Dekor') "
                 "and ICA has placed 2 orders. They are excluded from tier A only because they "
                 "have ZERO HelpScout tickets (verified), so inclusion would change nothing. "
                 "If either ever files a ticket, add it to `domains`."),
    },
    "drf": {
        "name": "Dorell Fabrics",
        "org_id": 290,
        "domains": ["dorellfabrics.com", "loomcraft.com"],
        "partners": [],
        "token_rx": r"dorell|loomcraft",
        "note": "brian@loomcraft.com attends drf onboarding calls — confirmed second domain",
    },
    "leg": {
        "name": "Legrand US",
        "org_id": 273,
        "domains": ["legrand.com"],
        "partners": [],
        # 'radiant' is deliberately NOT in the token: it is a common English word
        # and would drag in unrelated lighting threads. 'adorne' is distinctive.
        "token_rx": r"legrand|adorne",
        "note": ("THE ONLY ORG WITH status='onboarding' — this is the entire auto-cohort. "
                 "Identity trap: a second, inactive org is also named 'legrand' "
                 "(shortname `lna`, id 93, created 2015) — a name match returns two orgs; "
                 "the live one is id 273 / `leg`. order_email_recipient is EMPTY, so domain "
                 "resolution falls to the admin-email fallback, which yields legrand.com "
                 "cleanly (6 users, 5 non-admin). Brands: adorne and radiant."),
    },
    "mali": {
        "name": "Magic Lite | NSL",
        "org_id": 285,
        "domains": ["magiclite.com", "nslusa.com", "nslusa.co", "magiclite.co"],
        "partners": ["endeavoursolutions.com", "endeavor4solutions.com"],
        "token_rx": r"magic ?lite|nslusa|nsl\b",
        "note": ("two brands in one org (ML + NSL). Endeavour Solutions is the "
                 "**Dynamics GP** integrator (NOT Business Central — corrected "
                 "2026-08-25 by the mali blind read) and attends integration calls; "
                 "part of the journey, tier C. The .co variants are NOT typos: they "
                 "appear zero times in the corpus and exist only as the fabricated "
                 "login addresses of two eOL public-site service accounts. Harmless "
                 "to keep in the filter, but do not describe them as client domains."),
    },
}


def bq_client(sa_key: str):
    from google.cloud import bigquery
    from google.oauth2 import service_account
    creds = service_account.Credentials.from_service_account_file(sa_key)
    return bigquery.Client(credentials=creds, project=BQ_PROJECT)


def _arr(vals: list[str]) -> str:
    return "[" + ",".join("'" + v.replace("'", "\\'") + "'" for v in vals) + "]"


# --------------------------------------------------------------------- fathom

FATHOM_SQL = """
WITH flat AS (
  SELECT recording_id, meeting_title, meeting_start, duration_minutes,
         recording_url, invitee_names, invitee_emails_raw, summary,
         ARRAY_TO_STRING(external_domains, ',') AS domstr
  FROM `{p}.onboarding_assessment.fathom_recent_meetings`
),
hits AS (
  SELECT DISTINCT meeting_title, meeting_start, duration_minutes, recording_url,
         invitee_names, invitee_emails_raw, summary, domstr
  FROM flat
  WHERE REGEXP_CONTAINS(LOWER(meeting_title), r'{rx}')
     OR EXISTS (SELECT 1 FROM UNNEST(SPLIT(domstr, ',')) d
                WHERE TRIM(d) IN UNNEST({alldom}))
),
dedup AS (
  -- same call, several recorders -> one row
  SELECT meeting_title, meeting_start,
         MAX(duration_minutes)                                     AS duration_minutes,
         ARRAY_AGG(recording_url IGNORE NULLS ORDER BY recording_url)[SAFE_OFFSET(0)] AS url,
         ARRAY_AGG(invitee_emails_raw IGNORE NULLS
                   ORDER BY LENGTH(invitee_emails_raw) DESC)[SAFE_OFFSET(0)] AS emails,
         ARRAY_AGG(invitee_names IGNORE NULLS
                   ORDER BY LENGTH(invitee_names) DESC)[SAFE_OFFSET(0)]      AS names,
         ARRAY_AGG(summary IGNORE NULLS
                   ORDER BY LENGTH(summary) DESC)[SAFE_OFFSET(0)]            AS summary,
         ARRAY_AGG(domstr IGNORE NULLS
                   ORDER BY LENGTH(domstr) DESC)[SAFE_OFFSET(0)]             AS domstr,
         COUNT(*) AS dupe_recordings
  FROM hits GROUP BY 1, 2
)
SELECT d.meeting_title, d.meeting_start, d.duration_minutes, d.url, d.emails,
       d.names, d.summary, d.domstr, d.dupe_recordings,
       c.`Transcript Plaintext` AS transcript
FROM dedup d
LEFT JOIN `{p}.Fathom.call-transcripts` c
       ON c.`Recording Share URL` = d.url    -- NOT ID; see module docstring
{where}
ORDER BY d.meeting_start
"""


# ------------------------------------------------------------------ helpscout

HELPSCOUT_SQL = """
SELECT
  ticket_number, ticket_subject, ticket_status, conversation_id,
  primary_customer_domain, tags,
  thread_id, thread_type, thread_created_at,
  thread_created_by_type, thread_author_email, thread_body,
  CASE
    WHEN primary_customer_domain IN UNNEST({alldom})     THEN 'A'
    WHEN primary_customer_domain = '{staff}'             THEN 'B'
    ELSE 'C'
  END AS tier
FROM `{p}.onboarding_assessment.helpscout_tickets`
WHERE (
    primary_customer_domain IN UNNEST({alldom})
    OR REGEXP_CONTAINS(
         LOWER(CONCAT(IFNULL(ticket_subject,''), ' ', IFNULL(thread_body,''))),
         r'{rx}')
  )
  AND thread_body IS NOT NULL AND TRIM(thread_body) != ''
  {where}
ORDER BY thread_created_at, ticket_number, thread_id
"""


def fetch(client, cfg, since, before):
    alldom = _arr(cfg["domains"] + cfg["partners"])

    fw = []
    if since:
        fw.append(f"WHERE d.meeting_start >= TIMESTAMP('{since}')")
    if before:
        fw.append(("AND" if fw else "WHERE") + f" d.meeting_start < TIMESTAMP('{before}')")
    fathom = list(client.query(FATHOM_SQL.format(
        p=BQ_PROJECT, rx=cfg["token_rx"], alldom=alldom, where=" ".join(fw))).result())

    hw = ""
    if since:
        hw += f" AND thread_created_at >= TIMESTAMP('{since}')"
    if before:
        hw += f" AND thread_created_at < TIMESTAMP('{before}')"
    hs = list(client.query(HELPSCOUT_SQL.format(
        p=BQ_PROJECT, rx=cfg["token_rx"], alldom=alldom,
        staff=STAFF_DOMAIN, where=hw)).result())

    return fathom, hs


# ------------------------------------------------------------------- rendering

def render(sn, cfg, fathom, hs, since, before) -> tuple[str, dict]:
    tiers = {"A": set(), "B": set(), "C": set()}
    for r in hs:
        tiers[r["tier"]].add(r["ticket_number"])

    no_transcript = [r for r in fathom if not (r["transcript"] or "").strip()]
    total_chars = (
        sum(len(r["transcript"] or "") + len(r["summary"] or "") for r in fathom)
        + sum(len(r["thread_body"] or "") for r in hs)
    )

    manifest = {
        "client": sn,
        "calls": len(fathom),
        "calls_without_transcript": len(no_transcript),
        "hs_threads": len(hs),
        "hs_tickets_A": len(tiers["A"]),
        "hs_tickets_B": len(tiers["B"]),
        "hs_tickets_C": len(tiers["C"]),
        "total_chars": total_chars,
        "approx_tokens": round(total_chars / 3.7),
    }

    L = []
    w = L.append
    w(f"# RAW CORPUS — {cfg['name']} (`{sn}`)\n")
    w("> **This file is raw data.** Nothing here is summarised or interpreted.\n"
      "> Read it in order. Do not read `CLIENT_PROFILE.md`, `HANDOFF.md`, or any\n"
      "> framework document before you have written your own timeline.\n")

    w(f"\nGenerated {datetime.now(timezone.utc).isoformat()}  \n")
    w(f"Window: {since or 'beginning'} → {before or 'now'}\n")

    w("\n## Manifest\n")
    w(f"| Fathom calls (deduped) | {len(fathom)} |")
    w("|---|---|")
    w(f"| …without a transcript | {len(no_transcript)} |")
    w(f"| HelpScout threads | {len(hs)} |")
    w(f"| …tier A tickets (client domain) | {len(tiers['A'])} |")
    w(f"| …tier B tickets (internal, mentions client) | {len(tiers['B'])} |")
    w(f"| …tier C tickets (third party, mentions client) | {len(tiers['C'])} |")
    w(f"| Total characters | {total_chars:,} (~{round(total_chars/3.7):,} tokens) |")

    w(f"\n**Domains (tier A):** {', '.join(cfg['domains'])}")
    if cfg["partners"]:
        w(f"  \n**Partner domains (tier C, deliberately included):** {', '.join(cfg['partners'])}")
    w(f"  \n**Mention token:** `{cfg['token_rx']}`")
    w(f"  \n**Note:** {cfg['note']}\n")

    w("\n**Tier meanings.** A = the customer of record is on a client domain. "
      "B = an internal SuperCat thread that mentions the client (forwarded mail, "
      "internal coordination). C = some other party's thread that mentions the "
      "client. **B and C are unfiltered — judge relevance yourself and record what "
      "you discarded in `GAPS_<sn>.md`.**\n")

    if no_transcript:
        w("\n> ⚠ Calls with no transcript are rendered with their Fathom AI summary "
          "instead, and flagged inline. A summary is an interpretation — weight it "
          "lower than a transcript.\n")

    # ---- chronological merge
    items = []
    for r in fathom:
        items.append((r["meeting_start"], "fathom", r))
    for r in hs:
        items.append((r["thread_created_at"], "helpscout", r))
    items.sort(key=lambda x: (x[0] is None, x[0]))

    w("\n---\n\n# Chronological record\n")

    for ts, kind, r in items:
        stamp = ts.isoformat() if ts else "unknown-date"
        if kind == "fathom":
            w(f"\n## 📞 CALL — {stamp} — {r['meeting_title']}\n")
            dup = f" · {r['dupe_recordings']} recordings merged" if r["dupe_recordings"] > 1 else ""
            w(f"*{r['duration_minutes'] or '?'} min{dup}*  ")
            w(f"*Attendees:* {r['names'] or '—'}  ")
            w(f"*Emails:* {r['emails'] or '—'}  ")
            w(f"*External domains:* {r['domstr'] or '—'}  ")
            if r["url"]:
                w(f"*Recording:* {r['url']}\n")
            tx = (r["transcript"] or "").strip()
            if tx:
                w("\n### Transcript\n")
                w("```")
                w(tx)
                w("```\n")
            else:
                w("\n### ⚠ NO TRANSCRIPT — Fathom AI summary only (interpretation, not raw)\n")
                w("```")
                w((r["summary"] or "(no summary either)").strip())
                w("```\n")
        else:
            who = r["thread_author_email"] or "unknown"
            typ = r["thread_created_by_type"] or "?"
            w(f"\n## ✉️ TICKET #{r['ticket_number']} [tier {r['tier']}] — {stamp}"
              f" — {r['ticket_subject'] or '(no subject)'}\n")
            w(f"*From:* {who} (`{typ}`) · *customer domain:* "
              f"{r['primary_customer_domain'] or '—'} · *status:* {r['ticket_status']}"
              + (f" · *tags:* {r['tags']}" if r["tags"] else "") + "\n")
            w("```")
            w((r["thread_body"] or "").strip())
            w("```\n")

    return "\n".join(L), manifest


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--client", required=True, choices=sorted(CLIENTS))
    ap.add_argument("--out", help="write markdown here (default: stdout)")
    ap.add_argument("--manifest", action="store_true", help="counts only, no dump")
    ap.add_argument("--since", help="YYYY-MM-DD inclusive")
    ap.add_argument("--before", help="YYYY-MM-DD exclusive")
    ap.add_argument("--sa-key", default=DEFAULT_SA_KEY)
    args = ap.parse_args()

    cfg = CLIENTS[args.client]
    client = bq_client(args.sa_key)
    fathom, hs = fetch(client, cfg, args.since, args.before)
    text, manifest = render(args.client, cfg, fathom, hs, args.since, args.before)

    for k, v in manifest.items():
        print(f"  {k:<26} {v}", file=sys.stderr)

    if args.manifest:
        return 0
    if args.out:
        with open(args.out, "w") as f:
            f.write(text)
        print(f"  -> {args.out}", file=sys.stderr)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
