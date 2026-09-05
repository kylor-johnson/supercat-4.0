#!/usr/bin/env python3
"""
Manual review script to extract REAL competitive insights from Coaster calls
This will look for explicit comparisons and specific feature mentions
"""

import sys
import os
import json
from datetime import datetime

sys.path.insert(0, os.path.join(os.getcwd(), 'integrations/fathom'))

from fathom_api import get_meetings, get_transcript

def find_coaster_standups():
    """Find all [Hold] eCat x Coaster Standup meetings"""
    print("Fetching all meetings from Fathom API...")
    all_meetings = get_meetings(paginate=True)
    
    coaster_calls = []
    search_terms = [
        "[hold] ecat x coaster standup",
        "ecat x coaster standup",
        "coaster standup",
        "ecat x coaster"
    ]
    
    for meeting in all_meetings:
        title = meeting.get('meeting_title', '').lower()
        if any(term in title for term in search_terms):
            date_str = meeting.get('recording_start_time', '')
            if date_str:
                try:
                    date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                    if date_obj >= datetime(2024, 12, 16, tzinfo=date_obj.tzinfo):
                        coaster_calls.append(meeting)
                except:
                    coaster_calls.append(meeting)
    
    coaster_calls.sort(key=lambda x: x.get('recording_start_time', ''))
    return coaster_calls

def extract_real_competitive_insights(transcript, recording_id, meeting_title, date):
    """
    Extract REAL competitive insights - explicit mentions of features, comparisons, etc.
    """
    insights = {
        'supercat_advantages': [],
        'amp_advantages': [],
        'feature_requests': [],
        'migration_comments': []
    }
    
    if not transcript:
        return insights
    
    # Look for explicit Amp mentions and what features they had
    amp_feature_keywords = [
        'amp had', 'in amp', 'with amp', 'amp gave', 'amp allowed',
        'amp could', 'amp was', 'from amp', 'amp dashboard', 'amp table'
    ]
    
    # Look for SuperCat advantages
    supercat_advantage_keywords = [
        'supercat can', 'ecat can', 'supercat has', 'ecat has',
        'supercat allows', 'ecat allows', 'supercat does', 'ecat does'
    ]
    
    for i, segment in enumerate(transcript):
        text = segment.get('text', '').lower()
        speaker = segment.get('speaker', {})
        speaker_name = speaker.get('display_name', 'Unknown') if isinstance(speaker, dict) else str(speaker)
        timestamp = segment.get('start_time', 0)
        
        # Get context
        context_segments = []
        start_idx = max(0, i - 3)
        end_idx = min(len(transcript), i + 4)
        
        for j in range(start_idx, end_idx):
            seg = transcript[j]
            seg_speaker = seg.get('speaker', {})
            seg_speaker_name = seg_speaker.get('display_name', 'Unknown') if isinstance(seg_speaker, dict) else str(seg_speaker)
            context_segments.append(f"{seg_speaker_name}: {seg.get('text', '')}")
        
        context = "\n".join(context_segments)
        
        # Check for Amp feature mentions
        if any(keyword in text for keyword in amp_feature_keywords):
            # Filter out generic mentions
            if 'example' not in text and len(text) > 30:
                insights['amp_advantages'].append({
                    'quote': segment.get('text', ''),
                    'speaker': speaker_name,
                    'timestamp': timestamp,
                    'context': context,
                    'call_date': date,
                    'call_title': meeting_title,
                    'recording_id': recording_id
                })
        
        # Check for SuperCat advantages
        if any(keyword in text for keyword in supercat_advantage_keywords):
            if 'example' not in text and len(text) > 30:
                insights['supercat_advantages'].append({
                    'quote': segment.get('text', ''),
                    'speaker': speaker_name,
                    'timestamp': timestamp,
                    'context': context,
                    'call_date': date,
                    'call_title': meeting_title,
                    'recording_id': recording_id
                })
        
        # Look for migration comments
        migration_keywords = ['migrat', 'switch', 'transition', 'move from', 'coming from']
        if any(keyword in text for keyword in migration_keywords) and 'amp' in text:
            insights['migration_comments'].append({
                'quote': segment.get('text', ''),
                'speaker': speaker_name,
                'timestamp': timestamp,
                'context': context,
                'call_date': date,
                'call_title': meeting_title,
                'recording_id': recording_id
            })
    
    return insights

