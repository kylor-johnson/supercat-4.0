#!/usr/bin/env python3
"""Build eCat customers.csv from CopperSmith Odoo dealer export."""
from __future__ import annotations

import csv
import re
from pathlib import Path

BASE = Path(__file__).parent
SRC = BASE.parent / "Source Data" / "Dealers_eCat-Table 1.csv"
OUT = BASE / "customers.csv"
REPORT = BASE / "customers_build_report.csv"

DEFAULT_PRICE_CODE = "map"
DEFAULT_TERRITORY = "100"
INFERRED_ZIP = {"contact_334": "30540"}

US_STATES = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
}

CA_PROVINCES = {
    "Alberta": "AB",
    "British Columbia": "BC",
    "Manitoba": "MB",
    "New Brunswick": "NB",
    "Newfoundland and Labrador": "NL",
    "Nova Scotia": "NS",
    "Northwest Territories": "NT",
    "Nunavut": "NU",
    "Ontario": "ON",
    "Prince Edward Island": "PE",
    "Quebec": "QC",
    "Saskatchewan": "SK",
    "Yukon": "YT",
}

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
SYSTEM_NOTE_PREFIXES = ("region=default",)

HEADERS = [
    "BillToCode",
    "BillToName",
    "BillToShortname",
    "BillToAddress1",
    "BillToAddress2",
    "BillToCity",
    "BillToState",
    "BillToPostCode",
    "BillToCountry",
    "TerritoryCodes",
    "BuyerEmail",
    "BuyerPhone",
    "DefaultPriceCode",
    "Terms",
    "ShipToCode",
    "ShipToName",
    "ShipToAddress1",
    "ShipToAddress2",
    "ShipToCity",
    "ShipToState",
    "ShipToPostCode",
    "ShipToCountry",
    "ShipInstructions",
]


def load_csv(path: Path) -> list[dict[str, str]]:
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def abbrev_state(state: str, country: str) -> str:
    state = (state or "").strip()
    if not state:
        return state
    if len(state) == 2 and state.isalpha():
        return state.upper()
    if country == "CA":
        return CA_PROVINCES.get(state, state)
    return US_STATES.get(state, state)


def normalize_country(country: str) -> str:
    country = (country or "").strip()
    if country == "United States":
        return "US"
    if country == "Canada":
        return "CA"
    return country


def first_email(raw: str) -> str:
    raw = (raw or "").strip()
    if not raw:
        return ""
    for part in re.split(r"[;\s]+", raw):
        part = part.strip().strip(",")
        if part and EMAIL_RE.match(part):
            return part[:50]
    return ""


def normalize_phone(raw: str) -> str:
    return (raw or "").strip()[:25]


def ship_instructions(notes: str) -> str:
    notes = (notes or "").strip()
    if not notes:
        return ""
    if any(notes.startswith(p) for p in SYSTEM_NOTE_PREFIXES):
        return ""
    return notes[:100]


def post_code(external_id: str, raw: str) -> str:
    raw = (raw or "").strip()
    if raw:
        return raw[:20]
    return INFERRED_ZIP.get(external_id, "")


def territory(raw: str) -> str:
    raw = (raw or "").strip()
    return raw if raw else DEFAULT_TERRITORY


def build_report_row(
    external_id: str,
    name: str,
    issue: str,
    detail: str,
    action: str,
) -> dict[str, str]:
    return {
        "BillToCode": external_id,
        "BillToName": name,
        "Issue": issue,
        "Detail": detail,
        "Action": action,
    }


def transform_row(row: dict[str, str], report: list[dict[str, str]]) -> dict[str, str] | None:
    if (row.get("Type") or "").strip() == "Vendor":
        report.append(
            build_report_row(
                row.get("external_id", ""),
                row.get("Name", ""),
                "vendor_excluded",
                f"Type={row.get('Type')}",
                "Row dropped",
            )
        )
        return None

    external_id = (row.get("external_id") or "").strip()
    name = (row.get("Name") or "").strip()
    country = normalize_country(row.get("Country", ""))
    state = abbrev_state(row.get("State", ""), country)
    zip_code = post_code(external_id, row.get("Zip Code", ""))
    terr = territory(row.get("Territory #", ""))
    odoo_pricelist = (row.get("Pricelist") or "").strip()
    email_raw = row.get("Email", "")

    if not (row.get("Territory #") or "").strip():
        report.append(
            build_report_row(
                external_id,
                name,
                "territory_defaulted",
                "Territory # blank",
                f"Set TerritoryCodes={DEFAULT_TERRITORY}",
            )
        )

    if external_id in INFERRED_ZIP and not (row.get("Zip Code") or "").strip():
        report.append(
            build_report_row(
                external_id,
                name,
                "zip_inferred",
                "Zip Code blank",
                f"Set BillToPostCode={INFERRED_ZIP[external_id]}",
            )
        )

    if odoo_pricelist:
        report.append(
            build_report_row(
                external_id,
                name,
                "odoo_pricelist",
                odoo_pricelist,
                f"DefaultPriceCode={DEFAULT_PRICE_CODE} (no eCat level match)",
            )
        )

    if ";" in email_raw or email_raw.count("@") > 1:
        report.append(
            build_report_row(
                external_id,
                name,
                "email_simplified",
                email_raw[:80],
                f"BuyerEmail={first_email(email_raw)!r}",
            )
        )

    addr1 = (row.get("Street") or "").strip()[:60]
    addr2 = (row.get("Street 2") or "").strip()[:60]
    city = (row.get("City") or "").strip()[:60]

    out = {
        "BillToCode": external_id[:15],
        "BillToName": name[:60],
        "BillToShortname": name[:25],
        "BillToAddress1": addr1,
        "BillToAddress2": addr2,
        "BillToCity": city,
        "BillToState": state[:60],
        "BillToPostCode": zip_code,
        "BillToCountry": country[:60],
        "TerritoryCodes": terr[:60],
        "BuyerEmail": first_email(email_raw),
        "BuyerPhone": normalize_phone(row.get("Phone", "")),
        "DefaultPriceCode": DEFAULT_PRICE_CODE,
        "Terms": (row.get("Customer Payment Terms") or "").strip()[:30],
        "ShipToCode": external_id[:15],
        "ShipToName": name[:60],
        "ShipToAddress1": addr1,
        "ShipToAddress2": addr2,
        "ShipToCity": city,
        "ShipToState": state[:60],
        "ShipToPostCode": zip_code,
        "ShipToCountry": country[:60],
        "ShipInstructions": ship_instructions(row.get("Notes", "")),
    }
    return out


def sort_key(row: dict[str, str]) -> tuple[int, str]:
    code = row["BillToCode"]
    m = re.match(r"contact_(\d+)$", code)
    if m:
        return (0, f"{int(m.group(1)):08d}")
    return (1, code)


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"Missing source file: {SRC}")

    dealers = load_csv(SRC)
    report: list[dict[str, str]] = []
    customers: list[dict[str, str]] = []

    for row in dealers:
        out = transform_row(row, report)
        if out:
            customers.append(out)

    customers.sort(key=sort_key)

    with open(OUT, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(customers)

    report_fields = ["BillToCode", "BillToName", "Issue", "Detail", "Action"]
    with open(REPORT, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=report_fields)
        writer.writeheader()
        writer.writerows(report)

    print(f"Wrote {OUT.name}: {len(customers)} customers")
    print(f"Wrote {REPORT.name}: {len(report)} report rows")
    print(f"Excluded vendors: {sum(1 for r in report if r['Issue'] == 'vendor_excluded')}")


if __name__ == "__main__":
    main()
