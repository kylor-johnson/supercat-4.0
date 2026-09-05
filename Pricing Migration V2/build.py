#!/usr/bin/env python3
"""
SuperCat Pricing Migration V2 — Draft Builder
==============================================
Reads master CSVs, fills HTML templates, outputs one HTML file per account.

June cohort (55 accounts):
  - Core (13):     drafts/core/{ord_id}__{slug}__notice.html
                   drafts/core/{ord_id}__{slug}__value-summary.html
  - Narrative (15): drafts/narrative/{ord_id}__{slug}__notice.html
                    drafts/narrative/{ord_id}__{slug}__value-summary.html
  - Entity (27):   drafts/entity/{entity-slug}__entity-packet.html

Usage:
  python3 build.py              # build all June cohort drafts
  python3 build.py --ord lpf    # build one account by ord_id
  python3 build.py --segment Core  # build one segment
"""

import csv, io, json, os, re, sys, argparse
from collections import Counter
from datetime import datetime
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE         = Path(__file__).parent
DATA         = BASE / "data"
TEMPLATES    = BASE / "templates"
DRAFTS       = BASE / "drafts"
ACCOUNT_CSV  = DATA / "_master-account-data-v6.3.csv"
ENTITY_CSV   = DATA / "_master-entity-data-v6.3.csv"

TODAY_STR = datetime.now().strftime("%B %d, %Y")

# ── Postgres metrics cache ─────────────────────────────────────────────────────
# Loaded from data/postgres_metrics.json (queried 2026-05-27 via Postgres MCP).
# Source tables: public.login_events (90-day window) + public.orders (LTM, is_submitted=true).
# organizations.shortname == ord_id links records to accounts.
# To refresh: re-run the two queries in the MCP against login_events and orders, update the JSON.
_METRICS_PATH = DATA / "postgres_metrics.json"
POSTGRES_METRICS: dict[str, dict] = {}
if _METRICS_PATH.exists():
    try:
        raw = json.loads(_METRICS_PATH.read_text(encoding="utf-8"))
        POSTGRES_METRICS = {k: v for k, v in raw.items() if not k.startswith("_")}
    except Exception:
        pass  # JSON load failure is non-fatal; stat rows will be omitted

# ── Angie override table ──────────────────────────────────────────────────────
# Source: angies_notes field in the CSV, used as the decision-maker when it
# conflicts with the modeled data. Only confident field-level corrections are
# applied here. Remaining questions are flagged in the build output for Slack
# review (see SLACK_FLAGS below and the printed block at end of main()).
#
# DO NOT add numeric overrides (mrr, delta, user counts) without confirmed
# billing data from Angie — bad numbers in the brief are worse than no brief.

ANGIE_OVERRIDES: dict[str, dict] = {
    # jcusa: Angie says "only discounted rate is the additional users."
    # The platform base ($795) is NOT discounted vs book — only the per-user rate was.
    # platform_discount_correction incorrectly implies a base-level deal; corrected to
    # tier_base_increase (old module price → new tier base) with user_rate_normalization secondary.
    # Numbers ($795 current, $1,295 new, $500 delta) unchanged — still flagged for Slack.
    "jcusa": {
        "migration_driver":   "tier_base_increase",
        "secondary_drivers":  "user_rate_normalization",
    },
    # bp: Angie says "only have contracted Ecat at $725 and $25 per additional user."
    # Stack corrected from iPad+Catalog+Cart → iPad.
    # current_mrr ($1,765) still reflects old Cart-included pricing — cannot safely
    # override without confirmed current invoice amount. Flagged for Slack.
    "bp": {
        "current_stack": "iPad",
    },
    # abol: Angie says cart is cancelled, eCat-only now.
    # CSV already shows current_stack='iPad' — stack is correct.
    # current_mrr ($725) may reflect combined-module pricing before cancellation.
    # No safe numeric override without confirmed billing. Flagged for Slack.
    "abol": {},
}

# ── Slack flag messages (printed at build end for operator copy-paste) ─────────
# Generated from Angie's notes — questions only an operator can answer.

SLACK_FLAGS = [
    {
        "account": "Jonathan Charles Designs Inc. (jcusa)",
        "what_changed": "Driver corrected: `platform_discount_correction` → `tier_base_increase` + `user_rate_normalization` secondary.",
        "questions": [
            "Is $795/month the correct non-discounted book rate for iPad+CPQ at signing? (Model showed it as 14% below $920 legacy book — Angie says base is NOT discounted.)",
            "CPQ is a T3 feature in the new tier structure — should jcusa be on T2 ($1,295) or T3 ($2,295)? Brief currently shows T2.",
        ],
    },
    {
        "account": "Buster & Punch (bp)",
        "what_changed": "Stack corrected: `iPad+Catalog+Cart` → `iPad`. Current MRR ($1,765) and tier (T2) NOT yet corrected — need confirmed billing.",
        "questions": [
            "What is the actual current monthly invoice after cart cancellation? (Model has $1,765 based on full stack; eCat-only at $725 + $25/user would be a different number.)",
            "With eCat-only, should the tier be T1 ($749 base) instead of T2 ($1,295)? If T1, the delta and driver both change.",
            "How many active users are currently enabled in their SuperCat environment? (Trailing avg = 37; new T1 includes 10.)",
        ],
    },
    {
        "account": "America's Backyards (abol)",
        "what_changed": "No numeric override applied — stack already shows iPad in CSV.",
        "questions": [
            "What is the actual current monthly invoice (iPad/eCat only)? Model shows $725 — is that the post-cancellation rate or the old combined price?",
            "If their true current rate is below $725, the $24 increase flips and they may belong in the Tailwind (good-news) cohort instead of Core.",
        ],
    },
]

# Strategic accounts (health override — Watch/At Risk/Critical or VD < 40)
STRATEGIC_OVERRIDE_ORDS = {"hvl", "sccon"}  # HVLG + known Watch/At-Risk high-delta accounts

# CEO-delivered entities (from _root/04 §4.15.1)
CEO_ENTITY_NAMES = {"Gabriella White", "Jonathan Charles", "Rock House Farm", "Thesis"}

# June cohort notice deadline: 60-day legal notice for Oct 1 effective date
JUNE_NOTICE_DEADLINE = "August 1, 2026"
JULY_NOTICE_DEADLINE = "September 1, 2026"


# ── Tier lookup tables ─────────────────────────────────────────────────────────
# Source: _root/03_what_we_sell.md §1–2

TIER_NAMES = {
    "T1": "Catalog Essentials",
    "T2": "Commerce Professional",
    "T3": "Commerce Enterprise",
}

TIER_PRICES = {
    "T1": {"base": 749,  "included_users": 10, "floor": 749,  "ceiling": 1629},
    "T2": {"base": 1295, "included_users": 15, "floor": 1295, "ceiling": 1589},
    "T3": {"base": 2295, "included_users": 40, "floor": 2295, "ceiling": 2875},
}

TIER_SUBTITLES = {
    "T1": "The rep iPad app, your buyer-facing catalog, and standard support.",
    "T2": "Everything in Catalog Essentials, plus online ordering for your accounts and a dedicated CSM.",
    "T3": "The full platform — rep app, buyer catalog, online ordering, sales intelligence, CPQ, credit card processing, and priority support.",
}

TIER_FEATURES_HTML = {
    "T1": """<ul class="feature-list">
  <li>Rep iPad app — full catalog, offline-capable, field order writing</li>
  <li>Buyer-facing product catalog</li>
  <li>10 users included</li>
  <li>Standard support</li>
</ul>""",
    "T2": """<ul class="feature-list">
  <li>Everything in Catalog Essentials</li>
  <li>Buyer-facing online ordering (self-serve cart)</li>
  <li>Order and invoice tracking for buyers</li>
  <li>15 users included (up to 3 brands)</li>
  <li>Dedicated CSM</li>
</ul>""",
    "T3": """<ul class="feature-list">
  <li>Everything in Commerce Professional</li>
  <li>Sales intelligence dashboard</li>
  <li>CPQ (configure-price-quote)</li>
  <li>Credit card processing</li>
  <li>Priority support</li>
  <li>40 users included (up to 5 brands)</li>
  <li>Dedicated CSM</li>
</ul>""",
}


# ── Driver explanation prose (simplified summary form-cut) ─────────────────────
# Source: _root/05_driver_taxonomy.md §2–3 — condensed for value summary companion.
# Rule: plain English, no percentages, no apology, no hedging.

