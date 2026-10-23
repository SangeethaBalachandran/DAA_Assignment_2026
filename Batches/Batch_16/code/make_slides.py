"""Batch 16 - build slides.pdf from slides.html.

1. Fills {{TIMING_ROWS}} / {{LARGE_NOTE}} from results/*.csv, so the deck
   always shows the numbers the benchmark actually wrote.
2. Prints the filled HTML to slides.pdf with headless Google Chrome or
   Microsoft Edge (no extra Python dependency).
3. Optionally (--preview DIR) renders every page to PNG with PyMuPDF so the
   pages can be inspected.

Run from the Batch_16 folder:  python -B code/make_slides.py
"""

from __future__ import annotations

import argparse
import csv
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

BATCH = pathlib.Path(__file__).resolve().parent.parent
BROWSERS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "msedge", "google-chrome", "chromium", "chrome",
]


def find_browser() -> str:
    for cand in BROWSERS:
        if os.path.isfile(cand) or shutil.which(cand):
            return cand
    raise SystemExit("No Edge/Chrome found for headless PDF printing.")


def fill_template(html: str) -> str:
    with open(BATCH / "results" / "timing.csv", newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    table = "\n        ".join(
        f"<tr><td>{int(r['n']):,}</td><td>{float(r['time_chosen_ms']):.2f}</td>"
        f"<td>{float(r['time_rejected_ms']):.2f}</td></tr>" for r in rows)
    note = "Production scale was analysed asymptotically."
    large = BATCH / "results" / "large_scale.csv"
    if large.exists():
        with open(large, newline="", encoding="utf-8") as fh:
            big = list(csv.DictReader(fh))
        parts = [f"n = {int(r['n']):,}: {float(r['time_chosen_ms']) / 1000:.2f} s"
                 for r in big]
        note = ("Chosen algorithm at larger n (CPython, median of 3): "
                + "; ".join(parts) + ". This shows the pure-Python constant "
                "factor and does not represent a cluster measurement.")
    return html.replace("{{TIMING_ROWS}}", table).replace("{{LARGE_NOTE}}", note)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--preview", help="directory for per-page PNG previews")
    args = parser.parse_args(argv)

    html = fill_template((BATCH / "slides.html").read_text(encoding="utf-8"))
    pdf = BATCH / "slides.pdf"
    # The filled copy lives next to slides.html so relative image paths work.
    filled = BATCH / "_slides_filled.html"
    filled.write_text(html, encoding="utf-8")
    try:
        with tempfile.TemporaryDirectory() as profile:
            subprocess.run(
                [find_browser(), "--headless=new", "--disable-gpu",
                 "--no-pdf-header-footer", "--run-all-compositor-stages-before-draw",
                 f"--user-data-dir={profile}", f"--print-to-pdf={pdf}",
                 filled.as_uri()],
                check=True, timeout=180,
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    finally:
        filled.unlink(missing_ok=True)
    if not pdf.exists() or pdf.stat().st_size == 0:
        raise SystemExit("PDF generation failed")
    print(f"wrote {pdf} ({pdf.stat().st_size:,} bytes)")

    if args.preview:
        import pymupdf
        out = pathlib.Path(args.preview)
        out.mkdir(parents=True, exist_ok=True)
        doc = pymupdf.open(pdf)
        for i, page in enumerate(doc, start=1):
            page.get_pixmap(dpi=60).save(out / f"slide_{i:02d}.png")
        print(f"{doc.page_count} pages; previews in {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
