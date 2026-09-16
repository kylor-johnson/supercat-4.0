# Q-03: Behavioral Funnel Gap Analysis
- **Query ID**: Q-03 (VM-03)
- **Org**: RENWIL (rw, org_id=248)
- **Description**: Derived from Q-01 dimensional scores. For each selling rep (submit_order > 5), funnel ratios computed across behavioral dimensions.
- **Row count**: 49
- **Run date**: 2026-04-16
- **Derivation notes**:
  - Qualifying gate: submit_order > 5 in Q-01 Step 1
  - R1 (PD / CT): computable for 49/49 reps (all have CT > 0); bottom-quartile threshold (Q1) = 0.750; gap benchmark < 3:1
  - R2 (CB / PD): computable for 49/49 reps (all have PD > 0); bottom-quartile threshold (Q1) = 0.198; gap benchmark < 0.1
  - R3 (Pres / CB): computable for 48/49 reps (walfab_central has CB=0 → R3 N/A); bottom-quartile threshold (Q1) = 0.0008; gap benchmark < 0.1
  - R4 (SO / Pres): computable for 36/49 reps (13 reps have Pres=0 → R4 N/A); bottom-quartile threshold (Q1) = 2.418
  - **Structural org gap — Presentation**: 13 of 49 reps (27%) have presentation=0 (complete bypass of presentation tools). This inflates R3 bottom-quartile membership and makes R4 non-computable for those reps. Presentation bypass is an org-wide structural pattern, not solely a per-rep gap.
  - **Structural org gap — R1 (CT → PD)**: 46 of 49 reps (94%) fall below the 3:1 benchmark for R1. Only 3 reps exceed 3:1 (Roxanna Page at 3.29, Marie Andersen at 3.20, Lance Bissell at 3.05). This indicates an org-wide Customer Targeting → Product Discovery conversion pattern, not isolated rep behavior.
  - "Test Sales Portal" excluded per showroom_scan_results.md (submit_order ≤ 2 in Mixpanel; does not qualify)
  - "torontoshowroom" included (flagged for CSM review); remains in funnel analysis
  - "renwil" internal account included in funnel analysis

## Bottom-Quartile Thresholds

| Ratio | Definition | Bottom Q1 | Gap Benchmark | Computable (n) |
|-------|-----------|-----------|---------------|----------------|
| R1 | product_discovery / customer_targeting | 0.750 | < 3:1 | 49 |
| R2 | config_bundling / product_discovery | 0.198 | < 0.1 | 49 |
| R3 | presentation / config_bundling | 0.0008 | < 0.1 | 48 |
| R4 | submit_order / presentation | 2.418 | disproportionately low | 36 |

## Funnel Ratio Table

