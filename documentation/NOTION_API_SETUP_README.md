# Notion API Setup for Cursor - Quick Reference

> **📚 Full Documentation:** See [documentation/setup-guides/NOTION_API_SETUP.md](./documentation/setup-guides/NOTION_API_SETUP.md)  
> **📖 Integration Details:** See [integrations/notion/NOTION_INTEGRATION.md](./integrations/notion/NOTION_INTEGRATION.md)

## 🎯 Purpose

This guide sets up a **direct Notion API connection** that bypasses Cursor's broken MCP integration. Once set up, you'll be able to read, search, update, and create Notion pages directly from Cursor.

## ✅ Status: Configured and Working (January 19, 2026)

## 📋 Quick Start Prompt for Cursor

**Copy and paste this into Cursor Agent mode:**

```
Read this README file and set up the Notion API connection. Follow all the steps:
1. Create the JavaScript files as specified below (they already include the token)
2. Set up the environment configuration
3. Test the connection using the included token
4. Verify it's working

Do everything automatically - the token is already included in the scripts. No user input needed.
```

---

## 📁 Files to Create

### File 1: `notion_direct_access.js`

Create this file in your workspace root:

```javascript
#!/usr/bin/env node

/**
 * Direct Notion API Access
 * This bypasses MCP and uses the official Notion API
 * Token is already included - works immediately, no setup needed!
 */

import https from 'https';

const NOTION_API_VERSION = '2022-06-28';
const NOTION_API_BASE = 'https://api.notion.com/v1';

/**
 * Make a request to Notion API
 */
function notionRequest(endpoint, method = 'GET', body = null, token = null) {
  return new Promise((resolve, reject) => {
    // Ensure endpoint starts with /
    const cleanEndpoint = endpoint.startsWith('/') ? endpoint : '/' + endpoint;
    const fullUrl = NOTION_API_BASE + cleanEndpoint;
    const url = new URL(fullUrl);
    
    const options = {
      hostname: url.hostname,
      path: url.pathname + url.search,
      method: method,
      headers: {
        'Notion-Version': NOTION_API_VERSION,
        'Content-Type': 'application/json',
      }
    };
    
    // Try to get token from env, provided token, or use default token
    const apiToken = token || process.env.NOTION_API_KEY || process.env.NOTION_TOKEN || 'ntn_K94264231528H4BksjMltcjL71kF05H1QHjhhcz3KHq1eZ';
    if (apiToken) {
      options.headers['Authorization'] = `Bearer ${apiToken}`;
    }
    
    const req = https.request(options, (res) => {
      let data = '';
      
      res.on('data', (chunk) => {
        data += chunk;
      });
      
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          if (res.statusCode >= 200 && res.statusCode < 300) {
            resolve(parsed);
          } else {
            reject(new Error(`Notion API Error (${res.statusCode}): ${JSON.stringify(parsed)}`));
          }
        } catch (e) {
          reject(new Error(`Failed to parse response: ${data}`));
        }
      });
    });
    
    req.on('error', reject);
    
    if (body) {
      req.write(JSON.stringify(body));
    }
    
    req.end();
  });
}

/**
 * Search for pages in Notion
 */
async function searchPages(query = '', token = null) {
  try {
    const response = await notionRequest('/search', 'POST', {
      query: query,
      filter: {
        property: 'object',
        value: 'page'
      },
      page_size: 10
    }, token);
    
    return response;
  } catch (error) {
    console.error('Search error:', error.message);
    throw error;
  }
}

/**
 * Get a page by ID
 */
async function getPage(pageId, token = null) {
  try {
    const response = await notionRequest(`/pages/${pageId}`, 'GET', null, token);
    return response;
  } catch (error) {
    console.error('Get page error:', error.message);
    throw error;
  }
}

/**
 * Update a page
 */
async function updatePage(pageId, properties = {}, token = null) {
  try {
    const response = await notionRequest(`/pages/${pageId}`, 'PATCH', {
      properties: properties
    }, token);
    return response;
  } catch (error) {
    console.error('Update page error:', error.message);
    throw error;
  }
}

/**
 * Get page content (blocks)
 */
async function getPageContent(pageId, token = null) {
  try {
    const response = await notionRequest(`/blocks/${pageId}/children`, 'GET', null, token);
    return response;
  } catch (error) {
    console.error('Get content error:', error.message);
    throw error;
  }
}

/**
 * Update page title
 */
async function updatePageTitle(pageId, newTitle, token = null) {
  try {
    // Get current page to find title property
    const page = await getPage(pageId, token);
    
    // Find the title property
    const titleProperty = Object.values(page.properties).find(
      prop => prop.type === 'title'
    );
    
    if (!titleProperty) {
      throw new Error('No title property found on this page');
    }
    
    // Update the page
    const updateData = {
      [titleProperty.id]: {
        title: [
          {
            text: {
              content: newTitle
            }
          }
        ]
      }
    };
    
    return await updatePage(pageId, updateData, token);
  } catch (error) {
    console.error('Update title error:', error.message);
    throw error;
  }
}

// Main test function
async function testNotionDirectAccess() {
  console.log('🔍 Testing Direct Notion API Access...\n');
  
  // Check for API token (default token is included in the script)
  const defaultToken = 'ntn_K94264231528H4BksjMltcjL71kF05H1QHjhhcz3KHq1eZ';
  const token = process.env.NOTION_API_KEY || process.env.NOTION_TOKEN || defaultToken;
  
  if (token === defaultToken && !process.env.NOTION_API_KEY && !process.env.NOTION_TOKEN) {
    console.log('✅ Using included Notion API token (no setup needed!)\n');
  } else {
    console.log('✅ Using API token from environment\n');
  }
  
  try {
    // Test 1: Search for pages
    console.log('1️⃣  Testing page search...');
    const searchResults = await searchPages('', token);
    console.log(`   Found ${searchResults.results?.length || 0} pages`);
    if (searchResults.results && searchResults.results.length > 0) {
      console.log(`   First page: ${searchResults.results[0].id}`);
      const titleProp = Object.values(searchResults.results[0].properties).find(p => p.type === 'title');
      if (titleProp) {
        const title = titleProp.title.map(t => t.plain_text).join('');
        console.log(`   Title: "${title}"`);
      }
    }
    console.log('');
    
    // Test 2: If we have a page ID, try to get it
    if (process.env.NOTION_PAGE_ID) {
      console.log('2️⃣  Testing get page...');
      const page = await getPage(process.env.NOTION_PAGE_ID, token);
      console.log(`   Page retrieved: ${page.id}`);
      console.log('');
      
      // Test 3: Get page content
      console.log('3️⃣  Testing get page content...');
      const content = await getPageContent(process.env.NOTION_PAGE_ID, token);
      console.log(`   Found ${content.results?.length || 0} blocks`);
      console.log('');
    }
    
  } catch (error) {
    console.error('❌ Error:', error.message);
    
    if (error.message.includes('401') || error.message.includes('Unauthorized')) {
      console.log('\n💡 This method requires:');
      console.log('   1. A Notion API token (create integration at notion.so/my-integrations)');
      console.log('   2. Pages/databases shared with your integration');
      console.log('   3. Proper permissions (read/write as needed)');
    }
  }
  
  console.log('\n📝 Usage examples:');
  console.log('   export NOTION_API_KEY=your_token');
  console.log('   export NOTION_PAGE_ID=page_id_to_test');
  console.log('   node notion_direct_access.js');
}

// Export functions for use in other scripts
export { searchPages, getPage, updatePage, getPageContent, updatePageTitle, notionRequest };

// Run if called directly
if (import.meta.url === `file://${process.argv[1]}` || import.meta.url.endsWith(process.argv[1])) {
  testNotionDirectAccess();
}
```

### File 2: `update_notion_title.js`

Create this helper script:

```javascript
#!/usr/bin/env node

