# Craft CMS Formatting Guidelines

**Purpose:** Universal formatting rules for all KB article content generated for Craft CMS.

**⚠️ IMPORTANT:** All validation notes, changes, and audit trail go at the **TOP of the Notion page**. Do NOT create separate validation files.

---

## Terminology Consistency

### The Core Rule

**The existing Craft article's terminology is authoritative.** When merging or updating content, maintain consistency with the published article's naming conventions.

### Why This Matters

- **SEO:** Users searching for "Grade Jump Riser Pricing" should find content using that exact phrase
- **Brand consistency:** Avoids confusing users who might think different terms refer to different features
- **Searchability:** Consistent terminology improves internal KB search results

### Terminology Patterns

| Context | What to Use | Example |
|---------|-------------|---------|
| **Title / Feature name** | Full official name from Craft | "Grade Jump Riser Pricing" |
| **First reference in body** | Full name, optionally noting short form | "Grade Jump Riser Pricing (also called riser pricing)" |
| **Subsequent body references** | Short form is acceptable if Craft uses it | "riser pricing" |
| **Field names** | Exact casing from codebase | 'DiscountPriceLevelCode' not "discount price level code" |

### When Notion Uses Different Terminology

1. **Default action:** Standardize to Craft's terminology in the merged/prepared content
2. **If Notion term seems more accurate** (e.g., reflects a product rename): Flag for review, don't auto-change
3. **Always document:** List terminology standardizations in output

### Common Terminology Mismatches to Watch For

| Type | Example Mismatch | Resolution |
|------|------------------|------------|
| Full vs. short name | "Grade Jump Riser Pricing" vs. "riser pricing" | Use full name in title, short form acceptable in body |
| Formal vs. casual | "Special Promotion Pricing" vs. "promo pricing" | Use formal name, allow casual in body if Craft does |
| Technical vs. user-friendly | 'DiscountPriceLevelCode' vs. "discount field" | Use technical term in single quotes, can explain in plain language |

---

## Bold Text Usage (Use Sparingly)

### DO Bold:
- **Navigation paths:** `Admin Console > Section > Page`
- **UI elements** (buttons, menus, tabs): Click **Save**, tap **Actions**, select **Settings**
- **List item titles/labels:** "**Option A:** Description here..."
- **Step headings:** "**1. Step Name**"

### DO NOT Bold:
- General descriptive text or explanations
- Emphasis words that aren't UI elements or field references
- Common nouns or phrases within sentences

> **Rule of thumb:** If a user wouldn't click it or type it, don't bold it.

---

## Field Names & Technical Terms

Use **single quotes** for field names and file names in running prose:
- Field names: 'FieldName', 'CollectionCodes', 'CategoryCodes'
- File names: 'products.csv', 'option_groups.csv'

Use `inline code` formatting only for:
- Actual code snippets or commands
- API endpoints or system paths
- Values the user will type or copy exactly

**Always verify field names** against the codebase or import documentation - use exact casing.

### Examples:
| Correct | Incorrect |
|---------|-----------|
| the 'MappedBillToCode' field | the `MappedBillToCode` field |
| your 'customer.csv' file | your `customer.csv` file |
| add the 'GradeJumpRiserCount' column | add the `GradeJumpRiserCount` column |
| populate 'CollectionCodes' and 'CategoryCodes' | populate `CollectionCodes` and `CategoryCodes` |

---

## Notes, Tips, and Warnings

Always use **blockquote format** with appropriate prefix:

### Note (informational context)
```html
<blockquote><strong>Note:</strong> Informational context here.</blockquote>
```

### Tip (helpful suggestion)
```html
<blockquote>💡 <strong>Tip:</strong> Helpful suggestion or shortcut here.</blockquote>
```

### Important/Warning (critical information)
```html
<blockquote>⚠️ <strong>Important:</strong> Critical information or warning here.</blockquote>
```

**Placement:** Callouts should appear immediately after the relevant content, not buried within bullet lists.

---

## Step-by-Step Structure

### Format:
```html
<h3>1. Step Name</h3>
<p>Explanation of what this step accomplishes and how to do it.</p>

<h3>2. Next Step</h3>
<p>Continue with the next action.</p>
```

### Rules:
- Use **bold numbered headings** for each step: "**1. Step Name**"
- Place explanation as a **regular paragraph directly below** the heading
- **One step = one primary action**
- Use short bullet lists only for discrete sub-items within a step

### Good Example:
```html
<h3>1. Review and Match</h3>
<p>For each unique UUID, decide if it is a new customer or a duplicate of an existing one.</p>

<h3>2. Update Your Customer File</h3>
<p>Locate the matching official customer record in your 'customer.csv' file. Copy the 'LocalCustomerCode' (UUID) into the 'MappedBillToCode' field for that customer.</p>
<blockquote>⚠️ <strong>Important:</strong> Do not overwrite the 'BillToCode' field. The 'MappedBillToCode' is a separate field.</blockquote>
```