| Rep | R1 (CT→PD) | R2 (PD→Config) | R3 (Config→Pres) | R4 (Pres→Orders) | Flagged Gaps |
|-----|-----------|----------------|------------------|-------------------|--------------|
| Sandra Nash Braden | 1.44 | 0.321 | 0.0086 | 107.90 | R1<3:1; R3<0.1 |
| Louise Presseau | 1.35 | 0.328 | 0.0140 | 46.55 | R1<3:1; R3<0.1 |
| torontoshowroom | 0.87 | 0.645 | 0.0029 | 138.60 | R1<3:1; R3<0.1 |
| Penny Gould | 2.06 | 0.381 | 0.0155 | 53.82 | R1<3:1; R3<0.1 |
| Roxanne Toledo | 0.02 | 11.172 | 0.0010 | 576.00 | R1<Q1; R1<3:1; R3<0.1 |
| Rob Trottier | 1.56 | 0.412 | 0.0543 | 9.14 | R1<3:1; R3<0.1 |
| Paul deBellefeuille | 0.54 | 0.289 | 0.0478 | 20.33 | R1<Q1; R1<3:1; R3<0.1 |
| Cindy Smethurst | 1.32 | 0.704 | 0.0000 | N/A | R1<3:1; R3<Q1; R3<0.1; pres bypassed |
| Randy Gould | 1.50 | 0.265 | 0.0348 | 34.50 | R1<3:1; R3<0.1 |
| Roxanna Page | 3.29 | 0.258 | 0.0612 | 12.44 | R3<0.1 |
| Amy Reiman | 1.04 | 0.501 | 0.0000 | N/A | R1<3:1; R3<Q1; R3<0.1; pres bypassed |
| Marc Gilbert | 0.23 | 1.446 | 0.0646 | 6.56 | R1<Q1; R1<3:1; R3<0.1 |
| Samantha Murray | 1.89 | 0.169 | 0.4305 | 2.45 | R1<3:1; R2<Q1 |
| John Fraser | 3.04 | 0.325 | 0.1462 | 2.45 | — |
| Tanner Gould | 1.49 | 0.333 | 0.0506 | 11.75 | R1<3:1; R3<0.1 |
| Sandy Gerlock | 1.60 | 0.455 | 0.0115 | 27.60 | R1<3:1; R3<0.1 |
| Tim Matchunis | 0.99 | 0.350 | 0.0048 | 132.00 | R1<3:1; R3<0.1 |
| Neil Wasserman | 1.07 | 0.195 | 0.0280 | 20.17 | R1<3:1; R2<Q1; R3<0.1 |
| Jesse Gerber | 0.30 | 0.059 | 0.1429 | 56.00 | R1<Q1; R1<3:1; R2<Q1; R2<0.1 |
| Larry Gerber | 0.23 | 0.678 | 0.0000 | N/A | R1<Q1; R1<3:1; R3<Q1; R3<0.1; pres bypassed |
| Mandana Saxton | 1.73 | 0.363 | 0.0000 | N/A | R1<3:1; R3<Q1; R3<0.1; pres bypassed |
| Jean Beaulieu | 0.95 | 2.060 | 0.0390 | 4.55 | R1<3:1; R3<0.1 |
| Ted Dufresne | 2.41 | 0.294 | 0.0195 | 28.67 | R1<3:1; R3<0.1 |
| Denise Fraley | 0.35 | 0.353 | 0.2531 | 0.98 | R1<Q1; R1<3:1; R4<Q1 |
| Theresa Hackett | 1.28 | 0.273 | 0.1333 | 2.69 | R1<3:1 |
| The Walfab Company | 0.64 | 0.000 | N/A | N/A | R1<Q1; R1<3:1; R2<Q1; R2<0.1; pres bypassed; config=0 |
| Marie Andersen | 3.20 | 0.339 | 0.0042 | 61.00 | R3<0.1 |
| Tami Gleason | 0.87 | 0.100 | 0.0000 | N/A | R1<3:1; R2<Q1; R3<Q1; R3<0.1; pres bypassed |
| Dennis Grant | 1.16 | 0.225 | 0.9556 | 1.12 | R1<3:1; R4<Q1 |
| Suzanne Hogan | 1.91 | 0.198 | 0.5158 | 0.41 | R1<3:1; R4<Q1 |
| Melissa Klinger | 0.30 | 0.829 | 0.0426 | 7.83 | R1<Q1; R1<3:1; R3<0.1 |
| Dan Ewing | 1.28 | 0.115 | 0.5405 | 1.10 | R1<3:1; R2<Q1; R4<Q1 |
| renwil | 0.91 | 0.231 | 0.1688 | 2.69 | R1<3:1 |
| Ben Bonardelli | 0.87 | 0.529 | 0.0091 | 35.00 | R1<3:1; R3<0.1 |
| Brandon Kraese | 1.63 | 0.458 | 0.0865 | 3.44 | R1<3:1; R3<0.1 |
| Seth Neumann | 1.19 | 0.254 | 0.0000 | N/A | R1<3:1; R3<Q1; R3<0.1; pres bypassed |
| Patty Jesse | 1.60 | 0.391 | 0.0855 | 2.15 | R1<3:1; R3<0.1; R4<Q1 |
| Haris Baig | 0.76 | 0.099 | 0.4857 | 1.47 | R1<3:1; R2<Q1; R2<0.1; R4<Q1 |
| Lori Funk | 0.26 | 0.408 | 0.0000 | N/A | R1<Q1; R1<3:1; R3<Q1; R3<0.1; pres bypassed |
| Cheryl Gross | 0.53 | 0.250 | 0.0000 | N/A | R1<Q1; R1<3:1; R3<Q1; R3<0.1; pres bypassed |
| Anna Cowan | 0.75 | 0.467 | 0.0238 | 7.00 | R1<3:1; R3<0.1 |
| Joshua Jastal | 0.31 | 0.176 | 0.0000 | N/A | R1<Q1; R1<3:1; R2<Q1; R3<Q1; R3<0.1; pres bypassed |
| Michael Estrin | 0.84 | 0.162 | 0.0000 | N/A | R1<3:1; R2<Q1; R3<Q1; R3<0.1; pres bypassed |
| Jimmilea King | 0.64 | 1.286 | 0.1270 | 0.81 | R1<Q1; R1<3:1; R4<Q1 |
| Wendy Buzzard | 1.49 | 0.115 | 0.3750 | 1.33 | R1<3:1; R2<Q1; R4<Q1 |
| Lance Bissell | 3.05 | 0.078 | 0.2000 | 12.00 | R2<Q1; R2<0.1 |
| Judy Embury | 0.97 | 0.034 | 0.0000 | N/A | R1<3:1; R2<Q1; R2<0.1; R3<Q1; R3<0.1; pres bypassed |
| Katherine Hare | 0.79 | 0.231 | 0.0000 | N/A | R1<3:1; R3<Q1; R3<0.1; pres bypassed |
| Jeannette Grude | 1.05 | 0.846 | 0.0909 | 2.33 | R1<3:1; R3<0.1; R4<Q1 |
