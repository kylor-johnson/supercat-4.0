# Onboarding collector

Runs the Phase Progression framework's Postgres reads **inside the VPN** and emits a
dated snapshot, optionally loading it to BigQuery so an agent outside the network can
read it.

Why: `mcp-postgres-tools.tools.supercatsolutions.com` is split-horizon DNS — NXDOMAIN
on public resolvers. No cloud-hosted agent can reach Postgres, with or without
credentials. So state travels out; queries don't go in.

```
[inside VPN]                        [BigQuery]                 [anywhere]
 collector.py  ──push snapshot──>  onboarding_assessment.*  <──read──  agent
                                    + fathom + helpscout               (SA key only)
```

## Files

| file | what it is |
|---|---|
| `queries.py` | every spec-derived query, columns verified against live `information_schema` |
| `collector.py` | runner, block parser, domain resolution, snapshot builder, BQ loader |
| `RECONCILIATION.md` | **read this** — framework vs. skills vs. live schema, incl. one blocker bug |

## Two ways to run

**A — direct** (needs read-only DB creds; this is the cron-able one):

```bash
pip install psycopg2-binary pyyaml
DATABASE_URL=postgres://... ./collector.py --orgs mali,tcd,pebl,drf --load-bq
```

**B — through the MCP** (works today, zero new credentials):

```bash
# 1. resolve org ids via the supercat-postgres-vpn MCP, save as orgs.json
./collector.py --orgs-file orgs.json --emit-sql > plan.json
# 2. run plan.json's statements through the MCP, save as results.json
./collector.py --from-results results.json --load-bq
```

`plan.json` carries every statement fully rendered with literals — nothing to
parameterize by hand.

## Backtesting

```bash
./collector.py --orgs tcd --as-of 2026-03-01
```

`--as-of` filters every **append-only** source (`import_events`, `orders`). Mutable
tables cannot be reconstructed, so they are captured as of *today* and the snapshot
carries a `temporal_warning` plus a per-metric `POINT_IN_TIME` / `CURRENT_STATE` tag.

Practically: **Phases 1–3 backtest honestly. Phases 4–7 do not** — they depend on
current-state tables. Validate those forward on `leg`, the only org still in the
cohort.

Once snapshots accumulate, current-state history exists going forward and that
limitation lifts on its own.

## The incompleteness contract

A metric that can't be read emits `NOT_CAPTURED` with a reason. Never a zero, never
a silent omission — same rule as `preflight_gate.py`. Every snapshot carries:

```json
"completeness": {"metrics_expected": 13, "metrics_captured": 13},
"not_captured": [],
"flags": []
```

If that ever reads `11/13`, the snapshot names which two and why. Trust the count,
not the vibe.

## What is verified vs. what is not

Verified live 2026-08-18:
- every column referenced exists (`information_schema`)
- `orders_matched` returns real numbers on tcd (7 submitted, 6 customer-matched)
- catalog / customer / rep counts match hand-run queries
- the `import_events` block regex catches all 10 block types that actually occur
- block-level tier resolution: newest-first wins, a stale fatal is not masked

Not yet verified:
- a full `--from-results` round trip (needs the 52 statements actually executed)
- the BigQuery loader against a real table (creates `org_state_snapshots` on first run)
- `--as-of` output compared to a known historical phase

That last one is the next piece of work, and it's the one that tells you whether the
framework is right.
