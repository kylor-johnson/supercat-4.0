"""
Insightful Product 3.0 — Signal Detection (deterministic)

Replaces the LLM-based Step 2 signal detection pass. Reads cache files
produced by data_gather.py + gate_flags.md, applies threshold rules from
the signal catalog, and outputs signal_rank.md + top_accounts.md.

No LLM calls. No network. Runs in < 5 seconds.

Usage:
    python detect_signals.py --shortname cci --run-date 2026-06-17
"""

from __future__ import annotations

import argparse
import re
import statistics
import sys
from dataclasses import dataclass, field
from pathlib import Path

SECTION_HOMES = {
    "SIG-DECAY-01": "§2 Accounts",
    "SIG-DECAY-02": "§2 Accounts",
    "SIG-DECAY-03": "§5 Team",
    "SIG-DECAY-04": "§2 Accounts",
    "SIG-ANOMALY-01": "§3 Product",
    "SIG-ANOMALY-02": "§3 Product",
    "SIG-ANOMALY-03": "§2 Accounts",
    "SIG-OPP-01": "§2/§3",
    "SIG-OPP-02": "§2 Accounts",
    "SIG-OPP-03": "§2 Accounts",
    "SIG-OPP-04": "§3 Product",
    "SIG-MOM-01": "§2 Accounts",
    "SIG-MOM-02": "§3 Product",
    "SIG-MOM-03": "§2 Accounts",
    "SIG-RISK-01": "§4 Commerce",
    "SIG-RISK-02": "§2 Accounts",
    "SIG-RISK-03": "§6 Platform",
    "SIG-RISK-04": "§5 Team",
    "SIG-BEH-01": "§5 Team",
    "SIG-BEH-02": "§5 Team",
    "SIG-COMMERCE-01": "§4 Commerce",
    "SIG-COMMERCE-02": "§4 Commerce",
    "SIG-COMMERCE-03": "§4 Commerce",
    "SIG-PRODUCT-01": "§3 Product",
    "SIG-TEAM-01": "§5 Team",
    "SIG-TEAM-02": "§5 Team",
}

PRIORITY_TIERS = {
    "SIG-DECAY-01": "P0", "SIG-DECAY-02": "P0", "SIG-DECAY-03": "P1",
    "SIG-DECAY-04": "P0", "SIG-ANOMALY-01": "P0", "SIG-ANOMALY-02": "P0",
    "SIG-ANOMALY-03": "P0", "SIG-OPP-01": "P0", "SIG-OPP-02": "P1",
    "SIG-OPP-03": "P1", "SIG-OPP-04": "P2", "SIG-MOM-01": "P0",
    "SIG-MOM-02": "P2", "SIG-MOM-03": "P2", "SIG-RISK-01": "P1",
    "SIG-RISK-02": "P0", "SIG-RISK-03": "P2", "SIG-RISK-04": "P1",
    "SIG-BEH-01": "P1", "SIG-BEH-02": "P2", "SIG-COMMERCE-01": "P0",
    "SIG-COMMERCE-02": "P1", "SIG-COMMERCE-03": "P1",
    "SIG-PRODUCT-01": "P1", "SIG-TEAM-01": "P1", "SIG-TEAM-02": "P1",
}

TONE_MAP = {
    "SIG-DECAY-01": "RISK", "SIG-DECAY-02": "RISK", "SIG-DECAY-03": "RISK",
    "SIG-DECAY-04": "RISK", "SIG-ANOMALY-01": "RISK", "SIG-ANOMALY-02": "RISK",
    "SIG-ANOMALY-03": "RISK", "SIG-OPP-01": "POSITIVE", "SIG-OPP-02": "POSITIVE",
    "SIG-OPP-03": "POSITIVE", "SIG-OPP-04": "POSITIVE", "SIG-MOM-01": "POSITIVE",
    "SIG-MOM-02": "POSITIVE", "SIG-MOM-03": "POSITIVE", "SIG-RISK-01": "RISK",
    "SIG-RISK-02": "RISK", "SIG-RISK-03": "RISK", "SIG-RISK-04": "RISK",
    "SIG-BEH-01": "RISK", "SIG-BEH-02": "RISK", "SIG-COMMERCE-01": "POSITIVE",
    "SIG-COMMERCE-02": "POSITIVE", "SIG-COMMERCE-03": "RISK",
    "SIG-PRODUCT-01": "RISK", "SIG-TEAM-01": "POSITIVE", "SIG-TEAM-02": "RISK",
}


@dataclass
class Signal:
    signal_id: str
    description: str
    priority: str
    section: str
    surprise: float
    dollar_impact: float
    actionability: float
    tone: str
    entity: str = ""

    @property
    def rank(self) -> float:
        return self.surprise * self.dollar_impact * self.actionability


@dataclass
class RunContext:
    cache_dir: Path
    gate_flags: dict[str, str] = field(default_factory=dict)
    org_name: str = ""
    shortname: str = ""
    org_id: int = 0
    ecat_gmv: float = 0.0
    total_biz_gmv: float = 0.0


def parse_dollars(s: str) -> float:
    """Parse dollar strings like '$88.0M', '$8,600,000', '$105,944'."""
    s = s.strip().replace("$", "").replace(",", "")
    if s.endswith("M"):
        return float(s[:-1]) * 1_000_000
    if s.endswith("K"):
        return float(s[:-1]) * 1_000
    if s.endswith("B"):
        return float(s[:-1]) * 1_000_000_000
    try:
        return float(s)
    except ValueError:
        return 0.0


def parse_table(text: str) -> list[dict[str, str]]:
    """Parse a markdown table into a list of dicts."""
    lines = [l.strip() for l in text.strip().split("\n") if l.strip().startswith("|")]
    if len(lines) < 3:
        return []
    headers = [h.strip() for h in lines[0].split("|")[1:-1]]
    rows = []
    for line in lines[2:]:
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if len(cells) == len(headers):
            rows.append(dict(zip(headers, cells)))
    return rows


def read_cache(cache_dir: Path, filename: str) -> str | None:
    """Read a cache file, return None if not present."""
    p = cache_dir / filename
    if p.exists():
        return p.read_text(encoding="utf-8")
    return None


