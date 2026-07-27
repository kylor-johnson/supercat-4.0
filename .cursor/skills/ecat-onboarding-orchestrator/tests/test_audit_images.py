"""Regression tests for audit_images.py.

Covers the image traps from LESSONS_LEARNED.md: missing files, sub-500-byte error
pages, the per-product image limit (6 default / 12 with the paid flag), and the
oversized-hero heuristic (warns, does not fail).
"""


def test_all_present_passes(run_script, make_image_dir, write_csv):
    img_dir, add = make_image_dir
    add("A-1.jpg", 1500)
    csv = write_csv("BaseItemCode,ImageFileName\nA-1,A-1.jpg\n")
    rc, out = run_script("audit_images.py", str(csv), str(img_dir))
    assert rc == 0
    assert "PASS" in out


def test_missing_file_fails(run_script, make_image_dir, write_csv):
    img_dir, add = make_image_dir
    add("A-1.jpg", 1500)
    csv = write_csv("BaseItemCode,ImageFileName\nA-1,A-1.jpg\nB-1,does-not-exist.jpg\n")
    rc, out = run_script("audit_images.py", str(csv), str(img_dir))
    assert rc == 1
    assert "MISSING" in out


def test_sub_500_byte_file_is_corrupt(run_script, make_image_dir, write_csv):
    img_dir, add = make_image_dir
    add("TINY.jpg", 120)  # 404 error pages are typically < 500 bytes
    csv = write_csv("BaseItemCode,ImageFileName\nT-1,TINY.jpg\n")
    rc, out = run_script("audit_images.py", str(csv), str(img_dir))
    assert rc == 1
    assert "CORRUPT" in out


def test_over_default_limit_fails(run_script, make_image_dir, write_csv):
    img_dir, add = make_image_dir
    names = [add(f"P-{i}.jpg", 1500) for i in range(1, 8)]  # 7 images
    csv = write_csv(f"BaseItemCode,ImageFileName\nP-1,\"{','.join(names)}\"\n")
    rc, out = run_script("audit_images.py", str(csv), str(img_dir))
    assert rc == 1
    assert "> limit 6" in out


def test_twelve_image_flag_allows_seven(run_script, make_image_dir, write_csv):
    img_dir, add = make_image_dir
    names = [add(f"P-{i}.jpg", 1500) for i in range(1, 8)]  # 7 images
    csv = write_csv(f"BaseItemCode,ImageFileName\nP-1,\"{','.join(names)}\"\n")
    rc, out = run_script("audit_images.py", str(csv), str(img_dir), "--max", "12")
    assert rc == 0
    assert "PASS" in out


def test_oversized_hero_warns_but_passes(run_script, make_image_dir, write_csv):
    img_dir, add = make_image_dir
    add("H-1.jpg", 200_000)  # hero >4x next image => likely a lifestyle/scene shot
    add("H-2.jpg", 2_000)
    csv = write_csv("BaseItemCode,ImageFileName\nH-1,\"H-1.jpg,H-2.jpg\"\n")
    rc, out = run_script("audit_images.py", str(csv), str(img_dir))
    assert rc == 0  # heuristic warns, does not hard-fail
    assert "HERO WARNINGS" in out


# --- Phase 1 additions ----------------------------------------------------------
# Local disk is the narrowest of the three delivery paths. These cover the other two,
# plus the client rule that a blank image cell is a decision rather than a gap.


def test_a_url_is_not_looked_for_on_disk(run_script, make_image_dir, write_csv):
    """ImageFileName accepts a full HTTPS URL that eCat fetches itself.

    Before this, a URL was reported as a MISSING local file — which is both wrong and
    the reason the URL delivery path went unnoticed for five weeks.
    """
    img_dir, _add = make_image_dir
    csv = write_csv(
        "BaseItemCode,ImageFileName\nA-1,https://cdn.example.com/a-1.jpg\n")
    rc, out = run_script("audit_images.py", str(csv), str(img_dir))
    assert rc == 0
    assert "MISSING" not in out
    assert "URL-delivered references: 1" in out


def test_png_url_fails(run_script, make_image_dir, write_csv):
    """23 of these were live for eight weeks. PNG fails both CdnImageSync gates."""
    img_dir, _add = make_image_dir
    csv = write_csv(
        "BaseItemCode,ImageFileName\nCO18G,https://cdn.example.com/co18g.png\n")
    rc, out = run_script("audit_images.py", str(csv), str(img_dir))
    assert rc == 1
    assert "[png]" in out
    assert "suppresses every delete in the same import" in out


def test_drive_share_link_fails(run_script, make_image_dir, write_csv):
    img_dir, _add = make_image_dir
    csv = write_csv(
        "BaseItemCode,ImageFileName\n"
        "A-1,https://drive.google.com/file/d/abc/view\n")
    rc, out = run_script("audit_images.py", str(csv), str(img_dir))
    assert rc == 1
    assert "[share-link]" in out


