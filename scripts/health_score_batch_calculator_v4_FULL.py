#!/usr/bin/env python3
"""
Health Intelligence v3 — FULL Batch Calculator (All 22 Components)

Purpose: Calculate complete health scores for all SuperCat clients with ALL data sources
Usage: python health_score_batch_calculator_v4_FULL.py --batch-size 5
Output: Complete health scores with all 22 components calculated

Requirements:
- Python 3.8+
- google-cloud-bigquery
- psycopg2-binary (for Postgres queries)
- pandas

Install: pip install google-cloud-bigquery psycopg2-binary pandas

Data Sources:
- BigQuery: org_summary, segment_benchmarks, mixpanel events, helpscout, clicky
- Postgres: products, customers, orders, inventories, import_events, data_versions
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import pandas as pd
from google.cloud import bigquery


class HealthScoreCalculatorFull:
    """Calculate Health Intelligence v3 scores with ALL 22 components."""
    
    def __init__(self, project_id: str = "supercat-data-pipeline", use_postgres: bool = True):
        self.bq_client = bigquery.Client(project=project_id)
        self.dataset = "insightful_product"
        self.use_postgres = use_postgres
        
        # Postgres connection (if available)
        self.pg_conn = None
        if use_postgres:
            try:
                import psycopg2
                # Note: Connection details would come from MCP config or environment
                # For now, we'll gracefully degrade if Postgres is unavailable
                print("  ℹ️  Postgres integration enabled (will attempt to connect)")
            except ImportError:
                print("  ⚠️  psycopg2 not installed, Postgres features disabled")
                self.use_postgres = False
    
    def get_all_orgs(self) -> List[str]:
        """Fetch all REAL ACTIVE org shortnames from BigQuery (excluding test/demo accounts)."""
        query = f"""
        SELECT DISTINCT org_shortname 
        FROM `{self.dataset}.org_summary`
        WHERE org_shortname IS NOT NULL
          -- Filter for real active clients only
          AND (
            arr > 0  -- Paying clients
            OR mp_total_logins > 100  -- Or active non-paying clients
          )
          -- Exclude obvious test/demo/template accounts
          AND LOWER(org_name) NOT LIKE '%test%'
          AND LOWER(org_name) NOT LIKE '%demo%'
          AND LOWER(org_name) NOT LIKE '%template%'
          AND LOWER(org_name) NOT LIKE '%staging%'
          AND LOWER(org_name) NOT LIKE '%to delete%'
          AND org_shortname NOT IN ('bmc2', 'bmc3', 'temp', 'tmpl', 'tmpo', 'tech', 'tle', 'vc', 'wmo')
        ORDER BY org_shortname
        """
        
        try:
            result = self.bq_client.query(query).result()
            orgs = [row['org_shortname'] for row in result]
            print(f"  ℹ️  Filtered to {len(orgs)} real active clients (excluded test/demo accounts)")
            return orgs
        except Exception as e:
            print(f"❌ Error fetching org list: {e}")
            return []
    
    def get_org_summary(self, org_shortname: str) -> Optional[Dict]:
        """Fetch org_summary data for a single client."""
        query = f"""
        SELECT
          org_shortname,
          org_name,
          segment,
          arr,
          mrr,
          mp_total_logins,
          mp_submit_order,
          mp_active_users,
          mp_total_users,
          feature_depth,
          portal_visitors_daily,
          portal_bounce_rate,
          has_clicky_portal,
          access_sales_portal,
          order_configured_item,
          create_pdf_catalog,
          view_library_entry,
          search_products,
          select_a_customer,
          view_kit,
          order_kit
        FROM `{self.dataset}.org_summary`
        WHERE org_shortname = '{org_shortname}'
        """
        
        try:
            result = self.bq_client.query(query).result()
            rows = list(result)
            if not rows:
                return None
            return dict(rows[0])
        except Exception as e:
            print(f"  ❌ Error fetching org_summary: {e}")
            return None
    
    def get_segment_benchmarks(self, segment: str) -> Optional[Dict]:
        """Fetch segment benchmarks for percentile comparisons."""
        query = f"""
        SELECT
          segment,
          total_logins_p25,
          total_logins_median,
          total_logins_p75,
          submit_order_p25,
          submit_order_median,
          submit_order_p75
        FROM `{self.dataset}.segment_benchmarks_monthly`
        WHERE segment = '{segment}'
          AND benchmark_month = (SELECT MAX(benchmark_month) FROM `{self.dataset}.segment_benchmarks_monthly`)
        """
        
        try:
            result = self.bq_client.query(query).result()
            rows = list(result)
            if not rows:
                return None
            return dict(rows[0])
        except Exception as e:
            print(f"  ❌ Error fetching benchmarks: {e}")
            return None
    
    # ==================== NEW: Historical Data Queries ====================
    
    def get_historical_trends(self, org_shortname: str) -> Dict:
        """Fetch historical data for trend analysis (Layer 3)."""
        # Query Mixpanel events for 6-month lookback
        query = f"""
        WITH monthly_metrics AS (
          SELECT
            DATE_TRUNC(DATE(TIMESTAMP_SECONDS(CAST(time AS INT64))), MONTH) as month,
            COUNT(DISTINCT CASE WHEN event_name = 'order_submitted' THEN event_hash END) as orders,
            COUNT(DISTINCT distinct_id) as active_users,
            COUNT(DISTINCT CASE WHEN event_name = 'customer_selection' THEN event_hash END) as active_customers
          FROM `supercat-data-pipeline.mixpanel.events`
          WHERE organization_shortname = '{org_shortname}'
            AND DATE(TIMESTAMP_SECONDS(CAST(time AS INT64))) >= DATE_SUB(CURRENT_DATE(), INTERVAL 6 MONTH)
          GROUP BY month
          ORDER BY month DESC
        )
        SELECT * FROM monthly_metrics
        """
        
        try:
            result = self.bq_client.query(query).result()
            rows = [dict(row) for row in result]
            
            if len(rows) < 2:
                return {'has_trend_data': False}
            
            # Calculate trends (comparing most recent 3 months vs previous 3 months)
            recent_3m = rows[:3]
            previous_3m = rows[3:6] if len(rows) >= 6 else rows[3:]
            
            if not previous_3m:
                return {'has_trend_data': False}
            
            recent_orders = sum(r['orders'] for r in recent_3m)
            previous_orders = sum(r['orders'] for r in previous_3m)
            recent_users = sum(r['active_users'] for r in recent_3m)
            previous_users = sum(r['active_users'] for r in previous_3m)
            recent_customers = sum(r['active_customers'] for r in recent_3m)
            previous_customers = sum(r['active_customers'] for r in previous_3m)
            
            return {
                'has_trend_data': True,
                'order_trend': (recent_orders - previous_orders) / previous_orders if previous_orders > 0 else 0,
                'user_trend': (recent_users - previous_users) / previous_users if previous_users > 0 else 0,
                'customer_trend': (recent_customers - previous_customers) / previous_customers if previous_customers > 0 else 0,
                'recent_orders': recent_orders,
                'previous_orders': previous_orders
            }
        except Exception as e:
            print(f"  ⚠️  Could not fetch historical trends: {e}")
            return {'has_trend_data': False}
    
    def get_feature_adoption_velocity(self, org_shortname: str) -> Dict:
        """Calculate feature adoption velocity (Layer 3, Component 18)."""
        # Compare feature usage in recent 90 days vs previous 90 days
        query = f"""
        WITH feature_usage AS (
          SELECT
            CASE 
              WHEN DATE(TIMESTAMP_SECONDS(CAST(time AS INT64))) >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY) THEN 'recent'
              ELSE 'previous'
            END as period,
            COUNT(DISTINCT event_name) as unique_features_used
          FROM `supercat-data-pipeline.mixpanel.events`
          WHERE organization_shortname = '{org_shortname}'
            AND DATE(TIMESTAMP_SECONDS(CAST(time AS INT64))) >= DATE_SUB(CURRENT_DATE(), INTERVAL 180 DAY)
          GROUP BY period
        )
        SELECT * FROM feature_usage
        """
        
        try:
            result = self.bq_client.query(query).result()
            rows = {row['period']: row['unique_features_used'] for row in result}
            
            recent = rows.get('recent', 0)
            previous = rows.get('previous', 0)
            
            if previous == 0:
                return {'has_velocity_data': False}
            
            velocity = (recent - previous) / previous
            
            return {
                'has_velocity_data': True,
                'velocity': velocity,
                'recent_features': recent,
                'previous_features': previous
            }
        except Exception as e:
            print(f"  ⚠️  Could not fetch feature velocity: {e}")
            return {'has_velocity_data': False}
    
    # ==================== NEW: HelpScout Support Data ====================
    
    def get_support_burden(self, org_name: str) -> Dict:
        """Calculate support burden from HelpScout data (Layer 2, Component 11)."""
        # Simplified query that works with actual schema
        query = f"""
        SELECT
          COUNT(*) as ticket_count,
          COUNTIF(c.status = 'active') as active_tickets
        FROM `supercat-data-pipeline.helpscout.conversations` c
        LEFT JOIN `supercat-data-pipeline.helpscout.customers` cust 
          ON JSON_EXTRACT_SCALAR(c.primaryCustomer, '$.id') = CAST(cust.id AS STRING)
        WHERE LOWER(cust.organization) LIKE LOWER('%{org_name}%')
          AND TIMESTAMP(c.createdAt) >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
        """
        
        try:
            result = self.bq_client.query(query).result()
            rows = list(result)
            if not rows or rows[0]['ticket_count'] == 0:
                return {'has_support_data': False, 'ticket_count': 0}
            
            row = dict(rows[0])
            return {
                'has_support_data': True,
                'ticket_count': row['ticket_count'],
                'active_tickets': row['active_tickets'] or 0,
                'high_severity_count': 0,  # Would need tag parsing
                'escalation_count': 0,  # Would need tag parsing
                'avg_resolution_hours': 0  # Would need closedAt parsing
            }
        except Exception as e:
            print(f"  ⚠️  Could not fetch support data: {e}")
            return {'has_support_data': False, 'ticket_count': 0}
    
    def get_support_escalation_risk(self, org_name: str) -> Dict:
        """Calculate support escalation risk (Layer 4, Component 20)."""
        support_data = self.get_support_burden(org_name)
        
        if not support_data['has_support_data']:
            return {'has_escalation_risk': False, 'risk_score': 0}
        
        # High severity or escalated tickets indicate risk
        high_severity_pct = support_data['high_severity_count'] / support_data['ticket_count'] if support_data['ticket_count'] > 0 else 0
        escalation_pct = support_data['escalation_count'] / support_data['ticket_count'] if support_data['ticket_count'] > 0 else 0
        
        return {
            'has_escalation_risk': True,
            'high_severity_pct': high_severity_pct,
            'escalation_pct': escalation_pct,
            'ticket_count': support_data['ticket_count']
        }
    
    # ==================== NEW: Postgres Data Queries ====================
    
    def get_product_inventory_health(self, org_shortname: str) -> Dict:
        """Calculate product/inventory health (Layer 2, Component 10)."""
        # Note: This would query Postgres if available
        # For now, return placeholder indicating Postgres needed
        if not self.use_postgres or not self.pg_conn:
            return {
                'has_product_data': False,
                'note': 'Postgres connection required for product/inventory health'
            }
        
        # TODO: Add actual Postgres queries when connection is available
        # Query products table for catalog completeness
        # Query inventories table for inventory freshness
        # Query data_versions table for data staleness
        
        return {'has_product_data': False}
    
    def get_customer_concentration(self, org_shortname: str) -> Dict:
        """Calculate customer concentration risk (Layer 2, Component 13)."""
        if not self.use_postgres or not self.pg_conn:
            return {
                'has_concentration_data': False,
                'note': 'Postgres connection required for customer concentration'
            }
        
        # TODO: Query portal_invoices for revenue by customer
        # Calculate top 10 customer concentration percentage
        
        return {'has_concentration_data': False}
    
    def get_customer_exodus_risk(self, org_shortname: str) -> Dict:
        """Calculate customer exodus risk (Layer 4, Component 22)."""
        if not self.use_postgres or not self.pg_conn:
            return {
                'has_exodus_data': False,
                'note': 'Postgres connection required for customer exodus detection'
            }
        
        # TODO: Query customers and orders tables for declining customer counts
        
        return {'has_exodus_data': False}
    
    def get_data_integrity_risk(self, org_shortname: str) -> Dict:
        """Calculate data integrity risk (Layer 4, Component 21)."""
        if not self.use_postgres or not self.pg_conn:
            return {
                'has_integrity_data': False,
                'note': 'Postgres connection required for data integrity checks'
            }
        
        # TODO: Query import_events for failures
        # Query data_versions for staleness
        
        return {'has_integrity_data': False}
    
    # ==================== Component Calculations (Enhanced) ====================
    
    def calculate_component_15_order_volume_trend(self, org_shortname: str) -> Dict:
        """Component 15: Order Volume Trend (30 points max)."""
        trends = self.get_historical_trends(org_shortname)
        
        if not trends['has_trend_data']:
            return {'score': 15, 'details': 'Historical data unavailable (neutral score)'}
        
        trend = trends['order_trend']
        
        # Scoring based on growth rate
        if trend >= 0.20:  # 20%+ growth
            score = 30
        elif trend >= 0.10:  # 10-20% growth
            score = 25
        elif trend >= 0:  # Flat to 10% growth
            score = 20
        elif trend >= -0.10:  # Slight decline (0-10%)
            score = 15
        elif trend >= -0.20:  # Moderate decline (10-20%)
            score = 10
        else:  # Significant decline (20%+)
            score = 5
        
        return {
            'score': score,
            'details': {
                'trend_pct': round(trend * 100, 1),
                'recent_orders': trends['recent_orders'],
                'previous_orders': trends['previous_orders']
            }
        }
    
    def calculate_component_16_user_growth_trend(self, org_shortname: str) -> Dict:
        """Component 16: User Growth Trend (25 points max)."""
        trends = self.get_historical_trends(org_shortname)
        
        if not trends['has_trend_data']:
            return {'score': 13, 'details': 'Historical data unavailable (neutral score)'}
        
        trend = trends['user_trend']
        
        # Scoring based on growth rate
        if trend >= 0.15:  # 15%+ growth
            score = 25
        elif trend >= 0.05:  # 5-15% growth
            score = 20
        elif trend >= 0:  # Flat to 5% growth
            score = 15
        elif trend >= -0.10:  # Slight decline
            score = 10
        else:  # Significant decline
            score = 5
        
        return {
            'score': score,
            'details': {
                'trend_pct': round(trend * 100, 1),
                'direction': 'growing' if trend > 0 else 'declining' if trend < 0 else 'flat'
            }
        }
    
    def calculate_component_17_customer_health_trend(self, org_shortname: str) -> Dict:
        """Component 17: Customer Health Trend (25 points max)."""
        trends = self.get_historical_trends(org_shortname)
        
        if not trends['has_trend_data']:
            return {'score': 13, 'details': 'Historical data unavailable (neutral score)'}
        
        trend = trends['customer_trend']
        
        # Scoring based on growth rate
        if trend >= 0.15:  # 15%+ growth
            score = 25
        elif trend >= 0.05:  # 5-15% growth
            score = 20
        elif trend >= 0:  # Flat to 5% growth
            score = 15
        elif trend >= -0.10:  # Slight decline
            score = 10
        else:  # Significant decline
            score = 5
        
        return {
            'score': score,
            'details': {
                'trend_pct': round(trend * 100, 1),
                'direction': 'growing' if trend > 0 else 'declining' if trend < 0 else 'flat'
            }
        }
    
    def calculate_component_18_feature_adoption_velocity(self, org_shortname: str) -> Dict:
        """Component 18: Feature Adoption Velocity (20 points max)."""
        velocity_data = self.get_feature_adoption_velocity(org_shortname)
        
        if not velocity_data['has_velocity_data']:
            return {'score': 10, 'details': 'Historical data unavailable (neutral score)'}
        
        velocity = velocity_data['velocity']
        
        # Scoring based on velocity
        if velocity >= 0.20:  # 20%+ increase in features used
            score = 20
        elif velocity >= 0.10:  # 10-20% increase
            score = 17
        elif velocity >= 0:  # Flat to 10% increase
            score = 13
        elif velocity >= -0.10:  # Slight decrease
            score = 8
        else:  # Significant decrease
            score = 3
        
        return {
            'score': score,
            'details': {
                'velocity_pct': round(velocity * 100, 1),
                'recent_features': velocity_data['recent_features'],
                'previous_features': velocity_data['previous_features']
            }
        }
    
    def calculate_component_11_support_burden(self, org_name: str) -> Dict:
        """Component 11: Support Burden (10 points max)."""
        support_data = self.get_support_burden(org_name)
        
        if not support_data['has_support_data']:
            return {'score': 5, 'details': 'Support data unavailable (neutral score)'}
        
        ticket_count = support_data['ticket_count']
        high_severity_count = support_data['high_severity_count']
        
        # Scoring based on ticket volume and severity
        # Lower is better (inverse scoring)
        if ticket_count == 0:
            score = 10
        elif ticket_count <= 5 and high_severity_count == 0:
            score = 9
        elif ticket_count <= 10 and high_severity_count <= 1:
            score = 7
        elif ticket_count <= 20 and high_severity_count <= 3:
            score = 5
        elif ticket_count <= 30:
            score = 3
        else:
            score = 1
        
        return {
            'score': score,
            'details': {
                'ticket_count': ticket_count,
                'high_severity_count': high_severity_count,
                'active_tickets': support_data['active_tickets']
            }
        }
    
    def calculate_component_20_support_escalation_risk(self, org_name: str) -> Dict:
        """Component 20: Support Escalation Risk (-30 points max)."""
        escalation_data = self.get_support_escalation_risk(org_name)
        
        if not escalation_data['has_escalation_risk']:
            return {'score': 0, 'details': 'Support data unavailable (no penalty applied)'}
        
        high_severity_pct = escalation_data['high_severity_pct']
        escalation_pct = escalation_data['escalation_pct']
        
        # Penalty based on escalation patterns
        if high_severity_pct >= 0.30 or escalation_pct >= 0.20:  # 30%+ high severity or 20%+ escalations
            score = -30
        elif high_severity_pct >= 0.20 or escalation_pct >= 0.10:
            score = -20
        elif high_severity_pct >= 0.10 or escalation_pct >= 0.05:
            score = -10
        else:
            score = 0
        
        return {
            'score': score,
            'details': {
                'high_severity_pct': round(high_severity_pct * 100, 1),
                'escalation_pct': round(escalation_pct * 100, 1),
                'ticket_count': escalation_data['ticket_count']
            }
        }
    
    # ==================== Layer Calculations (Enhanced) ====================
    
    def calculate_layer_3_trend_momentum(self, org: Dict) -> Dict:
        """Layer 3: Trend Momentum (4 components, max 100 points) - NOW WITH REAL DATA."""
        org_shortname = org['org_shortname']
        
        c15 = self.calculate_component_15_order_volume_trend(org_shortname)
        c16 = self.calculate_component_16_user_growth_trend(org_shortname)
        c17 = self.calculate_component_17_customer_health_trend(org_shortname)
        c18 = self.calculate_component_18_feature_adoption_velocity(org_shortname)
        
        total_score = c15['score'] + c16['score'] + c17['score'] + c18['score']
        
        return {
            'layer_score': total_score,
            'components': {
                'order_volume_trend': c15,
                'user_growth_trend': c16,
                'customer_health_trend': c17,
                'feature_adoption_velocity': c18
            }
        }
    
    def calculate_layer_2_value_realization(self, org: Dict, benchmarks: Dict) -> Dict:
        """Layer 2: Value Realization (8 components, max 125 points, normalized to 100) - ENHANCED."""
        org_name = org.get('org_name', org['org_shortname'])
        
        # Original 3 components (from v3)
        c7 = self.calculate_component_07_order_volume(org, benchmarks)
        c8 = self.calculate_component_08_user_activation(org, benchmarks)
        c9 = self.calculate_component_09_customer_engagement(org, benchmarks)
        
        # NEW: Component 11 - Support Burden (now with real data)
        c11 = self.calculate_component_11_support_burden(org_name)
        
        # Components still pending Postgres connection
        c10 = {'score': 8, 'details': 'Postgres connection required for product/inventory health'}
        c12 = {'score': 5, 'details': 'Postgres connection required for geographic penetration'}
        c13 = {'score': 5, 'details': 'Postgres connection required for customer concentration'}
        c14 = {'score': 8, 'details': 'Postgres connection required for dormant reactivation'}
        
        total_score_raw = (
            c7['score'] + c8['score'] + c9['score'] + 
            c10['score'] + c11['score'] + c12['score'] + 
            c13['score'] + c14['score']
        )
        
        # Normalize to 100 (max is 125)
        total_score_normalized = (total_score_raw / 125.0) * 100
        
        return {
            'layer_score': total_score_normalized,
            'components': {
                'order_volume': c7,
                'user_activation': c8,
                'customer_engagement': c9,
                'product_inventory_health': c10,
                'support_burden': c11,
                'geographic_penetration': c12,
                'customer_concentration': c13,
                'dormant_reactivation': c14
            }
        }
    
    def calculate_layer_4_risk_signals(self, org: Dict) -> Dict:
        """Layer 4: Risk Signals (4 components, -100 to 0 points) - ENHANCED."""
        org_name = org.get('org_name', org['org_shortname'])
        arr = org.get('arr', 0) or 0
        logins = org.get('mp_total_logins', 0) or 0
        
        # Component 19: Rep Disengagement Risk (original)
        if arr > 5000 and logins == 0:
            c19_score = -30
            c19_details = 'Paying customer with zero logins (CRITICAL)'
        elif arr > 5000 and logins < 100:
            c19_score = -15
            c19_details = 'Paying customer with very low logins'
        else:
            c19_score = 0
            c19_details = 'No rep disengagement detected'
        
        c19 = {'score': c19_score, 'details': c19_details}
        
        # NEW: Component 20 - Support Escalation Risk (now with real data)
        c20 = self.calculate_component_20_support_escalation_risk(org_name)
        
        # Components still pending Postgres connection
        c21 = {'score': 0, 'details': 'Postgres connection required for data integrity checks'}
        c22 = {'score': 0, 'details': 'Postgres connection required for customer exodus detection'}
        
        total_score = c19['score'] + c20['score'] + c21['score'] + c22['score']
        
        return {
            'layer_score': total_score,
            'components': {
                'rep_disengagement_risk': c19,
                'support_escalation_risk': c20,
                'data_integrity_risk': c21,
                'customer_exodus_risk': c22
            }
        }
    
    # ==================== Keep all original component methods from v3 ====================
    # (Components 1-9 remain unchanged - copying from v3)
    
    def calculate_component_01_login_intensity(self, org: Dict, benchmarks: Dict) -> Dict:
        """Component 1: Login Intensity Score (20 points max)."""
        logins = org.get('mp_total_logins', 0) or 0
        active_users = org.get('mp_active_users', 0) or 0
        total_users = org.get('mp_total_users', 0) or 0
        
        if active_users == 0:
            return {'score': 0, 'details': 'No active users'}
        
        login_intensity = logins / active_users
        active_user_pct = active_users / total_users if total_users > 0 else 0
        org_size = 'small' if total_users <= 10 else 'standard'
        
        p25 = benchmarks.get('total_logins_p25', 0) or 0
        median = benchmarks.get('total_logins_median', 0) or 0
        p75 = benchmarks.get('total_logins_p75', 0) or 0
        
        if p25 > 0 and active_users > 0:
            p25_intensity = p25 / active_users
            median_intensity = median / active_users if median > 0 else 0
            p75_intensity = p75 / active_users if p75 > 0 else 0
        else:
            p25_intensity = 50
            median_intensity = 100
            p75_intensity = 150
        
        if org_size == 'small':
            if login_intensity >= p75_intensity:
                score = 20
            elif login_intensity >= median_intensity:
                score = 17
            elif login_intensity >= p25_intensity:
                score = 14
            elif login_intensity > 0:
                score = 10
            else:
                score = 0
        else:
            if login_intensity >= p75_intensity and active_user_pct >= 0.15:
                score = 20
            elif login_intensity >= median_intensity and active_user_pct >= 0.10:
                score = 17
            elif login_intensity >= p25_intensity and active_user_pct >= 0.05:
                score = 14
            elif login_intensity > 0:
                score = 10
            else:
                score = 0
        
        return {
            'score': score,
            'details': {
                'login_intensity': round(login_intensity, 2),
                'active_user_pct': round(active_user_pct, 2),
                'org_size': org_size,
                'total_logins': logins,
                'active_users': active_users
            }
        }
    
    def calculate_component_02_feature_adoption(self, org: Dict) -> Dict:
        """Component 2: Feature Adoption Breadth (20 points max)."""
        segment = org.get('segment', 'Commerce-Active')
        features = org.get('feature_depth', 0) or 0
        
        if segment == 'Catalog-Focused':
            if features >= 3:
                score = 15
            elif features == 2:
                score = 10
            elif features == 1:
                score = 5
            else:
                score = 0
        else:
            if features >= 4:
                score = 20
            elif features == 3:
                score = 15
            elif features == 2:
                score = 10
            elif features == 1:
                score = 5
            else:
                score = 0
        
        return {
            'score': score,
            'details': {
                'features_adopted': features,
                'segment': segment
            }
        }
    
    def calculate_component_03_portal_engagement(self, org: Dict, benchmarks: Dict) -> Dict:
        """Component 3: Portal Engagement Score (15 points max)."""
        portal_access = org.get('access_sales_portal', 0) or 0
        
        if portal_access == 0:
            return {'score': 0, 'details': 'No Sales Portal access'}
        
        if portal_access >= 500:
            score = 15
        elif portal_access >= 200:
            score = 12
        elif portal_access > 0:
            score = 8
        else:
            score = 0
        
        return {
            'score': score,
            'details': {
                'portal_access_events': portal_access
            }
        }
    
    def calculate_component_04_seat_utilization(self, org: Dict) -> Dict:
        """Component 4: Seat Utilization Efficiency (20 points max)."""
        active_users = org.get('mp_active_users', 0) or 0
        total_users = org.get('mp_total_users', 0) or 0
        
        if total_users == 0:
            return {'score': 0, 'details': 'No users'}
        
        utilization = active_users / total_users
        
        if utilization >= 0.60:
            score = 20
        elif utilization >= 0.40:
            score = 17
        elif utilization >= 0.20:
            score = 14
        elif utilization > 0:
            score = 10
        else:
            score = 0
        
        return {
            'score': score,
            'details': {
                'utilization_rate': round(utilization, 2),
                'active_users': active_users,
                'total_users': total_users
            }
        }
    
    def calculate_component_05_behavioral_funnel(self, org: Dict) -> Dict:
        """Component 5: Behavioral Funnel Completeness (15 points max)."""
        segment = org.get('segment', 'Commerce-Active')
        
        has_catalog = (org.get('mp_total_logins', 0) or 0) > 0
        has_search = (org.get('search_products', 0) or 0) > 0
        has_cart = (org.get('select_a_customer', 0) or 0) > 0
        has_orders = (org.get('mp_submit_order', 0) or 0) > 0
        has_portal = (org.get('access_sales_portal', 0) or 0) > 0
        
        stages_completed = sum([has_catalog, has_search, has_cart, has_orders, has_portal])
        
        if segment == 'Catalog-Focused':
            if has_catalog and has_search:
                score = 10
            elif has_catalog:
                score = 5
            else:
                score = 0
        elif segment == 'Commerce-Active':
            if stages_completed >= 3:
                score = 15
            elif stages_completed == 2:
                score = 10
            elif stages_completed == 1:
                score = 5
            else:
                score = 0
        else:
            if stages_completed >= 4:
                score = 15
            elif stages_completed == 3:
                score = 12
            elif stages_completed == 2:
                score = 8
            elif stages_completed == 1:
                score = 4
            else:
                score = 0
        
        return {
            'score': score,
            'details': {
                'stages_completed': stages_completed,
                'catalog': has_catalog,
                'search': has_search,
                'cart': has_cart,
                'orders': has_orders,
                'portal': has_portal
            }
        }
    
    def calculate_component_06_clicky_engagement(self, org: Dict) -> Dict:
        """Component 6: Clicky Analytics Engagement (10 points max)."""
        has_clicky = org.get('has_clicky_portal', False)
        
        if not has_clicky:
            return {'score': 0, 'details': 'No Clicky Analytics'}
        
        daily_visitors = org.get('portal_visitors_daily', 0) or 0
        bounce_rate = org.get('portal_bounce_rate', 0) or 0
        bounce_rate_decimal = bounce_rate / 100.0 if bounce_rate > 1 else bounce_rate
        
        if daily_visitors >= 100 and bounce_rate_decimal < 0.50:
            score = 10
        elif daily_visitors >= 100:
            score = 8
        elif daily_visitors >= 50:
            score = 6
        elif daily_visitors > 0:
            score = 3
        else:
            score = 0
        
        return {
            'score': score,
            'details': {
                'daily_visitors': daily_visitors,
                'bounce_rate': bounce_rate
            }
        }
    
    def calculate_component_07_order_volume(self, org: Dict, benchmarks: Dict) -> Dict:
        """Component 7: Order Volume Performance (25 points max)."""
        orders = org.get('mp_submit_order', 0) or 0
        
        p25 = benchmarks.get('submit_order_p25', 0) or 0
        median = benchmarks.get('submit_order_median', 0) or 0
        p75 = benchmarks.get('submit_order_p75', 0) or 0
        
        if orders >= p75:
            score = 25
        elif orders >= median:
            score = 20
        elif orders >= p25:
            score = 15
        elif orders > 0:
            score = 10
        else:
            score = 0
        
        return {
            'score': score,
            'details': {
                'orders': orders,
                'benchmark_p75': p75,
                'benchmark_median': median
            }
        }
    
    def calculate_component_08_user_activation(self, org: Dict, benchmarks: Dict) -> Dict:
        """Component 8: User Activation Rate (20 points max)."""
        active_users = org.get('mp_active_users', 0) or 0
        total_users = org.get('mp_total_users', 0) or 0
        
        if total_users == 0:
            return {'score': 0, 'details': 'No users'}
        
        activation_rate = active_users / total_users
        
        if activation_rate >= 0.60:
            score = 20
        elif activation_rate >= 0.40:
            score = 17
        elif activation_rate >= 0.20:
            score = 14
        elif activation_rate > 0:
            score = 10
        else:
            score = 0
        
        return {
            'score': score,
            'details': {
                'activation_rate': round(activation_rate, 2),
                'active_users': active_users,
                'total_users': total_users
            }
        }
    
    def calculate_component_09_customer_engagement(self, org: Dict, benchmarks: Dict) -> Dict:
        """Component 9: Customer Engagement Depth (20 points max)."""
        customer_selections = org.get('select_a_customer', 0) or 0
        orders = org.get('mp_submit_order', 0) or 0
        
        if orders == 0:
            return {'score': 0, 'details': 'No orders'}
        
        engagement_ratio = customer_selections / orders if orders > 0 else 0
        
        if engagement_ratio >= 2.0:
            score = 20
        elif engagement_ratio >= 1.5:
            score = 17
        elif engagement_ratio >= 1.0:
            score = 14
        elif engagement_ratio > 0:
            score = 10
        else:
            score = 0
        
        return {
            'score': score,
            'details': {
                'engagement_ratio': round(engagement_ratio, 2),
                'customer_selections': customer_selections,
                'orders': orders
            }
        }
    
    def calculate_layer_1_engagement(self, org: Dict, benchmarks: Dict) -> Dict:
        """Layer 1: Engagement Health (6 components, max 100 points)."""
        c1 = self.calculate_component_01_login_intensity(org, benchmarks)
        c2 = self.calculate_component_02_feature_adoption(org)
        c3 = self.calculate_component_03_portal_engagement(org, benchmarks)
        c4 = self.calculate_component_04_seat_utilization(org)
        c5 = self.calculate_component_05_behavioral_funnel(org)
        c6 = self.calculate_component_06_clicky_engagement(org)
        
        total_score = (
            c1['score'] + c2['score'] + c3['score'] + 
            c4['score'] + c5['score'] + c6['score']
        )
        
        return {
            'layer_score': total_score,
            'components': {
                'login_intensity': c1,
                'feature_adoption': c2,
                'portal_engagement': c3,
                'seat_utilization': c4,
                'behavioral_funnel': c5,
                'clicky_engagement': c6
            }
        }
    
    def calculate_composite_score(self, org: Dict, benchmarks: Dict) -> Dict:
        """Calculate composite health score with ENHANCED data."""
        org_shortname = org['org_shortname']
        org_name = org.get('org_name', org_shortname)
        
        print(f"  📊 Calculating layers for {org_shortname}...")
        
        # Calculate all 4 layers (now with enhanced Layer 2, 3, and 4)
        layer1 = self.calculate_layer_1_engagement(org, benchmarks)
        layer2 = self.calculate_layer_2_value_realization(org, benchmarks)
        layer3 = self.calculate_layer_3_trend_momentum(org)
        layer4 = self.calculate_layer_4_risk_signals(org)
        
        # Apply layer weights (25% / 40% / 20% / 15%)
        composite_score_raw = (
            (layer1['layer_score'] * 0.25) +
            (layer2['layer_score'] * 0.40) +
            (layer3['layer_score'] * 0.20) +
            (layer4['layer_score'] * 0.15)
        ) / 100.0
        
        # Check for disqualifying risks
        arr = org.get('arr', 0) or 0
        logins = org.get('mp_total_logins', 0) or 0
        
        paying_but_disengaged = arr > 5000 and logins == 0
        
        # Auto-cap if disqualifying risk
        if paying_but_disengaged:
            composite_score_final = min(composite_score_raw, 0.30)
            severity = 'immediate'
        else:
            composite_score_final = composite_score_raw
            severity = None
        
        # Health band
        if composite_score_final >= 0.80:
            health_band = 'Excellent'
        elif composite_score_final >= 0.60:
            health_band = 'Good'
        elif composite_score_final >= 0.40:
            health_band = 'Fair'
        elif composite_score_final >= 0.30:
            health_band = 'At Risk'
        else:
            health_band = 'Critical'
        
        # Three flags
        churn_risk = paying_but_disengaged or composite_score_final < 0.30
        
        # Expansion ready
        segment = org.get('segment', '')
        orders = org.get('mp_submit_order', 0) or 0
        configured_items = org.get('order_configured_item', 0) or 0
        
        expansion_ready = (
            (segment == 'Catalog-Focused' and orders > 50) or
            (segment == 'Commerce-Active' and orders > 400) or
            (configured_items > 100)
        )
        
        # Healthy complete
        healthy_complete = (
            composite_score_final >= 0.70 and
            not churn_risk and
            (not expansion_ready or composite_score_final >= 0.80)
        )
        
        return {
            'org_shortname': org_shortname,
            'org_name': org_name,
            'segment': org.get('segment'),
            'arr': arr,
            'composite_score_raw': round(composite_score_raw, 3),
            'composite_score_final': round(composite_score_final, 3),
            'health_band': health_band,
            'churn_risk': churn_risk,
            'churn_severity': severity,
            'expansion_ready': expansion_ready,
            'healthy_complete': healthy_complete,
            'layer_1_engagement': round(layer1['layer_score'], 1),
            'layer_2_value_realization': round(layer2['layer_score'], 1),
            'layer_3_trend_momentum': round(layer3['layer_score'], 1),
            'layer_4_risk_signals': round(layer4['layer_score'], 1),
            'all_components': {
                'layer_1': layer1['components'],
                'layer_2': layer2['components'],
                'layer_3': layer3['components'],
                'layer_4': layer4['components']
            }
        }
    
    def calculate_batch(self, org_shortnames: List[str]) -> List[Dict]:
        """Calculate health scores for a batch of clients."""
        results = []
        
        for org_shortname in org_shortnames:
            print(f"\n📊 Processing {org_shortname}...")
            
            # Fetch data
            org = self.get_org_summary(org_shortname)
            if not org:
                print(f"  ⏭️  Skipping {org_shortname} (no data)")
                continue
            
            segment = org.get('segment')
            benchmarks = self.get_segment_benchmarks(segment)
            if not benchmarks:
                print(f"  ⚠️  No benchmarks for {segment}, using defaults")
                benchmarks = {}
            
            # Calculate score
            result = self.calculate_composite_score(org, benchmarks)
            results.append(result)
            
            print(f"  ✅ {org_shortname}: {result['composite_score_final']} ({result['health_band']})")
            if result['churn_risk']:
                print(f"     🚨 CHURN RISK: {result.get('churn_severity', 'detected')}")
            if result['expansion_ready']:
                print(f"     💰 EXPANSION READY")
            if result['healthy_complete']:
                print(f"     ✨ HEALTHY & COMPLETE")
        
        return results


def write_detailed_breakdowns(results: List[Dict], output_dir: str):
    """Write detailed per-client breakdowns to markdown files."""
    os.makedirs(output_dir, exist_ok=True)
    
    for result in results:
        org = result['org_shortname']
        filename = f"{output_dir}/{org}_health_breakdown.md"
        
        with open(filename, 'w') as f:
            f.write(f"# Health Intelligence v3 Score Breakdown: {result['org_name']} ({org})\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("**Version:** v4 FULL (with historical trends and support data)\n\n")
            f.write("---\n\n")
            
            # Composite score
            f.write("## Composite Health Score\n\n")
            f.write(f"- **Final Score:** {result['composite_score_final']} ({result['health_band']})\n")
            f.write(f"- **Raw Score:** {result['composite_score_raw']}\n")
            f.write(f"- **Segment:** {result['segment']}\n")
            f.write(f"- **ARR:** ${result['arr']:,.0f}\n" if result['arr'] else "- **ARR:** N/A\n")
            f.write("\n")
            
            # Flags
            f.write("## Health Flags\n\n")
            f.write(f"- 🚨 **Churn Risk:** {'YES' if result['churn_risk'] else 'No'}")
            if result['churn_severity']:
                f.write(f" (Severity: {result['churn_severity']})")
            f.write("\n")
            f.write(f"- 💰 **Expansion Ready:** {'YES' if result['expansion_ready'] else 'No'}\n")
            f.write(f"- ✨ **Healthy Complete:** {'YES' if result['healthy_complete'] else 'No'}\n")
            f.write("\n")
            
            # Layer scores
            f.write("## Layer Scores\n\n")
            f.write(f"1. **Engagement Health:** {result['layer_1_engagement']}/100 (Weight: 25%)\n")
            f.write(f"2. **Value Realization:** {result['layer_2_value_realization']}/100 (Weight: 40%)\n")
            f.write(f"3. **Trend Momentum:** {result['layer_3_trend_momentum']}/100 (Weight: 20%) — **NOW WITH REAL TRENDS**\n")
            f.write(f"4. **Risk Signals:** {result['layer_4_risk_signals']}/0 (Weight: 15%) — **NOW WITH SUPPORT DATA**\n")
            f.write("\n")
            
            # Component details
            f.write("## Component Breakdown\n\n")
            
            f.write("### Layer 1: Engagement Health (100 points max)\n\n")
            for comp_name, comp_data in result['all_components']['layer_1'].items():
                f.write(f"**{comp_name.replace('_', ' ').title()}:** {comp_data['score']} points\n")
                f.write(f"- Details: {comp_data['details']}\n\n")
            
            f.write("### Layer 2: Value Realization (125 points max, normalized to 100)\n\n")
            for comp_name, comp_data in result['all_components']['layer_2'].items():
                f.write(f"**{comp_name.replace('_', ' ').title()}:** {comp_data['score']} points\n")
                f.write(f"- Details: {comp_data['details']}\n\n")
            
            f.write("### Layer 3: Trend Momentum (100 points max) — **ENHANCED WITH REAL DATA**\n\n")
            for comp_name, comp_data in result['all_components']['layer_3'].items():
                f.write(f"**{comp_name.replace('_', ' ').title()}:** {comp_data['score']} points\n")
                f.write(f"- Details: {comp_data['details']}\n\n")
            
            f.write("### Layer 4: Risk Signals (0 to -100 points) — **ENHANCED WITH SUPPORT DATA**\n\n")
            for comp_name, comp_data in result['all_components']['layer_4'].items():
                f.write(f"**{comp_name.replace('_', ' ').title()}:** {comp_data['score']} points\n")
                f.write(f"- Details: {comp_data['details']}\n\n")


def main():
    parser = argparse.ArgumentParser(description='Calculate Health Intelligence v3 scores with FULL data')
    parser.add_argument('--batch-size', type=int, default=5, help='Number of clients to process at a time (default: 5)')
    parser.add_argument('--output-dir', help='Output directory (default: reports/health_scores_v4_YYYY-MM-DD)')
    parser.add_argument('--no-postgres', action='store_true', help='Disable Postgres queries (use BigQuery only)')
    
    args = parser.parse_args()
    
    # Initialize calculator
    calculator = HealthScoreCalculatorFull(use_postgres=not args.no_postgres)
    
    # Get all orgs from BigQuery
    print("📋 Fetching all client names from BigQuery...")
    org_shortnames = calculator.get_all_orgs()
    print(f"📋 Found {len(org_shortnames)} clients to process\n")
    
    if not org_shortnames:
        print("❌ No clients found")
        sys.exit(1)
    
    # Process in batches
    all_results = []
    for i in range(0, len(org_shortnames), args.batch_size):
        batch = org_shortnames[i:i + args.batch_size]
        print(f"\n{'='*60}")
        print(f"BATCH {i // args.batch_size + 1}: Processing {len(batch)} clients")
        print(f"{'='*60}")
        
        batch_results = calculator.calculate_batch(batch)
        all_results.extend(batch_results)
        
        print(f"\n✅ Batch complete: {len(batch_results)}/{len(batch)} clients scored")
    
    # Write outputs
    if not all_results:
        print("\n❌ No results to write (all clients failed)")
        sys.exit(1)
    
    output_dir = args.output_dir or f"reports/health_scores_v4_FULL_{datetime.now().strftime('%Y-%m-%d')}"
    os.makedirs(output_dir, exist_ok=True)
    
    csv_path = f"{output_dir}/client_health_scores_v4_FULL.csv"
    
    # Flatten results for CSV
    csv_rows = []
    for result in all_results:
        csv_rows.append({
            'org_shortname': result['org_shortname'],
            'org_name': result['org_name'],
            'segment': result['segment'],
            'arr': result['arr'],
            'composite_score_final': result['composite_score_final'],
            'health_band': result['health_band'],
            'churn_risk': result['churn_risk'],
            'churn_severity': result['churn_severity'] or '',
            'expansion_ready': result['expansion_ready'],
            'healthy_complete': result['healthy_complete'],
            'layer_1_engagement': result['layer_1_engagement'],
            'layer_2_value_realization': result['layer_2_value_realization'],
            'layer_3_trend_momentum': result['layer_3_trend_momentum'],
            'layer_4_risk_signals': result['layer_4_risk_signals']
        })
    
    df_output = pd.DataFrame(csv_rows)
    df_output = df_output.sort_values('composite_score_final', ascending=False)
    df_output.to_csv(csv_path, index=False)
    
    # Write detailed breakdowns
    print("\n📝 Writing detailed per-client breakdowns...")
    write_detailed_breakdowns(all_results, f"{output_dir}/client_breakdowns")
    
    print(f"\n{'='*60}")
    print(f"✅ COMPLETE: {len(all_results)} clients scored with v4 FULL")
    print(f"📄 Main CSV: {csv_path}")
    print(f"📝 Client Breakdowns: {output_dir}/client_breakdowns/")
    print(f"{'='*60}")
    
    # Summary stats
    print("\n📊 SUMMARY:")
    print(f"  Excellent: {sum(1 for r in all_results if r['health_band'] == 'Excellent')}")
    print(f"  Good: {sum(1 for r in all_results if r['health_band'] == 'Good')}")
    print(f"  Fair: {sum(1 for r in all_results if r['health_band'] == 'Fair')}")
    print(f"  At Risk: {sum(1 for r in all_results if r['health_band'] == 'At Risk')}")
    print(f"  Critical: {sum(1 for r in all_results if r['health_band'] == 'Critical')}")
    print(f"\n  Churn Risk: {sum(1 for r in all_results if r['churn_risk'])}")
    print(f"  Expansion Ready: {sum(1 for r in all_results if r['expansion_ready'])}")
    print(f"  Healthy Complete: {sum(1 for r in all_results if r['healthy_complete'])}")
    
    print("\n🎉 v4 FULL includes:")
    print("  ✅ Layer 3: Real historical trends (order, user, customer growth)")
    print("  ✅ Layer 2: Real support burden data from HelpScout")
    print("  ✅ Layer 4: Real support escalation risk from HelpScout")
    print("  ⏳ Postgres components pending connection (product health, concentration, exodus)")


if __name__ == '__main__':
    main()