DRIVER_EXPLANATIONS = {
    "user_rate_normalization": (
        "Your per-user rate was locked at signing and hasn't been updated to the current "
        "standard. Going forward, every account we work with moves to the same graduated "
        "user-rate structure: $25/user for the first 10 excess users, $22 for the next 15, "
        "$20 for the next 25, and $18 beyond that."
    ),
    "platform_discount_correction": (
        "Your current pricing reflects a discount applied at signing. Legacy account-level "
        "discounts are being retired across every account we work with — everyone moves to "
        "the same standard tier pricing. Your new rate is the standard for your tier and "
        "usage profile."
    ),
    "tier_base_increase": (
        "When your account was set up, the platform was priced at the book rate at that "
        "time. The current standard rate for this tier is higher — your invoice is moving "
        "to the current standard. Your tier isn't changing, only the rate."
    ),
    "included_user_reduction": (
        "Your account was set up with an expanded included-user allotment that was part of "
        "your original arrangement. The included base is moving to the current tier "
        "standard, with additional users billed at the graduated rate."
    ),
    "at_book_tier_shift": (
        "Your account has been at the book rate for its tier. Your invoice is moving to the "
        "current standard for this tier — your tier is not changing, only the rate."
    ),
    "multi_org_retirement": (
        "Your account has been part of SuperCat's multi-organization pricing program — a "
        "structure that applied cross-entity benefits. That program is being retired. "
        "Every account we work with moves to individual standard tier pricing."
    ),
    "annual_discount_retirement": (
        "Your account has been billed at an annual commitment rate — a discount applied at "
        "signing for annual prepayment. Annual-commitment discounts are being retired across "
        "every account we work with. Annual prepay remains available if you prefer that "
        "billing structure."
    ),
    "special_arrangement": (
        "Your current pricing reflects a custom arrangement set outside SuperCat's standard "
        "structure. In 2026, every account we work with is moving to one clear pricing "
        "structure. The new rate is the standard for your tier and user count."
    ),
    "module_compression": (
        "The separate module charges that make up your current invoice are consolidating "
        "into a single platform tier subscription — at a lower combined rate."
    ),
    "user_count_variance": (
        "Your current invoice is based on a billed-user count above your trailing average. "
        "User counts across every account we work with are being aligned to trailing-average "
        "actuals."
    ),
    "rate_architecture": (
        "Your per-user rate was set under the structure in place at signing. In 2026, "
        "every account we work with moves to the same graduated structure — for your "
        "account, the recalculated rate produces a lower invoice."
    ),
}


# ── Notice-body driver prose (short form — 1–2 sentences) ────────────────────
# Source: _root/05_driver_taxonomy.md §2–3 + _root/04_communication_posture.md §4.2
# These appear in the "Why Your Pricing Is Changing" section of the notice.
# The full explanations live in the value summary (DRIVER_EXPLANATIONS above).

DRIVER_NOTICE_PROSE = {
    "user_rate_normalization": (
        "Your per-user rate was locked at signing and hasn't been updated to the current "
        "platform standard. Every account we work with is moving to the same graduated "
        "user-rate structure, and your invoice now reflects that rate."
    ),
    "platform_discount_correction": (
        "Your rate reflects a discount applied at signing that's being retired as part of "
        "this change. Legacy account-level discounts are being retired across every account "
        "we work with simultaneously — you are not being singled out. "
        "Your new rate is the standard for your tier and usage profile."
    ),
    "tier_base_increase": (
        "Your platform base is moving to the current standard for your tier. "
        "The tier itself isn't changing — only the rate, which now reflects "
        "the current book price for the capabilities you use."
    ),
    "included_user_reduction": (
        "Your current arrangement included an expanded user allotment set at signing. "
        "The included base is moving to the current tier standard, with additional users "
        "billed at the graduated rate — the breakdown above reflects your current user count."
    ),
    "at_book_tier_shift": (
        "Your platform base is moving to the current standard for this tier. "
        "Your tier is not changing — only the rate, which now reflects the current book price."
    ),
    "multi_org_retirement": (
        "Your account has been part of SuperCat's multi-organization pricing program. "
        "That program is being retired — every account we work with moves to individual "
        "standard tier pricing."
    ),
    "annual_discount_retirement": (
        "Your account has been billed at an annual-commitment discount. "
        "Annual commitment discounts are being retired across every account we work with. "
        "Annual prepay remains available — same rate, one invoice per year."
    ),
    "special_arrangement": (
        "Your current pricing reflects a custom arrangement set outside SuperCat's standard "
        "structure. In 2026, every account we work with moves to one clear pricing structure. "
        "Your new rate is the standard for your tier and user count."
    ),
    "module_compression": (
        "The separate module charges that make up your current invoice are consolidating "
        "into a single platform tier subscription — at a lower combined rate."
    ),
    "user_count_variance": (
        "Your current invoice is based on a billed-user count above your trailing average. "
        "User counts across every account we work with are being aligned to trailing-average "
        "actuals — your invoice now reflects what your team actually uses."
    ),
    "rate_architecture": (
        "Your per-user rate was set under the structure in place at signing. "
        "Every account we work with is moving to the same graduated structure in 2026 — "
        "for your account, the recalculated rate produces a lower invoice."
    ),
}


# ── Notice content generators (called by fill_notice) ─────────────────────────
# Each returns an HTML string (may be empty string for accounts where it doesn't apply).
# Source docs: _root/04_communication_posture.md, _root/03.6_platform_narrative.md

def _is_watch_band(health_band: str) -> bool:
    return health_band.lower().replace(" ", "_") in ("watch", "at_risk", "critical")

def generate_account_lede(account: dict) -> str:
    """
    Relationship-before-price for healthy accounts; dollar-first for Watch/At Risk/Critical.
    Source: _root/04 §4.1, §4.13 + _root/03.6 §5.3
    """
    health_band  = account.get("health_band", "")
    company      = account.get("company", "")
    cohort_year  = account.get("cohort_year", "").strip()
    curr_mrr     = fmt_money(account.get("current_mrr", ""))
    new_mrr      = fmt_money(account.get("new_total_mrr", ""))
    deadline     = account.get("notice_deadline", "TBD")

    try:
        delta_f   = float(account.get("delta_mrr", "0"))
        delta_pct = float(account.get("delta_pct", "0"))
    except (ValueError, TypeError):
        delta_f, delta_pct = 0.0, 0.0

    if _is_watch_band(health_band):
        # §4.13: Dollar-first. Format: "a change of $[DELTA]/month ([DELTA_PCT]%)"
        # No company possessive to avoid double-s (America's Backyards's).
        pct_str = f"{delta_pct:.1f}%".rstrip("0").rstrip(".")
        if delta_f > 0:
            change_phrase = f"a change of <strong>${delta_f:,.0f}/month ({pct_str})</strong>"
        elif delta_f < 0:
            change_phrase = f"a reduction of <strong>${abs(delta_f):,.0f}/month ({pct_str})</strong>"
        else:
            change_phrase = "no change to the monthly total"
        return (
            f"Effective <strong>{deadline}</strong>, the monthly invoice for "
            f"{company} is moving from <strong>${curr_mrr}</strong> to "
            f"<strong>${new_mrr}</strong> — {change_phrase}."
        )

    # Healthy / Thriving — relationship first, then dollar change
    # §4.4: include annual figure when delta_pct > 30%
    if delta_f > 0 and delta_pct > 30:
        annual = delta_f * 12
        delta_phrase = f"a ${delta_f:,.0f}/month increase (${annual:,.0f}/year)"
    else:
        delta_phrase = delta_framing(account.get("delta_mrr", ""))

    try:
        years = 2026 - int(cohort_year)
        tenure = f"{years} year{'s' if years != 1 else ''} on SuperCat"
    except (ValueError, TypeError):
        tenure = "on SuperCat"

    # Use trailing_avg_users (current monthly active) — active_users is a lifetime cumulative count
    trailing = account.get("trailing_avg_users", "").strip()
    if trailing and trailing not in ("0", "—", ""):
        stat = f"{trailing} monthly active users on the platform"
    else:
        stat = "your team actively using the platform"

    return (
        f"{tenure}, and {company} has {stat}. "
        f"Your monthly invoice is moving from <strong>${curr_mrr}</strong> to "
        f"<strong>${new_mrr}</strong> effective <strong>{deadline}</strong> — {delta_phrase}."
    )


