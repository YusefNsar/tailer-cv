#!/usr/bin/env python3
"""Render a plain-text letter (e.g. a cover letter) into a clean PDF.

Blank-line-separated blocks become paragraphs; a block whose every line
starts with "- " is rendered as a bullet list. Line breaks within a
non-bullet block (e.g. a sign-off) are preserved.

Usage: scripts/txt_to_pdf.py cover_letter.txt [output.pdf]
"""
import sys
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer


def main():
    if len(sys.argv) < 2:
        sys.exit("Usage: txt_to_pdf.py <input.txt> [output.pdf]")

    txt_path = Path(sys.argv[1])
    pdf_path = Path(sys.argv[2]) if len(sys.argv) > 2 else txt_path.with_suffix(".pdf")

    blocks = txt_path.read_text().strip("\n").split("\n\n")

    body_style = ParagraphStyle(
        "Body", fontName="Helvetica", fontSize=11, leading=16, spaceAfter=14
    )
    bullet_style = ParagraphStyle(
        "Bullet",
        parent=body_style,
        leftIndent=18,
        bulletIndent=0,
        spaceAfter=8,
    )

    story = []
    for block in blocks:
        lines = [line for line in block.split("\n") if line.strip()]
        if not lines:
            continue
        if all(line.startswith("- ") for line in lines):
            for line in lines:
                story.append(
                    Paragraph(escape(line[2:]), bullet_style, bulletText="•")
                )
            story.append(Spacer(1, 6))
        else:
            html = "<br/>".join(escape(line) for line in lines)
            story.append(Paragraph(html, body_style))

    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        topMargin=1 * inch,
        bottomMargin=1 * inch,
        leftMargin=1 * inch,
        rightMargin=1 * inch,
    )
    doc.build(story)
    print(f"Rendered: {pdf_path}")


if __name__ == "__main__":
    main()
