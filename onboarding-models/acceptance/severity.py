#!/usr/bin/env python3
"""F6 — one severity ladder, stage, demotion, repair channels, org-state header.

Implements `ground-truth/SPEC_F6_severity.md`. Every module imports from here;
no module decides its own vocabulary any more.

## Decision 1 — three severities, and FATAL retires

    BLOCKING  someone must act before this goes further
    WARN      worth a human's attention; not a stop
    INFO      measured, deliberately reported, not a defect

`FATAL` is gone as a HARNESS severity. Not because BUILD_SPEC §3.1 and §3.2 are
the same concern — the difference between them is `stage` (Decision 2) — but
because `fatal` is already the IMPORTER's word: `import_log.py` computes
`CASE WHEN n_fatal>0 THEN 'fatal'` for import blocks. Two live meanings for one
word in one codebase makes "was that finding fatal?" ambiguous.

`NOT CHECKED` and `DECLARED` are NOT severities. They have no position on the
ladder, they never demote, and they are counted separately from findings.

## Decision 3 — demotion applies to CLOSED evidence only

    demote one level when: evidence_state == 'closed'
                           AND a repair opportunity occurred at or after the
                               evidence ended, on the declared channel

The closed-evidence clause is load-bearing. Without it `leg`'s B4 finding
demotes: its alternation WINDOW is 2026-08-05..09-03 and the last Inventory
import is 09-04, so a naive "evidence older than the last relevant import"
demotes A8 to WARN. **For a standing condition the most recent import is part
of the evidence, not a chance to have fixed it.** That is the regression test
for this whole item.

## Decision 4 — repair_channel, verified before it is declared

    file:<type>    a later import of that file type repairs it
    admin:<table>  a later updated_at on that table repairs it
    none           nothing the operator does repairs this

`admin:custom_fields` was VERIFIED before being declared, per the spec: across
the 13-org cohort `custom_fields.updated_at` is non-null on 13 of 13 and
diverges from `created_at` on 11 of 13, so it is genuinely maintained rather
than a create-time backfill. `orders.price_level` gets `none`: a historical
order's price-level string is immutable and no operator action repairs it, so
the finding says demotion does not apply instead of appearing to have been
evaluated.
"""

import datetime

LADDER = ['BLOCKING', 'WARN', 'INFO']
NON_LADDER = ('NOT CHECKED', 'DECLARED')
STAGES = ('pre_upload', 'post_import')


def demote_one(level):
    """One step down the ladder. INFO is the floor; demotion never reaches
    NOT CHECKED, which is a statement about method, not a weaker finding."""
    if level not in LADDER:
        return level
    i = LADDER.index(level)
    return LADDER[min(i + 1, len(LADDER) - 1)]


# --------------------------------------------------------------------------
# rule -> (stage, repair_channel, default evidence_state)
#
# A rule absent from here is a bug: `meta()` raises rather than guessing, so a
# new rule cannot ship without someone deciding these three things about it.
RULE_META = {
    'A1.zero_overlap':                ('pre_upload',  'none',                'standing'),
    'A1.mass_delete':                 ('pre_upload',  'none',                'standing'),
    'A1.rival_org':                   ('pre_upload',  'none',                'standing'),
    'A1.empty_org':                   ('pre_upload',  'none',                'standing'),
    'A1.absent_records':              ('pre_upload',  'none',                'standing'),

    'A2.placeholder_pricing':         ('post_import', 'file:products',       'standing'),
    'A2.near_constant_pricing':       ('post_import', 'file:products',       'standing'),
    'A2.not_evaluated':               ('post_import', 'none',                'standing'),

    # A3's channel is per reference class - see a3_channel(). Price levels are
    # Admin objects; products taxonomy and related items come from products.csv.
    'A3.dangling_reference':          ('post_import', None,                  'closed'),
    'A3.coverage':                    ('post_import', 'none',                'standing'),

    'B1a.empty_field':                ('post_import', 'file:products',       'standing'),
    'B1a.sparse_field':               ('post_import', 'file:products',       'standing'),
    'B1b.unregistered_populated':     ('pre_upload',  'admin:custom_fields', 'standing'),
    'B1b.unregistered_empty':         ('pre_upload',  'admin:custom_fields', 'standing'),

    'B3.territory_codes_empty':       ('post_import', 'file:customers',      'standing'),
    'B3.no_customers':                ('post_import', 'file:customers',      'standing'),

    'B5.no_display_field_registered': ('post_import', 'admin:custom_fields', 'standing'),
    'B5.config_data_mismatch':        ('post_import', 'admin:custom_fields', 'standing'),
    'B5.negative_on_hand':            ('post_import', 'file:inventory',      'standing'),
    'B5.no_inventory':                ('post_import', 'file:inventory',      'standing'),
    'B5.agrees':                      ('post_import', 'file:inventory',      'standing'),
    'B5.partition_mismatch':          ('post_import', 'none',                'standing'),

    'A4.option_order_within_event':   ('post_import', 'file:option_groups',  'closed'),
    'A4.membership_window':           ('post_import', 'file:option_groups',  'closed'),
    'A4.membership_nulled_now':       ('post_import', 'file:option_groups',  'standing'),

    # B4's channel and evidence_state are computed per finding from the file
    # type and whether the pair is still active - see check_b4.
    'B4.two_feeds':                   ('post_import', None,                  None),

    'D19.at_risk':                    ('post_import', 'none',                'standing'),

    'header.no_users_ever':           ('post_import', 'none',                'standing'),
    'header.users_dropped':           ('post_import', 'none',                'closed'),
    'header.no_recent_import':        ('post_import', 'none',                'standing'),
}