def generate_platform_narrative(account: dict) -> str:
    """
    Variant A: standardized architecture framing.
    Source: _root/03.6 §2.3 Variant A
    """
    cohort_year = account.get("cohort_year", "your sign-up year")
    return (
        f"SuperCat is moving all accounts to standardized platform tiers — three plans "
        f"based on the capabilities you use, with a transparent, graduated user rate. "
        f"Your current terms reflect a legacy arrangement from {cohort_year} that we're "
        f"retiring across every account simultaneously. "
        f"What you get on the platform doesn't change: your catalog, your rep access, "
        f"your integrations, and your order workflows all stay exactly as they are."
    )


def generate_health_band_append(account: dict, cs_first_name: str) -> str:
    """
    Appends health-band context paragraph after the platform narrative.
    Source: _root/03.6 §2.2
    Returns HTML paragraph string, or empty string for Thriving/Healthy (no append needed).
    """
    health_band = account.get("health_band", "")

    if _is_watch_band(health_band):
        return (
            f'<p style="font-size:14px;color:#8888a0">'
            f"We also want to make sure you're getting full value from the platform. "
            f"{cs_first_name} will follow up separately to walk through how your team is "
            f"using SuperCat and whether there are opportunities we should address together."
            f"</p>"
        )

    return ""  # Thriving / Healthy — no append in the notice


def generate_early_adopter_para(account: dict) -> str:
    """
    Extra tenure acknowledgment paragraph for long-tenured accounts.
    Fires for cohort_year ≤ 2015.
    Source: _root/04 §4.7
    """
    cohort_year_str = account.get("cohort_year", "").strip()
    try:
        cohort_year = int(cohort_year_str)
    except (ValueError, TypeError):
        return ""

    if cohort_year > 2015:
        return ""

    return (
        f'<p style="font-size:14px;color:#8888a0">'
        f"A change of this size warrants a real explanation. The platform you're running "
        f"today is a fundamentally different product than it was in {cohort_year}: your reps, "
        f"your buyers, and your team are all working from the same catalog, the same customer "
        f"file, and the same order infrastructure. That's worth naming when a relationship "
        f"this long is moving to a new price."
        f"</p>"
    )


def generate_driver_notice(account: dict) -> str:
    """
    Short (1–2 sentence) driver explanation for the notice body.
    Source: _root/05_driver_taxonomy.md + DRIVER_NOTICE_PROSE table above.
    """
    driver = account.get("migration_driver", "")
    return DRIVER_NOTICE_PROSE.get(
        driver,
        "Your pricing is moving to the current standard for your tier and user count. "
        "The breakdown above reflects the full calculation."
    )


def generate_platform_base_grown(account: dict) -> str:
    """
    Fires when the tier base is higher than the current platform MRR — i.e., the base itself grew.
    Only fires for accounts with ≥ 3 years tenure (cohort ≤ 2023) — the framing rings hollow
    for very recent accounts where 'considerable growth since [YEAR]' covers only 1–2 years.
    Source: _root/04 §4.6 — sentence is VERBATIM, copy character-for-character.
    """
    try:
        tier_base   = float(account.get("tier_base", "0"))
        curr_plat   = float(account.get("current_platform_mrr", "0"))
        cohort_year = int(account.get("cohort_year", "9999"))
    except (ValueError, TypeError):
        return ""

    if tier_base <= curr_plat:
        return ""

    if cohort_year > 2023:
        return ""

    # §4.6 verbatim: "what the platform is today" — not "what SuperCat is today"
    return (
        f'<p style="font-size:14px;color:#8888a0">'
        f"The platform has grown considerably since {cohort_year} — more surfaces, "
        f"more capability, the infrastructure behind it. The rate now reflects what "
        f"the platform is today."
        f"</p>"
    )


def generate_billing_footnote(account: dict) -> str:
    """
    Footnote clarifying user-billing basis for URN and IUR accounts.
    Source: _root/04 §4.9
    """
    driver     = account.get("migration_driver", "")
    secondary  = account.get("secondary_drivers", "")
    drivers    = {driver} | {s.strip() for s in secondary.split(",") if s.strip()}

    user_drivers = {"user_rate_normalization", "included_user_reduction"}
    if not drivers & user_drivers:
        return ""

    # §4.9 verbatim, must be italicized
    return (
        '<p class="billing-footnote">'
        "<em>User billing is based on enabled accounts in your SuperCat environment — "
        "the user figures above reflect your current enabled count.</em>"
        "</p>"
    )


def generate_operations_unchanged(account: dict) -> str:
    """
    "What Doesn't Change" body text. IUR gets a variant that acknowledges the user-base change.
    Source: _root/04 §4.5
    """
    driver = account.get("migration_driver", "")
    if driver == "included_user_reduction":
        return (
            "Your workflow, your team's access, your catalog, and your integrations are unchanged. "
            "The included user base and the invoice are both changing — the breakdown above "
            "explains exactly how the new total is calculated."
        )
    return (
        "Your workflow, your team's access, your catalog, and your integrations are unchanged. "
        "The only thing changing is the invoice."
    )


def generate_companion_reference(segment: str) -> str:
    """
    Pointer to the attached value summary. Core gets a simplified version; Narrative gets full context.
    """
    if segment == "Narrative":
        return (
            '<p>A detailed account summary is attached — it covers your platform usage data, '
            'health profile, and the full context for this pricing change.</p>'
        )
    # Core (simplified)
    return (
        '<p>A simplified account summary is attached with your usage data and platform health profile.</p>'
    )


def generate_support_fire_notice(account: dict) -> str:
    """
    Internal operator flag. Visible in draft; must be stripped before sending.
    Source: _root/03.6 §5.4
    """
    sf = account.get("support_fire", "").strip().upper()
    if sf not in ("TRUE", "YES", "1"):
        return ""

    days = account.get("support_fire_days_open", "").strip() or "unknown number of"
    return (
        f'<div class="support-fire-notice">'
        f"<strong>⚠ OPERATOR FLAG — DO NOT SEND:</strong> "
        f"This account has an open support issue ({days} days open). "
        f"Per <em>_root/03.6 §5.4</em>, do not deliver this notice until the support issue "
        f"is fully resolved. Kylor must close the ticket before sending."
        f"</div>"
    )


def generate_platform_base_disclosure(account: dict) -> str:
    """
    §4.10: When URN is primary driver AND platform base also increases, include explicit
    disclosure. Without it, the brief presents a per-user rate change while silently moving
    the base — the reader catches the table discrepancy and loses trust.
    """
    driver   = account.get("migration_driver", "")
    if driver != "user_rate_normalization":
        return ""

    try:
        tier_base = float(account.get("tier_base", "0"))
        curr_plat = float(account.get("current_platform_mrr", "0"))
    except (ValueError, TypeError):
        return ""

    if tier_base <= curr_plat:
        return ""

    tier      = account.get("assigned_tier", "T1")
    tier_name = TIER_NAMES.get(tier, "your tier")
    # §4.10 Format B verbatim form
    return (
        f'<p style="font-size:14px;color:#8888a0">'
        f"Your platform base is also moving from ${fmt_money(str(curr_plat))} to "
        f"${fmt_money(str(tier_base))} — this is the current {tier_name} standard."
        f"</p>"
    )


def generate_close_section(account: dict, segment: str) -> str:
    """
    §4.12: Canonical close for Format A (Core) and Format B (Narrative).
    Replaces the generic 'Your Options' boilerplate.
    Format A — 'What Happens Next' (CS-led, passive offer)
    Format B — 'Let's Talk' (CS-led, meeting offer)
    Followed by companion reference and formal-notice line.
    """
    company    = account.get("company", "")
    deadline   = account.get("notice_deadline", "TBD")
    excess     = _safe_float(account.get("excess_users", "0"))

    # Companion reference
    if segment == "Narrative":
        companion = (
            "<p class=\"companion-ref\">A detailed account summary is attached — it covers "
            f"{company}'s platform usage data, health profile, and the full context "
            "for this pricing change.</p>"
        )
        # Format B close — verbatim per §4.12
        close_text = (
            "<p class=\"close-text\">I'll reach out in the next few days to walk through "
            "this together. If you want to get ahead of that — or if you have questions "
            "before then — reply directly and we'll find time.</p>"
        )
    else:
        # Core — Format A
        companion = (
            "<p class=\"companion-ref\">A simplified account summary is attached with "
            "your usage data and platform health profile.</p>"
        )
        # Format A close — verbatim per §4.12
        close_text = (
            f"<p class=\"close-text\">Your Customer Success contact will be in touch "
            f"directly before {deadline}. If you'd like to talk through the rate or "
            "anything about this before then — that conversation is welcome. Reach out "
            "now. There's no process here — just a direct conversation with someone who "
            "knows your account.</p>"
        )

    # User deactivation tip — only when there are excess users billed
    deact_tip = ""
    if excess > 0:
        deact_tip = (
            f"<p class=\"user-deact-tip\">One practical note: reviewing your active user "
            f"list before {deadline} — and deactivating any unused accounts — will reduce "
            "your user charges on the first invoice at the new rate.</p>"
        )

    # §4.12 formal-notice line — verbatim, italicized
    formal = (
        f"<p class=\"formal-notice-line\"><em>This document also serves as formal written "
        f"notice of a pricing modification under your SuperCat licensing agreement, "
        f"effective {deadline}.</em></p>"
    )

    return (
        f'<div class="close-section">'
        f"{companion}"
        f"{deact_tip}"
        f"{close_text}"
        f"{formal}"
        f"</div>"
    )


