"""End-to-end tests for preflight_gate.py — the command an operator actually runs.

Two contracts are being pinned:

1. **Exit codes.** 1 blocks the upload, 2 means a check could not run, 0 with warnings is
   a pass. A phase gate branches on these.
2. **Nothing is ever silently absent.** A check that does not apply prints `SKIP` with the
   flag that caused it; a check that could not confirm something prints a WARNING naming
   what went unconfirmed. There is no third outcome where a check just disappears.
"""
import json
import textwrap

import pytest

PROFILE = """# Client — eCat Client Profile

## Identity
- **Org shortname:** `acme`

## Archetype & applicability
- **Archetype:** standard
- **Product line:** ecat-ipad
- **Flags:** `options: none`
- **File owner mode:** csv
- **Image mode:** ftp
- **Source cutover date:** 2025-07-08
- **Sub-brands:** none
"""

PRODUCTS = (
    "BaseItemCode,LongDesc,TradeNameCode,CollectionCodes,CategoryCodes,ImageFileName\n"
    "A-1,Oak Chair,ML,SEATING,CHAIRS,a-1.jpg\n"
    "A-2,Oak Table,ML,SEATING,TABLES,a-2.jpg\n"
)


@pytest.fixture
def client(tmp_path):
    """A client folder with a profile and a Ready_For_Import dir, like the real layout."""
    root = tmp_path / "acme"
    ready = root / "00_Import_Files" / "Ready_For_Import"
    ready.mkdir(parents=True)
    (root / "CLIENT_PROFILE.md").write_text(PROFILE, encoding="utf-8")

    def _add(name, text):
        path = ready / name
        path.write_text(textwrap.dedent(text), encoding="utf-8")
        return path

    _add("products.csv", PRODUCTS)
    return root, ready, _add


def test_clean_run_passes_with_advisories(run_script, client):
    root, ready, _add = client
    rc, out = run_script("preflight_gate.py", "--client-dir", str(root),
                         "--dir", str(ready))
    assert rc == 0
    assert "PASS: no blocking issues" in out
    assert "advisory" in out


def test_header_names_the_org_the_profile_and_the_limit_provenance(run_script, client):
    root, ready, _add = client
    _, out = run_script("preflight_gate.py", "--client-dir", str(root),
                        "--dir", str(ready))
    assert "Pre-import gate — acme" in out
    assert "archetype=standard" in out
    assert "supercat_server @" in out
    assert "generated, never transcribed" in out


def test_flagged_subsystem_skips_with_its_reason(run_script, client):
    """acme declares `options: none`, so the OptionSet ref check must SKIP, not pass."""
    root, ready, _add = client
    _, out = run_script("preflight_gate.py", "--client-dir", str(root),
                        "--dir", str(ready))
    assert "SKIPPED" in out
    assert "flag: options none" in out
    assert "refs-optionsets" in out


def test_image_mode_skips_the_url_census(run_script, client):
    root, ready, _add = client
    _, out = run_script("preflight_gate.py", "--client-dir", str(root),
                        "--dir", str(ready))
    assert "flag: images ftp" in out
    assert "image-urls" in out


def test_without_a_profile_nothing_is_skipped(run_script, client):
    """An absent declaration must mean "check everything", never "skip quietly"."""
    root, ready, _add = client
    (root / "CLIENT_PROFILE.md").unlink()
    _, out = run_script("preflight_gate.py", "--client-dir", str(root),
                        "--dir", str(ready))
    assert "SKIPPED" not in out
    assert "archetype=UNDECLARED" in out


def test_missing_archetype_section_is_reported(run_script, client):
    root, ready, _add = client
    (root / "CLIENT_PROFILE.md").write_text(
        "# Client\n\n## Identity\n- **Org shortname:** `acme`\n", encoding="utf-8")
    _, out = run_script("preflight_gate.py", "--client-dir", str(root),
                        "--dir", str(ready))
    assert "no '## Archetype & applicability' section" in out


def test_no_live_state_is_announced_rather_than_assumed(run_script, client):
    root, ready, _add = client
    _, out = run_script("preflight_gate.py", "--client-dir", str(root),
                        "--dir", str(ready))
    assert "NONE SUPPLIED" in out
    assert "Pass --live-state before a hard-delete upload" in out


