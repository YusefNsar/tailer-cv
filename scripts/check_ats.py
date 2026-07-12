#!/usr/bin/env python3
"""Check ATS keyword coverage on a rendered CV PDF.

Extracts all page text via pypdf and checks each requirement line from a
keywords file against it. Each line is `required:` or `preferred:` followed
by a term, or a `|`-separated group of synonyms (any one counts as covered).

This is a diligence gate, not a pass/fail gate like check_layout.py: some
required keywords will be genuinely absent from real experience, and forcing
100% coverage would push toward fabrication. Exit code is always 0 — read
the printed report and act on it (weave in truthful matches, or record the
gap in changes.md).
"""
import sys

from pypdf import PdfReader


def parse_keywords(path: str) -> list[tuple[str, list[str]]]:
    requirements = []
    with open(path, encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            tag, _, rest = line.partition(":")
            tag = tag.strip().lower()
            if tag not in ("required", "preferred"):
                print(f"warning: skipping malformed line: {raw_line!r}", file=sys.stderr)
                continue
            synonyms = [s.strip() for s in rest.split("|") if s.strip()]
            if not synonyms:
                print(f"warning: skipping empty entry: {raw_line!r}", file=sys.stderr)
                continue
            requirements.append((tag, synonyms))
    return requirements


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: check_ats.py <path/to/cv.pdf> <path/to/keywords.txt>", file=sys.stderr)
        sys.exit(2)

    pdf_path, keywords_path = sys.argv[1], sys.argv[2]
    requirements = parse_keywords(keywords_path)

    reader = PdfReader(pdf_path)
    text = "\n".join(page.extract_text() or "" for page in reader.pages).lower()

    counts = {"required": [0, 0], "preferred": [0, 0]}
    for tag, synonyms in requirements:
        covered = any(s.lower() in text for s in synonyms)
        counts[tag][0] += int(covered)
        counts[tag][1] += 1
        label = "COVERED" if covered else "MISSING"
        term = " | ".join(synonyms)
        print(f"{label} {tag}: {term}")

    print()
    for tag in ("required", "preferred"):
        got, total = counts[tag]
        if total:
            print(f"{tag}: {got}/{total} covered")

    sys.exit(0)


if __name__ == "__main__":
    main()
