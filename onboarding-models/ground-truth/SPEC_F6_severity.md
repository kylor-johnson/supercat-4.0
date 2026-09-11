# F6 — severity, stage, and the org-state header

**Written 2026-09-05.** This is the spec the harness session is waiting on. It supersedes
whatever each module decided for itself.

---

## The three problems being solved

**1. Severity is defined three ways across five modules.**

```
a4_b4.py         FATAL  WARN  INFO
b1_fields.py     BLOCKING  WARN            <- no INFO: cannot say "measured, not a defect"
state_checks.py  BLOCKING  WARN  INFO
a1_fingerprint.py  none of these — prints its own shape
import_log.py      none — but computes the IMPORTER's tier, which is a different vocabulary
```

**2. A finding cannot say when its evidence is from.** `sp`'s surviving B4 finding is a
window in **September 2021** reported at the same weight as something live. G4 established
that "age" is not one dimension in this schema; nothing in the harness consumes that yet.

**3. Only B3 varies by whether anyone is affected.** This is why the cold read came back
green on an org with zero users and no import in 57 days.

---

## Decision 1 — three severities, and `FATAL` retires

| level | means |
|---|---|
| `BLOCKING` | someone must act before this goes further |
| `WARN` | worth a human's attention; not a stop |
| `INFO` | measured, deliberately reported, not a defect |

**`FATAL` is removed as a harness severity.** Not because §3.1 and §3.2 are the same
concern — they aren't — but because the difference between them is **stage, not severity**
(Decision 2), and because `fatal` is already the importer's own word. `import_log.py`
computes `CASE WHEN n_fatal>0 THEN 'fatal'` for import blocks, and a harness that also
emits `FATAL` makes "was that finding fatal?" ambiguous in a codebase where both meanings
are live. One word, one meaning.

Every module gains all three levels, `b1_fields.py` included. A module with no INFO tier
cannot report a measurement it does not consider a defect, which is how B1b came to return
`exit 1` on a file that was fine (§G3).

`NOT CHECKED` and `DECLARED` are **not severities.** They are statements about method and
about intent respectively, they have no position on the ladder, and they are counted
separately from findings — as the 175 / 2 / 26 split already does. Keep that.

---

## Decision 2 — stage is orthogonal to severity

BUILD_SPEC §3.1 is *"the file must not be produced"*; §3.2 is *"fix before sending to the
client."* Same weight, different moment: one can still be prevented, the other has landed.
Collapsing them into a severity loses the action.

Every finding carries:

```
stage:  pre_upload | post_import
```

`A1` and `B1b` are `pre_upload`. Everything else is `post_import`. A `BLOCKING` at
`pre_upload` means **stop, do not upload**; a `BLOCKING` at `post_import` means **remediate
what is already live.** The operator needs both words to know which.

---

## Decision 3 — demotion applies to closed evidence only

Findings age. A finding whose evidence predates a repair opportunity may already be fixed,
and reporting it at full weight trains the operator to skim.

```
demote one level when: the evidence is CLOSED
                       AND a repair opportunity occurred after the evidence ended
```

**Closed evidence** — a window that ended, a superseded state, a historical order.
**Standing evidence** — a condition true right now.

**This clause is load-bearing and its absence was a real bug in the first draft of this
spec.** Without it, `leg`'s B4 finding demotes: its alternation window is 2026-08-05 →
09-03, the last Inventory import is 09-04, so "evidence older than the last relevant
import" fires and A8 drops to WARN. For a standing condition **the most recent import is
part of the evidence, not a chance to have fixed it.**

| check | evidence | demotes? |
|---|---|---|
| `B4` live alternation | standing | never |
| `A4.membership_nulled_now` | standing | never |
| `B3` territory codes empty now | standing | never |
| `A4.membership_window` (restored) | closed | yes |
| `A3` dangling refs on old orders | closed | yes |
| `B4` `sp` Products, Sept 2021 | closed | yes |

`INFO` does not demote further. Demotion never crosses into `NOT CHECKED`.

---

## Decision 4 — every check declares a `repair_channel`

"The last relevant import" is undefined for about half the checks. `A3`'s orders dangle
because a price level was deleted in Admin — no file import could have fixed it, so the
demotion rule either no-ops silently or keys on whatever import happened to run last. Both
are worse than not demoting.

```
repair_channel:  file:<type>   e.g. file:inventory, file:products
                 admin:<table> e.g. admin:custom_fields
                 none          nothing the operator does repairs this
```

Demotion fires only against the declared channel: a **later import of that file type**, or
a later `updated_at` **on that table**. Where the channel is `none`, the finding says
*demotion does not apply* rather than appearing to have been evaluated.

**Verify before speccing a channel as `admin:`.** If the table has no usable timestamp —
check `custom_fields` first — the honest channel is `none`, and the finding says so. A rule
that looks like it ran and didn't is the failure mode this whole item exists to remove.

---

## Decision 5 — the org-state header, and it is what actually answers the cold read

Every report opens with the org's state, **printed whether or not anything is wrong**. This
is the structural fix: a green report becomes impossible, because the state is always
there to be read.

```
ecat-acceptance — leg (Legrand US, org 273)          status: onboarding

  users            41 provisioned · 38 ever logged in · 12 active in 30d
  last login       2026-09-04  (iPad 2026-09-04 · eOL 2026-08-29)
  last import      2026-09-04  Inventory · products 2026-08-27
  orders           last submitted 2026-09-02 · last row written 2026-09-04
```

Three requirements, each from something that has already cost us:

**(a) Distinguish _never_ from _dropped_.** "0 users" reads identically for a pre-launch org
and for one that had 40 last month. The cold-read org was the first case and the header
must be able to say which. This makes the header the first consumer of `login_events`,
closing part of D13/D16.

**(b) Name the clock on anything time-shaped.** G4: `orders.submit_date` is the business
event, `orders.created_at` is the row, and they diverge by up to 4,751 days at `ufi`.
Show **both**, always. They differ on four of the thirteen orgs. Same discipline for login:
`last_ipad_login_at` and `last_ecat_online_login_at` are two surfaces (D14).

**(c) State the definition or disclaim it.** "Users" must say provisioned vs. ever-logged-in
vs. active-in-window, or say the framework does not define it. A count whose definition is
private is how "10 reps" happened.

**The header can itself carry findings.** Zero users, or no import in 57 days, is a finding
about the org — emitted from the header, at the ladder above, not left implicit in a blank.

---

## The finding record

```
severity        BLOCKING | WARN | INFO
stage           pre_upload | post_import
repair_channel  file:<type> | admin:<table> | none
evidence_from   date or [start, end]
evidence_state  standing | closed
measured        what was counted, with a specimen
not_established what this finding does NOT claim
```

`measured` / `not_established` are already the house style in `a4_b4.py` after F7 — this
makes them structural rather than a convention one module happens to follow.

---

## Definition of done

1. One severity vocabulary across all five modules; `FATAL` gone; every module has INFO.
2. `stage` on every finding; `A1` and `B1b` are `pre_upload`.
3. Demotion implemented, **closed evidence only**, and `leg`'s B4 finding still reports at
   `BLOCKING` after it. That is the regression test for this item — if A8 demotes, the
   clause was dropped.
4. `repair_channel` declared per check, with `admin:` channels verified to have a usable
   timestamp and downgraded to `none` where they don't.
5. Org-state header on every report, all three requirements met, printing on clean orgs.
6. Re-run thirteen orgs. Report the new distribution and **name every finding whose level
   changed, with which decision moved it.** The total is expected to move; unattributed
   movement is not acceptable.
