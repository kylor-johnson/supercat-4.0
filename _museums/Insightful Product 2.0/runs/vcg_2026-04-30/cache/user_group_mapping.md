# User Group Mapping — Visual Comfort Signature (vcg, org_id=141)
- **Source**: Postgres MCP (org_users + users + user_types)
- **Run date**: 2026-04-30
- **Total active (non-disabled) users**: 93

## Group Distribution

| User Group | Count | % of Total |
|-----------|-------|-----------|
| Sales Reps | 69 | 74.2% |
| Admins | 17 | 18.3% |
| Sales Staff | 5 | 5.4% |
| z-SuperCat | 2 | 2.2% |

## Admins (17)

| Username | First Name | Last Name |
|----------|-----------|-----------|
| ragarwal1 | Rahul | Agarwal |
| kbrooker | Kevin | Brooker |
| jduke | Justin | Duke |
| reiermann | Ryan | Eiermann |
| vcit | Visual Comfort | IT Dept |
| mjasinski | Michele | Jasinski |
| jeremy-may | Jeremy | May |
| lemcintosh | Lenora | McIntosh |
| jmcnair1 | Jake | McNair |
| bmiller | Beth | Miller |
| jimmynorris | Jimmy | Norris |
| apfister | Andrew | Pfister |
| apizarro | Allyssa | Pizarro |
| breizner | Becky | Reizner |
| emilianor | Emiliano | Reyes |
| jskeen | Jennifer | Skeen |
| jthrasher | Jimmy | Thrasher (SuperCat) |

## Sales Reps (69)

| Username | First Name | Last Name |
|----------|-----------|-----------|
| dbandtock | Darryll | Bandtock |
| johnbenson | John | Benson |
| kyla | Kyla | Bosch |
| mbutryn | Marzanna | Butryn |
| dcandee | Dawn | Candee |
| JCashion | Julie | Cashion |
| acastaneda | Alfred | Castaneda |
| tcastaneda | Teresa | Castaneda |
| johnchapman | John | Chapman |
| roge95 | Joey | Cloutier |
| jconnolly | John | Connolly |
| gracec | Grace | Cooper |
| randy1 | Randy | Croson |
| fdenegri | Francesa | De Negri |
| nick | Nick | DeGaetano |
| justine | Justin | Elliott |
| erdem | Murat | Erdem |
| jevans1 | Jason | Evans |
| kimevans | Kim | Evans |
| sfowler | Sheldon | Fowler |
| greggf | Gregg | Fraker |
| Gamber | Pete | Gamber |
| lhorry | LESLIE | HORRY |
| sharrison | Stacy | Harrison |
| adamhayes | Adam | Hayes |
| brittneyh | Brittney | Hayes |
| chayes | Catherine | Hayes |
| caseyhelmick | Casey | Helmick |
| ehorry | Eric | Horry |
| simarj | Simar | James |
| lindaj | Linda | Johnson |
| akandil | Ahmed | Kandil |
| jeffk | Jeff | Katsuleas |
| lizzyk | Lizzy | Keenan |
| dlyons | Don | Lyons |
| trevor | Trevor | McBride |
| amckinney1 | Amy | McKinney |
| johnmclaughlin | John | Mclaughlin |
| arienne | Arienne | Mulligan |
| cmunro | Cory | Munro |
| kmunro | Kent | Munro |
| gneal | Gerald | Neal |
| johnnynelis | Johnny | Nelis |
| markobrien | Mark | O'Brien |
| foliveira | Flavia | Oliveira |
| jorange | Jodie | Orange |
| wparada | Wilson | Parada |
| katiep | Katie | Pokorski |
| jpomeroy | Jeff | Pomeroy |
| nrambo | Nikki | Rambo |
| cransom | Crystal | Ransom |
| lvanderbent | Laura | Robertie |
| rrosenthal | Ron | Rosenthal |
| michellescott | Michelle | Scott |
| tsecson | Thomas | Secson |
| gregsmith | Greg | Smith |
| GregSmith2 | Greg | Smith |
| jerardsnell | Jerard | Snell |
| pstanton | Paul | Stanton |
| tedteuten | Ted | Teuten |
| jthrasherna | Jimmy | Thrasher |
| voykim | Kim | Voy |
| lesleyw | Lesley | Weinstein |
| scottweinstein | Scott | Weinstein |
| chuck-user | Chuck | Wiebe |
| nwilliams1 | Nancy | Williams |
| bwoerner | Bryon | Woerner |
| jzanger | Jan | Zanger |
| daly | dina | aly |

## Sales Staff (5)

| Username | First Name | Last Name |
|----------|-----------|-----------|
| thomasbarnes | Thomas | Barnes |
| rbradley | Ryan | Bradley |
| VisualComfort1 | Visual | Comfort1 |
| dannykrauss | Danny | Krauss |
| Mvollmer | Matt | Vollmer |

Note: VisualComfort1 is a shared/showroom account (see showroom_scan_results.md). VisualComfort2-8 are not in the active org_users query (may be disabled).

## z-SuperCat (2)

| Username | First Name | Last Name |
|----------|-----------|-----------|
| mridge | Matt | Ridge |
| swt | Steve | Thrasher |

## Mixpanel Users NOT in Postgres org_users (active)

The following Mixpanel usernames have behavioral data but were NOT found in the active org_users table:
- bob1, daveake, ypovolotskiy, jmetekingi, mgubakin, wendyc
- These may be disabled accounts, former employees, or external demo users.
- Excluded from user_group classification.

## Cross-Reference Notes
- bmiller appears in both Admins (org_users) and orders table — Admin who also submits orders.
- breizner appears in both Admins and orders table — Admin who also submits orders.
- jthrasher (SuperCat) is internal SuperCat staff classified as Admin.
- jthrasherna (Jimmy Thrasher) is a Sales Rep — different from the SuperCat admin.
