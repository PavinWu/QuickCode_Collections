#!/bin/sh

# Note: Created partially by Gemini.

set -e # Exit immediately if a command exits with a non-zero status.

# Get the absolute path to the directory where this setup script is located.
# Note to self: $() - spawns a subshell, ${} - groupping expression.
# https://stackoverflow.com/questions/8748831/when-do-we-need-curly-braces-around-shell-variables
# https://unix.stackexchange.com/questions/726866/curly-braces-meaning
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
BACKUP_SCRIPT_PATH="$SCRIPT_DIR/obs_backup.sh"
LAUNCHD_PLIST="obs_backup_launchd.plist"

# Setup the backup script
chmod u+x "$BACKUP_SCRIPT_PATH"
mkdir -p ~/Library/LaunchAgents

PLIST_SOURCE="$SCRIPT_DIR/$LAUNCHD_PLIST"
PLIST_DEST="$HOME/Library/LaunchAgents/$LAUNCHD_PLIST"

# Update plist file
sed -e "s|__SCRIPT_PATH__|${BACKUP_SCRIPT_PATH}|g" \
    -e "s|__HOME_DIR__|${HOME}|g" \
    "$PLIST_SOURCE" > "$PLIST_DEST"

# Reload agent
launchctl unload "$PLIST_DEST" 2>/dev/null || true
launchctl load "$PLIST_DEST"