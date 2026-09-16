#!/usr/bin/env python3
"""Prefetch Postgres data via MCP-like JSON and save to CSV cache files.

This script is a manual step: copy MCP query results (as JSON arrays)
into the pg_cache/ directory as CSVs. Run each query via the Postgres MCP,
paste the JSON result, and this converts it to CSV.

Usage: python prefetch_pg_cache.py
       (interactive — paste MCP JSON results when prompted)

Or: use the auto mode with --from-mcp-output <file> to process
    saved MCP query outputs.
"""
import json
import os
import sys
import csv

CACHE_DIR = os.path.join(os.path.dirname(__file__), "pg_cache")

QUERIES = {
    "pg_cat": """SELECT o.shortname AS org_shortname, COUNT(*) FILTER (WHERE p.deleted = false) AS total_active_products, COUNT(*) FILTER (WHERE p.deleted = false AND p.image_exists = true AND p.net_price IS NOT NULL AND p.net_price > 0) AS complete_products, CASE WHEN COUNT(*) FILTER (WHERE p.deleted = false) = 0 THEN NULL ELSE ROUND(COUNT(*) FILTER (WHERE p.deleted = false AND p.image_exists = true AND p.net_price IS NOT NULL AND p.net_price > 0)::numeric / COUNT(*) FILTER (WHERE p.deleted = false)::numeric, 4) END AS catalog_completeness FROM products p JOIN organizations o ON p.organization_id = o.id GROUP BY o.shortname""",

    "pg_users": """SELECT o.shortname AS org_shortname, COUNT(*) AS total_users FROM org_users ou JOIN organizations o ON ou.organization_id = o.id GROUP BY o.shortname""",

    "pg_stacks": """SELECT o.shortname AS org_shortname, COUNT(*) AS smart_stack_count FROM smart_stacks ss JOIN organizations o ON ss.organization_id = o.id GROUP BY o.shortname""",

    "pg_imp": """SELECT o.shortname AS org_shortname, COUNT(*) FILTER (WHERE ie.created_at >= CURRENT_DATE - INTERVAL '90 days') AS total_imports_90d, COUNT(*) FILTER (WHERE ie.created_at >= CURRENT_DATE - INTERVAL '90 days' AND ie.data NOT LIKE '%%:error%%' AND ie.data NOT LIKE '%%:fatal%%') AS successful_imports_90d, CASE WHEN COUNT(*) FILTER (WHERE ie.created_at >= CURRENT_DATE - INTERVAL '90 days') = 0 THEN NULL ELSE ROUND(COUNT(*) FILTER (WHERE ie.created_at >= CURRENT_DATE - INTERVAL '90 days' AND ie.data NOT LIKE '%%:error%%' AND ie.data NOT LIKE '%%:fatal%%')::numeric / COUNT(*) FILTER (WHERE ie.created_at >= CURRENT_DATE - INTERVAL '90 days')::numeric, 4) END AS import_success_rate FROM organizations o LEFT JOIN import_events ie ON ie.organization_id = o.id GROUP BY o.id, o.shortname""",

    "pg_ord": """SELECT o.shortname AS org_shortname, COUNT(*) FILTER (WHERE ord.is_submitted = true AND ord.submit_date >= CURRENT_DATE - INTERVAL '90 days' AND ord.order_state = 'active') AS orders_90d, COUNT(*) FILTER (WHERE ord.is_submitted = true AND ord.submit_date >= CURRENT_DATE - INTERVAL '180 days' AND ord.submit_date < CURRENT_DATE - INTERVAL '90 days' AND ord.order_state = 'active') AS orders_prior_90d, COUNT(*) FILTER (WHERE ord.is_submitted = true AND ord.submit_date >= CURRENT_DATE - INTERVAL '90 days' AND ord.order_state = 'active' AND LOWER(ord.order_source) = 'ipad') AS ipad_orders_90d, COUNT(*) FILTER (WHERE ord.is_submitted = true AND ord.submit_date >= CURRENT_DATE - INTERVAL '90 days' AND ord.order_state = 'active' AND LOWER(ord.order_source) != 'ipad') AS online_orders_90d, CASE WHEN COUNT(*) FILTER (WHERE ord.is_submitted = true) > 0 THEN true ELSE false END AS orders_exist_any_time FROM organizations o LEFT JOIN orders ord ON ord.organization_id = o.id GROUP BY o.shortname""",

    "pg_cust": """WITH org_customer_counts AS (SELECT o.shortname AS org_shortname, COUNT(*) AS total_customers FROM customers c JOIN organizations o ON c.organization_id = o.id GROUP BY o.shortname), activation_metrics AS (SELECT o.shortname AS org_shortname, COUNT(DISTINCT ord.customer_num) FILTER (WHERE ord.submit_date >= CURRENT_DATE - INTERVAL '90 days' AND ord.is_submitted = true AND ord.order_state = 'active') AS ordering_customers_90d, COUNT(DISTINCT ord.customer_num) FILTER (WHERE ord.submit_date < CURRENT_DATE - INTERVAL '90 days' AND ord.is_submitted = true AND ord.order_state = 'active') - COUNT(DISTINCT ord.customer_num) FILTER (WHERE ord.submit_date >= CURRENT_DATE - INTERVAL '90 days' AND ord.is_submitted = true AND ord.order_state = 'active') AS dormant_customers FROM orders ord JOIN organizations o ON ord.organization_id = o.id WHERE ord.customer_num IS NOT NULL GROUP BY o.shortname) SELECT occ.org_shortname, occ.total_customers, COALESCE(am.ordering_customers_90d, 0) AS ordering_customers_90d, GREATEST(COALESCE(am.dormant_customers, 0), 0) AS dormant_customers FROM org_customer_counts occ LEFT JOIN activation_metrics am ON occ.org_shortname = am.org_shortname""",

    "pg_fresh": """SELECT o.shortname AS org_shortname, MAX(CASE WHEN dv.entity_type = 'products' THEN dv.timestamp END) AS last_products_update, MAX(CASE WHEN dv.entity_type = 'customers' THEN dv.timestamp END) AS last_customers_update, MAX(CASE WHEN dv.entity_type = 'inventories' THEN dv.timestamp END) AS last_inventories_update, EXTRACT(DAY FROM (CURRENT_TIMESTAMP - GREATEST(COALESCE(MAX(CASE WHEN dv.entity_type = 'products' THEN dv.timestamp END), '1970-01-01'), COALESCE(MAX(CASE WHEN dv.entity_type = 'customers' THEN dv.timestamp END), '1970-01-01'), COALESCE(MAX(CASE WHEN dv.entity_type = 'inventories' THEN dv.timestamp END), '1970-01-01'))))::integer AS days_since_critical_update FROM organizations o LEFT JOIN data_versions dv ON dv.organization_id = o.id AND dv.entity_type IN ('products', 'customers', 'inventories') GROUP BY o.shortname""",
}

if __name__ == "__main__":
    os.makedirs(CACHE_DIR, exist_ok=True)
    print("Postgres Cache Prefetch Queries")
    print("Run each query below via MCP (user-supercat-postgres-vpn execute_sql)")
    print("=" * 60)
    for key, sql in QUERIES.items():
        csv_path = os.path.join(CACHE_DIR, f"{key}.csv")
        if os.path.exists(csv_path):
            print(f"[SKIP] {key}.csv already exists")
            continue
        print(f"\n--- {key} ---")
        print(f"SQL: {sql[:100]}...")
        print(f"Save result to: {csv_path}")
