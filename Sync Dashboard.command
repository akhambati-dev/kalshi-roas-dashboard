#!/bin/bash
# ─────────────────────────────────────────────
#  Kalshi ROAS Dashboard — Data Sync Script
#  Double-click this file to push new data to GitHub.
#  Everyone who refreshes the dashboard URL sees the update.
# ─────────────────────────────────────────────

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_DIR="$REPO_DIR/data"
SOURCE_FOLDER="$HOME/Desktop/Kalshi Dashboard Data"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Kalshi ROAS Dashboard — Data Sync"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Step 1: Copy CSVs from the desktop source folder
if [ -d "$SOURCE_FOLDER" ]; then
    AGG=$(ls "$SOURCE_FOLDER"/liftoff_roas*.csv 2>/dev/null | head -1)
    CAMP=$(ls "$SOURCE_FOLDER"/liftoff_campaign_roas*.csv 2>/dev/null | head -1)

    if [ -n "$AGG" ]; then
        cp "$AGG" "$DATA_DIR/liftoff_roas.csv"
        echo "✓ Copied aggregate file: $(basename "$AGG")"
    else
        echo "⚠  No liftoff_roas*.csv found in '$SOURCE_FOLDER'"
    fi

    if [ -n "$CAMP" ]; then
        cp "$CAMP" "$DATA_DIR/liftoff_campaign_roas.csv"
        echo "✓ Copied campaign file:   $(basename "$CAMP")"
    else
        echo "⚠  No liftoff_campaign_roas*.csv found in '$SOURCE_FOLDER'"
    fi
else
    echo "⚠  Source folder not found: '$SOURCE_FOLDER'"
    echo "   Drop your CSVs directly into the data/ folder instead."
fi

echo ""

# Step 2: Push to GitHub
cd "$REPO_DIR"

if ! git diff --quiet data/ 2>/dev/null || git status --short data/ | grep -q .; then
    git add data/
    git commit -m "Data update $(date '+%Y-%m-%d %H:%M')"
    echo ""
    echo "Pushing to GitHub..."
    if git push; then
        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "  ✅  Done! Dashboard is now live."
        echo "  Refresh the link and you'll see the latest data."
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    else
        echo ""
        echo "❌  Push failed. Make sure you're connected to the internet"
        echo "   and GitHub Desktop is set up with your credentials."
    fi
else
    echo "No changes detected in data/ — nothing to push."
fi

echo ""
echo "Press any key to close..."
read -n 1
