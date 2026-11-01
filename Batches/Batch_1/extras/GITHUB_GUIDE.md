# GitHub guide for the two-member team (Batch 1)

Never share passwords or access tokens. Use your own GitHub login in the browser, or Git Credential Manager / an SSH key on your computer. This guide does not require you to publish any credential.

Instructor repository: `https://github.com/SangeethaBalachandran/DAA_Assignment_2026` · Pull-request title: **`DAA Assignment Submission - Batch_1`** · Deadline: **30 October 2026**.

## 1. Who creates the fork
Exactly **one** member (say Member 1). On the instructor repository click **Fork**. The fork lives at `https://github.com/<fork-owner>/DAA_Assignment_2026`.

## 2. Add the other member
Fork owner: **Settings → Collaborators → Add people** → type Member 2's GitHub username → send invite. Member 2 must **accept the invitation** (email or github.com/notifications).

## 3. Clone the shared fork (both members)
```
git clone https://github.com/<fork-owner>/DAA_Assignment_2026.git
cd DAA_Assignment_2026
git config user.name  "Your Name"
git config user.email "the email verified on YOUR GitHub account"
```
Commits are credited by the e-mail address: use the one linked to your own account, otherwise the commits will not show under your username.

## 4. Create the folder structure (Member 1, once)
Copy the prepared `Batch_1` folder into `Batches/` so that you have exactly:
```
Batches/Batch_1/README.md  slides.pdf  MEMBER_2_TASKS.md
Batches/Batch_1/code/...   Batches/Batch_1/results/...   Batches/Batch_1/extras/...
```
Do not touch other batch folders. Do not add `.exe`, `.class`, `a.out`, virtual environments or `__pycache__` (the repository `.gitignore` may already cover some; check with `git status`).

## 5. Meaningful commits from each person's own account
```
git add Batches/Batch_1/code/main_solution.py Batches/Batch_1/code/generate_inputs.py
git commit -m "Batch_1: main solution and input generator"
```
Suggested commit plan:
* Member 1: `Batch_1: problem model and report sections 1-3`, `Batch_1: main algorithm and tests`, `Batch_1: trace and proof`, `Batch_1: complexity and worst case`.
* Member 2: one commit per task in `MEMBER_2_TASKS.md` (independent brute force, hard-input check, benchmark re-run, reference check, slide edits…).
Small, specific commits are better than one giant commit.

## 6. Push
```
git pull origin main        # get your teammate's commits first
git push origin main
```
Pull before pushing, every time.

## 7. Conflicts
If `git pull` reports a conflict, Git marks the file with `<<<<<<<`, `=======`, `>>>>>>>`. Open the file, keep the correct lines (talk to your teammate), delete the markers, then:
```
git add <file>
git commit -m "Batch_1: resolve merge conflict in <file>"
git push origin main
```
Avoid conflicts: Member 1 edits README §1–3, §5–9; Member 2 edits README §4, §10–13 and the video link; tell each other before editing the same file. Never use `git push --force`.

## 8. Bring the fork up to date with the instructor's repository (before the pull request)
```
git remote add upstream https://github.com/SangeethaBalachandran/DAA_Assignment_2026.git
git pull upstream main
git push origin main
```
(`git remote add` is needed only the first time.)

## 9. Create the single pull request
1. Open your fork on GitHub → **Contribute → Open pull request**.
2. Base repository = the instructor's repository, base = `main`; head = your fork's `main`.
3. Title: `DAA Assignment Submission - Batch_1`
4. Description: both members' **roll number and GitHub username**, and the **presentation video link**.
5. Confirm "Files changed" shows only `Batches/Batch_1/...`. Submit **one** pull request for the batch, before the deadline.

## 10. Verify the video link
Upload to Google Drive (PSG account) or YouTube as **Unlisted**. Do not commit the video file. Set sharing to "Anyone with the link can view". Open the link in a **private/incognito window** (not logged in) and confirm it plays with sound and that the duration is at most 12:00. Paste the same link in `README.md` ("Presentation" section) and in the pull-request description.
