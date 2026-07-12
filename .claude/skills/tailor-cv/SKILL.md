---
name: tailor-cv
description: Tailor Yusef Nsar's CV to a specific job posting when the user pastes a job title, company, and description. Creates a new applications/ folder with a tailored cv.yaml, job_description.md, keywords.txt, changes.md, and a rendered PDF, and enforces the pagination check and ATS keyword coverage check.
---

# Tailor CV to a Job Posting

Goal: maximize Yusef's interview chances for one specific role.

## Ground truth

`cv.yaml` at the repo root is the ONLY source of truth for experience,
skills, and projects. It holds only the `cv:` key — formatting lives in
`cv-format.yaml`, shared by every rendered CV. A tailored
`applications/*/cv.yaml` must contain ONLY the `cv:` key. Never edit the
root `cv.yaml` or `cv-format.yaml`, and never regenerate the root
`rendercv_output/`. If a linter flags missing design/locale/settings keys
in a tailored file, that's an expected false positive.

## Hard rules

- **Never invent** a company, degree, or certification not in `cv.yaml`.
- **Everything else is fair game as truthful extension**: highlights,
  wording, even a role's `position:` title, so long as that role's real
  highlights plausibly support it. Seniority nudges (mid→senior) and
  sub-discipline reframing (toward whichever backend/frontend/infra/QA
  flavor the highlights actually lean into) are fine. Retitling into a
  domain the highlights don't support (engineering → sales) is not.
- **Stack mismatches**: tailor toward the JD's stack without asking.
  Genericize conflicting tool mentions instead of reattributing them —
  "built a templating engine in Node.js" → "built a templating engine" for
  a .NET posting. Never turn "built X in Node.js" into "built X in .NET."
- **Pagination is a MUST**: ≤2 pages total, and all 4 Professional
  Experience entries fit on page 1.
- No upfront confirmation needed for bullet edits, added skills, or
  wording — pre-authorized as long as flagged in `changes.md`. Only ask
  first if company or job title is unclear/missing.

## Steps to execute

1. Get the job posting (title + company + full description). Ask if
   missing/ambiguous — the folder name depends on it.