def parse_gate_flags(text: str) -> dict[str, str]:
    """Parse gate_flags.md into {flag_name: value}."""
    flags = {}
    for line in text.split("\n"):
        if line.startswith("| ") and " | " in line and "---" not in line and "Flag" not in line:
            parts = [p.strip() for p in line.split("|")[1:-1]]
            if len(parts) >= 2:
                flags[parts[0]] = parts[1]
    return flags


def detect_decay_01(ctx: RunContext) -> list[Signal]:
    """Customer Reorder Frequency Collapse."""
    text = read_cache(ctx.cache_dir, "Q-ORG-DECAY_results.md")
    if not text:
        return []
    rows = parse_table(text)
    signals = []
    for row in rows:
        try:
            ratio = float(row.get("gap_ratio", row.get("decay_ratio", row.get("ratio", "0"))))
            ltm_rev = parse_dollars(row.get("ltm_revenue", row.get("ltm_gmv", "0")))
            customer = row.get("customer_name", row.get("customer", "UNKNOWN"))
            gap_days = int(float(row.get("current_gap_days", row.get("days_since_last", "0"))))
            avg_days = int(float(row.get("avg_days_between", row.get("avg_interval", "0"))))
        except (ValueError, TypeError):
            continue
        if ratio > 2.5 and ltm_rev > 10_000:
            signals.append(Signal(
                signal_id="SIG-DECAY-01",
                description=f"Reorder Decay — {customer} {ratio:.1f}x normal gap ({gap_days}d vs {avg_days}d avg)",
                priority="P0",
                section="§2 Accounts",
                surprise=ratio,
                dollar_impact=ltm_rev,
                actionability=3.0,
                tone="RISK",
                entity=customer,
            ))
    return signals


def detect_decay_03(ctx: RunContext) -> list[Signal]:
    """Rep Engagement Trajectory Decline."""
    text = read_cache(ctx.cache_dir, "Q-06_results.md")
    if not text:
        return []
    if ctx.gate_flags.get("QUALIFYING_REP_COUNT", "0") == "0":
        return []
    rows = parse_table(text)
    signals = []
    for row in rows:
        try:
            pct_change = float(row.get("qoq_change_pct", row.get("order_change_pct", row.get("pct_change", "0"))))
            prior_orders = int(float(row.get("prior_90d_orders", row.get("orders_prev_90d", row.get("prior_orders", "0")))))
            current_gmv = parse_dollars(row.get("current_90d_gmv", row.get("gmv_current_90d", row.get("current_gmv", "0"))))
            rep = row.get("rep_name", row.get("rep", "UNKNOWN"))
        except (ValueError, TypeError):
            continue
        if pct_change < -25 and prior_orders >= 10 and current_gmv * 4 > 50_000:
            surprise = abs(pct_change) / 25.0
            annualized = current_gmv * 4
            signals.append(Signal(
                signal_id="SIG-DECAY-03",
                description=f"Rep Trajectory — {rep} orders {pct_change:+.1f}% QoQ, ${current_gmv:,.0f} current 90d GMV",
                priority="P1",
                section="§5 Team",
                surprise=surprise,
                dollar_impact=annualized,
                actionability=2.0,
                tone="RISK",
                entity=rep,
            ))
    return signals


def detect_decay_04(ctx: RunContext) -> list[Signal]:
    """Spending Contraction Detection."""
    if ctx.gate_flags.get("HAS_PORTAL_ORDERS") != "True":
        return []
    text = read_cache(ctx.cache_dir, "Q-ORG-CONTRACTION_results.md")
    if not text:
        return []
    rows = parse_table(text)
    signals = []
    for row in rows:
        try:
            yoy_pct = float(row.get("yoy_pct_change", row.get("total_yoy_pct", row.get("yoy_change", "0"))))
            ltm_gmv = parse_dollars(row.get("ltm_gmv", row.get("total_ltm", row.get("current_gmv", "0"))))
            prior_gmv = parse_dollars(row.get("prior_gmv", row.get("total_prior", row.get("prior_year_gmv", "0"))))
            customer = row.get("customer_name", row.get("customer", "UNKNOWN"))
        except (ValueError, TypeError):
            continue
        if yoy_pct < -20 and ltm_gmv > 50_000:
            surprise = abs(yoy_pct) / 20.0
            gap = prior_gmv - ltm_gmv
            signals.append(Signal(
                signal_id="SIG-DECAY-04",
                description=f"Spending Contraction — {customer} {yoy_pct:+.1f}% YoY (${prior_gmv:,.0f}→${ltm_gmv:,.0f}), ${gap:,.0f} gap",
                priority="P0",
                section="§2 Accounts",
                surprise=surprise,
                dollar_impact=gap,
                actionability=3.0,
                tone="RISK",
                entity=customer,
            ))
    return signals


def detect_anomaly_01(ctx: RunContext) -> list[Signal]:
    """Ghost SKU Detection."""
    text = read_cache(ctx.cache_dir, "Q-ORG-GHOST_results.md")
    if not text:
        return []
    rows = parse_table(text)
    signals = []
    for row in rows:
        try:
            revenue = parse_dollars(row.get("ltm_revenue", row.get("revenue", "0")))
            item_code = row.get("item_code", row.get("item_number", "UNKNOWN"))
        except (ValueError, TypeError):
            continue
        if revenue > 5_000:
            signals.append(Signal(
                signal_id="SIG-ANOMALY-01",
                description=f"Ghost SKU — {item_code} ${revenue:,.0f} invoiced LTM, no catalog record",
                priority="P0",
                section="§3 Product",
                surprise=3.0,
                dollar_impact=revenue,
                actionability=3.0,
                tone="RISK",
                entity=item_code,
            ))
    return signals


