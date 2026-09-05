# v4.0 archive (2026-07-09)

> **Correction (2026-07-09, later same day):** this folder's name says "archive," but the final
> pass done here — three-axis enrichment (how/what/who they sell) tested against every Postgres
> dimension for all 109 orgs — is what Kjael actually reviewed and **stamped**. It supersedes the
> `v4.1` handoff below, which was written *before* this pass and assumed v4.0 was insufficient.
> **This is the current baseline.** Copies of the stamped deliverables live in
> `Customer Segmentation/current/`; treat those (with the unmatched-account errata applied) as
> canonical. Folder is kept named `v4.0_archive` for path stability — do not read the name as
> "deprecated."

Contents:

- `SuperCat_Client_Segmentation_v4.0.md` — stamped analysis (header note explains 2 rounds of post-stamp correction; body preserved as-stamped)
- `SuperCat_Customer_Segmentation_v4.0_MASTER.csv` — corrected roster, 109 rows (matches the as-stamped count; the Gabriella White / Summer Classics identity fix is baked in — see the validation doc)
- `unmatched_accounts_validation_2026-07-09.md` — the `??`-account resolution AND the deeper Gabriella White/Summer Classics parent-family identity fix (2 rounds; task D of the propagation handoff)
- `build_v4.py` — reproducible build script; identity fixes now applied via `SHORTNAME_CORRECTIONS` (not hand-patched), and enrichment medians computed programmatically via `compute_enrichment_medians()`
- Salvage from earlier passes: `fms`/`shl` AOV corrections, T12M order counts, segment prose / HTML builder reference

**Do not treat `../handoffs/segmentation_v4.1_handoff.md` as the active plan** — it is stale (see
`current/README.md` for the full timeline). If a genuine re-validation is wanted later, start from
this stamped v4.0, not from v3.2.
)
