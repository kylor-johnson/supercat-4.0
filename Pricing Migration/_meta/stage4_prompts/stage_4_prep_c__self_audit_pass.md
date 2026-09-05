# Stage 4 Prep — Source-fix Session C: Self-audit pass per Appendix B.6.2 drift watchlist (12 pre-populated + 3 mid-session-surfaced findings; verify + extend + surface via AskQuestion)

> **For paste into a fresh Cursor agent chat as the first message.** Do not modify before pasting.
> **Drafted**: 2026-05-26 by Stage 4 planning agent (post-Stage-4.2 cohort iter 3 closeout) per operator stamp `audit_via_dedicated_session` 2026-05-26 on Action-3 sequencing AskQuestion.
> **Output target**: SURFACING ONLY — no source-file edits applied this session. This session produces a triaged-findings AskQuestion bundle for the operator to stamp; the planning agent that returns next session applies the operator-stamped trims to the source files per `_root/CONTRACTS.md §3` rule-change protocol.
> **Estimated authored length**: ~20–80 line conformance block + AskQuestion bundle (no rule-layer edits this session). Light-touch by design — the audit is calibration, not modification.
> **Dependency**: Stage 4.2 cohort iter 3 CLOSED 2026-05-26 (sca brief 137 + delivery email 47 APPROVED as-drafted as 2nd Format B production proof + 1st post-CL-027 reduction-direction sub-block production exercise). CL-028 RESOLVED at `_root/07 §4.5` source 2026-05-26 (drift watchlist finding 13 closed). Stage 4 prep Sessions A + B + Stage 4.1 + 4.2 (cci + sca) all CLOSED. All paste-ready inheritance through Stage 4.2 sca v2 (885 lines) operator-stamped. CL-024 strict + paste-verification discipline operator-stamped 2026-05-26 — **applies to this session in full**.

---

## You are a fresh agent

You have no prior context about the SuperCat Pricing Migration. That is **load-bearing** for this prompt. You are running the planning-agent self-audit pass per `_meta/stage4_prompts/PLANNING_AGENT_HANDOFF.md` Appendix B.6.2 drift watchlist. Your job is verification + triage + surfacing — NOT modification. **You do not silently edit any source file.** Every proposed trim lands via an `AskQuestion` for operator stamp; the next planning-agent session applies the operator-stamped trims per `_root/CONTRACTS.md §3`.

This is **calibration work** in the operator's "tight, not bloated" standing standard. The prior 5 source-fix sessions (Stage 4 prep Sessions A + B, Stage 4.1 lpf closeout, Stage 4.2 cohort iters 1 + 2 + 3 with CL-023 / CL-026 / CL-027 / CL-028 source-fixes) made rule-layer additions; this session pressure-tests those additions for drift artifacts (debug language, stale numbers, bloat, convention-inconsistency) and surfaces a triaged fix list.

**You will not invent new rules.** Every potential trim is either subtractive (cut conversational language; cut bloat) or replacing (point to authoritative source instead of restating). **Cleanups are SUBTRACTIVE or REPLACING, never ADDITIVE.** Per `_meta/stage4_prompts/PLANNING_AGENT_HANDOFF.md` Appendix B.6.3 guardrail 3: if your proposed cleanup adds 200 lines of clarification, the cure is worse than the disease.

**You will time-box this audit to ONE session.** If you spot >15 verified findings (beyond the 15 pre-populated below) during your verification pass, surface to operator: continue THIS session OR defer the additional surfacings to a follow-on hygiene pass.

---

## Step 1: Required reading (in this exact order) — STRICT MANIFEST-ECHO + PASTE-VERIFICATION CONTRACT

