#!/usr/bin/env python3
# Writes pg_stacks, pg_imp, pg_ord, pg_cust CSVs from embedded prefetch data.
from __future__ import annotations

from pathlib import Path
import re

import pandas as pd

OUT = Path(r"/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/Health V2/pg_cache")


def split_records(s: str) -> list[str]:
    # Records separated by " | " (pipes inside a record are not surrounded by spaces this way).
    return [x.strip() for x in re.split(r"\s+\|\s+", s.replace("\n", " ").strip()) if x.strip()]


STACKS_RAW = '''tle,1 | ufitest,5 | al,2 | rac,15 | hf,23 | vcg,4 | ta,6 | heb,255 | sbl,6 | ssi,2 | mfl,22 | cc,37 | ki,3 | mfc,46 | rw,8 | mhc,86 | uhc,67 | mli,38 | cfg,10 | khl,13 | sca,16 | bei,5 | scw,5 | hla,28 | jcsa,44 | ml,43 | pcl,29 | gl,10 | hatl,32 | kll,20 | swc,10 | fsf,4 | fc,8 | cci,7 | ih,11 | jcusa,47 | hh,8 | luc,12 | tla,12 | dpl,21 | lpf,26 | big,26 | jgw,22 | shl,12 | bsc,77 | elk,36 | bc,8 | ufi,46 | eli,18 | prog,4 | demo,17 | aa,15 | lss,2 | sccon,4 | hmjc,2 | mah,5 | da,39 | wac,11 | hcan,32 | sic,27 | fcc,18 | dws,8 | ebc,34 | hfg,7 | mlg,9 | wag,22 | mlc,8 | st,2 | gg,21 | ali,17 | art,61 | bp,6 | sarreid,63 | ril,6 | clc,16 | mpc,10 | ol,16 | cf,15 | am,10 | jc,28 | gsa,19 | ihw,7 | bri,19 | bcf,123 | ati,45 | gc,1 | hvl,20 | sgl,25 | etl,5 | eglo,9 | kkc,11 | ap,47 | ah,19 | fms,29 | gh,2 | sc,4 | asi,12 | wwjc,80 | cl,5 | afx,11 | kal,8 | vic,15 | sbmh,4 | vl,4 | df,5 | kii,17 | ttf,8 | dri,4 | clli,38 | cst,14 | pf,28 | mh,14 | et2,22 | tl,7 | el,11 | clm,20 | fal,2 | bmc,37 | vce,7 | dccl,12 | jyc,10 | rf,19'''

IMP_MAIN = '''mh|367|219|0.5967 | gb|293|293|1.0 | scw|1346|1335|0.9918 | pw|183|182|0.9945 | tam|122|113|0.9262 | vic|114|106|0.9298 | asi|1123|1106|0.9849 | gc|103|87|0.8447 | clli|3422|3413|0.9974 | arl|7|7|1.0 | sci|1098|1093|0.9954 | gl|508|463|0.9114 | rac|182|179|0.9835 | uhc|4917|4917|1.0 | bcf|377|360|0.9549 | cf|167|167|1.0 | ihw|874|863|0.9874 | mpc|608|608|1.0 | mali|176|121|0.6875 | bsc|33|19|0.5758 | gcl|59|41|0.6949 | ml|96|96|1.0 | sbmh|84|18|0.2143 | hf|130|40|0.3077 | kll|364|321|0.8819 | el|7169|7155|0.998 | bri|547|453|0.8282 | ih|875|873|0.9977 | hh|160|151|0.9438 | bp|242|118|0.4876 | ssi|180|179|0.9944 | sbl|157|59|0.3758 | sarreid|413|408|0.9879 | jyc|215|104|0.4837 | ufi|361|353|0.9778 | swc|297|297|1.0 | wwjc|1181|1151|0.9746 | eli|258|213|0.8256 | kal|339|249|0.7345 | rf|295|98|0.3322 | sp|122|63|0.5164 | df|65|65|1.0 | sc|1099|1087|0.9891 | tla|567|340|0.5996 | st|324|324|1.0 | fms|642|324|0.5047 | gg|292|283|0.9692 | jc|148|142|0.9595 | ali|223|150|0.6726 | ah|2501|2447|0.9784 | abol|37|37|1.0 | mlg|147|56|0.381 | fal|21|9|0.4286 | eglo_can|371|315|0.8491 | hmjc|148|148|1.0 | wag|65|41|0.6308 | hfg|264|174|0.6591 | et2|18|14|0.7778 | fsf|396|384|0.9697 | art|28|10|0.3571 | ril|126|89|0.7063 | cfg|58|33|0.569 | sca|6|6|1.0 | mah|229|146|0.6376 | etl|218|209|0.9587 | lpf|803|636|0.792 | gsa|235|226|0.9617 | rw|145|141|0.9724 | mli|292|283|0.9692 | vcg|238|130|0.5462 | kii|285|189|0.6632 | afx|31|30|0.9677 | clm|1016|964|0.9488 | gh|1350|1340|0.9926 | da|255|153|0.6 | big|82|79|0.9634 | shl|311|227|0.7299 | lss|701|696|0.9929 | hvusa|13|13|1.0 | pf|483|418|0.8654 | mah|229|146|0.6376 | heb|633|419|0.6619 | vl|314|213|0.6783 | wac|174|161|0.9253 | ihm|9|9|1.0 | mlc|6|6|1.0 | vce|210|201|0.9571 | ta|246|237|0.9634 | dccl|180|124|0.6889 | cci|1296|839|0.6474 | jcusa|158|153|0.9684 | sccon|1293|1285|0.9938 | clc|139|136|0.9784 | fc|912|655|0.7182 | ap|99|74|0.7475 | libco|42|24|0.5714 | eglo|398|179|0.4497 | all|27|27|1.0 | cst|1036|911|0.8793'''

