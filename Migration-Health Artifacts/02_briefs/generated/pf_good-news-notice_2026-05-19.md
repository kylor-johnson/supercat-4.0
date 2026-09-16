# Palecek: Your Invoice Is Decreasing

*Effective [EFFECTIVE_DATE — insert 60 days from send date]*

---

Your monthly invoice is decreasing from **$3,190** to **$2,909** — a reduction of **$281/month** — effective [EFFECTIVE_DATE].

## Why the Number Is Changing

**Driver: module_compression**

SuperCat's 2026 pricing restructure moves all accounts from legacy module-based billing to a unified tier subscription. Palecek's current invoice reflects separate component charges — iPad App and Catalog — that carried their own rate history going back to 2012. Under the new structure, both are included in a single Catalog Essentials (T1) subscription, and the user rate applies a graduated scale to your active user base.

Here's what changes:

| | Before | After |
|---|---|---|
| Platform components (iPad + Catalog) | $[CSM: fill from billing — approx. $1,230] | — |
| T1 Catalog Essentials base | — | **$749** |
| Included users | 10 | **10** |
| Additional billable users | ~98 users at $20/user = **$[CSM: fill]** | 110 users, graduated: 10×$25 + 15×$22 + 25×$20 + 60×$18 = **$2,160** |
| **Monthly total** | **$3,190** | **$2,909** |

> **CSM note (remove before sending):** Pull the exact legacy platform component breakdown from Stripe before sending. The new math is confirmed ($749 + $2,160 = $2,909). The legacy breakdown should match the $3,190 total so the table closes correctly. If the user count used is different from 110, recalculate the graduated column.

Palecek has been on SuperCat since 2012 — 14 years of active platform use. The rate structure in place at signing predates the current commercial model by more than a decade. The 2026 refresh applies the same unified pricing to every account across the install base. For Palecek, this produces a lower invoice.

Your workflow, your team's access, your catalog, and your integrations are unchanged. The only thing changing is the invoice.

Every account at every tier is moving to the same pricing structure in 2026. This is the number your configuration produces under that structure.

---

## Your Pricing at a Glance

| | Before | After |
|---|---|---|
| **Monthly** | $3,190 | **$2,909** |
| **Annual** | $38,280 | **$34,908** |
| **Change** | — | –$281/month (–8.8%) |
| **Effective date** | — | [EFFECTIVE_DATE] |
| **Tier** | T1 — Catalog Essentials | T1 — Catalog Essentials |
| **Included users** | 10 | 10 |
| **Additional user rate** | $20/user (legacy flat) | Graduated ($25/$22/$20/$18) |

---

Questions about what's changing or how the new rate was calculated — reach out directly.

*[CSM NAME] | Customer Success | SuperCat*

---

> **Internal routing note (remove before sending):**
> Brief type: `good_news_notice` | Format: Tailwind (decrease)
> Account: pf — Palecek | Tier: T1 | Wave: 1
> Migration driver: module_compression | Health: 95.9 — Thriving
> Current MRR: $3,190 | New MRR: $2,909 | Delta: –$281/month (–8.8%)
> Cohort: 2012 (14yr early adopter) — tenure acknowledged in body
> Expansion eligible: t1_to_t2 — queue Format C ONLY after confirmed positive signal from this notice
>
> **Pre-send checklist:**
> - [ ] Fill EFFECTIVE_DATE (60 days from send)
> - [ ] Pull legacy platform component breakdown from Stripe; fill CSM note in table
> - [ ] Confirm 110 as the modeled user count (trailing 6-month average from v6 model)
> - [ ] Confirm no open support tickets or billing disputes before sending
> - [ ] Do NOT include Format C expansion opportunity in this notice or any follow-up before positive signal
