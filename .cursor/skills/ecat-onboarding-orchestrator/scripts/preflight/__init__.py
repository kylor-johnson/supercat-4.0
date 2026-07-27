"""Read-only pre-import checks for the eCat file family (Phase 1 gate).

Every module here is a *gate*, not a brain: deterministic, independently runnable, and
incapable of writing. A validator may never modify a deliverable — see
IMPLEMENTATION_PLAN.md 5.1/5.2.

    core     severity tiers, CSV primitives, the Report renderer
    limits   two-tier field lengths, generated from supercat_server (never typed)
    flags    CLIENT_PROFILE.md -> archetype + applicability, so skips print as SKIP
    files    the file family: delete semantics and mandatory import order
    checks/  one module per check in the Phase 1 table
"""