def generate_bundle_flag(account: dict) -> str:
    """
    Operator flag for accounts where bundle_config_mismatch is TRUE.
    These accounts have known data accuracy issues (per angies_notes) and should not
    be sent until the mismatch is resolved.

    ── TASK 5 AUDIT (2026-05-27) — bundle_config_mismatch findings ──────────────

    jcusa — Jonathan Charles Designs Inc.
      Finding: OPERATOR CSV CORRECTION REQUIRED before draft can send.
      angies_notes: "This is reading the pricing incorrectly, only discounted rate
        is the additional users."
      Analysis: current_mrr=$795 with migration_driver=platform_discount_correction
        implies the base itself was discounted. Angie says only the per-user rate was
        discounted — the $795 was the standard book rate for eCat+CPQ at signing. The
        correct driver is likely user_rate_normalization or annual_discount_retirement
        (account is Annual). The current_platform_mrr and current_user_mrr split may
        also be wrong. This cannot be corrected in code without knowing the accurate
        base/user breakdown from billing. Operator must update the CSV fields:
        migration_driver, current_platform_mrr, current_user_mrr, and re-model
        new_total_mrr before this draft can be sent.

    bp — Buster & Punch
      Finding: OPERATOR CSV CORRECTION REQUIRED before draft can send.
      angies_notes: "This is incorrect, Buster and Punch only have contracted Ecat at
        this is billed at $725 and $25 per additional user."
      Analysis: current_stack='iPad+Catalog+Cart' implies portal/cart is still active,
        but Angie says the cart has been cancelled. If the account is T1-only (eCat iPad
        at $725 + user overage), current_mrr, current_stack, and assigned_tier all need
        updating. The delta ($44) and new_total_mrr ($1,809) would change substantially
        once the correct base is applied. Operator must confirm the current billing state,
        correct current_stack and current_mrr in the CSV, and re-model the new pricing.

    abol — America's Backyards
      Finding: OPERATOR CSV CORRECTION REQUIRED before draft can send.
      angies_notes: "This is incorrect, they have cancelled their cart and now are only
        billed for Ecat, this is calculating their Ecat price for both modules."
      Analysis: current_stack='iPad' is correct (already shows iPad-only), but current_mrr
        =$725 is the old combined-module price. The $749 new_total_mrr produces a $24
        delta, but if the correct current baseline is a lower iPad-only rate, this account
        may actually belong in the Tailwind (good-news/decrease) cohort rather than Core.
        Operator must confirm the active billing modules and correct current_mrr in the CSV.
        This is not a code-fixable issue — the correct current_mrr is unknown without
        reviewing the billing system.

    ─────────────────────────────────────────────────────────────────────────────
    """
    bm = account.get("bundle_config_mismatch", "").strip().upper()
    if bm not in ("TRUE", "YES", "1"):
        return ""

    notes = account.get("angies_notes", "").strip()
    notes_display = f" Note: <em>{notes[:200]}{'…' if len(notes) > 200 else ''}</em>" if notes else ""
    return (
        '<div class="support-fire-notice">'
        "<strong>⚠ OPERATOR FLAG — PRICING DATA ACCURACY:</strong> "
        "This account has a bundle configuration mismatch. Verify pricing data "
        f"before sending.{notes_display}"
        "</div>"
    )


def generate_signoff(account: dict) -> str:
    """
    Dynamic sign-off based on delivery_owner.
    CEO-delivered accounts get the CEO name; all others get Kylor.
    """
    owner = account.get("delivery_owner", "Kylor").strip().lower()
    if owner == "ceo":
        return "Best regards,<br>SuperCat Leadership"
    return "Best regards,<br>Kylor Johnson<br>Head of Customer Success, SuperCat"


# ── Score → CSS class / label helpers ─────────────────────────────────────────

def health_badge_class(health_band: str) -> str:
    b = (health_band or "").lower().replace(" ", "-")
    mapping = {
        "thriving":  "badge-thriving",
        "healthy":   "badge-healthy",
        "watch":     "badge-watch",
        "at-risk":   "badge-at-risk",
        "at_risk":   "badge-at-risk",
        "critical":  "badge-critical",
    }
    return mapping.get(b, "badge-unscored")

def score_css_class(score_str: str) -> str:
    try:
        s = float(score_str)
        if s >= 70: return "score-positive"
        if s >= 40: return "score-neutral"
        return "score-negative"
    except (ValueError, TypeError):
        return "score-neutral"

def score_label(score_str: str) -> str:
    try:
        s = float(score_str)
        if s >= 80: return "Strong"
        if s >= 60: return "Good"
        if s >= 40: return "Fair"
        return "Low"
    except (ValueError, TypeError):
        return "—"

def score_display(score_str: str) -> str:
    try:
        return f"{float(score_str):.0f}%"
    except (ValueError, TypeError):
        return "—"

def row_class(score_str: str) -> str:
    try:
        s = float(score_str)
        if s >= 70: return "row-positive"
        if s >= 40: return "row-neutral"
        return "row-negative"
    except (ValueError, TypeError):
        return "row-neutral"


# ── Evidence text generators ───────────────────────────────────────────────────
# composite_narrative from v6.2 is already written health prose — use it.
# For sub-dimension evidence, generate from scores when narrative isn't specific.

def engagement_evidence(account: dict) -> str:
    narrative = account.get("composite_narrative", "").strip()
    if narrative:
        # First sentence of composite narrative is usually the health summary
        first = narrative.split(".")[0].strip()
        if len(first) > 15:
            return first + "."
    active = account.get("active_users", "")
    trailing = account.get("trailing_avg_users", "")
    if active and trailing:
        return f"{active} active users, averaging {trailing} per month."
    return "User engagement data on file."

def adoption_evidence(account: dict) -> str:
    """
    Account-specific feature usage sentence.
    Uses current_stack (what modules they have) + trailing_avg_users (current team size).
    Never exposes the raw adoption_score number — score_label maps it to plain English.
    """
    stack   = clean_stack(account.get("current_stack", "")).strip()
    trailing = account.get("trailing_avg_users", "").strip()
    if stack and trailing and trailing not in ("0", "—", ""):
        return f"Using {stack} across {trailing} active reps."
    if stack:
        return f"Active on {stack}."
    label = score_label(account.get("adoption_score", ""))
    return f"Feature usage is {label.lower()}."

def value_delivery_evidence(account: dict, ord_id: str = "") -> str:
    """
    Business results evidence — uses live eCat order count from Postgres when available.
    §4.2: label as 'eCat orders submitted through SuperCat', never total ERP-side volume.
    Falls back to cleaned composite_narrative extract, then score label.
    """
    metrics = POSTGRES_METRICS.get(ord_id, {})
    orders  = metrics.get("ecat_orders_ltm")
    if orders is not None and orders > 0:
        return f"{orders:,} eCat orders submitted through SuperCat in the last 12 months."
    # Narrative fallback: first sentence of cleaned composite_narrative if substantive
    narrative = clean_narrative(clean_stack(account.get("composite_narrative", "")))
    if narrative:
        sentences = [s.strip() for s in narrative.split(".") if s.strip()]
        for s in sentences:
            # Skip user-count sentences (already shown in Team Activity row)
            if "users" not in s.lower() and len(s) > 20:
                return s.rstrip(".") + "."
    label = score_label(account.get("value_delivery_score", ""))
    return f"Business results are {label.lower()} — orders, quotes, and portal activity on file."

def operational_health_evidence(account: dict) -> str:
    """
    System health evidence — plain-language label only; raw score never shown (§2.5).
    """
    label = score_label(account.get("operational_health_score", ""))
    return f"Data integrations and catalog configuration are {label.lower()}."