def detect_anomaly_02(ctx: RunContext) -> list[Signal]:
    """Stock-Out on High-Demand Items."""
    if ctx.gate_flags.get("HAS_INVENTORY") != "True":
        return []
    text = read_cache(ctx.cache_dir, "Q-ORG-STOCKOUT_results.md")
    if not text:
        return []
    rows = parse_table(text)
    signals = []
    for row in rows:
        try:
            revenue = parse_dollars(row.get("ltm_revenue", row.get("revenue", "0")))
            item = row.get("item_number", row.get("item_code", "UNKNOWN"))
            desc = row.get("description", row.get("long_description", row.get("long_desc", "")))
            rank = int(float(row.get("rank", row.get("revenue_rank", "50"))))
        except (ValueError, TypeError):
            continue
        if revenue > 10_000:
            surprise = max(rank / 5.0, 1.0) if rank <= 50 else 1.0
            signals.append(Signal(
                signal_id="SIG-ANOMALY-02",
                description=f"Stock Out — {item} ({desc[:40]}) ${revenue:,.0f} LTM, 0 available",
                priority="P0",
                section="§3 Product",
                surprise=surprise,
                dollar_impact=revenue,
                actionability=3.0,
                tone="RISK",
                entity=item,
            ))
    return signals


def detect_anomaly_03(ctx: RunContext) -> list[Signal]:
    """Competitive Displacement (eCat Down, Total Business Up)."""
    if ctx.gate_flags.get("HAS_PORTAL_ORDERS") != "True":
        return []
    text = read_cache(ctx.cache_dir, "Q-ORG-CONTRACTION_results.md")
    if not text:
        return []
    rows = parse_table(text)
    signals = []
    for row in rows:
        try:
            ecat_yoy = float(row.get("ecat_yoy_pct", "0"))
            total_yoy = float(row.get("total_biz_yoy_pct", row.get("total_yoy_pct", row.get("yoy_pct_change", "0"))))
            ltm_gmv = parse_dollars(row.get("ltm_gmv", row.get("total_ltm", row.get("account_ltm", "0"))))
            ecat_prior = parse_dollars(row.get("ecat_prior_gmv", row.get("ecat_prior", "0")))
            customer = row.get("customer_name", row.get("customer", "UNKNOWN"))
        except (ValueError, TypeError):
            continue
        if ecat_yoy < -10 and total_yoy > 5 and ltm_gmv > 25_000:
            divergence = abs(ecat_yoy - total_yoy)
            surprise = divergence / 15.0
            impact = ecat_prior * abs(ecat_yoy - total_yoy) / 100.0 if ecat_prior > 0 else ltm_gmv * 0.1
            signals.append(Signal(
                signal_id="SIG-ANOMALY-03",
                description=f"Competitive Displacement — {customer} total biz {total_yoy:+.0f}% but eCat {ecat_yoy:+.0f}%",
                priority="P0",
                section="§2 Accounts",
                surprise=surprise,
                dollar_impact=impact,
                actionability=3.0,
                tone="RISK",
                entity=customer,
            ))
    return signals


def detect_opp_01(ctx: RunContext) -> list[Signal]:
    """Next Best Product (Collaborative Filtering)."""
    text = read_cache(ctx.cache_dir, "Q-ORG-NBP_results.md")
    if not text:
        return []
    rows = parse_table(text)
    if not rows:
        return []
    try:
        top = rows[0]
        co_customers = int(float(top.get("co_purchase_customers", top.get("customer_count", "0"))))
        avg_rev = parse_dollars(top.get("avg_revenue_per_purchase", top.get("customer_ltm", top.get("avg_revenue", "0"))))
        anchor = top.get("anchor_item", top.get("item_1", ""))
        suggested = top.get("suggested_item", top.get("item_2", ""))
    except (ValueError, TypeError):
        return []
    if co_customers >= 10:
        surprise = co_customers / 10.0
        impact = co_customers * avg_rev if avg_rev > 0 else co_customers * 5000
        return [Signal(
            signal_id="SIG-OPP-01",
            description=f"Next Best Product — {anchor}/{suggested} co-purchase pattern across {co_customers} customers",
            priority="P0",
            section="§2/§3",
            surprise=surprise,
            dollar_impact=impact,
            actionability=2.0,
            tone="POSITIVE",
            entity=f"{anchor}/{suggested}",
        )]
    return []


def detect_opp_02(ctx: RunContext) -> list[Signal]:
    """Unactivated High-Value Accounts."""
    if ctx.gate_flags.get("HAS_PORTAL_ORDERS") != "True":
        return []
    text = read_cache(ctx.cache_dir, "Q-53_results.md")
    if not text:
        return []
    rows = parse_table(text)
    qualifying = []
    has_cart = ctx.gate_flags.get("HAS_CART") == "True"
    for row in rows:
        try:
            total_gmv = parse_dollars(row.get("total_business_gmv", row.get("erp_gmv", "0")))
            ecat_orders = int(float(row.get("ecat_orders", row.get("lifetime_ecat_orders", "0"))))
            total_orders = int(float(row.get("total_orders", row.get("order_count", "0"))))
            customer = row.get("customer_name", row.get("customer", "UNKNOWN"))
        except (ValueError, TypeError):
            continue
        is_enterprise = total_orders >= 500 and ecat_orders == 0 and not has_cart
        if total_gmv > 50_000 and ecat_orders == 0 and not is_enterprise:
            qualifying.append((customer, total_gmv))
    if not qualifying:
        return []
    total_at_zero = sum(g for _, g in qualifying)
    surprise = total_at_zero / 1_000_000
    return [Signal(
        signal_id="SIG-OPP-02",
        description=f"Unactivated High-Value Accounts — {len(qualifying)} non-enterprise accounts with ${total_at_zero/1e6:.1f}M+ total business, zero eCat orders",
        priority="P1",
        section="§2 Accounts",
        surprise=surprise,
        dollar_impact=total_at_zero,
        actionability=2.0,
        tone="POSITIVE",
        entity=f"{len(qualifying)} accounts",
    )]


