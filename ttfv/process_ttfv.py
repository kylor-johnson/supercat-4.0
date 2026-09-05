#!/usr/bin/env python3
"""
TTFV (Time to First Value) Report Generator - February 2026
Processes Mixpanel events, admin users, and HubSpot/Postgres dates
to calculate TTFV metrics per org.
"""

import json
import ast
from datetime import datetime, date
from collections import defaultdict
import os

MIXPANEL_FILE = "/Users/kylorjohnson/.cursor/projects/Users-kylorjohnson-Library-Mobile-Documents-com-apple-CloudDocs-SuperCat-4-0/agent-tools/8c3bff1b-0ca7-447e-a989-16121c6fee97.txt"
ADMIN_FILE = "/Users/kylorjohnson/.cursor/projects/Users-kylorjohnson-Library-Mobile-Documents-com-apple-CloudDocs-SuperCat-4-0/agent-tools/cedb144c-23f0-48ea-9000-f9555815eded.txt"
OUTPUT_FILE = "/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/ttfv/ttfv_results_feb2026.json"

HUBSPOT_DATES = {
    "abol": "2024-03-29", "ali": "2024-06-13", "am": "2024-10-21",
    "arl": "2025-03-13", "bp": "2024-12-20", "bts": "2024-07-29",
    "clc": "2023-09-22", "dccl": "2024-06-04", "df": "2024-06-03",
    "di": "2025-02-28", "elk": "2024-07-13", "fal": "2024-08-01",
    "gc": "2024-05-29", "gl": "2024-09-27", "hf": "2024-08-20",
    "ihm": "2024-11-18", "ilc": "2024-03-11", "jcusa": "2025-06-13",
    "kll": "2025-10-03", "krb": "2024-08-15", "luc": "2025-02-28",
    "mlg": "2025-01-20", "ol": "2025-03-19", "ril": "2024-08-20",
    "rw": "2024-11-07", "sci": "2024-06-20", "ufi": "2025-06-26",
    "wag": "2025-02-07", "yw": "2024-05-10",
}

CREATED_AT_DATES = {
    "acsd": "2014-07-07", "afx": "2023-03-22", "ah": "2018-03-26",
    "all": "2023-09-19", "ap": "2012-01-26", "arl": "2025-03-26",
    "asi": "2011-12-13", "ati": "2016-11-08", "bc": "2013-08-17",
    "bcf": "2022-09-13", "bei": "2023-06-27", "big": "2018-05-10",
    "blh": "2019-02-04", "bmc": "2011-06-17", "bobo": "2024-03-27",
    "bri": "2023-08-23", "bsc": "2011-08-02", "cci": "2021-07-25",
    "cf": "2011-05-20", "cfg": "2015-02-04", "cfsd": "2019-10-30",
    "cl": "2014-04-14", "clli": "2019-10-30", "clm": "2013-09-26",
    "da": "2013-09-04", "dals": "2023-08-17", "di": "2023-12-20",
    "eglo": "2022-05-05", "eglo_can": "2024-03-13", "ekc": "2013-05-14",
    "el": "2020-02-17", "eli": "2013-12-10", "et2": "2019-03-21",
    "etl": "2019-04-08", "fc": "2017-11-28", "ffdm": "2015-09-11",
    "fms": "2016-10-06", "frh": "2011-03-04", "fsf": "2023-11-07",
    "gcl": "2024-03-01", "gg": "2013-06-24", "gh": "2013-04-24",
    "gsa": "2011-07-08", "heb": "2012-03-23", "hfg": "2022-01-28",
    "hh": "2014-09-09", "hmjc": "2018-09-06", "hvl": "2014-04-14",
    "ih": "2021-11-30", "ihw": "2016-08-31", "jc": "2013-10-24",
    "jyc": "2014-08-11", "kal": "2019-09-09", "khi": "2024-01-03",
    "kii": "2015-06-25", "kkc": "2015-11-03", "kl": "2012-11-30",
    "lpf": "2019-03-21", "lss": "2023-09-25", "mah": "2019-02-27",
    "mfc": "2012-11-09", "mh": "2023-02-22", "mhc": "2012-11-02",
    "ml": "2020-07-24", "mlc": "2023-08-23", "mli": "2019-03-21",
    "mpc": "2015-05-04", "ol": "2025-03-24", "opame": "2024-10-28",
    "pf": "2012-05-22", "pol": "2020-03-06", "pw": "2012-12-05",
    "rac": "2011-11-25", "rf": "2021-11-01", "sarreid": "2010-09-11",
    "sbl": "2023-02-09", "sbmh": "2011-03-04", "sc": "2014-02-05",
    "sca": "2015-05-05", "sccon": "2015-04-28", "scw": "2015-04-28",
    "shl": "2012-07-10", "sl": "2013-11-12", "soi": "2024-02-20",
    "sp": "2018-09-06", "ssi": "2011-11-25", "st": "2015-09-10",
    "swc": "2013-05-18", "ta": "2016-11-22", "tam": "2025-05-05",
    "tel": "2015-03-30", "tl": "2014-04-10", "tla": "2017-05-08",
    "uhc": "2021-07-06", "vce": "2022-04-25", "vcg": "2019-04-18",
    "vic": "2022-10-26", "vl": "2019-09-27", "wa": "2019-12-15",
    "wac": "2023-02-09", "wwjc": "2011-05-16", "yw": "2024-05-16",
}