# ── Account position within tier range ────────────────────────────────────────

def account_position_pct(new_mrr_str: str, tier: str) -> int:
    try:
        mrr   = float(new_mrr_str)
        t     = TIER_PRICES.get(tier, TIER_PRICES["T1"])
        floor = t["floor"]
        ceil  = t["ceiling"]
        pct   = int(100 * (mrr - floor) / max(ceil - floor, 1))
        return max(2, min(97, pct))
    except (ValueError, TypeError):
        return 50


# ── Next steps copy ────────────────────────────────────────────────────────────

def next_steps_copy(segment: str, health_band: str) -> str:
    band = (health_band or "").lower()
    is_watch = band in ("watch", "at risk", "at_risk", "critical")
    if is_watch:
        return (
            "If you have questions about how this was calculated or what your options are "
            "before the effective date, reach out directly. We&#39;re available."
        )
    return (
        "Your Customer Success contact will be in touch before the effective date. "
        "If you&#39;d like to talk through the rate or anything about this before then — "
        "reply directly and we&#39;ll find time."
    )

def callout_class(health_band: str) -> str:
    band = (health_band or "").lower()
    if band in ("watch", "at risk", "at_risk", "critical"):
        return "callout-neutral"
    return "callout-positive"


# ── Formatting helpers ─────────────────────────────────────────────────────────

def fmt_money(val_str: str) -> str:
    """Format a numeric string as comma-separated integer (no $ sign)."""
    try:
        f = float(val_str)
        if f == int(f):
            return f"{int(f):,}"
        return f"{f:,.2f}"
    except (ValueError, TypeError):
        return val_str or "—"

def tenure_years(cohort_year_str: str) -> str:
    try:
        return str(2026 - int(cohort_year_str))
    except (ValueError, TypeError):
        return "—"

def delta_framing(delta_str: str) -> str:
    try:
        d = float(delta_str)
        if d > 0:  return f"a ${d:,.0f}/month increase"
        if d < 0:  return f"a ${abs(d):,.0f}/month decrease"
        return "no change to your monthly total"
    except (ValueError, TypeError):
        return "a pricing change"

def engagement_stat(account: dict) -> str:
    active   = account.get("active_users", "").strip()
    trailing = account.get("trailing_avg_users", "").strip()
    if active and trailing and active != "0":
        return f"{active} active users, averaging {trailing} per month"
    elif active and active != "0":
        return f"{active} active users on the platform"
    return "your team actively using the platform"

def clean_stack(s: str) -> str:
    """Fix UTF-8 encoding artifacts from Mac CSV export."""
    return (s or "").replace("\u00e2\u20ac\u201c", "—").replace("‚Äî", "—").strip()

def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


# ── CSV loading ────────────────────────────────────────────────────────────────

def _load_csv(path: Path) -> list[dict]:
    """Load a CSV that has a leading blank/comma row followed by the real header."""
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()
    # Line 0: blank commas (offset row). Line 1: header with leading comma.
    data = "".join(lines[1:])
    data = "\n".join(line.lstrip(",") for line in data.split("\n"))
    reader = csv.DictReader(io.StringIO(data))
    return [{k: (v or "").strip() for k, v in row.items()} for row in reader]

def assign_segment(account: dict) -> str:
    """
    Derive migration_segment from v6.3 fields.
    Priority order (matches build_execution_html.py logic):
      Annual → Strategic overrides → Tailwind → Entity → Core/Narrative/Executive/Pre-Engagement
    """
    deal_type   = account.get("deal_type", "").strip()
    delta       = _safe_float(account.get("delta_mrr", "0"))
    health_band = account.get("health_band", "").lower()
    vd_score    = _safe_float(account.get("value_delivery_score", "100"))
    ord_id      = account.get("ord_id", "").strip()
    parent      = account.get("parent_entity", "").strip()
    company     = account.get("company", "").strip()
    is_watch    = health_band in ("watch", "at risk", "at_risk", "critical")

    if deal_type == "Annual":
        return "Annual"
    # Strategic: HVLG + Watch/At Risk/Critical with delta > $400 or VD < 40
    if is_watch and (delta > 400 or vd_score < 40):
        return "Strategic"
    if ord_id in STRATEGIC_OVERRIDE_ORDS:
        return "Strategic"
    if delta <= 0:
        return "Tailwind"
    # Entity: has a distinct parent_entity (multi-brand child)
    if parent and parent != company and parent.strip():
        return "Entity"
    if delta <= 200:
        return "Core"
    if delta <= 400:
        return "Narrative"
    if delta <= 600:
        return "Executive"
    return "Pre-Engagement"

def assign_cohort(segment: str) -> str:
    if segment in ("Core", "Narrative", "Entity"):
        return "June"
    if segment in ("Executive", "Pre-Engagement"):
        return "July"
    return "Deferred"

def assign_notice_deadline(segment: str, account: dict) -> str:
    cohort = assign_cohort(segment)
    if cohort == "June":
        return JUNE_NOTICE_DEADLINE
    if cohort == "July":
        return JULY_NOTICE_DEADLINE
    if segment == "Annual":
        # Renewal-based — pull from account notes if available
        return account.get("notice_deadline", "At renewal (≥90 days prior)")
    return "TBD"

def assign_artifact_type(segment: str) -> str:
    mapping = {
        "Core":           "Simplified value summary",
        "Narrative":      "Simplified value summary",
        "Entity":         "Entity packet",
        "Executive":      "CEO co-authored artifact + exec letter",
        "Pre-Engagement": "Full bespoke artifact + CEO call",
        "Strategic":      "CEO conversation",
        "Tailwind":       "Good News Notice",
        "Annual":         "Simplified value summary",
    }
    return mapping.get(segment, "TBD")

def assign_delivery_owner(segment: str, delta: float) -> str:
    if segment in ("Strategic", "Executive", "Pre-Engagement"):
        return "CEO"
    if segment == "Entity":
        return "CEO / Kylor"
    return "Kylor"

def compose_headline(account: dict, segment: str) -> str:
    """Compose a messaging headline from driver + health — mirrors build_execution_html.py."""
    driver      = account.get("migration_driver", "")
    health_band = account.get("health_band", "")
    company     = account.get("company", "")
    delta       = _safe_float(account.get("delta_mrr", "0"))
    headline    = account.get("messaging_headline", "").strip()  # may be blank in v6.3

    if headline:
        return headline  # keep if already present

    driver_stems = {
        "user_rate_normalization":      "User rate moving to graduated standard ladder.",
        "platform_discount_correction": "Legacy platform discount retired as part of install-base normalization.",
        "tier_base_increase":           "Platform base moving to current tier standard.",
        "included_user_reduction":      "Included user base normalizing to tier standard.",
        "at_book_tier_shift":           "Minor adjustment as book rate moves to current standard.",
        "multi_org_retirement":         "Multi-org program retired; moving to individual standard pricing.",
        "annual_discount_retirement":   "Annual commitment discount retired; standard monthly rate going forward.",
        "special_arrangement":          "Custom arrangement moving to standard tier pricing.",
        "module_compression":           "Module charges consolidating to single tier at a lower rate.",
        "user_count_variance":          "User count aligning to trailing-average actuals.",
        "rate_architecture":            "Rate recalculated under new structure — lower invoice.",
    }
    stem = driver_stems.get(driver, "Pricing moving to current standard.")

    health_suffix = {
        "Thriving": f" At {account.get('health_score', '')} health, the platform is delivering strong value.",
        "Healthy":  " Platform engagement and value delivery are solid.",
        "Watch":    " We see opportunity to strengthen value delivery — a conversation is warranted.",
        "At Risk":  " Flagged for CSM attention before notice.",
        "Critical": " Requires CEO involvement before outreach.",
    }
    suffix = health_suffix.get(health_band, "")
    return stem + suffix

def _safe_float(s: str) -> float:
    try:
        return float(s)
    except (ValueError, TypeError):
        return 0.0

