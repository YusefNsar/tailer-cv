# Tailor CV to a Job Posting

You are helping Yusef Nsar produce a job-posting-tailored version of his CV with
the single goal of maximizing his chance of landing an interview for that
specific role.

## Input

The user will paste a job posting (title, company, and description/requirements).
Sometimes just a URL or a pasted block of text. If the company or title is
ambiguous or missing, ask before proceeding — the folder name depends on it.

## Ground truth

`cv.yaml` at the repo root is the ONLY source of truth for Yusef's experience,
skills, and projects. Treat it as complete and accurate. It now holds only the
`cv:` content (plus an archived-content comment block) — formatting
(`design:`/`locale:`/`settings:`) lives in `cv-format.yaml` at the repo root
and is shared by every rendered CV.

Hard rules — do not break these, even if it would make the CV a better match:

- Never invent a company that isn't in `cv.yaml`, you can change highlights or the exact job title to match the job but in coherent way.
- You MAY NOT touch `cv-format.yaml` as part of a tailoring flow — formatting
  must stay identical across applications. A tailored `applications/*/cv.yaml`
  file must contain ONLY the `cv:` key (no `design:`/`locale:`/`settings:`
  blocks) — `scripts/render_application.sh` merges it with `cv-format.yaml`
  at render time.
- Since the user reviews every generated CV afterward for factual accuracy,
  optimize, add and edit freely for the perfect match quality first that grant an interview, then flag anything non-obvious you rephrased/added in `changes.md` (see below) so it's easy to double check and correct latter if needed by me.
- **Pagination is a MUST, not a suggestion**: the rendered CV must be at most
  2 pages, AND all 4 `Professional Experience` entries must fit on page 1.
  This is checked with `scripts/check_layout.sh` (see "Pagination check" below)
  — never skip it, and never hand back a CV that fails it.

## Tailoring approach

1. Read `cv.yaml` fully.
2. Extract the real requirements/keywords from the job posting: role level,
   must-have tech stack, domain (fintech/healthtech/etc.), and any
   soft-skill/leadership signals.
3. Set `cv.headline` to the exact job title from the posting (verbatim,
   not a paraphrase) — this is what ATS keyword-matches against most heavily.
4. Rewrite `Summary` to ONE minimal, maximum-impact line that leads with a
   strong action verb and result (same style as the master CV's summary —
   e.g. "Re-architected ... cutting infrastructure costs 40%..."). Do NOT
   state years of experience or restate a job title/position name in this
   line — the headline already carries the title, and a numeric years claim
   reads as filler, not impact. Use only claims already supported elsewhere
   in the new CV.
5. Reorder and edit `Professional Experience` highlights per role so the
   most relevant, keyword-matching bullets lead. You can drop or edit a bullet from a
   job entry if it's irrelevant to this posting, but keep every job entry
   (never delete an entire employer).
6. Reorder `Skills` categories/labels so the most relevant to this posting
   are listed first. You are pre-authorized to add skills that aren't in the
   master CV when it improves match quality — do NOT ask for confirmation
   before adding one; just add it and flag it as an `[add]` line in
   `changes.md` for the user to check afterward.
7. Reorder or edit `Projects` — keep the ones most relevant to the posting,
   cut ones with no relevance if space/focus is a concern.
8. Keep total length roughly the same as the original
9. Mirror the job posting's terminology, terms and language (e.g. if
   they say "microservices" and Yusef's bullet says "distributed services",
   align wording) — this measurably helps with ATS keyword
   matching, even at the cost of accuracy, just flag it in changes.md.

## Pagination check

Every added word costs vertical space, and the master CV's layout already has
very little slack — even small terminology-alignment edits (step 9) can push
an entry past page 1 or the CV past 2 pages. This is checked after every
render, not assumed:

1. Run `scripts/check_layout.sh "applications/<Company> - <Job Title>/cv.yaml"`.
   It renders the tailored CV to a scratch PDF and runs
   `scripts/check_layout.py` (via `pypdf`) on it, which prints `pages=N` and
   either `PASS`/`FAIL` for both the 2-page limit and whether "Epicore" (the
   oldest employer, always the last `Professional Experience` entry) is
   found on page 1 — a stand-in for "all 4 entries fit on page 1". Exit code
   is 0 only if both checks pass.
2. On any `FAIL` (or nonzero exit code), compact and retry: trim the
   least-impactful highlight clause(s) first (prefer shortening a bullet
   over deleting one, and prefer trimming the lowest-priority bullet in the
   largest entry, usually Propio, over touching higher-priority ones).
   Never fix this by editing `cv-format.yaml` (spacing/margins/font size) —
   the fix must come from the `cv:` content only. Re-run step 1 and repeat
   until it passes.
3. Only once it passes, move on to the final render (step 8 below) and note
   any trims made purely to fit pagination as `[cut]`/`[reword]` lines in
   `changes.md` (distinct from trims made for relevance).

## Output

Create a new folder:

```
applications/<Company> - <Job Title>/
├── cv.yaml                          # tailored copy — `cv:` key ONLY, no design/locale/settings
├── job_description.md               # verbatim copy of what the user gave you
├── changes.md                       # human-readable diff summary (see below)
└── Yusef_Nsar-<Job_Title>.pdf       # rendered via scripts/render_application.sh
```

Folder/file naming:
- Sanitize `<Company>` and `<Job Title>` for the filesystem (strip characters
  like `/`, `:`, `|`) but keep them human-readable — spaces are fine.
- The PDF job-title slug uses underscores in place of spaces (e.g.
  `Yusef_Nsar-Senior_Backend_Engineer.pdf`), matching what
  `scripts/render_application.sh` produces automatically — don't rename it
  by hand.

`changes.md` structure — a flat, tag-prefixed list, one line per change, no
headings, no filler. Optimize for a reviewer scanning it in seconds:

```md
# Changes for <Company> - <Job Title>

- [add] <what was added/pulled back in, terse>
- [cut] <what was removed, terse>
- [reword] <old> → <new> (only if non-obvious/stretches accuracy)
- [reorder] <what got promoted/demoted>
```

Rules:
- One line per change, past tense, no sub-bullets, no explanations unless the
  change stretches accuracy (then add ` — <why>` at the end of that line).
- Skip trivial/expected reorderings (e.g. routine skill-priority shuffles) —
  only list reorders material enough to catch the reviewer's eye.
- Omit a tag entirely if there's nothing to report under it — don't write
  "None".
- Merge related edits into one line instead of listing each sub-edit
  separately (e.g. one `[reorder]` line for the whole Skills section, not one
  per category).

## Steps to execute

1. Ask for the job posting if not already given (title + company + full
   description are all needed).
2. Read `/home/yusef/dev/cv/cv.yaml`.
3. Create the `applications/<Company> - <Job Title>/` folder.
4. Write `job_description.md` with the raw posting the user gave you.
5. Write the tailored `cv.yaml` into that folder.
6. Run the pagination check (see "Pagination check" above) and compact/retry
   until it passes.
7. Write `changes.md` (including any pagination-driven trims from step 6).
8. Run `scripts/render_application.sh "applications/<Company> - <Job Title>" "<Job Title>"`
   from the repo root to produce the final PDF.
9. Report back a short summary: what changed and why, and the final PDF path.

## Out of scope

- Don't touch the root `cv.yaml` — it's the master copy, never edit it as
  part of this flow.
- Don't regenerate the root `rendercv_output/` — that belongs to the master
  CV, not a tailored application.
- Don't ask the user to confirm every bullet choice, wording change, or
  added skill before rendering — all of that is pre-authorized as long as
  it's flagged in `changes.md`; they review the output afterward. Do ask
  upfront if the job posting itself is missing/ambiguous (title or company
  unclear) — that's the only case that warrants a question.