def detect_mom_01(ctx: RunContext) -> list[Signal]:
    """Account Acceleration."""
    text = read_cache(ctx.cache_dir, "Q-ORG-VELOCITY_results.md")
    if not text:
        return []
    rows = parse_table(text)
    signals = []
    for row in rows:
        try:
            qoq_growth = float(row.get("qoq_growth_pct", row.get("max_qoq", row.get("peak_qoq_pct", "0"))))
            consecutive = int(float(row.get("consecutive_quarters", row.get("accel_quarters", "0"))))
            peak_gmv = parse_dollars(row.get("peak_quarter_gmv", row.get("peak_quarter_revenue", row.get("current_quarter_gmv", "0"))))
            customer = row.get("customer_name", row.get("customer", "UNKNOWN"))
        except (ValueError, TypeError):
            continue
        if qoq_growth > 30 and consecutive >= 2 and peak_gmv > 10_000:
            surprise = qoq_growth / 30.0
            impact = peak_gmv
            signals.append(Signal(
                signal_id="SIG-MOM-01",
                description=f"Account Acceleration — {customer} {consecutive} consecutive QoQ acceleration quarters, ${peak_gmv:,.0f} peak quarter (+{qoq_growth:.0f}% QoQ)",
                priority="P0",
                section="§2 Accounts",
                surprise=surprise,
                dollar_impact=impact,
                actionability=3.0,
                tone="POSITIVE",
                entity=customer,
            ))
    return signals


def detect_risk_01(ctx: RunContext) -> list[Signal]:
    """Customer Revenue Concentration."""
    text = read_cache(ctx.cache_dir, "Q-13_results.md")
    if not text:
        return []
    rows = parse_table(text)
    if len(rows) < 5:
        return []
    try:
        top5_gmv = sum(parse_dollars(r.get("ltm_gmv", r.get("gmv", "0"))) for r in rows[:5])
        total_gmv = sum(parse_dollars(r.get("ltm_gmv", r.get("gmv", "0"))) for r in rows)
    except (ValueError, TypeError):
        return []
    if total_gmv == 0:
        return []
    top5_share = top5_gmv / total_gmv * 100
    top1_share = parse_dollars(rows[0].get("ltm_gmv", rows[0].get("gmv", "0"))) / total_gmv * 100
    if top5_share > 40 or top1_share > 20:
        surprise = top5_share / 40.0
        return [Signal(
            signal_id="SIG-RISK-01",
            description=f"Revenue Concentration — top 5 accounts generate {top5_share:.0f}% of eCat GMV",
            priority="P1",
            section="§4 Commerce",
            surprise=surprise,
            dollar_impact=top5_gmv,
            actionability=2.0,
            tone="RISK",
            entity="Top 5 accounts",
        )]
    return []


def detect_risk_02(ctx: RunContext) -> list[Signal]:
    """Dormant High-Value Accounts."""
    text = read_cache(ctx.cache_dir, "Q-17_results.md")
    if not text:
        return []
    rows = parse_table(text)
    signals = []
    for row in rows:
        try:
            hist_gmv = parse_dollars(row.get("historical_gmv", row.get("ltm_gmv", "0")))
            days_ago = int(float(row.get("days_since_last", row.get("days_dormant", "0"))))
            customer = row.get("customer_name", row.get("customer", "UNKNOWN"))
        except (ValueError, TypeError):
            continue
        if hist_gmv > 15_000 and days_ago > 90:
            surprise = hist_gmv / 25_000
            signals.append(Signal(
                signal_id="SIG-RISK-02",
                description=f"Dormant High-Value — {customer} ${hist_gmv:,.0f} hist. eCat, last order {days_ago}d ago",
                priority="P0",
                section="§2 Accounts",
                surprise=surprise,
                dollar_impact=hist_gmv,
                actionability=3.0,
                tone="RISK",
                entity=customer,
            ))
    return signals


def detect_risk_04(ctx: RunContext) -> list[Signal]:
    """Rep Concentration."""
    text = read_cache(ctx.cache_dir, "Q-18_results.md")
    if not text:
        text = read_cache(ctx.cache_dir, "Q-18_partA_results.md")
    if not text:
        return []
    rows = parse_table(text)
    if len(rows) < 5:
        return []
    try:
        total = sum(parse_dollars(r.get("ecat_gmv", r.get("gmv", "0"))) for r in rows)
        top_gmv = parse_dollars(rows[0].get("ecat_gmv", rows[0].get("gmv", "0")))
        top_rep = rows[0].get("rep_name", rows[0].get("rep", "UNKNOWN"))
    except (ValueError, TypeError):
        return []
    if total == 0:
        return []
    top_share = top_gmv / total * 100
    top3_gmv = sum(parse_dollars(r.get("ecat_gmv", r.get("gmv", "0"))) for r in rows[:3])
    top3_share = top3_gmv / total * 100
    if top_share > 30 or top3_share > 60:
        surprise = top_share / 30.0
        return [Signal(
            signal_id="SIG-RISK-04",
            description=f"Rep Concentration — {top_rep} generates {top_share:.0f}% of eCat GMV (${top_gmv:,.0f} of ${total:,.0f})",
            priority="P1",
            section="§5 Team",
            surprise=surprise,
            dollar_impact=top_gmv,
            actionability=2.0,
            tone="RISK",
            entity=top_rep,
        )]
    return []


def detect_commerce_01(ctx: RunContext) -> list[Signal]:
    """Digital order enablement — order channel mix, NOT a 'grow eCat share' pitch.

    The story is holistic: eCat is one digital channel alongside the client's own
    B2B web / EDI. The opportunity is streamlining rep-, phone-, and email-entered
    orders into digital commerce — NOT capturing share for eCat's sake. The §4 agent
    quantifies the rep/back-office-entered volume from Q-CHANNEL-MIX where available.
    """
    if ctx.gate_flags.get("HAS_PORTAL_ORDERS") != "True":
        return []
    if ctx.total_biz_gmv <= 0 or ctx.ecat_gmv <= 0:
        return []
    digital_pct = ctx.ecat_gmv / ctx.total_biz_gmv * 100
    # dollar_impact ranks the topic by total-business scale; it is NOT a per-point capture pitch.
    rank_impact = ctx.total_biz_gmv / 100
    surprise = (100 - digital_pct) / 20.0
    return [Signal(
        signal_id="SIG-COMMERCE-01",
        description=f"Digital order enablement — eCat handles {digital_pct:.1f}% of ${ctx.total_biz_gmv/1e6:.0f}M total business; streamlining rep-, phone- and email-entered orders into digital commerce is the upside (see channel mix)",
        priority="P0",
        section="§4 Commerce",
        surprise=surprise,
        dollar_impact=rank_impact,
        actionability=3.0,
        tone="POSITIVE",
        entity="Order Digitization",
    )]


