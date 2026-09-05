#!/bin/bash
# SuperCat Design System — local preview launcher (macOS)
# Double-click this file to start a local server and open the system in your browser.

set -e

cd "$(dirname "$0")"

PORT=8765

echo ""
echo "╭──────────────────────────────────────────────╮"
echo "│  SuperCat Design System — Preview            │"
echo "│  Serving at http://localhost:${PORT}/            │"
echo "│  Press ⌃C to stop.                           │"
echo "╰──────────────────────────────────────────────╯"
echo ""

# Open the browser after a short delay so the server is ready.
( sleep 0.6 && open "http://localhost:${PORT}/index.html" ) &

# Python 3 ships with macOS; fall back to python if needed.
if command -v python3 >/dev/null 2>&1; then
  python3 -m http.server $PORT --bind 127.0.0.1
elif command -v python >/dev/null 2>&1; then
  python -m SimpleHTTPServer $PORT
else
  echo "Python is required to run the local server."
  echo "Install it from https://python.org, or just open index.html directly."
  read -p "Press return to close." _
fi
