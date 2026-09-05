#!/usr/bin/env python3
"""Assemble 01_CODE_CENSUS.json from the per-section outputs."""
import json
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.dirname(HERE)


def load(n):
    return json.load(open(os.path.join(HERE, n)))


units, loc, surface, rest = load("units.json"), load("loc_split.json"), \
    load("surface.json"), load("rest.json")
diag = load("loc_diag.json")

ios_pin = subprocess.run(["git", "-C", "/tmp/ecat-audit/ios-master", "rev-parse", "HEAD"],
                         capture_output=True, text=True).stdout.strip()
srv_pin = subprocess.run(["git", "-C", "/tmp/ecat-audit/server-master", "rev-parse", "HEAD"],
                         capture_output=True, text=True).stdout.strip()

census = {
    "phase": 1,
    "generated_utc": subprocess.run(["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"],
                                    capture_output=True, text=True).stdout.strip(),
    "pins": {
        "ios_repo": "sarreid_ios", "ios_commit": ios_pin,
        "server_repo": "supercat_server", "server_commit": srv_pin,
        "worktrees": ["/tmp/ecat-audit/ios-master", "/tmp/ecat-audit/server-master",
                      "/tmp/ecat-audit/server-ecatweb"],
    },
    "scripts": sorted(f for f in os.listdir(HERE) if f.startswith("p1_")),

    "1_1_surface_inventory": {
        "summary": surface["summary"],
        "screens": surface["screens"],
        "storyboard_initial_view_controllers": surface["storyboard_initial"],
    },
    "1_2_loc_split": {
        "classification_rule": loc["rule"],
        "totals_approved_rule_logic_first": loc["totals_approved_rule"],
        "totals_sensitivity_ui_first": loc["totals_sensitivity_ui_first"],
        "entangled_loc_matches_logic_and_ui": diag["entangled_loc"],
        "cooccurrence_logic_ui_glue_by_loc": diag["cooccurrence"],
        "unclassified_trivial_le3loc": loc["unclassified_trivial_le3loc"],
        "unclassified_substantive_gt3loc": loc["unclassified_substantive_gt3loc"],
        "unclassified_top_members": diag["unclassified_top"],
        "mixed_class_files": loc["mixed_files"],
        "residue_lines_assigned_to_file_dominant_class": loc["residue_lines"],
        "ib_xml_counted_separately": loc["ib_xml"],
        "units": loc["units"],
        "files": loc["files"],
    },
    "1_3_data_model": rest["data_model"],
    "1_4_sync_offline_engine": rest["sync_engine"],
    "1_5_integration_surface": rest["integration_surface"],
    "1_6_port_hazards": {
        "hazards": rest["port_hazards"],
        "shipped_assets_without_source": rest["port_hazards_shipped_assets_without_source"],
    },
    "1_7_confidence_signals": rest["confidence_signals"],
    "1_8_dead_code": rest["dead_code"],
    "unit_boundaries": {
        "method": "Xcode PBXGroup tree (approved Phase 0 §1.3)",
        "group_count": units["group_count_total"],
        "unit_count": units["unit_count"],
        "files_mapped": units["file_count_mapped"],
        "unresolved_child_refs": units["unresolved_child_refs"],
        "units": {u: {"files": len(d["files"])} for u, d in units["units"].items()},
    },
}
p = os.path.join(OUTDIR, "01_CODE_CENSUS.json")
json.dump(census, open(p, "w"), indent=1)
print("wrote", p, os.path.getsize(p), "bytes")