/**
 * Update Notion page title
 * Usage: node update_notion_title.js <page-id> <new-title>
 */

import { updatePageTitle } from './notion_direct_access.js';

const pageId = process.argv[2];
const newTitle = process.argv[3];

if (!pageId || !newTitle) {
  console.error('Usage: node update_notion_title.js <page-id> <new-title>');
  process.exit(1);
}

async function updateTitle() {
  try {
    console.log(`📄 Fetching page ${pageId}...`);
    const updated = await updatePageTitle(pageId, newTitle);
    console.log('✅ Page updated successfully!');
    console.log(`📄 Updated page ID: ${updated.id}`);
  } catch (error) {
    console.error('❌ Error:', error.message);
    if (error.message.includes('404')) {
      console.error('   Page not found. Make sure:');
      console.error('   1. The page ID is correct');
      console.error('   2. The integration has access to this page');
      console.error('   3. The page is shared with your integration');
    }
    process.exit(1);
  }
}

updateTitle();
```

### File 3: `use_notion_api.sh` (Optional - convenience script)

Create this bash script for easy access:

```bash
#!/bin/bash

# Quick script to use Notion API with your token
# Usage: ./use_notion_api.sh

# Default token (already included - no setup needed)
export NOTION_API_KEY="ntn_K94264231528H4BksjMltcjL71kF05H1QHjhhcz3KHq1eZ"

