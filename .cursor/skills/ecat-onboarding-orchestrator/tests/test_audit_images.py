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
