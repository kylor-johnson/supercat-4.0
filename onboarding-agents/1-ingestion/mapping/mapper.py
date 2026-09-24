#!/usr/bin/env python3
"""The Phase 2 mapping engine — turns a declarative mapping into an eCat file.

The load-bearing division, from KICKOFF_mapping.md:

    The agent proposes the mapping and flags what it cannot map.
    The agent does not write transform code.

So this file is CLIENT-AGNOSTIC and is the only code that runs. Everything a
client needs is data in `<client>/<target>.toml`. A build produces a MAPPING,
not a script; the code is shared. That is the entire point of the phase.

The engine does three things and nothing else:

  1. load declared inputs (the primary table + keyed lookup tables)
  2. evaluate `derived` steps then `fields`, per row, in declared order
  3. run the whole-file passes: RelatedItems families, carry-forward, B6 diff

Every value-level operation delegates to `ecatlib`. If a mapping needs a
transform this engine cannot express, that is a SIGNAL, not a licence to write
Python here: either a primitive is missing from ecatlib (add it there, and the
next client gets it free) or it is a budgeted per-field escape hatch. See
MAPPING_FORMAT.md § The escape hatch.

Why TOML rather than YAML: see MAPPING_FORMAT.md § Why TOML. Short version —
stdlib `tomllib` means zero dependencies for a pipeline that has to run next to
the database inside the VPN, and YAML 1.1 parses the bare tokens `Y`, `N`, `NO`,
`ON` and `OFF` as BOOLEANS. This is a file format full of Y/N boolean dialects,
finish names and country codes. That is not a preference; it is the exact class
of silent rewrite this phase exists to stop.
"""

import os
import sys
import tomllib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

import ecatlib as lib  # noqa: E402


class MappingError(Exception):
    """A mapping that cannot be evaluated. Always names the field."""


# --- primitives -------------------------------------------------------------
# Name -> (callable, takes_dialect). The mapping names a primitive; it never
# names a Python function. Adding a primitive is an ecatlib change.

def _trim(v):
    return (v or '').strip()


PRIMITIVES = {
    'trim':          (_trim,                False),
    'money':         (lib.parse_money,      True),
    'weight':        (lib.parse_weight_lb,  True),
    'boolean':       (lib.to_boolean,       True),
    'date':          (lib.normalize_date,   True),
    'clean_text':    (lib.clean_text,       False),
    'clean_na':      (lib.clean_na,         False),
    'clean_country': (lib.clean_country,    False),
    'clean_lookup':  (lib.clean_lookup,     False),
    'split_first':   (lib.split_first,      False),
    'clean_integer': (lib.clean_integer,    False),
    'integer':       (lib.parse_int,        False),
    'round':         (lib.round_decimals,   False),
    'strip_tail':    (lib.strip_float_tail, False),
    'dimensions':    (lib.build_dimensions, True),
    'long_desc':     (lib.build_long_desc,  False),
    'short_desc':    (lib.build_short_desc, False),
    'variant_key':   (lib.variant_key_by_name, False),
}

# Primitives taking more than one source value. `apply` passes `args` in order.
MULTI_ARG = {'dimensions', 'long_desc', 'short_desc', 'variant_key'}

# Primitives returning (value, *flags). The value is field 0; the flags are
# recorded as report counters rather than silently dropped — build_long_desc's
# `finish_mismatch` is a source-quality contradiction between two columns and
# BUILD_SPEC's rule is to report it, not paper over it.
TUPLE_FLAGS = {'long_desc': ('truncated', 'finish_mismatch')}


class Report:
    """What the run observed. A mapping run that reports nothing is not
    trustworthy — every count here ships with a specimen (SKILL.md)."""

    def __init__(self):
        self.counters = {}
        self.specimens = {}
        self.warnings = []

    def count(self, key, specimen=None):
        self.counters[key] = self.counters.get(key, 0) + 1
        if specimen is not None and key not in self.specimens:
            self.specimens[key] = specimen

    def warn(self, msg):
        self.warnings.append(msg)

    def lines(self):
        out = []
        for key in sorted(self.counters):
            spec = self.specimens.get(key)
            out.append('  %-32s %6d   e.g. %s'
                       % (key, self.counters[key], spec if spec is not None else '(none)'))
        return out


# --- inputs -----------------------------------------------------------------

def _resolve(path, root):
    if not os.path.isabs(path):
        path = os.path.join(root, path)
    path = os.path.abspath(path)
    if not os.path.exists(path):
        raise MappingError('input not found: %s' % path)
    return path


