# Story pack — Bet B List tabs (rides with A)

**Date:** 2026-07-24 · **Disposition:** Rides with Bet A · **Type:** Shell / UX (not bug-primary)  
**AC:** `LIST-TABS-AC.md` · **Contract:** `DEMO-SURFACE-CONTRACT.md`  
**GO:** No separate GO — ships as proof shell under `ISOLATION OFF — GO on EBR-40` if eng pulls it in

---

## Problem (current)

List surfaces bury the answer in the grid. Bet A makes the filtered total trustworthy; Bet B makes that total the first thing on Invoices / Customers / Orders / Reports.

## Acceptance (when done)

Cite `LIST-TABS-AC.md`:

* LT-INV — Invoices hero = invoiced total for current filters; territory + date recompute hero and rows  
* LT-CUST — Selected-range sales hero; export matches (ties A2)  
* LT-ORD — Confirmed $ vs Quotes $ demoted (ties parked EBR-87 copy)  
* LT-RPT — Invoiced net = C1 spine label  

## Evidence

Internal demo + pitch mocks already show answer-first list heroes. Production = AC, not HTML chrome.

## Out of scope

Dashboard redesign as Bet A proof · What’s-broken as shipping nav · Bet F persona fork · Intelligence heroes (Bet C)

## SERV

Optional — fold into EBR-40/91 SERV descriptions as “proof shell” rather than separate stories unless eng asks.
