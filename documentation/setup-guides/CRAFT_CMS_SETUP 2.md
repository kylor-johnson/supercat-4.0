# Craft CMS MCP Setup Guide

**Last Updated:** January 7, 2026  
**Status:** ✅ Configured and Working  
**Location:** SuperCat 4.0 (iCloud Drive)

---

## Quick Reference

**GraphQL Endpoint:**
```
https://supercatsolutions.com/actions/graphql/api
```

**API Token:**
```
HF9F8pdP9YDpLvM8FRwTH0ytRXChgLaD
```

**Default Author:**
- **Name:** Kyla Bosch
- **ID:** 39645
- **UID:** 9d9076c8-2927-4931-8905-16adbd50577c
- **Email:** kyla@supercatsolutions.com

---

## MCP Configuration

Add this to `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "craft-cms": {
      "command": "npx",
      "args": ["-y", "mcp-graphql"],
      "env": {
        "ENDPOINT": "https://supercatsolutions.com/actions/graphql/api",
        "HEADERS": "{\"Authorization\":\"Bearer HF9F8pdP9YDpLvM8FRwTH0ytRXChgLaD\"}",
        "ALLOW_MUTATIONS": "true",
        "NAME": "craft-cms"
      }
    }
  }
}
```

---

## Knowledge Base Categories

### Level 1 Categories (Main Sections)
- **ID: 1772** - Sales Portal (`sales-portal`)
- **ID: 40045** - Getting Started with Supercat (`getting-started-with-supercat`)
- **ID: 40046** - Building & Managing Your Digital Catalog (`building-managing-your-digital-catalog`)
- **ID: 40047** - Selling Smarter: Orders, Presentations & Customer Engagement (`selling-smarter-orders-presentations-customer-engagement`)
- **ID: 40048** - Mastering Pricing, Promotions & Inventory (`mastering-pricing-promotions-inventory`)
- **ID: 40049** - Administering Your Supercat Platform (`administering-your-supercat-platform`)
- **ID: 40050** - Leveraging Data: Reporting & Analytics (`leveraging-data-reporting-analytics`)
- **ID: 40051** - Advanced Tools & Integrations (`advanced-tools-integrations`)
- **ID: 40052** - Troubleshooting & Getting Help (`troubleshooting-getting-help`)

### Level 2 Categories (Sub-sections)
- **ID: 1404** - Troubleshooting (`troubleshooting`)
- **ID: 1380** - Products (`products`)
- **ID: 1406** - Pricing (`pricing`)
- **ID: 1381** - Customers (`customers`)
- **ID: 127** - Orders (`api`)
- **ID: 1412** - Reports (`reports`)
- *(See full list in documentation)*

---

## Essential Queries

### 1. Test Connection

```graphql
{
  ping
}
```

**Expected:** `{"data": {"ping": "pong"}}`

### 2. Query Categories

```graphql
{
  categories(group: "knowledgeBase") {
    id
    title
    slug
    level
  }
}
```

### 3. Get Entry by ID

```graphql
{
  entries(section: "knowledgeBase", id: "41623") {
    id
    title
    slug
    summary
    dateCreated
    dateUpdated
  }
}
```

### 4. Query Recent Entries

```graphql
{
  entries(section: "knowledgeBase", limit: 10, orderBy: "dateCreated DESC") {
    id
    title
    slug
    dateCreated
  }
}
```

---

## Essential Mutations

### 1. Create Draft Entry

```graphql
mutation {
  save_knowledgeBase_knowledgeBase_Entry(
    title: "New Article Title"
    slug: "new-article-slug"
    enabled: false
    authorId: 39645
    siteId: 1
    summary: "<p>Article summary</p>"
  ) {
    id
    title
    slug
  }
}
```

### 2. Update Entry

```graphql
mutation {
  save_knowledgeBase_knowledgeBase_Entry(
    id: "41623"
    title: "Updated Title"
  ) {
    id
    title
    dateUpdated
  }
}
```

### 3. Delete Entry

```graphql
mutation {
  deleteEntry(id: 41635)
}
```

---

## Workflow Guidelines

### Creating New Entries

1. **Draft First:** Always create as draft (`enabled: false`)
2. **Prompt for Category:** If user doesn't specify, show category list
3. **Use Default Author:** Kyla Bosch (39645) unless specified
4. **Test Before Publishing:** Verify content in draft mode

### Updating Entries

1. **Query First:** Get current entry data
2. **Preserve Content:** Don't overwrite unintentionally
3. **Update Incrementally:** Test small changes first

---

## Documentation

- [Complete Craft CMS Setup Guide](../craft-cms/documentation/CRAFT_CMS_CURSOR_SETUP.md)
- [Craft CMS Mutations Reference](../craft-cms/mutations/)
- [Craft CMS Queries Reference](../craft-cms/queries/)

---

## Test Results (January 7, 2026)

✅ Connection Test - Success  
✅ Categories Query - 27 categories retrieved  
✅ Create Draft Entry - ID 41635 created  
✅ Delete Entry - Successfully deleted  
✅ Update Entry - Tested and working

---

**Setup By:** Kylor Johnson  
**Last Tested:** January 7, 2026  
**Status:** ✅ Production Ready

