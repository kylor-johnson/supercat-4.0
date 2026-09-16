# Elite Insights — Order of Operations

> How to execute the Phase 1 enhancements without context overload.
> Each "unit of work" is one agent chat, scoped to stay under ~50K tokens.

---

## Recommended Approach: Agent-Prompt Batching

**Do NOT try to implement all 5 in one session.** Each insight touches 3-4 files and requires SQL validation against live data. One insight per agent session, with a review checkpoint between each.

---

## Execution Sequence

### Session 1: Q-14b — Reorder Velocity Deceleration (EASIEST, enhances existing)

**Why first**: This ENHANCES an existing subsection (§3.6, Q-14). It's the simplest because:
- The subsection already exists and renders
- The data source (`portal_orders`) is already queried
- No new gate flags needed
- Just adds a deceleration-detection layer to existing output

**Scope for the agent**:
1. Read `authority/query_library.md` Q-14 section
2. Write Q-14b SQL (interval comparison with deceleration ratio)
3. Add Q-14b to `scripts/data_gather.py` (alongside Q-14 in Batch C)
4. Update `section_03_customers.md` subsection 6 rendering rules
5. Run `data_gather.py` for one org to validate the output

**Context needed**: query_library.md (Q-14 section only), data_gather.py (Batch C section), section_03_customers.md

---

### Session 2: Q-59 — Fill Rate Revenue Impact (HIGH IMPACT, straightforward SQL)

**Why second**: Fill rate is simple math (`qty_invoiced / qty_ordered`), the data lives in one table (`portal_order_items`), and it creates a new subsection in §4 that's visually distinct. High VP Sales impact.

**Scope for the agent**:
1. Write Q-59 SQL (fill rate + top impacted SKUs + revenue exposure)
2. Add Q-59 to `scripts/data_gather.py` (Batch G, gated on `HAS_PORTAL_ORDERS + HAS_INVENTORY`)
3. Add subsection 1b to `section_04_product.md`
4. Run to validate

**Context needed**: query_library.md (Q-37 area), data_gather.py (Batch G), section_04_product.md

---

### Session 3: Q-55 + Q-56 — Competitive Displacement (THE KILLER INSIGHT)

**Why third**: This is the #1 insight by impact ("I didn't know I was losing this") but requires more complex SQL (period-over-period comparison with category joins). Doing it third means we've validated the pipeline pattern with simpler queries first.

**Scope for the agent**:
1. Write Q-55 SQL (category-level displacement)
2. Write Q-56 SQL (per-rep capture rate trend)
3. Add both to `scripts/data_gather.py` (Batch F)
4. Add subsection 8 to `section_05_commerce.md`
5. Run to validate — check that `portal_order_items.ecat_item_number` actually works as the eCat link

**Context needed**: query_library.md (Q-45, Q-52 area for reference), data_gather.py (Batch F), section_05_commerce.md

---

### Session 4: Q-57 — Cross-Sell Whitespace (COHORT ANALYSIS)

**Why fourth**: Cohort-based analysis is the most complex SQL (peer grouping, category comparison). It also produces the biggest "money on the table" number. Needs careful validation.

**Scope for the agent**:
1. Write Q-57 SQL (customer category mix → peer comparison → gap identification)
2. Add to `scripts/data_gather.py` (Batch F, gated on `PORTAL_CUSTOMER_DATA_PRESENT`)
3. Add subsection 8 to `section_03_customers.md`
4. Run to validate — check that category grouping produces meaningful output

**Context needed**: query_library.md (Q-52, Q-53 area), data_gather.py (Batch F), section_03_customers.md

---

### Session 5: Q-58 — Post-Market Attribution (CONDITIONAL)

**Why last**: Depends on a new gate flag (`HAS_COMMITMENT_DATA`), and `commitment_reports.items` is a text field that may need parsing logic. Also, not all orgs have commitment data — so this won't render for everyone. Lower priority.

**Scope for the agent**:
1. Add `HAS_COMMITMENT_DATA` gate to `data_gather.py` preflight
2. Write Q-58 SQL (parse commitment items → match to portal_order_items within 90 days)
3. Add Q-58 to `scripts/data_gather.py` (new conditional batch)
4. Add subsection 9 to `section_05_commerce.md`
5. Run to validate — need to check an org that HAS commitment data (check which orgs have rows)

**Context needed**: query_library.md (end section), data_gather.py (preflight + new batch), section_05_commerce.md, schema of `commitment_reports`

---

## Review Checkpoint Protocol

After EACH session completes:

1. **Run `data_gather.py`** for a test org (e.g., `ufi` which has portal_orders)
2. **Inspect the new cache file** — does the SQL return meaningful rows? Are the numbers plausible?
3. **Run the report generation** for that org — does the new subsection render correctly?
4. **Open the HTML** — does it look right visually?

If YES → proceed to next session.  
If NO → fix in the same session before moving on.

---

## What I (current agent) Should Do Now

Given that:
- I have full context of the system
- I can write SQL and validate against the schema
- The user wants me to start implementing

**My recommendation**: I should do Session 1 (Q-14b) right now in this chat — it's the simplest, enhances existing content, and proves the pattern. Then generate handoff prompts for Sessions 2-5 that other agents can execute.

Alternatively, I can do Sessions 1-2 (Q-14b + Q-59) since both are straightforward, then hand off 3-5.

---

## Handoff Prompt Template (for future agents)

Each session should start with this context injection:

```
You are implementing a new insight for the Insightful Product 2.0 external report system.

Read these files first:
1. Insightful Product 2.0/ELITE_EXECUTION_PLAN.md — for what you're building
2. Insightful Product 2.0/authority/query_library.md — for SQL patterns and schema
3. Insightful Product 2.0/scripts/data_gather.py — for the data gathering pipeline
4. The specific section guide you'll be modifying

Your task: Implement [SPECIFIC INSIGHT NAME] per the execution plan.

Steps:
1. Write the SQL query (following patterns in query_library.md)
2. Register it in data_gather.py (correct batch, correct gate, correct filename)
3. Add the subsection to the section guide (rendering rules, gate check, checklist)
4. Run data_gather.py --shortname ufi --org-id [ID] --run-date 2026-06-15 to validate
5. Report the cache file contents for review

Hard constraints:
- Follow Global Query Guardrails from query_library.md
- Never use "ERP" in client-facing text
- portal_orders = total business, never "portal ordering"
- New subsection must have a what-this-means close
- Add to Conditional Subsection Checklist at end of guide
```

---

## Summary

| Session | Insight | Difficulty | Impact | Files Touched |
|---|---|---|---|---|
| 1 | Q-14b Reorder Deceleration | Easy | High | query_library, data_gather, section_03 |
| 2 | Q-59 Fill Rate Revenue | Easy | Very High | query_library, data_gather, section_04 |
| 3 | Q-55/56 Competitive Displacement | Medium | Highest | query_library, data_gather, section_05 |
| 4 | Q-57 Cross-Sell Whitespace | Hard | Very High | query_library, data_gather, section_03 |
| 5 | Q-58 Post-Market Attribution | Medium | High (conditional) | query_library, data_gather, section_05, preflight |

Total: 5 sessions, each 30-60 minutes of agent work. Full Phase 1 in ~one day.
