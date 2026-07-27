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
    csv = write_csv(
        "BillToCode,BillToName,BillToAddress1,BillToCity,BillToState,BillToPostCode,DefaultPriceCode\n"
        "THIS-CODE-IS-WAY-TOO-LONG,Acme,1 Main St,Austin,TX,78701,dn\n",
        name="customers.csv",
    )
    rc, out = run_script("validate_customers.py", str(csv))
    assert rc == 1
    assert "BillToCode" in out and ">15" in out
