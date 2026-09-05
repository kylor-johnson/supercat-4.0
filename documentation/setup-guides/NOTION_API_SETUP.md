# Notion API Setup Guide

**Last Updated:** January 19, 2026  
**Status:** ✅ Configured and Working  
**Location:** SuperCat 4.0 (iCloud Drive)

---

## Quick Reference

**API Endpoint:**
```
https://api.notion.com/v1
```

**API Token:**
```
ntn_K94264231528H4BksjMltcjL71kF05H1QHjhhcz3KHq1eZ
```

**API Version:**
```
2022-06-28
```

---

## Purpose

This integration provides **direct Notion API access** that bypasses Cursor's MCP integration. It enables reading, searching, updating, and creating Notion pages directly from Cursor.

---

## Files Location

| File | Path | Purpose |
|------|------|---------|
| `notion_direct_access.js` | Workspace root | Main API module |
| `update_notion_title.js` | Workspace root | Title update helper |
| `use_notion_api.sh` | Workspace root | Convenience bash script |
| Full documentation | `integrations/notion/` | Complete integration docs |

---

## Available Functions

| Function | Description | Parameters |
|----------|-------------|------------|
| `searchPages(query, token)` | Search for pages in workspace | `query`: search term |
| `getPage(pageId, token)` | Get page details by ID | `pageId`: Notion page ID |
| `updatePage(pageId, properties, token)` | Update page properties | `pageId`, `properties` object |
| `getPageContent(pageId, token)` | Get page blocks/content | `pageId`: Notion page ID |
| `updatePageTitle(pageId, newTitle, token)` | Update page title | `pageId`, `newTitle` |
| `notionRequest(endpoint, method, body, token)` | Low-level API request | See API docs |

---

## Quick Start

### Test Connection

```bash
node notion_direct_access.js
```

**Expected output:**
```
🔍 Testing Direct Notion API Access...

✅ Using included Notion API token (no setup needed!)

1️⃣  Testing page search...
   Found 10 pages
   First page: 240231db-cd70-806c-81f9-f432ce26b2f8
   Title: "How Riser Pricing Works — And How to Troubleshoot It"
```

### Search for Pages

```javascript
import { searchPages } from './notion_direct_access.js';

const results = await searchPages('pricing');
console.log(`Found ${results.results.length} pages`);
```

### Get a Page

```javascript
import { getPage } from './notion_direct_access.js';

const page = await getPage('240231db-cd70-806c-81f9-f432ce26b2f8');
console.log(page.properties);
```

### Update Page Title

```javascript
import { updatePageTitle } from './notion_direct_access.js';

await updatePageTitle('page-id-here', 'New Title');
```

### Command Line Usage

```bash
# Test connection
node notion_direct_access.js

# Update a page title
node update_notion_title.js "page-id" "New Title"

# Using convenience script
./use_notion_api.sh
```

---

## Extracting Page IDs

When you have a Notion URL like:
```
https://www.notion.so/workspace/Page-Title-240231dbcd70806c81f9f432ce26b2f8
```

The page ID is the last part: `240231dbcd70806c81f9f432ce26b2f8`

You can also use it with dashes: `240231db-cd70-806c-81f9-f432ce26b2f8`

---

## Sharing Pages with Integration

For the integration to access Notion pages:

1. Open any Notion page you want to access
2. Click **"..."** (three dots) → **"Add connections"**
3. Select the integration (associated with the API token)
4. Repeat for each page/database you need

---

## Troubleshooting

### "401 Unauthorized" Error
- Verify the API token is correct
- Ensure pages are shared with the integration
- Check that the integration has proper permissions

### "404 Not Found" Error
- Verify the page ID is correct (extract from Notion URL)
- Ensure the page is shared with the integration
- Check that you're using the correct workspace

### "Module not found" Error
- Run from the correct directory (workspace root)
- Verify all files are in the same folder
- Ensure Node.js supports ES modules (Node 14+)

---

## Security Best Practices

1. **Never commit tokens to git** - Add `.env.notion` to `.gitignore`
2. **Rotate tokens regularly** - Especially if shared with team members
3. **Limit access** - Only share pages/databases the integration actually needs
4. **Use individual tokens for teams** - Each person creates their own integration

---

## Creating Your Own Token (Optional)

If you need to create your own Notion API token:

1. Go to: **https://www.notion.so/my-integrations**
2. Click **"+ New integration"**
3. Give it a name (e.g., "Cursor API Access")
4. Select your workspace
5. Click **"Submit"**
6. Copy the **"Internal Integration Token"**
7. Replace the token in scripts or set `export NOTION_API_KEY="your_token"`

---

## Test Results (January 19, 2026)

✅ Connection Test - Success  
✅ Page Search - 10 pages retrieved  
✅ API Token - Working with included token  
✅ Direct API Access - Bypassing MCP successfully

---

## Related Documentation

- [Notion Integration Details](../../integrations/notion/NOTION_INTEGRATION.md)
- [Craft CMS Setup](./CRAFT_CMS_SETUP.md)
- [BigQuery MCP Setup](./BIGQUERY_MCP_SETUP.md)

---

**Setup By:** Kylor Johnson  
**Last Tested:** January 19, 2026  
**Status:** ✅ Production Ready
