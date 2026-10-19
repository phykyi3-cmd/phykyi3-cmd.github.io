#!/bin/bash
# ==============================================================================
# Adobe After Effects Auto Installer for macOS
# Copies Presets (.ffx), Scripts (.jsx), and LUTs (.cube) into After Effects dirs
# ==============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=========================================================="
echo "  Adobe After Effects Master Plugin Pack - macOS Installer"
echo "=========================================================="
echo ""

# 1. Install Color LUTs (.cube)
LUT_DIR="/Library/Application Support/Adobe/Common/LUTs/Creative"
USER_LUT_DIR="$HOME/Library/Application Support/Adobe/Common/LUTs/Creative"

mkdir -p "$USER_LUT_DIR" 2>/dev/null
echo "[+] Copying 45+ Cinematic LUTs to Lumetri Creative folder..."
cp -v "$SCRIPT_DIR/3. Color Plugins/Cinematic Lumetri LUTs (.cube)/"* "$USER_LUT_DIR/" 2>/dev/null
echo "    -> Installed in: $USER_LUT_DIR"

if [ -w "$LUT_DIR" ]; then
    cp "$SCRIPT_DIR/3. Color Plugins/Cinematic Lumetri LUTs (.cube)/"* "$LUT_DIR/" 2>/dev/null
fi

# 2. Find After Effects versions in Documents
AE_DOCS="$HOME/Documents/Adobe"
FOUND_PRESETS=0

if [ -d "$AE_DOCS" ]; then
    for version_dir in "$AE_DOCS"/After\ Effects*; do
        if [ -d "$version_dir" ]; then
            USER_PRESETS="$version_dir/User Presets"
            mkdir -p "$USER_PRESETS/Text Animation" 2>/dev/null
            mkdir -p "$USER_PRESETS/Visual Effects" 2>/dev/null
            mkdir -p "$USER_PRESETS/Color Grading" 2>/dev/null

            echo "[+] Installing Presets into: $USER_PRESETS"
            cp -r "$SCRIPT_DIR/1. Text Animation Plugins/FFX Text Presets/"* "$USER_PRESETS/Text Animation/" 2>/dev/null
            cp -r "$SCRIPT_DIR/2. Effect Plugins/Visual Effects Presets (.ffx)/"* "$USER_PRESETS/Visual Effects/" 2>/dev/null
            cp -r "$SCRIPT_DIR/3. Color Plugins/Color Adjustment Presets (.ffx)/"* "$USER_PRESETS/Color Grading/" 2>/dev/null
            FOUND_PRESETS=1
        fi
    done
fi

if [ $FOUND_PRESETS -eq 0 ]; then
    DEFAULT_PRESETS="$HOME/Documents/Adobe/After Effects 2024/User Presets"
    mkdir -p "$DEFAULT_PRESETS/Text Animation" 2>/dev/null
    mkdir -p "$DEFAULT_PRESETS/Visual Effects" 2>/dev/null
    mkdir -p "$DEFAULT_PRESETS/Color Grading" 2>/dev/null
    cp -r "$SCRIPT_DIR/1. Text Animation Plugins/FFX Text Presets/"* "$DEFAULT_PRESETS/Text Animation/" 2>/dev/null
    cp -r "$SCRIPT_DIR/2. Effect Plugins/Visual Effects Presets (.ffx)/"* "$DEFAULT_PRESETS/Visual Effects/" 2>/dev/null
    cp -r "$SCRIPT_DIR/3. Color Plugins/Color Adjustment Presets (.ffx)/"* "$DEFAULT_PRESETS/Color Grading/" 2>/dev/null
    echo "[+] Created preset directory: $DEFAULT_PRESETS"
fi

# 3. Install Scripts & ScriptUI Panels
for app_dir in /Applications/Adobe\ After\ Effects*; do
    if [ -d "$app_dir" ]; then
        PANEL_DIR="$app_dir/Scripts/ScriptUI Panels"
        if [ -d "$PANEL_DIR" ] && [ -w "$PANEL_DIR" ]; then
            echo "[+] Copying Scripts into: $PANEL_DIR"
            cp "$SCRIPT_DIR/2. Effect Plugins/Ease and Wizz Animation Engine/"*.jsx "$PANEL_DIR/" 2>/dev/null
            cp "$SCRIPT_DIR/2. Effect Plugins/Kyle Martinez Motion Scripts/"*.jsx "$PANEL_DIR/" 2>/dev/null
            cp "$SCRIPT_DIR/2. Effect Plugins/Workflow & Automation Scripts/"*.jsx "$PANEL_DIR/" 2>/dev/null
        fi
    fi
done

# User level script directory
USER_SCRIPT_DIR="$HOME/Library/Application Support/Adobe/After Effects/Scripts/ScriptUI Panels"
mkdir -p "$USER_SCRIPT_DIR" 2>/dev/null
cp "$SCRIPT_DIR/2. Effect Plugins/Ease and Wizz Animation Engine/"*.jsx "$USER_SCRIPT_DIR/" 2>/dev/null
cp "$SCRIPT_DIR/2. Effect Plugins/Kyle Martinez Motion Scripts/"*.jsx "$USER_SCRIPT_DIR/" 2>/dev/null
cp "$SCRIPT_DIR/2. Effect Plugins/Workflow & Automation Scripts/"*.jsx "$USER_SCRIPT_DIR/" 2>/dev/null

echo ""
echo "=========================================================="
echo "  [SUCCESS] All After Effects Assets Successfully Copied!"
echo "  Restart After Effects to load your new presets & scripts."
echo "=========================================================="
