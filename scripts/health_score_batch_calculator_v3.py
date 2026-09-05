#!/usr/bin/env python3
"""
Health Intelligence v3 — Batch Calculator (Updated for actual BigQuery schema)

Purpose: Calculate health scores for all 132 SuperCat clients
Usage: python health_score_batch_calculator_v3.py --batch-size 5
Output: Multiple files with detailed breakdowns

Requirements:
- Python 3.8+
- google-cloud-bigquery
- pandas

Install: pip install google-cloud-bigquery pandas
"""

import argparse
import csv
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional

import pandas as pd
from google.cloud import bigquery


class HealthScoreCalculator:
    """Calculate Health Intelligence v3 scores for SuperCat clients."""
    
    def __init__(self, project_id: str = "supercat-data-pipeline"):
        self.bq_client = bigquery.Client(project=project_id)
        self.dataset = "insightful_product"
        
    def get_all_orgs(self) -> List[str]:
        """Fetch all org shortnames from BigQuery."""
        query = f"""
        SELECT DISTINCT org_shortname 
        FROM `{self.dataset}.org_summary`
        WHERE org_shortname IS NOT NULL
        ORDER BY org_shortname
        """
        
        try:
            result = self.bq_client.query(query).result()
            return [row['org_shortname'] for row in result]
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
                print(f"  ⚠️  No data found for {org_shortname} in org_summary")
                return None
            return dict(rows[0])
        except Exception as e:
            print(f"  ❌ Error fetching org_summary for {org_shortname}: {e}")
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
                print(f"  ⚠️  No benchmarks found for segment {segment}")
                return None
            return dict(rows[0])
        except Exception as e:
            print(f"  ❌ Error fetching benchmarks for {segment}: {e}")
            return None
    
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
        
        # For login intensity, we need to calculate per active user benchmarks
        # Simplified: use raw login benchmarks as proxy
        if p25 > 0 and active_users > 0:
            p25_intensity = p25 / active_users
            median_intensity = median / active_users if median > 0 else 0
            p75_intensity = p75 / active_users if p75 > 0 else 0
        else:
            p25_intensity = 50
            median_intensity = 100
            p75_intensity = 150
        
        # Scoring logic
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
        
        # Use portal access events as engagement proxy
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
        # Use active users / total users as proxy
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
        else:  # Platform-Embedded
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
        
        # Use segment-based thresholds since we don't have activation rate benchmarks
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
        # Use select_a_customer as proxy for customer engagement
        customer_selections = org.get('select_a_customer', 0) or 0
        orders = org.get('mp_submit_order', 0) or 0
        
        if orders == 0:
            return {'score': 0, 'details': 'No orders'}
        
        # Customer engagement = selections per order (higher = more customer variety)
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
    
    def calculate_layer_2_value_realization(self, org: Dict, benchmarks: Dict) -> Dict:
        """Layer 2: Value Realization (8 components, max 125 points, normalized to 100)."""
        c7 = self.calculate_component_07_order_volume(org, benchmarks)
        c8 = self.calculate_component_08_user_activation(org, benchmarks)
        c9 = self.calculate_component_09_customer_engagement(org, benchmarks)
        
        # Components 10-14 require additional data - graceful degradation
        c10 = {'score': 8, 'details': 'Additional data unavailable (neutral score)'}  # Product/Inventory Health (15 max)
        c11 = {'score': 5, 'details': 'Additional data unavailable (neutral score)'}  # Support Burden (10 max)
        c12 = {'score': 5, 'details': 'Additional data unavailable (neutral score)'}  # Geographic Penetration (10 max)
        c13 = {'score': 5, 'details': 'Additional data unavailable (neutral score)'}  # Customer Concentration (10 max)
        c14 = {'score': 8, 'details': 'Additional data unavailable (neutral score)'}  # Dormant Reactivation (15 max)
        
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
    
    def calculate_layer_3_trend_momentum(self, org: Dict) -> Dict:
        """Layer 3: Trend Momentum (4 components, max 100 points)."""
        # All 4 components require historical data - graceful degradation for MVP
        c15 = {'score': 15, 'details': 'Historical data unavailable (neutral score)'}  # Order Volume Trend (30 max)
        c16 = {'score': 13, 'details': 'Historical data unavailable (neutral score)'}  # User Growth Trend (25 max)
        c17 = {'score': 13, 'details': 'Historical data unavailable (neutral score)'}  # Customer Health Trend (25 max)
        c18 = {'score': 10, 'details': 'Historical data unavailable (neutral score)'}  # Feature Adoption Velocity (20 max)
        
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
    
    def calculate_layer_4_risk_signals(self, org: Dict) -> Dict:
        """Layer 4: Risk Signals (4 components, -100 to 0 points)."""
        # Check for paying but disengaged
        arr = org.get('arr', 0) or 0
        logins = org.get('mp_total_logins', 0) or 0
        
        # Rep disengagement risk
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
        c20 = {'score': 0, 'details': 'Support data unavailable (no penalty applied)'}
        c21 = {'score': 0, 'details': 'Data integrity checks unavailable (no penalty applied)'}
        c22 = {'score': 0, 'details': 'Customer exodus data unavailable (no penalty applied)'}
        
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
    
    def calculate_composite_score(self, org: Dict, benchmarks: Dict) -> Dict:
        """Calculate composite health score and three flags."""
        org_shortname = org['org_shortname']
        org_name = org.get('org_name', org_shortname)
        
        # Calculate all 4 layers
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
        
        # Expansion ready (simplified)
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
            f.write(f"3. **Trend Momentum:** {result['layer_3_trend_momentum']}/100 (Weight: 20%)\n")
            f.write(f"4. **Risk Signals:** {result['layer_4_risk_signals']}/0 (Weight: 15%)\n")
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
            
            f.write("### Layer 3: Trend Momentum (100 points max)\n\n")
            for comp_name, comp_data in result['all_components']['layer_3'].items():
                f.write(f"**{comp_name.replace('_', ' ').title()}:** {comp_data['score']} points\n")
                f.write(f"- Details: {comp_data['details']}\n\n")
            
            f.write("### Layer 4: Risk Signals (0 to -100 points)\n\n")
            for comp_name, comp_data in result['all_components']['layer_4'].items():
                f.write(f"**{comp_name.replace('_', ' ').title()}:** {comp_data['score']} points\n")
                f.write(f"- Details: {comp_data['details']}\n\n")