ORG_NAMES = {
    "asi": "Abaline Supply Inc.", "ali": "Access Lighting",
    "all": "Accord Lighting", "afx": "AFX, Inc.",
    "ap": "Alden Home", "am": "Alfonso Marina",
    "ah": "Alfresco Home", "abol": "America's Backyards and Outdoor Living",
    "arl": "Arabela Lighting", "ati": "Art Trends & Prestige Arts",
    "acsd": "Ateliers Davoy", "big": "Baker-McGuire",
    "bmc": "Bassett Mirror", "bei": "Bethel International",
    "blh": "Bliss Studio", "bobo": "BOBO Intriguing Objects",
    "bcf": "Braxton Culler", "bts": "BT Shalom",
    "bri": "Bulbrite", "bp": "Buster & Punch",
    "bsc": "Butler Specialty Company", "clc": "Capital Lighting Fixture Co.",
    "cf": "Century Furniture", "cfg": "Charleston Forge",
    "cl": "Corbett Lighting", "clli": "Craftmade",
    "clm": "Crystorama", "cci": "Currey & Company",
    "da": "Dainolite Ltd.", "dals": "DALS Lighting",
    "di": "DEBRAH FURNITURE USA", "bc": "Decca Home / Bolier & Co,",
    "df": "Designer's Fountain", "dccl": "Donald Choi Canada",
    "eglo_can": "EGLO Canada", "eglo": "Eglo USA Inc.",
    "ekc": "Elan, a Kichler Company", "eli": "Elegant Furniture & Lighting",
    "etl": "ELICO LTD.", "elk": "Elk Home",
    "et2": "ET2 Lighting", "el": "Eurofase Inc.",
    "fal": "Fine Art Handcrafted Lighting", "ffdm": "Fine Furniture Design",
    "fsf": "Four Seasons Furniture", "frh": "French Heritage",
    "fc": "Furniture Classics", "gh": "Gabby",
    "gcl": "Geo Contemporary", "gg": "Godinger Group",
    "gsa": "Godinger Silver Art Co.", "gl": "Golden Lighting",
    "gc": "Groupe Courchesne", "hmjc": "Hancock & Moore / Jessica Charles",
    "hh": "Highland House", "heb": "Home Essentials & Beyond",
    "hf": "Hooker Furnishings", "hfg": "Hubbardton Forge",
    "hvl": "Hudson Valley Lighting", "ilc": "Ideal Living",
    "ihw": "Interlude Furniture", "ih": "Interlude Home",
    "ihm": "International Home Miami", "jyc": "Jamie Young Company",
    "jcusa": "Jonathan Charles Designs Inc.", "jc": "Jonathan Charles Fine Furniture Ltd.",
    "kal": "Kalco Lighting / Allegri Crystal", "krb": "Kaleen Rugs & Broadloom",
    "khi": "Karat Home Inc.", "kii": "Kennedy International, Inc.",
    "kl": "Kichler Lighting", "kkc": "Kindel Karges Furniture",
    "kll": "Kuzco Lighting Inc.", "lss": "Lifestyle Solutions",
    "lpf": "Linon/Powell Furniture", "luc": "Lucas McKearn",
    "mh": "Magnussen Home", "mlc": "Matteo Lighting",
    "mli": "Maxim Lighting", "ml": "Millennium Lighting",
    "mlg": "Minka Lighting Group", "mah": "Moda at Home Enterprises Ltd",
    "mhc": "Moe's Home Collection", "mfc": "Morgan Fabrics Corporation",
    "ol": "Oly Studio", "opame": "Opame Collective",
    "pol": "PageOne Lighting", "pf": "Palecek",
    "pw": "Philip Whitney", "mpc": "Pioneer Morton",
    "ril": "Ratana International Ltd.", "rw": "RENWIL",
    "rac": "Ricci Argentieri Company", "rf": "Rowe Furniture",
    "sp": "Sabine Pools, Spas, & Furnitur", "sci": "Sanders Collection Inc",
    "sarreid": "Sarreid, Ltd.", "swc": "Sauder Woodworking",
    "shl": "Savoy House Lighting", "sbl": "Schonbek Lighting",
    "sca": "Shadow Catchers", "soi": "Silver One",
    "st": "Sixtrees Limited", "sbmh": "Somerset Bay and Modern History",
    "sl": "Sonneman - A Way of Light", "cfsd": "Stoneline Designs by Charleston Forge",
    "ssi": "Studio Silversmiths, Inc.", "scw": "Summer Classics",
    "sccon": "Summer Classics Contract", "sc": "Summer Classics Retail",
    "ta": "Theodore Alexander", "tam": "Theodore Alexander Manhasset",
    "tel": "Tomlinson Companies", "tl": "Troy Lighting",
    "ufi": "Universal Furniture", "uhc": "Uniware Housewares Corp.",
    "vl": "Varaluz Lighting & Varaluz Casa", "vic": "Vaxcel International Corporation",
    "tla": "Visual Comfort - Modern", "fms": "Visual Comfort - Studio /Fans",
    "vce": "Visual Comfort Europe", "vcg": "Visual Comfort Signature",
    "wac": "WAC/Modern Forms Lighting", "wag": "Wendover Art Group",
    "wa": "Wesley Allen", "wwjc": "Wildwood/Chelsea House",
    "yw": "Yutzy Woodworking",
}

