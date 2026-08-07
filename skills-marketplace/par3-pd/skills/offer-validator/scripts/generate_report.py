#!/usr/bin/env python3
"""
Offer Validation Report Generator
Takes a JSON file with validation data and outputs a styled HTML report.

Usage:
    python generate_report.py --input data.json --output report.html
"""
import json, argparse, os, sys
from datetime import datetime

def get_score_color(score):
    if score >= 80: return "#10B981"   # green
    if score >= 65: return "#3B82F6"   # blue
    if score >= 50: return "#F59E0B"   # amber
    if score >= 35: return "#F97316"   # orange
    return "#EF4444"                    # red

def get_score_label(score):
    if score >= 80: return "Exceptional Opportunity"
    if score >= 65: return "Solid Opportunity"
    if score >= 50: return "Decent — Needs Work"
    if score >= 35: return "Risky — Consider Pivoting"
    return "Not Recommended"

def get_rec_color(rec):
    r = rec.upper()
    if "GO WITH" in r: return "#3B82F6"
    if r == "GO": return "#10B981"
    if "PIVOT" in r: return "#F59E0B"
    if "STOP" in r: return "#EF4444"
    return "#8B5CF6"

def get_channel_badge(rating):
    r = rating.lower()
    if r == "easy": return "#10B981"
    if r == "medium": return "#F59E0B"
    return "#EF4444"

def build_html(data):
    d = data
    score = d.get("overall_score", 0)
    score_color = get_score_color(score)
    score_label = get_score_label(score)
    rec = d.get("recommendation", "GO WITH CHANGES")
    rec_color = get_rec_color(rec)
    catchup = d.get("competition_catchup_speed", "Medium")
    catchup_explanation = d.get("competition_catchup_explanation", "")

    # Build scoring rows
    categories = d.get("scoring_categories", [])
    scoring_rows = ""
    for cat in categories:
        name = cat.get("name", "")
        pts = cat.get("score", 0)
        max_pts = cat.get("max", 10)
        note = cat.get("notes", "")
        pct = (pts / max_pts * 100) if max_pts > 0 else 0
        bar_color = get_score_color(pct)
        scoring_rows += f'''
        <div class="score-row">
          <div class="score-row-header">
            <span class="score-cat-name">{name}</span>
            <span class="score-cat-pts" style="color:{bar_color}">{pts}/{max_pts}</span>
          </div>
          <div class="score-bar-track"><div class="score-bar-fill" style="width:{pct}%;background:{bar_color}"></div></div>
          <p class="score-cat-note">{note}</p>
        </div>'''

    # ICP section
    icp = d.get("icp", {})
    pain_points = d.get("pain_points", [])
    pain_html = ""
    for i, p in enumerate(pain_points, 1):
        pain_html += f'<div class="pain-card"><span class="pain-num">{i}</span><p>{p}</p></div>'

    # Competitors
    competitors = d.get("competitors", [])
    comp_html = ""
    for c in competitors:
        comp_html += f'''
        <div class="comp-card">
          <div class="comp-header">
            <span class="comp-name">{c.get("name","")}</span>
            <span class="comp-type">{c.get("type","")}</span>
          </div>
          <div class="comp-detail"><strong>Price:</strong> {c.get("price","")}</div>
          <div class="comp-detail"><strong>Positioning:</strong> {c.get("positioning","")}</div>
          <div class="comp-detail"><strong>Weakness:</strong> {c.get("weakness","")}</div>
        </div>'''

    pricing = d.get("pricing_spectrum", {})

    # Outbound channels
    channels = d.get("outbound_channels", [])
    channel_rows = ""
    for ch in channels:
        badge_color = get_channel_badge(ch.get("beginner_rating", "Hard"))
        rec_badge = "Yes" if ch.get("recommended", False) else ("Long-term" if ch.get("long_term", False) else "No")
        rec_badge_color = "#10B981" if rec_badge == "Yes" else ("#3B82F6" if rec_badge == "Long-term" else "#6B7280")
        channel_rows += f'''
        <tr>
          <td>{ch.get("name","")}</td>
          <td><span class="badge" style="background:{badge_color}">{ch.get("beginner_rating","")}</span></td>
          <td>{ch.get("time_to_first","")}</td>
          <td><span class="badge" style="background:{rec_badge_color}">{rec_badge}</span></td>
        </tr>'''

    # Personal brand
    brand = d.get("personal_brand", {})
    brand_platform = brand.get("primary_platform", "")
    brand_platform_why = brand.get("platform_why", "")
    brand_pillars = brand.get("content_pillars", [])
    brand_cadence = brand.get("cadence", "")
    brand_quick_wins = brand.get("quick_wins", [])
    brand_flywheel = brand.get("flywheel", "")

    pillars_html = ""
    for i, p in enumerate(brand_pillars):
        colors = ["#8B5CF6", "#3B82F6", "#10B981", "#F59E0B"]
        c = colors[i % len(colors)]
        pillars_html += f'<div class="pillar-card" style="border-left-color:{c}"><span class="pillar-num" style="color:{c}">{i+1}</span><p>{p}</p></div>'

    quick_wins_html = ""
    for w in brand_quick_wins:
        quick_wins_html += f'<div class="qw-item">{w}</div>'

    # 90-day plan
    plan = d.get("ninety_day_plan", {})
    plan_html = ""
    for phase, desc in plan.items():
        plan_html += f'''
        <div class="plan-phase">
          <div class="plan-label">{phase}</div>
          <p>{desc}</p>
        </div>'''

    # Messaging
    one_liner = d.get("one_liner", "")
    outreach_template = d.get("outreach_template", "")
    key_phrases = d.get("key_phrases", [])
    phrases_html = " ".join([f'<span class="phrase-tag">{p}</span>' for p in key_phrases])

    # Honest assessment
    strengths = d.get("strengths", [])
    concerns = d.get("concerns", [])
    improvements = d.get("improvements", [])

    strengths_html = "".join([f'<li>{s}</li>' for s in strengths])
    concerns_html = "".join([f'<li>{s}</li>' for s in concerns])
    improvements_html = "".join([f'<li>{s}</li>' for s in improvements])

    offer = d.get("offer_summary", "")
    advantages = d.get("advantages", "")
    icp_who = icp.get("who", "")
    icp_where = icp.get("where_to_find", "")
    icp_triggers = icp.get("buying_triggers", "")
    gap = d.get("gap", "")
    primary_channel = d.get("primary_channel", {})
    secondary_channel = d.get("secondary_channel", {})

    today = datetime.now().strftime("%B %d, %Y")

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Offer Validation Report</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'DM Sans',sans-serif;background:#0A0A0F;color:#E2E8F0;line-height:1.7;-webkit-font-smoothing:antialiased}}
.container{{max-width:800px;margin:0 auto;padding:40px 24px 80px}}
.mono{{font-family:'Space Mono',monospace}}

