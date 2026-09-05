---
id: MEAS-07
title: Line F — direction of travel, 24 months
version: 1.0
status: evidence pack
date: 2026-08-31
database: supercatprod
---

# Line F — direction of travel

Everything in the register is point-in-time. This is the movement. Eight quarters, to the last
complete quarter (2026Q2).

---

## 1. Order volume and channel mix

`MEASURED` · Q054 · `data/Q054.csv`

| Quarter | Orders | Buyer web | iPad | Web share | Orgs | Distinct writers |
|---|---:|---:|---:|---:|---:|---:|
| 2024Q3 | 42,454 | 8,441 | 34,013 | 19.9% | 85 | 4,336 |
| 2024Q4 | 41,331 | 7,455 | 33,876 | 18.0% | 86 | 4,210 |
| 2025Q1 | 45,165 | 8,353 | 36,812 | 18.5% | 97 | 4,800 |
| 2025Q2 | 47,894 | 9,557 | 38,337 | 20.0% | 96 | 5,002 |
| 2025Q3 | 45,481 | 9,321 | 36,160 | 20.5% | 90 | 4,802 |
| 2025Q4 | 41,134 | 8,880 | 32,254 | 21.6% | 91 | 4,827 |
| 2026Q1 | 46,178 | 9,665 | 36,513 | 20.9% | 95 | 5,393 |
| **2026Q2** | **48,387** | **10,907** | **37,480** | **22.5%** | 94 | **5,528** |
| **Change** | **+14.0%** | **+29.2%** | **+10.2%** | +2.6pp | +9 | **+27.5%** |

**Buyer-initiated web ordering is growing at nearly three times the rate of iPad ordering.** Web
share of all orders has risen every year, from 19.9% to 22.5%. Distinct order writers are up 27.5%.

## 2. The rep population is flat

`MEASURED` · Q050 · `data/Q050.csv`

Distinct internal users generating an iPad login event per quarter:

| 2025Q1 | 2025Q2 | 2025Q3 | 2025Q4 | 2026Q1 | 2026Q2 |
|---:|---:|---:|---:|---:|---:|
| 1,994 | **2,530** | 2,316 | 2,294 | 2,348 | 2,301 |

**Flat to slightly declining since the 2025Q2 peak.** Orgs with any iPad login activity have moved
132 → 142 over the same period, so the platform is adding clients while the distinct rep headcount
inside them stays level.

*Note:* `login_events` is effectively an iPad-login table — buyers appear only 57–91 per quarter, so
it cannot be used for buyer trends. Buyer direction is read from web order volume above.

## 3. The headline trend

**The buyer population is growing faster than the rep population — and the rep population is not
growing at all.**

| | Direction |
|---|---|
| Buyer web orders | **+29.2%** over 8 quarters |
| Distinct order writers | +27.5% |
| Total orders | +14.0% |
| iPad orders | +10.2% |
| **Distinct active reps** | **flat / slightly down since 2025Q2** |
| Client orgs with order activity | 85 → 94 |

---

## 4. Does any trend reverse a priority?

`JUDGMENT`, grounded in Q054, Q050, Q017, Q062.

**Yes — one, and it is the same tension `04-REACH-AND-SIZING.md` finds from a static angle.**

The roadmap's bucket A ranks the two buyer configuration items **15th and 16th of 16** — last. The
trend says the buyer channel is where the growth is, and the static reach says those two items touch
**18,057 and 17,522 active buyers** respectively against **655 records / 559 people** for the
flagship rep build.

Three independent lines now point the same direction:

1. **Reach** — buyer config items reach 28× more users than the rep component (Q017, Q062)
2. **Growth** — the buyer channel grows 3× faster and the rep population is flat (Q054, Q050)
3. **Gap exposure** — the invoice-feed gap costs 49% of reps and 6% of buyers (Q020), so the client-
   data push the register recommends is also a rep-side motion

**This does not say cancel the rep component.** Band C reps (353 records) write 86% of all orders and
$143.4M of value — that is where the money is written today, and `02-PERSONA-EVIDENCE.md` shows they
are a real and coherent population. The rep story is the *value* story; the buyer story is the
*growth* story.

**It does say the readout should present the ordering as a deliberate choice rather than as an
output of the ranking.** The register's own text acknowledges "reach and job-strength are different
axes." The trend data means that acknowledgement now has to be defended rather than noted.

---

## 5. A caution about every value series

`MEASURED` · Q055, Q056 · **Do not chart `orders.total` without reading this.**

Over 24 months, 357,317 orders total **$2,048,128,996**. Of that:

- **15 orders above $1M account for $496,085,960 — 24.2% of the entire recorded value**
- A **single order at org `shl` is $464,039,002**, which alone creates the 2025Q2 spike
  ($705.6M against a $156M–$220M band in every other quarter)
- 11,925 orders (3.3%) have a total of zero
- No negative totals

**Excluding that one order, 24-month order value is approximately $1.584B.** The value column in
`data/Q054.csv` is flagged accordingly.

This matters beyond charting. It is a concrete mechanism behind the register's "eCat runs
0.22–3.10× invoiced truth, usually understating" — and it lands directly on JTBD-031 and JTBD-061,
whose whole purpose is a topline someone can defend. **A topline computed off `orders.total` with no
outlier handling is wrong by a quarter of its own value.** Any implementation of those jobs needs an
explicit outlier policy, and the register does not currently call for one.

---

## 6. Coverage trends worth watching

| | Now | Note |
|---|---:|---|
| Orgs with any invoice feed | 56 | but only **44 have a feed dated in the last 12 months** (Q003) — 12 have lapsed |
| Orgs with a territory master | 26 | of 258; 23 of the 144 orgs with active reps |
| Orgs with active order flow | 112 | up from 85 orgs with quarterly order activity two years ago |
| Active items in catalog | 938,893 across 241 orgs | Q005 |

The **12 lapsed feeds** are the trend item here: feed coverage is not only incomplete, it is
decaying. That is a monitoring gap as much as an onboarding one, and nothing currently surfaces it —
which is the same absence JTBD-034 describes for imports.
