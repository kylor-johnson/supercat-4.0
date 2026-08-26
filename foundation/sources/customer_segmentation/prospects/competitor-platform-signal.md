---
id: PROS-COMP
title: Competitor platform signal — detection method and results
version: 0.1
status: draft
date: 2026-08-25
owner: Kylor Johnson
scope: HPMKT exhibitor frame only (693 exhibitors). No sourcing beyond this frame.
depends_on: [PROS-CRIT]
---

# Competitor platform signal

## 1. What this is — and what it is not

**It is a QUALIFICATION signal.** A company running a competitor's B2B commerce platform has
self-certified every Gate-0 condition and one more:

| Gate 0 | Why the signal proves it |
|---|---|
| G0.1 manufacturer / brand owner | These platforms are sold to manufacturers, not retailers |
| G0.2 indirect channel exists | The deployment is a dealer/rep ordering portal |
| G0.3 catalog complexity | Nobody buys a B2B catalog platform for a 20-SKU line |
| G0.4 size band | Implied by willingness to license, though not directly evidenced |
| **+ willingness to pay** | **Already paying for this exact category, today** |

**It is NOT a segment signal.** It says nothing about selling motion. It does not predict SEG-01
vs SEG-02 vs SEG-03, it does not rescue Layer B, and it **must not be folded into the archetypes**.
Layer B's 33.3%-vs-34.5% result stands untouched. This signal answers *"is this a SuperCat
prospect?"* — never *"which segment is it?"*

Operationally it also changes the *motion*: displacement, not greenfield.

---

## 2. Detection method

**What is matched.** The platform's own hostname in page source, not a bare brand token:

```
(?:https?://|//|\.)(?:[a-z0-9-]+\.)?amptab\.com   |  powered by amptab  |  built by amptab
(?:https?://|//|\.)(?:[a-z0-9-]+\.)?wizcommerce\.com
… same shape for repzio.com, pepperi.com, markettime.com, brandwise.(com|net), joor.com,
  nuorder.com, supercatsolutions.com
```

**Where it appears.** All 14 true positives are in `src`/`href` attributes — three shapes:

1. **Dealer-login link** pointing at the platform: `href="https://cms.amptab.com/Manufacturer/12882/Shop2"` (Barcalounger), `href="http://cms.amptab.com"` (Parker House).
2. **Build attribution** in a meta tag: `<meta name="author" content="Website built by amptab.com">` (Albany Industries, Coast Lamp, La Vida Abode, Legends Home, Nest Home Collections).
3. **Footer credit**: `Powered By AMPTAB` (Delta Furniture Mfg).

WizCommerce appears as a **tenant subdomain** — `firesidelodgefurniture.wizcommerce.com`,
`woodedriver.wizcommerce.com`, `cdn.wizcommerce.com`.

**False-positive rate — measured, not estimated.** Loose token matching against strict hostname
matching over the same 437 pages:

| Platform | Loose token | Strict hostname | **False positives** |
|---|---:|---:|---:|
| **NuOrder** | 7 | **0** | **7 — all of them** |
| AmpTab | 11 | 11 | 0 |
| WizCommerce | 3 | 3 | 0 |
| JOOR | 0 | 0 | 0 |

**All 7 NuOrder "hits" were the string `"menuOrder":3` inside Wix site JSON** — `me·nuOrder`. A
bare-token scan would have reported seven fictional NuOrder installs. **Hostname matching is
mandatory; token matching is unsafe.**

**Positive control.** The same scan run for `supercatsolutions.com` returned exactly one hit —
**Furniture Classics** (`fc`), a known existing customer, via
`href="https://supercat.supercatsolutions.com/fc/e/1/login"`. The method detects a known-true
deployment, which is the only validation available without vendor data.

**Known limits.** Detects only platforms exposed on the public homepage. A deployment reached
through a login the homepage does not link, hosted on a bare custom domain, or behind a bot
challenge is invisible. **These counts are floors, not censuses.**

---

## 3. Results — full HPMKT frame

**Frame:** 693 unique HPMKT exhibitors (Upholstered Furniture + Lamp & Lighting).
**Scanned:** **437 homepages** (63%). The other 256 had no resolvable domain from a name-derived
guess, were bot-blocked, or returned a shell — recorded as UNKNOWN, not as absence.

| Platform | Detected | Notes |
|---|---:|---|
| **AmpTab** | **11** | Named direct competitor |
| **WizCommerce** | **3** | Named direct competitor |
| RepZio | 0 | Named direct competitor — none detected |
| Pepperi | 0 | Named direct competitor — none detected |
| MarketTime | 0 | Named direct competitor — none detected |
| Brandwise · JOOR · NuOrder | 0 | Adjacent platforms — none detected |
| SuperCat (control) | 1 | Furniture Classics — existing customer |

### AmpTab installs (11)

All 11 verified by manual pass, 2026-08-25 — see §3.1. **All 11 are CONFIRMED PLATFORM.**

