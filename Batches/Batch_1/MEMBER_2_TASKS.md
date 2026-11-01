# MEMBER_2_TASKS.md — Batch 1 (Fintech Audit)

Member 2: you are not a proofreader. Your marks are individual and depend on **your own commits, your rows in the contribution table, and your part of the video**. Every task below produces something you can point to. Do the work yourself rather than copying Member 1's code; where a task says "independently", write it before you read Member 1's version.

Folder: `Batches/Batch_1/` · Python 3.9+ · commands are run inside `code/` (see `code/RUN.md`).

## Status note
The technical checks in tasks 1–10 have been executed and recorded in `extras/MEMBER2_VERIFICATION.md` (script: `code/verify_independent.py`). That record is a starting point: **you still have to re-run it on your own machine, read and understand it, do tasks 7, 11, 12, 13 and 14 yourself (your own commits, your own voice, your own timing run), and be ready to explain every part in the viva.** Individual marks depend on your own commit history and your part of the video.

## What already exists (Member 1's package)
`README.md` (report draft), `code/main_solution.py`, `code/rejected_alternative.py`, `code/generate_inputs.py`, `code/benchmark.py`, `code/test_all.py`, `code/analysis_tools.py`, `code/extra_experiments.py`, `code/make_trace.py`, `results/timing.csv`, `results/timing_large_n.csv`, `results/timing_plot.png`, `results/search_tree.png`, `slides.pdf` (13 slides), `extras/TRACE.md`, `extras/SPEAKER_SCRIPT.md`.

The committed timings were measured in a Linux sandbox (Python 3.12.3). **They are not your laptop's numbers.** Task 7 asks you to reproduce them on your machine.

## Tasks

