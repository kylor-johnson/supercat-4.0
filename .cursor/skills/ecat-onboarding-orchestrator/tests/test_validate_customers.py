"""Regression tests for validate_customers.py.

The headline case is the Terracotta (tcd) blocker: DefaultPriceCode = 0 / status text
=> every row rejected => 0 customers imported. That must always be caught.
"""


def test_clean_file_passes(run_script, fixtures):
    rc, out = run_script("validate_customers.py", str(fixtures / "customers_clean.csv"))
    assert rc == 0
    assert "PASS" in out
    # bill-to rows + one ship-to continuation row are counted distinctly
    assert "ship-to continuation: 1" in out


def test_default_price_code_zero_fails(run_script, fixtures):
    rc, out = run_script("validate_customers.py", str(fixtures / "customers_bad_pricecode.csv"))
    assert rc == 1
    assert "DefaultPriceCode blocker" in out
    assert "'0'" in out


def test_status_text_price_code_fails(run_script, fixtures):
    _, out = run_script("validate_customers.py", str(fixtures / "customers_bad_pricecode.csv"))
    assert "DefaultPriceCode 'PENDING'" in out


def test_missing_required_column_fails(run_script, write_csv):
    csv = write_csv("BillToCode,BillToName\nC-1,Acme\n", name="customers.csv")
    rc, out = run_script("validate_customers.py", str(csv))
    assert rc == 1
    assert "MISSING REQUIRED COLUMNS" in out


def test_price_levels_membership_enforced(run_script, fixtures):
    # dn is valid; imap is valid -> clean file passes when both are allowed.
    rc, _ = run_script("validate_customers.py", str(fixtures / "customers_clean.csv"),
                       "--price-levels", "dn,imap,ns")
    assert rc == 0
    # Restrict to only 'dn' -> the imap customer now fails membership.
    rc, out = run_script("validate_customers.py", str(fixtures / "customers_clean.csv"),
                         "--price-levels", "dn")
    assert rc == 1
    assert "not in price levels" in out


def test_without_price_levels_warns(run_script, fixtures):
    rc, out = run_script("validate_customers.py", str(fixtures / "customers_clean.csv"))
    assert rc == 0
    assert "WARNINGS" in out
    assert "could not confirm DefaultPriceCode membership" in out


def test_billtocode_length_overflow_fails(run_script, write_csv):
    # "THIS-CODE-IS-WAY-TOO-LONG" is 24 chars, which exceeds the real limit of 20
    # (Customer::ATTR_LENGTHS :code => 20).  Old docs said 15 — that was wrong.
    csv = write_csv(
        "BillToCode,BillToName,BillToAddress1,BillToCity,BillToState,BillToPostCode,DefaultPriceCode\n"
        "THIS-CODE-IS-WAY-TOO-LONG,Acme,1 Main St,Austin,TX,78701,dn\n",
        name="customers.csv",
    )
    rc, out = run_script("validate_customers.py", str(csv))
    assert rc == 1
    assert "BillToCode" in out and ">20" in out


# --- Phase 1 additions ----------------------------------------------------------

HEADER = ("BillToCode,BillToName,BillToAddress1,BillToCity,BillToState,"
          "BillToPostCode,DefaultPriceCode")
ROW = "C-1,Acme,1 Main St,Austin,TX,78701,dn"


def test_bom_is_caught_here_too(run_script, tmp_path):
    path = tmp_path / "customers.csv"
    path.write_bytes(b"\xef\xbb\xbf" + f"{HEADER}\n{ROW}\n".encode("utf-8"))
    rc, out = run_script("validate_customers.py", str(path))
    assert rc == 1
    assert "UTF-8 BOM" in out
    assert "billtocode is missing" in out.lower()


def test_billtocode_between_15_and_20_warns_without_blocking(run_script, write_csv):
    """The importer logs a warning above 15; only the model's 20 rejects the row.

    Reporting the 16-char case as blocking is what the old transcribed table did, and it
    is how an operator learns to ignore the validator.
    """
    csv = write_csv(
        f"{HEADER}\n{'C' * 18},Acme,1 Main St,Austin,TX,78701,dn\n", name="customers.csv")
    rc, out = run_script("validate_customers.py", str(csv))
    assert rc == 0
    assert "18>15" in out
    assert "WARNINGS" in out


def test_terms_over_30_blocks(run_script, write_csv):
    """Pebl: all 171 rows rejected on lengths, and Terms was absent from the old table.

    55 characters against a 30-char field is a structural mismatch needing a client
    decision, not something to truncate.
    """
    terms = "30% T/T Advance, Balance Against Copy of Bill of Lading"
    csv = write_csv(
        f"{HEADER},Terms\n{ROW},\"{terms}\"\n", name="customers.csv")
    rc, out = run_script("validate_customers.py", str(csv))
    assert rc == 1
    assert "Terms 55>30" in out


def test_long_address_blocks(run_script, write_csv):
    """~45 of Pebl's rows failed here, not on a missing required field."""
    csv = write_csv(
        f"{HEADER}\nC-1,Acme,{'x' * 61},Austin,TX,78701,dn\n", name="customers.csv")
    rc, out = run_script("validate_customers.py", str(csv))
    assert rc == 1
    assert "BillToAddress1 61>60" in out


def test_length_findings_cite_the_model_attribute(run_script, write_csv):
    csv = write_csv(
        f"{HEADER}\nC-1,{'x' * 61},1 Main St,Austin,TX,78701,dn\n", name="customers.csv")
    _, out = run_script("validate_customers.py", str(csv))
    assert "Customer::ATTR_LENGTHS[:name]" in out
    assert "supercat_server @" in out


def test_duplicate_billtocode_blocks(run_script, write_csv):
    """BillToCode is unique per org, so the later row is rejected rather than merged."""
    csv = write_csv(f"{HEADER}\n{ROW}\n{ROW}\n", name="customers.csv")
    rc, out = run_script("validate_customers.py", str(csv))
    assert rc == 1
    assert "DUPLICATE BillToCode 'C-1'" in out


def test_a_shipto_continuation_row_is_not_a_duplicate(run_script, write_csv):
    """Ship-to rows repeat the bill-to code by design — that is the file's shape."""
    csv = write_csv(
        f"{HEADER},ShipToAddress1,ShipToCity\n"
        f"{ROW},1 Main St,Austin\n"
        "C-1,,,,,,,2 Side St,Dallas\n",
        name="customers.csv")
    rc, out = run_script("validate_customers.py", str(csv))
    assert rc == 0
    assert "DUPLICATE" not in out


def test_shipto_row_missing_its_address_fails(run_script, write_csv):
    csv = write_csv(
        f"{HEADER},ShipToAddress1,ShipToCity\n"
        f"{ROW},1 Main St,Austin\n"
        "C-1,,,,,,,,\n",
        name="customers.csv")
    rc, out = run_script("validate_customers.py", str(csv))
    assert rc == 1
    assert "ShipToAddress1" in out


def test_dash_placeholder_is_not_a_length(run_script, write_csv):
    """"-" in a ship-to cell means "same as bill-to", not a one-character value."""
    csv = write_csv(
        f"{HEADER},ShipToAddress1,ShipToCity\n{ROW},-,-\n", name="customers.csv")
    rc, _ = run_script("validate_customers.py", str(csv))
    assert rc == 0
