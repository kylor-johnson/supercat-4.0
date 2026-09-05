# V12 Stage-Gated Pipeline Assessment Prompt

**Version:** V12  
**Created:** January 14, 2026  
**Playbook Reference:** `Stage_Gated_Onboarding_Playbook_V12.md`

---

## Full Assessment Prompt (Recommended)

Copy and paste this into Cursor:

```
@Stage_Gated_Onboarding_Playbook_V12.md 

Run a V12 Stage-Gated Pipeline Assessment for the following client(s): [CLIENT_SHORTNAME(S)]

**Requirements:**
1. Execute ALL required tool calls as specified in the playbook (HubSpot → MCP → BigQuery → Fathom)
2. For batch assessments: Query HubSpot FIRST to get authoritative list of onboarding clients (lifecyclestage = 'evangelist')
3. Do NOT estimate, assume, or hallucinate any data - every metric must come from a verified tool call
4. Include the Tool Call Verification table showing each call made and its response
5. For Fathom: Check ALL calls with "implementation", "onboarding", "support", or client name in title. Do NOT skip "hold" calls.
6. For Help Scout: Query BOTH support and onboarding inboxes, BOTH open and closed tickets, extend to 180 days if 90 days yields no results
7. If ANY data point cannot be verified, mark it as ❓ UNVERIFIED and explain why
8. If a tool call fails, retry once then flag the failure explicitly
9. Output in the exact format specified in the playbook

**Accuracy Protocol:**
- If unsure about any metric: Flag it with ⚠️ and explain the uncertainty
- If data conflicts between sources: Show both values and flag the discrepancy
- If a stage assessment is ambiguous: Default to the more conservative (lower) status
- Never round readiness percentages - calculate exactly from stage completion

Begin assessment.
```

---

## Quick Version (Single Client)

```
@Stage_Gated_Onboarding_Playbook_V12.md 

V12 Assessment for [CLIENT_SHORTNAME]. Execute all MCP, BigQuery, and Fathom tool calls. Flag any data that cannot be verified. Output in playbook format.
```

---

## Batch Assessment Version (All Active Onboarding Clients)

```
@Stage_Gated_Onboarding_Playbook_V12.md 

V12 Pipeline Assessment for ALL active onboarding clients. 

Steps:
1. First, query HUBSPOT (NOT MCP) to get all companies in "Onboarding" lifecycle stage:
   - Use API: POST /crm/v3/objects/companies/search
   - Filter: lifecyclestage = 'evangelist' (internal value for "Onboarding")
   - HubSpot is the SOURCE OF TRUTH - MCP status field is unreliable
2. Map each HubSpot company to its MCP org shortname (use domain/name matching)
3. For each mapped client, run the full V12 assessment protocol (MCP → BigQuery → Fathom)
4. Compile into a single Pipeline Overview table sorted by readiness (lowest first)
5. Include individual client sections with full tool call verification

Flag any client where data retrieval fails or is uncertain.
```

---

## Usage Guide

| Scenario | Use This Prompt |
|----------|-----------------|
| Single client check | Quick Version with `[CLIENT_SHORTNAME]` |
| Weekly standup prep | Batch Assessment Version |
| Deep dive on specific client | Full Requirements Version |
| Validating team feedback | Full Requirements Version with specific clients |

---

## Client Shortnames Reference

| Shortname | Full Name |
|-----------|-----------|
| MALI | Magic Lite |
| DCCL | Donald Choi Canada |
| CST | Coaster |
| JC | Jonathan Charles |
| KRB | Kaleen Rugs & Broadloom |
| TCD | Terracotta Designs |
| PEBL | Pebl Furniture |

---

## Accuracy Guarantees

This prompt structure ensures:

1. ✅ **Uses HubSpot as source of truth** for identifying onboarding clients (not MCP status)
2. ✅ **References the unified playbook file** for complete context
3. ✅ **Explicitly requires tool call verification** - every metric has a source
4. ✅ **Mandates flagging of uncertainty** - no silent assumptions
5. ✅ **Specifies enhanced Fathom/Help Scout validation rules** - comprehensive search
6. ✅ **Prevents hallucination** by requiring source attribution for all data

---

## Output Includes

When run correctly, the assessment will produce:

- **Pipeline Overview Table** - All clients sorted by readiness
- **Visual Pipeline View** - ASCII progress bars
- **Per-Client Sections** with:
  - Stage-by-stage status (🟢/🟡/🔴)
  - Tool Call Verification table
  - Key Metrics Summary with sources
  - Validation Flags from Fathom/Help Scout
  - Next Action recommendation
- **Validation Flags Summary** - Critical and review flags
- **Key Takeaways** - Immediate actions and monitoring items

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| HubSpot 401 error | Token may be expired - check `HUBSPOT_INTEGRATION.md` for current token |
| MCP not returning data | Check that `supercat-cs-tools` server is running |
| MCP status mismatch | **Normal** - use HubSpot as source of truth, MCP status field is unreliable |
| BigQuery errors | Verify column names match schema |
| Fathom rate limiting | Script handles automatically with 5s delays |
| Missing Help Scout tickets | Extend search to 180 days, try alternate search terms |
| Output format wrong | Re-reference the playbook file |

---

## Related Files

- `Stage_Gated_Onboarding_Playbook_V12.md` - The unified operational playbook
- `FRD_V12_Accuracy_Stage_Gated_Onboarding.md` - Detailed FRD specification
- `V8 - Full Suite.md` - Original stage-gated checklist reference
