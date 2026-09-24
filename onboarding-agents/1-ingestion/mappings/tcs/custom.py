"""The CopperSmith's budgeted per-field escape hatches. 2 of 3 used."""


def image_filename(main_image_file_name):
    """`16WST` -> `16WST.jpg`.

    The source carries the image name with NO EXTENSION on all 283 lantern rows.
    An `ImageFileName` without an extension matches no file on FTP, and the
    import runs clean either way -- pebl shipped 18 days of `.jpg.jpg` that
    could never match, which is the same failure with the opposite typo.

    `.jpg` is an ASSUMPTION. Nothing in the source states the extension and the
    accessory sheets use S3 URLs instead. Flagged in VALIDATION.md, not settled.
    """
    v = (main_image_file_name or '').strip()
    if not v or v in ('----', '#', 'N/A'):
        return ''
    return v if '.' in v.rsplit('/', 1)[-1] else '%s.jpg' % v


def taxonomy_category(kind, fixture_subtype, accessory_category):
    """Category per the CLIENT'S OWN navigation file, not per the data.

    Class 3: the template is the contract. `eCat Navigation and Filtering` puts
    lanterns under Product Type > Outdoor Lighting > {Gas Lanterns, Electric
    Lanterns, Flush Mount, LED Fixtures, RLM Lighting, Sconces, Wildlife
    Friendly} -- which is exactly the value set of `Fixture Sub-Type`, so that
    column IS the category leaf.

    Accessories and parts take the other branch. The navigation file qualifies
    it: "Accessories (only items that aren't lantern configurations)" -- the
    distinction that makes a lantern buildable and an accessory not.
    """
    if kind == 'lantern':
        return (fixture_subtype or '').strip()
    cat = (accessory_category or '').strip()
    if not cat:
        return 'Accessories'
    return cat.title() if cat.isupper() else cat
