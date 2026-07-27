#!/usr/bin/env python3
"""Header <-> registered custom-field diff, case-insensitively.

A column the importer doesn't recognize produces `Field name X is unknown` and its data
is dropped. A custom field registered in Admin but absent from the file produces
`Custom field 'x' is missing`. Both are live at Legrand right now:

* 2026-07-23 products: `Custom field 'rohscompliant' is missing`, `'Color'`, `'voltage'`
* 2026-07-14 products: `Field name carton1_h / carton1_l / carton1_w is unknown`
* customers: seven `BillTo_*` unregistered-field warnings

Pebl carried a chronic warning set for three months on the same shape. The classic near
miss is a case/spelling drift pair like `ML_qtybackordered` vs `ML_QtyOnBackorder`, which
is why the compare is case-insensitive and why a near-match is called out by name rather
than reported as two unrelated problems.

Custom fields must be pre-registered in Admin (Products -> Custom Fields, "Send to
iPad") before import. This check needs that list passed in — it cannot read Admin.
"""
import difflib

from ..core import fail, skip, warn
from ..limits import LIMITS

CHECK = "custom-fields"
SUBSYSTEM = "core"


def run(csv_file, lookup, registered, known_extra=()):
    """Diff the file's headers against the org's registered custom fields.

    registered: iterable of custom field names from Admin, or None if not supplied.
    known_extra: headers that are legitimately not standard and not custom fields
                 (e.g. price_*, qty_*, optionset*, relateditems* prefixed columns).
    """
    if registered is None:
        return [warn(
            CHECK,
            "no --custom-fields list supplied: unknown columns and missing registered "
            "fields could not be checked. Pull the list from Admin (Products -> Custom "
            "Fields) or the DB before upload — this is the check that catches "
            "'Field name X is unknown'",
        )]

    standard = set(LIMITS.get(csv_file, {}))
    # Columns the importer accepts that are not length-limited attributes.
    standard |= {
        "hideable", "imagefilename", "categorycodes", "collectioncodes",
        "relateditems", "netprice", "net_price", "price_net_price", "newitem",
        "producttype", "customize", "minimumquantity", "packquantity", "packedvolume",
        "promotionprice", "marketcode", "scanvalue", "scangroupcodes", "startsat",
        "suitegroup", "enablerelateditemdrilldown", "territorycodes", "tradenamecodes",
        "mappedbilltocode", "creditcardauth", "billtoshortname", "shiptoname",
        "shiptoterritorycodes", "showroomlocationcode", "mappedshiptocode",
        "shipinstructions", "carrier", "distributioncenter", "story", "options",
        "priceaddend", "pricefactor", "gradejumprisercount", "description",
        "imagename", "sortvalue", "optionformcodes", "baseitemcode",
    }
    prefixes = ("price_", "qty_", "startsat_", "optionset", "relateditems", "option")

    registered_lower = {str(name).strip().lower(): str(name).strip()
                        for name in registered if str(name).strip()}
    headers = set(lookup)

    findings = []

    unknown = sorted(
        h for h in headers
        if h not in standard
        and h not in registered_lower
        and not h.startswith(prefixes)
        and h not in {k.lower() for k in known_extra}
    )
    for header in unknown:
        near = difflib.get_close_matches(header, registered_lower, n=1, cutoff=0.7)
        hint = (
            f" — did you mean the registered field '{registered_lower[near[0]]}'? "
            f"(case/spelling drift)" if near else
            " — register it in Admin (Products -> Custom Fields, 'Send to iPad') or "
            "remove the column"
        )
        findings.append(fail(
            CHECK,
            f"column '{lookup[header]}' is neither a standard field nor a registered "
            f"custom field. The importer will log \"Field name {header} is unknown\" "
            f"and DROP the data{hint}",
        ))

    missing = sorted(
        registered_lower[name] for name in registered_lower if name not in headers
    )
    for name in missing:
        findings.append(warn(
            CHECK,
            f"registered custom field '{name}' has no column in this file — the "
            f"importer logs \"Custom field '{name}' is missing\". Send the column with "
            f"empty values if you mean to clear it; omitting it does NOT clear it",
        ))

    return findings


def skipped(reason):
    return [skip(CHECK, reason)]