2. Read `/home/yusef/dev/cv/cv.yaml` fully.
3. Extract exactly five things from the JD (read deliberately, not "by
   feel" — long postings bury requirements):
   - `required:` / `preferred:` — every named hard skill/tool/framework.
   - seniority signal (junior/mid/senior/staff).
   - domain (fintech/healthtech/e-commerce/etc., or none).
   - the single most-emphasized responsibility/pain point (usually the
     first responsibilities bullet, or the repeated theme).
4. Get timestamp via `date +%y%m%d%H%M%S`, create
   `applications/<timestamp>_<Company> - <Job Title>/`.
5. Write `job_description.md` (verbatim posting) and `keywords.txt` (step
   3 extraction — format below).
6. Write the tailored `cv.yaml`:
   - `cv.headline` = exact job title from posting, verbatim (heaviest ATS
     signal).
   - `Summary`: one line, action verb + result, speaking to the priority
     from step 3. No years-of-experience claim, no restated title. Only
     claims supported elsewhere in the new CV.
   - `Professional Experience`: reorder highlights per role so the most
     relevant/keyword-matching lead; the single most relevant role's lead
     bullet speaks to the step-3 priority. Edit/drop weak bullets but
     never delete an entire employer.
   - `Skills`: reorder categories, most relevant first. Adding skills not
     in the master CV is pre-authorized — flag as `[add]`.
   - `Projects`: keep most relevant, cut irrelevant if space is tight.
   - Mirror the JD's terminology over Yusef's own (e.g. their
     "microservices" vs. his "distributed services") — flag as `[reword]`.
   - Keep total length roughly unchanged.
7. Run the pagination check (below); compact and retry until it passes.
8. Run `scripts/render_application.sh "applications/<timestamp>_<Company> - <Job Title>" "<Job Title>"` from the repo root.
9. Run the ATS keyword coverage check (below) against the rendered PDF. If
   it changes `cv.yaml`, repeat steps 7-9.
10. Write `changes.md`.
11. Report back: what changed, why, and the final PDF path.

## Pagination check

```
scripts/check_layout.sh "applications/<timestamp>_<Company> - <Job Title>/cv.yaml"
```

Renders to a scratch PDF and runs `check_layout.py` (via `pypdf`), printing
`pages=N` and PASS/FAIL for the 2-page limit and for whether "Epicore"
(oldest employer, last Professional Experience entry) lands on page 1 —
proxy for "all 4 entries fit on page 1." Exit 0 only if both pass. Treat as
a black box; its printed output is the whole contract.

On FAIL: trim the least-impactful highlight clause(s) first — shorten
before deleting, and trim the lowest-priority bullet in the largest entry
(usually Propio) before higher-priority ones. Never fix by editing
`cv-format.yaml`. Note pagination-driven trims as `[cut]`/`[reword]` in
`changes.md`, separate from relevance-driven trims.

## ATS keyword coverage check

Run only after pagination passes and the PDF is rendered:

```
python3 scripts/check_ats.py "applications/<timestamp>_<Company> - <Job Title>/Yusef_Nsar-<Job_Title>.pdf" "applications/<timestamp>_<Company> - <Job Title>/keywords.txt"
```

Prints COVERED/MISSING per requirement plus `required: X/Y covered` and
`preferred: X/Y covered`. Always exits 0 — a diligence gate, not a
pass/fail. Treat as a black box.

For every `MISSING required:` item: weave in a truthful mention if it's a
defensible extension of real `cv.yaml` work (flag `[add]`), or leave it out
with a one-line reason in the Match Report. Never leave one unaddressed.

## Output structure

```
applications/YYMMDDHHMMSS_<Company> - <Job Title>/
├── cv.yaml                          # tailored — `cv:` key ONLY
├── job_description.md               # verbatim posting
├── keywords.txt                     # step 3 extraction, feeds check_ats.py
├── changes.md                       # human-readable diff summary
└── Yusef_Nsar-<Job_Title>.pdf       # via scripts/render_application.sh
```

**Naming**: timestamp prefix via `date +%y%m%d%H%M%S` (e.g.
`260706143022_`), don't guess it. Sanitize `<Company>`/`<Job Title>` for
the filesystem (strip `/ : |`), spaces OK. PDF slug uses underscores per
`render_application.sh`'s own output — don't rename by hand; timestamp
prefix is folder-only.

**`keywords.txt`** — one line per fact. `#`-comments for
seniority/domain/priority first (ignored by `check_ats.py`, ride along
free); then the scored `required:`/`preferred:` lines, `|`-separated
synonyms where relevant (any one counts as covered):

```
# seniority: senior
# domain: fintech
# priority: reduce incident response time across distributed services
required: LangChain|LangGraph
required: GitOps
preferred: Terraform|Pulumi
```

**`changes.md`** — flat, tag-prefixed, one line per change, no headings,
scannable in seconds:

```md
# Changes for <Company> - <Job Title>

- [add] <what was added/pulled back in, terse>
- [cut] <what was removed, terse>
- [reword] <old> → <new> (only if non-obvious/stretches accuracy)
- [reorder] <what got promoted/demoted>

## ATS Match
- required: 9/11 covered
- preferred: 3/6 covered
- missing (required): <term> (<one-line reason>)
```

Rules: past tense, no sub-bullets; append ` — <why>` only if a change
stretches accuracy. Skip trivial/expected reorderings — only material ones.
Omit a tag entirely rather than writing "None." Merge related edits into
one line (one `[reorder]` for the whole Skills section, not per category).
`## ATS Match` is always present; one `missing (required):` line per gap;
omit that line if coverage is 100%.

## Referencing past applications

Don't scan the whole `applications/` tree — it grows with every job. Bound
to the most recent:

```
ls applications/ | sort | tail -5
```

Only read files inside the folder(s) that returns.