def main():
    parser = argparse.ArgumentParser(description='Calculate Health Intelligence v3 scores for all SuperCat clients')
    parser.add_argument('--batch-size', type=int, default=5, help='Number of clients to process at a time (default: 5)')
    parser.add_argument('--output-dir', default='health_scores_output', help='Output directory for results')
    
    args = parser.parse_args()
    
    # Initialize calculator
    calculator = HealthScoreCalculator()
    
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
    
    # Write output CSV
    if not all_results:
        print("\n❌ No results to write (all clients failed)")
        sys.exit(1)
    
    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)
    
    csv_path = f"{output_dir}/client_health_scores_2026-03-31.csv"
    
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
    
    # Write summary report
    summary_path = f"{output_dir}/SUMMARY_REPORT.md"
    with open(summary_path, 'w') as f:
        f.write("# Health Intelligence v3 — All Clients Summary Report\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Total Clients Scored:** {len(all_results)}\n\n")
        f.write("---\n\n")
        
        f.write("## How Health Scores Are Calculated\n\n")
        f.write("Health Intelligence v3 uses a **4-layer weighted composite model**:\n\n")
        f.write("### Layer Weights\n")
        f.write("1. **Engagement Health** (25%) — How actively users engage with the platform\n")
        f.write("2. **Value Realization** (40%) — How much business value the client derives\n")
        f.write("3. **Trend Momentum** (20%) — Direction of key metrics over time\n")
        f.write("4. **Risk Signals** (15%) — Early warning indicators of churn risk\n\n")
        
        f.write("### Health Bands\n")
        f.write("- **Excellent** (0.80+): Thriving clients with high engagement and value realization\n")
        f.write("- **Good** (0.60-0.79): Healthy clients with solid usage patterns\n")
        f.write("- **Fair** (0.40-0.59): Moderate health, may need attention\n")
        f.write("- **At Risk** (0.30-0.39): Low health, intervention recommended\n")
        f.write("- **Critical** (<0.30): Severe health issues, immediate action required\n\n")
        
        f.write("### Key Flags\n")
        f.write("- **Churn Risk:** Paying customers with zero/low engagement OR score < 0.30\n")
        f.write("- **Expansion Ready:** High-performing clients ready for upsell opportunities\n")
        f.write("- **Healthy Complete:** Excellent health with no expansion gaps\n\n")
        
        f.write("---\n\n")
        
        f.write("## Distribution by Health Band\n\n")
        excellent = sum(1 for r in all_results if r['health_band'] == 'Excellent')
        good = sum(1 for r in all_results if r['health_band'] == 'Good')
        fair = sum(1 for r in all_results if r['health_band'] == 'Fair')
        at_risk = sum(1 for r in all_results if r['health_band'] == 'At Risk')
        critical = sum(1 for r in all_results if r['health_band'] == 'Critical')
        
        f.write(f"- **Excellent:** {excellent} clients ({excellent/len(all_results)*100:.1f}%)\n")
        f.write(f"- **Good:** {good} clients ({good/len(all_results)*100:.1f}%)\n")
        f.write(f"- **Fair:** {fair} clients ({fair/len(all_results)*100:.1f}%)\n")
        f.write(f"- **At Risk:** {at_risk} clients ({at_risk/len(all_results)*100:.1f}%)\n")
        f.write(f"- **Critical:** {critical} clients ({critical/len(all_results)*100:.1f}%)\n\n")
        
        f.write("## Flag Summary\n\n")
        churn_risk_clients = [r for r in all_results if r['churn_risk']]
        expansion_ready_clients = [r for r in all_results if r['expansion_ready']]
        healthy_complete_clients = [r for r in all_results if r['healthy_complete']]
        
        f.write(f"### 🚨 Churn Risk: {len(churn_risk_clients)} clients\n\n")
        if churn_risk_clients:
            immediate = [r for r in churn_risk_clients if r.get('churn_severity') == 'immediate']
            if immediate:
                f.write(f"**Immediate Severity ({len(immediate)} clients):**\n")
                for r in sorted(immediate, key=lambda x: x['composite_score_final']):
                    f.write(f"- {r['org_name']} ({r['org_shortname']}): {r['composite_score_final']} — {r['health_band']}\n")
                f.write("\n")
            
            other = [r for r in churn_risk_clients if r.get('churn_severity') != 'immediate']
            if other:
                f.write(f"**Other Churn Risk ({len(other)} clients):**\n")
                for r in sorted(other, key=lambda x: x['composite_score_final']):
                    f.write(f"- {r['org_name']} ({r['org_shortname']}): {r['composite_score_final']} — {r['health_band']}\n")
                f.write("\n")
        
        f.write(f"### 💰 Expansion Ready: {len(expansion_ready_clients)} clients\n\n")
        if expansion_ready_clients:
            for r in sorted(expansion_ready_clients, key=lambda x: x['composite_score_final'], reverse=True)[:20]:
                f.write(f"- {r['org_name']} ({r['org_shortname']}): {r['composite_score_final']} — {r['health_band']}\n")
            if len(expansion_ready_clients) > 20:
                f.write(f"- ... and {len(expansion_ready_clients) - 20} more\n")
            f.write("\n")
        
        f.write(f"### ✨ Healthy Complete: {len(healthy_complete_clients)} clients\n\n")
        if healthy_complete_clients:
            for r in sorted(healthy_complete_clients, key=lambda x: x['composite_score_final'], reverse=True)[:20]:
                f.write(f"- {r['org_name']} ({r['org_shortname']}): {r['composite_score_final']} — {r['health_band']}\n")
            if len(healthy_complete_clients) > 20:
                f.write(f"- ... and {len(healthy_complete_clients) - 20} more\n")
            f.write("\n")
    
    print(f"📝 Detailed breakdowns written to: {output_dir}/client_breakdowns/")
    print(f"📊 Summary report written to: {summary_path}")


