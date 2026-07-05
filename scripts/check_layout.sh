#!/usr/bin/env bash
# Render a cv.yaml (merged with the shared cv-format.yaml) to a scratch PDF
# and check pagination: the CV must be <= 2 pages, and all 4 Professional
# Experience entries must fit on page 1 (checked via scripts/check_layout.py,
# which looks for "Epicore", the last entry, on page 1).
#
# This only renders to a scratch dir for inspection — it does not touch the
# application folder's final PDF.
#
# Usage: scripts/check_layout.sh <path/to/cv.yaml>
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
YAML_FILE="${1:?Usage: check_layout.sh <path/to/cv.yaml>}"
FORMAT_FILE="$REPO_ROOT/cv-format.yaml"
APP_DIR="$(cd "$(dirname "$YAML_FILE")" && pwd)"

if [[ ! -f "$YAML_FILE" ]]; then
  echo "error: $YAML_FILE not found" >&2
  exit 1
fi

FONTS_COPIED=0
if [[ ! -e "$APP_DIR/fonts" ]]; then
  cp -r "$REPO_ROOT/fonts" "$APP_DIR/fonts"
  FONTS_COPIED=1
fi

TMP_DIR="$(mktemp -d)"
cleanup() {
  rm -rf "$TMP_DIR"
  if [[ "$FONTS_COPIED" -eq 1 ]]; then
    rm -rf "$APP_DIR/fonts"
  fi
}
trap cleanup EXIT

rendercv render "$YAML_FILE" -d "$FORMAT_FILE" -lc "$FORMAT_FILE" -s "$FORMAT_FILE" -o "$TMP_DIR" -nomd -nohtml -nopng -q

PDF_FILE="$(find "$TMP_DIR" -maxdepth 1 -name '*.pdf' | head -n1)"
if [[ -z "$PDF_FILE" ]]; then
  echo "error: rendercv did not produce a PDF" >&2
  exit 1
fi

python3 "$REPO_ROOT/scripts/check_layout.py" "$PDF_FILE"
