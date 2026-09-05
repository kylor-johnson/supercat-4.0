---
name: hpmkt-follow-up-email
description: Draft High Point Market follow-up emails from raw meeting transcripts for SuperCat clients. Use when the user provides HPMKT, High Point Market, market meeting, Otter, or transcript notes and wants a polished Kjael-style client follow-up plus internal action register and assumptions.
---

# HPMKT Follow-Up Email

## Purpose

Transform raw High Point Market meeting transcripts into client-facing follow-up emails that are clear, commercially useful, and easy for busy customers to digest.

The goal is not to summarize the meeting. The goal is to convert the conversation into a client-facing path forward.

Each output must include:

1. Client-facing email
2. Internal action register
3. Assumptions / placeholders

## SuperCat Context

- **eCat iPad**: Rep-facing mobile app for product browsing, presentations, and order writing. Core module; every client has this.
- **eCat Online**: Web-based catalog for customers/dealers. Can be closed browse-only or open with Cart.
- **Cart**: Enables online order writing via eCat Online. Separate from iPad orders.
- **Sales Portal**: Brings ERP data into SuperCat for business intelligence. Without it, SuperCat only sees eCat-originated transactions.
- **Insightful Product**: Analytics/intelligence report built on flowing data. Only useful when meaningful data is flowing through the system.
- **Presentations**: Curated product presentations reps show customers on iPad.
- **Smart Lists**: Curated product lists for targeting, new introductions, and seasonal pushes.

Tier shorthand:

- **iPad-only** = limited to rep-submitted orders
- **Full tier** = iPad + eCat Online + Cart + Sales Portal

Internal team:

- **Kjael**: CEO. Writes these emails. Leads strategy and client conversations.
- **Kylor**: CS. Data configuration, Sales Portal setup, client-facing support.
- **Brent**: Engineering. Integrations, bugs, technical scoping.
- **Emery**: Training and enablement. Monthly workshop program.

Write as Kjael. Use **we** for SuperCat actions; do not write "SuperCat will" or "our team will."

## Core Writing Principle

Organize around client-facing workstreams, not internal categories. The customer should see practical business topics, such as:

- ERP order export
- Data visibility
- Option dependencies / configuration rules
- Rep activity capture
- Quote visibility
- Customer scorecards
- Admin workflow improvements
- Market attribution
- Rep group visibility
- Showroom ROI

Do not make the email feel like an internal ticketing report.

## Internal Follow-Up Taxonomy

Use this urgency order when analyzing the transcript:

| Priority | Category | Meaning |
|---|---|---|
| 1 | Support Ticket | Specific, immediate, trackable issue |
| 2 | Support Project | Grouped issues, implementation work, scoping, multi-step follow-through |
| 3 | Training | Admin or user education; include in email only if clearly a major client-raised issue |
| 4 | Bug | Product behavior that appears incorrect |
| 5 | Feature Request | New functionality to be scoped and prioritized |
| 6 | Design Partner | Customer input needed to shape emerging product areas |

Do not force every category into every email. Only include what is relevant.

Training note: do not default to mentioning rep training, workshops, or enablement programs unless the transcript makes clear this was a significant topic the client raised or asked for. If it is minor, put it in the internal action register only.

## Client-Facing Email Format

Use this order exactly:

```markdown
**To:** [Names]

**Subject:** High Point follow-up — [Company] [business/workflow path]

Hi [Primary Contact],

Great meeting with you [and names] at High Point. **The clearest takeaway was [sharp business-level insight].**

For [Company], the opportunity is not simply to [surface issue], but to [larger business outcome]. Today, [current friction] is creating [business consequence].

From here, we're organizing the follow-up around the workstreams below.

---

### **Support Status / Immediate Support Items**

[If support items exist:]
A few items need immediate attention - see below signature for more detail:

- **[Issue]** — [Plain-English explanation and what we're doing about it.]

[If no support items exist:]
Nothing from the meeting appeared to be a critical break/fix issue. The larger opportunity is structural: [summarize].

---

### **Recommended Next Steps**

From here, we will establish a support project to resolve the pressing items; [CS owner] (cc'd) will lead from our side:

- [Specific action we own.]
- [Specific action we own.]
- [Specific action we own.]

From there, I'll be in touch to regroup on the following:

- [Strategic/product/design partner follow-up.]

If we get this right, [Company] should be able to [business outcome], instead of [current manual/friction-heavy process].

Best,

Kjael

### **[Detailed Workstream 1]**

[What we heard. Why it matters. What we will do next.]

---

### **[Detailed Workstream 2]**

[What we heard. Why it matters. What we will do next.]
```

