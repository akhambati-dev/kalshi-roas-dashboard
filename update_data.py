#!/usr/bin/env python3
"""
Kalshi ROAS Dashboard — Data Embedder
Reads the latest CSVs from your Desktop folder and
embeds them directly into the HTML. No file copying needed.
"""
import csv, json, re, os, glob, sys
from pathlib import Path
from datetime import date

SCRIPT_DIR = Path(__file__).parent
HTML_FILE  = SCRIPT_DIR / 'kalshi_roas_dashboard.html'
SOURCE_DIR = Path.home() / 'Desktop' / 'Kalshi Dashboard Data'

def nf(v):
    try: return round(float(v), 6) if v and str(v).strip() else None
    except: return None

def newest(pattern):
    files = sorted(glob.glob(str(SOURCE_DIR / pattern)), key=os.path.getmtime, reverse=True)
    return files[0] if files else None

# ── Find newest CSVs ────────────────────────────────────
if not SOURCE_DIR.exists():
    print(f"⚠  Folder not found: {SOURCE_DIR}")
    sys.exit(1)

agg_file  = newest('liftoff_roas*.csv')
camp_file = newest('liftoff_campaign_roas*.csv')

if not agg_file:
    print("⚠  No liftoff_roas*.csv found in your Desktop folder.")
    sys.exit(1)
if not camp_file:
    print("⚠  No liftoff_campaign_roas*.csv found.")
    sys.exit(1)

print(f"  Aggregate : {os.path.basename(agg_file)}")
print(f"  Campaign  : {os.path.basename(camp_file)}")

# ── Parse CSVs ──────────────────────────────────────────
agg_rows = []
with open(agg_file) as f:
    for r in csv.DictReader(f):
        if not r.get('day'): continue
        agg_rows.append([
            r['day'], round(float(r.get('spend') or 0), 2),
            nf(r.get('roas_day_1')), nf(r.get('roas_day_7')), nf(r.get('roas_day_30')),
        ])

camp_rows = []
with open(camp_file) as f:
    for r in csv.DictReader(f):
        if not r.get('day') or not r.get('campaign'): continue
        camp_rows.append([
            r['day'], r['campaign'],
            round(float(r.get('spend') or 0), 2),
            round(float(r.get('signups') or 0), 1),
            round(float(r.get('depositors') or 0), 1),
            round(float(r.get('traders') or 0), 1),
            nf(r.get('roas_day_1')), nf(r.get('roas_day_7')), nf(r.get('roas_day_30')),
        ])

agg_json  = json.dumps({'cols':['day','spend','roas_day_1','roas_day_7','roas_day_30'],'rows':agg_rows}, separators=(',',':'))
camp_json = json.dumps({'cols':['day','campaign','spend','signups','depositors','traders','roas_day_1','roas_day_7','roas_day_30'],'rows':camp_rows}, separators=(',',':'))

# ── Embed into HTML ─────────────────────────────────────
html = HTML_FILE.read_text(encoding='utf-8')
html = re.sub(r'const FALLBACK_AGG\s*=\s*\{.*?\};',  f'const FALLBACK_AGG  = {agg_json};',  html, count=1, flags=re.DOTALL)
html = re.sub(r'const FALLBACK_CAMP\s*=\s*\{.*?\};', f'const FALLBACK_CAMP = {camp_json};', html, count=1, flags=re.DOTALL)
html = re.sub(r'// Last embedded: \d{4}-\d{2}-\d{2}', f'// Last embedded: {date.today()}', html)
HTML_FILE.write_text(html, encoding='utf-8')

latest = max(r[0] for r in agg_rows)
print(f"  {len(agg_rows)} rows | {len(camp_rows)} campaign rows | latest date: {latest}")
print(f"✓ HTML updated")
