#!/usr/bin/env python3
"""Check CV pagination constraints on a rendered PDF.

Must-haves: at most 2 pages, and all 4 Professional Experience entries on
page 1. Epicore is the oldest employer and always sorts last in
`Professional Experience`, so its presence on page 1 is used as a stand-in
for "all 4 entries fit" (update MARKER if the master cv.yaml's oldest
employer ever changes).
"""
import sys

from pypdf import PdfReader

#! always change to the name of the last company in your experience
MARKER = "Epicore"
MAX_PAGES = 2


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: check_layout.py <path/to/cv.pdf>", file=sys.stderr)
        sys.exit(2)

    reader = PdfReader(sys.argv[1])
    num_pages = len(reader.pages)
    page1_text = reader.pages[0].extract_text() or ""

    ok = True
    print(f"pages={num_pages}")
    if num_pages > MAX_PAGES:
        print(f"FAIL: {num_pages} pages exceeds the {MAX_PAGES}-page limit")
        ok = False

    if MARKER in page1_text:
        print(f"PASS: all 4 Professional Experience entries fit on page 1 ({MARKER} found on page 1)")
    else:
        print(f"FAIL: {MARKER} (4th Professional Experience entry) not found on page 1")
        ok = False

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