Important structure update:

- The sendable executive email lives above the signature.
- Detailed workstream notes live below the signature as supporting detail.
- Put immediate support items before Recommended Next Steps.
- Do not place 2-4 long workstream sections before the signature unless the user asks for the older long-form structure.
- In Recommended Next Steps, group urgent implementation/configuration items into a **support project** when there are multiple related support items.
- Use the likely CS owner when clear from context; otherwise use `[CS owner]` or `[Name]` as a placeholder. Do not invent owners.

## Insightful Product Section

Include a detailed **Insightful Product Report** section below the signature only if:

- We presented the report and the client engaged meaningfully with it, or
- The client expressed interest in being a design partner for intelligence/analytics.

Do not include it if:

- We did not show it to them.
- It was mentioned in passing but was not a focus.
- Data limitations made it non-actionable and the conversation moved on.

When included, ground it in what they reacted to and what we want from them next.

## Subject Line Rules

Use:

`High Point follow-up — [Company] [business/workflow path]`

Examples:

- `High Point follow-up — Charleston Forge path forward`
- `High Point follow-up — Fine Art's CRM and reporting path`
- `High Point follow-up — Interlude quote visibility and two-brand workflow`
- `High Point follow-up — Hubbardton Forge scorecards and customer intelligence`
- `High Point follow-up — Renwill rep visibility, market attribution, and intelligence path`

## Tone and Style

Written as Kjael: direct, thoughtful, commercially sharp, practical.

Use:

- "The clearest takeaway..."
- "The larger opportunity..."
- "The first step..."
- "This is a real workflow gap."
- "That is exactly the kind of manual work we should be helping remove."
- "We need to separate what can be solved quickly from what requires deeper scoping."
- "If we get this right..."

Avoid:

- Generic "thank you for your feedback" language
- Chronological meeting recap
- Software jargon
- Overly long meeting summary
- Treating all items as equally important
- "We'll circle back"
- "We're excited to partner"
- "Enhance the user experience"
- "Leverage synergies"
- "Actionable insights" unless grounded in a real workflow
- Mentioning other clients by name or referencing cross-client patterns
- **Naming a specific ERP system** (NetSuite, SAP, Business Central, Acumatica, etc.).
  Always say **"ERP"** — never the product name, even if the transcript names it.

Email length:

- Target 500-800 words.
- Complex accounts may run up to 1,000 words maximum.
- Keep the above-signature section especially tight.

## Internal Action Register

After the email, include:

| Priority | Category | Item | Owner | Source Detail | Next Step | In Email? |
|---|---|---|---|---|---|---|
| 1 | Support Ticket | [description] | [name/TBD] | [detail or quote] | [action] | Yes/No |

Rules:

- Do not fabricate owners. Use TBD when unclear.
- Do not fabricate ticket numbers, Jira IDs, or links. Use placeholders only if needed.
- Include items that are in the email and items too granular for the email but important internally.
- Training, workshop enrollment, and minor items belong here, not in the email unless they were a major client-raised topic.

## Assumptions / Placeholders

End with a short bulleted list:

- Assumptions made about data, ownership, or timeline
- Missing information needed before sending
- Placeholders requiring confirmation

## Quality Bar

Strong output:

- The customer feels deeply heard.
- The business implication is clear, not just the feature request.
- The follow-up has hierarchy: urgent support first, strategic items second, detail below signature.
- The next step is obvious.
- The email could be sent as-is by a CEO.

Weak output:

- Chronological meeting summary
- Transcript recap
- Ticket list
- Product wishlist
- Generic "thanks for your feedback"
- Overpromised roadmap commitments
- Training/workshop mentions shoehorned in without client context