def test_png_local_filename_is_rejected(run_script, make_image_dir, write_csv):
    img_dir, add = make_image_dir
    add("A-1.png", 1500)
    csv = write_csv("BaseItemCode,ImageFileName\nA-1,A-1.png\n")
    rc, out = run_script("audit_images.py", str(csv), str(img_dir))
    assert rc == 1
    assert "INVALID FILENAME" in out
    assert "CdnImageSync skips it" in out


def test_parentheses_in_a_filename_are_rejected(run_script, make_image_dir, write_csv):
    """Product::VALID_IMAGE_REGEX forbids them, and "chair (2).jpg" is a common export."""
    img_dir, add = make_image_dir
    add("chair (2).jpg", 1500)
    csv = write_csv("BaseItemCode,ImageFileName\nA-1,chair (2).jpg\n")
    rc, out = run_script("audit_images.py", str(csv), str(img_dir))
    assert rc == 1
    assert "forbidden character" in out


def test_missing_primary_against_the_live_set_fails(run_script, make_image_dir,
                                                   write_csv, tmp_path):
    """Lib & Co's portal outage: the file is fine on disk and absent from the org."""
    img_dir, add = make_image_dir
    add("lc-1.jpg", 1500)
    live = tmp_path / "uploaded.txt"
    live.write_text("# filenames from product_images\nsomething-else.jpg\n",
                    encoding="utf-8")
    csv = write_csv("BaseItemCode,ImageFileName,Hideable\nLC-1,lc-1.jpg,N\n")
    rc, out = run_script("audit_images.py", str(csv), str(img_dir),
                         "--live-images", str(live))
    assert rc == 1
    assert "image_exists=false" in out
    assert "eOL will suppress it from search" in out


def test_uploaded_alternate_does_not_satisfy_the_primary(run_script, make_image_dir,
                                                        write_csv, tmp_path):
    img_dir, add = make_image_dir
    add("lc-1.jpg", 1500)
    add("lc-1-alt.jpg", 1500)
    live = tmp_path / "uploaded.txt"
    live.write_text("lc-1-alt.jpg\n", encoding="utf-8")
    csv = write_csv(
        "BaseItemCode,ImageFileName\nLC-1,\"lc-1.jpg,lc-1-alt.jpg\"\n")
    rc, out = run_script("audit_images.py", str(csv), str(img_dir),
                         "--live-images", str(live))
    assert rc == 1
    assert "only the first filename counts" in out


def test_live_set_matching_passes(run_script, make_image_dir, write_csv, tmp_path):
    img_dir, add = make_image_dir
    add("lc-1.jpg", 1500)
    live = tmp_path / "uploaded.txt"
    live.write_text("lc-1.jpg, spare.jpg\n", encoding="utf-8")
    csv = write_csv("BaseItemCode,ImageFileName\nLC-1,lc-1.jpg\n")
    rc, out = run_script("audit_images.py", str(csv), str(img_dir),
                         "--live-images", str(live))
    assert rc == 0
    assert "1/1 products have their PRIMARY image uploaded" in out


def test_borrowing_a_sibling_image_fails_against_the_source(run_script, make_image_dir,
                                                           write_csv, tmp_path):
    """The client's standing rule: leave it blank rather than assume a similar SKU's image."""
    img_dir, add = make_image_dir
    add("a-1.jpg", 1500)
    source = tmp_path / "client_export.csv"
    source.write_text("BaseItemCode,ImageFileName\nA-1,a-1.jpg\nA-2,\n",
                      encoding="utf-8")
    csv = write_csv("BaseItemCode,ImageFileName\nA-1,a-1.jpg\nA-2,a-1.jpg\n")
    rc, out = run_script("audit_images.py", str(csv), str(img_dir),
                         "--source", str(source))
    assert rc == 1
    assert "blank at source" in out


def test_matching_the_source_passes(run_script, make_image_dir, write_csv, tmp_path):
    img_dir, add = make_image_dir
    add("a-1.jpg", 1500)
    source = tmp_path / "client_export.csv"
    source.write_text("BaseItemCode,ImageFileName\nA-1,a-1.jpg\nA-2,\n",
                      encoding="utf-8")
    csv = write_csv("BaseItemCode,ImageFileName\nA-1,a-1.jpg\nA-2,\n")
    rc, _ = run_script("audit_images.py", str(csv), str(img_dir),
                       "--source", str(source))
    assert rc == 0


def test_bom_is_caught_here_too(run_script, make_image_dir, tmp_path):
    img_dir, add = make_image_dir
    add("A-1.jpg", 1500)
    path = tmp_path / "products.csv"
    path.write_bytes(b"\xef\xbb\xbfBaseItemCode,ImageFileName\nA-1,A-1.jpg\n")
    rc, out = run_script("audit_images.py", str(path), str(img_dir))
    assert rc == 1
    assert "UTF-8 BOM" in out


def test_no_image_column_is_an_error_not_a_pass(run_script, make_image_dir, write_csv):
    img_dir, _add = make_image_dir
    csv = write_csv("BaseItemCode,LongDesc\nA-1,Chair\n")
    rc, out = run_script("audit_images.py", str(csv), str(img_dir))
    assert rc == 2
    assert "no ImageFileName column" in out
