# profiles/ — per-client report profiles (reading-contract input #2)

> **What this is.** One `*.md` per client that pins the **stable, settled context** for that org so the report's
> *interpretation layer* stops re-deciding it on every run. It is **reading-contract input #2** in
> [`../CANON.md`](../CANON.md) — loaded after `foundation/provenance_spine.md` and before
> `knowledge/industry_context.md` — and it sits **just below the Spine in precedence**: the profile overrides
> industry defaults and a possibly-wrong source-data segment label, but it **never** overrides the Spine or the
> live numbers.

---

## Why a profile exists (anti-drift, anti-generic-bias)

The data layer is already deterministic — the SQL in `../foundation/query_library_v2.md` returns the same numbers
every run. Run-to-run variance comes from the **interpretation layer**, where an agent with no client context has
to guess at judgment calls that aren't pinned anywhere:

- business model (manufacturer / distributor / marketplace seller),
- whether a big account is a "marquee win" or a "concentration risk,"
- whether a low reorder rate is alarming or normal for this buyer base (e.g. designer-project),
- which accounts are house/sample and must be screened out of leakage (changes the headline dollar),
- org identity disambiguation (right `organization_id`, not a same-named sibling).

Every one of those is both a **drift source** (two runs diverge) and a **bias source** (the model fills the gap
with a generic prior). The profile freezes them once, as governed input, so the model consumes them instead of
re-inventing them. That is the whole anti-drift mechanism: **same operator + same profile + same data → same report.**

## The facts-only guardrail (what keeps a profile from *adding* bias)

A profile is only anti-bias if it carries **facts and scope decisions**, never **findings or framing**. A profile
that editorializes ("Wayfair is fine," "the team underperforms") would bake a conclusion into every run — exactly
the failure to avoid.

| Allowed (facts / scope decisions) | Forbidden (findings / framing) |
|---|---|
| Identity: `organization_id`, shortname, same-name disambiguation | Any dollar finding or YoY claim (the data generates these) |
| Business model / segment | A judgment that a number is good/bad |
| Channel model (how they sell) | Narrative, tone, or "the story this year" |
| House/sample/marketplace accounts to **screen** | A pre-written conclusion about a rep or account |
| Buyer-type context (e.g. designer-project) | Anything that should re-derive from the Spine + live data |
| Structural concentration **stated as context, not a finding** | A fixed dollar threshold that the gates already compute |
| Report-mode default + confirmed scope exclusions | |

If a line could change because the *numbers* changed, it does **not** belong in the profile — it belongs in the
live run.

## Workflow: derive → ratify → cache (not free-authored)

A profile is **not** written from imagination. The elite path keeps the human expert on the few real judgment calls:

1. **Derive a draft** from the deterministic preflight (`Q-ECON-00`, the identity/tier gate, channel + concentration
   queries) — the same queries the report operator runs in Step 1. The draft is facts read straight off the data.
2. **Human ratifies** the handful of scope decisions the data can't settle alone (which accounts are house/sample,
   the buyer-type read, identity disambiguation).
3. **Cache** the ratified file here as `profiles/{shortname}.md`. From then on the report operator loads it as
   input #2 and does not re-derive context. Re-ratify only when the business actually changes.

## Files

- `profile_template.md` — the strict, facts-only schema to copy for a new client.
- `{shortname}.md` — one ratified instance per client (e.g. `sarreid.md`).

A run with **no** profile for `{org}` must stop at the derive-draft step and request human ratification — the
report operator (`../operators/report_operator.md`) enforces this; it does not free-guess context.
