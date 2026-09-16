# User Group Mapping — Visual Comfort - Studio /Fans (fms, org_id=108)
- **Run date**: 2026-04-30
- **Total Postgres users (all, including disabled)**: 222
- **Matched to Mixpanel (Q-01 Step 1)**: 128 of 147 (87.1%)
- **Classification confidence**: LOW
- **Split available**: false

## Confidence Gate Evaluation

| Condition | Required | Actual | Pass |
|-----------|----------|--------|------|
| join_rate >= 0.90 | ≥90% | 87.1% | FAIL |
| ambiguous_rate == 0 | 0% | 10.2% (13 users in "other") | FAIL |
| showroom_event_share >= 0.10 | ≥10% | 7.1% | FAIL |

All three conditions fail. §8 will skip the user group split.

## Group Classification

| User Group (Admin Console) | Bucket | User Count |
|---------------------------|--------|------------|
| 1 - Sales Rep - SGL | admin_internal | 11 |
| Dealer - Lighting East DN | other | 3 |
| Dealer - Lighting East UMAP | other | 4 |
| Dealer - Lighting West DN/UMAP | other | 1 |
| Dealer, Lighting, Retail, no orders | other | 1 |
| Dealer-Lighting West Special 2.2 | other | 1 |
| Executive - non-admin | admin_internal | 1 |
| Mobile App User Group | other | 4 |
| OrderXpert Test | admin_internal | 1 |
| Rep - Canada  | field_rep | 10 |
| Rep - Lighting w/ MC | field_rep | 130 |
| Standard Employee User | other | 46 |
| eCat Online (FMS) | admin_internal | 1 |
| z-SuperCat | admin_internal | 8 |

## Per-User Classification (matched to Mixpanel only)

