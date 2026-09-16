# Signal Detection Guide — The Surprise Pass

## Purpose

After data gathering completes (Step 1 in the run prompt), this pass:
1. Reads all cache files
2. Detects every signal defined in `authority/signal_catalog.md`
3. Scores each by `surprise_score × dollar_impact × actionability_multiplier`
4. Produces `cache/signal_rank.md` — the ranked manifest that drives section building

This replaces the 2.0 approach of "build every section comprehensively, then write executive summary." Instead: detect what matters FIRST, build sections ONLY around the strongest signals.

## Inputs

All files in `runs/{SHORTNAME}_{RUN_DATE}/cache/` produced by data_gather.py, including:
- Q-results files (all standard queries from 2.0)
- Q-ORG-* results (new org-level pattern detection queries)
- gate_flags.md
- section_manifest.md (from data_gather)

Plus: `authority/signal_catalog.md` (detection thresholds and scoring formulas)

## Output

`cache/signal_rank.md` with this exact format:

```markdown
# Signal Detection Results — {SHORTNAME} ({RUN_DATE})

## Detection Summary
- Signals scanned: [N]
- Signals fired: [M]
- P0 signals: [count]
- P1 signals: [count]
- P2 signals: [count]
- Top signal RANK score: [value]

## Ranked Signal Manifest

| Rank | Signal ID | Category | Headline | Surprise | Dollar Impact | Action Mult | SIGNAL_RANK | Section |
|------|-----------|----------|----------|----------|---------------|-------------|-------------|---------|
| 1 | SIG-DECAY-01 | Decay | Ticking Stripe — 244-day silence on $227K account | 8.1x | $227,309 | 3.0 | 5,522,783 | accounts |
| 2 | SIG-ANOMALY-02 | Anomaly | HAY-1417-AG stocked out — $20.7K LTM | 2.4x | $20,707 | 3.0 | 149,090 | product |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

## Section Signal Density

| Section | P0 Signals | P1 Signals | P2 Signals | Total RANK Sum | Render Order |
|---------|-----------|-----------|-----------|----------------|--------------|
| accounts | 4 | 3 | 2 | 6,284,000 | 1 |
| product | 2 | 2 | 1 | 891,000 | 2 |
| team | 0 | 3 | 2 | 445,000 | 3 |
| commerce | 1 | 1 | 1 | 312,000 | 4 |
| platform | 0 | 0 | 3 | 12,000 | 5 (collapsed) |

## Signal Summary Candidates (Top 7)

Pre-select the top 7 fired signals by SIGNAL_RANK descending and list them here.
Diversity and composition rules (slot caps, positive-first ordering) are applied
by the Signal Summary section guide (`section_01_signals.md`), not during detection.

1. **[Headline]** — [one-sentence context]. $[dollar figure]. → [section link]
2. ...

## Sections to SKIP (no signals AND alternate gate fails)
- [section_id]: [reason — e.g., "0 fired signals, alternate gate not met"]
```

## Detection Algorithm (per signal)

For each signal in the catalog:

### Step 0: Classify Enterprise Channel Accounts

Before running any opportunity signals, build the **Enterprise Channel exclusion set**:

1. From `portal_orders` cache, identify accounts where:
   - LTM order count >= 500
   - Lifetime eCat orders = 0
   - Org gate flag `HAS_CART = false`
2. These accounts are tagged as `ENTERPRISE_CHANNEL` and excluded from SIG-OPP-02 detection
3. Store the excluded list for rendering in the Account Intelligence "Enterprise Channel Accounts" collapsed callout
4. Typical enterprise accounts: national retailers (Home Depot, Lowe's, Wayfair), mass-market e-commerce platforms, and big-box chains that order through EDI/PO/marketplace integrations

If `HAS_CART = true`, do NOT exclude — these accounts are legitimate B2B Cart activation targets even at high volume.

### Step 1: Check gate

- Read the signal's `Data Gate` from the catalog
- Check `gate_flags.md` for the required conditions
- If gate not met, skip signal (do not score, do not include in manifest)

### Step 2: Run detection logic

- Read the cache file(s) specified by the signal's Query ID
- Apply the detection threshold (e.g., "Ratio > 2.5x AND account LTM > $10K")
- **For SIG-OPP-02**: Before checking threshold, remove all accounts in the `ENTERPRISE_CHANNEL` exclusion set
- If threshold not met, signal does not fire
- If threshold IS met, proceed to scoring

### Step 3: Compute scores

- `surprise_score`: Use the formula from the catalog (e.g., current_gap / avg_days_between)
- `dollar_impact`: Use the formula from the catalog (e.g., account LTM revenue)
- `actionability_multiplier`:
  - 3.0 = item-level + named customer + specific action available
  - 2.0 = category-level or customer-level without item specificity
  - 1.0 = general pattern without specific entity to act on
- `SIGNAL_RANK = surprise_score × dollar_impact × actionability_multiplier`

### Step 4: Generate headline

- Each fired signal produces a one-line headline following the Output Format in the catalog
- The headline MUST include: entity name, dollar figure, and the surprising metric

## Section Ordering

Section positions are FIXED. Signal density does NOT determine section position.

Signal density (P0/P1/P2 counts and RANK sum per section) is computed and saved
in `signal_rank.md` for two purposes only:
1. **Signal Summary candidate selection** — the top 7 signals across all sections
2. **Section render gates** — a section renders if it has ≥ 1 P0/P1 signal OR its alternate include gate passes

The fixed render order is defined in `run_prompt.md` Step 4.

## Account Intelligence: Top 10 Selection

The Account Intelligence section needs to identify which accounts get mini-briefs:
1. Collect all account-level signals (SIG-DECAY-01, SIG-DECAY-02, SIG-DECAY-04, SIG-ANOMALY-03, SIG-OPP-01, SIG-OPP-02, SIG-OPP-03, SIG-MOM-01, SIG-RISK-02)
2. Group by customer
3. For each customer, sum SIGNAL_RANK across all fired signals
4. Rank customers by total signal density
5. Top 10 get mini-briefs (top 5 rendered, 6-10 collapsed)
6. Save to `cache/top_accounts.md`

## Validation Checklist

Before proceeding to section building, verify:
- [ ] `signal_rank.md` exists and has > 0 fired signals
- [ ] At least 1 section has >= 1 P0/P1 signal or passes its alternate gate (otherwise report is Mode 2/3)
- [ ] Section ordering is determined and saved
- [ ] Top 10 accounts for mini-briefs are identified
- [ ] Signal Summary candidates (top 7) are pre-selected

## Edge Cases

- **Zero signals fire**: This means the org's data is too sparse or too stable for signal detection. Fall back to Mode 2 (Platform Activation) regardless of commerce history.
- **All signals in one section**: Render that section prominently, others lean. The report is ALLOWED to be dominated by one section if that's where the intelligence lives.
- **Same entity in multiple signals**: Deduplicate in rendering but count each signal separately for ranking. E.g., if Ticking Stripe fires SIG-DECAY-01 AND SIG-RISK-02, both count toward account intelligence signal density, but the mini-brief only mentions the dormancy once.