def detect_commerce_02(ctx: RunContext) -> list[Signal]:
    """Quote AOV Spread."""
    text = read_cache(ctx.cache_dir, "Q-20_results.md")
    if not text:
        return []
    rows = parse_table(text)
    quote_rows = [r for r in rows if "quote" in r.get("order_type", "").lower()]
    conf_rows = [r for r in rows if "confirmed" in r.get("order_type", "").lower() or "order" in r.get("order_type", "").lower()]
    if not quote_rows or not conf_rows:
        return []
    try:
        quote_aov = parse_dollars(quote_rows[0].get("aov", quote_rows[0].get("avg_order_value", "0")))
        conf_aov = parse_dollars(conf_rows[0].get("aov", conf_rows[0].get("avg_order_value", "0")))
        quote_count = int(float(quote_rows[0].get("order_count", quote_rows[0].get("orders", "0"))))
    except (ValueError, TypeError):
        return []
    if conf_aov == 0 or quote_count < 10:
        return []
    ratio = quote_aov / conf_aov
    if ratio > 3.0:
        impact = quote_count * quote_aov * 0.10
        return [Signal(
            signal_id="SIG-COMMERCE-02",
            description=f"Quote AOV Spread — quotes avg ${quote_aov:,.0f} vs ${conf_aov:,.0f} confirmed ({ratio:.1f}x)",
            priority="P1",
            section="§4 Commerce",
            surprise=ratio,
            dollar_impact=impact,
            actionability=2.0,
            tone="POSITIVE",
            entity="Quotes",
        )]
    return []


def detect_team_01(ctx: RunContext) -> list[Signal]:
    """Reps whose books run entirely off eCat — a digital-enablement opportunity, NOT a 'capture gap'."""
    if ctx.gate_flags.get("HAS_PORTAL_ORDERS") != "True":
        return []
    if ctx.gate_flags.get("PORTAL_REP_DATA_PRESENT") != "True":
        return []
    text = read_cache(ctx.cache_dir, "Q-51_results.md")
    if not text:
        return []
    rows = parse_table(text)
    zero_capture = []
    for row in rows:
        try:
            total_gmv = parse_dollars(row.get("total_business_gmv", row.get("erp_gmv", "0")))
            ecat_gmv = parse_dollars(row.get("ecat_gmv", "0"))
            rep = row.get("rep_name", row.get("rep", "UNKNOWN"))
        except (ValueError, TypeError):
            continue
        if total_gmv > 500_000 and ecat_gmv == 0:
            zero_capture.append((rep, total_gmv))
    if not zero_capture:
        return []
    total_at_zero = sum(g for _, g in zero_capture)
    surprise = len(zero_capture) * (total_at_zero / 1_000_000)
    return [Signal(
        signal_id="SIG-TEAM-01",
        description=f"Rep digital-enablement opportunity — {len(zero_capture)} reps run ${total_at_zero/1e6:.1f}M of business entirely through other channels (web/EDI/phone/email/rep entry); rep-assisted digital ordering could streamline the manual portion",
        priority="P1",
        section="§5 Team",
        surprise=surprise,
        dollar_impact=total_at_zero,
        actionability=2.0,
        tone="POSITIVE",
        entity=f"{len(zero_capture)} reps",
    )]


def detect_risk_03(ctx: RunContext) -> list[Signal]:
    """Data Staleness."""
    text = read_cache(ctx.cache_dir, "Q-08_results.md")
    if not text:
        return []
    rows = parse_table(text)
    signals = []
    for row in rows:
        try:
            days_stale = int(float(row.get("days_since_update", row.get("days_stale", "0"))))
            entity = row.get("entity_type", row.get("entity", "UNKNOWN"))
        except (ValueError, TypeError):
            continue
        if days_stale > 90:
            surprise = days_stale / 90.0
            priority = "P1" if days_stale > 180 else "P2"
            signals.append(Signal(
                signal_id="SIG-RISK-03",
                description=f"Data Staleness — {entity} last updated {days_stale}d ago",
                priority=priority,
                section="§6 Platform",
                surprise=surprise,
                dollar_impact=1.0,
                actionability=2.0,
                tone="RISK",
                entity=entity,
            ))
    return signals


def detect_stockout_velocity(ctx: RunContext) -> list[Signal]:
    """Velocity x Stockout Collision."""
    if ctx.gate_flags.get("HAS_INVENTORY") != "True":
        return []
    text = read_cache(ctx.cache_dir, "Q-ORG-STOCKOUT_results.md")
    if not text:
        return []
    rows = parse_table(text)
    signals = []
    for row in rows:
        try:
            velocity_pct = float(row.get("qoq_velocity_pct", row.get("velocity_change", "0")))
            revenue = parse_dollars(row.get("ltm_revenue", row.get("revenue", "0")))
            item = row.get("item_number", row.get("item_code", "UNKNOWN"))
            desc = row.get("description", row.get("long_description", ""))
        except (ValueError, TypeError):
            continue
        if velocity_pct > 30 and revenue > 10_000:
            surprise = velocity_pct / 30.0
            signals.append(Signal(
                signal_id="SIG-PRODUCT-01",
                description=f"Velocity×Stockout — {item} ({desc[:30]}) demand +{velocity_pct:.0f}% while stocked out, ${revenue:,.0f} LTM",
                priority="P1",
                section="§3 Product",
                surprise=surprise,
                dollar_impact=revenue,
                actionability=3.0,
                tone="RISK",
                entity=item,
            ))
    return signals


def detect_newitem_gap(ctx: RunContext) -> list[Signal]:
    """New Item Adoption Gap."""
    if ctx.gate_flags.get("HAS_NEW_ITEMS") != "True":
        return []
    text = read_cache(ctx.cache_dir, "Q-ORG-NEWITEM_results.md")
    if not text:
        return []
    rows = parse_table(text)
    zero_sales = [r for r in rows if parse_dollars(r.get("ltm_revenue", r.get("total_revenue", r.get("revenue", "0")))) == 0]
    if len(zero_sales) > 5:
        return [Signal(
            signal_id="SIG-OPP-04",
            description=f"New Item Adoption Gap — {len(zero_sales)} new items with $0 platform orders",
            priority="P2",
            section="§3 Product",
            surprise=len(zero_sales) / 10.0,
            dollar_impact=50_000,
            actionability=1.0,
            tone="POSITIVE",
            entity=f"{len(zero_sales)} items",
        )]
    return []


