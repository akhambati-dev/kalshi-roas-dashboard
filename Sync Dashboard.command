#!/bin/bash
# ─────────────────────────────────────────────
#  Kalshi ROAS Dashboard — Daily Data Sync
#  1. Drop new CSVs into ~/Desktop/Kalshi Dashboard Data/
#  2. Double-click this file
#  3. Done — everyone sees new data on refresh
# ─────────────────────────────────────────────
REPO_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Kalshi ROAS Dashboard — Data Sync"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Reading and embedding new data..."
echo ""

# Fix permissions on data folder before running
chmod -R 755 "$REPO_DIR/data/" 2>/dev/null

# Step 1: Run Python script to embed fresh data into HTML
python3 "$REPO_DIR/update_data.py"
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Data update failed. Check the messages above."
    echo "Press any key to close..."
    read -n 1
    exit 1
fi

# Step 2: Commit and push everything to GitHub
echo ""
echo "Pushing to GitHub..."
cd "$REPO_DIR"
git add .
git commit -m "Data update $(date '+%Y-%m-%d')"
git push

if [ $? -eq 0 ]; then
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  ✅  Done!"
    echo "  Everyone will see the new data"
    echo "  when they refresh the dashboard."
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
else
    echo "❌ Push failed. Check your internet connection."
fi

echo ""
echo "Press any key to close..."
read -n 1
