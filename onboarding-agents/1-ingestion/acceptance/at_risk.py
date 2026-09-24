#!/usr/bin/env python3
"""D19 — the at-risk state, with the guard that kept it from shipping.

## What D1 found and D19 broke

D1 (SCORECARD §3) is the highest-value finding of the whole programme: the
framework has no vocabulary for a client going BACKWARDS. `tcd`'s
`core_types_60d` fell to 1 for most of March 2026 — exactly the near-churn
window the blind read found independently from the conversation record — and a
weekly run would have reported a silent, unchanged "Phase 3".

v3.6 added an at-risk state. **D19 is a defect in that fix**, and it is why the
state was never shipped:

> `organizations.created_at` is not the project start. `leg`'s org was created
> 2025-06-10 for a pre-sales demo; the project began 2026-06-19. Run against
> `leg`, the at-risk rule would have raised PHASE_REGRESSED continuously from
> September 2025 to June 2026 — **nine months of escalation about a client that
> had not signed.**

## The guard, and it is the whole point

    NO project_start_date  ->  NOT CHECKED. Never fall back to created_at.

Falling back IS the bug. `created_at` is available, plausible, and wrong, and a
rule that quietly uses it looks like it ran. Six of the thirteen cohort orgs have
no derivable start date and this check declines on all six rather than inventing
one.

`project_start_date` lives in `overrides.toml`, which until 2026-09-05 could not
be read at all: `load_overrides` caught the PyYAML ImportError and returned `{}`,
so `leg`'s value — populated since D19 was written — was silently inert. That is
why this check is only now buildable.

## The measurement

`core_types_60d`: how many of the six core file types have an import inside the
last 60 days. Phase 3 clause 1 requires **>= 2**.

    BLOCKING  regressed: previously reached >= 2, now below it
    INFO      holding at exactly 2 - the threshold with no margin
    INFO      healthy
    NOT CHECKED  no project_start_date, or today is before it

Two things this deliberately does NOT do. It does not compute a phase — that is
the framework's job, not the harness's. And it does not treat "no imports at
all" as regression on its own: an org that never reached 2 never regressed, it
just has not started.
"""

import datetime

CORE_TYPES = ('Products', 'Customers', 'Inventory',
              'Product Stories', 'Options', 'Option Groups')
WINDOW_DAYS = 60
CLAUSE_MIN = 2


def _d(v):
    if v is None:
        return None
    if isinstance(v, datetime.datetime):
        return v.date()
    if isinstance(v, datetime.date):
        return v
    try:
        return datetime.date.fromisoformat(str(v)[:10])
    except ValueError:
        return None


def check(shortname, last_import_by_type, project_start_date,
          ever_reached_min, measured_at=None, today=None):
    """One finding. `ever_reached_min` says the org once had >= 2 core types
    live at the same time - without it, "below 2" is a start, not a regression.
    """
    import severity as sev
    today = _d(today) or datetime.date.today()
    measured_at = measured_at or today.isoformat()
    start = _d(project_start_date)

    if start is None:
        return sev.stamp({
            'rule': 'D19.at_risk', 'severity': 'NOT CHECKED',
            'measured_at': measured_at,
            'detail': 'NOT CHECKED - no project_start_date for %r in '
                      'overrides.toml. The at-risk rule is NOT evaluated, and it '
                      'deliberately does NOT fall back to organizations.created_at: '
                      'that fallback is D19, and on `leg` it would have raised '
                      'PHASE_REGRESSED for nine months about a client that had not '
                      'signed. Supply a start date or accept that this org is '
                      'unassessed.' % shortname,
            'measured': 'nothing - the check declined',
            'not_established': 'whether this org has regressed. Populate '
                               'overrides.toml § project_start_date from the '
                               'HubSpot closed-won date of the ORIGINAL onboarding '
                               'deal (not an expansion or renewal).',
        }, evidence_from=measured_at)

    if today < start:
        return sev.stamp({
            'rule': 'D19.at_risk', 'severity': 'NOT CHECKED',
            'measured_at': measured_at,
            'detail': 'NOT CHECKED - project has not started (start %s, today %s).'
                      % (start, today),
            'measured': 'project_start_date = %s' % start,
            'not_established': 'anything about regression before a project begins.',
        }, evidence_from=measured_at)

    cutoff = today - datetime.timedelta(days=WINDOW_DAYS)
    live = sorted(t for t in CORE_TYPES
                  if (_d((last_import_by_type or {}).get(t)) or datetime.date.min) >= cutoff)
    n = len(live)
    days_in = (today - start).days
    spec = ', '.join('%s %s' % (t, _d(last_import_by_type[t])) for t in live) or 'none'

    if n < CLAUSE_MIN and ever_reached_min:
        level, rule_txt = 'BLOCKING', (
            'REGRESSED. %d of the 6 core file types imported in the last %d days '
            '(need >= %d). This org previously reached the threshold and has '
            'fallen below it.' % (n, WINDOW_DAYS, CLAUSE_MIN))
    elif n < CLAUSE_MIN:
        level, rule_txt = 'INFO', (
            'below the threshold (%d of 6 core types in %d days, need >= %d) but '
            'has NEVER reached it - that is a start, not a regression.'
            % (n, WINDOW_DAYS, CLAUSE_MIN))
    elif n == CLAUSE_MIN:
        level, rule_txt = 'INFO', (
            'holding at exactly %d core types in %d days - the threshold with NO '
            'margin. One feed stopping puts this org at risk.' % (n, WINDOW_DAYS))
    else:
        level, rule_txt = 'INFO', (
            'healthy: %d of 6 core types imported in the last %d days.'
            % (n, WINDOW_DAYS))

    return sev.stamp({
        'rule': 'D19.at_risk', 'severity': level, 'measured_at': measured_at,
        'detail': '%s Project started %s (%d days ago), from '
                  'overrides.toml - NOT organizations.created_at. Types in window: %s.'
                  % (rule_txt, start, days_in, spec),
        'measured': 'core_types_60d = %d; cutoff %s; specimen: %s' % (n, cutoff, spec),
        'not_established': 'the org\'s PHASE. This measures one clause of Phase 3, '
                           'not the phase model, and D10 stands: a clean import '
                           'proves the file parsed and nothing about whether it '
                           'was right.',
    }, evidence_from=str(cutoff), evidence_to=measured_at,
       evidence_state='standing')