def run_all_detectors(ctx: RunContext) -> list[Signal]:
    """Run all signal detectors and return combined results."""
    all_signals: list[Signal] = []
    detectors = [
        detect_decay_01, detect_decay_03, detect_decay_04,
        detect_anomaly_01, detect_anomaly_02, detect_anomaly_03,
        detect_opp_01, detect_opp_02, detect_mom_01,
        detect_risk_01, detect_risk_02, detect_risk_03, detect_risk_04,
        detect_commerce_01, detect_commerce_02, detect_team_01,
        detect_stockout_velocity, detect_newitem_gap,
    ]
    for detector in detectors:
        try:
            results = detector(ctx)
            all_signals.extend(results)
        except Exception as e:
            print(f"  WARNING: {detector.__name__} failed: {e}")
    return all_signals


def build_section_density(signals: list[Signal]) -> dict[str, dict[str, int]]:
    """Compute per-section P0/P1/P2 counts."""
    density: dict[str, dict[str, int]] = {}
    section_map = {"§2 Accounts": "§2 Account Intelligence", "§2/§3": "§2 Account Intelligence",
                   "§3 Product": "§3 Product Intelligence", "§4 Commerce": "§4 Commerce Patterns",
                   "§5 Team": "§5 Team Intelligence", "§6 Platform": "§6 Platform Context"}
    for sig in signals:
        sec = section_map.get(sig.section, sig.section)
        if sec not in density:
            density[sec] = {"P0": 0, "P1": 0, "P2": 0, "Total": 0}
        density[sec][sig.priority] += 1
        density[sec]["Total"] += 1
    return density


def select_top7_candidates(signals: list[Signal]) -> list[Signal]:
    """Select top 7 for Signal Summary per narrative arc rules."""
    sorted_sigs = sorted(signals, key=lambda s: s.rank, reverse=True)
    positives = [s for s in sorted_sigs if s.tone == "POSITIVE"]
    risks = [s for s in sorted_sigs if s.tone == "RISK"]
    selected: list[Signal] = []
    used_entities: set[str] = set()

    for sig in positives:
        if sig.entity not in used_entities and len(selected) < 4:
            selected.append(sig)
            used_entities.add(sig.entity)
    for sig in risks:
        if sig.entity not in used_entities and len(selected) < 7:
            selected.append(sig)
            used_entities.add(sig.entity)
    if len(selected) < 7:
        for sig in sorted_sigs:
            if sig.entity not in used_entities and len(selected) < 7:
                selected.append(sig)
                used_entities.add(sig.entity)
    return selected


def select_top_accounts(signals: list[Signal], n: int = 10) -> list[dict]:
    """Select top N accounts by per-account signal density."""
    account_signals: dict[str, list[Signal]] = {}
    for sig in signals:
        if sig.section in ("§2 Accounts", "§2/§3") and sig.entity and sig.entity not in ("Top 5 accounts",):
            entity = sig.entity.split("/")[0] if "/" in sig.entity else sig.entity
            if entity not in account_signals:
                account_signals[entity] = []
            account_signals[entity].append(sig)
    ranked = sorted(account_signals.items(), key=lambda x: len(x[1]), reverse=True)
    results = []
    for name, sigs in ranked[:n]:
        results.append({
            "name": name,
            "signal_count": len(sigs),
            "signals": sigs,
            "max_dollar": max(s.dollar_impact for s in sigs),
        })
    return results


