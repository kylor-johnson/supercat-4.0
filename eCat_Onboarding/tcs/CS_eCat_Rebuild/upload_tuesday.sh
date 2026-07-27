#!/bin/bash
# Upload Tuesday-ready files to tcs FTP /data
# Usage: FTP_PASS='your-password' ./upload_tuesday.sh
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
HOST="${FTP_HOST:-ftp.supercatsolutions.com}"
USER="${FTP_USER:-tcs}"

if [[ -z "${FTP_PASS:-}" ]]; then
  echo "Set FTP_PASS (org FTP password from Admin Console → Company Settings)"
  exit 1
fi

for f in options.csv option_groups.csv products.csv stories.csv; do
  echo "Uploading $f ..."
  curl -sS --ftp-create-dirs -T "$DIR/$f" "ftp://$USER:$FTP_PASS@$HOST/data/$f"
  sleep 2
done

echo "Done. Import order: options → option_groups → products → stories"
echo "Check Admin → File Import Status after ~2 min, then verify with IMPORT_AND_VERIFY.md"
