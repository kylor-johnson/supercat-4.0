#!/bin/bash
set -euo pipefail

REPO_ROOT="/Users/brentsanders/sites/supercat/supercat_server"
WORKTREE_BASE="/tmp/supercat-review"

usage() {
  echo "Usage:"
  echo "  $0 <branch-name>              # Create worktree and install deps"
  echo "  $0 --cleanup <branch-name>    # Remove worktree"
  echo "  $0 --list                     # List active review worktrees"
  exit 1
}

if [ $# -lt 1 ]; then
  usage
fi

if [ "$1" = "--list" ]; then
  git -C "$REPO_ROOT" worktree list | grep "$WORKTREE_BASE" || echo "No active review worktrees."
  exit 0
fi

if [ "$1" = "--cleanup" ]; then
  [ $# -lt 2 ] && usage
  BRANCH="$2"
  WORKTREE_DIR="${WORKTREE_BASE}-${BRANCH}"

  if [ -d "$WORKTREE_DIR" ]; then
    git -C "$REPO_ROOT" worktree remove "$WORKTREE_DIR" --force 2>/dev/null || true
    echo "Removed worktree: $WORKTREE_DIR"
  else
    echo "Worktree not found: $WORKTREE_DIR"
  fi
  exit 0
fi

BRANCH="$1"
WORKTREE_DIR="${WORKTREE_BASE}-${BRANCH}"

if [ -d "$WORKTREE_DIR" ]; then
  echo "Worktree already exists at $WORKTREE_DIR"
  echo "To recreate, run: $0 --cleanup $BRANCH && $0 $BRANCH"
  exit 0
fi

git -C "$REPO_ROOT" fetch origin "$BRANCH" 2>/dev/null || true

if ! git -C "$REPO_ROOT" rev-parse --verify "$BRANCH" >/dev/null 2>&1; then
  if git -C "$REPO_ROOT" rev-parse --verify "origin/$BRANCH" >/dev/null 2>&1; then
    git -C "$REPO_ROOT" branch "$BRANCH" "origin/$BRANCH" 2>/dev/null || true
  else
    echo "Error: Branch '$BRANCH' not found locally or on origin."
    exit 1
  fi
fi

git -C "$REPO_ROOT" worktree add "$WORKTREE_DIR" "$BRANCH"

cd "$WORKTREE_DIR"
echo "Installing bundle (reusing system gems)..."
bundle install --quiet 2>/dev/null || echo "WARN: bundle install had issues — rubocop may still work"

echo ""
echo "Worktree ready at: $WORKTREE_DIR"
echo "Run review commands with: cd $WORKTREE_DIR"
echo ""
echo "When done, clean up with:"
echo "  $0 --cleanup $BRANCH"