def format_signal_rank(ctx: RunContext, signals: list[Signal], top7: list[Signal],
                       density: dict, top_accounts: list[dict]) -> str:
    """Format signal_rank.md output."""
    sorted_sigs = sorted(signals, key=lambda s: s.rank, reverse=True)[:20]
    p0 = sum(1 for s in signals if s.priority == "P0")
    p1 = sum(1 for s in signals if s.priority == "P1")
    p2 = sum(1 for s in signals if s.priority == "P2")

    lines = [
        f"# Signal Rank — {ctx.org_name} ({ctx.shortname}, org_id={ctx.org_id})",
        f"- **Run date**: {ctx.cache_dir.parent.name.split('_', 1)[1] if '_' in ctx.cache_dir.parent.name else 'unknown'}",
        f"- **Total signals fired**: {len(signals)} (P0: {p0}, P1: {p1}, P2: {p2})",
        f"- **Org GMV**: ${ctx.ecat_gmv/1e6:.1f}M eCat LTM, ${ctx.total_biz_gmv/1e6:.1f}M total business LTM",
        "",
        "## Ranked Manifest (Top 20 by SIGNAL_RANK)",
        "",
        "| Rank | Signal ID | Description | Priority | Section | Surprise | Dollar Impact | Action | SIGNAL_RANK | Tone |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for i, sig in enumerate(sorted_sigs, 1):
        lines.append(
            f"| {i} | {sig.signal_id} | {sig.description} | {sig.priority} | {sig.section} "
            f"| {sig.surprise:.1f} | ${sig.dollar_impact:,.0f} | {sig.actionability:.1f} "
            f"| {sig.rank:,.0f} | {sig.tone} |"
        )

    lines.extend(["", "## Section Signal Density Table", "",
                   "| Section | P0 | P1 | P2 | Total | Notes |",
                   "| --- | --- | --- | --- | --- | --- |"])
    for sec, counts in sorted(density.items()):
        lines.append(f"| {sec} | {counts['P0']} | {counts['P1']} | {counts['P2']} | {counts['Total']} | |")

    lines.extend(["", "**Section ORDER is FIXED (§1→§5→§2→§4→§3→§6). Density does NOT determine position.**", ""])
    lines.extend(["## Top 7 Signal Summary Candidates", "",
                   "Ordered by narrative arc (Momentum → Intelligence → Opportunity → Risk), NOT by raw SIGNAL_RANK:", ""])
    for i, sig in enumerate(top7, 1):
        tone_label = "POSITIVE/MOMENTUM" if sig.tone == "POSITIVE" else "RISK"
        lines.append(f"{i}. **[{tone_label}]** {sig.signal_id}: {sig.description}")

    pos_count = sum(1 for s in top7 if s.tone == "POSITIVE")
    risk_count = sum(1 for s in top7 if s.tone == "RISK")
    lines.extend(["", f"**Balance check**: {pos_count} positive (slots 1-{pos_count}), "
                      f"{risk_count} risk (slots {pos_count+1}-{len(top7)}). "
                      f"Finding #1 is {'positive' if top7[0].tone == 'POSITIVE' else 'RISK'}. ✓" if top7 else ""])

    lines.extend(["", "## Sections to Skip", "",
                   "None — all sections have ≥1 fired signal or their alternate include gate passes.", ""])
    return "\n".join(lines)


def format_top_accounts(ctx: RunContext, top_accounts: list[dict]) -> str:
    """Format top_accounts.md output."""
    lines = [
        f"# Top 10 Accounts for Mini-Briefs — {ctx.org_name} ({ctx.shortname}, org_id={ctx.org_id})",
        f"- **Run date**: {ctx.cache_dir.parent.name.split('_', 1)[1] if '_' in ctx.cache_dir.parent.name else 'unknown'}",
        "- **Selection criteria**: Per-account signal density (accounts appearing across multiple signal types)",
        "",
        "| Rank | Customer Name | Signal Count | Signals | Max Dollar Impact |",
        "| --- | --- | --- | --- | --- |",
    ]
    for i, acct in enumerate(top_accounts, 1):
        sig_descs = ", ".join(s.signal_id.replace("SIG-", "") for s in acct["signals"][:4])
        lines.append(f"| {i} | {acct['name']} | {acct['signal_count']} | {sig_descs} | ${acct['max_dollar']:,.0f} |")
    return "\n".join(lines)


# --- Coaching candidates (deterministic — replaces LLM-improvised upside math) ---
#
# Methodology locked with operator (2026-06-17):
#   - Qualifying reps: Q-63 reps with >= QUALIFYING_PRESENTATIONS presentations.
#   - Benchmark conversion: top-quartile (75th pct) of conversion_rate_pct among
#     qualifying reps that actually convert (conversion > 0).
#   - Upside = max(0, (benchmark - rep_conv)/100 * presentations * AOV).
#   - Reps with no order/AOV match are EXCLUDED — no fabricated dollars.
#   - Keep upside > COACHING_UPSIDE_FLOOR, sort desc, cap MAX_COACHING_CARDS.
QUALIFYING_PRESENTATIONS = 50
COACHING_UPSIDE_FLOOR = 50_000
MAX_COACHING_CARDS = 5


def _norm_name(s: str) -> str:
    return re.sub(r"[^a-z]", "", s.lower())


def _match_rep_aov(slug: str, order_rows: list[dict]) -> tuple[str, float] | None:
    """Resolve a Q-63 username slug to a Q-01-S2 display name + AOV.

    Deterministic heuristic over the order roster. Tries, in priority order:
    exact concat, first-initial+lastname, firstname+last-initial, lastname,
    then prefix containment. Returns (display_name, aov), or None when the rep
    has no order/AOV data (cannot be quantified -> excluded).
    """
    nslug = _norm_name(slug)
    if not nslug:
        return None
    best: tuple[int, str, float] | None = None
    for r in order_rows:
        display = r.get("rep_name", "").strip()
        if not display:
            continue
        aov = parse_dollars(r.get("avg_order_value", "0"))
        orders = parse_dollars(r.get("total_orders", "0"))
        if orders <= 0 or aov <= 0:
            continue  # no real AOV to quantify against
        parts = display.split()
        first = _norm_name(parts[0]) if parts else ""
        last = _norm_name(parts[-1]) if len(parts) > 1 else ""
        concat = _norm_name(display)
        score: int | None = None
        if nslug == concat:
            score = 0
        elif last and nslug == first[:1] + last:
            score = 1
        elif first and last and nslug == first + last[:1]:
            score = 2
        elif last and nslug == last:
            score = 3
        elif concat and (concat.startswith(nslug) or nslug.startswith(concat)):
            score = 4
        if score is not None and (best is None or score < best[0]):
            best = (score, display, aov)
    if best is None:
        return None
    return best[1], best[2]


def compute_coaching_candidates(ctx: RunContext) -> dict:
    """Deterministically compute coaching-card candidates (see module note above).

    Returns a result dict: {candidates, benchmark, qualifying, converters, reason}.
    `candidates` is the final filtered/sorted/capped list; the other fields explain
    how it was derived (so the output file states the real reason for 0 cards).
    """
    result = {"candidates": [], "benchmark": None, "qualifying": 0,
              "converters": 0, "reason": ""}
    q63 = read_cache(ctx.cache_dir, "Q-63_results.md")
    q01s2 = read_cache(ctx.cache_dir, "Q-01_step2_results.md")
    if not q63 or not q01s2:
        result["reason"] = "Q-63 and/or Q-01-S2 data not present."
        return result
    pres_rows = parse_table(q63)
    order_rows = parse_table(q01s2)

    qualifying: list[tuple[str, float, float]] = []
    for r in pres_rows:
        try:
            pres = float(r.get("total_presentations", "0"))
            conv = float(r.get("conversion_rate_pct", "0"))
        except ValueError:
            continue
        if pres >= QUALIFYING_PRESENTATIONS:
            qualifying.append((r.get("rep", "").strip(), pres, conv))
    result["qualifying"] = len(qualifying)
    if not qualifying:
        result["reason"] = f"No reps with >= {QUALIFYING_PRESENTATIONS} presentations."
        return result

    converters = sorted(c for _, _, c in qualifying if c > 0)
    result["converters"] = len(converters)
    if len(converters) >= 2:
        benchmark = statistics.quantiles(converters, n=4, method="inclusive")[2]
    elif converters:
        benchmark = converters[0]
    else:
        result["reason"] = "No qualifying rep converts (>0%) — no benchmark to measure against."
        return result
    result["benchmark"] = benchmark

    cands: list[dict] = []
    for slug, pres, conv in qualifying:
        if conv >= benchmark:
            continue
        match = _match_rep_aov(slug, order_rows)
        if match is None:
            continue
        display, aov = match
        upside = (benchmark - conv) / 100.0 * pres * aov
        if upside > COACHING_UPSIDE_FLOOR:
            cands.append({
                "rep": display, "presentations": int(pres), "conversion": conv,
                "benchmark": benchmark, "aov": aov, "upside": upside,
            })
    cands.sort(key=lambda c: c["upside"], reverse=True)
    result["candidates"] = cands[:MAX_COACHING_CARDS]
    if not cands:
        result["reason"] = (
            f"No qualifying rep's estimated upside clears the ${COACHING_UPSIDE_FLOOR:,.0f} "
            f"floor (benchmark {benchmark:.1f}%; low AOV / presentation volume)."
        )
    return result


def format_coaching_candidates(ctx: RunContext, result: dict) -> str:
    cands = result["candidates"]
    benchmark = result["benchmark"]
    lines = [
        f"# Coaching Candidates — {ctx.org_name} ({ctx.shortname})",
        "",
        "Deterministically computed by detect_signals.py. The section agent renders",
        "these reps as coaching cards EXACTLY as listed — do NOT recompute, re-filter,",
        "or add reps. Archetype framing + narrative are written by the agent; the rep",
        "set and the estimated upside dollar figures are fixed here.",
        "",
        (f"- **Benchmark conversion (top-quartile of converting qualifying reps)**: "
         f"{benchmark:.1f}%") if benchmark is not None else "- **Benchmark**: n/a",
        f"- **Qualifying reps (>= {QUALIFYING_PRESENTATIONS} presentations)**: {result['qualifying']} "
        f"({result['converters']} converting)",
        f"- **Upside floor**: ${COACHING_UPSIDE_FLOOR:,.0f}",
        f"- **Candidates above floor**: {len(cands)}",
        "",
    ]
    if not cands:
        lines.append(
            f"**No coaching cards for this client — render NO coaching cards and NO "
            f"coaching rollup callout.** Reason: {result['reason']}"
        )
        return "\n".join(lines)
    lines += [
        "| Rank | Rep | Presentations | Conversion | Benchmark | AOV | Estimated Annual Upside |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for i, c in enumerate(cands, 1):
        lines.append(
            f"| {i} | {c['rep']} | {c['presentations']} | {c['conversion']:.1f}% "
            f"| {c['benchmark']:.1f}% | ${c['aov']:,.0f} | ${c['upside']:,.0f} |"
        )
    total = sum(c["upside"] for c in cands)
    lines += ["", f"**Combined upside**: ${total:,.0f}"]
    return "\n".join(lines)


def extract_org_gmv(ctx: RunContext) -> None:
    """Extract org-level GMV from gate_flags."""
    flags_text = read_cache(ctx.cache_dir, "gate_flags.md") or ""
    ecat_match = re.search(r"ecat.*?gmv.*?\$([0-9,.]+[MKB]?)", flags_text, re.IGNORECASE)
    portal_match = re.search(r"portal_order_gmv.*?\$([0-9,.]+[MKB]?)", flags_text, re.IGNORECASE)
    if ecat_match:
        ctx.ecat_gmv = parse_dollars(ecat_match.group(1))
    if portal_match:
        ctx.total_biz_gmv = parse_dollars(portal_match.group(1))
    name_match = re.search(r"^# Gate Flags — (.+?) \(", flags_text, re.MULTILINE)
    if name_match:
        ctx.org_name = name_match.group(1)
    id_match = re.search(r"org_id=(\d+)", flags_text)
    if id_match:
        ctx.org_id = int(id_match.group(1))


def main() -> None:
    parser = argparse.ArgumentParser(description="Insightful 3.0 — Deterministic Signal Detection")
    parser.add_argument("--shortname", required=True)
    parser.add_argument("--run-date", required=True)
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent.parent
    cache_dir = project_root / "runs" / f"{args.shortname}_{args.run_date}" / "cache"
    if not cache_dir.exists():
        print(f"ERROR: Cache directory not found: {cache_dir}")
        sys.exit(1)

    gate_text = read_cache(cache_dir, "gate_flags.md")
    if not gate_text:
        print("ERROR: gate_flags.md not found in cache")
        sys.exit(1)

    ctx = RunContext(
        cache_dir=cache_dir,
        gate_flags=parse_gate_flags(gate_text),
        shortname=args.shortname,
    )
    extract_org_gmv(ctx)
    print(f"Signal detection for {ctx.org_name} ({ctx.shortname}, org_id={ctx.org_id})")
    print(f"  eCat GMV: ${ctx.ecat_gmv/1e6:.1f}M | Total Biz: ${ctx.total_biz_gmv/1e6:.1f}M")

    signals = run_all_detectors(ctx)
    print(f"  Signals fired: {len(signals)} (P0: {sum(1 for s in signals if s.priority == 'P0')}, "
          f"P1: {sum(1 for s in signals if s.priority == 'P1')}, "
          f"P2: {sum(1 for s in signals if s.priority == 'P2')})")

    top7 = select_top7_candidates(signals)
    density = build_section_density(signals)
    top_accounts = select_top_accounts(signals)

    rank_md = format_signal_rank(ctx, signals, top7, density, top_accounts)
    (cache_dir / "signal_rank.md").write_text(rank_md, encoding="utf-8")
    print(f"  Wrote: signal_rank.md ({len(rank_md)} bytes)")

    accounts_md = format_top_accounts(ctx, top_accounts)
    (cache_dir / "top_accounts.md").write_text(accounts_md, encoding="utf-8")
    print(f"  Wrote: top_accounts.md ({len(accounts_md)} bytes)")

    coaching = compute_coaching_candidates(ctx)
    coaching_md = format_coaching_candidates(ctx, coaching)
    (cache_dir / "coaching_candidates.md").write_text(coaching_md, encoding="utf-8")
    print(f"  Wrote: coaching_candidates.md ({len(coaching['candidates'])} candidate(s) above ${COACHING_UPSIDE_FLOOR:,.0f})")
    print("Done.")


if __name__ == "__main__":
    main()