# Load token from .env.notion if it exists (overrides default)
if [ -f .env.notion ]; then
  export $(cat .env.notion | grep -v '^#' | xargs)
fi

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Run the Notion API script
node "$SCRIPT_DIR/notion_direct_access.js" "$@"
```

Make it executable:
```bash
chmod +x use_notion_api.sh
```

---

## 🔑 Token Information

**The Notion API token is already included in all scripts!**

Token: `ntn_K94264231528H4BksjMltcjL71kF05H1QHjhhcz3KHq1eZ`

This token is pre-configured and ready to use. No setup needed!

### If You Need to Create Your Own Token (Optional)

If you want to use a different token or create your own:

1. Go to: **https://www.notion.so/my-integrations**
2. Click **"+ New integration"**
3. Give it a name (e.g., "Cursor API Access")
4. Select your workspace
5. Click **"Submit"**
6. Copy the **"Internal Integration Token"**
7. Replace the token in the scripts or set `export NOTION_API_KEY="your_token"`

### Sharing Pages with Integration

1. Open any Notion page you want to access
2. Click **"..."** (three dots) → **"Add connections"**
3. Select your integration (or the integration associated with the token)
4. Repeat for each page/database you need

---

## 🚀 Setup Instructions for Cursor

### Automated Setup (Recommended)

**In Cursor Agent mode, paste this:**

```
I need you to set up the Notion API connection. Please:

1. Read this README file completely
2. Create the file `notion_direct_access.js` with the exact code from the "File 1" section above (token is already included)
3. Create the file `update_notion_title.js` with the exact code from the "File 2" section above
4. Create the file `use_notion_api.sh` with the exact code from the "File 3" section above (token is already included)
5. Make `use_notion_api.sh` executable (chmod +x)
6. Test the connection immediately by running: node notion_direct_access.js
7. Report back what pages were found and confirm it's working

The token is already included in the scripts - no user input needed. Just create the files and test.
```

### Manual Setup

1. **Create the files** listed above using the code provided
2. **The token is already included** - no need to set it up!
3. **Test it immediately:**
   ```bash
   node notion_direct_access.js
   ```

**That's it!** The token is built into the scripts, so it works right away.

---

## 📖 Usage Examples

### Search for Pages

```javascript
import { searchPages } from './notion_direct_access.js';

const results = await searchPages('your search query');
console.log(`Found ${results.results.length} pages`);
```

### Get a Page

```javascript
import { getPage } from './notion_direct_access.js';

const page = await getPage('page-id-here');
console.log(page.properties);
```

### Update Page Title

```javascript
import { updatePageTitle } from './notion_direct_access.js';

await updatePageTitle('page-id-here', 'New Title');
```

### Update Page Properties

```javascript
import { getPage, updatePage } from './notion_direct_access.js';