def load_input(spec, root):
    """Load one declared input into either a row list or a keyed dict."""
    fmt = spec.get('format', 'csv')

    if fmt == 'csv':
        path = _resolve(spec['path'], root)
        rows = lib.read_rows(path, encoding=spec.get('encoding', 'utf-8-sig'))
        # A second header row is a LABEL row, not data. libco's spec master
        # carries eCat field names on row 1 and the client's own human labels on
        # row 2; reading it naively imports a product whose BaseItemCode is the
        # literal string "Item#".
        skip = spec.get('skip_rows_after_header', 0)
        if skip:
            rows = rows[skip:]
        if 'key' not in spec:
            return rows, path
        key, fields = spec['key'], spec.get('fields')
        out = {}
        for r in rows:
            k = (r.get(key) or '').strip()
            if not k:
                continue
            out[k] = {f: (r.get(f) or '').strip() for f in fields} if fields else r
        return out, path

    if fmt == 'csv_multi':
        # Two files into ONE importer slot. This is BUILD_SPEC B4 / OPEN_ITEMS
        # A8: leg's adorne and radiant inventory arrive as two daily
        # attachments and inventory.csv HARD-deletes and reloads, so whichever
        # lands second wins and only one brand's stock is in the app. The
        # mapping's answer has to be explicit -- here, UNION into one file.
        # Per-division files MERGE; they never compete (profiler REVIEW_LOG).
        rows = []
        for member in spec['files']:
            mpath = member['path']
            if not os.path.isabs(mpath):
                mpath = os.path.join(root, mpath)
            mpath = os.path.abspath(mpath)
            if not os.path.exists(mpath):
                raise MappingError('input member not found: %s' % mpath)
            with open(mpath, newline='',
                      encoding=spec.get('encoding', 'utf-8-sig')) as fh:
                raw = list(__import__('csv').reader(fh))
            # The header is NOT row 1: these exports carry a title row and a
            # blank row first. Locate it by content, never by index.
            marker = spec['header_at_first_cell']
            header_idx = None
            for i, r in enumerate(raw):
                if r and r[0].strip() == marker:
                    header_idx = i
                    break
            if header_idx is None:
                raise MappingError('%s: no header row whose first cell is %r'
                                   % (mpath, marker))
            header = raw[header_idx]
            for r in raw[header_idx + 1:]:
                if not r or not any(c.strip() for c in r):
                    continue
                rec = dict(zip(header, r))
                for k, v in member.get('tag', {}).items():
                    rec[k] = v
                rows.append(rec)
        return rows, ' + '.join(m['path'] for m in spec['files'])

    if fmt == 'csv_multi_named':
        """Union several sheets of ONE template BY HEADER NAME.

        The class-3 shape, and neither obvious union is safe:

          BY POSITION is wrong. tcs's Master and Weiyan sheets carry the same
          157 columns, but from index 99 the option block is REORDERED -- the
          four finish columns sit at 99-102 in Master and at 152-155 in Weiyan.
          A positional union pours Weiyan's `Wall Yoke` values into Master's
          `Matte Black` column: a mounting option silently becomes a finish.

          BY NAME ALONE is also wrong, twice over. Eight columns differ only in
          spelling or whitespace (`UPC` / `UPC/GTIN`, `Voltage` /
          `Total Voltage`, `Backplate Width  (inches)` with two spaces), so a
          naive name union produces two columns for one field. And both sheets
          repeat two header names (`Pier Mount`, `Turtle Friendly`), which a
          dict reader silently collapses to the last occurrence -- dropping a
          populated column without a word.

        So: name-based, with a declared `aliases` map per member, and repeated
        headers disambiguated positionally into `<name> #2` and reported.
        """
        rows = []
        seen_dupes = set()
        for member in spec['files']:
            mpath = _resolve(member['path'], root)
            with open(mpath, newline='',
                      encoding=spec.get('encoding', 'utf-8-sig')) as fh:
                raw = list(__import__('csv').reader(fh))
            hrow = member.get('header_row', spec.get('header_row', 1)) - 1
            aliases = member.get('aliases', {})
            header, counts = [], {}
            for c in raw[hrow]:
                name = (c or '').strip()
                name = aliases.get(name, name)
                if not name:
                    header.append('')
                    continue
                counts[name] = counts.get(name, 0) + 1
                if counts[name] > 1:
                    name = '%s #%d' % (name, counts[name])
                    seen_dupes.add(name)
                header.append(name)
            for r in raw[hrow + 1:]:
                if not r or not any((c or '').strip() for c in r):
                    continue
                rec = {h: ((r[i] if i < len(r) else '') or '').strip()
                       for i, h in enumerate(header) if h}
                for k, v in member.get('tag', {}).items():
                    rec[k] = v
                rows.append(rec)
        if seen_dupes:
            rows and rows[0].setdefault('_dupe_headers', ','.join(sorted(seen_dupes)))
        return rows, ' + '.join(m['path'] for m in spec['files'])

    path = spec['path']
    if not os.path.isabs(path):
        path = os.path.join(root, path)
    path = os.path.abspath(path)
    if not os.path.exists(path):
        raise MappingError('input not found: %s' % path)

    if fmt == 'xlsx_rows':
        # A whole sheet as dict rows keyed by its own header line. Distinct from
        # `xlsx`, which is the keyed lookup reader addressed by column INDEX.
        import openpyxl
        path = _resolve(spec['path'], root)
        wb = openpyxl.load_workbook(path, data_only=True)
        ws = wb[spec['sheet']] if spec.get('sheet') else wb.active
        raw = [list(r) for r in ws.iter_rows(values_only=True)]
        wb.close()
        hrow = spec.get('header_row', 1) - 1
        header = [('' if c is None else str(c)).strip() for c in raw[hrow]]
        out = []
        for r in raw[hrow + 1 + spec.get('skip_after_header', 0):]:
            if not r or not any(c is not None and str(c).strip() for c in r):
                continue
            out.append({h: ('' if v is None else str(v).strip())
                        for h, v in zip(header, r) if h})
        return out, path

    if fmt == 'xlsx':
        # One parameterised reader covers all four Legrand price books. They
        # differ only in which row the data starts on and which column index
        # holds which price — that is PARAMETERS, not four bespoke loaders.
        import openpyxl
        wb = openpyxl.load_workbook(path, data_only=True)
        ws = wb[spec['sheet']] if spec.get('sheet') else wb.active
        key_col = spec['key_col']
        cols = spec['columns']
        skip = set(spec.get('skip_key_values', []))
        prim = spec.get('value_primitive')
        dialect = spec.get('dialect')
        out = {}
        for row in ws.iter_rows(min_row=spec.get('data_start_row', 2), values_only=True):
            if not row or len(row) <= key_col or not row[key_col]:
                continue
            k = str(row[key_col]).strip()
            if not k or k in skip:
                continue
            rec = {}
            for name, idx in cols.items():
                # Truthiness, not `is not None`: a numeric 0 cell means NO PRICE
                # here. `is not None` would emit '0.00' for a 0.0 cell.
                raw = str(row[idx]) if (len(row) > idx and row[idx]) else ''
                rec[name] = apply_primitive(prim, [raw], {}, dialect) if prim else raw
            out[k] = rec
        wb.close()
        return out, path

    raise MappingError('unknown input format: %r' % fmt)


# --- evaluation -------------------------------------------------------------

def apply_primitive(name, args, params, dialect, report=None, tag=None):
    if name not in PRIMITIVES:
        raise MappingError('unknown primitive %r (add it to ecatlib, not here)' % name)
    fn, takes_dialect = PRIMITIVES[name]
    kwargs = dict(params or {})
    if takes_dialect and dialect:
        kwargs['dialect'] = dialect
    result = fn(*args, **kwargs)
    if name in TUPLE_FLAGS:
        value, flags = result[0], result[1:]
        if report is not None:
            for flag_name, flagged in zip(TUPLE_FLAGS[name], flags):
                if flagged:
                    report.count('%s.%s' % (tag or name, flag_name), specimen=args[0])
        return value
    return result