def test_bom_blocks_the_whole_run(run_script, client):
    root, ready, _add = client
    (ready / "stories.csv").write_bytes(
        b"\xef\xbb\xbfBaseItemCode,ProductStory\nA-1,A chair\n")
    rc, out = run_script("preflight_gate.py", "--client-dir", str(root),
                         "--dir", str(ready))
    assert rc == 1
    assert "UTF-8 BOM" in out


def test_hard_delete_file_blocks_until_acknowledged(run_script, client, tmp_path):
    root, ready, _add = client
    _add("customers.csv",
         "BillToCode,BillToName,BillToAddress1,BillToCity,BillToState,"
         "BillToPostCode,DefaultPriceCode\n"
         "C-1,Acme,1 Main St,Austin,TX,78701,dn\n")
    live = tmp_path / "live.json"
    live.write_text(json.dumps({
        "shortname": "acme",
        "queried_at": "2026-07-27T20:00:00Z",
        "price_levels": ["dn"],
        "keys": {"customers.csv": ["C-1", "C-2", "C-3"]},
        "counts": {"customers.csv": 3},
    }), encoding="utf-8")

    rc, out = run_script("preflight_gate.py", "--client-dir", str(root),
                         "--dir", str(ready), "--live-state", str(live))
    assert rc == 1
    assert "HARD-DELETES" in out
    assert "--ack-deletes" in out

    rc, out = run_script("preflight_gate.py", "--client-dir", str(root),
                         "--dir", str(ready), "--live-state", str(live),
                         "--ack-deletes")
    assert rc == 0
    assert "[acknowledged]" in out


def test_the_tcd_blocker_is_caught_through_the_gate(run_script, client):
    root, ready, _add = client
    _add("customers.csv",
         "BillToCode,BillToName,BillToAddress1,BillToCity,BillToState,"
         "BillToPostCode,DefaultPriceCode\n"
         "C-1,Acme,1 Main St,Austin,TX,78701,0\n")
    rc, out = run_script("preflight_gate.py", "--client-dir", str(root),
                         "--dir", str(ready), "--ack-deletes")
    assert rc == 1
    assert "DefaultPriceCode '0' is a placeholder/status" in out


def test_foreign_inventory_file_blocks(run_script, client, tmp_path):
    """The mali/leg wipe, through the CLI."""
    root, ready, _add = client
    _add("inventory.csv",
         "BaseItemCode,QtyAvailable\nLEG-1,5\nLEG-2,5\nLEG-3,5\n")
    live = tmp_path / "live.json"
    live.write_text(json.dumps({
        "shortname": "acme",
        "keys": {"inventory.csv": ["A-1", "A-2"]},
    }), encoding="utf-8")
    rc, out = run_script("preflight_gate.py", "--client-dir", str(root),
                         "--dir", str(ready), "--live-state", str(live),
                         "--ack-deletes")
    assert rc == 1
    assert "may belong to a different org" in out


def test_file_outside_the_client_folder_blocks(run_script, client, tmp_path):
    root, ready, _add = client
    stray = tmp_path / "elsewhere"
    stray.mkdir()
    (stray / "inventory.csv").write_text(
        "BaseItemCode,QtyAvailable\nA-1,5\n", encoding="utf-8")
    rc, out = run_script("preflight_gate.py", "--client-dir", str(root),
                         "--files", str(stray / "inventory.csv"), "--ack-deletes")
    assert rc == 1
    assert "outside the client's build folder" in out


def test_orphan_inventory_row_blocks(run_script, client):
    root, ready, _add = client
    _add("inventory.csv", "BaseItemCode,QtyAvailable\nA-1,5\nGHOST,9\n")
    rc, out = run_script("preflight_gate.py", "--client-dir", str(root),
                         "--dir", str(ready), "--ack-deletes")
    assert rc == 1
    assert "GHOST" in out
    assert "Product not found, record ignored" in out


def test_options_without_groups_blocks(run_script, client):
    root, ready, _add = client
    _add("options.csv", "Code,Name\n100,Black\n")
    rc, out = run_script("preflight_gate.py", "--client-dir", str(root),
                         "--dir", str(ready), "--ack-deletes")
    assert rc == 1
    assert "options.csv is being sent WITHOUT option_groups.csv" in out