def main():
    parser = argparse.ArgumentParser(description='Calculate Health Intelligence v3 scores for all SuperCat clients')
    parser.add_argument('--batch-size', type=int, default=5, help='Number of clients to process at a time (default: 5)')
    parser.add_argument('--output-dir', help='Output directory (default: reports/health_scores_YYYY-MM-DD)')
    
    args = parser.parse_args()
    
    # Initialize calculator
    calculator = HealthScoreCalculator()
    
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
    
    output_dir = args.output_dir or f"health_scores_{datetime.now().strftime('%Y-%m-%d')}"
    os.makedirs(output_dir, exist_ok=True)
    
    csv_path = f"{output_dir}/client_health_scores_2026-03-31.csv"
    
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
    
    # Write summary report
    summary_path = f"{output_dir}/SUMMARY_REPORT.md"
    with open(summary_path, 'w') as f:
        f.write("# Health Intelligence v3 — All Clients Summary Report\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Total Clients Scored:** {len(all_results)}\n\n")
        f.write("---\n\n")
        
        f.write("## How Health Scores Are Calculated\n\n")
        f.write("Health Intelligence v3 uses a **4-layer weighted composite model**:\n\n")
        f.write("### Layer Weights\n")
        f.write("1. **Engagement Health** (25%) — How actively users engage with the platform\n")
        f.write("2. **Value Realization** (40%) — How much business value the client derives\n")
        f.write("3. **Trend Momentum** (20%) — Direction of key metrics over time\n")
        f.write("4. **Risk Signals** (15%) — Early warning indicators of churn risk\n\n")
        
        f.write("### Health Bands\n")
        f.write("- **Excellent** (0.80+): Thriving clients with high engagement and value realization\n")
        f.write("- **Good** (0.60-0.79): Healthy clients with solid usage patterns\n")
        f.write("- **Fair** (0.40-0.59): Moderate health, may need attention\n")
        f.write("- **At Risk** (0.30-0.39): Low health, intervention recommended\n")
        f.write("- **Critical** (<0.30): Severe health issues, immediate action required\n\n")
        
        f.write("### Key Flags\n")
        f.write("- **Churn Risk:** Paying customers with zero/low engagement OR score < 0.30\n")
        f.write("- **Expansion Ready:** High-performing clients ready for upsell opportunities\n")
        f.write("- **Healthy Complete:** Excellent health with no expansion gaps\n\n")
        
        f.write("---\n\n")
        
        f.write("## Distribution by Health Band\n\n")
        excellent = sum(1 for r in all_results if r['health_band'] == 'Excellent')
        good = sum(1 for r in all_results if r['health_band'] == 'Good')
        fair = sum(1 for r in all_results if r['health_band'] == 'Fair')
        at_risk = sum(1 for r in all_results if r['health_band'] == 'At Risk')
        critical = sum(1 for r in all_results if r['health_band'] == 'Critical')
        
        f.write(f"- **Excellent:** {excellent} clients ({excellent/len(all_results)*100:.1f}%)\n")
        f.write(f"- **Good:** {good} clients ({good/len(all_results)*100:.1f}%)\n")
        f.write(f"- **Fair:** {fair} clients ({fair/len(all_results)*100:.1f}%)\n")
        f.write(f"- **At Risk:** {at_risk} clients ({at_risk/len(all_results)*100:.1f}%)\n")
        f.write(f"- **Critical:** {critical} clients ({critical/len(all_results)*100:.1f}%)\n\n")
        
        f.write("## Flag Summary\n\n")
        churn_risk_clients = [r for r in all_results if r['churn_risk']]
        expansion_ready_clients = [r for r in all_results if r['expansion_ready']]
        healthy_complete_clients = [r for r in all_results if r['healthy_complete']]
        
        f.write(f"### 🚨 Churn Risk: {len(churn_risk_clients)} clients\n\n")
        if churn_risk_clients:
            immediate = [r for r in churn_risk_clients if r.get('churn_severity') == 'immediate']
            if immediate:
                f.write(f"**Immediate Severity ({len(immediate)} clients):**\n")
                for r in sorted(immediate, key=lambda x: x['composite_score_final']):
                    f.write(f"- {r['org_name']} ({r['org_shortname']}): {r['composite_score_final']} — {r['health_band']}\n")
                f.write("\n")
            
            other = [r for r in churn_risk_clients if r.get('churn_severity') != 'immediate']
            if other:
                f.write(f"**Other Churn Risk ({len(other)} clients):**\n")
                for r in sorted(other, key=lambda x: x['composite_score_final']):
                    f.write(f"- {r['org_name']} ({r['org_shortname']}): {r['composite_score_final']} — {r['health_band']}\n")
                f.write("\n")
        
        f.write(f"### 💰 Expansion Ready: {len(expansion_ready_clients)} clients\n\n")
        if expansion_ready_clients:
            for r in sorted(expansion_ready_clients, key=lambda x: x['composite_score_final'], reverse=True)[:20]:
                f.write(f"- {r['org_name']} ({r['org_shortname']}): {r['composite_score_final']} — {r['health_band']}\n")
            if len(expansion_ready_clients) > 20:
                f.write(f"- ... and {len(expansion_ready_clients) - 20} more\n")
            f.write("\n")
        
        f.write(f"### ✨ Healthy Complete: {len(healthy_complete_clients)} clients\n\n")
        if healthy_complete_clients:
            for r in sorted(healthy_complete_clients, key=lambda x: x['composite_score_final'], reverse=True)[:20]:
                f.write(f"- {r['org_name']} ({r['org_shortname']}): {r['composite_score_final']} — {r['health_band']}\n")
            if len(healthy_complete_clients) > 20:
                f.write(f"- ... and {len(healthy_complete_clients) - 20} more\n")
            f.write("\n")
        
        f.write("## Top 10 Healthiest Clients\n\n")
        top_10 = sorted(all_results, key=lambda x: x['composite_score_final'], reverse=True)[:10]
        for i, r in enumerate(top_10, 1):
            f.write(f"{i}. **{r['org_name']}** ({r['org_shortname']}): {r['composite_score_final']} — {r['health_band']}\n")
        f.write("\n")
        
        f.write("## Bottom 10 Clients (Need Attention)\n\n")
        bottom_10 = sorted(all_results, key=lambda x: x['composite_score_final'])[:10]
        for i, r in enumerate(bottom_10, 1):
            f.write(f"{i}. **{r['org_name']}** ({r['org_shortname']}): {r['composite_score_final']} — {r['health_band']}\n")
        f.write("\n")
    
    print(f"\n{'='*60}")
    print(f"✅ COMPLETE: {len(all_results)} clients scored")
    print(f"📄 Main CSV: {csv_path}")
    print(f"📊 Summary Report: {summary_path}")
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


if __name__ == '__main__':
    main()