class Engine:
    def __init__(self, mapping, root, tables):
        self.m = mapping
        self.root = root
        self.tables = tables
        self.dialect = mapping.get('dialect')
        self.inputs = {}
        self.input_paths = {}
        self.custom = {}
        self.report = Report()

    # -- setup --

    def load_inputs(self):
        for name, spec in self.m.get('inputs', {}).items():
            self.inputs[name], self.input_paths[name] = load_input(spec, self.root)

    def load_custom(self):
        """Load the client's budgeted escape-hatch module, if it declares one."""
        budget = self.m.get('escape_hatch', {})
        mod_path = budget.get('module')
        if not mod_path:
            return
        import importlib.util
        full = os.path.abspath(os.path.join(self.root_mapping, mod_path))
        spec = importlib.util.spec_from_file_location('_client_custom', full)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for fn_name in budget.get('transforms', []):
            if not hasattr(mod, fn_name):
                raise MappingError('escape-hatch fn %r not in %s' % (fn_name, full))
            self.custom[fn_name] = getattr(mod, fn_name)

    def class2_guard(self):
        """A class-2 file's headers are IMMUTABLE. Enforced, not requested.

        OPEN_ITEMS A22. On libco I was wrong three times out of three, and every
        one was a sensible improvement to a file where a human had already
        decided: I renamed a header (`netprice` -> `NetPrice`) and dropped two
        columns (`ShipLBS`, `Video`). All three were defensible. All three
        overrode a decision someone had already made, which is precisely what
        the class-2 rule exists to stop.

        The failure mode is HELPFULNESS. Prompting does not fix helpfulness --
        the rule was written down, in the kickoff and in this file's own header,
        and I broke it anyway while quoting it. So it is a guard:

          * a field whose output name differs from its source column needs an
            explicit `rename_reason`
          * a source column that is not emitted needs an explicit `[[drop]]`
            entry carrying a `reason`

        Both are one line to add and impossible to do by accident, which is the
        whole point. The engine REFUSES otherwise.
        """
        if self.m.get('input_class') != 2 and self.m.get('mode') != 'validate':
            return
        rows = self.inputs.get(self.m['primary_input'])
        if not isinstance(rows, list) or not rows:
            return
        source_headers = [h for h in rows[0].keys() if h]
        emitted, renames = {}, []
        for f in self.m.get('fields', []):
            name = f['name']
            src = f.get('column', name)
            emitted[src] = f
            if src != name and f.get('op') in ('passthrough', 'column'):
                if not f.get('rename_reason'):
                    renames.append((src, name))
        declared_drops = {d['column']: d for d in self.m.get('drop', [])}
        missing_reason = [c for c, d in declared_drops.items()
                          if not (d.get('reason') or '').strip()]
        undeclared = [h for h in source_headers
                      if h not in emitted and h not in declared_drops]

        problems = []
        for src, name in renames:
            problems.append(
                'header renamed %r -> %r with no `rename_reason`. A class-2 '
                "file's headers are the human's mapping; renaming one is a "
                'transform.' % (src, name))
        for h in undeclared:
            problems.append(
                'source column %r is not emitted and not declared in [[drop]]. '
                'Dropping a column a human included is overriding them; say so '
                'explicitly, with a reason.' % h)
        for c in missing_reason:
            problems.append('[[drop]] for %r carries no reason.' % c)
        if problems:
            raise MappingError(
                'CLASS-2 GUARD (OPEN_ITEMS A22) — %d violation(s):\n   - %s'
                % (len(problems), '\n   - '.join(problems)))
        for c, d in declared_drops.items():
            self.report.count('class2.dropped_column', specimen='%s (%s)'
                              % (c, d['reason'][:60]))
        for f in self.m.get('fields', []):
            if f.get('rename_reason'):
                self.report.count('class2.renamed_header', specimen='%s -> %s'
                                  % (f.get('column'), f['name']))

    def declared_columns_check(self):
        """Warn when a DECLARED source column matches no header. Coverage stated.

        The cheapest item on the Phase 2 "what a fifth client would need" list,
        and it had already bitten three times: case (`materials` vs
        `Materials`), trailing whitespace (`Dealer Net ` in tcs's Master), and
        near-duplicates (`UPC` / `UPC/GTIN`). tcs W2 is the specimen -- the
        reader strips header whitespace, the mapping declared the raw name, and
        `NetPrice` came back blank on 379 of 425 rows. Two correct decisions
        that were not made in the same place, and nothing said so.

        It reports a NEAR MISS where one exists, because "matched no header" is
        only half an answer; `Dealer Net ` -> `Dealer Net` is the whole bug.
        """
        rows = self.inputs.get(self.m.get('primary_input'))
        if not isinstance(rows, list) or not rows:
            self.report.warn('declared-column check: evaluated 0 of ? declared '
                             'columns — the primary input is not a row list.')
            return
        headers = [h for h in rows[0].keys() if h]
        by_norm = {}
        for h in headers:
            by_norm.setdefault(h.strip().lower(), []).append(h)

        declared = []
        for spec in list(self.m.get('derived', [])) + list(self.m.get('fields', [])):
            col = spec.get('column')
            if col:
                declared.append((spec.get('name', col), col))
            if spec.get('op') == 'custom' and spec.get('args_are_columns'):
                for a in spec.get('args', []):
                    declared.append((spec.get('name', a), a))
            if spec.get('op') == 'apply':
                for a in spec.get('args', []):
                    if isinstance(a, str) and a in headers:
                        continue
        missing = 0
        for name, col in declared:
            if col in headers:
                continue
            missing += 1
            near = by_norm.get(col.strip().lower(), [])
            if near:
                self.report.warn(
                    'field %s declares column %r, which matches NO header — but '
                    '%r differs only in case/whitespace. Declare the header as '
                    'the reader sees it.' % (name, col, near[0]))
                self.report.count('declared_column.near_miss',
                                  specimen='%s -> %s' % (col, near[0]))
            else:
                self.report.warn(
                    'field %s declares column %r, which matches NO header in the '
                    'source. The field is silently blank on every row.'
                    % (name, col))
                self.report.count('declared_column.no_header', specimen=col)
        self.report.counters['declared_column.coverage'] = len(declared)
        self.report.specimens['declared_column.coverage'] = (
            'evaluated %d of %d declared columns against %d headers; %d matched nothing'
            % (len(declared), len(declared), len(headers), missing))

    # -- per-row --

    def eval_step(self, spec, row, scope, name):
        op = spec.get('op', 'column')

        # `otherwise_value` is a LITERAL; `branch`'s `otherwise` is a SCOPE NAME.
        # Two different things, so two different keys -- collapsing them would
        # silently emit the string "lit_sample" instead of its value.
        gate = spec.get('only_when')
        if gate and not self._gate_ok(gate, scope):
            return spec.get('otherwise_value', '')

        if op == 'const':
            return spec['value']

        if op == 'ref':
            return scope[spec['from']] or spec.get('default', '')

        if op == 'equals':
            return scope[spec['input']] == spec['value']

        if op == 'starts_with':
            return str(scope[spec['input']]).startswith(spec['value'])

        if op == 'ends_with':
            return str(scope[spec['input']]).endswith(spec['value'])

        if op == 'concat':
            # `skip_blank` and `prefix_each` are here because tcs's
            # `ProductStory` is `Marketing Copy` + a blank line + Feature 1..6
            # as a bullet list, and Features 4-6 are empty on most rows. Without
            # skip_blank that ships a story ending in three naked bullets; with
            # a per-field hatch it costs six of a budget of three.
            #
            # Composing a list from N optional columns is not client-specific --
            # every catalogue has a features block -- so it is an operator, and
            # the next client gets it free.
            parts = [str(scope[a]) if a in scope else str(a) for a in spec['of']]
            if spec.get('skip_blank'):
                parts = [p for p in parts if p.strip()]
            pre = spec.get('prefix_each')
            if pre:
                parts = [pre + p for p in parts]
            return spec.get('join', '').join(parts)

        if op == 'contains':
            return scope[spec['input']] in self.tables[spec['table']]

        if op == 'coalesce':
            for src in spec['of']:
                val = scope[src]
                if val:
                    return val
            return spec.get('default', '')

        if op == 'branch':
            return scope[spec['then']] if scope[spec['on']] else scope[spec['otherwise']]

        if op == 'lookup':
            table = self.tables[spec['table']]
            val = scope[spec['input']]
            if val in table:
                return table[val]
            if spec.get('default_to_input'):
                return val
            return spec.get('default', '')

        if op == 'source':
            rec = self.inputs[spec['input']].get(scope[spec['key']])
            if not rec:
                return spec.get('default', '')
            return rec.get(spec['field'], spec.get('default', '')) or spec.get('default', '')

        if op == 'source_switch':
            which = spec['cases'].get(scope[spec['on']], spec['default_input'])
            rec = self.inputs[which].get(scope[spec['key']])
            if not rec:
                return spec.get('default', '')
            return rec.get(spec['field'], '') or spec.get('default', '')

        if op == 'passthrough':
            # CLASS-2: the human already decided this mapping. Copy the
            # same-named source column and change NOTHING. A `primitive` here is
            # only ever an importer-required coercion (a float tail, a
            # datetime) -- never a re-derivation of the value.
            raw = row.get(spec.get('column', name), spec.get('missing', ''))
            prim = spec.get('primitive')
            if prim:
                params = self._resolve_params(spec.get('params', {}))
                raw = apply_primitive(prim, [raw], params,
                                      spec.get('dialect', self.dialect),
                                      self.report, name)
            return raw or spec.get('default', '')

        if op == 'column':
            override = spec.get('override_by_key')
            if override:
                table = self.tables[override['table']]
                k = scope[override['key']]
                if k in table:
                    return table[k]
            raw = row.get(spec['column'], spec.get('missing', ''))
            prim = spec.get('primitive')
            if prim:
                params = self._resolve_params(spec.get('params', {}))
                out = apply_primitive(prim, [raw], params, spec.get('dialect', self.dialect),
                                      self.report, name)
            else:
                out = raw
            return out or spec.get('default', '')

        if op == 'apply':
            args = [scope[a] if a in scope else a for a in spec['args']]
            params = self._resolve_params(spec.get('params', {}))
            out = apply_primitive(spec['primitive'], args, params,
                                  spec.get('dialect', self.dialect), self.report, name)
            return out or spec.get('default', '')

        if op == 'custom':
            fn = self.custom.get(spec['fn'])
            if fn is None:
                raise MappingError('field %r uses undeclared escape hatch %r'
                                   % (name, spec['fn']))
            args = [row.get(a, '') if spec.get('args_are_columns') else scope.get(a, a)
                    for a in spec['args']]
            return fn(*args)

        raise MappingError('field %r: unknown op %r' % (name, op))

    def _gate_ok(self, gate, scope):
        val = scope[gate['field']]
        if 'equals' in gate:
            return val == gate['equals']
        if 'not_equals' in gate:
            return val != gate['not_equals']
        return bool(val)

    def _resolve_params(self, params):
        """`table = "finish_fixes"` in a param position resolves to the table."""
        out = {}
        for k, v in params.items():
            if k == 'fixes' and isinstance(v, str):
                out[k] = self.tables[v]
            elif k == 'null_tokens':
                out[k] = tuple(v)
            else:
                out[k] = v
        return out

    # -- run --

    def build(self):
        primary_name = self.m['primary_input']
        rows = self.inputs[primary_name]
        if isinstance(rows, dict):
            raise MappingError('primary input %r must not declare a key' % primary_name)

        derived_specs = self.m.get('derived', [])
        field_specs = self.m['fields']

        skip_blank = self.m.get('skip_row_when_blank')

        scopes, products = [], []
        for row in rows:
            scope = {}
            for spec in derived_specs:
                scope[spec['name']] = self.eval_step(spec, row, scope, spec['name'])
            if skip_blank and not (scope.get(skip_blank) or '').strip():
                continue
            product = {}
            for spec in field_specs:
                product[spec['name']] = self.eval_step(spec, row, scope, spec['name'])
                scope[spec['name']] = product[spec['name']]
            scopes.append(scope)
            products.append(product)

        self.pass_related(scopes, products)
        self.pass_carryforward(products)
        products = self.pass_dedupe(products)
        products = self.pass_sort(products)
        products = self.pass_row_order(products)
        return products

    def pass_row_order(self, products):
        """Preserve the previous build's ROW ORDER.

        Row order is not derivable from mer's source: the live file's order came
        from an earlier hand-built generation and no ordering of the NetSuite
        export reproduces it. It is also not arbitrary to get right. The
        importer does not care, but a HUMAN reading `diff_against_previous`
        does: reordered rows turn a two-line change into a whole-file rewrite
        and hide the one column that actually moved. BUILD_SPEC B6 asks for a
        diff whose only differences are intended, and that is unreadable if
        every row moves.

        So this is carry-forward applied to ordering: same rule, same reason --
        a value the generator cannot derive must come from the last known-good
        file or regeneration destroys it. New codes append in source order.
        """
        if self.m.get('row_order') != 'carry_forward':
            return products
        cf = self.m.get('carry_forward')
        if not cf:
            raise MappingError("row_order='carry_forward' needs [carry_forward]")
        path = cf['source']
        if not os.path.isabs(path):
            path = os.path.join(self.root, path)
        path = os.path.abspath(path)
        key_col = cf.get('key_column', 'BaseItemCode')
        if not os.path.exists(path):
            raise MappingError('row_order source not found: %s' % path)
        prior = [(r.get(key_col) or '').strip() for r in lib.read_rows(path)]
        rank = {k: i for i, k in enumerate(prior) if k}
        new = [p for p in products if (p.get(key_col) or '').strip() not in rank]
        for p in new:
            self.report.count('row_order.new_code',
                              specimen=(p.get(key_col) or '').strip())
        return sorted(products,
                      key=lambda p: rank.get((p.get(key_col) or '').strip(),
                                             len(rank)))

    def pass_dedupe(self, products):
        """Collapse repeated keys. `keep` is DECLARED, never implicit: with two
        division files unioned into one slot, which row wins is a client
        decision and the file cannot be built without answering it."""
        spec = self.m.get('dedupe')
        if not spec:
            return products
        on, keep = spec['on'], spec.get('keep', 'first')
        if keep not in ('first', 'last'):
            raise MappingError('dedupe.keep must be first|last, got %r' % keep)
        seen, out = {}, []
        for product in products:
            k = (product.get(on) or '').strip()
            if k in seen:
                self.report.count('dedupe.dropped', specimen=k)
                if keep == 'last':
                    out[seen[k]] = product
                continue
            seen[k] = len(out)
            out.append(product)
        return out

    def pass_sort(self, products):
        keys = self.m.get('sort_by')
        if not keys:
            return products
        return sorted(products, key=lambda p: tuple(p.get(k, '') for k in keys))

    def pass_related(self, scopes, products):
        """Build RelatedItems families.

        Composed from `ecatlib.group_families` rather than calling
        `build_related_items` directly, because the two live builds genuinely
        DIFFER: Legrand's list INCLUDES the item itself in source order, mer's
        EXCLUDES it and sorts. Both are correct for their client, so both are
        declared in the mapping instead of one being imposed on the other.

        A wrong RelatedItems value is worse than a blank one - it is a dangling
        reference (BUILD_SPEC A3), and Legrand's own script records that fuzzy
        auto-merging produced 118 matches that were nearly all false.
        """
        spec = self.m.get('related_items')
        if not spec:
            return
        code = spec['code']
        include_self = spec.get('include_self', True)
        sort_members = spec.get('sort_members', False)

        if spec.get('key_from'):
            key_fn = lambda sc: sc[spec['key_from']]
        elif spec.get('key_custom'):
            fn = self.custom.get(spec['key_custom'])
            if fn is None:
                raise MappingError('related_items.key_custom %r not declared'
                                   % spec['key_custom'])
            key_fn = lambda sc: fn(*[sc[a] for a in spec['key_args']])
        else:
            key_fn = lambda sc: lib.variant_key_by_name(
                *[sc[a] for a in spec['key_args']])

        groups = lib.group_families(scopes, key_fn, lambda sc: sc[code])
        related_map, families = {}, []
        for members in groups.values():
            if len(members) < spec.get('min_family', 2):
                continue
            ordered = sorted(members) if sort_members else members
            families.append(ordered)
            for item in ordered:
                peers = ordered if include_self else [x for x in ordered if x != item]
                related_map[item] = ','.join(peers)

        for scope, product in zip(scopes, products):
            product[spec['into']] = related_map.get(scope[code], '')
        self.report.counters['related_items.families'] = len(families)
        self.report.counters['related_items.skus'] = sum(len(f) for f in families)
        if families:
            self.report.specimens['related_items.families'] = ','.join(families[0])

    def pass_carryforward(self, products):
        cf_fields = [f for f in self.m['fields'] if 'carry_forward' in f]
        if not cf_fields:
            return
        cf = self.m.get('carry_forward')
        if not cf:
            raise MappingError('fields declare carry_forward but no [carry_forward] source')

        path = cf['source']
        if not os.path.isabs(path):
            path = os.path.join(self.root, path)
        path = os.path.abspath(path)   # absolute, ALWAYS — the 19-images bug

        key_col = cf.get('key_column', 'BaseItemCode')
        for spec in cf_fields:
            name = spec['name']
            carried, warning = lib.load_carryforward(path, name, key_column=key_col)
            # The warning is NEVER discarded. A silent {} here is exactly how
            # Legrand lost 19 products' live images.
            if warning:
                self.report.warn('carry-forward %s: %s' % (name, warning))
                if cf.get('require', True):
                    raise MappingError('carry-forward required but unavailable: %s' % warning)
            rule = spec['carry_forward']
            when = rule.get('when', 'blank')
            default = rule.get('default', '')
            for product in products:
                k = (product.get(key_col) or '').strip()
                prior = carried.get(k, '')
                if when == 'always':
                    product[name] = prior or default
                elif when == 'blank':
                    if not (product.get(name) or '').strip() and prior:
                        product[name] = prior
                        self.report.count('carry_forward.%s.restored' % name, specimen=k)
                else:
                    raise MappingError('unknown carry_forward.when %r' % when)


