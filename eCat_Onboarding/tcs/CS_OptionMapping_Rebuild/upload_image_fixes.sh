#!/bin/bash
# Upload CopperSmith image fixes + import CSVs to the tcs FTP (org 291).
#
# Two stages, because they behave differently:
#   images  -> pushes converted JPGs to /images and /option_images. These are NOT
#              auto-applied; you trigger Admin Console -> Tools -> Import Images.
#   data    -> pushes the 4 CSVs to /data, which AUTO-IMPORTS on drop. Gated behind
#              an explicit arg + abort window so nothing imports until you approve.
#
# Usage:
#   FTP_PASS='...' ./upload_image_fixes.sh images   # safe: stage JPGs only
#   FTP_PASS='...' ./upload_image_fixes.sh data      # AUTO-IMPORTS CSVs (approve first!)
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
HOST="${FTP_HOST:-ftp.supercatsolutions.com}"
USER="${FTP_USER:-tcs}"
MODE="${1:-images}"

if [[ -z "${FTP_PASS:-}" ]]; then
  echo "Set FTP_PASS (org FTP password from Admin Console -> Company Settings)"
  exit 1
fi

upload_jpgs() {  # $1 = local dir, $2 = remote folder (flat root)
  local count=0
  shopt -s nullglob
  for f in "$1"/*.jpg; do
    curl -sS --ftp-create-dirs -T "$f" "ftp://$USER:$FTP_PASS@$HOST/$2/$(basename "$f")"
    count=$((count + 1))
  done
  echo "  uploaded $count .jpg file(s) to /$2"
}

case "$MODE" in
  images)
    echo "Staging product JPGs -> /images ..."
    upload_jpgs "$DIR/images_upload" images
    echo "Staging option JPGs -> /option_images ..."
    upload_jpgs "$DIR/option_images_upload" option_images
    echo
    echo "Images staged. In the Admin Console (org tcs):"
    echo "  Tools -> Import Images -> Product Photos   (processes /images, ~30-45 min)"
    echo "  Tools -> Import Images -> Option Photo      (processes /option_images, 300x300)"
    echo "Verify: Tools -> Admin Reports -> File Import Status (blue link = problems)."
    echo
    echo "NOTE: wall-mount.jpg / ceiling-mount.jpg / post-mount.jpg are eCat mount-meta"
    echo "swatches not staged here -- confirm they already exist in /option_images."
    echo
    echo "Only after images are confirmed AND you approve the data import, run:"
    echo "  FTP_PASS=... $0 data"
    ;;
  data)
    echo "!! Dropping CSVs into /data AUTO-IMPORTS them on the server."
    echo "!! Ctrl-C within 8s to abort."
    sleep 8
    # Mandatory order (ecat-ground-truth): options -> option_groups -> products -> stories.
    # option_groups MUST follow options because importing options nulls group membership.
    for f in options.csv option_groups.csv products.csv stories.csv; do
      echo "Uploading $f ..."
      curl -sS --ftp-create-dirs -T "$DIR/$f" "ftp://$USER:$FTP_PASS@$HOST/data/$f"
      echo "  uploaded; waiting 120s for import ..."
      sleep 120
    done
    echo "Done. Check Admin -> Admin Reports -> File Import Status for any Fatal/Error rows."
    ;;
  *)
    echo "Usage: FTP_PASS='...' $0 [images|data]"
    exit 1
    ;;
esac
