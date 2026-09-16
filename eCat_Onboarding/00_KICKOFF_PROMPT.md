# eCat Onboarding — Kickoff Prompt

Paste a filled-in version of the block below to start any client session. It points
the agent at the always-on rules, the right skill, and the client profile — so you
don't reload KB articles, field specs, or client context every time.

> Always-on rules (`ecat-ground-truth`, `ecat-import-ops`, `ecat-data-model`) and
> `.cursor/skills/ecat-*` live in **SuperCat Ops** (`~/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0`).
> Live client files live in **eCat Implementation**
> (`~/repos/ecat-onboarding-workspace` / iCloud `SuperCat_Simple_Final`)
> under `02_Implementation/<Client>/`.
>
> Keep the three-root `SuperCat.code-workspace` open so both load.
>
> **Do not recreate a live client folder under `eCat_Onboarding/`.**

---

## Copy / fill this

```
Client: <Client Name>  (org shortname: <shortname>)
Read first: 02_Implementation/<Client>/CLIENT_PROFILE.md and HANDOFF.md (if present).
Canonical tree: ~/repos/ecat-onboarding-workspace/02_Implementation/<Client>/
  (iCloud mirror: SuperCat_Simple_Final/02_Implementation/<Client>/)
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

Copy `_Template/` → `02_Implementation/<Client>/` in **ecat-onboarding-workspace**,
fill `CLIENT_PROFILE.md`, and work the phases in `LIFECYCLE_CHECKLIST.md`.
Do not create that folder under SuperCat 4.0 `eCat_Onboarding/`.