/* Header */
.report-header{{text-align:center;padding:60px 0 40px;border-bottom:1px solid rgba(255,255,255,0.06)}}
.report-header h1{{font-size:32px;font-weight:700;letter-spacing:-0.5px;margin-bottom:8px;color:#F8FAFC}}
.report-header .subtitle{{color:#94A3B8;font-size:15px}}
.report-header .date{{color:#64748B;font-size:13px;margin-top:12px}}

/* Score Hero */
.score-hero{{text-align:center;padding:48px 0;margin:32px 0;background:linear-gradient(135deg, rgba(15,15,25,0.8), rgba(20,20,35,0.6));border:1px solid rgba(255,255,255,0.06);border-radius:16px}}
.score-number{{font-family:'Space Mono',monospace;font-size:96px;font-weight:700;color:{score_color};line-height:1}}
.score-max{{font-size:28px;color:#475569}}
.score-label{{font-size:18px;color:{score_color};margin-top:8px;font-weight:500}}
.rec-badge{{display:inline-block;margin-top:20px;padding:8px 24px;border-radius:100px;font-size:14px;font-weight:700;letter-spacing:1px;color:#FFF;background:{rec_color}}}

/* Section */
.section{{margin-top:48px}}
.section-label{{font-family:'Space Mono',monospace;font-size:11px;letter-spacing:2px;text-transform:uppercase;color:#64748B;margin-bottom:8px}}
.section-title{{font-size:22px;font-weight:700;color:#F8FAFC;margin-bottom:20px}}
.section-divider{{height:1px;background:linear-gradient(90deg,rgba(255,255,255,0.08),transparent);margin-bottom:32px}}

/* Offer Box */
.offer-box{{background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:24px;margin-bottom:24px}}
.offer-box .label{{font-size:12px;color:#64748B;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px}}
.offer-box .value{{font-size:16px;color:#E2E8F0}}

/* Score Breakdown */
.score-row{{margin-bottom:20px}}
.score-row-header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:6px}}
.score-cat-name{{font-weight:500;font-size:14px;color:#CBD5E1}}
.score-cat-pts{{font-family:'Space Mono',monospace;font-weight:700;font-size:15px}}
.score-bar-track{{height:6px;background:rgba(255,255,255,0.06);border-radius:3px;overflow:hidden}}
.score-bar-fill{{height:100%;border-radius:3px;transition:width 0.8s ease}}
.score-cat-note{{font-size:13px;color:#64748B;margin-top:4px}}

/* Catchup */
.catchup-box{{background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:20px;margin-top:24px;display:flex;gap:16px;align-items:flex-start}}
.catchup-label{{font-family:'Space Mono',monospace;font-size:13px;font-weight:700;white-space:nowrap;padding:4px 12px;border-radius:6px;background:rgba(255,255,255,0.06)}}
.catchup-text{{font-size:14px;color:#94A3B8}}

/* Pain Cards */
.pain-card{{background:rgba(255,255,255,0.03);border-left:3px solid #3B82F6;padding:16px 20px;margin-bottom:12px;border-radius:0 8px 8px 0;display:flex;gap:16px;align-items:flex-start}}
.pain-num{{font-family:'Space Mono',monospace;font-size:20px;font-weight:700;color:#3B82F6;flex-shrink:0}}
.pain-card p{{font-size:14px;color:#CBD5E1}}

/* Competitor Cards */
.comp-grid{{display:grid;gap:12px}}
.comp-card{{background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:20px}}
.comp-header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px}}
.comp-name{{font-weight:700;font-size:15px;color:#F8FAFC}}
.comp-type{{font-size:12px;color:#64748B;background:rgba(255,255,255,0.06);padding:3px 10px;border-radius:100px}}
.comp-detail{{font-size:13px;color:#94A3B8;margin-bottom:4px}}
.comp-detail strong{{color:#CBD5E1}}

/* Pricing Spectrum */
.pricing-row{{display:grid;grid-template-columns:100px 1fr;gap:12px;align-items:center;padding:12px 0;border-bottom:1px solid rgba(255,255,255,0.04)}}
.pricing-tier{{font-family:'Space Mono',monospace;font-size:12px;color:#64748B;text-transform:uppercase}}
.pricing-value{{font-size:14px;color:#CBD5E1}}
.pricing-row.target{{background:rgba(59,130,246,0.08);border-radius:8px;padding:12px;border:1px solid rgba(59,130,246,0.2);border-bottom:1px solid rgba(59,130,246,0.2)}}
.pricing-row.target .pricing-tier{{color:#3B82F6}}
.pricing-row.target .pricing-value{{color:#F8FAFC;font-weight:700}}

/* Channel Table */
table{{width:100%;border-collapse:collapse}}
th{{font-family:'Space Mono',monospace;font-size:11px;letter-spacing:1px;text-transform:uppercase;color:#64748B;text-align:left;padding:12px 16px;border-bottom:1px solid rgba(255,255,255,0.06)}}
td{{font-size:14px;color:#CBD5E1;padding:14px 16px;border-bottom:1px solid rgba(255,255,255,0.04)}}
.badge{{display:inline-block;padding:3px 12px;border-radius:100px;font-size:12px;font-weight:600;color:#FFF}}
.channel-rec{{background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:20px;margin-top:16px}}
.channel-rec-title{{font-size:13px;color:#64748B;margin-bottom:4px}}
.channel-rec-name{{font-size:16px;font-weight:700;color:#F8FAFC}}
.channel-rec-why{{font-size:14px;color:#94A3B8;margin-top:4px}}

/* Plan Timeline */
.plan-phase{{position:relative;padding-left:28px;margin-bottom:24px}}
.plan-phase::before{{content:'';position:absolute;left:8px;top:28px;bottom:-24px;width:1px;background:rgba(255,255,255,0.06)}}
.plan-phase:last-child::before{{display:none}}
.plan-label{{font-family:'Space Mono',monospace;font-size:13px;font-weight:700;color:#3B82F6;margin-bottom:4px;position:relative}}
.plan-label::before{{content:'';position:absolute;left:-22px;top:5px;width:10px;height:10px;border-radius:50%;background:#3B82F6;border:2px solid #0A0A0F}}
.plan-phase p{{font-size:14px;color:#94A3B8}}

/* Messaging */
.one-liner-box{{background:linear-gradient(135deg,rgba(59,130,246,0.08),rgba(139,92,246,0.06));border:1px solid rgba(59,130,246,0.15);border-radius:12px;padding:24px;font-size:18px;font-weight:500;color:#F8FAFC;line-height:1.5;text-align:center}}
.outreach-box{{background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:24px;margin-top:16px;font-size:14px;color:#CBD5E1;white-space:pre-wrap;line-height:1.8}}
.phrase-tag{{display:inline-block;background:rgba(59,130,246,0.1);border:1px solid rgba(59,130,246,0.2);color:#93C5FD;padding:4px 12px;border-radius:100px;font-size:13px;margin:4px 4px 4px 0}}

/* Personal Brand */
.platform-hero{{background:linear-gradient(135deg,rgba(139,92,246,0.1),rgba(59,130,246,0.06));border:1px solid rgba(139,92,246,0.2);border-radius:12px;padding:24px;text-align:center;margin-bottom:20px}}
.platform-hero .platform-name{{font-size:22px;font-weight:700;color:#A78BFA}}
.platform-hero .platform-why{{font-size:14px;color:#94A3B8;margin-top:8px}}
.pillar-card{{background:rgba(255,255,255,0.03);border-left:3px solid #8B5CF6;padding:14px 20px;margin-bottom:10px;border-radius:0 8px 8px 0;display:flex;gap:14px;align-items:flex-start}}
.pillar-num{{font-family:'Space Mono',monospace;font-size:18px;font-weight:700;flex-shrink:0}}
.pillar-card p{{font-size:14px;color:#CBD5E1}}
.qw-item{{background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);border-radius:8px;padding:12px 16px;margin-bottom:8px;font-size:14px;color:#CBD5E1;position:relative;padding-left:28px}}
.qw-item::before{{content:'→';position:absolute;left:12px;color:#8B5CF6;font-weight:700}}
.flywheel-box{{background:linear-gradient(135deg,rgba(139,92,246,0.06),rgba(59,130,246,0.04));border:1px solid rgba(139,92,246,0.12);border-radius:12px;padding:20px;margin-top:16px;font-size:14px;color:#CBD5E1;line-height:1.7}}
.flywheel-box strong{{color:#A78BFA}}

/* Assessment */
.assess-grid{{display:grid;gap:16px}}
.assess-card{{border-radius:12px;padding:20px;border:1px solid rgba(255,255,255,0.06)}}
.assess-card.good{{background:rgba(16,185,129,0.06);border-color:rgba(16,185,129,0.15)}}
.assess-card.risk{{background:rgba(239,68,68,0.06);border-color:rgba(239,68,68,0.15)}}
.assess-card.improve{{background:rgba(59,130,246,0.06);border-color:rgba(59,130,246,0.15)}}
.assess-card h4{{font-size:14px;margin-bottom:10px}}
.assess-card.good h4{{color:#10B981}}
.assess-card.risk h4{{color:#EF4444}}
.assess-card.improve h4{{color:#3B82F6}}
.assess-card ul{{list-style:none;padding:0}}
.assess-card li{{font-size:14px;color:#94A3B8;padding:4px 0;padding-left:16px;position:relative}}
.assess-card li::before{{content:'→';position:absolute;left:0;color:#475569}}

/* Footer */
.report-footer{{text-align:center;padding:48px 0 0;margin-top:48px;border-top:1px solid rgba(255,255,255,0.06);color:#475569;font-size:12px}}
</style>
</head>
<body>
<div class="container">

<div class="report-header">
  <h1>Offer Validation Report</h1>
  <div class="subtitle">Deep market research & opportunity scoring</div>
  <div class="date">{today}</div>
</div>

<div class="score-hero">
  <div class="score-number">{score}<span class="score-max">/100</span></div>
  <div class="score-label">{score_label}</div>
  <div class="rec-badge">{rec}</div>
</div>

<div class="section">
  <div class="offer-box">
    <div class="label">Your Offer</div>
    <div class="value">{offer}</div>
  </div>
  <div class="offer-box">
    <div class="label">Your Advantages</div>
    <div class="value">{advantages}</div>
  </div>
</div>

<div class="section">
  <div class="section-label">Scoring</div>
  <div class="section-title">Score Breakdown</div>
  <div class="section-divider"></div>
  {scoring_rows}
  <div class="catchup-box">
    <span class="catchup-label">{catchup}</span>
    <span class="catchup-text">{catchup_explanation}</span>
  </div>
</div>

<div class="section">
  <div class="section-label">Research</div>
  <div class="section-title">Your Ideal Client</div>
  <div class="section-divider"></div>
  <div class="offer-box">
    <div class="label">Who They Are</div>
    <div class="value">{icp_who}</div>
  </div>
  {pain_html}
  <div class="offer-box" style="margin-top:16px">
    <div class="label">Where to Find Them</div>
    <div class="value">{icp_where}</div>
  </div>
  <div class="offer-box">
    <div class="label">What Triggers Them to Buy</div>
    <div class="value">{icp_triggers}</div>
  </div>
</div>

<div class="section">
  <div class="section-label">Competition</div>
  <div class="section-title">Competitive Landscape</div>
  <div class="section-divider"></div>
  <div class="comp-grid">{comp_html}</div>

  <div style="margin-top:24px">
    <div class="section-label" style="margin-bottom:12px">Pricing Spectrum</div>
    <div class="pricing-row">
      <span class="pricing-tier">Budget</span>
      <span class="pricing-value">{pricing.get("budget","")}</span>
    </div>
    <div class="pricing-row">
      <span class="pricing-tier">Mid-Tier</span>
      <span class="pricing-value">{pricing.get("mid","")}</span>
    </div>
    <div class="pricing-row">
      <span class="pricing-tier">Premium</span>
      <span class="pricing-value">{pricing.get("premium","")}</span>
    </div>
    <div class="pricing-row target">
      <span class="pricing-tier">Your Target</span>
      <span class="pricing-value">{pricing.get("target","")}</span>
    </div>
  </div>

  <div class="offer-box" style="margin-top:20px">
    <div class="label">The Gap You Can Fill</div>
    <div class="value">{gap}</div>
  </div>
</div>

<div class="section">
  <div class="section-label">Outreach</div>
  <div class="section-title">How to Reach Clients</div>
  <div class="section-divider"></div>
  <table>
    <thead><tr><th>Channel</th><th>Difficulty</th><th>Time to Response</th><th>Recommended</th></tr></thead>
    <tbody>{channel_rows}</tbody>
  </table>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:16px">
    <div class="channel-rec">
      <div class="channel-rec-title">Primary Channel (70%)</div>
      <div class="channel-rec-name">{primary_channel.get("name","")}</div>
      <div class="channel-rec-why">{primary_channel.get("why","")}</div>
    </div>
    <div class="channel-rec">
      <div class="channel-rec-title">Secondary Channel (30%)</div>
      <div class="channel-rec-name">{secondary_channel.get("name","")}</div>
      <div class="channel-rec-why">{secondary_channel.get("why","")}</div>
    </div>
  </div>
</div>

<div class="section">
  <div class="section-label">Personal Brand</div>
  <div class="section-title">Build Credibility So Outbound Converts</div>
  <div class="section-divider"></div>
  <div class="platform-hero">
    <div class="platform-name">{brand_platform}</div>
    <div class="platform-why">{brand_platform_why}</div>
  </div>
  <div class="offer-box">
    <div class="label">Posting Cadence</div>
    <div class="value">{brand_cadence}</div>
  </div>
  <div style="margin-top:20px">
    <div class="section-label" style="margin-bottom:12px">Content Pillars</div>
    {pillars_html}
  </div>
  <div style="margin-top:20px">
    <div class="section-label" style="margin-bottom:12px">Quick Wins (First 30 Days)</div>
    {quick_wins_html}
  </div>
  <div class="flywheel-box">
    <strong>How This Amplifies Your Outbound:</strong> {brand_flywheel}
  </div>
</div>

<div class="section">
  <div class="section-label">Action Plan</div>
  <div class="section-title">Your 90-Day Plan</div>
  <div class="section-divider"></div>
  {plan_html}
</div>

<div class="section">
  <div class="section-label">Messaging</div>
  <div class="section-title">Your Angle</div>
  <div class="section-divider"></div>
  <div class="one-liner-box">"{one_liner}"</div>
  <div class="outreach-box">{outreach_template}</div>
  <div style="margin-top:16px">
    <div class="section-label" style="margin-bottom:8px">Key Phrases to Use</div>
    {phrases_html}
  </div>
</div>

<div class="section">
  <div class="section-label">Assessment</div>
  <div class="section-title">Honest Take</div>
  <div class="section-divider"></div>
  <div class="assess-grid">
    <div class="assess-card good">
      <h4>What's Working</h4>
      <ul>{strengths_html}</ul>
    </div>
    <div class="assess-card risk">
      <h4>What Concerns Me</h4>
      <ul>{concerns_html}</ul>
    </div>
    <div class="assess-card improve">
      <h4>What Would Make This 10/10</h4>
      <ul>{improvements_html}</ul>
    </div>
  </div>
</div>

<div class="report-footer">
  Generated by Offer Validator &middot; {today}
</div>

</div>
</body>
</html>'''
    return html


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to JSON data file")
    parser.add_argument("--output", required=True, help="Path for output HTML file")
    args = parser.parse_args()

    with open(args.input) as f:
        data = json.load(f)

    html = build_html(data)

    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(html)

    print(json.dumps({"status": "success", "output": args.output}))


if __name__ == "__main__":
    main()
