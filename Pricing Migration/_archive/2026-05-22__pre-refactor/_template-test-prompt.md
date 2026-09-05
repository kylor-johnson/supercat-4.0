# Template Fix Verification — Test Prompt
*Run this in a fresh agent to confirm all 7 template fixes are present and correct*
*Last updated: 2026-05-19*

---

## What You Are

You are a quality assurance agent. Your only job is to verify that 7 specific changes are correctly present in 5 files. You are NOT drafting communications. You are NOT making improvements. You are running a mechanical checklist and returning a pass/fail report with evidence.

Do not interpret intent. Do not suggest improvements. Do not explain what the changes do. Just read the files, check for the exact conditions listed below, and report pass or fail with a quoted excerpt as evidence.

---

## Files to Read (read all 5 before checking anything)

1. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/format-b-notices/_brief-template.md`
2. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/ceo-letter-notices/_brief-template.md`
3. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/format-a-notices/_fresh-agent-prompt.md`
4. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/format-b-notices/_fresh-agent-prompt.md`
5. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/ceo-letter-notices/_fresh-agent-prompt.md`

---

## Checks

Run every check. Report PASS or FAIL. Quote the exact line(s) from the file as evidence for each check.

---

### CHECK 1 — Platform base conditional in `user_rate_normalization` block
**Files:** Format B brief template AND CEO Letter brief template (must pass in both)
**Condition:** The `DRIVER: user_rate_normalization` block must contain a conditional instruction stating that IF the platform base changes alongside the user rate, a sentence must be added explaining the platform base change. The conditional must reference "Before platform base ≠ After platform base" or equivalent.
**FAIL if:** The block jumps straight from the "We're standardizing" sentence to the user rate table with no platform base conditional.

---

### CHECK 2 — Billing basis definition after `user_rate_normalization` table
**Files:** Format B brief template AND CEO Letter brief template (must pass in both)
**Condition:** Immediately after the pricing table in the `DRIVER: user_rate_normalization` block (before the `---` separator leading to `tier_base_increase`), there must be a line containing "User billing is based on enabled accounts in your SuperCat environment."
**FAIL if:** The table is followed immediately by `---` with no billing basis line.

---

### CHECK 3 — Billing basis definition after `included_user_reduction` table
**Files:** Format B brief template AND CEO Letter brief template (must pass in both)
**Condition:** Immediately after the pricing table in the `DRIVER: included_user_reduction` block (before the `---` separator leading to `platform_discount_correction`), there must be a line containing "User billing is based on enabled accounts in your SuperCat environment."
**FAIL if:** The table is followed immediately by `---` with no billing basis line.

---

### CHECK 4 — "Only thing changing" conditional
**Files:** Format B brief template AND CEO Letter brief template (must pass in both)
**Condition:** The "Your Pricing at a Glance" section must contain BOTH of the following:
- A line with "IF primary or secondary driver is NOT `included_user_reduction`" leading to "The only thing changing is the invoice."
- A line with "IF primary or secondary driver IS `included_user_reduction`" leading to a variant that says "The included user base and the invoice are both changing."
**FAIL if:** Only the unconditional "The only thing changing is the invoice." appears.

---

### CHECK 5 — "Above the midpoint" user-count clause requirement
**Files:** Format B brief template AND CEO Letter brief template (must pass in both)
**Condition:** The guidance block in the "How This Compares" section must explicitly state that when using "above the midpoint," a clause explaining that the position is driven by user count (not tier premium) is REQUIRED/MANDATORY. The guidance must include language like "driven by your team size at [N] users" as an example.
**FAIL if:** The guidance only says "above the midpoint = above midpoint" with no mandatory clause requirement.

---

### CHECK 6 — Value anchor delta-per-order reframe
**Files:** Format B brief template AND CEO Letter brief template (must pass in both)
**Condition:** The "What This Works Out To" section must contain:
- A second formula: `delta_mrr × 12 / ltm_orders`
- Instructions to add a second sentence "The annual rate increase works out to approximately $[DELTA_PER_ORDER] per order."
- A gate condition: only include the second sentence if `delta_per_order < $50`
**FAIL if:** Only the original per-order cost formula exists with no delta-per-order calculation.

---

### CHECK 7 — Lede stat guardrail (provisioned-vs.-active ratio prohibition)
**Files:** Format A prompt, Format B prompt, AND CEO Letter prompt (must pass in all 3)
**Condition:** Each prompt must contain an explicit prohibition against expressing login data as a provisioned-vs.-active user ratio (e.g., "X of Y users logged in"). The prohibition must state that output metrics (orders, customers) should lead instead.
**Look for:** Language like "NEVER frame as a provisioned-vs.-active user ratio" or "Do NOT express login data as a provisioned-vs.-active ratio."
**Also check:** The Format A prompt's STEP 4 lede paragraph instruction must NOT say "X of your Y users logged in in the last 90 days" as an example to follow. It must instruct the agent to lead with `ltm_orders` and `ltm_customers_served`.
**FAIL if:** Any of the 3 prompts still tell the agent to frame lede stats as "X of Y users logged in."

---

### CHECK 8 — CEO Letter high-delta lede rule
**File:** CEO Letter brief template ONLY
**Condition:** The LEDE instruction block must contain a rule for accounts with delta >30% requiring the lede to directly acknowledge the annual dollar impact. Must include:
- Reference to delta >30% threshold
- Instruction to add a sentence naming the annual figure (e.g., "That's $[DELTA × 12]/year")
- Framing note that naming it directly is disarming, not alarming
**FAIL if:** The LEDE instruction ends without any high-delta rule.

---

## Output Format

Return a table:

| Check | Files | Result | Evidence (quoted excerpt) |
|---|---|---|---|
| 1 — Platform base conditional | Format B + CEO Letter | PASS/FAIL | "..." |
| 2 — Billing basis after URN table | Format B + CEO Letter | PASS/FAIL | "..." |
| 3 — Billing basis after IUR table | Format B + CEO Letter | PASS/FAIL | "..." |
| 4 — Only-thing-changing conditional | Format B + CEO Letter | PASS/FAIL | "..." |
| 5 — Above-midpoint clause requirement | Format B + CEO Letter | PASS/FAIL | "..." |
| 6 — Delta-per-order reframe | Format B + CEO Letter | PASS/FAIL | "..." |
| 7 — Lede stat guardrail | Format A + B + CEO Letter prompts | PASS/FAIL | "..." |
| 8 — CEO Letter high-delta lede rule | CEO Letter only | PASS/FAIL | "..." |

Then below the table: **OVERALL: X/8 checks passed.**

If any check fails, list the failing file and exact location after the table so it can be corrected immediately.
