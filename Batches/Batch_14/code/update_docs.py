"""Refresh benchmark numbers in README.md and slides.pptx from results/timing.csv.
Called automatically at the end of benchmark.py. Needs: pip install python-pptx (slides only)."""
import csv, os, re, shutil, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
S, E = "<!--BENCH-START-->", "<!--BENCH-END-->"


def load():
    return list(csv.DictReader(open(os.path.join(ROOT, "results", "timing.csv"))))


def summary(rows):
    f = lambda r, k: float(r[k])
    last, r15 = rows[-1], next(r for r in rows if r["n"] == "15")
    us = [f(r, "time_chosen_ms") * 1000 / int(r["bt_assignments_examined"]) for r in rows]
    return (f"Measured on this machine: exhaustive search needs {f(r15,'time_rejected_ms'):.1f} ms at n = 15 and "
            f"{f(last,'time_rejected_ms'):.1f} ms at n = {last['n']}; backtracking needs {f(r15,'time_chosen_ms'):.1f} ms and "
            f"{f(last,'time_chosen_ms'):.1f} ms, a speed-up of {f(last,'time_rejected_ms')/f(last,'time_chosen_ms'):.0f}x at n = {last['n']}. "
            f"Backtracking cost is about {min(us):.2f}-{max(us):.2f} µs per assignment examined.")


def update_readme(rows):
    p = os.path.join(ROOT, "README.md")
    t = open(p, encoding="utf-8").read()
    if S not in t:
        print("README markers not found; skipped"); return
    tab = ("| n | backtracking (ms) | exhaustive (ms) | speed-up | valid configs | BT assignments examined | exhaustive configs (2^n) |\n"
           "|---|---|---|---|---|---|---|\n")
    for r in rows:
        tab += (f"| {r['n']} | {r['time_chosen_ms']} | {r['time_rejected_ms']} | "
                f"{float(r['time_rejected_ms'])/float(r['time_chosen_ms']):.1f}x | {r['valid_configs']} | "
                f"{r['bt_assignments_examined']} | {r['exhaustive_configs_checked']} |\n")
    block = f"{S}\n{tab}\n{summary(rows)}\n{E}"
    t = re.sub(re.escape(S) + r".*?" + re.escape(E), lambda m: block, t, flags=re.S)
    open(p, "w", encoding="utf-8").write(t)
    print("README.md updated")


def update_slides(rows):
    p = os.path.join(ROOT, "slides.pptx")
    try:
        from pptx import Presentation
    except ImportError:
        print("python-pptx not installed; slides skipped"); return
    if not os.path.exists(p): return
    prs = Presentation(p)
    sl = prs.slides[13]
    last = rows[-1]; r15 = next(r for r in rows if r["n"] == "15")
    for sh in sl.shapes:
        if sh.has_table:
            t = sh.table
            for i, r in enumerate(rows, 1):
                vals = [r["n"], r["time_chosen_ms"], r["time_rejected_ms"],
                        f"{float(r['time_rejected_ms'])/float(r['time_chosen_ms']):.1f}x"]
                for j, v in enumerate(vals):
                    t.cell(i, j).text_frame.paragraphs[0].runs[0].text = v
        elif sh.has_text_frame and sh.text_frame.text.startswith("Exhaustive time"):
            ps = sh.text_frame.paragraphs
            ps[0].runs[0].text = (f"Exhaustive time ×≈4 per +2 features (2^n): {float(r15['time_rejected_ms']):.0f} ms at n = 15 "
                                  f"→ {float(last['time_rejected_ms'])/1000:.1f} s at n = {last['n']}.")
            ps[1].runs[0].text = (f"Backtracking time ∝ assignments examined (≈1 µs each), far below 2^n: "
                                  f"{int(last['bt_assignments_examined']):,} vs {int(last['exhaustive_configs_checked']):,} at n = {last['n']}.")
    prs.save(p)
    print("slides.pptx updated (slide 14)")
    exe = shutil.which("soffice") or shutil.which("libreoffice")
    if exe:
        subprocess.run([exe, "--headless", "--convert-to", "pdf", "--outdir", ROOT, p], capture_output=True)
        print("slides.pdf regenerated")
    else:
        print("LibreOffice not found: re-export slides.pptx to slides.pdf manually (File > Save as PDF)")


def update_script(rows):
    p = os.path.join(ROOT, "presentation_script.md")
    if not os.path.exists(p): return
    t = open(p, encoding="utf-8").read()
    a, b = "<!--SCRIPT14-START-->", "<!--SCRIPT14-END-->"
    if a not in t:
        print("script markers not found; skipped"); return
    f = lambda r, k: float(r[k])
    last, r15 = rows[-1], next(r for r in rows if r["n"] == "15")
    para = (f"**Slide 14 (0:50).** \"Benchmark, median of five runs. The first size is the real ECU; 9 to 21 features are seeded "
            f"synthetic instances. Exhaustive time grows about four times per two extra features: {f(r15,'time_rejected_ms'):.0f} ms at 15 "
            f"features to {f(last,'time_rejected_ms')/1000:.1f} seconds at {last['n']}. Backtracking took {f(r15,'time_chosen_ms'):.0f} ms at 15 "
            f"and {f(last,'time_chosen_ms'):.0f} ms at {last['n']}. Its time follows the assignments examined, about a microsecond each: "
            f"{int(last['bt_assignments_examined']):,} against {int(last['exhaustive_configs_checked']):,} at n = {last['n']}, a "
            f"{f(last,'time_rejected_ms')/f(last,'time_chosen_ms'):.0f}-times speed-up. Limits: noise below a millisecond at small n, "
            f"the instances are synthetic, and exhaustive search at 30 features was not run.\"")
    block = f"{a}\n{para}\n{b}"
    t = re.sub(re.escape(a) + r".*?" + re.escape(b), lambda m: block, t, flags=re.S)
    open(p, "w", encoding="utf-8").write(t)
    print("presentation_script.md updated (slide 14)")


if __name__ == "__main__":
    rows = load(); update_readme(rows); update_script(rows); update_slides(rows)
