# Complete MCP Configuration Guide

**Last Updated:** January 7, 2026  
**Configuration File:** `~/.cursor/mcp.json`  
**Location:** SuperCat 4.0 (iCloud Drive)

---

## Current MCP Configuration

This is your complete, working MCP configuration for all SuperCat integrations:

```json
{
  "mcpServers": {
    "supercat-cs-tools": {
      "command": "node",
      "args": ["/Users/kylorjohnson/supercat-code/supercat_server/bin/mcp-server"]
    },
    "bigquery": {
      "command": "/Users/kylorjohnson/.nvm/versions/node/v25.2.1/bin/npx",
      "args": [
        "-y",
        "@ergut/mcp-bigquery-server",
        "--project-id",
        "supercat-data-pipeline",
        "--location",
        "US",
        "--key-file",
        "/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/bigquery/service-account/supercat-data-pipeline-dbfab43c27bb.json"
      ]
    },
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

## MCP Servers Explained

### 1. supercat-cs-tools

**Purpose:** Custom customer success tools from supercat codebase  
**Location:** Local codebase (`/Users/kylorjohnson/supercat-code`)  
**Note:** Runs from local codebase, not iCloud

**Capabilities:**
- `get_organization_info` - Org overview and configuration
- `get_org_users` - Users with permissions
- `analyze_user_permissions` - Diagnose visibility issues
- `get_import_events` - Import history and errors
- `get_customer_hierarchy` - Customer relationships
- `get_products`, `get_customers`, `get_orders` - Data queries
- Plus 20+ more tools

### 2. bigquery

**Purpose:** Query SuperCat data in BigQuery  
**Location:** iCloud Drive (service account credentials)  
**Dataset:** `hevo_dataset_supercat_data_pipeline_Slhk`

**Capabilities:**
- Query Help Scout tickets
- Access customer support history
- Analyze product data
- Run custom SQL queries

### 3. craft-cms

**Purpose:** Read/write Knowledge Base articles  
**Location:** Cloud (GraphQL API)  
**Endpoint:** https://supercatsolutions.com/actions/graphql/api

**Capabilities:**
- Query KB articles
- Create/update/delete articles
- Manage categories
- Draft and publish content

---

## File Locations by Device

### iCloud Drive (Synced Across Devices)

```
~/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/
├── bigquery/
│   └── service-account/supercat-data-pipeline-dbfab43c27bb.json
├── craft-cms/
│   ├── queries/
│   └── documentation/
├── mcp-integration/
│   └── configs/
└── documentation/
```

### Local (Device-Specific)

```
~/.cursor/mcp.json                    # MCP configuration
/Users/kylorjohnson/supercat-code/    # Main codebase (git repo)
/Users/kylorjohnson/.nvm/             # Node.js versions
```

---

## Setup on New Device

### Step 1: Install Dependencies

```bash
# Install Node.js (via nvm)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 25.2.1
nvm use 25.2.1

# Install global npm packages
npm install -g npx
```

### Step 2: Clone Supercat Codebase

```bash
cd /Users/kylorjohnson
git clone <supercat-repo-url> supercat-code
cd supercat-code/supercat_server
npm install
```

### Step 3: Configure MCP

```bash
# Create MCP config directory
mkdir -p ~/.cursor

# Copy the configuration above to ~/.cursor/mcp.json
# Edit paths as needed for your device
```

### Step 4: Wait for iCloud Sync

Allow time for iCloud Drive to sync the "SuperCat 4.0" folder with:
- BigQuery credentials
- Documentation
- Saved queries

### Step 5: Restart Cursor

Restart Cursor to load the new MCP configuration.

### Step 6: Test Connections

```bash
# In Cursor, test each MCP server:
# 1. Test supercat-cs-tools
# 2. Test bigquery
# 3. Test craft-cms
```

---

## Troubleshooting

### MCP Server Not Loading

**Check:**
1. Node.js is installed: `node --version`
2. npx path is correct: `which npx`
3. Service account file exists in iCloud
4. Cursor has been restarted

### BigQuery Access Denied

**Fix:** Ensure using correct dataset name
```
hevo_dataset_supercat_data_pipeline_Slhk  ✅
hevo_helpscout  ❌
```

### Craft CMS Connection Failed

**Fix:** Verify API token is valid and endpoint is accessible
```bash
curl -H "Authorization: Bearer HF9F8pdP9YDpLvM8FRwTH0ytRXChgLaD" \
  https://supercatsolutions.com/actions/graphql/api \
  -d '{"query": "{ping}"}'
```

---

## Maintenance

### Updating Service Account Credentials

1. Place new JSON file in `SuperCat 4.0/bigquery/service-account/`
2. Update path in `~/.cursor/mcp.json`
3. Restart Cursor

### Updating Node.js Version

1. Install new version: `nvm install <version>`
2. Update npx path in `~/.cursor/mcp.json`
3. Restart Cursor

### Adding New MCP Server

1. Add configuration to `~/.cursor/mcp.json`
2. Document in this guide
3. Test on all devices

---

## Security Notes

### Credentials in iCloud

✅ **Safe:** Service account credentials in iCloud Drive
- iCloud is encrypted at rest
- End-to-end encryption for synced data
- Two-factor authentication required

### API Tokens in Config

✅ **Safe:** API tokens in `~/.cursor/mcp.json`
- File is local to each device
- Not synced via iCloud
- Protected by filesystem permissions

### Git Exclusions

❌ **Never commit:**
- `~/.cursor/mcp.json`
- Service account JSON files
- API tokens

---

## Quick Commands

### View Current Configuration

```bash
cat ~/.cursor/mcp.json
```

### Test BigQuery Connection

```bash
# In Cursor, run:
# SELECT CURRENT_TIMESTAMP()
```

### Test Craft CMS Connection

```bash
# In Cursor, run:
# { ping }
```

### View iCloud Sync Status

```bash
ls -la "/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0"
```

---

**Maintained By:** Kylor Johnson  
**Last Updated:** January 7, 2026  
**Status:** ✅ All Systems Operational