def enrich_accounts(accounts: list[dict]) -> list[dict]:
    """
    Add execution-layer fields that were dropped in v6.3.
    This replicates the enrichment that build_execution_html.py applied.
    Fields added: migration_segment, notice_cohort, notice_deadline,
                  artifact_type, delivery_owner, messaging_headline.
    """
    for a in accounts:
        if a.get("migration_status", "").strip() in ("already_migrated",):
            a.setdefault("migration_segment", "N/A")
            a.setdefault("notice_cohort",     "N/A")
            a.setdefault("notice_deadline",   "")
            a.setdefault("artifact_type",     "N/A")
            a.setdefault("delivery_owner",    "N/A")
            a.setdefault("messaging_headline","Already on new pricing.")
            continue

        segment  = assign_segment(a)
        delta    = _safe_float(a.get("delta_mrr", "0"))

        a["migration_segment"] = segment
        a["notice_cohort"]     = assign_cohort(segment)
        a["notice_deadline"]   = assign_notice_deadline(segment, a)
        a["artifact_type"]     = assign_artifact_type(segment)
        a["delivery_owner"]    = assign_delivery_owner(segment, delta)
        a["messaging_headline"] = compose_headline(a, segment)

    return accounts

def enrich_entities(entities: list[dict]) -> list[dict]:
    """Add execution-layer fields to entity rows."""
    for e in entities:
        name = e.get("entity_name", "")
        e.setdefault("delivery_owner", "CEO" if name in CEO_ENTITY_NAMES else "Kylor")
        e.setdefault("notice_cohort",  "June")
    return entities

def apply_angie_overrides(accounts: list[dict]) -> list[dict]:
    """Apply ANGIE_OVERRIDES to account dicts before enrichment and template filling."""
    for account in accounts:
        ord_id = account.get("ord_id", "")
        overrides = ANGIE_OVERRIDES.get(ord_id)
        if overrides:
            account.update(overrides)
    return accounts

def load_accounts() -> list[dict]:
    return enrich_accounts(apply_angie_overrides(_load_csv(ACCOUNT_CSV)))

def load_entities() -> list[dict]:
    return enrich_entities(_load_csv(ENTITY_CSV))

def load_template(name: str) -> str:
    return (TEMPLATES / name).read_text(encoding="utf-8")


# ── Template token fillers ─────────────────────────────────────────────────────

def fill_notice(account: dict, template: str) -> str:
    tier     = account.get("assigned_tier", "T1")
    segment  = account.get("migration_segment", "Core")

    # Determine CS name for inline references
    owner = account.get("delivery_owner", "Kylor").strip().lower()
    cs_first_name = "the SuperCat team" if owner == "ceo" else "Kylor"

    tokens = {
        # Structural / data tokens
        "{{COMPANY}}":                account.get("company", ""),
        "{{NOTICE_DATE}}":            TODAY_STR,
        "{{EFFECTIVE_DATE}}":         account.get("notice_deadline", "TBD"),
        "{{COHORT_YEAR}}":            account.get("cohort_year", ""),
        "{{CURRENT_STACK}}":          clean_stack(account.get("current_stack", "")),
        "{{ASSIGNED_TIER_NAME}}":     TIER_NAMES.get(tier, tier),
        "{{CURRENT_PLATFORM_MRR}}":   fmt_money(account.get("current_platform_mrr", "")),
        "{{TIER_BASE}}":              fmt_money(account.get("tier_base", "")),
        "{{CURRENT_PROVIDED_USERS}}": account.get("current_provided_users", "—"),
        "{{INCLUDED_USERS}}":         account.get("included_users", "—"),
        "{{CURRENT_USER_MRR}}":       fmt_money(account.get("current_user_mrr", "")),
        "{{TRAILING_AVG_USERS}}":     account.get("trailing_avg_users", "—"),
        "{{USER_CHARGE}}":            fmt_money(account.get("user_charge", "")),
        "{{EXCESS_USERS}}":           account.get("excess_users", "0"),
        "{{CURRENT_MRR}}":            fmt_money(account.get("current_mrr", "")),
        "{{NEW_TOTAL_MRR}}":          fmt_money(account.get("new_total_mrr", "")),
        "{{CS_FIRST_NAME}}":          cs_first_name,

        # Generated content blocks (all conditional, some may be empty string)
        "{{SUPPORT_FIRE_NOTICE}}":       generate_support_fire_notice(account),
        "{{BUNDLE_FLAG}}":               generate_bundle_flag(account),
        "{{ACCOUNT_LEDE}}":              generate_account_lede(account),
        "{{PLATFORM_NARRATIVE}}":        generate_platform_narrative(account),
        "{{HEALTH_BAND_APPEND}}":        generate_health_band_append(account, cs_first_name),
        "{{EARLY_ADOPTER_PARA}}":        generate_early_adopter_para(account),
        "{{BILLING_BASIS_FOOTNOTE}}":    generate_billing_footnote(account),
        "{{DRIVER_NOTICE}}":             generate_driver_notice(account),
        "{{PLATFORM_BASE_DISCLOSURE}}":  generate_platform_base_disclosure(account),
        "{{PLATFORM_BASE_GROWN}}":       generate_platform_base_grown(account),
        "{{OPERATIONS_UNCHANGED}}":      generate_operations_unchanged(account),
        "{{CLOSE_SECTION}}":             generate_close_section(account, segment),
        "{{SIGNOFF}}":                   generate_signoff(account),
    }
    out = template
    for k, v in tokens.items():
        out = out.replace(k, v)
    return out


def clean_narrative(text: str) -> str:
    """
    Strip sentences from composite_narrative that contain internal score vocabulary OR
    internal ops-note language (action items, escalation notes, CSM notes).
    §2.5: health scores, health bands, and dimension scores never appear in client copy.
    """
    import re as _re
    if not text:
        return ""
    banned_patterns = [
        # Score references
        r"score of \d+",
        r"at \d+ or (higher|above|below)",
        r"overall score",
        r"\bscore \d+\b",
        r"\b\d{2,3} reflects\b",
        # Health band names
        r"\bThriving\b", r"\bHealthy\b", r"\bAt Risk\b", r"\bCritical\b",
        r"\bEngagement:\s*\d+", r"\bValue Delivery:\s*\d+",
        r"\bAdoption:\s*\d+", r"\bOperational:\s*\d+",
        # Internal ops notes — action items, escalation, CSM instructions
        r"No action needed",
        r"monitor at standard cadence",
        r"CSM attention",
        r"requires (CEO|operator|escalation)",
        r"flag(ged)? for",
        r"before (notice|outreach|send)",
        r"escalat",
        r"priority: (high|medium|low)",
        r"Flagged",
    ]
    combined = "|".join(banned_patterns)
    sentences = _re.split(r"(?<=[.!?])\s+", text.strip())
    clean = [s for s in sentences if not _re.search(combined, s, flags=_re.IGNORECASE)]
    return " ".join(clean)


def generate_value_summary_lede(account: dict) -> str:
    """
    Lede for the value summary.
    §4.13 override: Watch/At Risk/Critical → dollar-first, no engagement stats.
    Healthy/Thriving → relationship-before-price per §4.1.
    Uses trailing_avg_users (not the cumulative active_users) per §4.2.
    """
    health_band = account.get("health_band", "")
    company     = account.get("company", "")
    cohort_year = account.get("cohort_year", "").strip()
    curr_mrr    = fmt_money(account.get("current_mrr", ""))
    new_mrr     = fmt_money(account.get("new_total_mrr", ""))
    deadline    = account.get("notice_deadline", "TBD")

    try:
        delta_f   = float(account.get("delta_mrr", "0"))
        delta_pct = float(account.get("delta_pct", "0"))
    except (ValueError, TypeError):
        delta_f, delta_pct = 0.0, 0.0

    if _is_watch_band(health_band):
        pct_str = f"{delta_pct:.1f}%".rstrip("0").rstrip(".")
        if delta_f > 0:
            change_phrase = f"a change of ${delta_f:,.0f}/month ({pct_str})"
        elif delta_f < 0:
            change_phrase = f"a reduction of ${abs(delta_f):,.0f}/month ({pct_str})"
        else:
            change_phrase = "no change to the monthly total"
        return (
            f"Effective {deadline}, the monthly invoice for {company} is moving from "
            f"${curr_mrr} to ${new_mrr} — {change_phrase}."
        )

    # Healthy / Thriving
    if delta_f > 0 and delta_pct > 30:
        annual = delta_f * 12
        delta_phrase = f"a ${delta_f:,.0f}/month increase (${annual:,.0f}/year)"
    else:
        delta_phrase = delta_framing(account.get("delta_mrr", ""))

    try:
        years  = 2026 - int(cohort_year)
        # "3 years" — drop "on SuperCat" to avoid repeating it in the same sentence
        tenure_short = f"{years} year{'s' if years != 1 else ''}"
    except (ValueError, TypeError):
        tenure_short = ""

    trailing = account.get("trailing_avg_users", "").strip()
    if trailing and trailing not in ("0", "—", ""):
        stat_sentence = f"{trailing} monthly active users on the platform."
    else:
        stat_sentence = ""

    tenure_clause = (
        f"{company} has been on SuperCat since {cohort_year} — {tenure_short}."
        if tenure_short else f"{company} has been on SuperCat."
    )
    parts = [tenure_clause]
    if stat_sentence:
        parts.append(stat_sentence)
    parts.append(
        f"Your monthly invoice is moving from ${curr_mrr} to ${new_mrr} — {delta_phrase}."
    )
    return " ".join(parts)


