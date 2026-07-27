# CopperSmith (tcs) — Admin Pre-flight (Tuesday)

Verified via Postgres org 291 on 2026-06-12.

## Done — no action needed

| Item | Status |
|------|--------|
| Option Types (8 labels) | Verified: Finish (Required), Wall Mount, Wall Mount Accessories, Ceiling Mount, Post & Pier Mount, Decorative, Electric, Gas |
| Taxonomies import | Clean import 2026-06-12; 2 TN, 48 COL, 2 groups, 10 categories |
| Custom fields (filter/display) | Genre, Subcategory, GasElectricDual, Installation, TurtleFriendly, Materials-adjacent fields all registered + send_to_ipad |

## Manual Admin action required (Kylor — ~5 min)

**Tools → Company Settings → eCat App Behavior** (or org eCat behavior page):

1. Enable **Drill Down Left-Nav Collections** — so sidebar shows TN1 CopperSmith | TN2 Biltmore → family collections
2. Enable **Drill Down Left-Nav Categories** — so Product Types drills OL → Gas Lanterns / Electric / etc. and ACC → accessory sub-types

Live DB flags currently `false` for both.

## Optional (post-Tuesday)

- Register custom field `ShortDescription` if marketing one-liner should display separately from LongDesc (REVIEW item 4)
- Register `FixtureSubType` when Jordan confirms column H label for sidebar filtering
- Register **Feature1–Feature6** and **ProductTags** (only net-new product columns from source sync)