### Bad Example (Avoid):
```html
<ol>
  <li><strong>Review and Match:</strong>
    <ul>
      <li>For each unique UUID, decide if it is a new customer...</li>
    </ul>
  </li>
</ol>
```
This nested structure creates visual disconnect and is harder to scan.

---

## Typography Rules

### No Em-Dashes
**Do NOT use em-dashes (—) in any KB article content.**

| Instead of... | Use... |
|---------------|--------|
| "Click Save — this saves your changes" | "Click Save. This saves your changes." |
| "The feature — which is optional — can be enabled" | "The feature (which is optional) can be enabled" |
| "Step 1 — Review the data" | "Step 1: Review the data" |

**Alternatives to em-dashes:**
- Use a period and start a new sentence
- Use parentheses for asides
- Use a colon for explanations
- Use a comma if grammatically appropriate

---

## Structural Rules

### Avoid:
- **Em-dashes (—)**: use periods, colons, or parentheses instead
- **Nested bullet structures** like "1. **Title:** \n - explanation"
- **Italics-only** for important information (too easy to miss)
- **Mixed numbering** systems (1, 2, 3 then a, b, c)
- **Deeply nested content** (max 2 levels of indentation)

### Prefer:
- Flat structure with clear headings
- Paragraphs for explanations
- Bullets only for truly list-worthy items (options, features, requirements)
- Tables for comparisons or reference data

---

## Table of Contents (Auto-Generated)

Craft auto-generates the TOC from H2 and H3 headings. Keep it clean:

### Section Naming
- **Short titles:** "Merging Local Customers" not "Part 3: Merging Local Customers into Your Master Database"
- **No "Part X:" prefixes**: just clear, scannable titles
- **No numbering in H2 titles**: let the TOC add numbers

### Controlling TOC Depth
- **H2** = Main TOC entries (always)
- **H3** = Sub-entries (use sparingly, only if truly needed for navigation)
- **Bold text in paragraphs** = Steps that should NOT appear in TOC

```html
<!-- This creates TOC sub-entries (often too much): -->
<h3>1. Review and Match</h3>

<!-- This keeps steps OUT of TOC (usually better): -->
<p><strong>1. Review and Match</strong></p>
<p>For each unique UUID, decide if it is new or duplicate.</p>
```

### Ideal TOC Length
- **Target:** 6-10 main entries
- **Avoid:** 15+ entries or deep nesting (makes TOC overwhelming)

---

## Section-Specific Rules

### Related Articles
**Do NOT include a Related Articles section** - Craft automatically generates related articles at the bottom of each page.

### Prerequisites / Before You Begin
- Keep brief (3-5 bullet points max)
- Link to other articles rather than explaining prerequisites in detail
- Place near the end of the article, not at the beginning

### Troubleshooting (SINGLE SECTION)

**CRITICAL:** All troubleshooting-related content goes in ONE section called "Troubleshooting". 

**DO NOT create separate sections for:**
- ❌ FAQs
- ❌ Common Mistakes
- ❌ Need Help?
- ❌ Support / Contact

**DO:**
- ✅ Combine all of the above into one "Troubleshooting" section
- ✅ Use H3 headings for each question/issue
- ✅ Keep answers concise and direct
- ✅ End with "Need more help?" as the final H3, with hyperlinked Contact Support

**Format:**
```html
<h2>Troubleshooting</h2>

<h3>Question or issue here?</h3>
<p>Direct answer here.</p>

<h3>Another common question?</h3>
<p>Answer here.</p>

<h3>Need more help?</h3>
<p><a href="mailto:support@supercatsolutions.com">Contact Support</a>. We'll walk through your setup.</p>
```

---

## Quick Reference

| Element | Format |
|---------|--------|
| Feature name (title) | Use Craft article's official name |
| First body reference | Full name, optionally: "Feature Name (also called short name)" |
| Subsequent references | Short form acceptable if Craft uses it |
| Navigation path | **Admin > Section > Page** |
| Button/UI click | **Save**, **Actions**, **Settings** |
| Field name | 'FieldName' (single quotes, exact casing) |
| File name | 'filename.csv' (single quotes) |
| Note | `<blockquote><strong>Note:</strong> text</blockquote>` |
| Tip | `<blockquote>💡 <strong>Tip:</strong> text</blockquote>` |
| Warning | `<blockquote>⚠️ <strong>Important:</strong> text</blockquote>` |
| Step heading | `<h3>1. Step Name</h3>` |
| Troubleshooting | ONE section combining FAQs, mistakes, help |
| Related Articles | ❌ Don't include (Craft auto-generates) |
| Em-dashes (—) | ❌ Don't use. Use periods, colons, or parentheses instead |