def a3_channel(reference):
    """A3's repair channel depends on which reference class dangled."""
    if reference.startswith('customers.'):
        return 'file:customers'
    if reference.startswith('products.'):
        return 'file:products'
    # orders.price_level: the order's stored string is immutable and the level
    # is gone. No import and no Admin edit repairs a historical order, so this
    # is honestly `none` rather than keyed on whatever ran last.
    return 'none'


def meta(rule):
    if rule not in RULE_META:
        raise KeyError(
            'rule %r has no F6 metadata. Every finding must declare stage, '
            'repair_channel and evidence_state - add it to RULE_META rather '
            'than defaulting, because a default here is a decision nobody made.'
            % rule)
    return RULE_META[rule]


def stamp(f, evidence_from=None, evidence_to=None,
          repair_channel=None, evidence_state=None):
    """Attach the F6 record to a finding. Mutates and returns it."""
    stage, chan, state = meta(f['rule'])
    f['stage'] = stage
    f['repair_channel'] = repair_channel or chan or 'none'
    f['evidence_state'] = evidence_state or state or 'standing'
    f['evidence_from'] = evidence_from
    f['evidence_to'] = evidence_to or evidence_from
    return f


# --------------------------------------------------------------------------

def _key(s):
    """Fold a file type or table name to a comparison key: lowercase, and
    spaces/hyphens as underscores. 'Option Groups' == 'option_groups'."""
    return str(s).strip().lower().replace(' ', '_').replace('-', '_')


def _as_date(v):
    if v is None:
        return None
    if isinstance(v, datetime.date) and not isinstance(v, datetime.datetime):
        return v
    if isinstance(v, datetime.datetime):
        return v.date()
    s = str(v)[:10]
    try:
        return datetime.date.fromisoformat(s)
    except ValueError:
        return None


def repair_opportunity(channel, org_state):
    """Latest moment the declared channel could have repaired the finding."""
    if not channel or channel == 'none':
        return None
    kind, _, name = channel.partition(':')
    # `import_events` carries 'Option Groups' and 'Product Stories'; the declared
    # channels are 'file:option_groups'. Normalise case AND separators, because a
    # silent miss here is indistinguishable from "no repair opportunity" and
    # quietly stops demotion from ever firing. It did: the first run of this
    # returned 0 demotions on all 73 A4 windows because 'option groups' never
    # matched 'option_groups'.
    src = ('last_import_by_type' if kind == 'file'
           else 'admin_touched' if kind == 'admin' else None)
    if src is None:
        return None
    by = {_key(k): v for k, v in (org_state.get(src) or {}).items()}
    return _as_date(by.get(_key(name)))


def apply_demotion(findings, org_state):
    """Decision 3. Returns (findings, moves) with `moves` naming every change."""
    moves = []
    for f in findings:
        if f['severity'] in NON_LADDER:
            f['demotion'] = 'not on the ladder'
            continue
        if f['severity'] == 'INFO':
            f['demotion'] = 'INFO is the floor'
            continue
        if f.get('evidence_state') != 'closed':
            f['demotion'] = ('standing evidence - demotion does not apply; the most '
                             'recent activity is part of this finding, not a chance '
                             'to have fixed it')
            continue
        chan = f.get('repair_channel') or 'none'
        if chan == 'none':
            f['demotion'] = ('repair_channel none - nothing the operator does repairs '
                             'this, so demotion does not apply')
            continue
        repair_at = repair_opportunity(chan, org_state)
        ev_end = _as_date(f.get('evidence_to'))
        if repair_at is None:
            f['demotion'] = 'no repair opportunity recorded on %s' % chan
            continue
        if ev_end is None:
            f['demotion'] = 'evidence has no end date; not demoted'
            continue
        if repair_at >= ev_end:
            was = f['severity']
            f['severity'] = demote_one(was)
            f['demotion'] = ('demoted %s -> %s: evidence closed %s and %s ran %s'
                             % (was, f['severity'], ev_end, chan, repair_at))
            moves.append((f['rule'], was, f['severity'],
                          'D3 closed-evidence demotion via %s' % chan))
        else:
            f['demotion'] = ('closed %s but %s has not run since; not demoted'
                             % (ev_end, chan))
    return findings, moves


