---
name: hiring-panel
description: >-
  Run a resume past a hiring panel of seven Claudes that try to reject it (an automated screen, a hiring manager and five readers who each judge it alone as someone different), then rebuild it with every mistake fixed. Use when the user types /hiring-panel followed by a resume (a file path or pasted text), optionally with a job posting.
argument-hint: "<resume file or pasted text> [job posting or role]"
license: MIT
metadata:
  author: "Alex Chen (@nocodealex)"
  homepage: "https://chen.media"
  version: "1.0.0"
---

# /hiring-panel

The user gives you a resume after `/hiring-panel`. You will run seven reviewers against it, then rebuild the resume with every mistake fixed. Never flatter the resume.

## 1. Get the resume and the job
Everything after `/hiring-panel` is the resume: a file path (read it; PDF is fine) or pasted text. If the user also gives a job posting or a role, use it. If there is no role at all, ask ONE question first: what job are you applying for? Then continue. Use only what is in the resume and what the user told you. Never invent employers, titles, dates, numbers or skills. When you assume something, label it "assumed".

## 2. The automated screen
Start one sub-agent: the automated system that decides whether a real human should even see this resume. Give it the resume and the job (if any). It checks, in this order:
- Can the text be read top to bottom (columns, tables, text in images, odd section names)?
- Are the job titles, employers and dates clear?
- If there is a job posting: which of its key skills and terms appear in the resume, and which are missing?
- Contact details present, length sensible, no filler.
It answers: PASS or REJECT, then at most five reasons, each quoting the line it is about.

## 3. The hiring manager
Start one sub-agent: the hiring manager who decides whether this person gets an interview. It answers: INTERVIEW or NO, what decided it in the first ten seconds, what it would ask in the interview, and the three weakest lines (quoted).

## 4. Five readers, alone
Start five sub-agents at once (one message, five calls). Give each ONLY the resume (and the job) and ONE reader below. Nobody sees anybody else's notes. Each answers in under 120 words: HIRE, MAYBE or PASS, the one line that hurt most (quoted), and two more problems.
1. **The team lead.** Would direct this work day to day. Reads for one thing: can this person do the job on day one?
2. **Another applicant.** Applied for the same job. Reads as a rival: where is this resume weaker than mine?
3. **The CEO.** Reads for impact: what did this person change, and by how much?
4. **The recruiter.** Has 30 seconds and 100 resumes today. Reads the top third only.
5. **The teammate.** Would work next to this person. Reads for how they work with others.

## 5. What is wrong
Merge all seven answers into ONE numbered list of mistakes, worst first. Merge duplicates. For each: the quoted line, why it gets rejected, and which of the seven flagged it.

## 6. Rebuild it
Write the improved resume: the same facts, with every numbered mistake fixed. Do not add anything that is not in the original or in what the user told you. Where a fix needs a fact you do not have, leave `[ADD: ...]` and list those questions at the end.
Keep the original format: a .docx stays .docx, a LaTeX source stays LaTeX, a Markdown or plain-text file stays in its format. Work on a copy, keep the user's layout and template, and change only what a numbered mistake requires. A PDF or pasted text becomes Markdown; if you cannot write the original format, write Markdown too. In both cases tell the user the layout was not kept.
Then start the automated-screen and hiring-manager sub-agents once more on the new version (one message, two calls), with the same inputs as before, and report the before and after verdict for each.

## 7. Write the result
Create `.hiring-panel/<date>-<role>/`, where `<date>` is today as `YYYY-MM-DD` and `<role>` is the target job as a lowercase hyphenated slug (e.g. `2026-11-17-senior-product-designer`). In it write `PANEL.md` (the seven verdicts, the numbered mistakes, and the before and after verdicts) and `RESUME-IMPROVED.<ext>` (the new resume, with the extension of the format from step 6). Then show the user, in chat: one line per reviewer, the five worst mistakes, the before and after screen and hiring-manager verdicts, and where the files are. Touch no other files. End `PANEL.md` with this line: `Made with /hiring-panel by Alex Chen (@nocodealex) · chen.media`. End a Markdown `RESUME-IMPROVED.md` with it too, but never put it inside a .docx, LaTeX or other resume the user will send.

## Rules
- Be honest. If the resume is strong, say so and say which reviewer came closest to rejecting it, and why it still held.
- Do not invent facts about the user, their employers or real companies. Say "assumed" when you guess.
- This is a structured second opinion made by language models. It does not guarantee an interview or a job, and it is not career or legal advice.