def generate_postgres_stat_row(ord_id: str) -> str:
    """
    Populate the session-count + eCat-order-count stat row from cached Postgres metrics.
    Returns empty string if no data is available for the account — never invents numbers.
    §4.2: eCat orders are labeled explicitly as submitted through SuperCat.
    HTML pattern matches the col-2 stat-row used elsewhere in value_summary.html.
    Queried 2026-05-27 via user-supercat-postgres-vpn MCP (login_events 90d + orders LTM).
    """
    metrics = POSTGRES_METRICS.get(ord_id)
    if not metrics:
        return ""  # account not in Postgres cache — leave row empty

    logins = metrics.get("logins_90d")
    orders = metrics.get("ecat_orders_ltm")

    if logins is None and orders is None:
        return ""

    stats_html = ""
    if logins is not None:
        stats_html += (
            f'<div class="stat">'
            f'<div class="stat-val">{logins:,}</div>'
            f'<div class="stat-lbl">Sessions (90 days)</div>'
            f"</div>"
        )
    if orders is not None:
        stats_html += (
            f'<div class="stat">'
            f'<div class="stat-val">{orders:,}</div>'
            f'<div class="stat-lbl">eCat orders (last 12 months)</div>'
            f"</div>"
        )

    if not stats_html:
        return ""

    col_class = "col-2" if (logins is not None and orders is not None) else "col-1"
    return f'<div class="stat-row {col_class}">{stats_html}</div>'


def fill_value_summary(account: dict, template: str) -> str:
    tier        = account.get("assigned_tier", "T1")
    segment     = account.get("migration_segment", "Core")
    health_band = account.get("health_band", "")
    driver      = account.get("migration_driver", "")
    ord_id      = account.get("ord_id", "")
    t           = TIER_PRICES.get(tier, TIER_PRICES["T1"])
    pos_pct     = account_position_pct(account.get("new_total_mrr", ""), tier)

    # Tier name short form for the stat-row col-3 tile
    tier_name_short = TIER_NAMES.get(tier, tier).replace("Commerce ", "")

    # Clean composite narrative — strip sentences with internal score vocabulary (§2.5)
    raw_narrative = account.get("composite_narrative", "")
    clean_narrative_text = clean_narrative(clean_stack(raw_narrative))

    # Engagement evidence: cleaned narrative if meaningful; plain user-count statement otherwise.
    # Never use the raw composite_narrative — it may contain internal ops notes or score references.
    trailing = account.get("trailing_avg_users", "").strip()
    if len(clean_narrative_text) > 20:
        engagement_ev = clean_narrative_text
    elif trailing and trailing not in ("0", "—"):
        engagement_ev = f"{trailing} monthly active users on the platform."
    else:
        engagement_ev = "User activity data on file."

    tokens = {
        # Identity
        "{{COMPANY}}":                      account.get("company", ""),
        "{{DATE}}":                         TODAY_STR,
        "{{EFFECTIVE_DATE}}":               account.get("notice_deadline", "TBD"),
        "{{COHORT_YEAR}}":                  account.get("cohort_year", ""),
        "{{TENURE_YEARS}}":                 tenure_years(account.get("cohort_year", "")),
        # Lede — §4.13 override applied inside generate_value_summary_lede
        "{{VALUE_SUMMARY_LEDE}}":           generate_value_summary_lede(account),
        # Stats (no raw scores or ratios — §2.5 + §4.2)
        "{{TRAILING_AVG_USERS}}":           account.get("trailing_avg_users", "—"),
        "{{ASSIGNED_TIER_NAME_SHORT}}":     tier_name_short,
        # Postgres live metrics — session count (90d) + eCat order count (LTM)
        # Populated from data/postgres_metrics.json (queried 2026-05-27).
        "{{POSTGRES_STAT_ROW}}":            generate_postgres_stat_row(ord_id),
        # Activity table — plain-language labels only, no numeric scores (§2.5)
        "{{ENGAGEMENT_ROW_CLASS}}":         row_class(account.get("engagement_score", "")),
        "{{ENGAGEMENT_STATUS}}":            score_label(account.get("engagement_score", "")),
        "{{ENGAGEMENT_EVIDENCE}}":          engagement_ev,
        "{{ADOPTION_ROW_CLASS}}":           row_class(account.get("adoption_score", "")),
        "{{ADOPTION_STATUS}}":              score_label(account.get("adoption_score", "")),
        "{{ADOPTION_EVIDENCE}}":            adoption_evidence(account),
        "{{VALUE_DELIVERY_ROW_CLASS}}":     row_class(account.get("value_delivery_score", "")),
        "{{VALUE_DELIVERY_STATUS}}":        score_label(account.get("value_delivery_score", "")),
        "{{VALUE_DELIVERY_EVIDENCE}}":      value_delivery_evidence(account, ord_id),
        "{{OPERATIONAL_HEALTH_ROW_CLASS}}": row_class(account.get("operational_health_score", "")),
        "{{OPERATIONAL_HEALTH_STATUS}}":    score_label(account.get("operational_health_score", "")),
        "{{OPERATIONAL_HEALTH_EVIDENCE}}":  operational_health_evidence(account),
        # Tier
        "{{ASSIGNED_TIER_NAME}}":           TIER_NAMES.get(tier, tier),
        "{{TIER_SUBTITLE}}":                TIER_SUBTITLES.get(tier, ""),
        "{{TIER_FEATURES_HTML}}":           TIER_FEATURES_HTML.get(tier, ""),
        # Driver
        "{{DRIVER_EXPLANATION}}":           DRIVER_EXPLANATIONS.get(
                                                driver,
                                                "Your pricing is moving to the current standard for your tier and user count."
                                            ),
        # Pricing table
        "{{CURRENT_STACK}}":                clean_stack(account.get("current_stack", "")),
        "{{CURRENT_MRR}}":                  fmt_money(account.get("current_mrr", "")),
        "{{NEW_TOTAL_MRR}}":                fmt_money(account.get("new_total_mrr", "")),
        "{{CURRENT_PLATFORM_MRR}}":         fmt_money(account.get("current_platform_mrr", "")),
        "{{TIER_BASE}}":                    fmt_money(account.get("tier_base", "")),
        "{{CURRENT_PROVIDED_USERS}}":       account.get("current_provided_users", "—"),
        "{{INCLUDED_USERS}}":               account.get("included_users", "—"),
        "{{CURRENT_USER_MRR}}":             fmt_money(account.get("current_user_mrr", "")),
        "{{USER_CHARGE}}":                  fmt_money(account.get("user_charge", "")),
        "{{EXCESS_USERS}}":                 account.get("excess_users", "0"),
        # Tier position bar
        "{{ACCOUNT_POSITION_PCT}}":         str(pos_pct),
        "{{TIER_FLOOR}}":                   fmt_money(str(t["floor"])),
        "{{TIER_CEILING}}":                 fmt_money(str(t["ceiling"])),
        "{{ACCOUNT_PRICE}}":                fmt_money(account.get("new_total_mrr", "")),
        # Close
        "{{CALLOUT_CLASS}}":                callout_class(health_band),
        "{{NEXT_STEPS_COPY}}":              next_steps_copy(segment, health_band),
    }
    out = template
    for k, v in tokens.items():
        out = out.replace(k, v)
    return out


def build_brand_card(member: dict) -> str:
    """Generate a single brand card HTML block for the entity packet."""
    tier      = member.get("assigned_tier", "T1")
    company   = member.get("company", "")
    curr_mrr  = fmt_money(member.get("current_mrr", ""))
    new_mrr   = fmt_money(member.get("new_total_mrr", ""))
    headline  = member.get("messaging_headline", "")

    try:
        d = float(member.get("delta_mrr", "0"))
        sign   = "+" if d >= 0 else "−"
        delta  = f"{sign}${abs(d):,.0f}/mo"
        d_cls  = "delta-positive" if d > 0 else ("delta-negative" if d < 0 else "delta-neutral")
    except (ValueError, TypeError):
        delta = "—"
        d_cls = "delta-neutral"

    return f"""<div class="brand-card">
  <div class="brand-card-header">
    <span class="brand-name">{company}</span>
    <span class="brand-tier">{TIER_NAMES.get(tier, tier)}</span>
  </div>
  <div class="brand-pricing">
    <span class="brand-current">${curr_mrr}/mo → ${new_mrr}/mo</span>
    <span class="brand-delta {d_cls}">{delta}</span>
  </div>
  <p class="brand-headline">{headline}</p>
</div>"""


