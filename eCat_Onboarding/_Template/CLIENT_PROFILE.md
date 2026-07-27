# {Client Name} — eCat Client Profile

> The one file a new chat reads to get full context. Keep it current. Pair with
> `HANDOFF.md` (generated per session by the `ecat-session-handoff` skill).

## Identity
- **Org shortname:** `{shortname}`
- **Admin Console:** supercatsolutions.com/{SHORTNAME}
- **TradeNameCode:** `{CODE}`
- **Domain / vertical:** {e.g. furniture / lighting / fabric}
- **Status / stage:** {kickoff | build | import | review | go-live | maintenance}
- **Go-live / event:** {date, e.g. market/trade fair}

## Archetype & applicability

> Read by `scripts/preflight_gate.py`. Keep the field names exactly as written — the
> parser matches on them. These are **policy declarations**, never counts: counts come
> from the live DB, not from this file.

- **Archetype:** standard | snowflake | churned
- **Product line:** ecat-ipad | eol | sales-portal (comma-separate if more than one)
- **Flags:** {`pricing: n/a`, `inventory: n/a`, `options: none`, `customers: n/a`, `stories: none`, `sample-catalog`, or "none"}
- **File owner mode:** generator | csv | mixed
- **Image mode:** ftp | cdn-url | both
- **Source cutover date:** {YYYY-MM-DD — everything before this is POC/demo data and excluded from ground truth}
- **Sub-brands:** {e.g. ML,NSL — or "none"}

Rules that make these load-bearing rather than decorative:

- A flag makes a check print `SKIP (flag: ...)`. It never makes a check pass silently,
  because an unexplained absence is how "we don't do X for this client" gets forgotten.
- **Only declare a flag you can cite** — a call, a client email, or an explicit statement
  in this profile. An undeclared subsystem stays *checked*, which is the safe default.
- `snowflake` **annotates, it never blocks.** Unusual clients are still automated; the
  archetype just attaches a human checkpoint.
- **File owner mode is per deliverable, and never two owners for one file.** `generator`
  means the script owns it and every correction is codified in its config; `csv` means the
  CSV is the deliverable and the generator is retired with a tombstone. Dual ownership is
  what silently reverted hand-applied fixes at The CopperSmith.

## Contacts
- **Client:** {name, email, role}
- **SuperCat:** Kylor Johnson{, AE/CTO}

## Systems
- **ERP / PIM:** {e.g. Business Central, Catsy, Odoo}
- **Integration posture:** {manual FTP | recurring feed | API — tier}

## Taxonomy decisions
- **Method:** Standard (pre-create codes) | Auto-Create (strings become labels)
- **Collections → :** {what maps to CollectionCodes}
- **Categories → :** {what maps to CategoryCodes}
- **Custom fields:** {list, or "see Admin"}

## Pricing
- **Model:** {NetPrice only | imported levels | arithmetic | divisions}
- **Price levels (codes):** {dn, imap, ...}
- **Divisions:** {e.g. ML=mali, NSL=nsl}
- **List price hidden?** {yes/no — which groups}

## Images
- **Naming convention:** {...}
- **Which rows get images:** {e.g. base colors yes; WF/sample = `-`}

## Files & paths
- **Working folder:** eCat_Onboarding/{Client}/00_Import_Files/Ready_For_Import/
- **Current source of truth:** {latest file the client sent}
- **Reference (superseded):** {...}

## Snowflake quirks
- {Client-specific rules that bite — variant codes, sample SKUs, etc.}

## Import history
| Date | File | Rows | Result / notes |
|------|------|------|----------------|

## Open items / client confirmations
- [ ] {...}
