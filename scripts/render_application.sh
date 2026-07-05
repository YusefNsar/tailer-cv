#!/usr/bin/env bash
# Render the tailored cv.yaml (cv: section only) inside an
# applications/<Company - Job Title>/ folder into a PDF named
# Yusef_Nsar-<Job_Title>.pdf, placed in that same folder.
#
# Formatting (design/locale/settings) is shared from the repo-root
# cv-format.yaml. Calibri is only resolved by Typst when the fonts/
# folder sits next to the input YAML, so it's temporarily copied in.
#
# Usage: scripts/render_application.sh "applications/Acme - Senior Backend Engineer" "Senior Backend Engineer"
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APP_DIR="${1:?Usage: render_application.sh <application_folder> <job_title>}"
JOB_TITLE="${2:?Usage: render_application.sh <application_folder> <job_title>}"

YAML_FILE="$APP_DIR/cv.yaml"
FORMAT_FILE="$REPO_ROOT/cv-format.yaml"
if [[ ! -f "$YAML_FILE" ]]; then
  echo "error: $YAML_FILE not found" >&2
  exit 1
fi
if [[ ! -f "$FORMAT_FILE" ]]; then
  echo "error: $FORMAT_FILE not found" >&2
  exit 1
fi

SLUG="$(echo "$JOB_TITLE" | tr ' -' '__' | tr -s '_')"
TMP_DIR="$(mktemp -d)"

FONTS_COPIED=0
if [[ ! -e "$APP_DIR/fonts" ]]; then
  cp -r "$REPO_ROOT/fonts" "$APP_DIR/fonts"
  FONTS_COPIED=1
fi

cleanup() {
  rm -rf "$TMP_DIR"
  if [[ "$FONTS_COPIED" -eq 1 ]]; then
    rm -rf "$APP_DIR/fonts"
  fi
}
trap cleanup EXIT

rendercv render "$YAML_FILE" -d "$FORMAT_FILE" -lc "$FORMAT_FILE" -s "$FORMAT_FILE" -o "$TMP_DIR" -nomd -nohtml -nopng -q

PDF_SRC="$(find "$TMP_DIR" -maxdepth 1 -name '*.pdf' | head -n1)"
if [[ -z "$PDF_SRC" ]]; then
  echo "error: rendercv did not produce a PDF" >&2
  exit 1
fi

PDF_DEST="$APP_DIR/Yusef_Nsar-$SLUG.pdf"
mv "$PDF_SRC" "$PDF_DEST"
echo "Rendered: $PDF_DEST"

DESKTOP_DIR="/mnt/c/Users/yusef/Desktop"
if [[ -d "$DESKTOP_DIR" ]]; then
  cp -f "$PDF_DEST" "$DESKTOP_DIR/$(basename "$PDF_DEST")"
  echo "Copied to: $DESKTOP_DIR/$(basename "$PDF_DEST")"
else
  echo "warning: $DESKTOP_DIR not found, skipped desktop copy" >&2
fi
