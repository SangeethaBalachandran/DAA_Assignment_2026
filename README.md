# DAA_Assignment_2026

Repository for DAA Assignments. Submit via fork and pull request, one submission per batch.

**Course:** 23I501 – Design and Analysis of Algorithms (DAA)
**Instructor:** Dr. B. Sangeetha
**Institution:** PSG College of Technology
**Semester:** Odd Semester (5th), Academic Year 2026–27
**Submission deadline:** `<30/10/2026>`
**Contact:** bsg.it@psgtech.ac.in

---

## Assignment overview

Each batch has **one industry scenario** (see the assignment document shared in class). Your batch number decides your scenario.

The design technique is **not** given. Identifying the most suitable technique among Divide and Conquer, Greedy, Dynamic Programming, Backtracking and Branch and Bound, and showing why the other four do not fit, is part of the assessment.

Every submission must contain:

1. **Report** (`README.md` in your batch folder), written from [`Instructions/REPORT_TEMPLATE.md`](Instructions/REPORT_TEMPLATE.md).
2. **Code** for your algorithm and for one rejected alternative, in any language.
3. **Timing results**: a CSV and a plot of running time against input size (at least five sizes).
4. **Slides** as PDF.
5. **Recorded presentation**: a link to a video of at most 12 minutes in which **every member presents their own part** with voice (face optional).

Marks are awarded **individually, out of 10**. The commit history, the contribution table in your report, and your part of the video are the evidence for your individual marks.

---

## Step-by-step submission

### Step 1: One member forks the repository

Click **Fork** (top right). This fork is your batch's working copy.

### Step 2: Add your teammates as collaborators

In your fork: **Settings → Collaborators → Add people**. Add every member of the batch.

Each member must commit their own part **from their own GitHub account**. Work committed by one person on behalf of others will be credited to that person only.

### Step 3: Clone the fork

```bash
git clone https://github.com/<fork-owner-username>/DAA_Assignment_2026.git
cd DAA_Assignment_2026
```

### Step 4: Create your batch folder

Inside `Batches/`, create **one** folder named with your batch number, for example `Batch_7`:

```
Batches/Batch_8/
├── README.md              ← your report (from Instructions/REPORT_TEMPLATE.md)
├── slides.pdf
├── code/
│   ├── main_solution.<ext>        ← your chosen algorithm
│   ├── rejected_alternative.<ext> ← one rejected technique, for comparison
│   ├── generate_inputs.<ext>      ← produces the inputs used for timing
│   └── RUN.md                     ← exact commands to compile and run
├── timing.csv                 ← n, time_chosen_ms, time_rejected_ms
└── timing_plot.png
```

- Do **not** name files or folders after the design technique or a textbook problem name (for example, no `greedy.cpp`, no `Q1_Knapsack/`).
- Do **not** touch any other batch's folder.
- Keep binary files out: no `.exe`, `.class`, `a.out`, `node_modules/` or virtual environments.

### Step 5: Record and link the presentation

- Maximum 12 minutes. Every member presents at least one part.
- Upload to Google Drive (PSG account) or YouTube (**Unlisted**). Do **not** commit the video file to GitHub; files over 100 MB are rejected.
- Set sharing to **"Anyone with the link can view"**, then open the link in a private browser window to check it plays.
- Paste the link in the **Presentation** section of your report.

### Step 6: Commit and push

Each member commits their own work:

```bash
git add Batches/Batch_8
git commit -m "Batch_8: <what you added>"
git push origin main
```

Before opening the pull request, bring your fork up to date so it does not conflict with other batches:

```bash
git remote add upstream https://github.com/SangeethaBalachandran/DAA_Assignment_2026.git
git pull upstream main
git push origin main
```

### Step 7: Open one pull request per batch

1. Go to your fork on GitHub.
2. Click **Contribute → Open pull request**.
3. Title: `DAA Assignment Submission - Batch_7`
4. In the description, list the members (roll number and GitHub username) and paste the presentation link.
5. Submit before the deadline. The instructor will review and merge it.

---

## Repository structure

```
DAA_Assignment_2026/
├── README.md
├── Instructions/
│   └── REPORT_TEMPLATE.md
└── Batches/
    ├── Batch_8/
    │   ├── README.md
    │   ├── slides.pdf
    │   ├── code/
    │   └── results/
    ├── Batch_2/
    └── ...
```

---

## Checklist before you open the pull request

- [ ] Report follows the template and covers all sections
- [ ] Technique is identified and the other four are rejected with concrete evidence
- [ ] Trace on the given instance is complete and the answer is correct
- [ ] Code compiles and runs with the commands in `code/RUN.md`
- [ ] `batch8/timing.csv` and `batch8/timing_plot.png` are present (at least five input sizes)
- [ ] `slides.pdf` is present
- [ ] Presentation link opens in a private browser window and is at most 12 minutes
- [ ] Every member has commits from their own account
- [ ] Only your own batch folder is changed
- [ ] Pull request title follows the format
