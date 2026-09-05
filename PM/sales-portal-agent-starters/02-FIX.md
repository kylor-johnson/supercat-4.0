# STARTER — FIX / Lane 0 (Agent Mode)

Paste this. Replace `TICKET` with one key (default: **EBR-40** — active Bet A filter truth).

---

You are **diagnosing** Sales Portal trust bugs (Lane 0). One ticket per pass.

## ISOLATION MODE — ON
**Read-only on code.** Do not edit `supercat-code/` / `supercat_server`.  
Deliver diagnosis + proposed patch **as markdown only**. No apply, no commit, no PR.  
Implement only if I later say: `ISOLATION OFF — GO on SERV-XXXX`.

## Ticket
`TICKET` = **EBR-40** (territory filter not working on invoice list) — active Bet A, paired with **EBR-212** (dashboard half) as one filter-truth story. See `cycle-03-outputs/PITCH-phase1-filter-metric-law.md` + `TECHNICAL-PLAN.md` §3.  
**Shelf (do not start without GO):** SERV-2178/2180 = EBR-180 XL multi-territory (Appendix A downstream). SERV-2196 / SERV-2395 = related trust surfaces — only pull in if same root cause.

## READ
1. `SuperCat 4.0/PM/sales-portal-agent-starters/00-PROGRAM-SPINE.md` (§3 + §6 Lane 0 + Isolation)
2. Jira issue via Atlassian MCP (`getJiraIssue`)
3. Code (**read only**):  
   - `supercat-code/supercat_server/app/helpers/ecat_permissions_helper.rb`  
   - `supercat-code/supercat_server/app/models/base_portal_dataflow.rb`  
   - `supercat-code/supercat_server/app/models/eol_left_nav_dataflow.rb`  
   - `supercat-code/supercat_server/app/controllers/ecat_customers_controller.rb` (and dashboard if needed)  
4. `SuperCat 4.0/documentation/KLL_Territory_Sales_Portal_Analysis_Feb_2026.md` if territory-related

## Rules
- Smallest correct fix proposal; no reface, no new metrics, no LLM
- Prefer reproducing with Postgres MCP (read-only) on a named shortname
- Write the proposed patch as a fenced diff or step list in chat / a `.md` under `PM/` — **not** into the Rails repo

## Deliverable
1. Root cause in plain language  
2. Repro steps / org evidence  
3. Proposed fix + risk (layout/catalog coupling?) — markdown only  
4. Acceptance criteria  
5. Stop. Paste output to Orchestrator (05) for Review Card. Do not implement unless isolation is lifted.