def format_timestamp(seconds):
    """Convert seconds to MM:SS format"""
    if isinstance(seconds, (int, float)):
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"
    return "00:00"

def main():
    print("=" * 80)
    print("COASTER COMPETITIVE ANALYSIS - MANUAL REVIEW")
    print("=" * 80)
    
    coaster_calls = find_coaster_standups()
    print(f"\nFound {len(coaster_calls)} Coaster Standup calls\n")
    
    all_supercat_advantages = []
    all_amp_advantages = []
    all_feature_requests = []
    all_migration_comments = []
    
    for i, call in enumerate(coaster_calls, 1):
        recording_id = call.get('recording_id')
        title = call.get('meeting_title', 'Untitled')
        date = call.get('recording_start_time', '')[:10]
        share_url = call.get('share_url', 'N/A')
        
        print(f"\n[{i}/{len(coaster_calls)}] Analyzing: {date} - {title}")
        
        transcript = get_transcript(recording_id)
        if not transcript:
            print("  ⚠️  No transcript available")
            continue
        
        print(f"  ✓ Retrieved {len(transcript)} segments")
        
        insights = extract_real_competitive_insights(transcript, recording_id, title, date)
        
        # Add share URL to all insights
        for insight_list in [insights['supercat_advantages'], insights['amp_advantages'], 
                            insights['feature_requests'], insights['migration_comments']]:
            for insight in insight_list:
                insight['share_url'] = share_url
        
        all_supercat_advantages.extend(insights['supercat_advantages'])
        all_amp_advantages.extend(insights['amp_advantages'])
        all_feature_requests.extend(insights['feature_requests'])
        all_migration_comments.extend(insights['migration_comments'])
        
        print(f"  → SuperCat advantages: {len(insights['supercat_advantages'])}")
        print(f"  → Amp advantages: {len(insights['amp_advantages'])}")
        print(f"  → Migration comments: {len(insights['migration_comments'])}")
    
    # Generate report
    output_file = f"documentation/Coaster_Competitive_Intelligence_Report_{datetime.now().strftime('%Y%m%d')}.md"
    
    with open(output_file, 'w') as f:
        f.write("# Coaster Competitive Intelligence Report\n")
        f.write("## SuperCat vs Amp - Detailed Analysis\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Analysis Period:** December 16, 2024 - Present\n\n")
        f.write(f"**Calls Analyzed:** {len(coaster_calls)}\n\n")
        
        f.write("---\n\n")
        f.write("## Executive Summary\n\n")
        f.write(f"- **Total SuperCat Advantage Mentions:** {len(all_supercat_advantages)}\n")
        f.write(f"- **Total Amp Advantage Mentions:** {len(all_amp_advantages)}\n")
        f.write(f"- **Migration-Related Comments:** {len(all_migration_comments)}\n\n")
        
        # Amp Advantages (What SuperCat needs to improve)
        f.write("---\n\n")
        f.write("## 🔴 Where Amp Was Better (Product Improvement Opportunities)\n\n")
        
        if all_amp_advantages:
            for i, insight in enumerate(all_amp_advantages, 1):
                f.write(f"### Finding #{i}\n\n")
                f.write(f"**Date:** {insight['call_date']}\n\n")
                f.write(f"**Speaker:** {insight['speaker']}\n\n")
                f.write(f"**Timestamp:** {format_timestamp(insight['timestamp'])}\n\n")
                f.write(f"**Recording:** [{insight['share_url']}]({insight['share_url']})\n\n")
                f.write(f"**Quote:**\n\n")
                f.write(f"> {insight['quote']}\n\n")
                f.write(f"**Context:**\n\n")
                f.write(f"```\n{insight['context']}\n```\n\n")
                f.write("---\n\n")
        else:
            f.write("No specific Amp advantages mentioned in the analyzed calls.\n\n")
        
        # SuperCat Advantages
        f.write("---\n\n")
        f.write("## 🟢 Where SuperCat Is Better (Sales Ammunition)\n\n")
        
        if all_supercat_advantages:
            for i, insight in enumerate(all_supercat_advantages, 1):
                f.write(f"### Finding #{i}\n\n")
                f.write(f"**Date:** {insight['call_date']}\n\n")
                f.write(f"**Speaker:** {insight['speaker']}\n\n")
                f.write(f"**Timestamp:** {format_timestamp(insight['timestamp'])}\n\n")
                f.write(f"**Recording:** [{insight['share_url']}]({insight['share_url']})\n\n")
                f.write(f"**Quote:**\n\n")
                f.write(f"> {insight['quote']}\n\n")
                f.write(f"**Context:**\n\n")
                f.write(f"```\n{insight['context']}\n```\n\n")
                f.write("---\n\n")
        else:
            f.write("No specific SuperCat advantages explicitly mentioned in the analyzed calls.\n\n")
        
        # Migration Comments
        f.write("---\n\n")
        f.write("## 🔄 Migration & Transition Comments\n\n")
        
        if all_migration_comments:
            for i, insight in enumerate(all_migration_comments, 1):
                f.write(f"### Comment #{i}\n\n")
                f.write(f"**Date:** {insight['call_date']}\n\n")
                f.write(f"**Speaker:** {insight['speaker']}\n\n")
                f.write(f"**Timestamp:** {format_timestamp(insight['timestamp'])}\n\n")
                f.write(f"**Recording:** [{insight['share_url']}]({insight['share_url']})\n\n")
                f.write(f"**Quote:**\n\n")
                f.write(f"> {insight['quote']}\n\n")
                f.write(f"**Context:**\n\n")
                f.write(f"```\n{insight['context']}\n```\n\n")
                f.write("---\n\n")
        else:
            f.write("No specific migration comments found.\n\n")
        
        f.write("---\n\n")
        f.write("## 📋 Action Items\n\n")
        f.write("### For Sales Team\n\n")
        f.write("1. Review SuperCat advantages section for competitive talking points\n")
        f.write("2. Prepare responses for Amp advantage points that may come up in sales conversations\n")
        f.write("3. Use migration comments to understand customer pain points during transitions\n\n")
        f.write("### For Product Team\n\n")
        f.write("1. Prioritize features mentioned in 'Amp Better' section\n")
        f.write("2. Validate that SuperCat advantages are well-documented and easy to demo\n")
        f.write("3. Consider migration comments when planning onboarding improvements\n\n")
    
    print(f"\n\n{'='*80}")
    print(f"✅ Report saved to: {output_file}")
    print(f"{'='*80}\n")
    
    # Print summary to console
    print("\n📊 SUMMARY\n")
    print(f"SuperCat Advantages Found: {len(all_supercat_advantages)}")
    print(f"Amp Advantages Found: {len(all_amp_advantages)}")
    print(f"Migration Comments: {len(all_migration_comments)}")
    
    if all_amp_advantages:
        print("\n🔴 KEY AMP ADVANTAGES (Product should review):\n")
        for i, insight in enumerate(all_amp_advantages[:5], 1):
            print(f"{i}. [{insight['call_date']}] {insight['speaker']}: {insight['quote'][:100]}...")
    
    if all_supercat_advantages:
        print("\n🟢 KEY SUPERCAT ADVANTAGES (Sales should leverage):\n")
        for i, insight in enumerate(all_supercat_advantages[:5], 1):
            print(f"{i}. [{insight['call_date']}] {insight['speaker']}: {insight['quote'][:100]}...")

if __name__ == "__main__":
    main()
