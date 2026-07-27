# eCat Onboarding — Kickoff Prompt

Paste a filled-in version of the block below to start any client session. It points
the agent at the always-on rules, the right skill, and the client profile — so you
don't reload KB articles, field specs, or client context every time.

> The always-on rules (`ecat-ground-truth`, `ecat-import-ops`, `ecat-data-model`) and
> the `.cursor/skills/ecat-*` skills live in the **SuperCat 4.0** workspace
> (`.cursor/`). Keep both workspace folders open so they load.

---

## Copy / fill this

```
Client: <Client Name>  (org shortname: <shortname>)
Read first: 02_Implementation/<Client>/CLIENT_PROFILE.md and HANDOFF.md (if present).
Task: <what we're doing today>.
Source file: <path to the latest file the client sent — this is the source of truth>.

Apply the always-on eCat rules. Use the skill(s) for this task:
- products/stories/inventory build → ecat-core-files
- customers → ecat-customers-build
- pricing/price levels/divisions → ecat-pricing-levels
- options + Option Mapping → ecat-options-and-mapping
- images / FTP / missing images → ecat-images-ftp
- smartlists → ecat-smartlists
- users/reps/territories/go-live → ecat-go-live
- client email/reply → ecat-client-email
- live DB audit → ecat-postgres-audit
- end of session → ecat-session-handoff (update CLIENT_PROFILE.md + HANDOFF.md)
```

---

## Reminders the rules already enforce (don't re-explain)

- Import order: options → option_groups → products → stories → inventory → customers.
- Delete semantics differ per file (products soft-delete; customers/inventory/options
  HARD-delete on omission) — send full files; deletes only run on a clean import.
- iPad only (not eOL/Portal). KB corrections live in `ecat-ground-truth`.

## New client?

Copy `_Template/` → `<Client>/`, fill `CLIENT_PROFILE.md`, and work the phases in
`LIFECYCLE_CHECKLIST.md`.
