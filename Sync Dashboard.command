#!/bin/bash
# ─────────────────────────────────────────────
#  Kalshi ROAS Dashboard — Data Sync
#  Double-click this file to push new data to GitHub.
#  Everyone who refreshes the dashboard URL sees the update instantly.
# ─────────────────────────────────────────────
REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_DIR="$REPO_DIR/data"
SOURCE="$HOME/Desktop/Kalshi Dashboard Data"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Kalshi ROAS Dashboard — Data Sync"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ -d "$SOURCE" ]; then
    # Always pick the newest file by modification date
    AGG=$(ls -t "$SOURCE"/liftoff_roas*.csv 2>/dev/null | head -1)
    CAMP=$(ls -t "$SOURCE"/liftoff_campaign_roas*.csv 2>/dev/null | head -1)
    [ -n "$AGG" ]  && cp "$AGG"  "$DATA_DIR/liftoff_roas.csv"  && echo "✓ $(basename "$AGG")"
    [ -n "$CAMP" ] && cp "$CAMP" "$DATA_DIR/liftoff_campaign_roas.csv" && echo "✓ $(basename "$CAMP")"
else
    echo "⚠  '$SOURCE' not found — add CSVs directly to the data/ folder"
fi

echo ""
cd "$REPO_DIR"
git add data/
git commit -m "Data update $(date '+%Y-%m-%d')" 2>/dev/null || echo "No new changes to push"
git push && echo "" && echo "✅ Done! Everyone will see the new data on refresh." || echo "❌ Push failed — check internet connection"
echo ""
echo "Press any key to close..."
read -n 1
