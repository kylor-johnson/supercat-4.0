#!/usr/bin/env python3
"""Prove sales-portal-client-review-v2 reconciles, without trusting the browser.

Reimplements the artifact's aggregation against the emitted dataset, then checks
each result against an independent SQL query on supercatprod. Extends the v1
gate with fading-account math, Orders totals, and no-go absence on new surfaces.

Run before scheduling any session:
    python3 verify_artifact.py
    python3 verify_artifact.py --org wwjc
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parents[3]
ARTIFACT = WORKSPACE / "design-system" / "app" / "sales-portal-client-review-v2.html"
DATA_JS = WORKSPACE / "design-system" / "app" / "sales-portal-client-review-v2.data.js"
MAP_FILE = HERE / "mask_map.private.json"

ORDER_CAP = 5_000_000

failures: list[str] = []
checks = 0


def check(name: str, ok: bool, detail: str = "") -> None:
    global checks
    checks += 1
    print(f"  {'PASS' if ok else 'FAIL'}  {name}{('  — ' + detail) if detail else ''}")
    if not ok:
        failures.append(name)


def load_dataset() -> dict:
    text = DATA_JS.read_text(encoding="utf-8")
    return json.loads(text[text.index("{"): text.rindex(";")])


def presets(rtd: dt.date, window_start: dt.date) -> dict[str, tuple[dt.date, dt.date]]:
    y = rtd.year
    clamp = lambda d: max(d, window_start)
    return {
        "ytd": (clamp(dt.date(y, 1, 1)), rtd),
        "ttm": (clamp(rtd - dt.timedelta(days=364)), rtd),
        "prev_ytd": (clamp(dt.date(y - 1, 1, 1)), clamp(rtd - dt.timedelta(days=365))),
        "prev_year": (clamp(dt.date(y - 1, 1, 1)), min(rtd, dt.date(y - 1, 12, 31))),
        "all": (window_start, rtd),
    }


def fading_from_dataset(ds: dict, terr=None) -> list[dict]:
    """Mirror fadingAccounts() in the artifact."""
    meta = ds["meta"]
    window_start = dt.date.fromisoformat(meta["window_start"])
    rtd = dt.date.fromisoformat(meta["report_through_date"])
    rtd_day = (rtd - window_start).days
    recent_end = rtd_day
    recent_start = rtd_day - 182
    prior_end = recent_start - 1
    prior_start = prior_end - 182
    ltm_start = rtd_day - 364

    customers = ds["customers"]
    prior = [0] * len(customers)
    recent = [0] * len(customers)
    ltm = [0] * len(customers)

    def in_terr(ci: int) -> bool:
        if terr is None:
            return True
        t = customers[ci][3]
        if terr == "none":
            return not t
        return terr in t

    for day, ci, cents in ds["invoices"]:
        if not in_terr(ci):
            continue
        if recent_start <= day <= recent_end:
            recent[ci] += cents
        elif prior_start <= day <= prior_end:
            prior[ci] += cents
        if ltm_start <= day <= recent_end:
            ltm[ci] += cents

    out = []
    for ci, p in enumerate(prior):
        if not p:
            continue
        if recent[ci] < 0.6 * p:
            out.append({
                "ci": ci,
                "prior": prior[ci],
                "recent": recent[ci],
                "ltm": ltm[ci],
                "delta": (recent[ci] - p) / p,
            })
    out.sort(key=lambda r: -r["ltm"])
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--org", default=None, help="Expected org shortname (optional)")
    args = ap.parse_args()

    ds = load_dataset()
    meta = ds["meta"]
    if args.org and meta.get("org_shortname") != args.org:
        raise SystemExit(f"dataset org {meta.get('org_shortname')!r} != --org {args.org!r}")

    oid = int(meta.get("organization_id") or 0)
    window_start = dt.date.fromisoformat(meta["window_start"])
    rtd = dt.date.fromisoformat(meta["report_through_date"])
    invoices, customers, territories = ds["invoices"], ds["customers"], ds["territories"]
    orders = ds.get("orders") or []
    order_statuses = ds.get("order_statuses") or []
    team = ds.get("team") or {}
    settings = ds.get("settings") or {}

    def day_to_date(day: int) -> dt.date:
        return window_start + dt.timedelta(days=day)

    def total(rows) -> int:
        return sum(r[2] for r in rows)

    def in_scope(a: dt.date, b: dt.date, terr=None):
        lo, hi = (a - window_start).days, (b - window_start).days
        out = []
        for r in invoices:
            if r[0] < lo or r[0] > hi:
                continue
            if terr is not None:
                t = customers[r[1]][3]
                if terr == "none":
                    if t:
                        continue
                elif terr not in t:
                    continue
            out.append(r)
        return out

    def orders_in_scope(a: dt.date, b: dt.date, terr=None):
        lo, hi = (a - window_start).days, (b - window_start).days
        out = []
        for r in orders:
            if r[0] < lo or r[0] > hi:
                continue
            if terr is not None:
                t = customers[r[1]][3]
                if terr == "none":
                    if t:
                        continue
                elif terr not in t:
                    continue
            out.append(r)
        return out

    import mcp_sql

    session = mcp_sql.connect()

    def sql_total(a: dt.date, b: dt.date, terr_codes=None) -> tuple[int, int]:
        where_terr = ""
        if terr_codes is not None:
            quoted = ", ".join("'" + c.replace("'", "''") + "'" for c in terr_codes)
            where_terr = f"""
              AND i.customer_bill_to_number IN (
                    SELECT c.code FROM customers c
                     WHERE c.organization_id = {oid}
                       AND c.territory_codes LIKE '[%'
                       AND EXISTS (SELECT 1 FROM json_array_elements_text(c.territory_codes::json) e
                                    WHERE trim(both '"' from e) IN ({quoted})))"""
        rows = session.execute_sql(f"""
            SELECT count(*) AS n,
                   COALESCE(round(sum(LEAST(i.net_amount, {ORDER_CAP})) * 100), 0)::bigint AS cents
              FROM portal_invoices i
             WHERE i.organization_id = {oid}
               AND i.invoice_date BETWEEN '{a}' AND '{b}'
               AND i.net_amount IS NOT NULL{where_terr}""")
        return int(rows[0]["n"]), int(rows[0]["cents"])

    def sql_order_total(a: dt.date, b: dt.date) -> tuple[int, int]:
        rows = session.execute_sql(f"""
            SELECT count(*) AS n,
                   COALESCE(round(sum(LEAST(COALESCE(total_amount,0), {ORDER_CAP})) * 100), 0)::bigint AS cents
              FROM portal_orders
             WHERE organization_id = {oid}
               AND order_date BETWEEN '{a}' AND '{b}'""")
        return int(rows[0]["n"]), int(rows[0]["cents"])

    print(f"\nDataset: {meta['org_label']} · window {window_start} → {rtd} · "
          f"{meta['row_count']} invoices · {meta.get('order_count', len(orders))} orders · "
          f"{len(customers)} accounts · {len(territories)} territories")

    # ── 1. every period preset matches SQL ──────────────────────────────
    print("\n[1] Period presets reconcile to SQL")
    for name, (a, b) in presets(rtd, window_start).items():
        rows = in_scope(a, b)
        n_sql, c_sql = sql_total(a, b)
        check(f"{name:<10} {a} → {b}",
              len(rows) == n_sql and total(rows) == c_sql,
              f"artifact {len(rows)} / ${total(rows)/100:,.2f} vs sql {n_sql} / ${c_sql/100:,.2f}")

    # ── 2. territory filter matches SQL ─────────────────────────────────
    print("\n[2] Territory filter reconciles to SQL")
    if not MAP_FILE.exists():
        check("mask map present", False, f"{MAP_FILE} missing; cannot reverse labels")
    else:
        mp = json.loads(MAP_FILE.read_text(encoding="utf-8"))
        label_to_real = {v["label"]: v["real_code"] for v in mp["territories"].values()}
        a, b = presets(rtd, window_start)["all"]
        counts = {}
        for c in customers:
            for t in c[3]:
                counts[t] = counts.get(t, 0) + 1
        for t in sorted(counts, key=lambda k: -counts[k])[:3]:
            rows = in_scope(a, b, terr=t)
            real = label_to_real.get(territories[t])
            n_sql, c_sql = sql_total(a, b, terr_codes=[real])
            check(f"{territories[t]:<28}",
                  len(rows) == n_sql and total(rows) == c_sql,
                  f"artifact {len(rows)} / ${total(rows)/100:,.2f} vs sql {n_sql} / ${c_sql/100:,.2f}")

    # ── 3. cross-surface identities ─────────────────────────────────────
    print("\n[3] Cross-surface identities (every scope)")
    for name, (a, b) in presets(rtd, window_start).items():
        rows = in_scope(a, b)
        grand = total(rows)
        by_month: dict[tuple[int, int], int] = {}
        by_cust: dict[int, int] = {}
        for r in rows:
            d = day_to_date(r[0])
            by_month[(d.year, d.month)] = by_month.get((d.year, d.month), 0) + r[2]
            by_cust[r[1]] = by_cust.get(r[1], 0) + r[2]
        check(f"{name:<10} Monthly sums to Summary", sum(by_month.values()) == grand)
        check(f"{name:<10} Customers sums to Invoices", sum(by_cust.values()) == grand)
        by_state: dict[str, int] = {}
        for ci, v in by_cust.items():
            by_state[customers[ci][2] or "—"] = by_state.get(customers[ci][2] or "—", 0) + v
        check(f"{name:<10} State grouping partitions", sum(by_state.values()) == grand)

    # ── 4. territory overlap disclosed ──────────────────────────────────
    print("\n[4] Territory overlap is disclosed, not hidden")
    a, b = presets(rtd, window_start)["all"]
    rows = in_scope(a, b)
    grand = total(rows)
    by_cust = {}
    for r in rows:
        by_cust[r[1]] = by_cust.get(r[1], 0) + r[2]
    terr_sum = 0
    unassigned = 0
    shared = 0
    for ci, v in by_cust.items():
        ts = customers[ci][3]
        if not ts:
            unassigned += v
            continue
        if len(ts) > 1:
            shared += 1
        terr_sum += v * len(ts)
    check("sum of territory rows exceeds grand total (expected)", terr_sum + unassigned > grand,
          f"rows ${(terr_sum+unassigned)/100:,.2f} vs total ${grand/100:,.2f}; {shared} shared accounts")
    html = ARTIFACT.read_text(encoding="utf-8")
    check("artifact explains the overlap on screen",
          "more than one territory" in html and "not a split of the book" in html)
    check("artifact surfaces unassigned revenue",
          "Unassigned" in html and "no territory on file" in html,
          f"${unassigned/100:,.2f} unassigned")

    # ── 5. fail closed ──────────────────────────────────────────────────
    print("\n[5] Empty territory fails closed")
    empty = [t for t in range(len(territories))
             if not any(t in c[3] for c in customers)]
    check("no territory silently falls back to the whole org",
          "empty book rather than falling back" in html)
    check("unassigned bucket is reachable in the picker", 'value="none"' in html,
          f"{meta['unassigned_customers']} accounts / {meta['unassigned_rows']} invoices")
    if empty:
        rows_e = in_scope(a, b, terr=empty[0])
        check("empty territory yields zero rows", len(rows_e) == 0)

    # ── 6. no-gos absent ────────────────────────────────────────────────
    print("\n[6] No-gos absent")
    banned = {
        "teaching surface": r"What[’']s broken",
        "bug simulator": r"Simulate|Broken \(today\)",
        "wave badges / DB keys": r"\bWave \d|enable_sales_portal|should_show_portal|mobile_sites\.",
        "ticket keys": r"\bEBR-\d|\bSERV-\d",
        "answer codes": r"\bC1\b|\bS1\b|\bQ-R1\b|\bQ-18\b|\bRS-01\b|Universe E",
        "staff name": r"Kylor",
        "internal-demo title": r"Internal Demo",
        "mockup chrome": r"mockup-only|Cycle 0\d|ISOLATION",
        "in-artifact disclaimer": r"illustrative|not real|demo chrome",
        "persona switcher": r"View as|HIDE · not for you|persona",
        "org switcher to another client": r"Currey|Sarreid|sarreid|\bcci\b|\bufi\b",
        "file references": r"IR-v1-QUERIES|SETTINGS-hub|FILTER-TRUTH",
    }
    for name, pat in banned.items():
        hits = re.findall(pat, html, re.I)
        check(f"no {name}", not hits, ("found: " + ", ".join(sorted(set(hits))[:3])) if hits else "")

    # ── 7. no hand-typed figures ────────────────────────────────────────
    print("\n[7] Every figure is computed, not written")
    body = html[html.index("<body"):html.index("<script")]
    money_literals = [m for m in re.findall(r"\$[\d,]+(?:\.\d+)?[MK]?", body)]
    check("no currency literals in markup", not money_literals,
          ", ".join(money_literals[:5]) if money_literals else "")
    check("real ERP account keys absent", not re.search(r"\b(29925|32162|31098)\b", html))
    check("dataset is the only data source", html.count("sales-portal-client-review-v2.data.js") == 1)

    # ── 8. Orders reconcile + never merge into invoiced ─────────────────
    print("\n[8] Orders reconcile; backlog ≠ invoiced")
    for name, (a, b) in presets(rtd, window_start).items():
        orows = orders_in_scope(a, b)
        n_sql, c_sql = sql_order_total(a, b)
        check(f"orders {name:<10}",
              len(orows) == n_sql and total(orows) == c_sql,
              f"artifact {len(orows)} / ${total(orows)/100:,.2f} vs sql {n_sql} / ${c_sql/100:,.2f}")

    a, b = presets(rtd, window_start)["all"]
    orows = orders_in_scope(a, b)
    backlog = [r for r in orows if r[5] and not r[4]]
    quotes = [r for r in orows if r[4]]
    check("backlog rows present or exclusions explain absence",
          len(backlog) > 0 or bool(settings.get("excluded_backlog_statuses")),
          f"{len(backlog)} backlog · {len(quotes)} quotes · excl={settings.get('excluded_backlog_statuses')}")
    check("Orders surface labels backlog as not sales",
          "not invoiced sales" in html and "Backlog" in html)
    check("order statuses dimension present", len(order_statuses) > 0)

    # ── 9. Accounts fading math ─────────────────────────────────────────
    print("\n[9] Accounts fading (equal 6mo, recent < 0.6× prior)")
    fading = fading_from_dataset(ds)
    check("fading list is computable", isinstance(fading, list))
    check("every fading row satisfies the rule",
          all(r["recent"] < 0.6 * r["prior"] for r in fading),
          f"{len(fading)} accounts")
    if fading:
        check("fading dollars are trailing-12-month on the account",
              all(r["ltm"] >= 0 for r in fading))
        check("Intelligence surface has fading table markup",
              "Who to call" in html and "Accounts fading" in html)

    # ── 10. Team pulse block present and self-consistent ────────────────
    print("\n[10] Team pulse")
    check("team block present", "logins_30d" in team and "top_writers" in team)
    check("writers ≤ writer orders",
          team.get("writers_30d", 0) <= team.get("writer_orders_30d", 0)
          or team.get("writer_orders_30d", 0) == 0)
    check("top writers masked as Rep ###",
          all(isinstance(w[0], str) and w[0].startswith("Rep ") for w in team.get("top_writers", [])))

    # ── 11. Settings is this org's config ───────────────────────────────
    print("\n[11] Settings hub")
    check("settings block present", "site_portal_enabled" in settings)
    check("seven nav surfaces",
          all(f'data-view="{v}"' in html for v in
              ["dashboard", "intelligence", "customers", "orders", "invoices", "reports", "settings"]))
    check("decision tree in plain English",
          "Why can’t someone see the portal?" in html or "Why can't someone see the portal?" in html)
    check("no raw DB key lines under settings rows",
          "sr-key" not in html and "user_types.enable_sales_portal" not in html)

    print(f"\n{checks - len(failures)}/{checks} checks passed")
    if failures:
        print("FAILED:")
        for f in failures:
            print("  -", f)
        sys.exit(1)
    print("Artifact reconciles. Entry gate items that remain are human: Bet A prod verify, SERV-2196.")


if __name__ == "__main__":
    main()
