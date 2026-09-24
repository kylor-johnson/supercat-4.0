#!/usr/bin/env python3
"""Declared configuration intent — F5. Loads `config_intent.toml` and applies it.

## The problem this fixes

`config_intent.toml` has existed for days, carries every "that's fine" answer
given during config review, and states in its own header:

    Anything declared here prints as DECLARED, never as a finding.

**Nothing printed anything, because no line of code loaded it.** A fleet grep
found five references, all prose in ground-truth documents. Every declaration
made in the last two weeks was inert.

## TOML, and why the hand-rolled parser is gone

Converted from YAML 2026-09-05. This module briefly shipped ~70 lines of
strict subset parser, which existed only because of a format choice and which
would have drifted from its own spec silently. Deleted.

  * `tomllib` is **stdlib** (Python 3.11+). Nothing to install.
  * PyYAML is not installed and **cannot be**: Homebrew's Python is externally
    managed (PEP 668), so `pip install` is refused. The Phase 2 session hit the
    same wall independently and reached the same answer.
  * YAML 1.1 — what PyYAML's `safe_load` implements — resolves bare `N`, `NO`,
    `ON` and `OFF` to booleans. This config describes eCat, whose boolean
    tokens are literally `Y` and `N`. A declaration reading
    `boolean_dialect: N` would have become `False` with nothing to notice it.
    TOML has no implicit typing.

## Fail CLOSED, and loudly

`collector.py::load_overrides` used to do the opposite: catch the PyYAML
`ImportError`, warn to stderr, return `{}`. Downstream that is
indistinguishable from "this org has no declarations", so a missing dependency
silently converted every declared exception back into a finding — including the
`project_start_date` that D19's at-risk fix depends on. Both loaders now raise.

  * If the file is missing, empty, or malformed, `load()` raises. Callers must
    decide to proceed WITHOUT declarations explicitly and say so in their
    output — never by default.

## What a declaration may and may not do

A declaration suppresses a *named rule at a named org* and must carry a reason.
It never suppresses a whole check, and it never applies fleet-wide — that is
the difference between this file and a hardcoded exception inside a skill,
which applies everywhere and cannot be argued with.

`DECLARATIONS` below is deliberately conservative: it maps only the rules whose
entire content is answered by the declaration. `drf`'s presentation-only
archetype answers "is this catalogue placeholder-priced" (yes, deliberately);
it does NOT answer "are these two registered filter chips empty" (they are, and
that is a real defect the archetype says nothing about).
"""

import os
import tomllib

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PATH = os.path.join(os.path.dirname(HERE), 'config_intent.toml')


class IntentError(RuntimeError):
    """Raised rather than returning an empty dict. See module docstring."""


# --------------------------------------------------------------------------
# declaration -> the rules it answers
#
# (declared_key, declared_value or None for "any") -> [rule ids], reason
# `None` as the value means the key's presence is enough.
DECLARATIONS = [
    (('archetype', 'presentation_only'),
     ['A2.placeholder_pricing', 'A2.near_constant_pricing'],
     'presentation-only archetype: catalogue is deliberately unpriced, pricing '
     'lives in the stories file'),
    (('pricing', 'not_used'),
     ['A2.placeholder_pricing', 'A2.near_constant_pricing'],
     'pricing declared not used at this org'),
    (('inventory_field', None),
     ['B5.no_display_field_registered', 'B5.config_data_mismatch'],
     'the inventory field this org displays is declared, so "which field does '
     'it show" is answered and does not need a finding'),
]

# Declared keys that are real intent but that NO §3 criterion currently reads.
# Listed so the DECLARED block can say "recorded, consumed by nothing" instead
# of implying coverage that does not exist.
UNCONSUMED_KEYS = {
    'library_scoping': 'user-group conformance — no §3 criterion reads user groups',
    'parent_company': 'email-domain checks live in the config-check skill, not §3',
    'order_email_domain': 'email-domain checks live in the config-check skill, not §3',
}


# --------------------------------------------------------------------------