def fill_entity_packet(entity: dict, members: list[dict], template: str) -> str:
    entity_name = entity.get("entity_name", "")

    # Delta math
    try:
        default_delta   = float(entity.get("default_delta", "0") or "0")
        delta_sign      = "+" if default_delta >= 0 else "−"
        delta_abs       = fmt_money(str(abs(default_delta)))
        delta_class     = "delta-positive" if default_delta > 0 else ("delta-negative" if default_delta < 0 else "delta-neutral")
    except (ValueError, TypeError):
        delta_sign, delta_abs, delta_class = "+", "—", "delta-neutral"

    try:
        cons_delta      = float(entity.get("consolidated_delta", "0") or "0")
        cons_delta_sign = "+" if cons_delta >= 0 else "−"
        cons_delta_abs  = fmt_money(str(abs(cons_delta)))
    except (ValueError, TypeError):
        cons_delta_sign, cons_delta_abs = "+", "—"

    try:
        saving          = float(entity.get("consolidation_saving", "0") or "0")
        default_mrr_f   = float(entity.get("default_mrr", "1") or "1")
        saving_pct      = f"{100 * saving / default_mrr_f:.0f}"
    except (ValueError, TypeError):
        saving_pct = "0"

    # Effective date from first member's notice_deadline
    effective_date = "TBD"
    if members:
        for m in members:
            nd = m.get("notice_deadline", "").strip()
            if nd and nd != "TBD" and nd:
                effective_date = nd
                break

    # Delivery owner → readable name
    owner_raw = entity.get("delivery_owner", "Kylor")
    cs_contact = "Kylor Johnson" if owner_raw.strip().lower() in ("kylor", "kylor johnson") else owner_raw

    brand_cards = "\n".join(build_brand_card(m) for m in members)

    tokens = {
        "{{ENTITY_NAME}}":           entity_name,
        "{{DATE}}":                  TODAY_STR,
        "{{EFFECTIVE_DATE}}":        effective_date,
        "{{WEIGHTED_HEALTH_SCORE}}": entity.get("weighted_health_score", "—"),
        "{{BRAND_COUNT}}":           str(len(members)) if members else entity.get("brands", "—"),
        "{{CURRENT_ENTITY_MRR}}":    fmt_money(entity.get("current_entity_mrr", "")),
        "{{DEFAULT_MRR}}":           fmt_money(entity.get("default_mrr", "")),
        "{{DELTA_SIGN}}":            delta_sign,
        "{{DEFAULT_DELTA}}":         delta_abs,
        "{{DELTA_CLASS}}":           delta_class,
        "{{BRAND_CARDS_HTML}}":      brand_cards,
        "{{CONSOLIDATED_MRR}}":      fmt_money(entity.get("consolidated_mrr", "")),
        "{{DEFAULT_DELTA_SIGN}}":    delta_sign,
        "{{CONSOLIDATED_DELTA_SIGN}}": cons_delta_sign,
        "{{CONSOLIDATED_DELTA}}":    cons_delta_abs,
        "{{CONSOLIDATION_SAVING}}":  fmt_money(entity.get("consolidation_saving", "")),
        "{{CONSOLIDATION_SAVING_PCT}}": saving_pct,
        "{{CS_CONTACT}}":            cs_contact,
        "{{SCHEDULE_LINK}}":         "mailto:kylor@supercat.io",
    }
    out = template
    for k, v in tokens.items():
        out = out.replace(k, v)
    return out


# ── Main build logic ───────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Build pricing migration HTML drafts")
    parser.add_argument("--ord",     help="Build only this ord_id")
    parser.add_argument("--segment", help="Build only this segment (Core|Narrative|Entity)")
    args = parser.parse_args()

    print("Loading data...")
    accounts = load_accounts()
    entities = load_entities()

    print("Loading templates...")
    notice_tpl  = load_template("notice_standard.html")
    summary_tpl = load_template("value_summary.html")
    entity_tpl  = load_template("entity_packet.html")

    # Build fast lookups
    account_by_ord: dict[str, dict] = {
        a["ord_id"]: a for a in accounts if a.get("ord_id")
    }

    # June cohort filter
    june = [
        a for a in accounts
        if a.get("migration_status") == "migration_pending"
        and a.get("notice_cohort") == "June"
    ]

    if args.ord:
        june = [a for a in june if a.get("ord_id") == args.ord]
        if not june:
            print(f"No June cohort account found with ord_id '{args.ord}'")
            sys.exit(1)

    if args.segment:
        june = [a for a in june if a.get("migration_segment") == args.segment]

    print(f"\nJune cohort ({len(june)} accounts):")
    for seg, ct in sorted(Counter(a["migration_segment"] for a in june).items()):
        print(f"  {seg}: {ct}")

    # Ensure output dirs exist
    for seg in ("core", "narrative", "entity"):
        (DRAFTS / seg).mkdir(parents=True, exist_ok=True)

    generated, errors = 0, []

    # ── Core + Narrative ──────────────────────────────────────────────────────
    for account in june:
        seg = account.get("migration_segment", "")
        if seg not in ("Core", "Narrative"):
            continue

        company = account.get("company", "unknown")
        ord_id  = account.get("ord_id", "xxx")
        out_dir = DRAFTS / seg.lower()
        base    = f"{ord_id}__{slugify(company)}"

        try:
            notice_path = out_dir / f"{base}__notice.html"
            notice_path.write_text(fill_notice(account, notice_tpl), encoding="utf-8")

            summary_path = out_dir / f"{base}__value-summary.html"
            summary_path.write_text(fill_value_summary(account, summary_tpl), encoding="utf-8")

            print(f"  ✓ {company} ({ord_id}) [{seg}]")
            generated += 2
        except Exception as e:
            errors.append(f"{company} ({ord_id}): {e}")
            print(f"  ✗ {company} ({ord_id}): {e}")

    # ── Entity packets ────────────────────────────────────────────────────────
    if not args.segment or args.segment == "Entity":
        june_entities = [e for e in entities if e.get("notice_cohort") == "June"]

        for entity_row in june_entities:
            entity_name = entity_row.get("entity_name", "")
            if not entity_name:
                continue

            # Resolve member accounts via member_ord_ids (separator: " || ")
            raw_ids = entity_row.get("member_ord_ids", "")
            ord_ids = [x.strip() for x in re.split(r"\s*\|\|\s*", raw_ids) if x.strip()]
            members = [account_by_ord[o] for o in ord_ids if o in account_by_ord]

            if not members:
                print(f"  ⚠ Entity '{entity_name}': no member accounts resolved from '{raw_ids}'")
                continue

            out_path = DRAFTS / "entity" / f"{slugify(entity_name)}__entity-packet.html"
            try:
                out_path.write_text(
                    fill_entity_packet(entity_row, members, entity_tpl),
                    encoding="utf-8"
                )
                print(f"  ✓ {entity_name} ({len(members)} brands) [Entity]")
                generated += 1
            except Exception as e:
                errors.append(f"Entity {entity_name}: {e}")
                print(f"  ✗ Entity {entity_name}: {e}")

    # ── Slack flags — bundle_config_mismatch accounts ─────────────────────────
    print(f"\n{'─' * 55}")
    print("📋 SLACK FLAGS — copy/paste for Angie review:")
    print(f"{'─' * 55}")
    for flag in SLACK_FLAGS:
        print(f"\n*{flag['account']}*")
        print(f"  ✅ Applied: {flag['what_changed']}")
        print(f"  ❓ Still need from Angie:")
        for q in flag["questions"]:
            print(f"     • {q}")

    # ── Summary ───────────────────────────────────────────────────────────────
    print(f"\n{'═' * 55}")
    print(f"Generated: {generated} files → {DRAFTS}/")
    if errors:
        print(f"\nErrors ({len(errors)}):")
        for e in errors:
            print(f"  ✗ {e}")
    else:
        print("No errors.")


if __name__ == "__main__":
    main()
