# tcs Phase 2b — predictions, committed before any answer key was opened

Written after `mappings/tcs/options.toml` was on disk and had produced output,
and before `CS_eCat_Rebuild/options.csv` or `option_groups.csv` was read.
Boundary: `BLIND_BOUNDARY_2b.md`.

## What the mapping produced

```
options.csv              354 rows   (distinct option codes)
option_groups.csv        320 rows
option_assignments.csv   379 rows   = 283 Master + 96 Weiyan, the whole lantern set
```

Groups per axis, and this is the shape of the prediction:

```
FIN Finish               2      MNT Mount               142
GAS Gas Accessories      7      SCR Scroll & Moustache   77
SHD Shades & Glass       1      PST Post & Pier          38
FEA Feature              3      ORN Ornament & Top       50
```

Integrity: **1,890 of 1,890** group-membership references and **1,936 of 1,936**
OptionSet references resolve. 0 dangling. That is the A4 condition `mali` fails,
checked on the output before anyone proposes an upload.

## The four predictions, ranked by how likely I am to be wrong

**P1 — the reading is `per_product`, and I expect this to be RIGHT.**
The test was in the data and it is not a matter of taste: `Gas Pressure
Regulator` is `GPR` on all 125 populated rows (constant), `Post Fitter` is
PF1/PF2/PF3/PF4/PF5/PFPAU/PFG15 (varies). A varying cell can only mean *this
product's post fitter is PF3*. A `per_column` reading would show a product all
five post fitters.

**P2 — the option CODES are right, the group codes are not.**
Codes come straight out of the cells (`BLK`, `GH1`, `WY`), so `options.Code`
should match well. Group codes are mine (`MNT47`); a human invented something
else. **I expect `option_groups.Code` near 0% byte-exact even where the
membership is exactly right**, which is why membership is scored separately from
code spelling below.

**P3 — the axis partition is where I lose points.** Eight axes read off column
names alone. The count agreeing with `OptionSet1-8` is encouraging and is not
proof. Most exposed: `SHD` (are the three Hurricane Shades a shade type, or gas
accessories? the navigation contract files `HSI, CHSI` under *Electric*
Accessories, which contradicts both) and `FEA` (four flag-ish columns that may
not be options at all).

**P4 — `Weiyan` should probably not be an option.** It carries the literal `Yes`
on 96 rows. Under "the cell is the code" that emits an option coded `Yes`, which
is legal, imports clean, and is almost certainly wrong. **Shipped deliberately
unfixed**: special-casing it in the engine is how tcs's layout gets baked into
the format. If the key excludes it, the fix belongs in the mapping (drop the
column from the axis), not in the code.

## Source-quality findings, from the source alone, before unblinding

**F1 — five option codes carry two different names.** The same code is emitted
once, with the first name seen; the second name is discarded. Counted (37
occurrences), never silent:

| code | names | axes |
|---|---|---|
| `LR` | Ladder Rests · Post Ladder Rest | **MNT and PST — spans two types** |
| `HSCM` | Heavy Chain Mount · Heavy Slope Ceiling Mount | MNT |
| `PFPAU` | Post Fitter · Biltmore® Post Fitter | PST |
| `BMDSM2` | Dual Scroll Moustache · Biltmore® Moustache | SCR |
| `BS4` | Bottom Scroll · Bottom Scroll Wide | SCR |

`options.csv` is keyed on Code globally, so one code is one option with one
name. `LR` is the one that matters: it is a mount on some products and a post
accessory on others, and no import would object.

**F2 — `----` is a null token and appears 768 times** (480 on SHD, 288 on FEA).
Read as a code it would put six wrongly-named options into the file under a
single code `----`. Declared, counted per axis.

**F3 — four declared columns are empty on both sheets** (`Pier Mount` the first
of the two, `Single 12-V Base`, and two Replacement Glass columns in Master).
They are declared anyway so the file states the whole 72-column block.

**F4 — the two repeated headers are both load-bearing.** `Turtle Friendly #2`
(index 96) is populated on 169 Master rows and is an OPTION; `Turtle Friendly`
(index 47) is a Y/N product attribute. Same name, two files. A dict reader keeps
one and drops the other silently.

## Scoring plan

Three scores, because they answer different questions:

1. `options.csv` — Code as key. Byte-exact / semantic / differ / not produced.
2. `option_groups.csv` — **twice**: once keyed on Code (which will score badly
   and should), and once on MEMBERSHIP SETS, ignoring code spelling: for each
   reference group, is there a produced group with the identical option set?
   That is the question "did I get the grouping right", and code spelling is a
   separate question.
3. `option_assignments.csv` vs the build's products.csv `OptionSet1-8`, by
   membership again.

Every one states `evaluated N of M candidates` (BUILD_SPEC §3.4).
