# Story pack — Bet E Portal & Access hub (shaped; optional Wave 0–1)

**Date:** 2026-07-24 · **Disposition:** Shaped · Wave 0–1 may ride with A (human call) · **Type:** New functionality  
**AC:** `SETTINGS-hub-v1-AC.md` · **Control plane:** `../cycle-02-outputs/PORTAL-SETTINGS-CONTROL-PLANE.md`  
**GO required:** `ISOLATION OFF — GO on Bet E` (or Wave 0) · **Ship gate:** `SHIP-READINESS-bet-e.md`  
**Eng footnote:** SERV-2254 (self-service anchor)

---

## Problem (current)

134 toggles · 6 layers · 39 YAML flags · no admin surface → every portal change is a SuperCat ticket; access rules (`territory_access_via_rep_number`) hide in deploy config.

## Appetite

* **Small:** Wave 0–1 — delete 5 dead flags + graduate named stable flags  
* **Big:** Waves 2–5 — six-section Portal & Access hub  

## Solution (elements)

Enablement tree · Territory & data access · Portal display · Reports & export · Revenue definitions 🔒 · Experiments lab

## Acceptance (when done)

`SETTINGS-hub-v1-AC.md` AC-E0…E6. Wave 4 territory match mode **pairs with Bet A** — never alone.

## Evidence

Control-plane triage of 134 toggles (cycle-02). Demo hub IA in internal demo / `SETTINGS-hub-v1-DEMO-SPEC.md` (layout reference only).

## Out of scope / no-gos

Exposing revenue definitions to clients · deleting 4 dormant-wired flags without ship/cut call · implying hub exists in Rails while only mockup ships · Wave 4 without Bet A path

## SERV

* Wave 0–1: optional small SERV stories if betting table says ride with A  
* Hub Waves 2+: after `GO on Bet E` · link SERV-2254 as footnote  

Not auto-created in Bet A sprint unless Kylor asks.