**Reading file mtimes is NOT the manifest echo.** The manifest echo requires reading `_root/00_manifest.md §2` table AND reading every `_root/` doc's header block AND echoing each doc's title + Last-updated date from the header in your first chat response. **A pre-existing artifact in the workspace (e.g. a prior session's audit output, a Stage 4 paste-ready, the handoff doc itself) is NOT a substitute for re-reading the canonical rule layer.**

If you cannot produce the canonical manifest echo, your session is not ready to audit; STOP and flag per `_root/CONTRACTS.md §2`.

**This is the CL-024 strict + paste-verification protocol** (operator-stamped 2026-05-26; 4 catches within Stage 4 to date — Stage 3.5 Thesis + Stage 4.2 bri + Stage 4.2 sca v1 + Stage 4.2 sca v2 audit→CL-028). The audit session is heavy-leverage planning-agent work — drift in the audit propagates to every Stage 4 + Stage 5 future session.

**Additionally — paste-verification requirement (CL-024)**: in your conformance block, you must paste-quote the FULL TEXT of the following operator-stamped source passages, verbatim from the source files (not paraphrased, not summarized, not just cited):

1. `_meta/stage4_prompts/PLANNING_AGENT_HANDOFF.md` Appendix **B.6.1** — the three lessons (Lesson 1 + 2 + 3) verbatim.
2. `_meta/stage4_prompts/PLANNING_AGENT_HANDOFF.md` Appendix **B.6.2** — the 12-row drift watchlist table verbatim (every cell including "Source location" + "Type" + "Prior agent's note" + "Verify by" columns).
3. `_meta/stage4_prompts/PLANNING_AGENT_HANDOFF.md` Appendix **B.6.3** — the 5-rule guardrail list verbatim.
4. `_meta/stage3_cleanup.md` **CL-028 entry** — the entire entry verbatim (Source / Fix applied / Status). This is your verification baseline for finding 13 (CL-028 RESOLVED) confirmation.
5. `_root/07 §4.5` post-CL-028 prose (line 246 area + the resolution parenthetical immediately below) — the full text including the AND-discipline tightening + CL-028 closing parenthetical.

If you cannot paste-quote any of these passages because the source text is not present at the cited location, STOP and flag per QB-125 propagation-failure rule. Do NOT proceed to verification.

### Folder orientation (mandatory — echo in conformance block per `_root/00_manifest.md §6`)

1. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/AGENTS.md`
2. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/00_README.md`
3. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/00_manifest.md` — the index. **The §2 manifest table is the authoritative list of every `_root/` doc; you echo it in your first chat response per the manifest-echo contract in §1 step 6. ALL ENTRIES, NOT A SUBSET.** Particularly for this session: read row 0 self-row + row 5 (`_root/05`) + row 7 (`_root/07`) + row 9 (`_root/09`) cell annotations in full — these are the targets of findings 4 + 5 (cell-bloat verification).
4. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/CONTRACTS.md`
5. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/09_changelog.md` — read every 2026-05-22 entry + every 2026-05-26 entry. Particularly important for this session:
    - Wave 1 (`_root/04` initial authoring 2026-05-22) — baseline convention for §2 / §3 / §4 / §6 structure.
    - All 2026-05-26 entries — the source-fix series whose by-products are the audit targets.
    - CL-027 + CL-028 RESOLVED entries — most recent source-fixes; finding 13 verification baseline.

### The rule layer — read in FULL

6. `_root/01_why_we_are_migrating.md` — read for orientation.
7. `_root/02_who_is_being_migrated.md` — read for orientation.
8. `_root/03_what_we_sell.md` — read for orientation.
9. `_root/04_communication_posture.md` — read in FULL. Target sub-sections for this audit:
    - **§3 (32-row forbidden-phrase table)** — verify row count matches manifest's "32-row" claim; verify no Stage-4-prep-Session-A row drift.
    - **§4.11 "How This Compares"** — finding 14 (3rd-consecutive-omission lockdown candidate) reads §4.11 prose to determine whether the OMISSION pattern (lpf + cci + sca = 3 consecutive) should be codified as default-omit at template scope.
    - **§4.2 "Lede stat guardrail"** — finding 15 (lede health-data extension candidate) reads §4.2 to determine whether the 4-component health translation could be added as a 4th-stat variant.
    - **§4.15 + §4.16** — the most recent source-fix additions; verify no drift.
10. `_root/05_driver_taxonomy.md` — read in FULL. Target sub-sections for this audit:
    - **§2.1.2 (post-CL-027 reduction-direction sub-block)** — verify mutual-exclusivity-rule prose is clean (finding 8 verification).
    - **§2.1.3 (CEO Letter URN canonical block, pre-existing reduction sub-block since CL-012 RESOLVED)** — finding 8 verification: does §2.1.3 carry the SAME explicit mutual-exclusivity rule that CL-027 added to §2.1.2? Or is §2.1.3's mutual-exclusivity implicit (asymmetric to §2.1.2's now-explicit codification)?
    - **§2.4.1 (CL-027-edited paragraph enumerating "TBI primary + IUR-secondary (9 accounts)")** — finding 1 verification: paragraph carries "Wait — `bcf` was re-stamped TBI→URN in the next iteration of joint resolution; not in this TBI cohort." Read carefully — is the "Wait —" a debug-language artifact or a load-bearing clarification?
    - **§2.4.7 (CL-027-edited cross-reference paragraph)** — finding 2 verification: parallel debug-language artifact to finding 1.
    - **§4 weaving matrix** — finding 9 verification (IUR-(none) row count "21" reconcile) + finding 10 verification (aggregate occurrence "83" + reconcile to 107 pending).
11. `_root/06_format_routing.md` — read for orientation.
12. `_root/07_data_pipeline.md` — read in FULL. Target sub-sections for this audit:
    - **§4.5 (post-CL-028 prose tightening)** — finding 13 verification (RESOLVED): verify the AND-discipline tightening landed at line 246 area + the resolution parenthetical is in place; verify Last-updated header carries CL-028 annotation.
13. `_root/08_quality_bar.md` — read for orientation.

### Source materials for the audit (REQUIRED — paste-verify in conformance block per CL-024)

14. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_meta/stage4_prompts/PLANNING_AGENT_HANDOFF.md` — **explicit per-prompt authorization to read this file** (the normal AGENTS.md hard rule against browsing `_meta/` is overridden for this Stage 4 prep session, scoped to this specific file). Read sections:
    - **§5 In-flight state** — particularly Stage 4.2 cohort iter 3 status.
    - **§9 Action sequence** — particularly Action 3 (this session) + Appendix B.6.2 cross-reference.
    - **Appendix A + B + B.4 + B.5 + B.6** — all canonical disciplines this audit operates against.
15. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_meta/stage3_cleanup.md` — **explicit per-prompt authorization to read this file** (Stage 3 cleanup tracker; normally consulted by planning agent only). Read CL-001 / CL-003 / CL-004 / CL-005 (finding 7 staleness verification), CL-027 RESOLVED entry (finding 3 debug-language verification), and CL-028 RESOLVED entry (finding 13 verification baseline).
16. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_meta/stage4_account_ledger.md` — **explicit per-prompt authorization to read this file** (Stage 4 per-account ledger; planning-agent custodianship). Read the 3 populated rows (lpf + cci + sca) — context for finding 14 (3rd-consecutive-omission lockdown candidate verification).
17. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_meta/v6_2_reconciliation_log.md` — verify line 21 methodology still says AND (finding 13 propagation check). 37 flagged rows count should be unchanged.
18. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_meta/stage4_prompts/_paste-ready/stage_4_1__lpf.md` (735 lines) + `_paste-ready/stage_4_2__cci.md` (841 lines) + `_paste-ready/stage_4_2__sca.md` (885 lines) — finding 6 verification (paste-ready bloat). Read all three structurally + compare to the format-X drafter prompt at `stage_4_2__format-b__per-account-drafter.md` (697 lines).
19. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_master-account-data-v6.2.csv` — **explicit per-prompt authorization to read** (Appendix B canonical data; planning-agent + drafter consulted). Used for `csv.DictReader` arithmetic verification of findings 9 + 10.

### Files NOT to read (per AGENTS.md hard rules; explicit re-statement for this session)

- `_archive/**` — anti-archive rule per `_root/CONTRACTS.md §4`; no explicit-extraction exception opened for this audit session.
- `Migration-Health Artifacts/**` — out of scope. The lede health-data extension (finding 15) verification looks at `_root/04 §4.2` only; the `Migration-Health Artifacts/` source data does NOT need to be read this session (the question is structural: should the 4th-stat variant be authorized as a Stage 4 template-level convention; not what the specific data point would say).
- `_reference/**` — out of scope.
- `_meta/stage2_prompts/**` + `_meta/stage3_prompts/**` — out of scope.
- Other `_meta/stage4_prompts/_paste-ready/*.md` (the `bri` paste-ready in particular; superseded post-CL-026 hard-stop) — out of scope.
- `format-*-notices/*.md` per-account artifacts (lpf + cci + sca briefs/emails) — out of scope for this audit (the ledger captures the audit results); read only if a specific finding requires it.

---

## Step 2: The 15 findings to verify

Findings 1–12 are operator-stamped pre-populated in `_meta/stage4_prompts/PLANNING_AGENT_HANDOFF.md` Appendix B.6.2. Finding 13 was surfaced and RESOLVED in-session via CL-028 at the Stage 4.2 sca v2 cohort iter 3 closeout; your verification confirms the source-fix landed cleanly. Findings 14 + 15 are mid-session-surfaced by the prior planning agent during the sca v2 audit; they are pending operator-stamp triage at this session.

### Findings 1–12 (verbatim from Appendix B.6.2)

Read Appendix B.6.2 in `_meta/stage4_prompts/PLANNING_AGENT_HANDOFF.md` — the 12-row table is your authoritative source. Each row has 5 columns: `#` / `Source location` / `Type` / `Prior agent's note` / `Verify by`. Your verification reads the cited source + cross-checks the suspected drift type + classifies as one of:

- `RESOLVED-verify-only` — finding was resolved in-session at sca closeout; you confirm the source-fix landed cleanly (only Finding 13 has this status; see below).
- `definitely_fix` — verified drift; concrete trim proposed (BEFORE prose vs AFTER prose). Cleanup is SUBTRACTIVE or REPLACING per Appendix B.6.3 guardrail 3.
- `consider_fix` — verified drift but cleanup is judgment-call (e.g. bloat reduction at scale; the operator should weigh whether to do it now or defer to a Stage 5 finalization pass).
- `leave_alone` — verified that the apparent drift is actually load-bearing or false-positive; finding closes with no action.

### Finding 13 (RESOLVED in-session via CL-028 2026-05-26 — verify only)

`_root/07 §4.5` reconciliation-flag prose tightening: pre-CL-028 prose used "(or the dollar discrepancy exceeds $60/month)" parenthetical (ambiguous; could be read as disjunction or synonym); operator-stamped `resolve_now_AND_canonical` 2026-05-26 → post-CL-028 prose now uses explicit "AND the dollar discrepancy exceeds $60/month" matching `_meta/v6_2_reconciliation_log.md` line 21 operationalized methodology. **Verify**: read `_root/07 §4.5` at line ~246 area + verify the AND-tightening + verify the resolution parenthetical is in place + verify the `_root/07` header carries the CL-028 annotation. Confirm `_meta/v6_2_reconciliation_log.md` line 21 still says "AND" (propagation check). Confirm 37 flagged-row count is unchanged.

### Finding 14 (mid-session-surfaced at sca v2 audit — triage candidate)

**3rd-consecutive §3m "How This Compares" OMISSION on URN-primary Format B accounts**:

- **lpf** (Format A 60-Day Notice; URN-primary; OMITTED 2026-05-26 per drafter judgment + `_root/04 §4.11` + QB-071)
- **cci** (Format B Notice + Meeting; URN-primary standalone; OMITTED 2026-05-26 per drafter judgment + lpf precedent)
- **sca** (Format B Notice + Meeting; URN-primary + IUR-secondary REDUCTION; OMITTED 2026-05-26 per drafter judgment + lpf + cci precedent)

3 consecutive omissions across 2 formats with URN-primary driver. Pattern locked: URN-primary brief is structurally self-explaining via the `_root/05 §2.1.2 / §2.1.4 / §2.1.5` URN canonical-block + pricing-table + ladder; peer-position framing adds no client-side clarity. **Verify by**: read `_root/04 §4.11` source prose; verify it carries a "drafter judgment to omit" clause vs being a default-include rule. **Classify**: should the §3m OMISSION be codified as Stage 4 template-level convention default for URN-primary briefs at `_root/04 §4.11` source (operator-stamp candidate) or kept as case-by-case drafter judgment (carries informational drift if 5+ consecutive omissions happen without convention codification)?

### Finding 15 (mid-session-surfaced at sca v2 audit — operator-raised — triage candidate)

**Section 3b lede 4th-stat health-component variant** (operator raised at sca v2 closeout: "can we add health data here … to add one compelling data point … is it too complex to add this now and something we do later?"):

- Current Section 3b lede pattern (`_root/04 §4.1 + §4.2 + §4.4`) carries 3 Postgres-derived stats (sessions / orders / customers) + tenure + dollar change.
- Proposed extension: 4th stat from `Migration-Health Artifacts/` (health-v3 folder) — one health-component data point translated to customer-facing prose.
- Constraint: `_root/04 §3` 32-row forbidden-phrase table forbids health-band names + dimension scores in client copy; translation discipline non-trivial.
- Path-reference + Appendix A.5 narrow drafter-generated prose discipline: extension would require `_root/04 §4.2` extension authorizing the 4th-stat variant + per-component translation rules; affects every subsequent Format B + likely Format A + CEO Letter drafter prompt; template-scope, not per-account-scope (per Architectural concept #7).
- **Verify by**: read `_root/04 §4.1 + §4.2` source prose; understand current stat-guardrail rules; determine whether the 4th-stat extension belongs at Stage 4 template-level (operator-stamped at this audit) OR Stage 5 finalization (deferred to bulk-production gate) OR Stage 6+ post-program scope.
- **Classify**: should `_root/04 §4.2` be extended at this audit with a 4th-stat health-component variant via Stage 4 prep Source-fix Session D paste-ready, OR deferred to a later cycle, OR rejected as scope-creep?

---

## Step 3: Per-finding verification methodology

For each finding (1 through 15 + any new findings you extend with):

1. **Read the cited source file + lines** verbatim. Do not infer from manifest descriptions; the source is authoritative.
2. **Cross-check against authoritative sources**:
   - Appendix B canonicality (v6.2 CSVs) — for any finding involving account counts, driver enumerations, secondary-driver matrix rows (`csv.DictReader` per Appendix B.5.1).
   - Manifest line counts (`wc -l` ground-truth via terminal) — for any finding involving "row line counts" or "footer cumulative" claims.
   - Audit baseline (post-CL-027 91.6% clean: 98 pass / 8 flag / 1 fail per `_meta/stage3_cleanup.md` CL-026 RESOLVED entry) — for any finding involving v6.2 driver-stamp audit-baseline.
   - `_meta/v6_2_reconciliation_log.md` 37 flagged rows (cohort sweep 2026-05-26) — for any finding involving reconciliation-tracker drift.
3. **Classify** per the 4-bucket schema above (`RESOLVED-verify-only` / `definitely_fix` / `consider_fix` / `leave_alone`).
4. **Propose a concrete trim** (only for `definitely_fix` and `consider_fix`):
   - Cite the source file + line range to modify.
   - Show the BEFORE prose (the current text) verbatim.
   - Show the AFTER prose (the proposed trim) verbatim.
   - Note any propagation steps needed per `_root/CONTRACTS.md §3` (e.g. manifest §2 row line-count refresh; `_root/09_changelog.md` CL-NNN entry; downstream paste-ready refreshes if any).
5. **Surface via AskQuestion**: bundle all findings into ONE `AskQuestion` with per-finding options.

### Hierarchical fix-priority (per Appendix B.6.3 guardrail 4)

When proposing trims, prioritize:

1. **Contradictions in source rule prose** (e.g. a rule paragraph that contradicts another rule paragraph; CL-028 was this class of finding pre-resolution).
2. **Stale counts/numbers** (e.g. §4 weaving matrix occurrence counts that no longer reconcile to v6.2 post-CL-026/CL-023/CL-027 stamps).
3. **Conversational debug language** (e.g. "Wait —" inline parentheticals; planning-agent state-of-mind leaks).
4. **Bloat** (cell-annotations defeating manifest one-line-summary purpose; paste-ready compounding history).

Fix contradictions first; numbers second; conversational artifacts third; bloat last (bloat is style not correctness).

### Cleanup discipline (per Appendix B.6.3 guardrail 3)

Cleanups are SUBTRACTIVE (trim language; cut bloat) or REPLACING (point to authoritative source instead of restating). Never ADDITIVE. If your proposed trim adds clarification prose, the cure is worse than the disease.

Example of SUBTRACTIVE (acceptable): cutting "Wait — `bcf` was re-stamped TBI→URN in the next iteration of joint resolution; not in this TBI cohort." from `_root/05 §2.4.1` post-CL-027 edit.

Example of REPLACING (acceptable): replacing the `_root/00_manifest.md` row 0 cell's 3,000+ words of cumulative annotation with `→ see _root/09_changelog.md 2026-05-26 entries chain` pointer (relocates the narrative-history to its canonical doc, leaves a pointer in the manifest cell).

Example of ADDITIVE (forbidden): adding a new "Clarification" paragraph to `_root/04 §3` to "improve" the forbidden-phrase guidance.

---

## Step 4: Extension protocol — new findings spotted during verification

`_meta/stage4_prompts/PLANNING_AGENT_HANDOFF.md` Appendix B.6.2 is operator-stamped open-ended: "The drift watchlist (B.6.2) is open-ended; you are expected to extend it, not just verify the 12 starting items." (Appendix B.6.2 footer.)

During your verification reading, you will likely spot additional drift artifacts. For each:

1. **Document it** in the same triaged-findings table (as finding #16, #17, etc.).
2. **Same verification methodology** (read source; cross-check; classify; propose trim if applicable).
3. **Time-box check**: if you reach 15+ verified extension findings (beyond the 15 pre-populated below), surface a checkpoint AskQuestion to the operator: continue this session OR defer the additional surfacings to a follow-on hygiene pass per Appendix B.6.3 guardrail 1.

You are NOT required to find new findings — the 15 pre-populated are sufficient for one audit pass. Extensions are bonuses, not obligations.

---

## Step 5: Output + conformance block

Your single deliverable this session is:

### (a) A triaged-findings table (in markdown, in your final chat response)

15+ rows. For each finding:

| # | Status (RESOLVED-verify-only / definitely_fix / consider_fix / leave_alone) | Source location | Type | Verified observation | Proposed trim (BEFORE prose → AFTER prose) | Propagation steps if applied |

### (b) A consolidated AskQuestion bundle

ONE `AskQuestion` call with N questions (one per finding requiring operator stamp). Each question carries:

- The verified finding (one-paragraph summary).
- 3–4 options for operator selection (typically: "apply the trim per Source-fix Session D" / "consider but defer to Stage 5 finalization" / "leave alone — false positive" / occasionally "escalate as new CL-NNN").
- For findings 14 + 15: explicit options reflecting the mid-session-surfaced triage (template-convention codification candidates).

### (c) Conformance block per `_root/00_manifest.md §5` + audit-specific additions

Per the canonical conformance-block format. Audit-specific additions:

- **Findings verified count**: N (typically 15 pre-populated + any extensions).
- **Findings classified by bucket**: counts per bucket (e.g. "1 RESOLVED-verify-only, 4 definitely_fix, 7 consider_fix, 3 leave_alone").
- **Proposed trim total line-change**: sum across all `definitely_fix` + `consider_fix` proposals (e.g. "–82 lines if all `definitely_fix` approved; –300 lines if all `consider_fix` also approved"). Audit is subtractive; this number should be NEGATIVE (lines removed).
- **CL-024 paste-verification carry-forward**: every verbatim source passage you paste-quoted (per Step 1 requirement).
- **Open questions for operator**: NONE expected by default (the AskQuestion bundle IS the operator-decision surface; conformance block "open questions" is reserved for issues that can't be triaged into the AskQuestion bundle).

### (d) STOP after surfacing

You do NOT apply any source-file edit this session. After producing (a) + (b) + (c), you stop and await operator stamps. The next planning-agent session applies the operator-stamped trims per `_root/CONTRACTS.md §3` rule-change protocol (with full propagation sweep including `_root/09_changelog.md` entry + manifest refresh + any downstream paste-ready refreshes if needed).

---

## Hard rules

1. **You will not silently edit any source file this session.** Every proposed trim lands via `AskQuestion` for operator stamp. The next planning-agent session applies operator-stamped trims.
2. **You will not introduce new drift via the audit itself.** Cleanups are SUBTRACTIVE or REPLACING only; never ADDITIVE.
3. **You will time-box this audit to ONE session.** If >15 extension findings surface beyond the 15 pre-populated, surface checkpoint to operator (continue OR defer to follow-on pass).
4. **You will verify before classifying.** A finding only counts if you've read the cited source + cross-checked the suspected drift. "I think this might be drifty" without source-citation is not actionable.
5. **You will prioritize hierarchically** per Appendix B.6.3 guardrail 4: contradictions > stale numbers > conversational debug language > bloat.
6. **You will not paraphrase or soften any operator-stamped content.** Paste-fidelity is the operator stamp's enforcement mechanism per CL-024.
7. **You will not extend beyond audit scope.** No new rules. No new architectural concepts. No template-level convention codification (that's a separate Stage 4 prep Source-fix Session if findings 14/15 stamp toward action). The audit's purpose is calibration of existing rule-layer; not redesign.
8. **You will produce the consolidated AskQuestion bundle as your single output surface.** The operator stamps; the next planning-agent session executes.

---

## Stop conditions (where you `_root/CONTRACTS.md §2` flag)

- A required manifest-echo file is missing or has a mismatched Last-updated date relative to `_root/00 §2` table → STOP + flag QB-125 propagation failure.
- A paste-verification source passage (per Step 1 list 1–5) is missing or non-paste-quotable → STOP + flag.
- A finding's verification surfaces a CONTRADICTION you cannot triage into one of the 4 buckets → STOP + flag as new CL-NNN candidate (do NOT silently classify).
- Your verification of Finding 13 (CL-028 RESOLVED) finds that the source-fix did NOT land at `_root/07 §4.5` (the AND-tightening prose is absent) → STOP + flag CL-028 propagation-incomplete; do NOT proceed with the other findings until the operator triages.
- You spot a contradiction between Appendix B.6.2 and a source rule that wasn't pre-flagged in the watchlist (i.e. a HIGHER-priority finding than any of the 15) → STOP + flag as new CL-NNN candidate; do NOT silently fold into the audit findings table.

The audit's value is its discipline: tightly bounded scope, time-boxed, calibration-not-redesign, surface-don't-edit, operator-stamps-the-trim.

---

## Conformance block (paste-into-final-response template)

Use the canonical format from `_root/00_manifest.md §5` with these audit-specific additions:

```
─── Conformance Block (Stage 4 prep Source-fix Session C — Self-audit pass per Appendix B.6.2) ─────────
Session task: Planning-agent self-audit pass per `_meta/stage4_prompts/PLANNING_AGENT_HANDOFF.md` §9 Action 3 + Appendix B.6.2 12-finding drift watchlist + 3 mid-session-surfaced findings (13 RESOLVED via CL-028 / 14 omission-lockdown candidate / 15 lede health-data extension candidate); SURFACING ONLY (no source-file edits applied this session).
Output target: triaged-findings table (markdown) + consolidated AskQuestion bundle + conformance block. Next planning-agent session applies operator-stamped trims.

Manifest echo (per `_root/00_manifest.md §1 step 6 + §6` — paste-quote ALL ENTRIES from §2 with title + Last-updated header date verified at source, NOT mtime alone per CL-024):
[paste-quote 11 entries verbatim]

Files read (with last-updated date / mtime):
[list every file from Step 1 with last-updated date or mtime as appropriate]

Files NOT read (per Step 1 "Do NOT read"):
[list per Step 1 + any judgment calls]

CL-024 paste-verification (REQUIRED — paste-quote verbatim each operator-stamped source passage per Step 1 list 1–5):

1. Appendix B.6.1 three lessons (verbatim from `_meta/stage4_prompts/PLANNING_AGENT_HANDOFF.md`):
   [paste-quote]

2. Appendix B.6.2 12-row drift watchlist table (verbatim):
   [paste-quote]

3. Appendix B.6.3 5-rule guardrail list (verbatim):
   [paste-quote]

4. CL-028 entry verbatim from `_meta/stage3_cleanup.md`:
   [paste-quote]

5. `_root/07 §4.5` post-CL-028 prose verbatim:
   [paste-quote line 246 area + resolution parenthetical immediately below]

Triaged-findings table (15 pre-populated + N extensions):
[table per Step 5 (a)]

Findings classified by bucket:
- RESOLVED-verify-only: N (expected: 1 if Finding 13 verified clean)
- definitely_fix: N
- consider_fix: N
- leave_alone: N
- new-CL-NNN candidates (escalated; not silently triaged): N

Proposed trim total line-change: −N lines if all `definitely_fix` approved; −N lines if all `consider_fix` also approved (subtractive; should be NEGATIVE).

Hierarchical fix-priority distribution:
- Contradictions: N
- Stale numbers: N
- Conversational debug language: N
- Bloat: N

Extensions to Appendix B.6.2 surfaced this session (beyond the 12 pre-populated + Finding 13 + 14 + 15):
[list each new finding with #, source location, type, verified observation]

Time-box status: within ONE session; checkpoint NOT needed (or: surfaced checkpoint at finding #X per Appendix B.6.3 guardrail 1).

Gaps surfaced (audit finding that fits no existing CL-NNN class + can't be cleanly triaged):
[list or "none"]

Open questions for operator:
[bundled into the AskQuestion surface; conformance-block "open questions" only for issues outside that surface]

Stage-4 prep Source-fix Session C output: SURFACING COMPLETE. Operator stamps the AskQuestion bundle. Next planning-agent session applies operator-stamped trims per `_root/CONTRACTS.md §3` rule-change protocol.
─────────────────────────────────────────────────────────────
```

---

*Operator-stamped Stage 4 prep Source-fix Session C drafter prompt by Stage 4 planning agent 2026-05-26 per operator stamp `audit_via_dedicated_session` at Action-3 sequencing AskQuestion. Mirrors Stage 4 prep Sessions A + B pattern (in-place rule-layer edits at canonical source, fresh-agent CL-024 strict + paste-verification discipline) WITH the critical distinction that this session is SURFACING-ONLY (no source-file edits; operator stamps via AskQuestion bundle; next planning-agent session applies operator-stamped trims). Audit calibration discipline per Appendix B.6.3 guardrails 1–5 + cleanup-subtractive-or-replacing discipline per guardrail 3. CL-024 strict + paste-verification carry-forward applies in full to this session.*