# --- the option stack -------------------------------------------------------
#
# Every mapping before this one is column -> column: one source row in, one
# output row out. The option stack is not, and that is a FORMAT change rather
# than another mapping.
#
# tcs's 72 columns between `Propane Tip` and `Seeded Replacement Glass - SRG`
# are the option stack transposed sideways into the product sheet. Each HEADER
# is an option name; each CELL is an option code (`WY`, `GH1`, `BLK`), blank, or
# a null token (`----`). N source columns have to become M rows in two other
# files, plus a per-product reference back into products.csv. There is no way to
# say that with `[[fields]]`.
#
# THREE readings of a sideways block are legal and the source does not choose:
#
#   per_column   one column is one group; its distinct cell values are its
#                options. `Post Fitter` becomes a group holding PF1..PF5, and a
#                product carrying PF3 sees all five. Cheap, and rep-facing wrong
#                whenever the cell varies by row.
#   single       the whole axis is one group. Right when the cell is constant
#                per column (the four finish columns) and the choice is
#                catalogue-wide.
#   per_product  the group IS the distinct combination of codes one product
#                offers on that axis; identical combinations share a group.
#                This is the granular pattern the Admin Console's Option
#                Mapping requires -- you cannot cascade from one big group.
#
# The format expresses all three and REFUSES to default, for the same reason
# `dedupe.keep` is declared: with a sideways block, which reading applies is a
# client decision and the file cannot be built without answering it.
#
# ONE MAPPING, THREE ARTIFACTS -- deliberately, and the only place in this
# format where that is true. options.csv, option_groups.csv and the per-product
# assignment are one derivation, not three: importing options.csv NULLS group
# membership, so option_groups.csv must be re-sent from the SAME traversal or it
# references codes that no longer exist. mali sits at BLOCKING for exactly that
# (A4, 2 of 2 groups). Splitting them into two mappings is how they drift.

