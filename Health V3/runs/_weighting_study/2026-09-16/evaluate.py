import pandas as pd, numpy as np, glob, os
S='/private/tmp/claude-501/-Users-kylorjohnson-repos-supercat-4-0/cebc3611-8568-4e17-a5b5-56e3f8ed2ee2/scratchpad/ab'
def load(w):
    fs=[p for p in sorted(glob.glob(f"{S}/{w}/*/client_health_scores_*.csv")) if 'formatted' not in p]
    d=pd.concat([pd.read_csv(p) for p in fs],ignore_index=True); d['run_date']=pd.to_datetime(d['run_date']); return d
E,V=load('equal'),load('v330')
DATES=sorted(E.run_date.unique())

# ---- OUTCOME LABELS as of 2026-09-16 (4 months past last snapshot) --------
CHURN   = {'hmjc','tel'}                       # 0 active subscription plans
DOWNGR  = {'abol','clm','gc','luc','wwjc'}     # >=1 plan canceled, still active
DARK    = {'hmjc','tel','st','hh','krb','ol'}  # logins_90d_now <= 25 (functionally dead)
LOGINS_NOW = {'hmjc':0,'tel':0,'st':2,'hh':12,'krb':20,'ol':22,'ihm':34,'dals':38,'cf':54,'luc':67,
              'jc':89,'swc':113,'mfc':125,'tl':125,'pw':154,'ssi':166,'abol':169,'clm':898,'gc':786,'wwjc':2505}
AT={'Watch','At Risk','Critical'}

def auc(score,y):
    s=pd.Series(score).reset_index(drop=True); y=pd.Series(y).astype(bool).reset_index(drop=True)
    r=s.rank(); n1=y.sum(); n0=(~y).sum()
    return np.nan if n1==0 or n0==0 else (r[y].sum()-n1*(n1+1)/2)/(n1*n0)

print("="*78)
print("TEST 1 — FORWARD SEPARATION: does the score at time T anticipate")
print("         functional death observed 2026-09-16?  (n=6 dead / 104)")
print("="*78)
print(f"{'snapshot':12s} {'lead':>5s} | {'AUC equal':>10s} {'AUC v330':>9s} | {'mean score dead (eq/v330)':>26s} | {'alive':>12s}")
for d in DATES:
    e=E[E.run_date==d].set_index('org_shortname'); v=V[V.run_date==d].set_index('org_shortname')
    yd=e.index.isin(DARK)
    lead=round((pd.Timestamp('2026-09-16')-pd.Timestamp(d)).days/30.4)
    ae,av=1-auc(e.composite_score,yd),1-auc(v.composite_score,yd)
    print(f"{str(d)[:10]:12s} {lead:>4}m | {ae:10.3f} {av:9.3f} | "
          f"{e.composite_score[yd].mean():11.1f} /{v.composite_score[yd].mean():6.1f}   | "
          f"{e.composite_score[~yd].mean():5.1f} /{v.composite_score[~yd].mean():5.1f}")

print()
print("="*78)
print("TEST 2 — CS WORKLIST PRECISION & RECALL (band = Watch/At Risk/Critical)")
print("="*78)
print(f"{'snapshot':12s} | {'equal: n  caught  prec':>24s} | {'v330: n  caught  prec':>24s}")
for d in DATES:
    e=E[E.run_date==d].set_index('org_shortname'); v=V[V.run_date==d].set_index('org_shortname')
    row=[]
    for df in (e,v):
        fl=set(df.index[df.health_band.isin(AT)]); c=len(fl&DARK)
        row.append((len(fl),c,c/len(fl)*100 if fl else 0))
    print(f"{str(d)[:10]:12s} | {row[0][0]:6d} {row[0][1]:7d}  {row[0][2]:5.1f}%  | {row[1][0]:6d} {row[1][1]:7d}  {row[1][2]:5.1f}%")

print()
print("="*78)
print("TEST 3 — PER-ORG: when did each scheme first flag the 6 that died?")
print("="*78)
print(f"{'org':6s} {'logins_90d now':>14s} {'outcome':10s} | {'first flagged (equal)':>22s} | {'first flagged (v330)':>21s}")
for o in sorted(DARK):
    out = 'CHURNED' if o in CHURN else 'dark'
    r=[]
    for df in (E,V):
        g=df[df.org_shortname==o].sort_values('run_date')
        f=g[g.health_band.isin(AT)]
        r.append(str(f.run_date.iloc[0])[:10] if len(f) else 'never')
    print(f"{o:6s} {LOGINS_NOW.get(o,'?'):>14} {out:10s} | {r[0]:>22s} | {r[1]:>21s}")

print()
print("="*78)
print("TEST 4 — FALSE POSITIVES: orgs flagged at 2026-05-13 that are FINE today")
print("="*78)
l=E.run_date.max()
for nm,df in [('equal',E),('v330',V)]:
    g=df[df.run_date==l].set_index('org_shortname')
    fl=g.index[g.health_band.isin(AT)]
    fp=[o for o in fl if o not in DARK and o not in CHURN]
    print(f"  {nm:6s}: {len(fl)} flagged, {len(fp)} still healthy 4 months later "
          f"({len(fp)/len(fl)*100:.0f}% false-positive), ${g.loc[fp,'arr'].sum():,.0f} ARR of wasted CS attention")
print()
gE=E[E.run_date==l].set_index('org_shortname'); gV=V[V.run_date==l].set_index('org_shortname')
only_v = set(gV.index[gV.health_band.isin(AT)])-set(gE.index[gE.health_band.isin(AT)])
print("  Orgs v330 flags that equal does NOT — and their login activity today:")
for o in sorted(only_v):
    print(f"    {o:6s} arr ${gV.loc[o,'arr']:>9,.0f}  bundle {gV.loc[o,'bundle']:<18s} logins_90d_now={LOGINS_NOW.get(o,'healthy (>250)')}")
