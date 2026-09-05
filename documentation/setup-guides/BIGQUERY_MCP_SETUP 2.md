# BigQuery MCP Setup Guide

**Last Updated:** January 7, 2026  
**Status:** ✅ Configured and Working  
**Location:** SuperCat 4.0 (iCloud Drive)

---

## Quick Reference

**Service Account Credentials:**
```
/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/bigquery/service-account/supercat-data-pipeline-dbfab43c27bb.json
```

**Dataset:** `hevo_dataset_supercat_data_pipeline_Slhk`  
**Project:** `supercat-data-pipeline`  
**Service Account:** `cursor-gc-mcp@supercat-data-pipeline.iam.gserviceaccount.com`

---

## MCP Configuration

Add this to `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
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
    }
  }
}
```

---

## Essential Queries

### 1. Test Connection

```sql
SELECT 
  'Connection test' as status,
  CURRENT_TIMESTAMP() as query_time
```

### 2. List Available Tables

```sql
SELECT 
  table_schema,
  table_name,
  table_type
FROM `supercat-data-pipeline.hevo_dataset_supercat_data_pipeline_Slhk.INFORMATION_SCHEMA.TABLES`
ORDER BY table_name
```

### 3. Query Help Scout Tickets

```sql
SELECT DISTINCT
  conversation_id,
  ticket_number,
  ticket_subject,
  ticket_status,
  ticket_created_at
FROM `supercat-data-pipeline.hevo_dataset_supercat_data_pipeline_Slhk.help_scout_tickets`
ORDER BY ticket_created_at DESC
LIMIT 10
```

---

## Common Issues

### Issue: "Access Denied" Error

**Problem:** Using wrong dataset name

**Wrong:**
```sql
FROM `supercat-data-pipeline.hevo_helpscout.help_scout_tickets`
```

**Correct:**
```sql
FROM `supercat-data-pipeline.hevo_dataset_supercat_data_pipeline_Slhk.help_scout_tickets`
```

### Issue: MCP Server Not Found

**Solution:** Ensure npx path is correct for your Node.js version

```bash
# Check your npx location
which npx

# Update the path in ~/.cursor/mcp.json accordingly
```

---

## Documentation

- [HelpScout BigQuery Guide](../bigquery/documentation/HELPSCOUT_BIGQUERY_GUIDE.md)
- [BigQuery Troubleshooting](../bigquery/documentation/BIGQUERY_TROUBLESHOOTING.md)

---

## Backup Service Account

**Backup Location:** Also stored in local directory  
`/Users/kylorjohnson/bigquery/service-account/`

**Note:** Both locations contain the same file for redundancy. iCloud version is used by MCP.

---

**Setup By:** Kylor Johnson  
**Date:** January 7, 2026  
**Status:** ✅ Production Ready