AXIS_KEYS = {
    'code', 'name', 'option_set', 'required', 'columns', 'option_types', 'grouping',
    'group_code', 'group_name', 'option_code', 'option_name', 'null_tokens',
    'description', 'imagename', 'priceaddend', 'pricefactor', 'sortvalue',
}

INPUT_KEYS = {
    'format', 'path', 'encoding', 'files', 'key', 'fields', 'header_row',
    'header_at_first_cell', 'skip_rows_after_header', 'sheet', 'key_col',
    'columns', 'skip_key_values', 'value_primitive', 'dialect',
    'data_start_row', 'skip_after_header', 'aliases', 'tag',
}

OPTION_LIMITS = {'Code': 15, 'Name': 50}   # code-verified. The KB says 8/25 and
                                           # is wrong; see README § field limits.


class OptionStack:
    """Build options.csv + option_groups.csv + the per-product assignment."""

    def __init__(self, mapping, engine):
        self.m = mapping
        self.eng = engine
        self.report = engine.report
        self.options = {}      # code -> {'Code','Name',...}
        self.code_names = {}   # code -> first name seen, for collision reports
        self.groups = []       # ordered [{'Code','Name','Options'}]
        self.group_by_sig = {}
        self.assignments = []
        self.axis_members = {}   # axis code -> ordered distinct option codes
        self.catalogue = {}      # code -> record, when the client ships a list
        self.catalogue_type = {} # code -> its declared type value

    # -- helpers --

    @staticmethod
    def _fmt(tpl, **kw):
        try:
            return tpl.format(**kw)
        except KeyError as e:
            raise MappingError('template %r references unknown placeholder %s'
                               % (tpl, e))

    def _limit(self, kind, field, value, where):
        cap = OPTION_LIMITS[field]
        if len(value) > cap:
            raise MappingError(
                '%s %s %r is %d chars; the importer caps %s at %d. '
                'Shorten it in the mapping -- a long code fails the import '
                'outright (%s).' % (kind, field, value, len(value), field, cap, where))
        return value

    def _add_option(self, code, name, axis):
        seen = self.axis_members.setdefault(axis['code'], [])
        if code not in seen:
            seen.append(code)
        if code in self.options:
            if self.code_names[code] != name:
                self.report.count('option.code_collision',
                                  specimen='%s = %r and %r'
                                  % (code, self.code_names[code], name))
            return
        self._limit('option', 'Code', code, 'axis %s' % axis['code'])
        self._limit('option', 'Name', name, 'axis %s' % axis['code'])
        rec = {'Code': code, 'Name': name}
        for extra in ('Description', 'ImageName', 'PriceAddend', 'PriceFactor',
                      'SortValue'):
            tpl = axis.get(extra.lower(), self.m.get(extra.lower()))
            if tpl is not None:
                rec[extra] = self._fmt(str(tpl), code=code, name=name,
                                       axis=axis['code'])
        self.options[code] = rec
        self.code_names[code] = name

    def _group(self, axis, codes, seq_state):
        """Return the group code for this combination, creating it if new."""
        sig = (axis['code'], tuple(codes))
        if sig in self.group_by_sig:
            return self.group_by_sig[sig]
        seq_state[axis['code']] = seq_state.get(axis['code'], 0) + 1
        n = seq_state[axis['code']]
        code = self._fmt(axis['group_code'], n=n, axis=axis['code'],
                         first=codes[0] if codes else '')
        name = self._fmt(axis['group_name'], n=n, axis=axis['code'],
                         axis_name=axis['name'], first=codes[0] if codes else '')
        self._limit('option group', 'Code', code, 'axis %s' % axis['code'])
        self._limit('option group', 'Name', name, 'axis %s' % axis['code'])
        if code in {g['Code'] for g in self.groups}:
            raise MappingError(
                'group code %r generated twice by axis %r. group_code must be '
                'unique per combination -- include {n}.' % (code, axis['code']))
        rec = {'Code': code, 'Name': name, 'Options': ','.join(codes)}
        for extra in ('PriceAddend', 'PriceFactor'):
            if axis.get(extra.lower()) is not None:
                rec[extra] = str(axis[extra.lower()])
        self.groups.append(rec)
        self.group_by_sig[sig] = code
        return code

    # -- the option catalogue -------------------------------------------

    def load_catalogue(self):
        """Load the client's own option LIST, when it has one.

        THE CORRECTION THAT MATTERS, and it is a format lesson rather than a tcs
        one. Written blind, this mapping treated the 72 transposed columns as the
        whole option stack: the header was the option name, the cell was the
        code, and the axis partition was mine, read off the column names.

        338 of the 341 options in tcs's build are rows of
        `Accessories-Table 1.csv` -- a sheet I had already classified, on the
        products run, as a source of PRODUCTS. It carries `Accessory SKU`
        (the option code), `Accessory Name`, `Accessory Dealer Net` (the
        PriceAddend on 338 of 341) and `Accessory Category` -- which IS the
        option-type partition I spent a paragraph of the mapping inventing.

        So a sideways block is TWO sources, not one, and they answer different
        questions:

            the CATALOGUE     what the options are      rows -> options.csv
            the MATRIX        who can have which        columns -> groups

        When both exist, the axis partition is not a judgement call at all --
        it is a column the client already filled in. `option_types` selects an
        axis by that column's values instead of by a hand-written column list.

        The general rule, and the one to carry to the next client:
        **before declaring a partition, look for the column that already
        carries it.**
        """
        spec = self.m.get('option_catalogue')
        if not spec:
            return
        rows = self.eng.inputs[spec['input']]
        if isinstance(rows, dict):
            raise MappingError('option_catalogue input must not declare a key')
        labels = self.m.get('type_labels', {})

        # PER-CODE TYPE OVERRIDE, and it exists because of a measured hole in
        # the catalogue reading rather than as a general convenience.
        #
        # The catalogue's type column is per CODE. The matrix's type is per
        # COLUMN. When one code appears in columns of two different types the
        # catalogue cannot express it, and the code lands in exactly one axis.
        #
        # tcs's `LR`: the catalogue calls it `Ladder Rests` and files it under
        # POST & PIER MOUNT; the matrix uses it in the `Ladder Rests` column
        # (171 rows, a ceiling mount) AND in `Post Ladder Rest` (3 rows, where
        # the other 156 are `PLR` -- a source typo). The client's own category
        # is wrong and the live build overrides it to Ceiling Mount.
        #
        # That one code was 68 of the 100 reproduced-wrongly member sets:
        # placing it as the build does moves group-membership recall from 67.8%
        # to 90.0%. A single miscategorised code in a client's catalogue moved a
        # whole-file metric by 22 points, because per-product groups multiply
        # it across every product that offers it.
        #
        # It is DECLARED DATA with a reason, never inferred: a mapping that
        # silently re-filed a client's categories would be the class-2 failure
        # in a new costume.
        overrides = self.m.get('option_type_overrides', {})
        for r in rows:
            code = (r.get(spec['code']) or '').strip()
            if not code:
                continue
            typ = (r.get(spec['type']) or '').strip() if spec.get('type') else ''
            if code in overrides:
                self.report.count('catalogue.type_override',
                                  specimen='%s: %s -> %s'
                                  % (code, typ, overrides[code]))
                typ = overrides[code]
            rec = {'Code': code, 'Name': (r.get(spec['name']) or '').strip()}
            rec['Description'] = labels.get(typ, typ)
            for out_field, src in spec.get('fields', {}).items():
                rec[out_field] = (r.get(src) or '').strip()
            if code in self.catalogue:
                self.report.count('catalogue.duplicate_code', specimen=code)
                continue
            self.catalogue[code] = rec
            self.catalogue_type[code] = typ

    # -- the traversal --

    def build(self, rows):
        axes = self.m.get('axis', [])
        if not axes:
            raise MappingError("an option_stack mapping needs at least one [[axis]]")
        # A file-level key that landed inside an `[inputs.*]` table is the same
        # TOML scoping trap as the axis one, and it is silent in the same way.
        for iname, ispec in self.m.get('inputs', {}).items():
            stray = sorted(set(ispec) - INPUT_KEYS)
            if stray:
                raise MappingError(
                    'input %r carries key(s) %s that are not input settings. In '
                    'TOML a bare key written after `[inputs.%s]` binds to it — '
                    'move file-level settings ABOVE the first table.'
                    % (iname, ', '.join(repr(x) for x in stray), iname))

        # STRICT AXIS KEYS. In TOML a bare key written after `[[axis]]` belongs
        # to that axis, not to the file -- so `options_columns` placed at the
        # bottom of the mapping silently becomes a key of the LAST axis and the
        # emitter never sees it. That happened while writing tcs's mapping and
        # ImageName vanished from options.csv with no error anywhere. It is the
        # same shape as every other defect in this programme: a declaration that
        # reads as though it applies and does not. So: unknown axis key refuses.
        for axis in axes:
            unknown = sorted(set(axis) - AXIS_KEYS)
            if unknown:
                raise MappingError(
                    'axis %r carries unknown key(s) %s. If you meant them as '
                    'file-level settings, TOML has already bound them to this '
                    'axis -- move them ABOVE the first table.'
                    % (axis.get('code', '?'), ', '.join(repr(u) for u in unknown)))
            # OptionSet1..20 is the real ceiling. CLAUDE.md said 5 and was
            # wrong -- fleet max is 20, 30 orgs use more than 5, and 37,803
            # references sit above OptionSet5 (corrected 2026-09-05). The engine
            # never capped, which is the right behaviour and was untested; it
            # also never REFUSED an out-of-range slot, which is not. OptionSet25
            # is not a column, and a products.csv carrying one imports with that
            # column ignored -- silently, so every option on that axis vanishes
            # while the file reads clean.
            slot = axis.get('option_set')
            if not isinstance(slot, int) or not 1 <= slot <= 20:
                raise MappingError(
                    'axis %r declares option_set = %r. The importer has '
                    'OptionSet1..OptionSet20; anything else is not a column and '
                    'is silently ignored on import, taking the whole axis with '
                    'it.' % (axis.get('code', '?'), slot))
            for req in ('code', 'name', 'option_set', 'grouping',
                        'group_code', 'group_name'):
                if req not in axis:
                    raise MappingError('axis %r is missing required key %r'
                                       % (axis.get('code', '?'), req))
            # An axis names its options ONE way: by the source columns it reads
            # (no catalogue), or by the catalogue types it claims (catalogue).
            # Both, or neither, means the mapping has not said which reading it
            # is using -- and that is the whole decision.
            if ('columns' in axis) == ('option_types' in axis):
                raise MappingError(
                    'axis %r must declare exactly one of `columns` (the '
                    'transposed block IS the option list) or `option_types` '
                    '(the client ships a catalogue and it carries the '
                    'partition). It declares %s.'
                    % (axis.get('code', '?'),
                       'both' if 'columns' in axis else 'neither'))

        key_col = self.m['product_key']['column']
        header_names = set()
        for r in rows[:1]:
            header_names = {h for h in r.keys() if h}

        # A declared column that matches no header is the cheapest check on the
        # "what a fifth client would need" list and it is built here first --
        # tcs's W2 (379 blank Dealer Net prices) and part of libco were exactly
        # this. A column named in the mapping and absent from the source is
        # silence today; here it is a counted warning with a specimen.
        for axis in axes:
            for col in axis.get('columns', []):
                if col not in header_names:
                    self.report.warn(
                        'axis %s declares column %r, which matches NO header in '
                        'the source. It contributes nothing and the mapping '
                        'reads as though it does.' % (axis['code'], col))
                    self.report.count('axis.column_matched_no_header', specimen=col)

        seq_state = {}
        null_default = tuple(self.m.get('null_tokens', []))
        collision = self.m.get('on_code_collision', 'report')
        if collision not in ('report', 'error'):
            raise MappingError('on_code_collision must be report|error')

        if self.catalogue:
            return self._build_from_catalogue(rows, axes, key_col, seq_state,
                                              null_default, header_names)

        for row in rows:
            key = (row.get(key_col) or '').strip()
            if not key:
                continue
            assign = {key_col: key}
            for axis in axes:
                nulls = tuple(axis.get('null_tokens', null_default))
                codes, seen = [], set()
                for col in axis['columns']:
                    cell = (row.get(col) or '').strip()
                    if not cell or cell in nulls:
                        if cell in nulls and cell:
                            self.report.count('axis.null_token.%s' % axis['code'],
                                              specimen='%s / %s' % (col, cell))
                        continue
                    code = (cell if axis.get('option_code', 'cell') == 'cell'
                            else col if axis['option_code'] == 'header'
                            else self._fmt(axis['option_code'], cell=cell,
                                           header=col, key=key))
                    name_src = axis.get('option_name', 'header')
                    name = (col if name_src == 'header'
                            else cell if name_src == 'cell'
                            else self._fmt(name_src, cell=cell, header=col,
                                           code=code, key=key))
                    self._add_option(code, name, axis)
                    if code not in seen:
                        seen.add(code)
                        codes.append(code)
                if not codes:
                    continue
                mode = axis['grouping']
                if mode == 'per_product':
                    gcodes = [self._group(axis, codes, seq_state)]
                elif mode == 'per_column':
                    gcodes = []
                    for col in axis['columns']:
                        cell = (row.get(col) or '').strip()
                        if not cell or cell in nulls:
                            continue
                        gcodes.append(self._group(
                            dict(axis, group_code=axis['group_code'],
                                 group_name=axis['group_name']),
                            [cell], seq_state))
                elif mode == 'single':
                    gcodes = [self._group(axis, ['*'], seq_state)]
                else:
                    raise MappingError(
                        'axis %s: grouping must be per_product|per_column|single, '
                        'got %r. There is no default: with a sideways block the '
                        'reading is a client decision.' % (axis['code'], mode))
                slot = 'OptionSet%d' % axis['option_set']
                assign[slot] = ','.join(
                    dict.fromkeys((assign.get(slot, '').split(',') if assign.get(slot) else []) + gcodes))
                assign['%sRequired' % slot] = axis.get('required', 'N')
            self.assignments.append(assign)

        # `single` collects membership across the WHOLE run, not per row: the
        # group is created on the first product that has anything on the axis,
        # but its members are every code the axis ever contributed. Filling it
        # per row would ship a group holding only the first product's finishes.
        for axis in axes:
            if axis['grouping'] != 'single':
                continue
            gcode = self.group_by_sig.get((axis['code'], ('*',)))
            if gcode is None:
                self.report.count('axis.no_rows', specimen=axis['code'])
                continue
            for g in self.groups:
                if g['Code'] == gcode:
                    g['Options'] = ','.join(self.axis_members.get(axis['code'], []))

        if collision == 'error' and self.report.counters.get('option.code_collision'):
            raise MappingError(
                'on_code_collision = "error" and %d code(s) carry two different '
                'names. e.g. %s' % (self.report.counters['option.code_collision'],
                                    self.report.specimens.get('option.code_collision')))
        return self

    def _build_from_catalogue(self, rows, axes, key_col, seq_state, nulls,
                              header_names):
        """Catalogue-driven: the matrix says WHO, the catalogue says WHAT."""
        matrix = self.m.get('matrix_columns')
        if not matrix:
            raise MappingError('option_catalogue needs `matrix_columns` — the '
                               'columns that say which products take which '
                               'options. Without it nothing references anything.')
        for col in matrix:
            if col not in header_names:
                self.report.warn('matrix_columns declares %r, which matches NO '
                                 'header in the source.' % col)
                self.report.count('matrix.column_matched_no_header', specimen=col)

        axis_of_type = {}
        for a in axes:
            if 'option_types' not in a:
                raise MappingError(
                    'axis %r must declare `option_types` when an '
                    '[option_catalogue] is present: the partition comes from '
                    'the catalogue, not from a hand-written column list.'
                    % a['code'])
            for t in a['option_types']:
                if t in axis_of_type:
                    raise MappingError('option type %r claimed by two axes' % t)
                axis_of_type[t] = a

        emit_rule = self.m['option_catalogue'].get('emit', 'referenced')
        if emit_rule not in ('referenced', 'all'):
            raise MappingError("option_catalogue.emit must be referenced|all")

        referenced = set()
        for row in rows:
            key = (row.get(key_col) or '').strip()
            if not key:
                continue
            assign = {key_col: key}
            buckets = {}
            for col in matrix:
                cell = (row.get(col) or '').strip()
                if not cell or cell in nulls:
                    if cell:
                        self.report.count('matrix.null_token', specimen='%s / %s'
                                          % (col, cell))
                    continue
                if cell not in self.catalogue:
                    # A code in the matrix with no catalogue row is a dangling
                    # reference in the SOURCE. Counted, never dropped silently.
                    self.report.count('matrix.code_not_in_catalogue',
                                      specimen='%s (column %s)' % (cell, col))
                    continue
                typ = self.catalogue_type.get(cell, '')
                axis = axis_of_type.get(typ)
                if axis is None:
                    self.report.count('matrix.type_no_axis',
                                      specimen='%s -> type %r' % (cell, typ))
                    continue
                b = buckets.setdefault(axis['code'], [])
                if cell not in b:
                    b.append(cell)
                referenced.add(cell)
                seen = self.axis_members.setdefault(axis['code'], [])
                if cell not in seen:
                    seen.append(cell)
            for axis in axes:
                codes = buckets.get(axis['code'])
                if not codes:
                    continue
                mode = axis['grouping']
                if mode == 'per_product':
                    gcodes = [self._group(axis, codes, seq_state)]
                elif mode == 'per_column':
                    gcodes = [self._group(axis, [c], seq_state) for c in codes]
                elif mode == 'single':
                    gcodes = [self._group(axis, ['*'], seq_state)]
                else:
                    raise MappingError('axis %s: unknown grouping %r'
                                       % (axis['code'], mode))
                slot = 'OptionSet%d' % axis['option_set']
                assign[slot] = ','.join(gcodes)
                assign['%sRequired' % slot] = axis.get('required', 'N')
            self.assignments.append(assign)

        for axis in axes:
            if axis['grouping'] != 'single':
                continue
            gcode = self.group_by_sig.get((axis['code'], ('*',)))
            if gcode:
                for g in self.groups:
                    if g['Code'] == gcode:
                        g['Options'] = ','.join(self.axis_members.get(axis['code'], []))

        keep = referenced if emit_rule == 'referenced' else set(self.catalogue)
        skipped = 0
        for code, rec in self.catalogue.items():
            if code not in keep:
                skipped += 1
                continue
            if self.catalogue_type.get(code) not in axis_of_type:
                skipped += 1
                continue
            self._limit('option', 'Code', code, 'catalogue')
            self._limit('option', 'Name', rec['Name'], 'catalogue')
            self.options[code] = rec
        self.report.counters['catalogue.rows'] = len(self.catalogue)
        self.report.counters['catalogue.emitted'] = len(self.options)
        self.report.specimens['catalogue.emitted'] = (
            'evaluated %d of %d catalogue rows; emitted %d (rule=%s), skipped %d '
            'as unreferenced or outside a declared axis'
            % (len(self.catalogue), len(self.catalogue), len(self.options),
               emit_rule, skipped))
        return self

    # -- emit --

    def emit(self, out_dir):
        emit = self.m.get('emit', {})
        for required in ('options', 'option_groups', 'assignments'):
            if required not in emit:
                raise MappingError('[emit] must name %r' % required)
        term = {'crlf': '\r\n', 'lf': '\n'}[self.m.get('line_terminator', 'crlf')]
        os.makedirs(out_dir, exist_ok=True)

        opt_cols = self.m.get('options_columns', ['Code', 'Name'])
        rows = [ {c: o.get(c, '') for c in opt_cols} for o in self.options.values() ]
        if self.m.get('options_sort_by'):
            rows.sort(key=lambda r: tuple(r.get(k, '') for k in self.m['options_sort_by']))
        p_opt = os.path.join(out_dir, emit['options'])
        lib.write_rows(p_opt, opt_cols, rows, lineterminator=term)

        grp_cols = self.m.get('option_groups_columns', ['Code', 'Name', 'Options'])
        grows = [ {c: g.get(c, '') for c in grp_cols} for g in self.groups ]
        if self.m.get('option_groups_sort_by'):
            grows.sort(key=lambda r: tuple(r.get(k, '') for k in self.m['option_groups_sort_by']))
        p_grp = os.path.join(out_dir, emit['option_groups'])
        lib.write_rows(p_grp, grp_cols, grows, lineterminator=term)

        # THE ASSIGNMENT FILE IS NOT AN eCAT IMPORT FILE.
        #
        # The importer reads exactly two files here, options.csv and
        # option_groups.csv. A product references a group through OptionSet
        # columns INSIDE products.csv -- there is no importer slot that takes a
        # product-to-group table. This file is an internal intermediate that is
        # merged into products.csv before upload.
        #
        # It looks exactly like an import file, sits next to two real ones, and
        # three of the six file types hard-delete. So the name has to make the
        # mistake impossible rather than unlikely, and a name that could be
        # mistaken for an importer target is REFUSED.
        IMPORTER_TARGETS = {
            'options.csv', 'option_groups.csv', 'products.csv',
            'inventory.csv', 'customers.csv', 'stories.csv',
            'matrix_options.csv', 'taxonomies.csv',
        }
        asn_name = emit['assignments']
        if asn_name.lower() in IMPORTER_TARGETS:
            raise MappingError(
                'emit.assignments is named %r, which is an eCat IMPORTER TARGET. '
                'The assignment table is an internal intermediate merged into '
                'products.csv -- naming it after a real import file is how it '
                'gets FTPed to /data. Use a name that cannot be mistaken for '
                'one, e.g. "_INTERMEDIATE_option_assignments.csv".' % asn_name)
        if not os.path.basename(asn_name).startswith('_INTERMEDIATE'):
            self.report.warn(
                'emit.assignments = %r does not start with "_INTERMEDIATE". It '
                'is not an import file and it will sit next to two that are.'
                % asn_name)

        slots = sorted({int(a['option_set']) for a in self.m['axis']})
        acols = [self.m['product_key']['column']]
        for s in slots:
            acols += ['OptionSet%d' % s, 'OptionSet%dRequired' % s]
        arows = [{c: a.get(c, '') for c in acols} for a in self.assignments]
        p_asn = os.path.join(out_dir, emit['assignments'])
        lib.write_rows(p_asn, acols, arows, lineterminator=term)

        self.report.counters['options.emitted'] = len(self.options)
        self.report.counters['option_groups.emitted'] = len(self.groups)
        self.report.counters['assignments.emitted'] = len(self.assignments)
        return p_opt, p_grp, p_asn

    def integrity(self):
        """Every membership reference must resolve. This is A4.

        `mali` sits at BLOCKING because option_groups references option codes
        that are not in options.csv -- 2 of 2 groups, membership nulled. That is
        not a database accident: importing options.csv nulls membership, and a
        group file naming a code the option file does not carry re-creates it on
        every reload. So the check runs on the OUTPUT, before anybody proposes an
        upload, and it states its coverage.
        """
        problems, checked = [], 0
        known = set(self.options)
        for g in self.groups:
            for code in [c for c in g['Options'].split(',') if c]:
                checked += 1
                if code not in known:
                    problems.append('group %s references option %r, which is not '
                                    'in options.csv' % (g['Code'], code))
        gknown = {g['Code'] for g in self.groups}
        acheck = 0
        for a in self.assignments:
            for k, v in a.items():
                if not k.startswith('OptionSet') or k.endswith('Required') or not v:
                    continue
                for code in v.split(','):
                    acheck += 1
                    if code not in gknown:
                        problems.append('product %s OptionSet reference %r is not '
                                        'an emitted group'
                                        % (a.get(self.m['product_key']['column']), code))
        return problems, {'group_members': checked, 'assignment_refs': acheck,
                          'options': len(self.options), 'groups': len(self.groups)}


