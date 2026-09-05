# SuperCat 4.0 - Quick Start Guide

**Welcome to your consolidated SuperCat integration hub!**

---

## 🎯 What is This?

SuperCat 4.0 is your **device-agnostic integration hub** for:
- ✅ BigQuery data access
- ✅ Craft CMS knowledge base management
- ✅ MCP (Model Context Protocol) integrations
- ✅ Documentation and setup guides

**Synced via iCloud Drive** - Access from any Mac!

---

## 🚀 Quick Start (5 Minutes)

### 1. Update MCP Configuration

```bash
cd "/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/scripts/setup"
./update-mcp-config.sh
```

This script will:
- ✅ Detect your Node.js installation
- ✅ Update `~/.cursor/mcp.json` with correct paths
- ✅ Point to iCloud service account credentials
- ✅ Create backup of existing config

### 2. Restart Cursor

Close and reopen Cursor to load the new MCP configuration.

### 3. Test Connections

In Cursor, run these tests:

**BigQuery Test:**
```sql
SELECT CURRENT_TIMESTAMP() as test
```

**Craft CMS Test:**
```graphql
{ ping }
```

**SuperCat CS Tools Test:**
```
Use any mcp_supercat-cs-tools function
```

---

## 📁 Folder Structure

```
SuperCat 4.0/
├── README.md                    # Main documentation
├── QUICKSTART.md               # This file
├── bigquery/                   # BigQuery integrations
│   ├── service-account/        # Credentials
│   ├── queries/                # Saved SQL queries
│   └── documentation/          # BigQuery docs
├── craft-cms/                  # Craft CMS integrations
│   ├── queries/                # GraphQL queries
│   ├── mutations/              # GraphQL mutations
│   └── documentation/          # CMS docs
├── mcp-integration/            # MCP configurations
│   ├── configs/                # Config templates
│   └── documentation/          # MCP docs
├── documentation/              # General docs
│   ├── setup-guides/           # Setup instructions
│   ├── validation-reports/     # KB validation reports
│   └── troubleshooting/        # Troubleshooting guides
└── scripts/                    # Automation scripts
    ├── setup/                  # Setup scripts
    └── utilities/              # Utility scripts
```

---

## 📖 Essential Documentation

### Setup Guides
- [BigQuery MCP Setup](documentation/setup-guides/BIGQUERY_MCP_SETUP.md)
- [Craft CMS Setup](documentation/setup-guides/CRAFT_CMS_SETUP.md)
- [Complete MCP Configuration](documentation/setup-guides/MCP_CONFIGURATION.md)

### Reference Docs
- [HelpScout BigQuery Guide](bigquery/documentation/HELPSCOUT_BIGQUERY_GUIDE.md)
- [BigQuery Troubleshooting](bigquery/documentation/BIGQUERY_TROUBLESHOOTING.md)
- [Craft CMS Cursor Setup](craft-cms/documentation/CRAFT_CMS_CURSOR_SETUP.md)

---

## 🔧 Common Tasks

### Query Help Scout Tickets

```sql
SELECT DISTINCT
  conversation_id,
  ticket_number,
  ticket_subject,
  ticket_created_at
FROM `supercat-data-pipeline.hevo_dataset_supercat_data_pipeline_Slhk.help_scout_tickets`
WHERE EXISTS (
  SELECT 1 FROM UNNEST(ticket_tags) as tag 
  WHERE tag.tag_name = 'add to knowledge base'
)
ORDER BY ticket_created_at DESC
LIMIT 10
```

### Query Knowledge Base Categories

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

### Create Draft KB Article

```graphql
mutation {
  save_knowledgeBase_knowledgeBase_Entry(
    title: "My New Article"
    slug: "my-new-article"
    enabled: false
    authorId: 39645
    siteId: 1
    summary: "<p>Article summary</p>"
  ) {
    id
    title
  }
}
```

---

## 🆘 Troubleshooting

### BigQuery Access Denied

**Fix:** Use correct dataset name
```
✅ hevo_dataset_supercat_data_pipeline_Slhk
❌ hevo_helpscout
```

### MCP Server Not Loading

**Fix:** 
1. Check Node.js installed: `node --version`
2. Run setup script: `./scripts/setup/update-mcp-config.sh`
3. Restart Cursor

### Service Account Not Found

**Fix:** Wait for iCloud Drive to sync
```bash
ls -la "bigquery/service-account/"
```

---

## 📍 File Locations

### iCloud Drive (This Folder)
```
~/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/
```

### Local Codebase (Not Synced)
```
~/supercat-code/
```

### MCP Configuration (Local)
```
~/.cursor/mcp.json
```

---

## 🔒 Security Notes

✅ **Safe to sync via iCloud:**
- Service account credentials (encrypted by iCloud)
- Documentation
- Query templates

❌ **Never commit to git:**
- Service account JSON files
- API tokens
- MCP configuration file

---

## 🎯 Design Philosophy

**Device-Agnostic:**
- Access integrations from any Mac
- iCloud sync keeps everything up to date
- Local codebase stays separate for git

**Organized:**
- Clear folder structure
- Comprehensive documentation
- Easy to find what you need

**Production-Ready:**
- All integrations tested and working
- Backup of existing configurations
- No manual setup required

---

## 📞 Need Help?

1. Check documentation in `documentation/` folder
2. Review troubleshooting guides
3. Run setup script again: `./scripts/setup/update-mcp-config.sh`

---

**Created:** January 7, 2026  
**Version:** 4.0  
**Status:** ✅ Ready to Use

**Get started now:**
```bash
./scripts/setup/update-mcp-config.sh
```

