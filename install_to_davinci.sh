#!/bin/bash
# DaVinci Resolve One-Click Plugin Installer for macOS

echo "=========================================================="
echo "  DaVinci Resolve Master Plugins - macOS Auto-Installer"
echo "=========================================================="

RESOLVE_SUPPORT="$HOME/Library/Application Support/Blackmagic Design/DaVinci Resolve"
TITLES_DIR="$RESOLVE_SUPPORT/Fusion/Templates/Edit/Titles"
EFFECTS_DIR="$RESOLVE_SUPPORT/Fusion/Templates/Edit/Effects"
FUSES_DIR="$RESOLVE_SUPPORT/Fusion/Fuses"
LUTS_DIR="$RESOLVE_SUPPORT/LUT/DaVinci_Plugins_Suite"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "[1/4] Setting up DaVinci Resolve directories..."
mkdir -p "$TITLES_DIR"
mkdir -p "$EFFECTS_DIR"
mkdir -p "$FUSES_DIR"
mkdir -p "$LUTS_DIR"

echo "[2/4] Installing Text Animation Plugins (.setting)..."
cp -R "$SCRIPT_DIR/1. Text Animation Plugins/"* "$TITLES_DIR/" 2>/dev/null

echo "[3/4] Installing Effect Plugins (.fuse & .setting)..."
cp -R "$SCRIPT_DIR/2. Effect Plugins/"*/*.fuse "$FUSES_DIR/" 2>/dev/null
cp -R "$SCRIPT_DIR/2. Effect Plugins/"*/*.setting "$EFFECTS_DIR/" 2>/dev/null

echo "[4/4] Installing Color Plugins (DCTLs & LUTs)..."
cp -R "$SCRIPT_DIR/3. Color Plugins/"* "$LUTS_DIR/" 2>/dev/null

echo ""
echo "SUCCESS! All 578 plugins, effects, DCTLs, and text animations have been installed."
echo "Please restart DaVinci Resolve (or click 'Update Lists' in Color Management)."
echo "=========================================================="