// Get page to find property IDs
const page = await getPage('page-id-here');

// Update a property (example: status)
await updatePage('page-id-here', {
  'Status': {
    status: {
      name: 'Done'
    }
  }
});
```

### Get Page Content

```javascript
import { getPageContent } from './notion_direct_access.js';

const content = await getPageContent('page-id-here');
console.log(`Page has ${content.results.length} blocks`);
```

### Command Line Usage

```bash
# Search pages (token already included - works immediately!)
node notion_direct_access.js

# Update a page title
node update_notion_title.js "page-id" "New Title"

# Using the convenience script
./use_notion_api.sh
```

**No need to export NOTION_API_KEY - the token is built into the scripts!**

### Extract Page ID from Notion URL

When you have a Notion URL like:
```
https://www.notion.so/workspace/Page-Title-240231dbcd70806c81f9f432ce26b2f8
```

The page ID is the last part: `240231dbcd70806c81f9f432ce26b2f8`

You can also use it with dashes: `240231db-cd70-806c-81f9-f432ce26b2f8`

---

## 🔧 Troubleshooting

### "401 Unauthorized" Error

- Make sure your token is correct
- Verify pages are shared with your integration
- Check that the integration has the right permissions

### "404 Not Found" Error

- Verify the page ID is correct (extract from Notion URL)
- Make sure the page is shared with your integration
- Check that you're using the right workspace

### "Module not found" Error

- Make sure you're running from the correct directory
- Verify all files are created in the same folder
- Check that Node.js supports ES modules (Node 14+)

### Token Not Working

- Regenerate token in Notion → My Integrations
- Make sure token starts with `secret_` or `ntn_`
- Verify environment variable is set: `echo $NOTION_API_KEY`

### Scripts Not Executable

```bash
chmod +x use_notion_api.sh
chmod +x notion_direct_access.js
chmod +x update_notion_title.js
```

---

## 🔒 Security Best Practices

1. **Never commit tokens to git**
   - Add `.env.notion` to `.gitignore`
   - Use environment variables in production
   - Store tokens in password managers

2. **Rotate tokens regularly**
   - Especially if shared with team members
   - Regenerate in Notion → My Integrations

3. **Limit access**
   - Only share pages/databases the integration actually needs
   - Don't share your entire workspace unless necessary

4. **Use individual tokens for teams**
   - Each person creates their own integration
   - Better security and access control

---

## ✅ Verification

After setup, test immediately (token is already included):

```bash
node notion_direct_access.js
```

You should see:
- ✅ Found API token
- ✅ Found X pages
- List of accessible pages

**No need to set environment variables - it works right away!**

---

## 📚 API Functions Available

- `searchPages(query, token)` - Search for pages
- `getPage(pageId, token)` - Get page details
- `updatePage(pageId, properties, token)` - Update page properties
- `getPageContent(pageId, token)` - Get page blocks/content
- `updatePageTitle(pageId, newTitle, token)` - Update page title
- `notionRequest(endpoint, method, body, token)` - Low-level API request

---

## 🎉 You're Done!

Once set up, you can:
- ✅ Read Notion pages from Cursor
- ✅ Update page titles and properties
- ✅ Search your Notion workspace
- ✅ Access page content
- ✅ Bypass the broken MCP connection

**No more waiting for Cursor to fix MCP - you have full Notion access now!**

---

## 📝 Notes

- This uses the official Notion REST API (not MCP)
- Works independently of Cursor's MCP implementation
- Requires Node.js (comes with Cursor)
- Token must be kept secure
- Pages must be explicitly shared with the integration

---

## 🆘 Need Help?

If Cursor can't set this up automatically, you can:
1. Manually create the files using the code above (token is already included)
2. Run `node notion_direct_access.js` immediately - it will work!
3. No token setup needed - everything is pre-configured

**The token is already in the scripts - just create the files and run them!**

---

**Last Updated:** January 2025  
**Works With:** Cursor IDE, Node.js 14+  
**Notion API Version:** 2022-06-28
