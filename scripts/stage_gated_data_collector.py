#!/usr/bin/env python3
"""
Stage-Gated Data Collection Script
Collects quantitative TRUE/FALSE metrics from PostgreSQL and BigQuery for onboarding clients
"""

import sys
import os
import json
import psycopg2
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from google.cloud import bigquery
from google.oauth2 import service_account

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

class StageGatedDataCollector:
    """Collects all quantitative metrics for stage-gated onboarding assessment"""
    
    def __init__(self, org_shortnames: List[str]):
        """
        Initialize the collector
        
        Args:
            org_shortnames: List of organization shortnames to assess
        """
        self.org_shortnames = org_shortnames
        self.results = {}
        
        # PostgreSQL connection (from environment or config)
        self.pg_conn = None
        
        # BigQuery client
        credentials_path = os.path.join(parent_dir, 'integrations', 'bigquery', 'service-account', 
                                       'supercat-data-pipeline-dbfab43c27bb.json')
        credentials = service_account.Credentials.from_service_account_file(credentials_path)
        self.bq_client = bigquery.Client(credentials=credentials, project='supercat-data-pipeline')
        
    def connect_postgres(self):
        """Connect to PostgreSQL database using DATABASE_URL or PG* env vars"""
        print("📊 Connecting to PostgreSQL...")
        db_url = os.environ.get('DATABASE_URL')
        if db_url:
            self.pg_conn = psycopg2.connect(db_url)
        else:
            self.pg_conn = psycopg2.connect(
                host=os.environ.get('PGHOST', 'localhost'),
                port=os.environ.get('PGPORT', '5432'),
                dbname=os.environ.get('PGDATABASE', 'supercat_production'),
                user=os.environ.get('PGUSER', 'postgres'),
                password=os.environ.get('PGPASSWORD', ''),
            )
        self.pg_conn.set_session(readonly=True, autocommit=True)
        print("  ✓ PostgreSQL connected")
        
    def close(self):
        """Close database connections"""
        if self.pg_conn:
            self.pg_conn.close()
            self.pg_conn = None
    
    def collect_all_data(self) -> Dict[str, Any]:
        """
        Collect all data for all organizations
        
        Returns:
            Dictionary with all collected metrics per organization
        """
        self.connect_postgres()
        for shortname in self.org_shortnames:
            print(f"\n{'='*60}")
            print(f"Collecting data for: {shortname.upper()}")
            print(f"{'='*60}\n")
            
            org_data = {
                'shortname': shortname,
                'collection_date': datetime.now().isoformat(),
                'organization_info': self._get_organization_info(shortname),
                'product_metrics': self._get_product_metrics(shortname),
                'customer_metrics': self._get_customer_metrics(shortname),
                'user_metrics': self._get_user_metrics(shortname),
                'price_levels': self._get_price_levels(shortname),
                'options': self._get_options_count(shortname),
                'territories': self._get_territories(shortname),
                'orders': self._get_orders(shortname),
                'inventories': self._get_inventories(shortname),
                'import_events': self._get_import_events(shortname),
                'mobile_sites': self._get_mobile_sites(shortname),
                'report_formats': self._get_report_formats(shortname),
                'user_types': self._get_user_types(shortname),
                'ipad_activity': self._get_ipad_activity_bigquery(shortname),
            }
            
            self.results[shortname] = org_data
            
        return self.results
    
    def _execute_sql(self, query: str, params: tuple = None) -> List[Dict]:
        """Execute SQL query and return results as list of dicts"""
        if self.pg_conn is None:
            self.connect_postgres()
        cur = self.pg_conn.cursor()
        try:
            cur.execute(query, params)
            columns = [desc[0] for desc in cur.description]
            return [dict(zip(columns, row)) for row in cur.fetchall()]
        finally:
            cur.close()
    
    def _get_organization_info(self, shortname: str) -> Dict:
        """Get basic organization information"""
        print(f"  📋 Organization info...")
        rows = self._execute_sql(
            "SELECT id, name, shortname, created_at, order_email_recipient FROM organizations WHERE shortname = %s",
            (shortname,)
        )
        return rows[0] if rows else {}
    
    def _get_product_metrics(self, shortname: str) -> Dict:
        """Get product-related metrics"""
        print(f"  📦 Product metrics...")
        rows = self._execute_sql("""
            SELECT 
                COUNT(*) as total_products,
                COUNT(CASE WHEN image_exists = true THEN 1 END) as products_with_images,
                COUNT(DISTINCT category_code) as categories_count,
                COUNT(DISTINCT collection_code) as collections_count,
                MAX(last_modified_at) as last_product_update
            FROM products p
            JOIN organizations o ON p.organization_id = o.id
            WHERE o.shortname = %s AND p.deleted = false
            """, (shortname,))
        return rows[0] if rows else {}
    
    def _get_customer_metrics(self, shortname: str) -> Dict:
        """Get customer-related metrics"""
        print(f"  👥 Customer metrics...")
        rows = self._execute_sql("""
            SELECT 
                COUNT(*) as total_customers,
                MAX(updated_at) as last_customer_update
            FROM customers c
            JOIN organizations o ON c.organization_id = o.id
            WHERE o.shortname = %s
            """, (shortname,))
        return rows[0] if rows else {}
    
    def _get_user_metrics(self, shortname: str) -> Dict:
        """Get user-related metrics"""
        print(f"  🔐 User metrics...")
        rows = self._execute_sql("""
            SELECT 
                COUNT(*) as total_users,
                COUNT(CASE WHEN is_admin = true THEN 1 END) as admin_users,
                COUNT(CASE WHEN is_admin = false THEN 1 END) as non_admin_users
            FROM org_users ou
            JOIN organizations o ON ou.organization_id = o.id
            JOIN users u ON ou.user_id = u.id
            WHERE o.shortname = %s
            AND u.email NOT IN ('kylor@supercat.io', 'brent@supercat.io', 'cwiebe@supercat.io')
            """, (shortname,))
        return rows[0] if rows else {}
    
    def _get_price_levels(self, shortname: str) -> Dict:
        """Get price level information"""
        print(f"  💰 Price levels...")
        rows = self._execute_sql("""
            SELECT code, name
            FROM price_levels pl
            JOIN organizations o ON pl.organization_id = o.id
            WHERE o.shortname = %s
            ORDER BY code
            """, (shortname,))
        return {'price_levels': rows, 'count': len(rows)}
    
    def _get_options_count(self, shortname: str) -> Dict:
        """Get options count (CRITICAL: count records, not schema columns)"""
        print(f"  ⚙️  Options...")
        rows = self._execute_sql("""
            SELECT COUNT(*) as options_count
            FROM options opt
            JOIN organizations o ON opt.organization_id = o.id
            WHERE o.shortname = %s
            """, (shortname,))
        return rows[0] if rows else {}
    
    def _get_territories(self, shortname: str) -> Dict:
        """Get territory configuration"""
        print(f"  🗺️  Territories...")
        rows = self._execute_sql("""
            SELECT COUNT(*) as territory_count
            FROM territories t
            JOIN organizations o ON t.organization_id = o.id
            WHERE o.shortname = %s
            """, (shortname,))
        return rows[0] if rows else {}
    
    def _get_orders(self, shortname: str) -> Dict:
        """Get order count"""
        print(f"  📝 Orders...")
        rows = self._execute_sql("""
            SELECT COUNT(*) as order_count
            FROM orders ord
            JOIN organizations o ON ord.organization_id = o.id
            WHERE o.shortname = %s
            """, (shortname,))
        return rows[0] if rows else {}
    
    def _get_inventories(self, shortname: str) -> Dict:
        """Get inventory data"""
        print(f"  📊 Inventories...")
        rows = self._execute_sql("""
            SELECT 
                COUNT(*) as inventory_count,
                MAX(updated_at) as last_inventory_update
            FROM inventories inv
            JOIN organizations o ON inv.organization_id = o.id
            WHERE o.shortname = %s
            """, (shortname,))
        return rows[0] if rows else {}
    
    def _get_import_events(self, shortname: str) -> Dict:
        """Get recent import events"""
        print(f"  🔄 Import events...")
        rows = self._execute_sql("""
            SELECT 
                COUNT(CASE WHEN status = 'error' THEN 1 END) as error_count,
                COUNT(*) as total_imports
            FROM import_events ie
            JOIN organizations o ON ie.organization_id = o.id
            WHERE o.shortname = %s
            AND ie.created_at > NOW() - INTERVAL '30 days'
            """, (shortname,))
        return rows[0] if rows else {}
    
    def _get_mobile_sites(self, shortname: str) -> Dict:
        """Get eCat Online site configuration"""
        print(f"  🌐 Mobile sites...")
        rows = self._execute_sql("""
            SELECT enabled, public_enabled
            FROM mobile_sites ms
            JOIN organizations o ON ms.organization_id = o.id
            WHERE o.shortname = %s
            """, (shortname,))
        return rows[0] if rows else {}
    
    def _get_report_formats(self, shortname: str) -> Dict:
        """Get report format count"""
        print(f"  📄 Report formats...")
        rows = self._execute_sql("""
            SELECT COUNT(*) as report_format_count
            FROM ipad_reports ir
            JOIN organizations o ON ir.organization_id = o.id
            WHERE o.shortname = %s
            """, (shortname,))
        return rows[0] if rows else {}
    
    def _get_user_types(self, shortname: str) -> Dict:
        """Get user types"""
        print(f"  👤 User types...")
        rows = self._execute_sql("""
            SELECT name
            FROM user_types ut
            JOIN organizations o ON ut.organization_id = o.id
            WHERE o.shortname = %s
            ORDER BY name
            """, (shortname,))
        return {'user_types': [r['name'] for r in rows], 'count': len(rows)}
    
    def _get_ipad_activity_bigquery(self, shortname: str) -> Dict:
        """Query BigQuery for iPad activity from MixPanel"""
        print(f"  📱 iPad activity (BigQuery)...")
        
        query = f"""
        SELECT 
            COUNT(*) as ipad_order_count,
            COUNT(DISTINCT distinct_id) as unique_ipad_users,
            MAX(time) as last_ipad_order
        FROM `supercat-data-pipeline.hevo_dataset_supercat_data_pipeline_Slhk.mixpanel_order_submitted`
        WHERE currentorganizationshortname = '{shortname}'
        AND mp_lib = 'iphone'
        """
        
        try:
            query_job = self.bq_client.query(query)
            results = query_job.result()
            
            for row in results:
                return {
                    'ipad_order_count': row.ipad_order_count,
                    'unique_ipad_users': row.unique_ipad_users,
                    'last_ipad_order': row.last_ipad_order.isoformat() if row.last_ipad_order else None
                }
        except Exception as e:
            return {
                'error': str(e),
                'ipad_order_count': '❓ QUERY FAILED',
                'unique_ipad_users': '❓ QUERY FAILED',
                'last_ipad_order': '❓ QUERY FAILED'
            }
        
        return {}
    
    def generate_markdown_report(self) -> str:
        """Generate markdown report from collected data"""
        report = []
        report.append("# Stage-Gated Data Collection Results\n")
        report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report.append(f"**Organizations Assessed:** {', '.join([s.upper() for s in self.org_shortnames])}\n")
        report.append("\n---\n")
        
        for shortname, data in self.results.items():
            report.append(f"\n## CLIENT: {shortname.upper()}\n")
            report.append(f"**Collection Date:** {data['collection_date']}\n")
            
            for section, section_data in data.items():
                if section in ('shortname', 'collection_date'):
                    continue
                if not isinstance(section_data, dict):
                    continue
                report.append(f"\n### {section.replace('_', ' ').title()}\n")
                for key, val in section_data.items():
                    if isinstance(val, list):
                        report.append(f"- **{key}:** {', '.join(str(v) for v in val)}\n")
                    else:
                        report.append(f"- **{key}:** {val}\n")
            
            report.append("\n---\n")
        
        return ''.join(report)


def main():
    """Main execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Stage-Gated Data Collection')
    parser.add_argument('--orgs', nargs='+', required=True, 
                       help='Organization shortnames (e.g., pebl mali tcd)')
    
    args = parser.parse_args()
    
    collector = StageGatedDataCollector(args.orgs)
    try:
        collector.collect_all_data()
    finally:
        collector.close()
    
    report = collector.generate_markdown_report()
    
    # Save to file
    output_file = f"stage_gated_data_collection_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    output_path = os.path.join(parent_dir, 'reports', output_file)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(report)
    
    print(f"\n✅ Report saved to: {output_path}")
    print(report)


if __name__ == '__main__':
    main()
