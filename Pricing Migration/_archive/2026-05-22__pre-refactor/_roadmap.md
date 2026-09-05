# Pricing Migration — Roadmap
*Last updated: 2026-05-20*

---

## ✅ Done

### Good-News Notice
Template built. 4 accounts drafted: dccl, jyc, pf, rw.

### Format A — 60-Day Notice
All 15 accounts drafted 2026-05-19. Math verified on all 15.
Completed: kal, sbmh, ah, abol, bp, etl, kii, lpf, lss, mh, ril, soi, swc, ufi, wwjc
Open flags: abol/bp data accuracy (Angie — verify before send), kii Annual contract (confirm renewal date), ufi/wwjc ⚠️ support fire (flagged in routing block; operator decides timing), soi bundle_config_mismatch.

### Format B — Notice + Meeting Offer
All 19 accounts drafted 2026-05-19. Math verified on all 19.
Completed: cci, gl, ih, afx, bri, bsc, df, fal, fc, gblx, heb, hf, mli, ol, rf, sca, uhc, vl, yw
Open flags: yw Finance sign-off required (special_arrangement driver — confirm before send), gblx Postgres fallback used.
Note: afx is Watch-band — do not send without health check-in confirmation.

### CEO Letter — Format B, CEO-signed
Templates, delivery email, and Postgres-integrated agent prompt built. All 9 accounts drafted.
Completed: hfg, da, fsf, vic, ali, mlc, all, am, shl
Note: shl ⚠️ support fire (39 days open) — flagged in routing block and delivery email; production-ready; operator decides send timing. Billing entity = Progressive Lighting.
Note: mlc value anchor omitted — operator decision pending (see _current-state.md).

---

## Build Queue

### Format C — Expansion/Upgrade Notice
**Priority:** Medium — not needed until wave 1 migration responses come in.
The Job 2 document. Strictly separate from the migration notice. For accounts with T1→T2 or T2→T3 upgrade eligibility.
**Hard constraint:** Never send Format C simultaneously with or before a migration notice. Only after confirmed positive migration signal (no cancellation, no pushback within 30 days of notice).
Note: pf and dccl in Good News tier are flagged `EXPANSION` — route Format C when positive signal received.

### CEO Pre-Call Accounts — 9 notices not yet drafted
delta ≥$600: arl, clc, clm, el, eli, gcl, kll, sarreid, wag.
These use the same Format B framework. Notices drafted once ready to engage.

### HOLD Accounts — 51 accounts pending
Entity-gated, Watch-band, Annual-contract, and VD-override accounts. See routing CSV (`migration_comm_tiers_2026-05-19.csv`) and `_master-account-data-v6.2.csv` for per-account status and comm format assignment. Draft notices once accounts are unblocked.

---

## Future

### Format C Agent Prompt
Once Format C template is built, needs the same Postgres-integrated agent prompt as Format A, B, and CEO Letter.
