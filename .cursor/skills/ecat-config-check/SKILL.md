---
name: ecat-config-check
description: Read-only configuration audit of a SuperCat org by shortname — finds settings that are wrong, missing, or contradictory (order email on with no recipient, filters registered with no values, a user group that deviates from the pattern its peers follow, stored ids that no longer resolve, territory codes emptied). Use when checking an org's Admin Console configuration, assessing go-live config readiness, or diagnosing "it imported clean but the app is wrong."
---

# eCat Config Check (consultant-only, read-only)

Answers one question for one org:

> **What about this org's configuration is wrong, missing, or contradictory?**

`organizations` carries 92 settings columns, plus taxonomies, price levels, user types,
custom fields and report formats. There is no checklist and no diff, so settings get
forgotten. A five-client audit found seven live defects; most were configuration, not data.

**Read-only. No writes of any kind** — not to Postgres (the `supercat-postgres-vpn` MCP is
SELECT-only anyway), not to the Admin Console. This reports; a human acts. When a finding
needs applying, hand off to `ecat-admin-write`; this skill never calls it, so the line
between reporting and acting stays visible.

Requires the VPN. Use `ecat-postgres-audit` for general org state; this skill is
specifically the config layer.

## Two kinds of check, weighted unequally

1. **Contradictions** — two settings that cannot both be right. Cheap to detect, nothing
   else checks them, and every rule below is a real incident. **This is the prize.**
2. **Prevalence** — is a setting unusual against the 127-org cohort. Weaker evidence;
   report the value, and only call it an anomaly where the cohort is lopsided.

Weight the output accordingly: a contradiction outranks any prevalence line.

**Before reporting anything, read `onboarding-models/config_intent.toml`** — § 4. Declared
configuration prints as `DECLARED` and never as a finding.

## 0. Resolve the org first

```sql
select id, shortname, name, properties ->> 'status' as status
from organizations where shortname = '<shortname>';
```

Lifecycle lives in `properties->>'status'`, never in `organizations.state` (that is the
geographic state). **Two orgs are named "legrand"** — live is `leg` id 273; `lna` id 93 is
an inactive 2015 org. Scope every subsequent query by `organization_id`.

Note the status. Some thresholds below are **go-live rules and must not fire at full weight
on an org still in `onboarding`** — see § 6.

## 0.1 Any user count is staff-excluded, and says so

**We hold accounts on nearly every org.** An unfiltered user count measures our own
presence alongside the client's. The rule, derived and tested rather than assumed
(OPEN_ITEMS A27, resolved 2026-09-05):

```sql
-- staff = users.billable IS FALSE  OR  email ILIKE '%@supercatsolutions.com'
not (u.billable is false or u.email ilike '%@supercatsolutions.com')   -- client-side
```

**Both halves earn their place.** The domain half catches the staff seats provisioned
inside client orgs and marked billable (`chuck+911@`, `steve+53@`, `kyla+rep@`,
`brent+demo2@`, `sarah+test@`). The `billable` half catches staff on personal or
contractor domains that a domain filter misses — including `kylor22johnson@gmail.com`,
`is_admin = true`, member of 110 orgs, which is the admin account on both `leg` and `mer`.
Either half alone undercounts.

Fleet, verified live 2026-09-09 over users provisioned into at least one org:
**97 staff** (34 both signals · 24 billable-only · 39 domain-only) against **70,040
client-side**, total 70,137. A27 recorded 96 / 70,008 on 2026-09-05; the rule reproduces
and the drift is one new staff account in four days. `login_events.is_super_user`
corroborates independently — 10 accounts, none missed.

**Proportional damage is worst on small onboarding orgs** — the ones this skill runs on
most: `sp` −41% of provisioned users, `leg` −29%, `mer` −25%. `mer`'s "2 users logged in"
is really **1**.

Two hard rules:

- **The definition travels with the number.** Every count states that it is staff-excluded
  and names the rule. A staff-excluded count reported bare is indistinguishable from an
  unfiltered one, and the next reader will compare it against a raw Admin Console figure.
- **Never use org-count as a staff signal. It is refuted** (A28). eCat's client-side
  population includes multi-line rep agencies and multi-brand dealers who legitimately
  hold accounts at many manufacturers — `riccisales.com` up to 11 orgs,
  `decorlightingsales.com` up to 15, `lightingvision@comcast.net` 16.
  **2,982 client accounts sit in 5+ orgs and none of them are staff.** `billable`
  separates where org-count does not: the 57 non-billable accounts average 32.4 orgs,
  the 70,047 billable average 1.6.

