#!/bin/sh

pushd ~/Sync/ObsidianNotes

git pull --prune
git add --all
git commit -m "vault backup: $(date)"
git push

popd