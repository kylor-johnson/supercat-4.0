# drf — what doesn't add up

Computed BLIND from `Source Data/` alone, before opening any build artifact.
This is the deliverable for this client. It is not a column-mapping report,
because the column mapping is not the problem.

---

## The reconciliation

```
product source          1 file, 11.7 KB
patterns                72   (73 data rows, minus one client label row)
distinct BaseItemCodes  72
image references         0   of 72   ImageFileName empty on every row
image files on disk      0            no image directory exists in the client tree
price values             0   of 72   NetPrice empty on every row
colourway rows           0            no column in any source file carries one
```

**A fabric catalogue is pattern × colourway. This source is the pattern axis
only.** There is no second axis anywhere in `Source Data/`, and there are no
images and no prices.

## The three questions this raises, before any build starts

**1. Where do the orderable SKUs come from?** 72 patterns cannot be a catalogue
a rep sells from. Each pattern ships in many colourways and the colourway is
what gets ordered. No file here lists them. Until someone says where that list
lives, the size of the finished catalogue is unknown — and *"how many products
are we building"* is not a question to discover halfway through.

**2. Where do prices come from?** `NetPrice` is empty on all 72 and there is no
price file. The programme's own notes say drf's pricing lives in `stories.csv`,
which is an unusual arrangement and a decision, not a default. It needs
confirming, not assuming.

**3. Where do images come from?** `ImageFileName` is empty on all 72 and the
client tree contains **zero** image files. For a fabric catalogue — where the
image *is* the product — this is not a gap to fill later.

## Findings inside the 72 rows

Real, and worth reporting even though they are the smaller half.

| finding | measurement | why it matters |
|---|---|---|
| `LongDesc` is a classification | **3 distinct values across 72 rows** (`WOVEN`, `KNIT`, `ULTRA-BLEACH CLEANABLE+MIN. 400HRS COLORFASTNESS`). The client's own label for the column is "Product Class". | 72 products share 3 names in a rep's list view |
| `NewItem` is not boolean | `NEW ITEM` / `ACTIVE`, 72/72 | eCat's `NewItem` is Y/N. Same family as libco A19 |
| the taxonomy never reached the taxonomy columns | `CollectionCodes` and `CategoryCodes` **1 of 72** populated, while the client-domain `Collection` column ("Product Sub-class": CHENILLE, FLAT, HIGH PILE FUR, JACQUARD …) is **72/72 with 7 values** | auto-create would build the collection list from one row |
| `MinimumQuantity` vs `Minimum` | `MinimumQuantity` empty; client `Minimum` is 72/72 (`330 YDS`, `1,100 YDS`) | a yardage minimum is not an integer order minimum. **Not joined** — that is a client question, not a derivation |
| 9 client-domain columns need registering | `Origin` `Content` `Minimum` `CleaningCode` `Direction` `Abrasion` `Backing` `Finishing` `Collection`, all 72/72 | these are what a fabric rep filters on; unregistered = discarded silently on every import |
| two-header-row file | row 2 is the client's labels | third client in a row; reading it naively imports a product called `Product` |

## The prediction this run was set up to test

`BLIND_BOUNDARY.md`, written before any file was opened:

> The product source will not contain enough rows to explain the built
> catalogue, and that discrepancy — not any column mapping — will be the
> finding.

**It held.** The profiler's "what doesn't add up" check is the one that earns
its keep here, and it earns it by refusing to produce a catalogue rather than by
producing a wrong one.

## What this mapping therefore does

Produces **72 rows** — exactly what the source supports — and stops. It does not
invent colourways, does not derive an image filename from an item code, and does
not fill `NetPrice`.

That is the entire lesson from the two weeks lost here: *the data question was
never actually settled before the build started.* A mapping layer's most
valuable output on this client is a short list of questions and a refusal to
guess, delivered on day one instead of after an import runs clean.