# --------------------------------------------------------------------------
# Decision 5 — the org-state header

def sql_header(org_ref_sql):
    """Org state. Printed on EVERY report, clean or not.

    Three requirements, each from something that already cost us:

    (a) NEVER vs DROPPED. "0 users" reads identically for a pre-launch org and
        one that lost forty last month. `login_events` survives user deletion -
        it denormalises username, name and user_group_name - so it can say
        which. This makes the header the first consumer of login_events,
        closing part of D13/D16.

    (b) NAME THE CLOCK. G4: `orders.submit_date` is the business event,
        `orders.created_at` is the row, and they diverge by up to 4,751 days at
        `ufi`. Show both, always. Same for login: iPad and eOL are two surfaces
        (D14), and measuring one misreports any org with eOL.

    (c) STATE THE DEFINITION. provisioned / ever-logged-in / active-in-30d are
        three different numbers. A count whose definition is private is how
        "10 reps" happened.
    """
    o = org_ref_sql
    return """
SELECT
  (SELECT name FROM organizations WHERE id = {o})                       AS org_name,
  (SELECT id FROM organizations WHERE id = {o})                         AS org_id,
  (SELECT properties->>'status' FROM organizations WHERE id = {o})      AS status,
  -- STAFF EXCLUSION. `users.billable = false` is the schema's own internal-seat
  -- flag; `@supercatsolutions.com` catches staff seats that ARE billable (test
  -- and demo accounts provisioned inside a client org). NEITHER alone is
  -- enough, which is why this is a union - see STAFF_DEFINITION.
  (SELECT count(*) FROM org_users ou WHERE ou.organization_id = {o})    AS provisioned_all,
  (SELECT count(*) FROM org_users ou JOIN users su ON su.id = ou.user_id
    WHERE ou.organization_id = {o}
      AND (NOT COALESCE(su.billable,false)
           OR su.email ILIKE '%@supercatsolutions.com'))                AS staff_seats,
  (SELECT count(*) FROM org_users ou JOIN users su ON su.id = ou.user_id
    WHERE ou.organization_id = {o}
      AND COALESCE(su.billable,false)
      AND NOT su.email ILIKE '%@supercatsolutions.com')                 AS provisioned,
  (SELECT count(*) FROM org_users ou JOIN users su ON su.id = ou.user_id
    WHERE ou.organization_id = {o}
      AND COALESCE(su.billable,false)
      AND NOT su.email ILIKE '%@supercatsolutions.com'
      AND (ou.last_ipad_login_at IS NOT NULL
        OR ou.last_ecat_online_login_at IS NOT NULL))                   AS ever_logged_in,
  (SELECT count(*) FROM org_users ou JOIN users su ON su.id = ou.user_id
    WHERE ou.organization_id = {o}
      AND COALESCE(su.billable,false)
      AND NOT su.email ILIKE '%@supercatsolutions.com'
      AND (ou.last_ipad_login_at > now() - interval '30 days'
        OR ou.last_ecat_online_login_at > now() - interval '30 days'))  AS active_30d,
  (SELECT string_agg(su.email, ', ' ORDER BY su.email)
     FROM org_users ou JOIN users su ON su.id = ou.user_id
    WHERE ou.organization_id = {o}
      AND (NOT COALESCE(su.billable,false)
           OR su.email ILIKE '%@supercatsolutions.com'))                AS staff_seat_emails,
  (SELECT max(ou.last_ipad_login_at)::date FROM org_users ou
     WHERE ou.organization_id = {o})                                    AS last_ipad_login,
  (SELECT max(ou.last_ecat_online_login_at)::date FROM org_users ou
     WHERE ou.organization_id = {o})                                    AS last_eol_login,
  -- (a) never vs dropped
  (SELECT count(DISTINCT le.user_id) FROM login_events le
     WHERE le.organization_id = {o})                                    AS login_event_users,
  (SELECT count(DISTINCT le.user_id) FROM login_events le
     WHERE le.organization_id = {o}
       AND NOT EXISTS (SELECT 1 FROM org_users ou2
                        WHERE ou2.organization_id = {o}
                          AND ou2.user_id = le.user_id))                AS users_since_removed,
  (SELECT max(le.created_at)::date FROM login_events le
     WHERE le.organization_id = {o})                                    AS last_login_event,
  -- (b) both clocks, always
  (SELECT max(od.submit_date)::date FROM orders od
     WHERE od.organization_id = {o} AND COALESCE(od.is_submitted,false)) AS last_order_submitted,
  (SELECT max(od.created_at)::date FROM orders od
     WHERE od.organization_id = {o} AND COALESCE(od.is_submitted,false)) AS last_order_row_written,
  (SELECT count(*) FROM orders od
     WHERE od.organization_id = {o} AND COALESCE(od.is_submitted,false)) AS orders_submitted,
  (SELECT max(e.created_at)::date FROM import_events e
     WHERE e.organization_id = {o})                                     AS last_import_any
""".format(o=o).strip()


