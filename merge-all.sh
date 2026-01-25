#!/bin/bash
branches=(
  "origin/jmikedupont2-patch-2"
  "origin/jmikedupont2-patch-3"
  "origin/jmikedupont2-patch-4"
  "origin/jmikedupont2-patch-5"
  "origin/jmikedupont2-patch-6"
  "origin/jmikedupont2-patch-7"
  "origin/jmikedupont2-patch-8"
  "origin/jmikedupont2-patch-9"
  "origin/jmikedupont2-patch-10"
  "origin/jmikedupont2-patch-11"
  "origin/jmikedupont2-patch-12"
  "origin/jmikedupont2-patch-13"
  "origin/jmikedupont2-patch-14"
  "origin/jmikedupont2-patch-15"
  "origin/jmikedupont2-patch-16"
  "origin/jmikedupont2-patch-17"
  "origin/jmikedupont2-patch-18"
  "origin/jmikedupont2-patch-19"
  "origin/jmikedupont2-patch-20"
  "origin/jmikedupont2-patch-3-universe-of-universes"
  "origin/jmikedupont2-patch-6-monster"
  "origin/jmikedupont2-patch-12-genesis"
  "origin/jmikedupont2-goedel-golem"
  "origin/feature/CRQ-016-nixify-workflow"
  "origin/docs"
  "origin/emojis"
  "origin/209-use-cursor"
  "origin/example/scripts/meta-introspector/meta-meme/github/export/discussion/21/head"
)

for branch in "${branches[@]}"; do
  echo "Merging $branch..."
  git merge "$branch" --no-edit -X ours || {
    git add .
    git commit -m "Merge $branch with conflicts resolved"
  }
done