ACTION_TYPE_MAP = {
    "document_email_drafted": "Email Draft",
    "item_email_drafted": "Email Draft",
    "item_added_via_magic_button": "Presentation (Stack)",
}


def parse_date(s):
    return datetime.strptime(s, "%Y-%m-%d").date()


def get_start_date(org):
    """Return (start_date, source) using HubSpot first, then created_at fallback."""
    if org in HUBSPOT_DATES:
        return parse_date(HUBSPOT_DATES[org]), "HubSpot"
    if org in CREATED_AT_DATES:
        return parse_date(CREATED_AT_DATES[org]), "created_at"
    return None, "unknown"


def load_mixpanel_events():
    with open(MIXPANEL_FILE, "r") as f:
        raw = json.load(f)
    events = []
    for row in raw["data"]:
        ed = row["event_date"]
        if isinstance(ed, dict):
            date_str = ed["value"]
        else:
            date_str = ed
        events.append({
            "org": row["org"].lower(),
            "username": row["username"].lower(),
            "event_name": row["event_name"],
            "event_date": parse_date(date_str),
        })
    return events


def load_admin_users():
    with open(ADMIN_FILE, "r") as f:
        raw = f.read()
    admin_list = ast.literal_eval(raw)
    admins = defaultdict(set)
    for entry in admin_list:
        admins[entry["org"].lower()].add(entry["username"].lower())
    return admins