def load_mapping(path):
    with open(path, 'rb') as fh:
        mapping = tomllib.load(fh)
    root = os.path.dirname(os.path.abspath(path))
    tables = {}
    for rel in mapping.get('tables_files', []):
        with open(os.path.join(root, rel), 'rb') as fh:
            tables.update(tomllib.load(fh))
    return mapping, tables


def run(mapping_path, client_root, out_path):
    mapping, tables = load_mapping(mapping_path)
    eng = Engine(mapping, client_root, tables)
    eng.root_mapping = os.path.dirname(os.path.abspath(mapping_path))
    eng.load_inputs()
    eng.load_custom()

    # The option stack is a different SHAPE of output, so it is a different
    # builder -- but the same engine, the same loaders, the same report.
    if mapping.get('kind') == 'option_stack':
        rows = eng.inputs[mapping['primary_input']]
        if isinstance(rows, dict):
            raise MappingError('primary input must not declare a key')
        stack = OptionStack(mapping, eng)
        stack.load_catalogue()
        stack = stack.build(rows)
        paths = stack.emit(out_path)
        problems, coverage = stack.integrity()
        eng.report.counters['integrity.group_members_checked'] = coverage['group_members']
        eng.report.counters['integrity.assignment_refs_checked'] = coverage['assignment_refs']
        eng.report.specimens['integrity.group_members_checked'] = (
            'evaluated %d of %d group-membership references and %d of %d OptionSet '
            'references; %d unresolved'
            % (coverage['group_members'], coverage['group_members'],
               coverage['assignment_refs'], coverage['assignment_refs'],
               len(problems)))
        for pr in problems:
            eng.report.warn('INTEGRITY (A4): %s' % pr)
        return (stack, paths), eng

    eng.class2_guard()
    eng.declared_columns_check()
    products = eng.build()
    fieldnames = [f['name'] for f in mapping['fields']]
    # The line terminator is part of the CLIENT'S file contract, not a global
    # default. leg's live products.csv is CRLF (1,021 of them); mer's is LF on
    # all 103 lines. Both are live and both import clean, so neither is "the"
    # right answer -- which makes it exactly the kind of thing that has to be
    # declared per client rather than inherited from whatever wrote it last.
    terminators = {'crlf': '\r\n', 'lf': '\n'}
    term = mapping.get('line_terminator', 'crlf').lower()
    if term not in terminators:
        raise MappingError('line_terminator must be crlf|lf, got %r' % term)
    lib.write_rows(out_path, fieldnames, products,
                   lineterminator=terminators[term])
    return products, eng


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        print('usage: mapper.py <mapping.toml> <client root> <out.csv>')
        return 2
    mapping_path, client_root, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
    products, eng = run(mapping_path, client_root, out_path)
    if isinstance(products, tuple):
        stack, paths = products
        print('option stack -> %s' % out_path)
        for pth in paths:
            print('  %-24s %d rows' % (os.path.basename(pth),
                                       sum(1 for _ in open(pth, encoding='utf-8')) - 1))
        print()
        print('UPLOAD: options.csv and option_groups.csv ONLY.')
        print('  _INTERMEDIATE_option_assignments.csv is NOT an eCat import file.')
        print('  There is no importer slot for a product-to-group table: a product')
        print('  references a group through OptionSet1..20 INSIDE products.csv.')
        print('  Merge it into products.csv, then upload that. Never FTP it.')
        print()
        print('IMPORT ORDER — mandatory, and options.csv NULLS group membership,')
        print('so option_groups.csv is sent AGAIN after it:')
        print('  options -> option_groups -> products -> stories -> inventory -> customers')
        print('  (re-send option_groups after options. That is A4.)')
    else:
        print('rows: %d -> %s' % (len(products), out_path))
    if eng.report.counters:
        print('report:')
        for line in eng.report.lines():
            print(line)
    for w in eng.report.warnings:
        print('  ! %s' % w)
    return 0


if __name__ == '__main__':
    sys.exit(main())
