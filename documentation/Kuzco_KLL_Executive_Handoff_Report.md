# Kuzco Lighting (KLL) - Executive Handoff Report

**Date:** February 2, 2026  
**Prepared For:** CS Member Transition  
**Account Status:** 🔴 **RED** - Immediate attention required

---

## Executive Summary

**The Situation:**
Kuzco gave negative feedback about their experience, prompting this CS member change. After analyzing their database, 10 Fathom calls, and 26 Help Scout tickets, the root cause is clear: **they paid $6,990 for a Sales Portal that doesn't work, and territory issues have persisted unresolved for 6+ months.**

**The Good News:**
- Core eCat implementation is excellent (91% complete)
- Strong product adoption: 242 iPad orders, 837 users, 856 total orders
- $31,680 ARR ($2,640/month) - healthy revenue
- Technical foundation is solid

**The Bad News:**
- Sales Portal (their paid add-on) has been broken since "go-live" in January
- **Help Scout Ticket #13878 still PENDING** - users can't access portal (5+ days unresolved)
- Territory configuration issues recurring since July 2025 (never systematically fixed)
- Critical issues surfaced right before Lightovation (their major trade show)
- Admin team not self-sufficient despite being 3+ months post-implementation

**Why They're Unhappy:**
They're paying for a premium feature that doesn't work, issues keep surfacing at critical business moments (trade shows, go-live), and they've had to open 7 support tickets in January alone trying to get things working.

---

## Critical Issues & Evidence

### 1. Sales Portal Not Working (🔴 CRITICAL)

**The Problem:**
- Sold October 2025, $2,250 implementation + $4,740/year
- "Go-live" was January 1, 2026
- **Still doesn't work as of January 26, 2026**

**Evidence:**
- **Database:** 0 territories configured in Sales Portal (required for it to work)
- **Fathom (Jan 30):** Training revealed territory blocker - "Sunburst" territory showing all customers instead of assigned territories
- **Help Scout #13878 (Jan 21-26, PENDING):** Users can't see portal button or their invoices/orders
- **Status:** They paid $6,990 for a feature that's been broken for 1+ month

**Impact:** This is likely the primary driver of negative feedback.

---

### 2. Recurring Territory Data Problems (🔴 SYSTEMIC)

**The Problem:**
Same territory issues keep recurring for 6+ months without systematic resolution.

**Evidence:**
- **Jul 2025 - Ticket #12797:** Territory code mismatch (DALE vs LEGACYSALES)
- **Oct 2025 - Ticket #13339:** Territory assignment help needed
- **Jan 2026 - Ticket #13806:** Territory visibility issues (18 threads to resolve)
- **Jan 2026 - Fathom:** "Sunburst" territory showing all customers
- **Database:** 0 territories configured for Sales Portal

**Pattern:** Band-aid fixes each time, never addressed root cause.

---

### 3. Critical Issues at Critical Times (🟡 TIMING)

**The Problem:**
Issues surface at the worst possible moments for their business.

