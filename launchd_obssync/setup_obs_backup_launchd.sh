#!/bin/sh

# will need to run from scirpt dir

chmod u+x obs_backup.sh
mkdir ~/Library/LaunchAgents
cp obs_backup_launchd.plist ~/Library/LaunchAgents
launchctl load ~/Library/LaunchAgents/obs_backup_launchd.plist