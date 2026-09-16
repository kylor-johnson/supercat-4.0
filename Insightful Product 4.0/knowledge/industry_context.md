# Industry Context — Furniture, Lighting & Décor Manufacturing

> **Scope.** This file is the "everyone in this industry already knows it" layer. Its job is to stop the
> report from *discovering* things that are simply true of the industry — seasonality, market-calendar dips,
> structural account concentration, channel mix — and presenting them as findings. It is read on **every**
> report, alongside `communication_guideline.md` and the client's `profile.md`.
>
> **The governing rule this file exists to enforce:**
> **If a pattern in the data is explained by something in this file, it is CONTEXT, not a FINDING.**
> Name it as expected ("the Q1→Q2 cooling is the normal post-market pattern") and move on — or don't mention
> it at all. A "finding" must be something the operator could *not* have predicted from the calendar alone.

---

## Who these clients are (the book we serve)

The clients are **B2B manufacturers and wholesalers** of furniture, lighting, and home décor who sell
through SuperCat's eCat suite. Across the current book of ~110 clients the mix is roughly:

- **~54% lighting** (decorative + architectural: chandeliers, pendants, sconces, lamps, fans, outdoor)
- **~32% furniture** (case goods, upholstery, outdoor, contract)
- **~13% home décor / housewares / art** (mirrors, wall art, tabletop, giftware, accessories)

So the default voice should assume a lighting or furniture manufacturer — **but never assume which one for a
specific client.** The per-client `profile.md` states it. (And note the segment *label* in source data can be
wrong — e.g., a case-goods house mis-tagged "Lighting" — so the profile, not the label, is authoritative.)