def test_manifest_includes_the_second_groups_pass(run_script, client):
    root, ready, _add = client
    _add("options.csv", "Code,Name\n100,Black\n")
    _add("option_groups.csv", "Code,Name,Options\nFIN,Finishes,100\n")
    _, out = run_script("preflight_gate.py", "--client-dir", str(root),
                        "--dir", str(ready), "--ack-deletes")
    assert ("upload in this order: options.csv -> option_groups.csv -> products.csv "
            "-> option_groups.csv") in out


def test_declared_order_is_verified(run_script, client):
    root, ready, _add = client
    _add("inventory.csv", "BaseItemCode,QtyAvailable\nA-1,5\n")
    rc, out = run_script("preflight_gate.py", "--client-dir", str(root),
                         "--dir", str(ready), "--ack-deletes",
                         "--order", "inventory.csv,products.csv")
    assert rc == 1
    assert "declared order puts products.csv" in out


def test_live_state_feeds_the_checks_that_need_it(run_script, client, tmp_path):
    """One JSON document supplies price levels, taxonomy, keys, counts, and images."""
    root, ready, _add = client
    live = tmp_path / "live.json"
    live.write_text(json.dumps({
        "shortname": "acme",
        "queried_at": "2026-07-27T20:00:00Z",
        "taxonomy": {"codes": ["ML", "SEATING", "CHAIRS", "TABLES"], "groups": ["MAIN"]},
        "custom_fields": {"products": []},
        "keys": {"products.csv": ["A-1", "A-2"]},
        "counts": {"products.csv": 2},
        "uploaded_images": ["a-1.jpg", "a-2.jpg"],
    }), encoding="utf-8")
    rc, out = run_script("preflight_gate.py", "--client-dir", str(root),
                         "--dir", str(ready), "--live-state", str(live))
    assert rc == 0
    assert "queried 2026-07-27T20:00:00Z" in out
    assert "2/2 products have their PRIMARY image uploaded" in out
    assert "nothing will be deleted" in out


def test_unqueried_live_state_is_called_stale(run_script, client, tmp_path):
    root, ready, _add = client
    live = tmp_path / "live.json"
    live.write_text(json.dumps({"shortname": "acme"}), encoding="utf-8")
    _, out = run_script("preflight_gate.py", "--client-dir", str(root),
                        "--dir", str(ready), "--live-state", str(live))
    assert "UNKNOWN — treat as stale" in out


def test_missing_taxonomy_code_blocks(run_script, client, tmp_path):
    root, ready, _add = client
    live = tmp_path / "live.json"
    live.write_text(json.dumps({
        "shortname": "acme",
        "taxonomy": {"codes": ["ML", "SEATING"], "groups": ["MAIN"]},
    }), encoding="utf-8")
    rc, out = run_script("preflight_gate.py", "--client-dir", str(root),
                         "--dir", str(ready), "--live-state", str(live))
    assert rc == 1
    assert "CategoryCodes 'CHAIRS' does not exist in Admin" in out


def test_two_files_resolving_to_one_family_is_reported(run_script, client):
    """Only one file per family is checked, so the second must not pass unnoticed."""
    root, ready, _add = client
    _add("products_final.csv", PRODUCTS)
    _, out = run_script("preflight_gate.py", "--client-dir", str(root),
                        "--dir", str(ready))
    assert "both resolve to products.csv" in out
    assert "Upload exactly one file per family" in out


def test_empty_file_is_reported_not_skipped(run_script, client):
    root, ready, _add = client
    _add("stories.csv", "")
    _, out = run_script("preflight_gate.py", "--client-dir", str(root),
                        "--dir", str(ready))
    assert "no data rows / empty header" in out


def test_directory_with_no_ecat_files(run_script, tmp_path):
    empty = tmp_path / "empty"
    empty.mkdir()
    rc, out = run_script("preflight_gate.py", "--dir", str(empty))
    assert rc == 0
    assert "no eCat import files found" in out


def test_no_target_is_a_usage_error(run_script):
    rc, out = run_script("preflight_gate.py")
    assert rc == 2
    assert "--files and/or --dir" in out


def test_claims_flag_documents_what_is_deliberately_not_enforced(run_script):
    """The retired limits have to be discoverable, or the next agent re-adds them."""
    rc, out = run_script("preflight_gate.py", "--claims")
    assert rc == 0
    assert "NOT enforced" in out
    assert "ProductStory <= 500" in out
    assert "unbounded" in out