STAFF_DEFINITION = """SuperCat staff seat, derived - never a hardcoded address list.

    staff  ==  users.billable IS FALSE  OR  email ILIKE '%@supercatsolutions.com'

Four candidate signals were TESTED against the fleet, not assumed:

  1. @supercatsolutions.com domain - NECESSARY, NOT SUFFICIENT. It misses 24
     staff accounts on personal or contractor domains, including
     `kylor22johnson@gmail.com`, an admin on 110 orgs. It is still needed,
     because 39 staff seats ARE marked billable (test/demo accounts provisioned
     inside a client org: chuck+911@, steve+53@, kyla+rep@, brent+demo2@).

  2. users.billable IS FALSE - CARRIES THE LOAD. 57 accounts, averaging 32.4
     orgs each, max 167; against 70,047 billable accounts averaging 1.6 orgs,
     max 17. The separation is sharp and it is the schema's own flag rather than
     an inference.

  3. Same person across many orgs - REFUTED for this domain, and it was the
     hypothesis that looked strongest. eCat's client-side population INCLUDES
     multi-line rep agencies and multi-brand dealers who legitimately hold
     accounts at many manufacturers: riccisales.com reaches 11 orgs,
     decorlightingsales.com 15, lightingvision@comcast.net 16. 2,982 accounts
     sit in 5+ orgs and are NOT staff. Using org-count as a staff signal would
     misclassify thousands of real client users.

  4. login_events.is_super_user - CONFIRMS, ADDS NOTHING. True for 10 accounts,
     all 10 already caught by the union above (0 additional). Useful as an
     independent corroboration that the union is not missing the obvious cases.

COVERAGE (BUILD_SPEC §3.4): 96 staff accounts classified fleet-wide, 70,008
client-side, 70,104 total - the partition sums. The residual risk is a staff
member on a personal domain holding a BILLABLE seat: that account is invisible
to both signals, and the only cross-check available - org count - is unusable
here for the reason in (3). The residual is unbounded but small; it is not zero
and this check does not claim it is."""


def _fmt(d):
    return str(d) if d else 'never'