def main():
    print("Loading Mixpanel events...")
    events = load_mixpanel_events()
    print(f"  Loaded {len(events)} first-events across orgs")

    print("Loading admin users...")
    admins = load_admin_users()
    print(f"  Loaded admins for {len(admins)} orgs")

    all_orgs = sorted(ORG_NAMES.keys())
    print(f"Processing {len(all_orgs)} active orgs...\n")

    events_by_org = defaultdict(list)
    for e in events:
        events_by_org[e["org"]].append(e)

    results = []
    for org in all_orgs:
        org_name = ORG_NAMES.get(org, org)
        start_date, start_source = get_start_date(org)
        org_events = events_by_org.get(org, [])
        org_admins = admins.get(org, set())

        non_admin_events = [
            e for e in org_events if e["username"] not in org_admins
        ]

        if not org_events:
            results.append({
                "org_shortname": org,
                "org_name": org_name,
                "ttfv_days": None,
                "action_type": None,
                "start_date": str(start_date) if start_date else None,
                "first_action_date": None,
                "start_date_source": start_source,
                "ttfv_username": None,
                "status": "no_ttfv_events",
            })
            continue

        if not non_admin_events:
            results.append({
                "org_shortname": org,
                "org_name": org_name,
                "ttfv_days": None,
                "action_type": None,
                "start_date": str(start_date) if start_date else None,
                "first_action_date": None,
                "start_date_source": start_source,
                "ttfv_username": None,
                "status": "no_valid_ttfv",
            })
            continue

        earliest = min(non_admin_events, key=lambda e: e["event_date"])
        action_type = ACTION_TYPE_MAP.get(earliest["event_name"], earliest["event_name"])
        first_action_date = earliest["event_date"]

        if start_date:
            ttfv_days = (first_action_date - start_date).days
        else:
            ttfv_days = None

        results.append({
            "org_shortname": org,
            "org_name": org_name,
            "ttfv_days": ttfv_days,
            "action_type": action_type,
            "start_date": str(start_date) if start_date else None,
            "first_action_date": str(first_action_date),
            "start_date_source": start_source,
            "ttfv_username": earliest["username"],
            "status": "valid",
        })

    valid = [r for r in results if r["status"] == "valid"]
    no_valid = [r for r in results if r["status"] == "no_valid_ttfv"]
    no_events = [r for r in results if r["status"] == "no_ttfv_events"]
    hubspot_count = sum(1 for r in results if r["start_date_source"] == "HubSpot")
    created_at_count = sum(1 for r in results if r["start_date_source"] == "created_at")

    summary = {
        "report_period": "February 2026",
        "generated_at": datetime.now().isoformat(),
        "total_orgs": len(all_orgs),
        "orgs_with_valid_ttfv": len(valid),
        "orgs_no_valid_ttfv": len(no_valid),
        "orgs_no_ttfv_events": len(no_events),
        "orgs_hubspot": hubspot_count,
        "orgs_created_at": created_at_count,
    }

    if valid:
        ttfv_values = [r["ttfv_days"] for r in valid if r["ttfv_days"] is not None]
        if ttfv_values:
            summary["median_ttfv_days"] = sorted(ttfv_values)[len(ttfv_values) // 2]
            summary["avg_ttfv_days"] = round(sum(ttfv_values) / len(ttfv_values), 1)
            summary["min_ttfv_days"] = min(ttfv_values)
            summary["max_ttfv_days"] = max(ttfv_values)

    output = {"summary": summary, "orgs": results}

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2)
    print(f"Results written to: {OUTPUT_FILE}\n")

    # Print summary table
    print("=" * 110)
    print(f"{'TTFV Report - February 2026':^110}")
    print("=" * 110)
    print(f"\n{'SUMMARY':}")
    print(f"  Total Active Orgs:       {summary['total_orgs']}")
    print(f"  Valid TTFV:              {summary['orgs_with_valid_ttfv']}")
    print(f"  No Valid TTFV (admins):  {summary['orgs_no_valid_ttfv']}")
    print(f"  No TTFV Events:          {summary['orgs_no_ttfv_events']}")
    print(f"  Start Date - HubSpot:    {summary['orgs_hubspot']}")
    print(f"  Start Date - created_at: {summary['orgs_created_at']}")
    if "avg_ttfv_days" in summary:
        print(f"  Avg TTFV Days:           {summary['avg_ttfv_days']}")
        print(f"  Median TTFV Days:        {summary['median_ttfv_days']}")
        print(f"  Min TTFV Days:           {summary['min_ttfv_days']}")
        print(f"  Max TTFV Days:           {summary['max_ttfv_days']}")

    print(f"\n{'─' * 110}")
    header = f"{'Org':<8} {'Org Name':<35} {'TTFV':>6} {'Action Type':<22} {'Start Date':<12} {'Source':<11} {'First Action':<12} {'User':<15}"
    print(header)
    print(f"{'─' * 110}")

    for r in sorted(results, key=lambda x: (x["ttfv_days"] is None, x["ttfv_days"] or 0)):
        ttfv = str(r["ttfv_days"]) if r["ttfv_days"] is not None else "—"
        action = r["action_type"] or "—"
        sd = r["start_date"] or "—"
        src = r["start_date_source"] or "—"
        fa = r["first_action_date"] or "—"
        user = r["ttfv_username"] or "—"
        name = r["org_name"][:34]
        print(f"{r['org_shortname']:<8} {name:<35} {ttfv:>6} {action:<22} {sd:<12} {src:<11} {fa:<12} {user:<15}")

    print(f"{'─' * 110}")

    # Print orgs with no events / no valid TTFV
    if no_events:
        print(f"\nOrgs with NO Mixpanel events ({len(no_events)}):")
        for r in no_events:
            print(f"  {r['org_shortname']:<8} {r['org_name']}")

    if no_valid:
        print(f"\nOrgs with events but NO valid (non-admin) TTFV ({len(no_valid)}):")
        for r in no_valid:
            print(f"  {r['org_shortname']:<8} {r['org_name']}")


if __name__ == "__main__":
    main()
