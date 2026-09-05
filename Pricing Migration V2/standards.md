# Migration Communication Standards — 2026

> **This is the single reference document for all migration communication decisions.**
> Source: distilled from `_root/` (original governance layer) + `communication_standards__v1.md` (CEO package).
> Last updated: 2026-05-27

---

## 1. The Core Principle

**The notice triggers the legal 60-day clock. Companion materials carry the substance.**

- Notice = formal legal vehicle (Standard Migration Notice, Value Migration Notice, Entity Packet)
- Companion = value + context (Simplified Value Summary, Full Bespoke Artifact)
- Every account migration_pending needs a notice. Some also need a companion.

---

## 2. Who Gets What

| Segment | Delta | Notice template | Companion | Owner | Cohort |
|---|---|---|---|---|---|
| **Core** | ≤$200 | Standard Migration Notice | Simplified Value Summary | Kylor | June |
| **Narrative** | $201–$400 | Standard Migration Notice | Simplified Value Summary | Kylor | June |
| **Entity** | Any | Entity Migration Packet | (packet IS the notice) | CEO (complex) / Kylor (simple) | June |
| **Executive** | $401–$600 | Value Migration Notice | Full Bespoke Artifact + CEO Letter | CEO + Kylor | July |
| **Pre-Engagement** | >$600 | Value Migration Notice | Full Bespoke Artifact + CEO call first | CEO | July |
| **Tailwind** | < $0 | Good News Notice | None | Kylor | Deferred |
| **Strategic** | Any | Strategic Migration Notice (post-conversation) | None | CEO | Post-Migration |
| **Annual** | Any | Annual Renewal Notice | Matches natural segment | Kylor + CEO | Renewal-Based |

**June cohort = 55 accounts (Core 13 + Narrative 15 + Entity 27). Target: notices out by July 1, effective October 1.**

---

## 3. The Three Tiers

| Tier | Name | Base | Included Users | What's included |
|---|---|---|---|---|
| T1 | Catalog Essentials | $749/mo | 10 | Rep iPad app, buyer catalog, standard support |
| T2 | Commerce Professional | $1,295/mo | 15 | + online ordering, order/invoice tracking, dedicated CSM |
| T3 | Commerce Enterprise | $2,295/mo | 40 | + sales intelligence, CPQ, credit card processing, priority support |

**User-rate ladder (above included base):**
- 1–10 excess: $25/user
- 11–25 excess: $22/user
- 26–50 excess: $20/user
- 51+: $18/user

---

## 4. Voice — The Non-Negotiables

1. **Lead with the dollar amount and effective date. Never lead with a percentage.**
2. **Never apologize for the change.** The prior invoice reflected the legacy structure. It wasn't wrong.
3. **Never use "we're adjusting your pricing."** Corporate hedging reads as discomfort.
4. **Confirm operations are unchanged.** Reader's first question is "what breaks?" Answer it early.
5. **Never include health scores, bands, or dimension scores in client copy.** Internal only.
6. **No expansion or upgrade language in a migration notice.** Migration first. Expansion after a positive signal.
7. **State "every account we work with is moving to the same structure" without hedge.** No "most," "many," "broader install base."
8. **Lede stats must be unambiguous platform metrics.** Active users, sessions, tenure. Never total ERP order volume.

---

## 5. Forbidden Phrases → Replacements