| Company | Domain | Frame category | Verdict | Status |
|---|---|---|---|---|
| Albany Industries | albanyindustries.com | Upholstered | **CONFIRMED PLATFORM** | HubSpot MQL |
| **Barcalounger** | barcalounger.com | Upholstered | **CONFIRMED PLATFORM** | **not in HubSpot** |
| Bellona USA | bellonausa.com | Upholstered | **CONFIRMED PLATFORM** | HubSpot lead |
| **Coast Lamp Mfg** | coastlampmfg.com | Lamp & Lighting | **CONFIRMED PLATFORM** (tenant id 170782) | HubSpot lead · **the only genuine lane-3 candidate** |
| Delta Furniture Mfg | deltafurnituremfg.com | Upholstered | **CONFIRMED PLATFORM** | HubSpot lead |
| La Vida Abode | lavidaabode.com | Upholstered | **CONFIRMED PLATFORM** | HubSpot lead |
| **Legends Home** | legendshome.com | Upholstered | **CONFIRMED PLATFORM** | **not in HubSpot** |
| **Nest Home Collections** | nesthomecollections.com | Upholstered | **CONFIRMED PLATFORM** (tenant id 174882) | **not in HubSpot** |
| **Parker House Furniture** | parkerhousefurniture.com | Upholstered | **CONFIRMED PLATFORM** | **not in HubSpot** · lane-2 candidate |
| Steve Silver Company | stevesilver.com | Upholstered | **CONFIRMED PLATFORM** | HubSpot SQL |
| **Titanic Furniture** | titanicfurniture.com | Upholstered | **CONFIRMED PLATFORM** | **not in HubSpot** |

### 3.1 Disambiguation pass — build attribution vs deployed platform

An earlier draft of this file cautioned that 5 of the 11 were detected only via
`<meta name="author" content="Website built by amptab.com">`, and that AmpTab might merely have
built the marketing site. **That caution was wrong, and the manual pass settles it.**

All five — Albany Industries, Coast Lamp Mfg, La Vida Abode, Legends Home, Nest Home Collections —
carry **both** the build-attribution meta tag **and** a dealer/B2B login pointing at the AmpTab
host `[OBSERVED 2026-08-25]`:

| Company | Dealer login target |
|---|---|
| Albany Industries | `https://cms.amptab.com` (anchor "Log In") |
| Coast Lamp Mfg | `https://cms.amptab.com/Manufacturer/170782/Shop2` |
| La Vida Abode | `https://cms.amptab.com` (anchor "Log In") |
| Legends Home | `https://cms.amptab.com` (anchor "Log In") |
| Nest Home Collections | `https://cms.amptab.com/Manufacturer/174882/shop` |

Two carry a **per-tenant manufacturer ID in the path** (170782, 174882) — a provisioned instance,
not a template. **Build attribution and deployment co-occur in every case observed**, which makes
sense: AmpTab appears to build the marketing site *and* host the dealer portal as one engagement.

**Net: 11 of 11 confirmed, 0 build-attribution-only.** File closed — no further sourcing.

### WizCommerce installs (3)

| Company | Domain | Frame category | Status |
|---|---|---|---|
| Big House Fabrics | bighousefabrics.com | Upholstered | Gate-0 fail (fabric supplier) |
| Fireside Lodge Furniture | firesidelodgefurniture.com | Upholstered | HubSpot MQL |
| Sagebrook Home | sagebrookhome.com | Lamp & Lighting | not in HubSpot |

---

## 4. What the result says

**AmpTab is the incumbent to displace in this frame, by a wide margin** — 11 of 14 detected
installs, and the only competitor with a visible presence at High Point. RepZio, Pepperi and
MarketTime detected **zero** installs across 437 exhibitor homepages. That is a floor, not proof of
absence, but it is a meaningfully different competitive picture from the five-competitor set in
`foundation/04_market_and_competitors.md`, where AmpTab is one name among several.

**Five of 14 are not in HubSpot at all** — Barcalounger, Legends Home, Nest Home Collections,
Parker House, Titanic Furniture. Against a ~17% fresh rate for the frame overall, that is a better
yield from a cheaper signal than the entire lane-criteria screen produced.

**All 11 AmpTab hits are confirmed deployments** (§3.1). The build-attribution caveat raised in an
earlier draft did not survive checking: every one of the five attribution-only hits also carries a
dealer login on the AmpTab host, two with per-tenant manufacturer IDs. There is no
build-attribution-only tier in this data.

---

## 5. Scope

**One pass, complete.** Run only over the existing 693-exhibitor HPMKT frame using pages already
fetched. No sourcing beyond the frame.

**What a broader pass would take**, if you scope one later: the binding constraint is not detection
— it is **domain resolution**. 256 of 693 exhibitors (37%) have no page scanned because a
name-derived domain guess failed. Closing that gap needs a real domain source per company rather
than a guess. Detection itself is cheap and already built; roughly a day of work to resolve domains
across a larger frame and re-run, plus the dealer-login-vs-build-credit disambiguation above.
