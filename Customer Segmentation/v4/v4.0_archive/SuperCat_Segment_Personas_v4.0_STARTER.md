# SuperCat Segment Personas v4.0 Starter

**Date:** July 7, 2026
**Parent segmentation:** `Customer Segmentation/current/SuperCat_Client_Segmentation_v4.0.md`
**Purpose:** Start the persona layer for rep co-pilot initialization without reopening segment membership.

## Persona Rules

- Personas live inside accepted segments; they do not reclassify orgs.
- Use segment membership for tone and default sales motion.
- Use account-level facts for recommendations only after the segment context is set.
- Treat Specialty/Non-Traditional as an exception flow until a client-specific operating model is known.

## 1. Luxury Specification

Designer-specification selling motion: products are selected by interior designers, architects, and trade professionals for projects. Price supports the read, but the real distinction is high-touch spec work.

### Project Specifier

**Buyer / rep context:** Designer or architect specifying a full room, residence, hospitality space, or high-touch custom project.

**Co-pilot should:** Surface collection fit, finish/material language, lead time sensitivity, and project-scale completeness.

**Avoid:** Do not push commodity replenishment or generic promos; keep the advice project-aware and design-literate.

### Trade Showroom Partner

**Buyer / rep context:** Showroom or trade dealer helping designers translate client intent into a curated product set.

**Co-pilot should:** Suggest complementary pieces, margin-aware alternatives, and presentation-ready talking points.

**Avoid:** Do not treat the buyer as an end consumer browsing one-off SKUs.

## 2. Premium Trade Brand

Brand-led dealer and trade selling: reps manage dealer relationships, territory coverage, and brand pull across trade channels.

### Authorized Dealer Manager

**Buyer / rep context:** Dealer principal or buyer managing a branded line across showroom, ecommerce, or territory demand.

**Co-pilot should:** Emphasize top sellers, line coherence, reorder opportunities, and tier-appropriate pricing.

**Avoid:** Do not assume every order is a bespoke project; this motion often needs dealer growth and assortment guidance.

### Brand Rep Territory Builder

**Buyer / rep context:** Rep managing dealer coverage and trying to expand penetration across accounts.

**Co-pilot should:** Flag under-penetrated accounts, missing categories, and next-best brand stories for a dealer visit.

**Avoid:** Do not over-index on eCat user counts as proof of channel strategy.

## 3. Mid-Market Multi-Channel

Broader distribution across trade, retail, ecommerce, and contractor channels with moderate price points and simpler selling structures.

### Channel Mix Operator

**Buyer / rep context:** Buyer or rep balancing trade, retail, ecommerce, contractor, and distributor demand.

**Co-pilot should:** Prioritize clean product positioning, price clarity, availability, and channel-specific recommendations.

**Avoid:** Do not assume a single buyer type or luxury-spec conversation.

### Self-Service Reorder Buyer

**Buyer / rep context:** Account user placing repeat or fill-in orders through a portal or rep-assisted workflow.

**Co-pilot should:** Make reorder paths fast, highlight substitutions, and keep recommendations practical and availability-aware.

**Avoid:** Do not bury the user in brand narrative when they need speed and certainty.

## 4. Volume Distribution

High-volume, low-unit-price distribution where the selling motion is replenishment, commodity-adjacent assortment, or private-label/house-brand scale.

### Replenishment Buyer

**Buyer / rep context:** Buyer focused on bulk movement, stock availability, low unit economics, and reorder cadence.

**Co-pilot should:** Lead with availability, pack/quantity logic, velocity, and simple alternatives.

**Avoid:** Do not recommend high-touch design language or expensive project bundles.

### House-Brand Assortment Manager

**Buyer / rep context:** Account manager maintaining broad commodity-adjacent assortments across retailers or distributors.

**Co-pilot should:** Identify assortment gaps, high-volume winners, and low-friction substitutions.

**Avoid:** Do not confuse high AOV bulk baskets with luxury intent.

## 5. Specialty/Non-Traditional

Exception bucket for accounts that do not fit the standard manufacturer-to-dealer motion or have too little comparable data to classify confidently.

### Exception Account Operator

**Buyer / rep context:** User in an account whose eCat usage or business model does not fit standard manufacturer-to-dealer assumptions.

**Co-pilot should:** Start with account-specific facts and ask for the operating context before recommending a playbook.

**Avoid:** Do not force-fit these accounts into one of the four primary segment motions without review.

## Next Build Step

For each segment, select 3-5 representative orgs and draft concrete prompt starters, discovery questions, and recommendation guardrails. Keep those persona prompts grounded in this segment document plus account-specific evidence.
