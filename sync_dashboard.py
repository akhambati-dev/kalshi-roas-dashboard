#!/usr/bin/env python3
"""
Kalshi ROAS Dashboard Sync Script
----------------------------------
1. Reads the newest liftoff_roas*.csv and liftoff_campaign_roas*.csv
   from ~/Desktop/Kalshi Dashboard Data/
2. Embeds the data into kalshi_roas_dashboard.html
3. Commits and pushes via git (use GitHub Desktop if git push fails)

Run from the repo folder:
  python3 sync_dashboard.py
"""

import csv
import json
import re
import glob
import os
import subprocess
from pathlib import Path
from datetime import date

# ── Paths ────────────────────────────────────────────────────────────────────
SOURCE = Path.home() / "Desktop" / "Kalshi Dashboard Data"
HTML   = Path("kalshi_roas_dashboard.html")

# ── Helpers ──────────────────────────────────────────────────────────────────
def nf(v):
    try:
        return round(float(v), 6) if v and str(v).strip() else None
    except Exception:
        return None

# ── Find newest CSVs ─────────────────────────────────────────────────────────
agg_files  = sorted(glob.glob(str(SOURCE / "liftoff_roas*.csv")),
                    key=os.path.getmtime, reverse=True)
camp_files = sorted(glob.glob(str(SOURCE / "liftoff_campaign_roas*.csv")),
                    key=os.path.getmtime, reverse=True)

if not agg_files:
    raise FileNotFoundError(f"No liftoff_roas*.csv found in {SOURCE}")
if not camp_files:
    raise FileNotFoundError(f"No liftoff_campaign_roas*.csv found in {SOURCE}")

agg_path  = agg_files[0]
camp_path = camp_files[0]
print(f"Aggregate  : {agg_path}")
print(f"Campaign   : {camp_path}")

# ── Read CSVs ────────────────────────────────────────────────────────────────
ar = [
    [
        r["day"],
        round(float(r.get("spend") or 0), 2),
        nf(r.get("roas_day_1")),
        nf(r.get("roas_day_7")),
        nf(r.get("roas_day_30")),
    ]
    for r in csv.DictReader(open(agg_path))
    if r.get("day")
]

cr = [
    [
        r["day"],
        r["campaign"],
        round(float(r.get("spend") or 0), 2),
        round(float(r.get("signups") or 0), 1),
        round(float(r.get("depositors") or 0), 1),
        round(float(r.get("traders") or 0), 1),
        nf(r.get("roas_day_1")),
        nf(r.get("roas_day_7")),
        nf(r.get("roas_day_30")),
    ]
    for r in csv.DictReader(open(camp_path))
    if r.get("day") and r.get("campaign")
]

print(f"Agg rows   : {len(ar)}")
print(f"Camp rows  : {len(cr)}")
print(f"Latest date: {max(r[0] for r in ar)}")

# ── Build compact JSON ───────────────────────────────────────────────────────
aj = json.dumps(
    {"cols": ["day", "spend", "roas_day_1", "roas_day_7", "roas_day_30"], "rows": ar},
    separators=(",", ":"),
)
cj = json.dumps(
    {
        "cols": [
            "day", "campaign", "spend",
            "signups", "depositors", "traders",
            "roas_day_1", "roas_day_7", "roas_day_30",
        ],
        "rows": cr,
    },
    separators=(",", ":"),
)

# ── Patch HTML ───────────────────────────────────────────────────────────────
if not HTML.exists():
    raise FileNotFoundError(f"{HTML} not found. Run from the repo folder.")

h = HTML.read_text(encoding="utf-8")

h_new = re.sub(
    r"const EMBEDDED_AGG\s*=\s*\{.*?\};",
    f"const EMBEDDED_AGG  = {aj};",
    h, count=1, flags=re.DOTALL,
)
h_new = re.sub(
    r"const EMBEDDED_CAMP\s*=\s*\{.*?\};",
    f"const EMBEDDED_CAMP = {cj};",
    h_new, count=1, flags=re.DOTALL,
)

if h_new == h:
    print("WARNING: HTML was not modified — EMBEDDED_AGG/CAMP constants not found.")
    print("Make sure you are running this script from the repo folder.")
else:
    HTML.write_text(h_new, encoding="utf-8")
    print("HTML updated successfully.")

# ── Git commit ───────────────────────────────────────────────────────────────
today = date.today().isoformat()
try:
    subprocess.run(["git", "add", "kalshi_roas_dashboard.html"], check=True)
    subprocess.run(["git", "commit", "-m", f"Data {today}"], check=True)
    print(f"Committed: Data {today}")
except subprocess.CalledProcessError as e:
    print(f"Git commit step failed: {e}")
    print("Open GitHub Desktop to commit manually.")

# ── Git push ─────────────────────────────────────────────────────────────────
try:
    result = subprocess.run(
        ["git", "push"],
        capture_output=True, text=True, timeout=30,
    )
    if result.returncode == 0:
        print("Pushed to GitHub successfully!")
        print("Dashboard is live at: https://akhambati-dev.github.io/kalshi-roas-dashboard/kalshi_roas_dashboard.html")
    else:
        print("git push failed (common on corporate networks).")
        print("Open GitHub Desktop and click 'Push origin' to finish.")
        print(result.stderr)
except Exception as e:
    print(f"git push error: {e}")
    print("Open GitHub Desktop and click 'Push origin'.")
