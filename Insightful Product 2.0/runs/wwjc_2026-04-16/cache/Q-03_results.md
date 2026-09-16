# Q-03: Behavioral Funnel Gap Analysis
- **Query ID**: Q-03 (VM-03)
- **Org**: Wildwood/Chelsea House (wwjc, org_id=8)
- **Description**: Derived from Q-01 dimensional scores. For each selling rep (submit_order > 5), funnel ratios computed across behavioral dimensions.
- **Row count**: 32
- **Run date**: 2026-04-16
- **Derivation notes**: Ratio 1 (CT→PD) = N/A for all reps — customer_targeting unavailable (field split in source report). Ratio 2 (PD→Config) = 0.00 for all reps — config_bundling = 0 org-wide (CPQ/kits not used); this is a structural org gap, not a per-rep gap. Ratio 3 (Config→Pres) = N/A for all reps — division by zero (config_bundling = 0). Ratio 4 (Pres→Orders) is the only computable ratio. Bottom-quartile threshold for R4 ≈ 0.74 (n=27 computable values). Reps with presentation=0 flagged separately as "pres bypassed."

| Rep | R1 (CT→PD) | R2 (PD→Config) | R3 (Config→Pres) | R4 (Pres→Orders) | Flagged Gaps |
|-----|-----------|----------------|-----------------|------------------|--------------|
| Daniel Ratchford (dratchford) | N/A | 0.00 | N/A | 10.85 | None (computable) |
| Tammy Preusse (tpreusse) | N/A | 0.00 | N/A | 14.75 | None (computable) |
| Roger Miles (rmiles2) | N/A | 0.00 | N/A | 8.50 | None (computable) |
| Marilee Ambro (mambro2) | N/A | 0.00 | N/A | 4.00 | None (computable) |
| Erica Stein (estein) | N/A | 0.00 | N/A | 1.16 | None (computable) |
| Pam Cain (pcain) | N/A | 0.00 | N/A | 0.13 | R4: bottom-quartile (high pres 86 vs 11 orders) |
| Christy Nein (cnein) | N/A | 0.00 | N/A | 1.39 | None (computable) |
| Luke & Brandi Gillis (lbgillis3) | N/A | 0.00 | N/A | 0.57 | R4: bottom-quartile (pres 86 vs 49 orders) |
| Mark Horne (mark) | N/A | 0.00 | N/A | 0.38 | R4: bottom-quartile (pres 113 vs 43 orders) |
| Whit Barnes (wbarnes) | N/A | 0.00 | N/A | 0.32 | R4: bottom-quartile (pres 100 vs 32 orders) |
| Bill Minchew (bminchew) | N/A | 0.00 | N/A | 8.33 | None (computable) |
| Gigi Lane (gigilane) | N/A | 0.00 | N/A | 0.79 | None (computable) |
| Katherine McMullan (katherinemcmullan) | N/A | 0.00 | N/A | 108.00 | None (computable) |
| Janice Roetman (jroetman) | N/A | 0.00 | N/A | N/A (pres=0) | R4: pres bypassed (34 orders, 0 presentations) |
| Lorne Gardner (lornegardner) | N/A | 0.00 | N/A | 10.00 | None (computable) |
| Stan Barris (sbarris) | N/A | 0.00 | N/A | 12.00 | None (computable) |
| Jason Stein (jstein) | N/A | 0.00 | N/A | 1.67 | None (computable) |
| Madeline Cole (mcole1) | N/A | 0.00 | N/A | 0.84 | None (computable) |
| Glenn Fritzmeyer (gf) | N/A | 0.00 | N/A | 3.80 | None (computable) |
| Seth Neumann (seth) | N/A | 0.00 | N/A | N/A (pres=0) | R4: pres bypassed (15 orders, 0 presentations) |
| Michael & Beverly Best (teambest) | N/A | 0.00 | N/A | 3.78 | None (computable) |
| Tamara Rachel (rachelt) | N/A | 0.00 | N/A | 2.38 | None (computable) |
| Ryan McWilliams (ryan) | N/A | 0.00 | N/A | 0.12 | R4: bottom-quartile (pres 59 vs 7 orders) |
| Flavia Oliveira (foliveira) | N/A | 0.00 | N/A | N/A (pres=0) | R4: pres bypassed (7 orders, 0 presentations) |
| jgerber | N/A | 0.00 | N/A | 4.83 | None (computable) |
| Nate McElwee (nmcelwee) | N/A | 0.00 | N/A | 24.00 | None (computable) |
| Krissa DeGennaro Newell (kdnewell) | N/A | 0.00 | N/A | 1.00 | None (computable) |
| Sheryl Watts (watts) | N/A | 0.00 | N/A | 2.50 | None (computable) |
| Hannah Hoxworth (hhoxworth) | N/A | 0.00 | N/A | 4.50 | None (computable) |
| Weezie Ward (weezieward) | N/A | 0.00 | N/A | 0.43 | R4: bottom-quartile (pres 23 vs 10 orders) |
| Atlanta Showroom (atlantashowroom) | N/A | 0.00 | N/A | N/A (pres=0) | R4: pres bypassed (41 orders, 0 presentations) |
| Jensen Meier (jensen) | N/A | 0.00 | N/A | N/A (pres=0) | R4: pres bypassed (10 orders, 0 presentations) |

**Flag Summary**:
| Flag Type | Count | Reps |
|-----------|-------|------|
| R4: bottom-quartile (≤ 0.74) | 6 | pcain, lbgillis3, mark, wbarnes, ryan, weezieward |
| R4: pres bypassed (pres=0) | 5 | jroetman, seth, foliveira, atlantashowroom, jensen |
| R2: org-wide structural gap | 32 | All reps (config_bundling = 0) |
| R1, R3: data unavailable | 32 | All reps (customer_targeting split; config_bundling = 0) |