| Don't write | Write instead |
|---|---|
| "we're adjusting your pricing" | Lead with dollar + effective date |
| "as part of this refresh" | "going forward" |
| "rate card" | "our current standard pricing" / "the standard rate" |
| "T1 / T2 / T3" in running prose | "Catalog Essentials" / "Commerce Professional" / "Commerce Enterprise" |
| "install base" | "every account we work with" |
| "Thriving," "Healthy," "Watch," "At Risk" | Never client-facing |
| "p25," "p75," "percentile" | "below the midpoint" / "near the midpoint" / "above the midpoint" |
| peer dollar ranges ("ranges from $1,295–$1,589") | Position language only, no dollar ranges |
| "trailing 12-month average" | "your team averages around [N] users" |
| "transition" (describing customer's side) | "going forward" / "effective [DATE]" |
| "renewal," "auto-renew," "subscription renewal" | Lead with dollar + effective date; explain via driver |
| "gift," "reward for loyalty" (Good News) | State the mechanic: "the consolidation produces a lower combined rate" |

---

## 6. The 11 Migration Drivers

| `migration_driver` | Plain English | Accts |
|---|---|---:|
| `user_rate_normalization` | Per-user rate locked at signing → graduated standard ladder | 38 |
| `platform_discount_correction` | Signing-time platform discount retired across all accounts | 17 |
| `tier_base_increase` | Platform base moving from old book rate to current tier standard | 13 |
| `included_user_reduction` | Legacy expanded included-user allotment normalizing to tier standard | 10 |
| `at_book_tier_shift` | Already at book rate; minor adjustment as book moves to standard | 9 |
| `multi_org_retirement` | Multi-org pricing program retired; each entity to individual standard | 6 |
| `annual_discount_retirement` | Annual commitment discount retired; standard monthly rate going forward | 2 |
| `special_arrangement` | Custom arrangement → standard tier pricing | 1 |
| `module_compression` | Separate module charges consolidating to single tier (price decrease) | 8 |
| `user_count_variance` | Billed user count above trailing average; aligning to actuals (decrease) | 2 |
| `rate_architecture` | Legacy rate structure recalculated → lower invoice (decrease) | 1 |

**Key rule:** Use v6.2 `migration_driver` value to select the explanation block. Never infer from pricing math.

---

## 7. Health Band → Tone

| Health Band | Score | Tone rule |
|---|---|---|
| Thriving | 80–100 | Lead with platform value stats; warm but direct |
| Healthy | 60–79 | Standard tone; relationship-before-price |
| Watch | 40–59 | Skip platform stats. Lead with dollar + date. Don't lecture on health |
| At Risk / Critical | 0–39 | Dollar-first opening only. No platform stats. No cheerfulness |

Health band names **never** appear in client copy.

---

## 8. Platform Narrative (canonical paragraph)

Use this sentence when explaining *why* everyone is moving:

> "SuperCat is moving all accounts to a standardized pricing architecture — three platform tiers based on the capabilities you use, with transparent, graduated user pricing. Your current terms reflect a legacy arrangement from [COHORT_YEAR] that predates this structure. Every SuperCat account is migrating to the same architecture — consistent tiers, consistent user economics, consistent investment in the platform you depend on."

---

## 9. "What's Coming in 2026" (verbatim block — include in every notice)

> **June 1**
> - **Rebuilt admin console** — The admin console is getting its first major redesign in years. Faster to navigate, easier to update, cleaner day-to-day management from top to bottom.
> - **Rapid fire scanning** — Optimized for high-volume market environments. Your reps write more orders, move between meetings faster, without losing momentum mid-floor.
> - **Multiple active orders** — Open more than one order at a time. Start a cart for one account, shift to another buyer, come back without starting over.
>
> **July 1**
> - **Rep activity log** — Your reps log calls, visits, and follow-up notes inside SuperCat. You see it in one place — no separate system needed.
> - **Direct catalog editing** — Edit product data, configurations, and mappings in a live web view. The export-edit-reimport cycle for small catalog changes goes away.

---

## 10. Pre-Send Quality Checks

Before sending any notice:

- [ ] Dollar amount and effective date are in the first sentence
- [ ] No percentages in the lede
- [ ] Operations-unchanged sentence is present
- [ ] Health band names absent from all client-facing copy
- [ ] Platform narrative paragraph present
- [ ] "What's Coming in 2026" block present and verbatim
- [ ] Driver explanation matches `migration_driver` from v6.2
- [ ] Pricing table numbers match v6.2 CSV exactly
- [ ] Formal notice line present (except Good News)
- [ ] Internal routing notes stripped before send

---

## 11. Concession Guardrails

| Segment | Pre-authorized (Kylor can offer) | Requires CEO approval |
|---|---|---|
| Core | User cleanup, billing date adjustment, annual prepay | Any discount > 10% of target |
| Narrative | User cleanup, 30-day transition credit, annual prepay | Permanent discount, credit > 30 days, any discount > 10% |
| Entity | Multi-brand consolidation, user cleanup, 30-day transition credit | Entity-level concessions only — no brand-by-brand improvisation |
| Executive | TBD | All concessions |
| Pre-Engagement | TBD | All concessions |

---

## 12. Audience

The reader is the **CFO, business owner, or principal of a B2B furniture, lighting, or decor wholesaler**.

> Write for a principal who runs a wholesale business, not a software buyer renewing a SaaS seat.

- Declarative. Professional. Empathetic on impact. Firm on architecture.
- Peer-to-peer (CEO Letter) or vendor-to-principal (all other formats).
- Never service-rep-to-buyer. Never marketing-to-prospect.
