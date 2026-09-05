#!/usr/bin/env python3
"""
Sales Week-Ahead Analyst
Generates tactical weekly sales intelligence reports by combining HubSpot pipeline data
with Fathom Voice of Customer intelligence.

Usage:
    python3 sales_week_ahead_analyst.py --ae-name "Kylor Johnson"
    python3 sales_week_ahead_analyst.py --ae-name "Kylor Johnson" --days 7
"""

import sys
import os
import json
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Import HubSpot integration
from integrations.hubspot.client import HubSpotClient

# Import Fathom integration
fathom_path = os.path.join(parent_dir, 'integrations', 'fathom')
sys.path.insert(0, fathom_path)
from fathom_api import get_meetings, get_transcript, get_summary


class SalesWeekAheadAnalyst:
    """Generates tactical weekly sales intelligence reports"""
    
    def __init__(self, ae_name: str, days_ahead: int = 7):
        """
        Initialize the analyst
        
        Args:
            ae_name: Account Executive name (e.g., "Kylor Johnson")
            days_ahead: Number of days to look ahead (default: 7)
        """
        self.ae_name = ae_name
        self.days_ahead = days_ahead
        self.today = datetime.now()
        self.week_end = self.today + timedelta(days=days_ahead)
        
        # Initialize clients
        print("🔌 Connecting to HubSpot...")
        self.hubspot = HubSpotClient()
        if not self.hubspot.test_connection():
            raise Exception("Failed to connect to HubSpot")
        
        print("✅ Connected to data sources\n")
        
        # Data storage
        self.ae_owner_id = None
        self.discovery_calls = []
        self.pipeline_deals = []
        self.recent_meetings = []
        self.voc_data = {
            'pain_themes': defaultdict(int),
            'objections': defaultdict(int),
            'competitor_mentions': defaultdict(int),
            'phrases': []
        }
    
    def generate_report(self) -> str:
        """
        Generate the complete week-ahead report
        
        Returns:
            Markdown-formatted report
        """
        print("📊 Generating Week-Ahead Report...")
        print(f"   AE: {self.ae_name}")
        print(f"   Period: {self.today.strftime('%Y-%m-%d')} to {self.week_end.strftime('%Y-%m-%d')}\n")
        
        # Step 1: Find the AE in HubSpot
        self._find_ae_owner()
        
        # Step 2: Pull discovery calls scheduled this week
        self._pull_discovery_calls()
        
        # Step 3: Pull open pipeline deals
        self._pull_pipeline_deals()
        
        # Step 4: Pull recent Fathom meetings for VoC
        self._pull_voc_intelligence()
        
        # Step 5: Generate the report
        report = self._build_report()
        
        return report
    
    def _find_ae_owner(self):
        """Find the AE's owner ID in HubSpot"""
        print(f"🔍 Finding owner ID for {self.ae_name}...")
        
        # Get all owners
        result = self.hubspot.get('/crm/v3/owners')
        if 'error' in result:
            print(f"   ⚠️  Could not fetch owners: {result.get('message')}")
            return
        
        owners = result.get('results', [])
        
        # Search for matching name
        for owner in owners:
            first = owner.get('firstName', '').lower()
            last = owner.get('lastName', '').lower()
            full_name = f"{first} {last}"
            
            if self.ae_name.lower() in full_name or full_name in self.ae_name.lower():
                self.ae_owner_id = owner.get('id')
                print(f"   ✅ Found: {owner.get('firstName')} {owner.get('lastName')} (ID: {self.ae_owner_id})")
                return
        
        print(f"   ⚠️  Could not find owner matching '{self.ae_name}'")
        owner_names = [f"{o.get('firstName')} {o.get('lastName')}" for o in owners[:5]]
        print(f"   Available owners: {', '.join(owner_names)}")
    
    def _pull_discovery_calls(self):
        """Pull all discovery calls scheduled in the next week"""
        print(f"📅 Pulling discovery calls for next {self.days_ahead} days...")
        
        # Search for meetings/tasks scheduled this week
        # Note: This searches for meetings associated with the owner
        
        # Get deals with recent activity to find associated meetings
        search_data = {
            'filterGroups': [],
            'properties': [
                'dealname', 'dealstage', 'amount', 'closedate', 
                'hubspot_owner_id', 'createdate', 'notes_last_updated'
            ],
            'limit': 100
        }
        
        # Add owner filter if we found the AE
        if self.ae_owner_id:
            search_data['filterGroups'].append({
                'filters': [{
                    'propertyName': 'hubspot_owner_id',
                    'operator': 'EQ',
                    'value': self.ae_owner_id
                }]
            })
        
        result = self.hubspot.post('/crm/v3/objects/deals/search', search_data)
        
        if 'error' in result:
            print(f"   ⚠️  Error pulling deals: {result.get('message')}")
            return
        
        deals = result.get('results', [])
        
        # Filter for discovery stage deals (these are likely upcoming discovery calls)
        discovery_stages = ['appointmentscheduled', 'qualifiedtobuy', 'presentationscheduled']
        
        for deal in deals:
            props = deal.get('properties', {})
            stage = props.get('dealstage', '').lower()
            
            if any(disc_stage in stage for disc_stage in discovery_stages):
                self.discovery_calls.append(deal)
        
        print(f"   ✅ Found {len(self.discovery_calls)} potential discovery opportunities")
    
    def _pull_pipeline_deals(self):
        """Pull all open pipeline deals for the AE"""
        print("💰 Pulling open pipeline deals...")
        
        search_data = {
            'filterGroups': [{
                'filters': [
                    {
                        'propertyName': 'dealstage',
                        'operator': 'NEQ',
                        'value': 'closedwon'
                    },
                    {
                        'propertyName': 'dealstage',
                        'operator': 'NEQ',
                        'value': 'closedlost'
                    }
                ]
            }],
            'properties': [
                'dealname', 'dealstage', 'amount', 'closedate',
                'hubspot_owner_id', 'createdate', 'notes_last_updated',
                'hs_lastmodifieddate', 'num_associated_contacts'
            ],
            'limit': 100
        }
        
        # Add owner filter if we found the AE
        if self.ae_owner_id:
            search_data['filterGroups'][0]['filters'].append({
                'propertyName': 'hubspot_owner_id',
                'operator': 'EQ',
                'value': self.ae_owner_id
            })
        
        result = self.hubspot.post('/crm/v3/objects/deals/search', search_data)
        
        if 'error' in result:
            print(f"   ⚠️  Error pulling pipeline: {result.get('message')}")
            return
        
        self.pipeline_deals = result.get('results', [])
        
        # Calculate total pipeline value
        total_value = sum(
            float(d.get('properties', {}).get('amount', 0) or 0) 
            for d in self.pipeline_deals
        )
        
        print(f"   ✅ Found {len(self.pipeline_deals)} open deals (${total_value:,.0f} total)")
    
    def _pull_voc_intelligence(self):
        """Pull recent Fathom meetings for Voice of Customer intelligence"""
        print("🎙️  Pulling Voice of Customer intelligence from Fathom...")
        
        try:
            # Get meetings from last 30 days
            all_meetings = get_meetings(limit=50, paginate=False)
            
            # Filter to last 30 days
            cutoff_date = self.today - timedelta(days=30)
            
            for meeting in all_meetings:
                meeting_date_str = meeting.get('recording_start_time', meeting.get('created_at', ''))
                if not meeting_date_str:
                    continue
                
                try:
                    # Parse ISO date
                    meeting_date = datetime.fromisoformat(meeting_date_str.replace('Z', '+00:00'))
                    
                    if meeting_date.replace(tzinfo=None) >= cutoff_date:
                        self.recent_meetings.append(meeting)
                except:
                    continue
            
            print(f"   ✅ Found {len(self.recent_meetings)} meetings in last 30 days")
            
            # Extract VoC themes from summaries (if available)
            self._extract_voc_themes()
            
        except Exception as e:
            print(f"   ⚠️  Error pulling Fathom data: {e}")
    
    def _extract_voc_themes(self):
        """Extract pain themes, objections, and phrases from meeting data"""
        print("   🔍 Extracting VoC themes...")
        
        # Common pain keywords
        pain_keywords = [
            'problem', 'issue', 'challenge', 'struggle', 'difficult',
            'frustrated', 'manual', 'time-consuming', 'inefficient'
        ]
        
        # Common objection keywords
        objection_keywords = [
            'expensive', 'cost', 'price', 'budget', 'timing',
            'not sure', 'concerned', 'worried', 'risk'
        ]
        
        # Competitor names
        competitors = [
            'coaster', 'amp', 'salesforce', 'hubspot', 'pipedrive'
        ]
        
        for meeting in self.recent_meetings:
            title = meeting.get('meeting_title', '').lower()
            
            # Count pain mentions
            for keyword in pain_keywords:
                if keyword in title:
                    self.voc_data['pain_themes'][keyword] += 1
            
            # Count objection mentions
            for keyword in objection_keywords:
                if keyword in title:
                    self.voc_data['objections'][keyword] += 1
            
            # Count competitor mentions
            for competitor in competitors:
                if competitor in title:
                    self.voc_data['competitor_mentions'][competitor] += 1
    
    def _build_report(self) -> str:
        """Build the final markdown report"""
        
        # Segment deals into stalled vs moving
        stalled_deals, moving_deals = self._segment_pipeline()
        
        # Calculate key metrics
        total_pipeline_value = sum(
            float(d.get('properties', {}).get('amount', 0) or 0) 
            for d in self.pipeline_deals
        )
        
        biggest_deal = max(
            self.pipeline_deals,
            key=lambda d: float(d.get('properties', {}).get('amount', 0) or 0),
            default=None
        )
        biggest_deal_value = float(biggest_deal.get('properties', {}).get('amount', 0) or 0) if biggest_deal else 0
        
        # Build report sections
        report_lines = []
        
        # Header
        report_lines.append(f"# Sales Week-Ahead Report")
        report_lines.append(f"**AE:** {self.ae_name}")
        report_lines.append(f"**Week:** {self.today.strftime('%B %d, %Y')} - {self.week_end.strftime('%B %d, %Y')}")
        report_lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")
        
        # SECTION 1: Week at a Glance
        report_lines.append("## 1. WEEK AT A GLANCE")
        report_lines.append("")
        report_lines.append(f"- **Discovery calls scheduled:** {len(self.discovery_calls)}")
        report_lines.append(f"- **Pipeline deals to focus on:** {len(moving_deals)} moving, {len(stalled_deals)} stalled")
        report_lines.append(f"- **Biggest revenue at risk:** ${biggest_deal_value:,.0f} ({biggest_deal.get('properties', {}).get('dealname', 'Unknown') if biggest_deal else 'N/A'})")
        report_lines.append(f"- **Total pipeline value:** ${total_pipeline_value:,.0f}")
        report_lines.append(f"- **One thing to do well:** {self._get_top_priority(stalled_deals, moving_deals)}")
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")
        
        # SECTION 2: Discovery Call Prep
        report_lines.append("## 2. DISCOVERY CALL PREP")
        report_lines.append("")
        
        if not self.discovery_calls:
            report_lines.append("*No discovery calls scheduled in HubSpot for the next 7 days.*")
            report_lines.append("")
            report_lines.append("**Action:** Review your calendar and ensure all discovery calls are logged in HubSpot.")
        else:
            for i, call in enumerate(self.discovery_calls[:5], 1):  # Limit to 5
                report_lines.extend(self._format_discovery_brief(call, i))
        
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")
        
        # SECTION 3: Pipeline Reality
        report_lines.append("## 3. PIPELINE REALITY")
        report_lines.append("")
        
        # Stalled Deals
        report_lines.append("### A) STALLED DEALS (No activity in 14+ days)")
        report_lines.append("")
        
        if not stalled_deals:
            report_lines.append("*No stalled deals - great pipeline hygiene!*")
        else:
            for deal in stalled_deals[:5]:  # Limit to 5
                report_lines.extend(self._format_stalled_deal(deal))
        
        report_lines.append("")
        
        # Moving Deals
        report_lines.append("### B) MOVING DEALS (Recent activity)")
        report_lines.append("")
        
        if not moving_deals:
            report_lines.append("*No deals with recent activity.*")
        else:
            for deal in moving_deals[:5]:  # Limit to 5
                report_lines.extend(self._format_moving_deal(deal))
        
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")
        
        # SECTION 4: VoC Intelligence
        report_lines.append("## 4. VOICE OF CUSTOMER INTELLIGENCE")
        report_lines.append("")
        report_lines.append(f"*Based on {len(self.recent_meetings)} Fathom calls from the last 30 days*")
        report_lines.append("")
        
        report_lines.extend(self._format_voc_intelligence())
        
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")
        
        # SECTION 5: Weekly Game Plan
        report_lines.append("## 5. MY WEEKLY GAME PLAN")
        report_lines.append("")
        
        report_lines.extend(self._build_game_plan(stalled_deals, moving_deals))
        
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")
        report_lines.append("*Report generated by Sales Week-Ahead Analyst*")
        
        return "\n".join(report_lines)
    
    def _segment_pipeline(self) -> Tuple[List[Dict], List[Dict]]:
        """Segment pipeline into stalled vs moving deals"""
        stalled = []
        moving = []
        
        cutoff_date = self.today - timedelta(days=14)
        
        for deal in self.pipeline_deals:
            props = deal.get('properties', {})
            last_modified = props.get('hs_lastmodifieddate', props.get('notes_last_updated', ''))
            
            if not last_modified:
                stalled.append(deal)
                continue
            
            try:
                # Parse date
                modified_date = datetime.fromisoformat(last_modified.replace('Z', '+00:00'))
                
                if modified_date.replace(tzinfo=None) < cutoff_date:
                    stalled.append(deal)
                else:
                    moving.append(deal)
            except:
                stalled.append(deal)
        
        # Sort by deal value
        stalled.sort(key=lambda d: float(d.get('properties', {}).get('amount', 0) or 0), reverse=True)
        moving.sort(key=lambda d: float(d.get('properties', {}).get('amount', 0) or 0), reverse=True)
        
        return stalled, moving
    
    def _get_top_priority(self, stalled_deals: List[Dict], moving_deals: List[Dict]) -> str:
        """Determine the top priority for the week"""
        if stalled_deals:
            return f"Unblock the {len(stalled_deals)} stalled deals and get them moving"
        elif moving_deals:
            return f"Accelerate the {len(moving_deals)} moving deals to close"
        else:
            return "Fill the pipeline with qualified discovery calls"
    
    def _format_discovery_brief(self, call: Dict, number: int) -> List[str]:
        """Format a discovery call brief"""
        props = call.get('properties', {})
        lines = []
        
        lines.append(f"### Discovery Call #{number}")
        lines.append("")
        lines.append(f"**Deal:** {props.get('dealname', 'Unknown')}")
        lines.append(f"**Stage:** {props.get('dealstage', 'Unknown')}")
        lines.append(f"**Value:** ${float(props.get('amount', 0) or 0):,.0f}")
        lines.append("")
        
        lines.append("**A) Account & Fit Snapshot**")
        lines.append("- Fit score: *To be determined in discovery*")
        lines.append("- Segment: *Unknown - discover in call*")
        lines.append("")
        
        lines.append("**B) Historical Context**")
        lines.append(f"- Deal created: {props.get('createdate', 'Unknown')[:10]}")
        lines.append("- Prior interactions: *Check HubSpot timeline*")
        lines.append("")
        
        lines.append("**C) Hypothesized SPICED**")
        lines.append("- **Situation:** *To be discovered*")
        lines.append("- **Pain:** *To be discovered*")
        lines.append("- **Impact:** *To be quantified*")
        lines.append("- **Critical Event:** *To be identified*")
        lines.append("- **Decision:** *To be mapped*")
        lines.append("")
        
        lines.append("**D) Discovery Strategy**")
        lines.append("- **3 Must-Ask Questions:**")
        lines.append("  1. What triggered you to look for a solution now?")
        lines.append("  2. What's the cost of not solving this problem?")
        lines.append("  3. Who else needs to be involved in this decision?")
        lines.append("- **Urgency Question:** What's your timeline for making a decision?")
        lines.append("- **Qualify-Out Question:** Are you currently using any similar tools?")
        lines.append("- **Don't Pitch Yet:** Wait until you understand their full situation")
        lines.append("")
        
        return lines
    
    def _format_stalled_deal(self, deal: Dict) -> List[str]:
        """Format a stalled deal"""
        props = deal.get('properties', {})
        lines = []
        
        lines.append(f"**{props.get('dealname', 'Unknown')}**")
        lines.append(f"- Stage: {props.get('dealstage', 'Unknown')} | Amount: ${float(props.get('amount', 0) or 0):,.0f}")
        lines.append(f"- Last modified: {props.get('hs_lastmodifieddate', 'Unknown')[:10]}")
        lines.append(f"- Why stalled: No activity in 14+ days")
        lines.append(f"- SPICED gap: Missing urgency/critical event")
        lines.append(f"- **Best next action:** Send re-engagement email with value prop")
        lines.append(f"- **Risk if no action:** Deal goes cold, competitor wins")
        lines.append("")
        
        return lines
    
    def _format_moving_deal(self, deal: Dict) -> List[str]:
        """Format a moving deal"""
        props = deal.get('properties', {})
        lines = []
        
        lines.append(f"**{props.get('dealname', 'Unknown')}**")
        lines.append(f"- Stage: {props.get('dealstage', 'Unknown')} | Amount: ${float(props.get('amount', 0) or 0):,.0f}")
        lines.append(f"- Last activity: {props.get('hs_lastmodifieddate', 'Unknown')[:10]}")
        lines.append(f"- What's working: Recent engagement")
        lines.append(f"- **Acceleration action:** Schedule next step meeting")
        lines.append("")
        
        return lines
    
    def _format_voc_intelligence(self) -> List[str]:
        """Format Voice of Customer intelligence"""
        lines = []
        
        # Top pain themes
        lines.append("### A) Top 3 Pain Themes")
        lines.append("")
        
        top_pains = sorted(
            self.voc_data['pain_themes'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]
        
        if top_pains:
            for i, (pain, count) in enumerate(top_pains, 1):
                lines.append(f"{i}. **{pain.title()}** (mentioned {count}x)")
        else:
            lines.append("*No pain themes extracted from recent calls*")
        
        lines.append("")
        
        # Top objections
        lines.append("### B) Top 3 Objections")
        lines.append("")
        
        top_objections = sorted(
            self.voc_data['objections'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]
        
        if top_objections:
            for i, (objection, count) in enumerate(top_objections, 1):
                lines.append(f"{i}. **{objection.title()}** (mentioned {count}x)")
        else:
            lines.append("*No objections extracted from recent calls*")
        
        lines.append("")
        
        # Competitor mentions
        lines.append("### C) Competitor Intelligence")
        lines.append("")
        
        if self.voc_data['competitor_mentions']:
            for competitor, count in sorted(
                self.voc_data['competitor_mentions'].items(),
                key=lambda x: x[1],
                reverse=True
            ):
                lines.append(f"- **{competitor.title()}** mentioned {count}x")
        else:
            lines.append("*No competitor mentions in recent calls*")
        
        lines.append("")
        
        # Talk track recommendation
        lines.append("### D) Talk Track Recommendations")
        lines.append("")
        lines.append("**Lean into:**")
        lines.append("- Focus on quantifying impact and ROI early")
        lines.append("- Address timing/urgency in discovery")
        lines.append("")
        lines.append("**Stop saying:**")
        lines.append("- Generic feature lists without context")
        lines.append("")
        
        return lines
    
    def _build_game_plan(self, stalled_deals: List[Dict], moving_deals: List[Dict]) -> List[str]:
        """Build the weekly game plan"""
        lines = []
        
        lines.append("### A) Top 5 Actions (Ranked)")
        lines.append("")
        
        actions = []
        
        # Action 1: Unblock stalled deals
        if stalled_deals:
            top_stalled = stalled_deals[0]
            actions.append(
                f"1. **Unblock stalled deal:** Re-engage {top_stalled.get('properties', {}).get('dealname', 'Unknown')} "
                f"with value-focused email by {(self.today + timedelta(days=2)).strftime('%A')}"
            )
        
        # Action 2: Advance moving deals
        if moving_deals:
            top_moving = moving_deals[0]
            actions.append(
                f"2. **Advance moving deal:** Schedule next step with {top_moving.get('properties', {}).get('dealname', 'Unknown')} "
                f"by {(self.today + timedelta(days=3)).strftime('%A')}"
            )
        
        # Action 3: Discovery prep
        if self.discovery_calls:
            actions.append(
                f"3. **Discovery prep:** Research and prepare SPICED questions for {len(self.discovery_calls)} upcoming calls"
            )
        
        # Action 4: Pipeline hygiene
        actions.append(
            f"4. **Pipeline hygiene:** Update all deal stages and next steps in HubSpot by {(self.today + timedelta(days=4)).strftime('%A')}"
        )
        
        # Action 5: Learning
        actions.append(
            f"5. **Learning:** Review last 3 Fathom calls and extract objection handling patterns"
        )
        
        for action in actions:
            lines.append(action)
        
        lines.append("")
        
        # Deals to close or disqualify
        lines.append("### B) Deals to CLOSE or DISQUALIFY This Week")
        lines.append("")
        
        if stalled_deals:
            lines.append("**Disqualify candidates:**")
            for deal in stalled_deals[:2]:
                lines.append(f"- {deal.get('properties', {}).get('dealname', 'Unknown')} (stalled 14+ days)")
        else:
            lines.append("*No clear disqualify candidates*")
        
        lines.append("")
        
        if moving_deals:
            lines.append("**Close candidates:**")
            for deal in moving_deals[:2]:
                lines.append(f"- {deal.get('properties', {}).get('dealname', 'Unknown')} (has momentum)")
        else:
            lines.append("*No clear close candidates this week*")
        
        lines.append("")
        
        # Personal focus
        lines.append("### C) Personal Focus Improvement")
        lines.append("")
        lines.append("**This week's focus:** Slow down in discovery and quantify impact before moving to demo.")
        lines.append("")
        
        return lines
    
    def save_report(self, report: str) -> str:
        """
        Save the report to a file
        
        Args:
            report: The markdown report content
            
        Returns:
            Path to the saved file
        """
        # Create reports directory if it doesn't exist
        reports_dir = os.path.join(parent_dir, 'reports')
        os.makedirs(reports_dir, exist_ok=True)
        
        # Generate filename
        date_str = self.today.strftime('%Y-%m-%d')
        ae_slug = self.ae_name.lower().replace(' ', '_')
        filename = f"sales_week_ahead_{date_str}_{ae_slug}.md"
        filepath = os.path.join(reports_dir, filename)
        
        # Save report
        with open(filepath, 'w') as f:
            f.write(report)
        
        return filepath


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Generate Sales Week-Ahead tactical intelligence report'
    )
    parser.add_argument(
        '--ae-name',
        type=str,
        required=True,
        help='Account Executive name (e.g., "Kylor Johnson")'
    )
    parser.add_argument(
        '--days',
        type=int,
        default=7,
        help='Number of days to look ahead (default: 7)'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='Output file path (default: auto-generated in reports/)'
    )
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("SALES WEEK-AHEAD ANALYST")
    print("=" * 70)
    print()
    
    try:
        # Initialize analyst
        analyst = SalesWeekAheadAnalyst(
            ae_name=args.ae_name,
            days_ahead=args.days
        )
        
        # Generate report
        report = analyst.generate_report()
        
        # Save report
        if args.output:
            filepath = args.output
            with open(filepath, 'w') as f:
                f.write(report)
        else:
            filepath = analyst.save_report(report)
        
        print()
        print("=" * 70)
        print("✅ REPORT GENERATED SUCCESSFULLY")
        print("=" * 70)
        print()
        print(f"📄 Report saved to: {filepath}")
        print()
        print("Preview:")
        print("-" * 70)
        print(report[:1000])
        print("...")
        print("-" * 70)
        print()
        print(f"📖 Open the full report: {filepath}")
        
    except Exception as e:
        print()
        print("=" * 70)
        print("❌ ERROR")
        print("=" * 70)
        print()
        print(f"Failed to generate report: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
