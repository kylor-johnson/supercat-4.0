# Kickoff — build the `ecat-config-check` skill

Paste this whole file into a fresh Claude Code session in the **SuperCat 4.0**
workspace, VPN up. It is self-contained.

---

## Read these first, in this order

| file | why |
|---|---|
| `onboarding-models/ground-truth/SESSION_HANDOFF.md` | three weeks of context: what exists, what's true, the traps that will bite you |
| `onboarding-models/ground-truth/BUILD_SPEC.md` **§ 4** | the empirical config profile — this is your spec |
| `onboarding-models/ground-truth/SCORECARD.md` | the evidence behind every rule you'll write. Skim § 8–11 at minimum |

Don't start querying until you've read § 4 of BUILD_SPEC. It contains prevalence data
across 127 orgs that took real work to produce and that you should not re-derive.

---

## What you are building

A skill at `~/.claude/skills/ecat-config-check/SKILL.md` that takes an org shortname and
answers one question:

> **What about this org's configuration is wrong, missing, or contradictory?**

It sits alongside 26 existing `ecat-*` skills. Match their shape — read a couple first,
particularly `ecat-postgres-audit`, which already has several of the queries you need.

**Read-only. No writes of any kind.** Not to Postgres (the MCP is SELECT-only anyway),
not to the Admin Console. v1 reports; a human acts. Writing comes much later, if ever.

---

## Why this exists

92 settings columns on `organizations`, plus taxonomies, price levels, user types,
custom fields and report formats. Every org needs them configured, there is no checklist,
and settings get forgotten — including by the person who wrote the process.

A five-client audit found seven live defects. Most were configuration, not data.

---

## The two kinds of check

### 1. Prevalence — is this setting unusual for us?

`BUILD_SPEC.md § 4` has the numbers. The shape of the rule:

- **`send_order_email_on_submit` is on for 121 of 127 orgs.** Off is an anomaly worth a line.
- **`use_modern_ui`: 1 org. `enable_data_import3`, `enable_image_import2`, `import_active`: zero orgs.** These are dead. **Do not report dead flags at all** — noise is how a checklist gets ignored.
- Mid-prevalence settings (`mobile_enabled` 53%, `enrollment_enabled` 45%) are genuinely per-client. Report the value, never a verdict.

### 2. Contradictions — the actual prize

Cheap to detect, nothing checks them today, and every one below is a real incident:

| Contradiction | Seen at |
|---|---|
| `send_order_email_on_submit = true` **and** `order_email_recipient` empty | `leg` today; `mali` for months |
| `product_synch_requires_photo = true` **and** products without images | those products never reach the iPad while counting as "visible" |
| custom field registered with `send_to_ipad` + `use_as_filter` **and** zero populated values | `leg`, 13 of them, still empty |
| a user group that **deviates from the pattern its peers follow** | `leg`'s `Catalyst` is `auth='a'` with 0 scoped resources against 23 peers at `'c'`/96; `Futura` has 95. **Empty groups alone are NOT a finding** — see the declared-intent section |
| `ipad_reports` < 3 | go-live checklist requires ≥3; `tcd` shipped with 1 |
| a stored id that no longer resolves | `pebl` — 12 orders on a deleted price level; `mali` — a site on price level 5722, which exists in no org |
| customers with empty `territory_codes` where rep filtering is expected | `pebl`, 171 of 171 |

Contradictions are worth more than prevalence. Weight the output accordingly.

---

## Required in v1 — the declared-intent file

**The database shows structure. It cannot show intent.** Two findings in the source
docs were wrong for exactly this reason (SCORECARD § 12):

- `leg` has 26 user groups with one populated. That reads as neglect and is deliberate:
  Legrand hosts a per-agency Design Studio link in the Library, so each agency needs its
  own group to scope access to its own URL. 24 groups, all `shared_resources_auth='c'`
  with 96 scoped resources.
- `leg` sends `QtyOnHand` and no `QtyAvailable`. That was reported as a broken display.
  Both fields are used live across the fleet; which one shows is configurable.

So build `onboarding-models/config_intent.yml` alongside the skill:

```yaml
leg:
  library_scoping: per-agency     # 24 agency groups deliberate — do not flag empty groups
  inventory_field: qty_on_hand    # not qty_available
  note: "Design Studio links are per-agency; group count follows agency count"
```

