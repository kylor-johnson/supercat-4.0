"""Legrand's budgeted per-field escape hatches. 1 of 3 used.

The rule that puts something here (KICKOFF_mapping.md § The escape hatch is
budgeted): if it touches a SINGLE FIELD'S VALUE it is a transform and it is
budgeted. If it decides WHICH ROWS AND FILES EXIST it is a loader and it is not.

Legrand needs no bespoke loaders: the four price books differ only in start row
and column index, which the shared xlsx reader takes as parameters.

Past three transforms, STOP -- that is evidence ecatlib is missing a primitive.
File it against ecatlib and the next client gets it free. Never fork a primitive
into a client's mapping.
"""


def packed_volume_cuft(carton_height, carton_length, carton_width):
    """Carton H x L x W (inches) -> cubic feet, as the importer wants it.

    Not `primitive + dialect + parameters`: it is a cube over three columns with
    a unit divisor and a non-zero floor. If a second client ships carton dims,
    promote it to ecatlib rather than copying it.

    The "0.01" floor is deliberate. PackedVolume of 0 reads to the importer as
    "unknown", and the source's carton tiers are blank on part of the catalogue.
    """
    try:
        h = float((carton_height or '0').replace(' in', '').strip() or '0')
        ln = float((carton_length or '0').replace(' in', '').strip() or '0')
        w = float((carton_width or '0').replace(' in', '').strip() or '0')
        volume = round((h * ln * w) / 1728, 2) if (h and ln and w) else 0
    except (ValueError, TypeError):
        volume = 0
    return str(volume) if volume > 0 else '0.01'