| Username | User Group | Bucket | Total Events |
|----------|-----------|--------|-------------|
| cdq6175 | Rep - Lighting w/ MC | field_rep | 16,308 |
| jaa | Rep - Lighting w/ MC | field_rep | 16,176 |
| johnmclaughlin | Rep - Lighting w/ MC | field_rep | 14,233 |
| neilgraves | Rep - Lighting w/ MC | field_rep | 11,794 |
| emilianor | Standard Employee User | admin_internal | 6,885 |
| lvanderbent | Rep - Lighting w/ MC | field_rep | 6,147 |
| bob1 | Rep - Lighting w/ MC | field_rep | 6,122 |
| sfowler | Rep - Lighting w/ MC | field_rep | 4,905 |
| sknaak | Rep - Lighting w/ MC | field_rep | 4,501 |
| rodney | Rep - Lighting w/ MC | field_rep | 4,353 |
| bmiller | Standard Employee User | admin_internal | 4,308 |
| kdougher | Rep - Lighting w/ MC | field_rep | 4,156 |
| shamrock | Rep - Lighting w/ MC | field_rep | 4,101 |
| conoreyko | Rep - Canada  | field_rep | 3,981 |
| stantonb | Rep - Lighting w/ MC | field_rep | 3,950 |
| johnnynelis | Rep - Lighting w/ MC | field_rep | 3,781 |
| jerardsnell | Rep - Lighting w/ MC | field_rep | 3,732 |
| simarj | Rep - Lighting w/ MC | field_rep | 3,531 |
| greg | Rep - Canada  | field_rep | 3,385 |
| bwoerner | Rep - Lighting w/ MC | field_rep | 3,275 |
| gary | Rep - Lighting w/ MC | field_rep | 2,817 |
| lindsey2018 | Rep - Lighting w/ MC | field_rep | 2,739 |
| cmunro | Rep - Lighting w/ MC | field_rep | 2,650 |
| lizzyk | Rep - Lighting w/ MC | field_rep | 2,590 |
| kamidm | Rep - Lighting w/ MC | field_rep | 2,585 |
| ehorry | Rep - Lighting w/ MC | field_rep | 2,516 |
| scottweinstein | Rep - Lighting w/ MC | field_rep | 2,154 |
| jamiemarie | Rep - Lighting w/ MC | field_rep | 2,104 |
| roge95 | Rep - Lighting w/ MC | field_rep | 1,851 |
| travisw | Rep - Lighting w/ MC | field_rep | 1,848 |
| dcandee | Rep - Lighting w/ MC | field_rep | 1,836 |
| lhorry | Rep - Lighting w/ MC | field_rep | 1,791 |
| amallory | Rep - Lighting w/ MC | field_rep | 1,785 |
| randy1 | Rep - Lighting w/ MC | field_rep | 1,765 |
| breizner | Standard Employee User | admin_internal | 1,663 |
| deanduggar | Rep - Lighting w/ MC | field_rep | 1,587 |
| cduggar | Rep - Lighting w/ MC | field_rep | 1,585 |
| erikam | Rep - Lighting w/ MC | field_rep | 1,311 |
| mwintersteller | Rep - Lighting w/ MC | field_rep | 1,307 |
| fenz61 | Rep - Canada  | field_rep | 1,274 |
| lori | Rep - Lighting w/ MC | field_rep | 1,242 |
| connors | Rep - Lighting w/ MC | field_rep | 1,236 |
| pjcasper | Rep - Lighting w/ MC | field_rep | 1,214 |
| ecommerce | Standard Employee User | other | 1,138 |
| tsecson | Rep - Lighting w/ MC | field_rep | 1,084 |
| charles | Rep - Lighting w/ MC | field_rep | 1,065 |
| hunterm | Rep - Lighting w/ MC | field_rep | 970 |
| brittneyh | Rep - Lighting w/ MC | field_rep | 925 |
| gamber | Standard Employee User | other | 906 |
| graves | Rep - Lighting w/ MC | field_rep | 895 |
| mjasinski | Standard Employee User | admin_internal | 884 |
| adamhayes | Rep - Lighting w/ MC | field_rep | 874 |
| davidkruse | Rep - Lighting w/ MC | field_rep | 824 |
| markf3 | Rep - Lighting w/ MC | field_rep | 803 |
| nick | Rep - Lighting w/ MC | field_rep | 713 |
| mgubakin | Rep - Lighting w/ MC | field_rep | 670 |
| mfowler | Rep - Lighting w/ MC | field_rep | 661 |
| djuneau | Rep - Lighting w/ MC | field_rep | 649 |
| greggf | Rep - Lighting w/ MC | field_rep | 612 |
| acastaneda | Rep - Lighting w/ MC | field_rep | 536 |
| arienne | Rep - Canada  | field_rep | 525 |
| colin | Rep - Canada  | field_rep | 444 |
| jose | Rep - Lighting w/ MC | field_rep | 417 |
| jorange | Rep - Lighting w/ MC | field_rep | 408 |
| johncarter | Rep - Canada  | field_rep | 374 |
| visualcomfort6 | Standard Employee User | other | 352 |
| visualcomfort1 | Standard Employee User | other | 343 |
| johnchapman | Rep - Lighting w/ MC | field_rep | 337 |
| katiep | Rep - Lighting w/ MC | field_rep | 313 |
| chayes | Rep - Lighting w/ MC | field_rep | 301 |
| jpomeroy | Rep - Lighting w/ MC | field_rep | 297 |
| jevans1 | Rep - Lighting w/ MC | field_rep | 297 |
| thomasbarnes | Rep - Lighting w/ MC | field_rep | 265 |
| tedteuten | Rep - Lighting w/ MC | field_rep | 247 |
| danebrock | Rep - Lighting w/ MC | field_rep | 235 |
| karen2018 | Rep - Lighting w/ MC | field_rep | 231 |
| jconnolly | Rep - Lighting w/ MC | field_rep | 203 |
| stan | Rep - Lighting w/ MC | field_rep | 201 |
| visualcomfort5 | Standard Employee User | other | 195 |
| sharrison | Rep - Lighting w/ MC | field_rep | 184 |
| bneal | Rep - Lighting w/ MC | field_rep | 166 |
| benfehr | Standard Employee User | other | 154 |
| lesleyw | Rep - Lighting w/ MC | field_rep | 147 |
| johnbenson | Rep - Lighting w/ MC | field_rep | 140 |
| pstanton | Rep - Lighting w/ MC | field_rep | 140 |
| visualcomfort2 | Standard Employee User | other | 138 |
| jomana | Rep - Lighting w/ MC | field_rep | 128 |
| dlyons | Rep - Lighting w/ MC | field_rep | 128 |
| ptheos | Rep - Lighting w/ MC | field_rep | 127 |
| swt | z-SuperCat | admin_internal | 113 |
| bobweinstein | Rep - Lighting w/ MC | field_rep | 103 |
| stevelinder | Rep - Lighting w/ MC | field_rep | 87 |
| visualcomfort4 | Standard Employee User | other | 70 |
| foliveira | Rep - Lighting w/ MC | field_rep | 60 |
| msakamoto | 1 - Sales Rep - SGL | field_rep | 58 |
| daly | Rep - Lighting w/ MC | field_rep | 57 |
| caroline | Rep - Canada  | field_rep | 54 |
| jchilds1 | Rep - Lighting w/ MC | field_rep | 44 |
| gracec | Rep - Lighting w/ MC | field_rep | 43 |
| justine | Rep - Lighting w/ MC | field_rep | 42 |
| wparada | Rep - Lighting w/ MC | field_rep | 39 |
| tpatrick | Rep - Lighting w/ MC | field_rep | 38 |
| fionaj | Rep - Lighting w/ MC | field_rep | 32 |
| erdem | Rep - Lighting w/ MC | field_rep | 28 |
| cphilhower | Standard Employee User | other | 25 |
| earp727 | Rep - Lighting w/ MC | field_rep | 24 |
| philcook | Rep - Lighting w/ MC | field_rep | 19 |
| nickmansfield | Dealer - Lighting West DN/UMAP | other | 19 |
| jskula | Rep - Lighting w/ MC | field_rep | 19 |
| johnkchilds | Rep - Lighting w/ MC | field_rep | 17 |
| rnugent | Rep - Lighting w/ MC | field_rep | 16 |
| scrosby | Rep - Lighting w/ MC | field_rep | 12 |
| lindaj | Rep - Lighting w/ MC | field_rep | 12 |
| apfister | Standard Employee User | other | 12 |
| mridge | OrderXpert Test | admin_internal | 9 |
| bknaak | Rep - Lighting w/ MC | field_rep | 7 |
| brentsanders | 1 - Sales Rep - SGL | admin_internal | 6 |
| ox | z-SuperCat | admin_internal | 5 |
| coryreed | Rep - Lighting w/ MC | field_rep | 5 |
| kyla | 1 - Sales Rep - SGL | field_rep | 4 |
| lamarquez | Standard Employee User | other | 4 |
| ognezdyonova | 1 - Sales Rep - SGL | admin_internal | 3 |
| lemcintosh | Standard Employee User | other | 3 |
| jthrasherna | z-SuperCat | admin_internal | 3 |
| hillo | Rep - Lighting w/ MC | field_rep | 2 |
| jimmorrison | Rep - Lighting w/ MC | field_rep | 2 |
| gregsmith2 | Rep - Lighting w/ MC | field_rep | 2 |
| ypovolotskiy | Rep - Lighting w/ MC | field_rep | 1 |

## Aggregate Split

| Bucket | Users | Total Events | Event Share |
|--------|-------|-------------|-------------|
| field_rep | 105 | 178,581 | 91.2% |
| admin_internal | 10 | 13,879 | 7.1% |
| other | 13 | 3,359 | 1.7% |