IMP_ZERO = '''leg|0|0| | elk|0|0| | bc|0|0| | cc|0|0| | ebc|0|0| | pcl|0|0| | ki|0|0| | bi|0|0| | ati|0|0| | sic|0|0| | sl|0|0| | bmc|0|0| | bmc3|0|0| | bobo|0|0| | bei|0|0| | hla|0|0| | hatl|0|0| | krb|0|0| | jgw|0|0| | dws|0|0| | mhc|0|0| | khl|0|0| | frh|0|0| | tft|0|0| | hcan|0|0| | lcf|0|0| | dpl|0|0| | sgl|0|0| | kkc|0|0| | acsd|0|0|'''

ORD_MAIN = '''dccl|64|65|62|2|True | jyc|2058|1971|1057|1001|True | rf|15|17|15|0|True | ta|467|539|465|2|True | heb|113|64|113|0|True | sbl|104|16|104|0|True | tam|123|110|123|0|True | vcg|258|145|258|0|True | uhc|908|966|908|0|True | rw|2271|2192|2271|0|True | mli|78|2|78|0|True | cfg|117|124|59|58|True | scw|3510|2129|2636|874|True | fsf|1972|1776|211|1761|True | fc|869|782|551|318|True | cci|1006|878|1006|0|True | ih|782|845|782|0|True | jcusa|40|97|40|0|True | tla|156|25|156|0|True | lpf|443|448|186|257|True | shl|337|60|256|81|True | eli|111|77|107|4|True | sccon|2137|1340|2109|28|True | kl|123|0|123|0|True | mah|200|168|162|38|True | da|1097|952|1097|0|True | wac|971|262|971|0|True | eglo_can|33|2|33|0|True | mlg|124|3|124|0|True | wag|902|776|902|0|True | mlc|73|13|73|0|True | gg|371|155|371|0|True | bp|3|0|3|0|True | sarreid|123|174|123|0|True | ril|329|172|292|37|True | clc|261|2|261|0|True | mpc|1250|1544|1175|75|True | am|21|34|21|0|True | gsa|9|9|9|0|True | ihw|430|393|430|0|True | bri|720|792|57|663|True | bcf|744|547|358|386|True | gc|351|367|235|116|True | kal|83|39|74|9|True | vic|21|20|0|21|True | sbmh|841|746|511|330|True | vl|79|6|79|0|True | kii|676|654|662|14|True | clli|168|9|168|0|True | pf|659|581|659|0|True | mh|65|52|65|0|True | el|131|9|131|0|True | clm|108|20|108|0|True | fal|589|601|589|0|True | vce|18|14|18|0|True | lss|64|2|64|0|True | gh|3726|3097|2443|1283|True | sc|6725|6388|6725|0|True | asi|2058|2340|1209|849|True | wwjc|1799|1559|362|1437|True | afx|60|1|60|0|True | sp|89|58|89|0|True | fms|515|190|515|0|True | ah|267|227|203|64|True | hfg|581|384|581|0|True | rac|147|126|147|0|True | hf|17|54|17|0|True | arl|115|58|115|0|True | prog|71|2|71|0|True | gl|79|46|12|67|True | kll|128|46|72|56|True | sca|87|108|87|0|True | etl|146|150|146|0|True | eglo|41|17|41|0|True | ap|8|6|1|7|True | df|2|2|2|0|True | dals|2|0|2|0|True | st|0|0|0|0|True | gcl|70|58|70|0|True | ml|35|1|35|0|True | blh|2|14|0|2|True | all|12|7|12|0|True | cst|21|0|21|0|True | big|0|6|0|0|True | bsc|2|12|2|0|True | opame|2|12|2|0|True | yw|5|38|5|0|True | swc|0|0|0|0|True | ufi|492|545|492|0|True'''