| # | Task | Exact action | Expected output | File / report section | How to verify completion | Evidence for the contribution table |
|---|------|--------------|-----------------|-----------------------|--------------------------|--------------------------------------|
| 1 | **Implement brute force independently** | Without opening `rejected_alternative.py`, write your own `my_brute.py`: for every subset of `n` items (bitmask or `itertools`) test `lo ≤ sum ≤ hi`, skip the empty subset, return **sorted tuples of 0-based original indices**. Then compare with the existing file and keep the better-documented version (or merge ideas) in `rejected_alternative.py`. | A working brute force you wrote; if you improve the shared file, a commit that changes it. | `code/rejected_alternative.py`; report §10 | `python rejected_alternative.py` prints 2 solutions and `Subsets tested: 128`; your function returns the same list as `brute_force_solve` on 20 random inputs. | Commit message e.g. "Batch_1: independent brute force + comparison test"; one line in the table: "wrote/verified brute-force alternative". |
| 2 | **Verify outputs against the pruned search** | Write `compare_check.py` (a short script) that generates 200 random small inputs (`n ≤ 12`, amounts 1–40, random target, tolerance in `{0, 1, 5}`), runs both solvers and asserts equal solution lists. Include inputs with duplicated amounts. | Script prints `OK` after 200 cases. | new file `code/compare_check.py` (optional to keep) | The assertion passes; deliberately break one pruning line locally (e.g. change `>` to `>=` in the overshoot test) and confirm your script **fails**, then undo. | Commit of the script; note "found failure when pruning was broken" in your notes. |
| 3 | **Independently verify the solution list** | By hand (no code), find all subsets of `{15,22,35,40,48,53,61}` summing to 110. Suggested method: write all subsets by size (pairs, triples, quadruples…) and note that `15+22+35+40 = 112 > 110`. | Exactly 2 subsets: `{22,35,53}`, `{22,40,48}`. | README §7; `extras/TRACE.md` | Matches both programs. Also check the claim "no pair and no 4+ set works". | A short hand-written working (photo or markdown) kept in your notes; one table line. |
| 4 | **Review data-structure comparison and technique rejections** | Read README §2 and §4. For each claim, check the arithmetic yourself: `(n+1)(T+1)` for n = 40, T = 10⁹; 41 GB vs 5.1 GB; `2⁴⁰` vs `n·T`; greedy trace 61 → 48 → remainder 1. Look for any sentence that says a technique "cannot" solve the problem when it can. Write at least **3 concrete improvements or corrections** and apply them. | A reviewed §2 and §4 with your edits. | README §2, §4 | Run `python extra_experiments.py`; the last block prints the DP numbers. Your edits appear in `git diff`. | Commit "Batch_1: review of §2 and §4" and a list of what you changed. |
| 5 | **Build and verify a difficult input** | Using only the description in README §9, write your own generator for the hard family, run the main solver, and check `states == C(n, ⌊n/2⌋)` for n = 8, 12, 16, 20. Then propose **one more** hard input of your own (for example all amounts equal, target half the total) and report its states and solutions. | Table of your own measurements. | README §9; optionally `code/generate_inputs.py` | Your numbers equal the README table for n = 10, 14, 18, 22. | Commit of your generator or table; one line in the table. |
| 6 | **Execute or review the benchmark** | Read `code/benchmark.py`. Confirm: same input to both algorithms, timed region excludes printing, median used, correctness check before timing. Write down one weakness (for example only 5 inputs per n in the random family) and one possible fix. | Written review (5–10 lines) in your notes or README §10. | `code/benchmark.py`; README §10 | You can explain each line of `median_ms` and `measure` to the instructor. | Commit with the review text; table line "reviewed benchmark design". |
| 7 | **Regenerate or verify `timing.csv` and `timing_plot.png`** | Run `python benchmark.py` on your own computer. Compare with the committed CSV. If your absolute times differ (they will), commit the **new** `timing.csv` **and** `timing_plot.png` **together**, and update the numbers quoted in README §10 and slides 10–11. If you keep Member 1's files, state in §10 that you re-ran and the shapes agree. | CSV with ≥ 5 sizes; plot with labelled axes, legend, title. | `results/timing.csv`, `results/timing_plot.png`, README §10 | The plot's points equal the CSV values; `time_chosen_ms` and `time_rejected_ms` columns exist; ratios in the README match the CSV. | Commit of the regenerated files + your machine description (CPU, Python version). |
| 8 | **Review the correctness proof and complexity derivation** | Read README §6 and §8. Rewrite Lemma A, Lemma B and the induction in your own words (half a page). Test the proof on a tiny example: `[5,5,5,10]`, target 10, by hand, and say where each lemma applies. Check the hockey-stick derivation in §9 for `n = 6`: states should be `C(6,3) = 20`. | Half-page summary + verified example. | README §6, §8, §9 | `python test_all.py` prints `ALL TESTS PASS`; you can answer "why does the loop `break` and not `continue`?" | Commit of your summary; table line "reviewed proof and complexity". |
| 9 | **Verify the changed-requirement results** | Run `python main_solution.py --tolerance 50` and the hypothetical amounts from README §11 with `--scale 1`: `python main_solution.py --amounts 15020 22000 35000 39990 48000 53030 61000 --target 110000 --scale 1 --tolerance 50`. Check by hand that `22000+35000+53030 = 110030` and `22000+39990+48000 = 109990`. Try one more input of your own where the answer changes. | Your verified table of solutions and states. | README §11 | Your outputs equal the README (35 states; 2 solutions in both cases for the original; 0 vs 2 for the hypothetical). | Commit adding your extra example to §11; table line. |
| 10 | **Research and validate the real-world reference** | Open the DOIs in README §13 yourself: Horowitz & Sahni (10.1145/321812.321823), Golomb & Baumert (10.1145/321296.321300), and the Python `itertools` page. Confirm authors, year, journal and pages. Read the Horowitz–Sahni abstract and check that the sentence about "all combinations that sum to M" is accurate. If you find a better reference, replace it. | Verified reference list. | README §13 | Every link opens in a private window; every claim in §13 is supported by the page you read. | Commit "Batch_1: verified references"; table line. |
| 11 | **Prepare the slides allocated to you** | You present slides 8–13. A full draft is in `slides.pdf` and `extras/SPEAKER_SCRIPT.md`. Make them yours: rewrite each script in your own words, check each number against the CSV/report, and fix anything you cannot justify. Keep ≤ 12 minutes in total with Member 1's part. | Your edited script and (if you change the slides) a regenerated `slides.pdf`. | `slides.pdf`; `extras/SPEAKER_SCRIPT.md` | Time yourself reading slides 8–13: about 5:00. | Commit of the edited script; table row "Part presented: slides 8–13". |
| 12 | **Present your part of the recorded video** | Record slides 8–13 with your voice (face optional). Member 1 records slides 1–7; join the two parts or record one session. | Video link, ≤ 12:00. | README "Presentation" section | Open the link in a private/incognito window; check sound; check duration. | The video itself (your voice) + the link in README. |
| 13 | **Make meaningful commits from your own account** | Commit your files separately (tasks 1, 2, 4, 5, 7, 9, 10, 11 give natural commits). At least 4 commits, each with a clear message and each touching real content. | Commit history under your GitHub username. | whole folder | `git log --author="<your name>" --oneline` shows them; GitHub "Commits" page shows your avatar. | Table column "GitHub username" matches your commits. |
| 14 | **Final review before submission** | Read `slides.pdf`, README top to bottom, `code/RUN.md`, and click the video link. Run every command in `RUN.md` on a clean checkout. Use `extras/FINAL_CHECKLIST.md`. | Tick-box list completed. | all | All boxes ticked; the only changes outside `Batches/Batch_1/` are none. | Final commit "Batch_1: final review fixes" and your sign-off in the PR description. |

## Dependency checklist

**Can start immediately, in parallel (no dependency on Member 1's remaining work):** tasks 1, 3, 5 (generator only), 10.

**Need Member 1's delivered package (already in the folder), then can proceed in parallel with each other:** 2 (needs `main_solution.py`), 4, 6, 8, 9.

**Need earlier tasks:** 7 needs 6 (so you understand what you are re-running); 11 needs 7 and 9 (numbers on your slides); 12 needs 11; 13 runs throughout; 14 needs everything, including the video link from 12.

**Needs both members:** merging the two video parts, filling the contribution table, the pull request.

Suggested schedule (deadline **30 October 2026**): finish 1, 3, 10 first; 2, 4, 5, 8, 9 next; 6, 7 after that; 11–12 two days before the deadline; 14 the day before.

## Contribution-table template (fill in your own words after finishing)

| Task | Evidence (commit link / file) |
|---|---|
| Independent brute force and comparison | `[link]` |
| Hand verification of solution list | `[link]` |
| Review of §2, §4, §6, §8 | `[link]` |
| Hard-input verification | `[link]` |
| Benchmark re-run / verification | `[link]` |
| Changed-requirement verification | `[link]` |
| Reference validation | `[link]` |
| Slides 8–13 and recorded part | `[video link]` |