**Residual, named rather than zeroed:** a staff member on a personal domain holding a
billable seat is invisible to both signals. Say so when the count is load-bearing.

## 1. Contradictions

### 1.1 Order email on, no recipient

Orders submit and the email goes nowhere. Live at `mali` for months; was live at `leg`
until it was fixed (recipient is now `legrand.cs@legrand.us` — the kickoff doc still lists
`leg` as broken and is out of date). Live right now at `ufi` (37,814 orders) and `fms`
(17,088 orders), both `true` with an empty recipient — **this fires on mature transacting
orgs, not just onboarding ones.**

```sql
select send_order_email_on_submit,
       coalesce(nullif(btrim(order_email_recipient),''),'(empty)') as recipient,
       coalesce(nullif(btrim(backup_order_email_recipient),''),'(empty)') as backup
from organizations where id = :org_id;
```

Fire when `send_order_email_on_submit` is true and `order_email_recipient` is blank.
**Cohort context: 25 of the 121 orgs with the flag on have no recipient** — this is
systemic, not exotic. Still report it per-org; it is still broken.

#### Is the recipient the *right* address?

A separate, weaker check: `drf` sat on the client contact's own address for 32+ days after
it was flagged. Worth a line — but **never compare the domain to the org's name.** Org names
are brands and clients are often the parent company. `mer` is "111Mercer" and its order mail
goes to `jen.dolan@tempaper.com`, which reads as a stranger's address until you notice all
three client users are `@tempaper.com`: 111Mercer is a Tempaper brand and the recipient is
correct. The name test produced a confident false positive on the first org it met.

**Compare against the org's own evidence instead** — the domains its users actually use, and
the contact details it carries:

```sql
with norm as (
  select o.id,
         lower(split_part(o.order_email_recipient,'@',2)) as recipient_domain,
         lower(split_part(nullif(btrim(o.company_email),''),'@',2)) as company_domain,
         -- strip scheme, www. and any path: 'https://www.legrand.us/' -> 'legrand.us'
         lower(regexp_replace(regexp_replace(coalesce(o.company_website,''),
               '^https?://(www\.)?','','i'), '/.*$','')) as website_domain
  from organizations o where o.id = :org_id
)
select n.recipient_domain, n.company_domain, n.website_domain,
       (select string_agg(distinct lower(split_part(u.email,'@',2)), ', ')
          from org_users ou join users u on u.id = ou.user_id
         where ou.organization_id = :org_id and not coalesce(ou.disabled,false)
           -- staff-excluded per 0.1: the domain test alone leaks a staff account on a
           -- personal or contractor domain into the client-domain set, which would
           -- whitelist a recipient by our own presence
           and not (u.billable is false
                    or u.email ilike '%@supercatsolutions.com')
           and lower(split_part(u.email,'@',2)) not in (
             'gmail.com','outlook.com','yahoo.com','icloud.com','hotmail.com',
             'live.com','aol.com','msn.com','me.com','sbcglobal.net')) as client_domains
from norm n;
```

- Recipient domain matches `company_domain`, `website_domain`, or any `client_domains`
  entry → **correct, say nothing.** (`mer` → matches its users' `tempaper.com`, silent.
  `leg` → matches `legrand.us` only after the website is normalized, silent.)
