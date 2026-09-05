# Story pack — Bet C Computational IR v1 (after A)

**Date:** 2026-07-24 · **Disposition:** After A · **Type:** New functionality (feature template)  
**Epic:** [EBR-775](https://supercatsolutions.atlassian.net/browse/EBR-775) · **AC:** `INSIGHT-IR-v1-AC.md` · **SQL:** `IR-v1-QUERIES.md`  
**GO required:** `ISOLATION OFF — GO on EBR-775` · **Ship gate:** re-stamp cci + kll · `SHIP-READINESS-bet-c.md`

> EBR-775 Jira summary/description still reads as an **LLM epic**. Before C GO, rewrite description to computational IR v1 and keep EBR-772/776 parked (description edit only — no hygiene comments).

---

## Problem (current)

Owners/reps need computational heroes without Excel. Insightful already computes invoiced truth; Sales Portal does not surface C1 / S1 / team strip as a trusted Intelligence view.

## Appetite

Big batch after Bet A trust lands. Deterministic ledger first — not LLM.

## Solution (elements)

1. **C1 True Topline** — LTM invoiced `net_amount`, RTD-clamped, STRONG  
2. **S1 accounts fading** (EBR-198) — equal 6-vs-prior-6; $-at-risk = account LTM  
3. **Team strip** — Q-R1 pulse always; Q-18 eCat GMV or Q-01 engagement fallback  
4. Provenance stamps on every number  
5. Optional concentration with healthy-diversification degrade  

## Acceptance (when done)

Full AC in `INSIGHT-IR-v1-AC.md` (AC-1…AC-5). Grade on **cci + kll**; demo **sarreid + ufi**.

## Evidence

`IR-v1-QUERIES.md` stamped on sarreid 2026-07-17 (C1 ~$15.98M; S1 25 accounts; team strip). Re-stamp required before build.

## Out of scope / no-gos

EBR-772/776 LLM · named RS-01 rep→revenue as v1 default · margin · FULL completeness · shipping before Bet A filter truth is trustworthy

## SERV

Create after C GO — link to EBR-775 (+ EBR-198 for S1). Not part of Bet A sprint create.
