# eCat Data Readiness Questionnaire (Client-Facing)

**To:** [Client Name]  
**From:** SuperCat Solutions Team  
**Goal:** A quick check to help us plan your setup. Don't worry about technical terms—just tell us how your business works today.

---

### SECTION 1: YOUR PRODUCTS (The Catalog)

**1. How do you keep track of all the items you sell?**
*   **Select one:**
    *   [ ] We have one master list in our system (Accounting/ERP)
    *   [ ] We keep everything in a spreadsheet (Excel)
    *   [ ] It's split across different files and catalogs
    *   [ ] We don't really have a single list right now
*   **Notes:** ___________________________________________________________

**2. Do you have digital photos of your products?**
*   **Select one:**
    *   [ ] Yes, and they are organized by part number (Easy to match up)
    *   [ ] Yes, but they have random names (We'd need to organize them)
    *   [ ] No, they are mostly stuck inside PDF catalogs or printed brochures
    *   [ ] We need to take new photos
*   **Notes:** ___________________________________________________________

**3. Do you sell products with lots of options (like fabrics, finishes, or sizes)?**
*   **Select one:**
    *   [ ] No, mostly simple items (What you see is what you get)
    *   [ ] Yes, but the price stays the same regardless of the option
    *   [ ] Yes, and the price changes depending on the fabric/finish chosen
*   **Notes:** ___________________________________________________________

---

### SECTION 2: YOUR CUSTOMERS (The Accounts)

**4. Do your customers have multiple locations?**
*(For example: A retail chain where the Head Office pays the bill, but you ship products to 10 different stores)*
*   **Select one:**
    *   [ ] Yes, and our system tracks the "Main Office" vs. the "Shipping Locations"
    *   [ ] Yes, but our contact list just mixes them all together
    *   [ ] No, we mostly sell to single-location businesses
*   **Notes:** ___________________________________________________________

**5. How do your Sales Reps know which customers are "theirs"?**
*   **Select one:**
    *   [ ] We assign them in our system (using codes or names)
    *   [ ] We just give them a list or spreadsheet
    *   [ ] It's open—reps can sell to anyone
*   **Notes:** ___________________________________________________________

---

### SECTION 3: OPERATIONS (The How)

**6. Do you want Reps to see "In Stock" levels in the app?**
*   **Select one:**
    *   [ ] Yes, our inventory numbers are generally accurate
    *   [ ] No, we prefer not to show stock levels right now
*   **Notes:** ___________________________________________________________

**7. How do you decide what price a customer pays?**
*   **Select one:**
    *   [ ] We have standard levels (e.g. Retail Price vs. Wholesale Price)
    *   [ ] We just give a flat discount (e.g. "Everyone gets 50% off")
    *   [ ] It's complicated—lots of customers have special negotiated contracts
    *   [ ] The Rep decides the price for each deal
*   **Notes:** ___________________________________________________________

**8. (Optional) Do you want to see past sales history in the app?**
*   **Select one:**
    *   [ ] Yes, we have good records from the last year or two
    *   [ ] No, let's just start fresh
*   **Notes:** ___________________________________________________________

---

### 📝 Internal Use Only: Sales Rep Mapping Key

*Use the client's answers above to populate HubSpot*

| If Client Checks... | You Select in HubSpot... |
| :--- | :--- |
| **Q1:** ERP / Clean Excel | **Data: Product Readiness** → *Ready / Clean* |
| **Q1:** Scattered / No List | **Data: Product Readiness** → *Messy / None* |
| | |
| **Q2:** Named by SKU | **Data: Image Status** → *Ready* |
| **Q2:** Random / Descriptive | **Data: Image Status** → *Needs Renaming* (Add Data Services) |
| **Q2:** PDF Only | **Data: Image Status** → *Not Available* (Risk) |
| | |
| **Q3:** Pricing Matrix | **Data: Complexity** → *High* (Requires Tech Scoping) |
| **Q3:** No / Same Price | **Data: Complexity** → *Simple / Medium* |
| | |
| **Q4:** Yes (Parent/Child) | **Data: Customer Data** → *ERP Export* |
| **Q4:** Mixed / Contact List | **Data: Customer Data** → *Flat List / None* |
| | |
| **Q7:** Contract Pricing / Manual | **Data: Pricing Model** → *Complex* (Risk) |
| **Q7:** Price Levels / Discount | **Data: Pricing Model** → *Standard* |

**Scoring the Deal:**
*   **0 Red Flags:** Standard Implementation
*   **1-2 Red Flags (Images/Data Cleaning):** Add "Data Services" Package
*   **"Pricing Matrix" or "Manual Pricing":** 🛑 STOP. Schedule Technical Scoping Call.
