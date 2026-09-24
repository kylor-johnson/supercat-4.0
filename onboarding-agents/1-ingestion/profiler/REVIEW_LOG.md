# Profiler review log

Bugs found in this tooling, by the data rather than by review. Kept because the
*shape* of each recurs, and because a scorecard that hides its own errors is worth
nothing (SCORECARD §12).

## 2026-09-04 — folder mode

**Rival-versions vs division-variants.** Two files of the same shape whose names differ
by one token (ML / NSL) were classified as rivals, i.e. "choose one". They are one
dataset split by division. Acting on that verdict would have deleted NSL's inventory.
*Rule:* per-division files merge into one file with per-division columns; they never
compete.

**Jaccard where containment was needed.** `ML CUSTOMER LIST REVISED` (421 keys) is a
strict subset of `COMBINED 2.0` (3,517). Jaccard reads 12% and says "complementary —
union them", the opposite of the truth. *Rule:* test containment before Jaccard; a
subset is superseded, not complementary.

**Key overlap computed over non-key columns.** Comparing the top-2 columns by a
uniqueness heuristic matched a quantity column and reported 18% overlap between the two
Legrand inventory files, which actually share **zero** item numbers. *Rule:* only
key-shaped columns may be compared across files, and once the target is known, use that
file type's key semantics instead.

**Extension-based routing.** Decoded XLSX ZIP bytes as mac_roman and returned parsed
garbage instead of an error. *Rule:* route on magic bytes. Confident garbage is worse
than a crash.

**Sheet 1 only.** Read the first worksheet, so a 646-row data sheet behind a 25-row
cover sheet was reported as a 25-row file. *Rule:* profile the most populated sheet and
name the ones not profiled.

## 2026-09-04 — file mode

**Target-blind exact match produced a false certain.** `Name` mapped to `Name` at
confidence *certain* because `name` is a genuine eCat field — in `options.csv`. In the
NetSuite products export that column holds the item code. *Rule:* scope exact-name
matches to the detected target; a field belonging to another eCat file is evidence to
check, not a mapping to trust. **A false certain is worse than an honest moderate.**

**Numeric surrogate preferred over a code-shaped key.** Picked `Internal ID` (6796) over
`Name` (GL9190-S) as the key merely because it came first among unique columns. The
human's own template confirms `Name` is the BaseItemCode. *Rule:* prefer code-shaped
values over numeric ids, show the rivals, and say that only the client can settle it.
