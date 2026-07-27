"""One module per check in the Phase 1 table (IMPLEMENTATION_PLAN.md 7).

Every module exposes `CHECK` (its name in the output), `SUBSYSTEM` (which
applicability flag can switch it off), and a `run(...)` returning a list of
`core.Finding`. None of them writes anything, ever.
"""