**Evidence:**
- **Jan 12-19 (Ticket #13821):** Scanning issues right before Lightovation show (16 threads)
- **Dec 9-18 (Ticket #13530):** Sales Portal deleting old invoices/orders during rollout
- **Jan 21+ (Ticket #13878):** Portal access broken, still unresolved

**Impact:** Erodes trust - they can't rely on the system for critical business moments.

---

### 4. Admin Capability Gap (🟡 ONGOING)

**The Problem:**
Kevin Batkiewicz is designated admin but team isn't self-sufficient.

**Evidence:**
- **Fathom (Jan 30):** Kevin needed basic admin training 3 months after go-live
- **Help Scout:** Katy Tipton handles 50% of tickets (13 of 26), Kevin only 12% (3 of 26)
- **Training gaps:** Didn't understand Smart Lists, User Groups, product field config
- **Database:** Kevin has admin flag but Katy doing the work

**Impact:** High support volume, dependency on SuperCat for routine tasks.

---

### 5. Support Volume Spike (🟡 INDICATOR)

**The Pattern:**
- **2024-2025:** 2-4 tickets per quarter (normal)
- **January 2026:** 7 tickets in 3 weeks (spike)
- **Thread counts:** 16-18 threads for complex issues (high effort)

**What This Means:**
Frustration is building. More tickets = more problems surfacing.

---

## Immediate Action Plan

### Week 1 (Next 7 Days)

**Priority 1: Resolve Open Ticket #13878** ⏰ 24 hours
- **Owner:** Chuck Wiebe
- **Action:** Determine why users can't see Sales Portal button/data
- **Validate:** Test with actual user account before marking resolved
- **Communicate:** Update Kevin/Katy with timeline

**Priority 2: Fix Sales Portal Territory Configuration** ⏰ 3-5 days
- **Owner:** Brent/Chuck (engineering support needed)
- **Root cause:** Investigate why 0 territories configured, why "Sunburst" showing all customers
- **Action:** Configure proper territory structure for 75 U.S. reps
- **Test:** Non-production environment first, then validate with Kevin
- **Goal:** Sales Portal actually working for first time

**Priority 3: Fix Pricing Display Bug** ⏰ 2 days
- **Owner:** Chuck (already identified in Ticket #13867)
- **Action:** Remove `price USDN` from "U.S. reps" user group Quick View fields
- **Test:** Validate with Devon Dollar's account
- **Document:** Proper price level configuration for future reference

**Priority 4: Proactive Check-In Call** ⏰ This week
- **Attendees:** New CS member, Kevin Batkiewicz, Katy Tipton (she handles most support)
- **Agenda:**
  1. Acknowledge the issues and apologize for experience
  2. Present clear timeline for Sales Portal fix (with dates)
  3. Ask: "What else isn't working that we don't know about?"
  4. Clarify: Why is Katy handling admin work instead of Kevin?
- **Goal:** Rebuild trust, surface hidden issues

---

### Weeks 2-4 (Next 30 Days)

**1. Comprehensive Admin Training for Kevin** ⏰ Week 2
- **Format:** 2-hour live session + recorded for reference
- **Topics:**
  - Territory management (deep dive - this is their recurring issue)
  - User Groups and permissions structure
  - Smart Lists vs User-Created Lists
  - Product field configuration
  - Sales Portal activation and troubleshooting
- **Goal:** Kevin self-sufficient for 80% of admin tasks

**2. Territory Data Audit & Cleanup** ⏰ Week 2-3
- **Owner:** Brent + Kevin
- **Action:** 
  - Audit all territory codes in customer file vs user assignments
  - Document territory structure (which reps cover which territories)
  - Clean up legacy territory codes (DALE, LEGACYSALES, etc.)
  - Implement proper territory hierarchy
- **Goal:** Eliminate recurring territory issues permanently

**3. Sales Portal Go-Live (For Real This Time)** ⏰ Week 3
- **Prerequisites:** Territories configured, tested, validated
- **Action:**
  - Enable Sales Portal for pilot group (5-10 reps)
  - Monitor for 48 hours
  - Expand to all 75 reps if successful
- **Communication:** Clear rollout plan to Kevin/Katy
- **Goal:** Sales Portal actually working as sold

**4. Proactive Health Check** ⏰ Week 4
- **Format:** 30-min call with Kevin/Katy
- **Agenda:**
  1. Validate Sales Portal working for reps
  2. Review any new issues surfaced
  3. Confirm admin team self-sufficiency
  4. Set expectations for ongoing support cadence
- **Goal:** Confirm issues resolved, relationship stabilized

---

## Key Contacts & Handoff Notes

### Primary Contacts

**Kevin Batkiewicz** - kevin.b@kuzcolighting.com
- **Title:** Director of Showroom Sales
- **Role:** Designated admin (took over from Katie)
- **Context:** 
  - Involved in all 10 Fathom implementation calls
  - Needed basic admin training in Jan 2026 (3 months post-go-live)
  - Only appears in 3 of 26 Help Scout tickets (12%)
  - **Approach:** Patient, educational - he wants to learn but wasn't properly trained
  - **Red flag:** May be overwhelmed with admin role on top of sales director duties

**Katy Tipton** - katy.t@kuzcolighting.com
- **Title:** Trade Sales Support Manager
- **Role:** De facto admin (handles most support)
- **Context:**
  - Appears in 13 of 26 Help Scout tickets (50%)
  - Primary point of contact for day-to-day issues
  - Not officially designated admin but doing the work
  - **Approach:** She's your ally - knows the system, knows the pain points
  - **Question to explore:** Should she be the official admin instead of Kevin?

**Rupinder Kaur** - rupinder.k@kuzcolighting.com
- **Title:** IT/Data contact
- **Context:** Involved in data sync and technical integration
- **Note:** Less frequent contact but critical for technical issues

### Account Context

**Company Profile:**
- **Industry:** Lighting manufacturer
- **Size:** 75 U.S. sales reps, 837 total eCat users
- **Critical Events:** Lightovation trade show (twice yearly) - their make-or-break moments

**What They Value:**
- Reliability during trade shows (scanning, presentations)
- Sales Portal for rep access to invoices/orders
- Territory-based customer visibility for reps

**What Frustrates Them:**
- Issues surfacing at critical times (trade shows, go-live)
- Paying for features that don't work
- Recurring problems that aren't systematically fixed
- Having to open multiple tickets for same underlying issue

### Previous CS Interactions

**Implementation Timeline:**
- **June-Nov 2025:** Core eCat implementation (10 Fathom calls)
- **Oct 2025:** Sales Portal sold ($2,250 + $4,740/year)
- **Jan 1, 2026:** Supposed "go-live" for Sales Portal
- **Jan 30, 2026:** Admin training revealed Sales Portal doesn't work

**Support Pattern:**
- **Primary agents:** Chuck Wiebe (complex issues), Kyla Bosch (L1 support)
- **Ticket velocity:** Spiking (7 tickets in Jan 2026 vs 2-4/quarter previously)
- **Complexity:** High (16-18 thread conversations for L2 issues)

### Conversation Starters for First Call

**Opening:**
> "Hi Kevin and Katy - I'm [Name], taking over as your CS lead. I've done a deep dive on your account, and I want to start by acknowledging that we haven't delivered the experience you deserve. Specifically, the Sales Portal you paid for isn't working, and I'm here to fix that. Here's my plan..."

**Key Points to Hit:**
1. **Acknowledge the issues:** Sales Portal, territory problems, timing of issues
2. **Take ownership:** "This is on us, not you"
3. **Present clear timeline:** "Sales Portal working by [specific date]"
4. **Ask the hard question:** "What else isn't working that we don't know about?"
5. **Set expectations:** "Here's how we'll communicate going forward..."

**Questions to Ask:**
1. "Kevin, you're the designated admin, but Katy, you're handling most support. How should we structure this going forward?"
2. "What's your biggest pain point right now that I haven't mentioned?"
3. "Lightovation is coming up - what do you need to be confident the system will work?"
4. "How often would you like proactive check-ins from me?"

### Red Flags to Monitor

🚩 **If you see these, escalate immediately:**
1. Another critical issue surfaces right before Lightovation
2. Sales Portal still not working after 30 days
3. Kevin/Katy mention considering other solutions
4. Support ticket volume continues increasing
5. They stop responding to outreach (radio silence = danger)

### Success Metrics (90 Days)

**Must-Haves:**
- ✅ Sales Portal working for all 75 reps
- ✅ Zero territory-related support tickets
- ✅ Support ticket volume back to 2-4/quarter baseline
- ✅ Kevin self-sufficient for routine admin tasks

**Nice-to-Haves:**
- 🎯 Kevin/Katy proactively sharing positive feedback
- 🎯 Successful Lightovation with zero issues
- 🎯 Referral or case study opportunity

---

## Bottom Line

**The Real Issue:** Not technical complexity - it's broken promises and unresolved recurring problems.

**The Fix:** Deliver what we sold (working Sales Portal), fix the root cause (territory configuration), and rebuild trust through proactive communication.

**Timeline:** 30 days to stabilize, 90 days to fully recover relationship.

**Risk Level:** 🔴 **HIGH** - They're paying $31,680/year but considering alternatives if we don't fix this fast.

---

**Next Steps:**
1. Schedule handoff call with outgoing CS member
2. Review this document together
3. Schedule first call with Kevin/Katy (this week)
4. Assign owners for Priority 1-3 action items
5. Set 30-day follow-up to review progress

---

*Data Sources: PostgreSQL database, BigQuery MixPanel, 10 Fathom calls (Jun 2025-Jan 2026), 26 Help Scout tickets (Aug 2024-Jan 2026)*