ORD_EXTRA = '''cc|0|0|0|0|True | ssi|0|0|0|0|True | mfl|0|0|0|0|True | ki|0|0|0|0|True | bi|0|0|0|0|True | khl|0|0|0|0|True | bei|0|0|0|0|True | elk|0|0|0|0|True | bobo|0|0|0|0|True | bc|0|0|0|0|True | bmc3|0|0|0|0|True | pcl|0|0|0|0|True | acsd|0|0|0|0|True | jgw|0|0|0|0|True | tft|0|0|0|0|True | dpl|0|0|0|0|True | art|0|0|0|0|True | ati|0|0|0|0|True | frh|0|0|0|0|True | ebc|0|0|0|0|True | dws|0|0|0|0|True | sgl|0|0|0|0|True | sl|0|0|0|0|True | hatl|0|0|0|0|True | hla|0|0|0|0|True | kkc|0|0|0|0|True | bmc|0|44|0|0|True | hmjc|0|0|0|0|True | pw|0|0|0|0|True | mhc|0|83|0|0|True | sci|0|0|0|0|True | luc|0|0|0|0|True | mfc|0|0|0|0|True | sic|0|0|0|0|True | gb|0|0|0|0|True | dccl|64|65|62|2|True | hcan|0|0|0|0|False | lcf|0|0|0|0|True | krb|0|0|0|0|True | ttf|0|0|0|0|True | wmo|0|0|0|0|True'''

CUST_RAW = '''aa|2302|0|281 | acsd|6263|0|12 | afx|3492|45|0 | ah|3718|208|1280 | ali|2351|0|44 | all|669|7|28 | am|92|5|8 | ap|4752|8|334 | arl|33|36|0 | art|3849|0|495 | asi|1670|584|974 | ati|789|0|204 | bc|433|0|15 | bcf|1984|201|334 | bei|16588|0|1 | bi|30|0|1 | big|301|0|9 | blh|8527|2|1044 | bmc|6775|0|4097 | bp|6956|2|13 | bri|3213|207|181 | bsc|8400|0|1364 | bts|957|0|1 | cc|6368|0|1363 | cci|38605|610|2894 | cfg|2534|55|853 | cl|2272|0|138 | clc|3216|244|0 | clli|5155|126|189 | clm|4693|83|492 | da|1994|163|322 | dals|630|1|7 | dccl|357|29|44 | df|778|1|12 | dpl|2254|0|981 | ebc|1007|0|164 | eglo|1312|27|40 | eglo_can|777|28|36 | el|2006|103|247 | eli|5714|64|1200 | elk|6738|0|536 | etl|595|68|421 | fal|6806|193|354 | fc|3605|518|3818 | fcc|2968|0|286 | fms|5299|273|1363 | frh|2820|0|33 | fsf|760|299|172 | gb|10484|0|1 | gc|1506|208|345 | gcl|158|35|46 | gg|2046|168|1541 | gh|11850|1216|8851 | gl|2343|38|138 | gsa|2046|6|965 | hatl|6304|0|57 | heb|1787|47|2323 | hf|13246|11|128 | hfg|8908|230|1022 | hmjc|1689|0|1 | hvl|2289|0|354 | ih|19837|373|2041 | ihw|6045|186|1302 | jc|34|0|19 | jcsa|2|0|1 | jcusa|4837|17|752 | jyc|9319|846|4649 | kal|2203|48|341 | khl|2744|0|1355 | ki|2589|0|25 | kii|3618|297|1057 | kl|3011|67|251 | kll|2780|90|268 | lcf|1656|0|403 | lpf|1931|210|898 | lss|50|28|0 | mah|876|85|248 | mfc|94|0|25 | mfl|3980|0|1824 | mh|1509|43|356 | mhc|11723|0|5698 | mlc|1211|42|91 | mlg|8453|98|0 | mli|9254|59|20 | mpc|1745|514|2083 | pf|17276|364|4960 | prog|12422|53|0 | rac|552|56|408 | rf|4768|9|351 | ril|4324|124|194 | rw|4881|540|420 | sarreid|4661|70|1745 | sbl|1294|84|58 | sbmh|6461|442|4020 | sc|91452|1596|30836 | sca|2782|23|351 | sccon|5266|418|2201 | scw|8320|868|3867 | sgl|3576|0|182 | shl|1318|241|665 | sl|6939|0|66 | sp|10610|0|0 | ssi|416|0|145 | st|787|0|53 | ta|7146|276|1489 | tam|189|13|0 | uhc|6617|334|762 | vce|1694|11|40 | vcg|5170|151|809 | vic|1491|11|38 | vl|1832|53|173 | wac|9476|710|522 | wag|24122|441|601 | wwjc|13740|1017|8078 | yw|231|5|35 | ufi|14422|235|2585 | dws|6371|0|166 | ebc|1007|0|164 | hla|2766|0|285 | hcan|1223|0|0 | kkc|368|0|4 | luc|877|0|4 | pcl|1773|0|40 | sci|80|0|25 | swc|0|0|0 | sic|6329|0|2 | acsd|6263|0|12 | bobo|23380|0|167 | ati|789|0|204 | bi|30|0|1 | bei|16588|0|1 | bmc3|5782|0|95 | tft|343|0|294 | ffdm|1067|0|72 | jgw|137|0|13 | jbl|1152|0|233 | krb|2208|0|1 | leg|80|0|1 | lna|14|0|1 | ol|13364|0|23 | pbp|767|0|112'''