def render_header(st, out):
    """Print the header. Always. A green report is structurally impossible
    because the org's state is on it whether or not anything is wrong."""
    w = out.write
    name = st.get('org_name') or '?'
    w('%s\n' % ('=' * 72))
    w('ecat-acceptance — %s (%s, org %s)     status: %s\n'
      % (st.get('shortname', '?'), name, st.get('org_id', '?'),
         st.get('status') or 'unknown'))
    w('%s\n' % ('=' * 72))

    prov = int(st.get('provisioned') or 0)
    ever = int(st.get('ever_logged_in') or 0)
    act = int(st.get('active_30d') or 0)
    seen = int(st.get('login_event_users') or 0)
    gone = int(st.get('users_since_removed') or 0)
    prov_all = int(st.get('provisioned_all') or (prov + int(st.get('staff_seats') or 0)))
    staff = int(st.get('staff_seats') or 0)

    # The definition travels WITH the number. A count whose definition is
    # private is how "10 reps" happened, and staff seats sit inside every raw
    # user count - `kylor22johnson@gmail.com` is an admin on 110 orgs on a
    # personal gmail address, so a domain filter alone does not find them.
    w('  users            %d client-side provisioned · %d ever logged in · '
      '%d active in 30d\n' % (prov, ever, act))
    w('                   STAFF-EXCLUDED: %d of %d org_users seats are SuperCat '
      'staff\n' % (staff, prov_all))
    w('                   staff = users.billable IS FALSE  OR  '
      'email @supercatsolutions.com\n')
    if st.get('staff_seat_emails'):
        w('                   excluded here: %s\n' % st['staff_seat_emails'])
    w('                   NOT the framework\'s "rep" (collector/queries.py::REPS),\n'
      '                    which is narrower again - it also drops admins, the\n'
      '                    DefaultUserGroup and disabled seats.\n')
    if seen or gone:
        w('  login history    %d distinct users seen in login_events'
          '%s · last %s\n'
          % (seen,
             ('; %d of them NO LONGER PROVISIONED' % gone) if gone else '',
             _fmt(st.get('last_login_event'))))
    w('  last login       iPad %s · eOL %s\n'
      % (_fmt(st.get('last_ipad_login')), _fmt(st.get('last_eol_login'))))

    imports = st.get('last_import_by_type') or {}
    w('  last import      any %s' % _fmt(st.get('last_import_any')))
    named = [(k, v) for k, v in sorted(imports.items()) if v]
    if named:
        w('  ·  ' + ' · '.join('%s %s' % (k, v) for k, v in named))
    w('\n')

    w('  orders           %s submitted · last submitted %s · last row written %s\n'
      % (st.get('orders_submitted', '?'),
         _fmt(st.get('last_order_submitted')),
         _fmt(st.get('last_order_row_written'))))
    if (st.get('last_order_submitted') and st.get('last_order_row_written')
            and st['last_order_submitted'] != st['last_order_row_written']):
        w('                   (the two clocks differ — submit_date is the business\n'
          '                    event, created_at is the row. G4.)\n')


def header_findings(st, measured_at, stale_import_days=60):
    """(c) The header carries findings of its own, on the same ladder."""
    out = []
    prov = int(st.get('provisioned') or 0)
    seen = int(st.get('login_event_users') or 0)
    gone = int(st.get('users_since_removed') or 0)
    status = (st.get('status') or '').strip()

    if prov == 0:
        if seen == 0:
            out.append(stamp({
                'rule': 'header.no_users_ever', 'measured_at': measured_at,
                'severity': 'WARN' if status == 'active' else 'INFO',
                'detail': 'no users have EVER been provisioned, and login_events has '
                          'no record of any either. This org has never been usable by '
                          'anyone. (Status %r.)' % (status or 'unknown'),
                'measured': 'org_users = 0 and login_events = 0 rows',
                'not_established': 'whether that is expected — a demo or a pre-launch '
                                   'org looks exactly like this.',
            }, evidence_from=measured_at))
        else:
            out.append(stamp({
                'rule': 'header.users_dropped', 'measured_at': measured_at,
                'severity': 'BLOCKING',
                'detail': 'NO users are provisioned now, but login_events records %d '
                          'distinct users who logged in, most recently %s. They were '
                          'removed. This is not a pre-launch org.'
                          % (seen, _fmt(st.get('last_login_event'))),
                'measured': 'org_users = 0; login_events holds %d distinct user_ids' % seen,
                'not_established': 'who removed them or why — that is audit_log_entries '
                                   '(D13), which nothing reads.',
            }, evidence_from=st.get('last_login_event')))
    elif gone:
        out.append(stamp({
            'rule': 'header.users_dropped', 'measured_at': measured_at,
            'severity': 'INFO',
            'detail': '%d user(s) appear in login_events but have no org_users row '
                      'today — provisioned, used the app, since removed. Their orders '
                      'carry org_user_id NULL rather than a dangling id, so any '
                      'group-by-creator read silently drops them.' % gone,
            'measured': '%d distinct login_events user_ids with no current org_users row'
                        % gone,
            'not_established': 'when or why each was removed — audit_log_entries (D13).',
        }, evidence_from=st.get('last_login_event')))

    last = _as_date(st.get('last_import_any'))
    if last:
        age = (datetime.date.today() - last).days
        if age > stale_import_days:
            out.append(stamp({
                'rule': 'header.no_recent_import', 'measured_at': measured_at,
                'severity': 'WARN',
                'detail': 'no import of any kind for %d days (last %s). The catalogue '
                          'in the app is whatever it was then.' % (age, last),
                'measured': 'max(import_events.created_at) = %s' % last,
                'not_established': 'whether that is wrong — a stable catalogue on a '
                                   'mature org legitimately stops importing.',
            }, evidence_from=last))
    return out
