# Sales Data Scoping Framework (MVP)

**Goal:** Assess data readiness *during* the sales process to accurately forecast implementation effort.
**User:** Sales Reps (AEs)
**Timing:** Discovery Call or Demo

---

## 1. The 5-Minute Data Discovery Script

Ask these simple questions to understand their setup. We are looking for **Existence** (Do they have it?) and **Organization** (Is it messy?).

### Pillar A: PRODUCT DATA (The Catalog)
*Most critical. If this is messy, everything delays.*

**1. "How do you keep track of all the items you sell right now?"**
*   *Green Flag:* "We have one master list in our system (Accounting/ERP)."
*   *Red Flag:* "It's all over the place / We just have PDF catalogs."

**2. "Are your product photos organized?"**
*   *Green Flag:* "Yes, they are named by part number."
*   *Red Flag:* "No, they have random names (DSC_001.jpg) or we need to take new ones."

**3. "Do you have complex products where the price changes based on options?"**
*(e.g., Fabric A is cheaper than Fabric B)*
*   *Green Flag:* "No, simple items. What you see is what you pay."
*   *Yellow Flag:* "Yes, but the price is the same regardless of the fabric."
*   *Red Flag:* "Yes, it's complicated. The price changes depending on the exact finish and fabric grade chosen." *(High Complexity)*

### Pillar B: CUSTOMER DATA (The Accounts)
*Required for writing orders.*

**4. "Do you have a clean list of all your customers and their shipping locations?"**
*   *Green Flag:* "Yes, our system tracks the main office and all their store locations."
*   *Red Flag:* "We just have a contact list in Outlook/Gmail."

**5. "How do your Reps know which customers belong to them?"**
*   *Green Flag:* "We assign them in our system."
*   *Red Flag:* "It's a free-for-all / We don't track that."

### Pillar C: INVENTORY & PRICING (The Operations)
*Required for trust and accuracy.*

**6. "Do you want to show 'In Stock' numbers in the app?"**
*   *Green Flag:* "Yes, our inventory numbers are good."
*   *Red Flag:* "No, our inventory is a mess / we don't track it."

**7. "How do you decide what price a customer pays?"**
*   *Green Flag:* "We have standard levels (Retail vs. Wholesale)."
*   *Red Flag:* "Every customer has a special deal / The rep just makes it up."

### BONUS: SALES HISTORY
*Nice to have for day-one value.*

**8. "Do you have good sales history from the last year or two?"**
*   *Green Flag:* "Yes."
*   *Red Flag:* "No / It's too messy." *(Note: This is okay, just means we skip importing history).*

---

## 2. The "Traffic Light" Scoring Matrix

Use this to select the **Implementation Level** in HubSpot.

| | 🟢 **LOW EFFORT** <br>*(Standard Onboarding)* | 🟡 **MEDIUM EFFORT** <br>*(Data Services Needed)* | 🔴 **HIGH EFFORT** <br>*(Custom / Risk)* |
| :--- | :--- | :--- | :--- |
| **Products** | One master list in system. | Scattered sheets, but usable. | No master list exists. |
| **Images** | Named by Part Number. | Needs renaming. | Stuck in PDFs / Needs photos. |
| **Complexity**| Simple items. | Options exist, simple pricing. | **Complex Pricing** (Price changes by option). |
| **Customers** | Tracks Main Office vs. Stores. | Flat list (mixed together). | No list / Contacts only. |
| **Territories** | Assigned in system. | Needs manual work. | Free-for-all / No logic. |
| **Pricing** | Standard Levels (Retail/Wholesale). | Simple Discounts. | **Complex Contracts** / Manual Pricing. |

---

## 3. HubSpot Fields (The Checklist)

Rep must fill these out to move Deal to **"Proposal/Scoping"** stage.

| Property Label | Type | Options |
| :--- | :--- | :--- |
| **Data: Product List** | Dropdown | • System Export (Ready)<br>• Spreadsheets (Clean)<br>• Spreadsheets (Messy)<br>• None |
| **Data: Image Status** | Dropdown | • Named by Part # (Ready)<br>• Random Names (Needs Work)<br>• Not Available / PDF Only |
| **Data: Product Complexity** | Dropdown | • Simple (One price)<br>• Medium (Options, same price)<br>• **High (Price changes by option)** |
| **Data: Customer List** | Dropdown | • System Export (Good)<br>• Messy / Flat List<br>• None |
| **Data: Inventory Avail?** | Radio | • Yes<br>• No |
| **Data: Sales History?** | Radio | • Yes (Include)<br>• No (Skip) |
| **Implementation Level** | Dropdown | • **Standard** (Low Effort)<br>• **Elevated** (Medium - Add Data Hours)<br>• **Custom** (High - Req. Tech Scoping) |

---

### Implementation Note for Sales
*   **Low Effort:** We give them templates, they fill them out. Easy.
*   **Medium Effort:** We'll likely need to help them fix their Excel files or rename images. **Budget for 5-10 hours of Data Services.**
*   **High Effort:** Do not quote without talking to Tech. We might need to build something custom.