**Rules:**
- Anything declared here prints as `DECLARED`, never as a finding.
- A declaration needs a reason, and the reason is the point.
- When Kylor says "that's fine" during the review loop, that answer goes **here**, not
  into a hardcoded exception in the skill.

A checker that flags intentional configuration gets ignored by week two. This file is
what prevents that, and it is why the review loop below is the real work.

## How to build it — the loop matters more than the code

**The expected-config profile does not exist and cannot be written in the abstract.**
It gets written by running the check and arguing about the output.

1. Write a v0 that reports everything it can see for one org.
2. Run it against **`leg`** (org 273, the only org in onboarding), **`mer`** (302, mid-build), **`fal`** (241, mature and transacting — the healthy contrast), and **two more active orgs** of your choosing.
3. Show Kylor the output. For each line he says *"that's wrong"* or *"that's fine."*
4. **Record every answer in the skill** as a rule with its reason. That record is the deliverable as much as the code.
5. Repeat until the output stops surprising him.

Ask about anything ambiguous rather than guessing a threshold. A wrong threshold that
looks confident is worse than a question.

---

## Output shape

Terminal-readable, grouped by severity, quiet when there's nothing to say:

```
ecat-config-check — leg (Legrand US, org 273)     status: onboarding

CONTRADICTIONS  2
  order email    send_order_email_on_submit=true but order_email_recipient is empty
  custom fields  13 registered with send_to_ipad, 9 used as filters, 0 populated
                 rohscompliant, Color, voltage, wattage, switchtype, workswith,
                 wiresize, mountingtype, prop65, warranty, numberofswitches,
                 bulbcompatibility, numberofgangs

UNUSUAL         1
  user groups    Catalyst is shared_resources_auth='a' with 0 scoped resources
                 23 peer agency groups are 'c' with 96 — deviates from the pattern
                 (26 groups / 1 populated is DECLARED, not a finding)

NOT CHECKED     1
  FTP creds      no data source — cannot verify from the database
```

Three rules on the output:

- **`NOT CHECKED` is mandatory.** Anything the skill cannot see gets named with a reason.
  An unexplained absence is how a real gap becomes a silent pass — this is the same
  discipline as `preflight_gate.py`.
- **Never print a zero you didn't verify.** See the traps below.
- Silence on a clean org. If nothing is wrong, say so in one line.

---

## Traps that will bite you

All learned the hard way; full detail in `SESSION_HANDOFF.md`.

- **`territory_codes` empty is the literal string `'[]'`** — not `''`, not NULL. A `btrim(x) = ''` test returns 0 and reports "everyone has a territory" when nobody does.
- **`is_submitted` is nullable.** `WHERE is_submitted` silently drops rows.
- **Two login columns** — `last_ipad_login_at` *and* `last_ecat_online_login_at`. Checking one misreports any org with eCat Online.
- **`use_as_filter` is a varchar** (`'multi'`, `'binary'`, `''`), not a boolean. `COALESCE(use_as_filter, false)` throws.
- **`customers.company_name` does not exist.** It's `customers.name`.
- **Two orgs are named "legrand"** — live is `leg` id 273; `lna` id 93 is an inactive 2015 org.
- **Always scope by `organization_id`.** `audit_log_entries` is a 13M-row global table.

---

## Out of scope for this session

- The ingestion / data-transformation agent. It has a spec (`BUILD_SPEC.md` §§ 2–3) and it comes later.
- Anything in eve. eve cannot reach Postgres — split-horizon DNS, verified. Deploying anything there needs a snapshot bridge built first, and that comes after this skill is trusted.
- Writes of any kind.
- Re-running the blind audits. They're done; five clients, `ground-truth/clients/`.

---

## Definition of done

- `~/.claude/skills/ecat-config-check/SKILL.md` exists and follows the house style
- Run clean against all five test orgs
- Every rule carries the reason it exists — ideally the incident behind it
- Kylor has seen the output for all five and stopped finding surprises
- `NOT CHECKED` honestly lists what it can't see

Then the next thing is the session-prep skill, which is mostly assembly of
`collector/corpus.py` and `collector/rawstate.py`.
