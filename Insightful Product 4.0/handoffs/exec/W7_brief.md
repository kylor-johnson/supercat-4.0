# W7 — Phase 9: the remaining seven backlog queries

**Working tree:** `~/repos/supercat-4.0/Insightful Product 4.0`
**Branch:** cut `exec/W7-backlog-queries` from `main`. Do not work on `main`.
**Requires:** VPN up and the `supercat-postgres-vpn` MCP connected.

## Read first, in this order

1. `handoffs/exec/TRAPS.md` — all 16 entries. Non-negotiable.
2. `handoffs/exec/README.md` — the stamp protocol.
3. `git log --oneline -8` and read the full message of the two commits whose
   subjects begin "Phase 9, first query" and "Q-ORG-DECAY". **They are your
   worked examples.** Your job is the same shape, seven more times.

## The state you are inheriting

26 of 111 library queries are wired. `make check` is green: 895 tests,
`GOLDEN SET: PASS (11/11)`, golden v24, cohort clean. Every org SHIPs except
bsc (REDIRECT, the correct-refusal path — it is the ONLY regression coverage
of that path, never let it change).

Two queries were wired this way already: `Q-53` and `Q-ORG-DECAY`. Copy that
pattern exactly.

## Your queue

Do them one at a time, each its own commit, `make check` green before you
move on. Ordered by expected value:

| # | Query | What it answers | Notes |
|---|---|---|---|
| 1 | `Q-68` | Contraction vs the account's OWN historical peak rolling-12 | Complements S1's 6mo-vs-6mo with a longer horizon. Gate: `HAS_PORTAL_ORDERS` + `PORTAL_CUSTOMER_DATA_PRESENT` |
| 2 | `Q-51` | Rep-level eCat capture | Pairs with the rep-activity block already in §6 |
| 3 | `Q-52` | Customer-level eCat penetration | Pairs with Q-53; do not duplicate its list |
| 4 | `Q-61` | New-item adoption gap (`new_item = true`) | Gate: org has new items |
| 5 | `Q-59` | Fill rate + backorder revenue exposure | Gate: `HAS_INVENTORY`. Note methodology already says "Stock-outs: backorder field is unpopulated" — if that is still true for an org, this query yields nothing and that sentence must stay |
| 6 | `Q-20` | eCat AOV | Contains an intentional non-filtered "Quote Orders" contrast row — **never sum it into eCat sales** |
| 7 | `Q-21` | eCat order type / workflow | Pairs with the Q-R4 submit-rate block. hfg's 30% submit rate is the live example |

## The procedure, per query

1. **Verify the SQL exists before adding the name.** Catalog hygiene:
   ```
   .venv-renderer/bin/python -c "from pipeline import cache; print(cache.extract_sql('Q-68')[:200])"
   ```
   `extract_sql` returns the FIRST fenced block after the heading — check that
   is the block you want (Q-ORG-DECAY has two; step 1 is the right one).
2. Add the id to `config.QUERIES_GATHER` with a one-line comment.
3. `populate_cache --org X --date D --queries Q-68` for each org in
   `tools/cohort.conf`. Skip orgs the gate excludes and say why.
4. **Pull via MCP with the VALUES pattern** — write the SQL once, iterate orgs:
   ```sql
   SELECT p.org, (SELECT json_agg(row_to_json(_q)) FROM ( <body, organization_id = p.oid> ) _q) AS "Q-68"
   FROM (VALUES ('hfg',165),('kal',146)) AS p(org,oid);
   ```
   Postgres accepts outer references inside a CTE in a scalar subquery — this
   is verified. Org ids: sarreid 1, bmc 11, bsc 14, clc 40, da 62, ali 127,
   kal 146, cci 161, hfg 165, bri 222, sca 90.
5. Write the result to JSON, then **verify against the database before
   importing** (TRAPS #14): row counts, two independent sums, and an MD5 of
   the ranked identity pairs. Do not import on a mismatch.
6. `mcp_cache_tool import-batch --org X --date D --result f.json`.
   For a query that legitimately returns nothing for an org, write a
   header-only CSV so "empty" is recorded rather than looking unpulled.
7. Dataclass + loader in `gather.py`. Loader drops rows with no identity
   (TRAPS #10) and rows missing the field the finding depends on.
8. Bundle field, and **read it BEFORE `outreach_screen.apply()`** (TRAPS #9).
9. Screen any named list through `bill_to_is_screened`.
10. Render. Gate on posture AND on the list being non-empty — omit, never stub.
    Label platform dollars as platform order volume, never invoiced revenue.
11. Tests: one for the loader's drop rules, one for the gate, one that the
    rendered figure agrees with the rows beneath it (TRAPS #7).
12. `make check`, read `cohort_diff.sh --full`, re-baseline, re-stamp, commit.

## Claim rules you must honour

Each query's library entry has an **External claim rules** paragraph. They are
binding, not advisory. The recurring ones:

- Never write "ERP" in client-facing copy — it is "total business".
- Never frame low platform penetration as failure; it may be legitimate
  multi-channel business.
- An activation gap is an opportunity, never a verdict on the account.
- A quote is interest, not adoption.

## Definition of done

- `make check` exit 0: tests pass, `GOLDEN SET: PASS (11/11)`, cohort clean
- Every org still SHIP/REDIRECT; bsc byte-identical
- `foundation/WHAT_ACTUALLY_RUNS.md` updated in the SAME commit as each query
- One commit per query, message stating what it surfaces per org with numbers
- `handoffs/exec/W7_evidence.md`: per query, the verification aggregates you
  ran and their match, plus any org you excluded and the gate that excluded it

## What will get you a REWORK

- A number on the page that disagrees with the rows beneath it
- A named list that skipped `bill_to_is_screened`
- Re-baselining without pasting the diff you read
- "I verified it" without the aggregate query and its output
- Touching bsc's output