**Their customers (the manufacturer's customers) are almost never end consumers.** They are:
- **Interior designers and the design trade** — buy for specific client projects; lumpy, project-driven,
  often order after hours via web; price-sensitive to trade discounts.
- **Independent furniture/lighting retailers and dealers** — reorder around their own floor turns; the
  classic stocking-dealer relationship.
- **Hospitality / contract / commercial** — hotels, senior living, restaurants; large, lumpy, spec-driven
  project orders with long lead times.
- **Online retailers / marketplaces** — Wayfair, Perigold, 1stDibs, Lumens, Lamps Plus, Ferguson. Often
  **drop-ship**, often a manufacturer's single largest account, and structurally different from the dealer
  book (high volume, lower touch, concentration risk).
- **Electrical / lighting distributors** (lighting-specific) and **specifiers/architects** (contract).

A given manufacturer usually sells through **several of these at once** (dealer network + trade program +
marketplace + some DTC). Multi-channel is the norm, not the exception — so "you sell through multiple
channels" is never a finding.

---

## How they sell (channel reality — don't "reveal" this)

Near-universal across the book: a **dealer/distributor network** and a **trade program** (login-gated
pricing for designers). Very common: a **DTC/e-commerce** storefront and **marketplace** presence. The eCat
suite itself splits into the **iPad app** (reps in the field and at markets, online/offline), **eCat Online**
(web catalog / B2B eComm / after-hours designer ordering), and the **Sales Portal** (the BI layer).

**Critical for confidence framing:** eCat capture is almost always a *minority* of a client's total business
— a manufacturer's orders also flow through EDI, phone, marketplace drop-ship, and direct CS email that eCat
never sees. **eCat-channel data is never high-confidence about the client's whole business.** This is the
single most important honesty constraint and it is structural to the industry, not a per-client quirk.

---

## The market calendar (this is the seasonality fix)

Furniture, lighting, and décor run on a **wholesale market / trade-show calendar**, and order flow clusters
around it. This is the #1 source of fake "discoveries" — a report sees Q1 strong and summer soft and calls
it a finding, when every operator knows exactly why. The major beats:

- **High Point Market (North Carolina)** — the dominant furnishings market. **Spring (April)** and
  **Fall (October)** editions. The single biggest driver of order timing for most case-goods and décor brands.
- **Las Vegas Market** — **Winter (late Jan)** and **Summer (late July/Aug)**. Big for furniture, lighting,
  gift, and home décor; West-coast and cross-category reach.
- **Dallas Total Home & Gift Market** — multiple editions (Jan, June); strong for décor, gift, lighting.
- **Atlanta (AmericasMart)** — gift/décor/home, January and July.
- **Lightovation / Dallas Lighting Market** and **lighting-specific** beats — relevant for lighting houses.
- **Salone del Mobile (Milan, April)** — global design bellwether, more influence than direct US order flow.

### What follows from the calendar — treat ALL of this as expected, not as findings:

- **Q1 is seasonally strong** for many brands: orders written at Winter Vegas / January Dallas-Atlanta and
  the run-up to Spring High Point land as Q1–early-Q2 revenue.
- **Spring (post–High Point, April–May)** is typically a high-water mark; **summer (June–August) cools** as
  the industry quiets between Spring and Fall markets and showrooms slow. **A Q1→Q2 or spring→summer dip is
  the normal pattern, not a warning sign.** Only flag it if the decline is materially steeper than the
  client's own prior-year same-period pattern.
- **Fall (post-October High Point)** typically re-accelerates orders into Q4.
- **Holiday/Q4** matters more for décor, gift, and tabletop than for case goods.
- **Year-over-year, same-period comparisons are the only honest momentum read.** Comparing Q2 to Q1 in this
  industry mostly measures the calendar, not the business. Always compare a period to the **same period last
  year**, and say so.

### How to write about seasonality (examples)

| ❌ Tone-deaf "discovery" | ✅ Context-aware |
|---|---|
| "The growth rate halved from Q1 to Q2 — March was the peak, then May/June settled lower." | *(Cut, or: "Q2 softened off the spring-market peak as expected; the number that matters is Q2 vs. Q2 last year, which is +X%.")* |
| "Revenue cooled in the second half." | *(Only a finding if it diverges from their own seasonal norm. Otherwise it's the calendar — don't mention it.)* |
| "Summer orders dropped across the board." | *(Expected between markets. Silence is the right move unless a specific account broke its own seasonal pattern.)* |

---

## Structural truths that are NEVER findings on their own

These are inherent to the industry. State them only as *framing* for a sharper point, never as the insight:

- **Big-account concentration is normal.** A dealer or a marketplace (often Wayfair) being 20–40% of a
  manufacturer's revenue is structurally common. Concentration becomes a *finding* only when paired with a
  second fact: it's growing dangerously, it's declining, or it's tied to a single rep / single relationship
  that could discontinue. "You're concentrated" alone is not news; "your #1 account is 30%, grew 65%, and
  sits with one rep whose book is 76% that account" is.
- **Lumpy, project-driven revenue** is normal for trade/designer and contract/hospitality buyers. A big
  one-time project order followed by silence is not "churn" — it may be a completed project. Don't call a
  project buyer "dormant" the way you'd call a stocking dealer dormant.
- **Reorder vs. project cadence differ by buyer type.** Lighting and décor stocking dealers reorder
  frequently; designers and contract buyers order in project bursts. The *same* "60 days silent" means
  different things for each. Cadence findings must respect buyer type (from the profile).
- **Long lead times** (custom, configure-to-order, COM upholstery, imported case goods, container freight)
  are normal. Order-to-ship gaps are not automatically a problem.
- **Custom / configure-to-order pricing** (grade-riser, fabric grade, finish, COM) is core to furniture
  especially — price dispersion on configured items can be legitimate configuration, not discount leakage.
  Be careful attributing "leakage" where configuration explains the spread.
- **Returns are low-frequency but high-stakes** (freight damage on large items). Absence of returns data is
  a gap to disclose, not a zero to assume.

---

## Selling-motion segments in SuperCat's client book (context, not findings)

SuperCat classifies its ~109 client **organizations** by **selling motion** into four stamped segments
(Client Segmentation v4.0, 2026-07-09). This is **Workstream A** — how *this manufacturer* goes to market.
Do not confuse it with the per-client **customer** segmentation (behavior-derived clusters of the buyers
*inside* one client's book), which is a different, 🧊 FROZEN method (`../foundation/segmentation_derivation.md`
/ Q-SEG-DERIVE, Spine §8) and is out of scope for the report.

**Where membership lives:** the client's `profile.md` §2 states the stamped segment. **Never invent or
re-derive segment membership in the report** — read it from the profile, or treat it as absent. The four
selling motions:

- **Luxury Specification** — designers and architects specify the product into a project; the sale is
  project-driven, relationship-driven, taste-driven. When the profile says this segment, treat as CONTEXT
  (not a finding):
  - Revenue is **project-lumpy** — big, complex, sometimes bespoke orders followed by quiet.
  - A one-time / lumpy buyer is often a **designer/project purchase** — a conversion / project-completion
    test, **not** assumed churn.
  - Buyers are trade/designers/showrooms/A&D; multiple trade/designer/contract price tiers are normal.
- **Premium Trade Brand** — dealers carry the line on brand reputation (brand → dealer → end consumer).
  CONTEXT (not a finding):
  - **Stocking-dealer reorder** is the default mental model for the base.
  - Broad dealer / territory coverage (often the widest territory spread of any segment) is structural.
  - A one-time tail is still a **conversion test**, not automatic churn.
- **Mid-Market Multi-Channel** — the line reaches market through trade + retail + online + contract at once.
  CONTEXT (not a finding):
  - **Do not assume a single buyer type** — the book mixes stocking dealers, retailers, online/marketplace,
    and some trade.
  - Many price codes / **channel-mix pricing complexity** is expected, not a finding.
  - Cadence findings must **respect the channel mix** — the same "60 days silent" means different things
    across channels.
- **Volume Distribution** — commodity distribution: high volume, low unit price, low touch; edge is
  logistics, breadth, and price. CONTEXT (not a finding):
  - A **replenishment / retailer-procurement** motion, often importer/distributor rather than manufacturer.
  - **Extreme account concentration and a very low unit price are structurally common** — don't "discover"
    commodity concentration as a surprise without a second fact (growing dangerously, declining, or tied to
    a single rep/relationship).
  - Flat pricing (often a single price code) and very high order counts are the norm.

**Reaffirmations (these are why the segment is context, not the insight):**
- **Price is a correlate, not a classifier.** Spec vs Brand-Building is **selling motion**, not average
  selling price — Specification and Brand-Building overlap heavily in the $300–$700 zone, and several
  Specification orgs price *below* Brand-Building orgs. Do not infer a segment from price.
- **Product vertical does not define segment.** Lighting spans all four segments; furniture spans three.
  What they sell is a tag, not the classifier.
- **Never print the internal segment label in client-facing copy.** The report does **not** say "As a
  Luxury Specification manufacturer…". Framing flows through the **buyer-type / channel language the
  profile already authorizes** (designer-project vs stocking-dealer vs marketplace), never through the
  internal selling-motion label.

---

## Vocabulary to use correctly (so the report sounds native, not borrowed)

- **The trade / to the trade / trade program** — designer-facing, login-gated wholesale pricing.
- **Stocking dealer vs. non-stocking dealer** — carries inventory vs. orders per-project.
- **COM (Customer's Own Material)** — buyer supplies fabric; common in upholstery.
- **Spec / specifier** — architects/designers writing products into a commercial project.
- **Drop-ship** — manufacturer ships direct to the marketplace's customer (Wayfair model).
- **Quick-ship / stocked program** — in-stock SKUs for fast fulfillment vs. made-to-order.
- **Case goods** — non-upholstered furniture (tables, casegoods, storage). **Upholstery** is its own world.
- **Market** (noun) — a trade-show edition ("at Spring Market," "we wrote it at High Point").

**Avoid borrowed cleverness:** no "franchise," no "flywheel," no "treadmill" as a *label*. If you mean a SKU
sells a lot, say it sells a lot and give the number. (See the anti-cute rule in the communication guideline.)

---

> **One-line version:** This is a seasonal, multi-channel, relationship-driven wholesale industry where
> big-account concentration, lumpy project orders, post-market summer cooling, and eCat being a minority of
> total sales are all *normal*. None of them is a finding by itself. A finding is what's left after you
> subtract everything an experienced operator already expects from the calendar and the structure.
