# Q-02: Selling Archetype Classification
- **Query ID**: Q-02 (VM-02)
- **Org**: RENWIL (rw, org_id=248)
- **Description**: Derived from Q-01 behavioral ratios. Each rep with submit_order > 2 classified into one selling archetype.
- **Row count**: 57
- **Run date**: 2026-04-16
- **Derivation notes**:
  - Org median AOV (from Q-01 Step 2): $1,235.62
  - Presentation top-quartile threshold (Q3, n=57): ≥ 17
  - Product Discovery top-quartile threshold (Q3, n=57): ≥ 891
  - Product Discovery median (n=57): 264
  - Customer Targeting median (n=57): 335
  - Config/Order median (n=57): 1.77
  - Unique Customers median (n=54 matched): 10.5
  - Deep-Account Specialist gate: unique_customers ≤ 3 (from Step 2)
  - Precision Closer gate: PD < median (264) + Config/Order > median (1.77) + AOV > $1,606.31 (1.3× org median)
  - Curated Discovery Seller gate: Pres ≥ Q3 (17) + PD ≥ median (264) + AOV > $1,235.62; two reps classified as non-presenting variant (high PD, above-median AOV, UC ≥ 5, Pres ≤ 1)
  - Volume Relationship Seller gate: UC ≥ 5 + AOV < median (primary); extended to include above-median AOV reps with UC ≥ median and high activity
  - Non-Selling Role candidates (submit_order ≤ 2 AND total_events > 500): 0 — none routed to Q-04
  - "Test Sales Portal" excluded per showroom_scan_results.md (1 order, $313.19 — does not qualify for Q-02 with submit_order ≤ 2)
  - "torontoshowroom" included (flagged for CSM review); classified by behavioral pattern only — no Step 2 match
  - "renwil" internal account included; classified by behavioral pattern only — no Step 2 match
  - "jonv" unclassified — no Step 2 data and low behavioral activity (179 events, 4 submit_order)
  - Sheryl Lowe (#1 in Step 2 by GMV at $1,232,454.94 / 602 orders) has no Mixpanel username match in Step 1 — cannot classify without behavioral dimensions
  - "mh-dewing" tentatively matched to Dan Ewing (44 submit_order vs 42 Postgres orders; Mixpanel is all-time, Postgres is trailing 12 months)
  - "bgraham" mapped to combined B Graham (2 orders, $3,948) + B. Graham (1 order, $2,347.39) = 3 orders, $6,295.39 total GMV, ~$2,098.46 AOV

## Archetype Distribution

| Archetype | Count |
|-----------|-------|
| Curated Discovery Seller | 9 |
| Deep-Account Specialist | 16 |
| Precision Closer | 5 |
| Volume Relationship Seller | 26 |
| Unclassified (no Step 2 data) | 1 |
| **Total** | **57** |

## Classification Table

| Rep | Archetype | Key Signals |
|-----|-----------|-------------|
| Suzanne Hogan | Curated Discovery Seller | Pres=114 (≥Q3); PD=1,118; AOV=$7,117.38 |
| Dan Ewing | Curated Discovery Seller | Pres=40 (≥Q3); PD=643; AOV=$2,318.41 |
| Marie Andersen | Curated Discovery Seller | PD=697; CB=236; AOV=$2,024.93; UC=10; Pres=1 (non-presenting variant) |
| Denise Fraley | Curated Discovery Seller | Pres=82 (≥Q3); PD=917; AOV=$1,891.54 |
| Theresa Hackett | Curated Discovery Seller | Pres=26 (≥Q3); PD=714; AOV=$1,760.54 |
| John Fraser | Curated Discovery Seller | Pres=62 (≥Q3); PD=1,306; AOV=$1,747.68 |
| Paul deBellefeuille | Curated Discovery Seller | Pres=24 (≥Q3); PD=1,737; AOV=$1,564.44 |
| Mandana Saxton | Curated Discovery Seller | PD=579; CB=210; AOV=$1,527.47; UC=20; Pres=0 (non-presenting variant) |
| Marc Gilbert | Curated Discovery Seller | Pres=27 (≥Q3); PD=289; AOV=$1,317.07 |
| Wendy Buzzard | Deep-Account Specialist | UC=1; AOV=$4,599.53; CT=140; SO=12 |
| Patty Jesse | Deep-Account Specialist | UC=2; AOV=$2,795.88; CT=243; SO=28 |
| B Graham | Deep-Account Specialist | UC=1; AOV=$2,098.46; CT=67; SO=3 |
| Bill France | Deep-Account Specialist | UC=2; AOV=$1,848.01; CT=29; SO=5 |
| Jeannette Grude | Deep-Account Specialist | UC=3; AOV=$1,499.67; CT=37; SO=7 |
| Christian Dufresne | Deep-Account Specialist | UC=2; AOV=$940.60; CT=30; SO=5 |
| Seth Neumann | Deep-Account Specialist | UC=2; AOV=$905.02; CT=222; SO=30 |
| Laurie Reinhardt | Deep-Account Specialist | UC=1; AOV=$861.88; CT=45; SO=4 |
| Lance Bissell | Deep-Account Specialist | UC=3; AOV=$807.14; CT=21; SO=12 |
| Carlos Bohorquez | Deep-Account Specialist | UC=2; AOV=$797.06; CT=143; SO=4 |
| Dennis Grant | Deep-Account Specialist | UC=2; AOV=$662.29; CT=172; SO=48 |
| Kenneth & Linda Cezar | Deep-Account Specialist | UC=1; AOV=$638.50; CT=15; SO=3 |
| Katherine Hare | Deep-Account Specialist | UC=2; AOV=$607.31; CT=33; SO=8 |
| Todd Tracy | Deep-Account Specialist | UC=0; AOV=$593.69; CT=29; SO=3 |
| Judy Embury | Deep-Account Specialist | UC=1; AOV=$554.97; CT=30; SO=9 |
| Cheryl Gross | Deep-Account Specialist | UC=3; AOV=$462.54; CT=60; SO=18 |
| Jimmilea King | Precision Closer | PD=98 (<med); Config/Order=9.7; AOV=$4,794.45 |
| Jean Beaulieu | Precision Closer | PD=249 (<med); Config/Order=5.6; AOV=$2,811.71 |
| Ben Bonardelli | Precision Closer | PD=208 (<med); Config/Order=3.1; AOV=$1,958.45 |
| Brandon Kraese | Precision Closer | PD=227 (<med); Config/Order=3.4; AOV=$1,519.22 |
| Anna Cowan | Precision Closer | PD=180 (<med); Config/Order=6.0; AOV=$1,515.36 |
| Louise Presseau | Volume Relationship Seller | DA=315; UC=111; AOV=$880.24 |
| Roxanne Toledo | Volume Relationship Seller | DA=209; UC=106; AOV=$1,127.56 |
| Rob Trottier | Volume Relationship Seller | DA=256; UC=67; AOV=$931.45 |
| Cindy Smethurst | Volume Relationship Seller | DA=174; TE=7,636; UC=59; AOV=$2,050.68 |
| Sandra Nash Braden | Volume Relationship Seller | DA=300; UC=52; AOV=$606.30 |
| Sandy Gerlock | Volume Relationship Seller | DA=137; TE=2,713; UC=40; AOV=$1,493.83 |
| Neil Wasserman | Volume Relationship Seller | DA=260; TE=3,412; UC=30; AOV=$1,627.46 |
| Larry Gerber | Volume Relationship Seller | DA=90; UC=30; AOV=$477.97 |
| Amy Reiman | Volume Relationship Seller | DA=171; UC=29; AOV=$1,033.48 |
| Jesse Gerber | Volume Relationship Seller | DA=210; TE=1,739; UC=29; AOV=$1,329.82 |
| Samantha Murray | Volume Relationship Seller | DA=164; UC=23; AOV=$717.89 |
| Roxanna Page | Volume Relationship Seller | DA=202; UC=23; AOV=$1,220.22 |
| Ted Dufresne | Volume Relationship Seller | DA=146; TE=1,462; UC=22; AOV=$1,250.69 |
| The Walfab Company | Volume Relationship Seller | DA=60; UC=22; AOV=$718.95 |
| Melissa Klinger | Volume Relationship Seller | DA=76; UC=19; AOV=$852.17 |
| Tanner Gould | Volume Relationship Seller | DA=191; UC=16; AOV=$1,074.45 |
| Tim Matchunis | Volume Relationship Seller | DA=133; UC=14; AOV=$948.14 |
| Haris Baig | Volume Relationship Seller | DA=125; UC=12; AOV=$939.56 |
| Tami Gleason | Volume Relationship Seller | UC=9; AOV=$1,358.77; above-med AOV variant |
| Lori Funk | Volume Relationship Seller | DA=64; UC=8; AOV=$662.65 |
| Penny Gould | Volume Relationship Seller | DA=193; UC=7; AOV=$951.36 |
| Randy Gould | Volume Relationship Seller | DA=181; UC=7; AOV=$833.07 |
| Joshua Jastal | Volume Relationship Seller | DA=74; UC=7; AOV=$477.87 |
| Michael Estrin | Volume Relationship Seller | DA=66; UC=7; AOV=$265.52 |
| torontoshowroom | Volume Relationship Seller | DA=293; TE=9,387; behavioral pattern (no Step 2 data); CSM-flagged |
| renwil | Volume Relationship Seller | DA=122; TE=1,943; behavioral pattern (no Step 2 data); internal account |
| jonv | Unclassified (no Step 2 data) | DA=24; TE=179; AOV=N/A; UC=N/A |