def load_stacks() -> pd.DataFrame:
    rows: list[dict] = []
    for part in split_records(STACKS_RAW):
        org, cnt = part.rsplit(",", 1)
        rows.append({"org_shortname": org.strip(), "smart_stack_count": int(cnt.strip())})
    return pd.DataFrame(rows)


def parse_imp_record(rec: str) -> tuple[str, int, int, object]:
    parts = rec.split("|")
    org = parts[0].strip()
    total = int(parts[1])
    succ = int(parts[2])
    rate_raw = parts[3].strip() if len(parts) > 3 else ""
    if rate_raw == "":
        rate: object = ""
    else:
        rate = float(rate_raw)
    return org, total, succ, rate


def load_imp() -> pd.DataFrame:
    merged: dict[str, dict] = {}
    for rec in split_records(IMP_MAIN):
        org, total, succ, rate = parse_imp_record(rec)
        merged[org] = {
            "org_shortname": org,
            "total_imports_90d": total,
            "successful_imports_90d": succ,
            "import_success_rate": rate,
        }
    for rec in split_records(IMP_ZERO):
        org, total, succ, rate = parse_imp_record(rec)
        if org not in merged:
            merged[org] = {
                "org_shortname": org,
                "total_imports_90d": total,
                "successful_imports_90d": succ,
                "import_success_rate": rate,
            }
    return pd.DataFrame(list(merged.values()))


def load_ord() -> pd.DataFrame:
    merged: dict[str, dict] = {}

    def add_from(raw: str, skip_existing: bool) -> None:
        for rec in split_records(raw):
            p = rec.split("|")
            org = p[0]
            if skip_existing and org in merged:
                continue
            merged[org] = {
                "org_shortname": org,
                "orders_90d": int(p[1]),
                "orders_prior_90d": int(p[2]),
                "ipad_orders_90d": int(p[3]),
                "online_orders_90d": int(p[4]),
                "orders_exist_any_time": p[5] == "True",
            }

    add_from(ORD_MAIN, skip_existing=False)
    add_from(ORD_EXTRA, skip_existing=True)
    return pd.DataFrame(list(merged.values()))


def load_cust() -> pd.DataFrame:
    rows: list[dict] = []
    seen: set[str] = set()
    for rec in split_records(CUST_RAW):
        p = rec.split("|")
        org = p[0]
        if org in seen:
            continue
        seen.add(org)
        rows.append(
            {
                "org_shortname": org,
                "total_customers": int(p[1]),
                "ordering_customers_90d": int(p[2]),
                "dormant_customers": int(p[3]),
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    load_stacks().to_csv(OUT / "pg_stacks.csv", index=False)
    load_imp().to_csv(OUT / "pg_imp.csv", index=False)
    load_ord().to_csv(OUT / "pg_ord.csv", index=False)
    load_cust().to_csv(OUT / "pg_cust.csv", index=False)


if __name__ == "__main__":
    main()
