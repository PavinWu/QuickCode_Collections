#!/bin/sh

pushd ~/Sync/ObsidianNotes

git pull --rebase --autostash
git add --all
git commit -m "vault backup: $(date)"
git push

popd