- Matches none of them → **one `UNUSUAL` line showing the comparison**, no verdict.
  (`uhc` → recipient `uniwarehs@gmail.com` while the org carries
  `sales@uniwarehouseware.com`; 20,032 orders have gone through the gmail, so it works —
  but the org's own record disagrees with it. Declared in `config_intent.toml`.)
- `@supercatsolutions.com` → **always fire.** Our address is never the client's order desk.

**Both exclusions in that query are load-bearing, and both were found by running it:**

- **Normalize the website before comparing.** `leg` stores `https://www.legrand.us/` and
  sends to `legrand.us`. A raw string compare calls that a mismatch and reports a correct
  configuration as a defect.
- **Drop `supercatsolutions.com` from the client-domain set.** Our consultants hold accounts
  on nearly every org, so leaving it in would whitelist a `@supercatsolutions.com` recipient
  by our own presence — defeating the rule directly above it.

Consumer domains are excluded for the same reason: individual reps log in from
`aol.com`, `sbcglobal.net` and `live.com` across `fal` and `ufi`, and counting those as
client domains would whitelist exactly the addresses this check exists to find.

### 1.2 Photo-gated sync with imageless products

`product_synch_requires_photo = true` means a product without an image **never reaches the
iPad while still counting as active**. Rare (6 of 127) and always deliberate, so the flag
is not the defect — the imageless products under it are.

```sql
select o.product_synch_requires_photo,
       count(*) filter (where not p.deleted) as active_products,
       count(*) filter (where not p.deleted and not coalesce(p.image_exists,false)) as no_image
from organizations o join products p on p.organization_id = o.id
where o.id = :org_id group by 1;
```

Fire only when the flag is true and `no_image > 0`. Report the count as *silently invisible
to reps*, not as "missing images." When the flag is false, `no_image` is informational.

### 1.3 Custom fields registered but never populated

A field registered with `send_to_ipad` and used as a filter, carrying zero values, is
**worse than absent** — it ships a filter chip that returns nothing. At `leg`, 13 fields
warned on 2026-07-23, went clean 61 minutes later, and remain empty across all 1,020
products; `# of Gangs` had been announced to the client as enabled.

Values live in `products.ecat_custom_field_N`; `custom_fields.db_column_name` names the
column. Resolve it through `to_jsonb` rather than dynamic SQL:

```sql
select cf.field_name, cf.label, cf.send_to_ipad, cf.use_as_filter,
       count(*) filter (where nullif(btrim(to_jsonb(p) ->> cf.db_column_name), '') is not null) as populated,
       count(*) as of_products
from custom_fields cf
join products p on p.organization_id = cf.organization_id and not p.deleted
where cf.organization_id = :org_id
  and cf.field_type = 'custom' and cf.db_column_name is not null
group by 1,2,3,4 order by populated asc, cf.field_name;
```

**The `field_type = 'custom'` filter is not optional.** Rows with `field_type = 'alias'`
are display relabels for built-in inventory quantities ("Qty On Hand", "Qty Available");
they carry a NULL `db_column_name`, so `to_jsonb(p) ->> NULL` returns NULL and every one
of them counts as empty. Without the filter `mali` reports 13 empty fields when the real
number is 3 — 10 working inventory aliases wrongly named as defects.

Fire on `populated = 0` where `send_to_ipad` is true. Count how many of those are filters
separately — **`use_as_filter` is a varchar** (`'multi'`, `'binary'`, `''`), not a boolean,
so test `nullif(btrim(use_as_filter),'') is not null`. `COALESCE(use_as_filter, false)`
throws.

A partially-populated filter (say 40 of 1,020) is a judgement call, not a defect — report
the ratio, no verdict.

### 1.4 A user group that deviates from the pattern its peers follow

**This check replaced an empty-group count on 2026-09-03. Do not put that back.** The old
rule reported "26 groups, 1 populated" at `leg` as scaffolding. That was wrong: the 24
agency groups are deliberate per-agency Library scoping, and the reading cost real
credibility (SCORECARD § 12 R2). **Group count is never a finding, empty groups are never a
finding, and fleet prevalence is the wrong lens.** The right question is whether a group
conforms to the pattern **its own org's peers** follow.

**Step 1 — split into cohorts.** An admin/default group is correctly "all access", so it
must never be scored against client groups. Classify by name:

```sql
select ut.id, ut.name,
  case
    when lower(btrim(ut.name)) ~ '(^|[^a-z])(z-supercat|supercat)([^a-z]|$)' then 'supercat'
    when lower(btrim(ut.name)) ~ '(^|[^a-z])(admin|admins|administrator|internal|default|defaultusergroup)([^a-z]|$)' then 'admin'
    else 'client'
  end as cohort,
  ut.shared_resources_auth as sr_auth,
  (select count(*) from shared_resources_user_types x where x.user_type_id = ut.id) as sr_scoped,
  ut.customer_synching,
  -- staff-excluded per 0.1; an unfiltered count here measures our own presence
  (select count(*) from org_users ou join users u on u.id = ou.user_id
    where ou.user_type_id = ut.id and not coalesce(ou.disabled,false)
      and not (u.billable is false
               or u.email ilike '%@supercatsolutions.com')) as client_users,
  (select count(*) from org_users ou join users u on u.id = ou.user_id
    where ou.user_type_id = ut.id and not coalesce(ou.disabled,false)
      and (u.billable is false
           or u.email ilike '%@supercatsolutions.com')) as staff_users
from user_types ut
where ut.organization_id = :org_id
order by cohort, ut.name;
```

The naming convention is read off the fleet, not invented. Across active/onboarding orgs:
`z-supercat` 75 orgs (72 at `auth='a'`), `defaultusergroup` 38 (38 at `'a'`), `admin` 27
(26), `admins` 16 (14). "All access" is the point of these groups.

**`z-SuperCat` is our own access group, not the client's.** Drop it from the maths
entirely rather than exempting it, so it cannot skew a modal shape.

The query returns `client_users` and `staff_users` separately (§ 0.1) — the cohort split is
by group *name*, but a client-named group can still hold staff seats, and reporting a group
as populated on the strength of our own accounts is the same error one level down. Report
`client_users`; mention `staff_users` only when it is the sole reason a group looks
populated. **Group membership count is never itself a finding** — § 1.4 scores
`(shared_resources_auth, sr_scoped)` shape, not headcount (see § 8, 2026-09-03 R2).

**Step 2 — find the modal shape** of the `client` cohort over
`(shared_resources_auth, sr_scoped)`, and report members that deviate from it.

**Require ≥5 groups in the cohort before claiming a pattern exists.** Two points are not a
shape. Below the minimum, say so under `NOT CHECKED` with the count — never silently skip.

Verified behaviour:

| org | cohort | result |
|---|---|---|
| `leg` | 25 client | modal `('c', 96)` ×23 → **`Catalyst` `('a', 0)`** and **`Futura` `('c', 95)`**, and nothing else |
| `ufi` | 17 client | modal `('a', 0)` ×15 → `Retailer -standard`, `eCat Online` — both DECLARED, § 4 |
| `uhc` | 2 client | below minimum → `NOT CHECKED` |
| `fal` | 2 client | below minimum → `NOT CHECKED` |
| `mer` | 0 client | `DefaultUserGroup` is admin cohort → nothing to check |

Phrase a deviation as **"deviates from the pattern its N peers follow"** — never as "empty",
"unconfigured", or "scaffolding". Those words are what got this wrong the first time.

**A near-miss is the stronger signal.** `Futura` at 95 of 96 resources is a shape reached by
accident; `Catalyst` at `('a', 0)` could conceivably be a decision. Rank the near-miss
higher and say why.

### 1.5 Stored ids that no longer resolve

**Nothing anywhere validates that a stored reference still resolves.** `pebl` has 12 orders
worth $264,130 against a deleted price level.

**Split by recency (added 2026-09-03).** A price code retired years ago, still stamped on
the orders it priced, is what history looks like — not a defect. The same code appearing on
*recent* activity means orders are being written today against something that does not
resolve. That is the `pebl` incident. The data has a clear joint in it, so this is not a
tuned threshold: `pebl`'s dangling level was last used 83 days ago, while `ufi`'s twelve
retired codes were last used in 2019 or earlier (~1,600+ days). Use **180 days**.

```sql
-- orders against a price level the org no longer has, with recency
select o.price_level, count(*) as orders,
       min(o.created_at)::date as first_order,
       max(o.created_at)::date as last_order,
       (current_date - max(o.created_at)::date) as days_since_last,
       sum(coalesce(o.total,0))::numeric(14,2) as value
from orders o
where o.organization_id = :org_id
  and nullif(btrim(o.price_level),'') is not null
  and not exists (select 1 from price_levels pl
                  where pl.organization_id = o.organization_id and pl.code = o.price_level)
group by 1 order by days_since_last;
```

- `days_since_last <= 180` → **CONTRADICTION**, one line per code, with orders and value.
- older → **one collapsed informational line**: how many codes, how many orders, and the
  date they went quiet. Naming thirteen retired codes as thirteen findings is how a
  checklist gets ignored.

Live example — `ufi`: `H` fires (71 orders, last 2026-08-05), and the other twelve collapse
to *"12 further codes unresolvable, none used since 2019."*

**Current-state pointers are never recency-gated** — they describe the org now, not its
history, so a dangling one is always a defect:

```sql
-- customers against a price code the org no longer has
select c.default_price_code, count(*)
from customers c
where c.organization_id = :org_id
  and nullif(btrim(c.default_price_code),'') is not null
  and not exists (select 1 from price_levels pl
                  where pl.organization_id = c.organization_id and pl.code = c.default_price_code)
group by 1;

-- eOL site pointing at a price level that is gone, or belongs to another org
select ms.id, ms.price_level_id,
       (select code from price_levels pl where pl.id = ms.price_level_id) as resolves_to,
       (select organization_id from price_levels pl where pl.id = ms.price_level_id) as belongs_to_org
from mobile_sites ms where ms.organization_id = :org_id and ms.price_level_id is not null;
```

`resolves_to` null, or `belongs_to_org` different from the org, is the defect. `mali` had a
site on price level 5722, which existed in no organization; **that is now fixed** — both
mali sites resolve within org 285 as of 2026-09-03.

### 1.6 Territory codes empty where rep filtering is expected

`pebl`: all 171 emptied on 2026-07-30 by a customer re-import, turning rep↔customer
filtering off org-wide. If reps report seeing every customer, this is why.

```sql
select count(*) as customers,
       count(*) filter (where territory_codes is null) as nulls,
       count(*) filter (where btrim(territory_codes) = '[]') as empty_brackets,
       count(*) filter (where btrim(territory_codes) = '') as empty_string,
       count(*) filter (where territory_codes is null
                          or btrim(territory_codes) in ('','[]')) as no_territory
from customers where organization_id = :org_id;
```

**The empty value is the literal string `'[]'`** — not `''`, not NULL. A `btrim(x) = ''`
test returns 0 and reports "everyone has a territory" when nobody does. This bug was live
in the audit tooling itself and cost a near-miss. The query above decomposes the three
encodings deliberately: **that is how you earn the right to print a zero here.**

Fire when `no_territory > 0` and any user group is set to associated-customers-only:

```sql
select name, customer_synching from user_types where organization_id = :org_id;
```

If every group shows all customers, territory codes are unused by design — report the
count, no verdict.

### 1.7 No iPad report formats configured

```sql
select count(*) from ipad_reports where organization_id = :org_id;
```

**Fire only at 0.** The go-live checklist asks for ≥3, and `tcd` shipped with 1 — but the
checklist number and the defect threshold are different things. One configured report is
fine and is not a blocker (Kylor, 2026-09-03). The old ≥3 rule would have flagged `uhc`
every run: active, 20,032 orders, 1 format, working fine for years. That is exactly the
noise that trains a reader to skip the output.

**Go-live rule — demote, do not suppress, on an `onboarding` org.** See § 6.

## 2. Prevalence

Cohort is the 127 orgs at `status in ('active','onboarding')`. Verified live 2026-09-03.

| Setting | On | How to report |
|---|---|---|
| `send_order_email_on_submit` | 121 / 127 (95%) | **Off is an anomaly** — one line, check why |
| `enable_sales_data` | 97 (76%) | Common default; off is worth a mention only with other signals |
| `mobile_enabled` | 67 (53%) | Per-client — **value only, never a verdict** |
| `enrollment_enabled` | 57 (45%) | Per-client — value only |
| `contract_pricing_enabled` | 42 (33%) | Per-client — value only |
| `imports_options` | 34 (27%) | Per-client; should follow the options build |
| `product_synch_requires_photo` | 6 (5%) | Rare and deliberate — never flag the flag, only § 1.2 |
| `enable_rep_activity` | 4 (3%) | Rare — a line if on |
| `hide_order_totals` | 2 (1.6%) | Rare — a line if on |

**Dead flags — never report these at all**, on or off: `use_modern_ui` (1 org),
`enable_data_import3` (0), `enable_image_import2` (0), `import_active` (0 of 257).
Noise is how a checklist gets ignored.

Do not re-derive these percentages per run; they took a cohort survey to produce and move
slowly. Re-survey only if a number looks wrong.

## 3. Output shape

Terminal-readable, grouped by severity, quiet when there is nothing to say.

```
ecat-config-check — leg (Legrand US, org 273)     status: onboarding
user counts: staff-excluded (billable IS FALSE OR @supercatsolutions.com) — 11 of 38 excluded

CONTRADICTIONS  2
  custom fields  13 registered with send_to_ipad, 9 used as filters, 0 populated
                 rohscompliant, Color, voltage, wattage, switchtype, workswith,
                 wiresize, mountingtype, prop65, warranty, numberofswitches,
                 bulbcompatibility, numberofgangs
  photo gate     product_synch_requires_photo=true, 2 active products have no image
                 those 2 never reach the iPad but still count as active

UNUSUAL         2
  user groups    Futura  'c' with 95 scoped resources; its 23 peers have 96
                 a near-miss is reached by accident, not by decision
  user groups    Catalyst  'a' with 0 scoped resources; its 23 peers are 'c' / 96

DECLARED        2
  library scoping   26 groups / 1 populated is per-agency by design (config_intent.toml)
  inventory field   qty_on_hand is the configured field; null qty_available is correct

NOT CHECKED     2
  FTP contents   no data source — cannot compare ImageFileName to disk from Postgres
  catalogue      only that it parsed; a clean import proves nothing about correctness
```

Four rules on the output:

- **`NOT CHECKED` is mandatory.** Anything the skill cannot see gets named with a reason.
  An unexplained absence is how a real gap becomes a silent pass — same discipline as
  `preflight_gate.py`. Standing entries are in § 5.
- **`DECLARED` is mandatory when anything was declared.** A reader must be able to see what
  was deliberately not flagged, or the exception file becomes an invisible mute button.
- **Never print a zero you didn't verify.** Every trap in § 7 produces a confident zero.
  If a count is 0, confirm the column and the empty-value encoding before reporting it.
  A query over an org with no rows returns **no row at all, not a zero** — `mer` has 0
  customers, so § 1.6 yields an empty result set. Say "no customers loaded", not "0 without
  territory codes".
- **Silence on a clean org.** If nothing is wrong, say so in one line. Do not pad.

## 4. Declared intent — `onboarding-models/config_intent.toml`

**The database shows structure. It cannot show intent.** Two findings in the source
documents were wrong for exactly this reason, and both reached a human as fact
(SCORECARD § 12). Read the file before reporting; anything declared prints as `DECLARED`
and never as a finding.

Rules:

- **A declaration needs a reason, and the reason is the point.** No reason, no declaration.
- **A "that's fine" goes in that file, never into a hardcoded exception here.** An
  exception in this skill applies to every org and cannot be argued with; a line in the
  TOML is scoped, dated, and reversible.
- Keys are org shortnames. `declared_deviations` lists user-group names exempt from § 1.4.

A checker that flags intentional configuration gets ignored by week two. This file is what
prevents that, which is why the review loop is the real work and not a formality.

### 4.1 How to read it — stdlib `tomllib`, and nothing else

The file was YAML until 2026-09-05. It is **TOML** now, and the format is not cosmetic:

- **`tomllib` is stdlib** (Python 3.11+). Nothing to install.
- **But `python3` on this machine is NOT 3.11+.** `/usr/bin/python3` is Apple's **3.9.6**
  and has no `tomllib`; `import tomllib` there raises `ModuleNotFoundError`. Verified
  2026-09-09. **Run this with an explicit interpreter:**

  ```bash
  /opt/homebrew/bin/python3.12   # 3.12.13, tomllib present — verified
  /opt/homebrew/bin/python3.13   # 3.13.13, tomllib present — verified
  ```

  There is no `/opt/homebrew/bin/python3` symlink, so a bare `python3` silently gets 3.9.
  **A bare `python3` is the PyYAML `ImportError` in a different costume** — same missing
  module, same temptation to catch it and continue with `{}`. Do not catch it: an
  interpreter without `tomllib` is a refusal (§ 4.2), not a degraded mode.
- **PyYAML is not installed and cannot be.** Homebrew's Python is externally managed
  (PEP 668), so `pip install` is refused. That wall is *why* the format changed.
- **YAML 1.1 — what `safe_load` implements — resolves bare `N`, `NO`, `ON`, `OFF` to
  booleans.** This config describes eCat, whose boolean tokens are literally `Y` and `N`.
  A declaration reading `boolean_dialect: N` would have silently become `False`. TOML has
  no implicit typing.

```python
import tomllib
with open('onboarding-models/config_intent.toml', 'rb') as fh:
    intent = tomllib.load(fh)          # note: binary mode
org_intent = dict(intent.get(shortname) or {})
```

**Never hand-roll a parser.** `acceptance/intent.py` shipped ~70 lines of strict-subset
parser that existed only because of a format choice; a bespoke parser drifts from its own
spec and the drift is silent. Those lines were deleted. `acceptance/intent.py` itself is
the working reference — read it before writing a loader here, and reuse
`load()` / `for_org()` / `declarations_for()` rather than restating them.

### 4.2 Fail closed, and loudly

**A missing declaration file is indistinguishable from an org with no declarations, and
that difference is the entire point of the file.** `collector.py::load_overrides` once
caught the PyYAML `ImportError`, warned to stderr and returned `{}` — which silently
converted every declared exception back into a finding.

**Refuse to run** if `config_intent.toml` is missing, parses as empty, or is malformed
(`tomllib.TOMLDecodeError`). Do not fall back to "no declarations". Report the refusal as
the result:

```
ecat-config-check — leg (Legrand US, org 273)          REFUSED TO RUN

  declared-intent file unreadable: onboarding-models/config_intent.toml
  <missing | parsed as empty | not valid TOML: line N, col M>

  Refusing to audit without it. An absent declaration file reads identically to
  "this org declared nothing", so every retraction in § 8 would fire again as a
  fresh finding. Fix the file, or re-run with --no-intent and read § 4.3.
```

### 4.3 The opt-out flag stamps every line

`--no-intent` is the only way to proceed without declarations, it must be passed
explicitly, and it is never the default. When it is set, **every line of the report
carries the stamp** — not just a header, which scrolls away:

```
ecat-config-check — leg (Legrand US, org 273)     status: onboarding
!! --no-intent: declarations NOT applied. Every line below is unfiltered. !!

CONTRADICTIONS  2
  [NO-INTENT] custom fields  13 registered with send_to_ipad, 9 used as filters, 0 populated
  [NO-INTENT] photo gate     product_synch_requires_photo=true, 2 active products no image

UNUSUAL         3
  [NO-INTENT] inventory field  qty_available null on 1,204 products
              ^ this is leg's declared configuration and is NOT a defect — see § 8 R1
```

A run under `--no-intent` **reproduces the two findings this project already retracted**
(§ 8: `leg` inventory field, `leg` library scoping). One of them was reported to the client
as broken, was not true, and the client reacted badly. The stamp is what stops that output
from being read as an audit.

### 4.4 The DECLARED block always prints

Print it **even when the org declared nothing** — `no declarations for <org> in
config_intent.toml`. A silent block is unreadable two ways: it cannot be distinguished
from a skipped read, and a suppressed finding nobody can see is worse than the finding.

Only five orgs currently declare anything — `leg`, `mer`, `uhc`, `pebl`, `drf`. For every
other org the correct DECLARED block is the "no declarations" line, not an absent block.

A declared key that no criterion here reads is still real intent: print it as
**`RECORDED, CONSUMED BY NOTHING`** rather than implying coverage that does not exist.
`library_scoping`, `parent_company` and `order_email_domain` are in that state today.

## 5. Standing NOT CHECKED entries

Name these every run unless the check was actually performed:

- **FTP contents** — no data source. `ImageFileName` cannot be compared byte-for-byte to
  what is on FTP from Postgres. `pebl` ran 18 days of clean image imports with doubled
  `.jpg.jpg` extensions that could never match.
- **Whether the catalogue is *correct*** — only that it parsed. Confirmed on `drf`, `mali`
  and `leg`: nine clean imports at `leg` while 13 announced filters sat empty; 86 clean
  image imports at `mali` over ~200 wrong photos. **A clean import proves the file parsed
  and nothing else.** This is a property of the data, not a gap to close.
- **Admin Console state with no column** — order origins, email templates and report
  content are partly JSONB or absent; check the console directly.
- **Intent** — nothing records what the client asked for. A setting can be wrong-for-them
  and indistinguishable from correct here. § 4 narrows this; it does not close it.
- **Group conformance below the cohort minimum** — § 1.4 needs ≥5 client groups. Name the
  count so a reader knows the check was skipped rather than passed.
- **Staff on a personal domain holding a billable seat** — invisible to both halves of the
  § 0.1 rule. Every user count here is "staff-excluded to the limit of that rule", not
  "staff-free". Name it whenever a count carries weight.

## 6. Status gates

`mer` (0 customers, 0 report formats, 1 user group) is mid-build, not broken. Firing
go-live thresholds at an onboarding org produces noise that trains the reader to skip the
output.

**Gating demotes, it never hides.** A gated finding moves from `CONTRADICTIONS` to
`UNUSUAL` and is phrased as state, not fault — "0 report formats, none built yet" rather
than "fails the go-live checklist." Suppressing it entirely would hide a real gap behind
a status field, which is the `NOT CHECKED` failure in a different costume.

- **Gated on `status = 'onboarding'`:** § 1.7 (report formats) and any "not yet configured"
  line.
- **Never gated:** § 1.1, § 1.2, § 1.3, § 1.4, § 1.5, § 1.6. These are wrong at any stage —
  a dangling id or an empty announced filter is a defect the day it appears.

## 7. Traps — every one produces a confident wrong zero

- **`territory_codes` empty is the literal `'[]'`**, not `''` or NULL.
- **`is_submitted` is nullable.** A bare `WHERE is_submitted` or
  `count(*) FILTER (WHERE is_submitted)` silently drops rows — `mali`'s only order row is
  NULL and vanishes. Use `coalesce(is_submitted,false)` and report the NULL count.
- **`use_as_filter` is a varchar**, not a boolean. So is `user_types.hide_order_totals`.
- **Two login columns** — `last_ipad_login_at` *and* `last_ecat_online_login_at`. Checking
  one misreports any org with eCat Online; 4 of 5 `mali` ML Reps are eOL-only.
- **`customers.company_name` does not exist.** The column is `customers.name`.
- **`user_types` has no `disabled` column** — the flag is `org_users.disabled`, and it is
  nullable, so `not coalesce(ou.disabled,false)`.
- **Custom field values are `products.ecat_custom_field_1..180`**, mapped through
  `custom_fields.db_column_name`. There is no `products.custom*` column.
- **`custom_fields` holds two kinds of row.** `field_type='custom'` maps to a product
  column; `field_type='alias'` is an inventory-quantity relabel with a NULL
  `db_column_name`. Counting values for an alias always returns 0. Filter to `'custom'`.
- **`custom_fields.field_name` is nullable** — alias rows have only a `label`. Report the
  label and fall back to it when naming fields.
- **An empty result set is not a zero.** See § 3.
- **Always scope by `organization_id`.** `audit_log_entries` is a 13M-row global table.
- **Two orgs named "legrand"** — `leg` 273 live, `lna` 93 inactive.

## 8. Review log

Every rule here carries the reason it exists. These are the ones that were argued about,
with who decided and when — so a later reader knows which thresholds are settled and which
have never been tested.

| Date | Rule | Verdict |
|---|---|---|
| 2026-09-03 | § 1.4 empty user groups | **Removed.** Replaced with peer-pattern conformance. The old rule reproduced the retracted § 12 R2 finding. |
| 2026-09-03 | § 1.4 admin cohort | Identify admin/default groups by fleet naming convention, not by whether they have users. Kylor: *"there should be some kind of coherent way to understand an admin user group."* Convention verified across 127 orgs. |
| 2026-09-03 | § 1.7 report formats | Threshold **3 → 1**. Kylor: *"as long as there is one report configured that is fine and shouldn't be a blocker."* |
| 2026-09-03 | § 1.5 dangling ids | Recency split at 180 days. Confirmed against `pebl` (83 days, fires) and `ufi` (12 codes ≥1,600 days, collapsed). |
| 2026-09-03 | `ufi` group deviations | Reported as `UNUSUAL`; **no declaration written.** Kylor declined to declare them without a confirmed reason. The check keeps flagging them until someone knows why they differ. |
| 2026-09-03 | § 1.1 recipient domain | **Gated.** Compare the domain to the org's own user domains and contact details, never to its name. The name test false-positived on `mer` the first time it ran. |
| 2026-09-03 | `mer` / `uhc` recipients | Declared in `config_intent.toml`. `mer` is correct (Tempaper is the parent). `uhc` is an accepted mismatch, not a correct setting — recorded as such. |
| 2026-09-05 | § 4 intent file format | **YAML → TOML.** PyYAML is not installed and cannot be (PEP 668, Homebrew Python externally-managed); `tomllib` is stdlib. YAML 1.1 also coerces bare `N`/`NO`/`OFF` to booleans, and eCat's boolean tokens are literally `Y`/`N`. Hand-rolled parser deleted — see § 4.1. |
| 2026-09-05 | § 4 missing intent file | **Fail closed.** Was: warn and return `{}`, which silently reconverted every declaration into a finding. Now refuses to run; `--no-intent` is the explicit opt-out and stamps every line (§ 4.2–4.3). |
| 2026-09-09 | § 4.1 interpreter | **Name the interpreter explicitly.** `import tomllib` fails on this machine's default `python3` (Apple 3.9.6, no `tomllib`); only Homebrew `python3.12`/`3.13` carry it, and there is no bare `python3` symlink to them. Found by running the skill, not by reading it. |
| 2026-09-05 | § 0.1 user counts | **Staff-excluded, always**, by `billable IS FALSE OR @supercatsolutions.com` (A27). Both halves load-bearing. Org-count as a staff signal **refuted** (A28) — 2,982 client accounts sit in 5+ orgs because multi-line rep agencies hold accounts at many manufacturers. |

**Not yet reviewed:** § 1.1 placeholder-recipient heuristic (what counts as a placeholder),
§ 1.3 partial-population ratio (no threshold set, deliberately), § 2 prevalence lines on an
org that is neither active nor onboarding.