def load(path=None):
    """Return {shortname: {key: value}}. Raises IntentError — never returns {}."""
    path = path or DEFAULT_PATH
    if not os.path.exists(path):
        raise IntentError(
            'declared-intent file not found: %s. Refusing to run without it: an '
            'absent declaration file is indistinguishable from an org with no '
            'declarations, and that difference is the whole point of the file.'
            % path)
    try:
        with open(path, 'rb') as fh:
            data = tomllib.load(fh)
    except tomllib.TOMLDecodeError as exc:
        raise IntentError(
            '%s is not valid TOML: %s. Refusing to continue - a declaration file '
            'that half-parses is how a declaration silently disappears.'
            % (path, exc)) from exc
    if not data:
        raise IntentError('%s parsed as empty. Refusing to treat that as "no '
                          'declarations" - see module docstring.' % path)
    return data


def for_org(intent, shortname):
    return dict(intent.get(shortname) or {})


def declarations_for(org_intent):
    """-> (suppressed_rules, shown, unconsumed).

    `shown` is every declaration with its reason, printed whether or not it
    suppressed anything. A suppressed finding nobody can see is worse than the
    finding.
    """
    suppressed, shown, unconsumed = {}, [], []
    for key, value in sorted(org_intent.items()):
        if key == 'note':
            continue
        if key in UNCONSUMED_KEYS:
            unconsumed.append((key, value, UNCONSUMED_KEYS[key]))
            continue
        matched = False
        for (dkey, dval), rules, reason in DECLARATIONS:
            if dkey != key:
                continue
            if dval is not None and str(value).strip() != dval:
                continue
            matched = True
            # First declaration to claim a rule owns it. Two keys can legitimately
            # cover the same rule - drf declares both `archetype:
            # presentation_only` and `pricing: not_used` - and attributing the
            # suppression to whichever happened to be written last would make the
            # DECLARED block report the wrong reason.
            already = [r for r in rules if r in suppressed]
            for r in rules:
                suppressed.setdefault(r, (key, value, reason))
            shown.append((key, value, reason, rules,
                          suppressed[already[0]][0] if already else None))
        if not matched:
            unconsumed.append((key, value, 'no §3 criterion maps this key'))
    return suppressed, shown, unconsumed


def apply(findings, suppressed, measured_at):
    """Rewrite matching findings to DECLARED. Returns (kept, declared)."""
    kept, declared = [], []
    for f in findings:
        hit = suppressed.get(f.get('rule'))
        if not hit:
            kept.append(f)
            continue
        key, value, reason = hit
        d = dict(f)
        d['severity'] = 'DECLARED'
        d['was'] = f['severity']
        d['declared_by'] = '%s: %s' % (key, value)
        d['detail'] = ('%s  [DECLARED %s: %s — %s. Was %s.]'
                       % (f['detail'], key, value, reason, f['severity']))
        declared.append(d)
    return kept, declared


def render(shown, unconsumed, suppressed, declared, org, out):
    """The DECLARED block. ALWAYS printed, including when empty."""
    w = out.write
    w('\n-- DECLARED INTENT %s\n' % ('-' * 53))
    if not shown and not unconsumed:
        w('   no declarations for %s in config_intent.toml\n' % org)
        return
    for key, value, reason, rules, owned_by in shown:
        w('   %-22s %s\n' % (key, value))
        w('     %s\n' % reason)
        w('     covers: %s\n' % ', '.join(rules))
        fired = [d for d in declared if d.get('declared_by') == '%s: %s' % (key, value)]
        if fired:
            for d in fired:
                w('     -> %s was %s, now DECLARED\n' % (d['rule'], d['was']))
        elif owned_by:
            w('     -> same rule(s) already declared above by %r; no double count\n'
              % owned_by)
        else:
            w('     -> nothing to declare this run (no matching finding fired)\n')
    for key, value, why in unconsumed:
        w('   %-22s %s\n' % (key, value))
        w('     RECORDED, CONSUMED BY NOTHING: %s\n' % why)
