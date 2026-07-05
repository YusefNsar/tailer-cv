# TailorCV

**Stop fighting Word and Photoshop-ing your PDF just to match a job posting.**
TailorCV is a small toolkit that turns your CV into structured data (YAML) so
you — or an AI assistant working on your behalf — can safely tailor,
edit, and format it, without ever touching layout by hand and without the
usual pain points of doing this the "normal" way:

- **Manually editing Word/PDF for every application** — reflowing text,
  fixing broken alignment, redoing margins, one tedious application at a time.
- **Inconsistent formatting** across versions — different fonts, spacing, or
  layout drifting from one CV to the next because everything is edited by
  eye.
- **Asking a chatbot to "write me a CV" on the fly** — which tends to
  quietly invent experience, titles, or numbers you never had, with nothing
  to check it against.

TailorCV fixes all three by splitting your CV into **content** (your real,
factual experience — the only thing that ever changes) and **formatting**
(theme, fonts, margins — locked, so it never drifts), then giving an AI
assistant a strict, auditable contract for how it's allowed to tailor that
content to a specific job.

## Prerequisites

Install these once before your first render:

- **Python 3.9+** — check with `python3 --version`.
- **[RenderCV](https://github.com/rendercv/rendercv) v2.8** — the engine that
  turns YAML into a PDF (it bundles Typst, so you don't install that
  separately):
  ```bash
  pip install "rendercv==2.8"
  rendercv --version   # should print 2.8.x
  ```
- **[pypdf](https://pypi.org/project/pypdf/)** — only needed for the
  pagination check (`scripts/check_layout.py`):
  ```bash
  pip install pypdf
  ```
- **An AI coding assistant** — e.g. [Claude Code](https://claude.com/claude-code)
  — only needed for the tailoring flow (step 3 below); you can render/edit
  the CV yourself without it.

Quick sanity check that everything is wired up:

```bash
rendercv render cv.yaml -d cv-format.yaml -lc cv-format.yaml -s cv-format.yaml
```

If this produces a PDF in `rendercv_output/` without errors, you're ready.

## How to use

Setup is two edits, done once. Applying is one paste, done forever after:

1. **Edit [cv.yaml](cv.yaml) once** with your real experience, skills, and
   projects. This is the only file that needs to be factually accurate.
2. **Edit [cv-format.yaml](cv-format.yaml) once** (optional) if you want a
   different theme, font, or margins than the defaults. Most people can skip
   this entirely.
3. **For every job you apply to, paste the job description into Claude
   Code** and ask it to tailor your CV. That's it — open
   `applications/<Company> - <Job Title>/` and your tailored `cv.yaml`,
   `job_description.md`, `changes.md`, and ready-to-send PDF are already
   there waiting for you.

No re-formatting, no re-checking margins, no re-running a render command by
hand — just paste and go.

## How it works

1. **Your master CV lives in [cv.yaml](cv.yaml).** This is the one source of
   truth — every real job, skill, and project. You keep this accurate and up
   to date; nothing downstream is allowed to invent beyond it.
2. **Formatting lives separately, in [cv-format.yaml](cv-format.yaml).**
   Theme, colors, fonts, margins — defined once, merged in at render time, so
   every CV you generate looks identical and professional. You basically
   never touch this file.
3. **To apply for a job, paste the job posting to an AI coding assistant**
   (e.g. [Claude Code](https://claude.com/claude-code)) and ask it to tailor
   your CV. Following the contract in
   [prompts/tailor-cv.md](prompts/tailor-cv.md), it:
   - reads your master `cv.yaml` as ground truth,
   - rewrites the headline, summary, and highlights to match the posting's
     keywords and seniority — without fabricating companies or experience,
   - saves the result to `applications/<Company> - <Job Title>/cv.yaml`,
     alongside a copy of the job description and a `changes.md` explaining
     what it changed, so you can double-check anything non-obvious.
4. **Automated checks keep it print-ready.**
   [scripts/check_layout.sh](scripts/check_layout.sh) rejects any tailored CV
   that overflows the page-count/pagination rules you set (by default: 2
   pages max, all experience entries visible on page 1), so you never
   silently ship a broken layout.
5. **One command renders the final PDF.**
   [scripts/render_application.sh](scripts/render_application.sh) merges the
   tailored content with your locked formatting and produces a
   correctly-named, ready-to-send PDF.

The day-to-day loop is simple: **update `cv.yaml` when your real experience
changes, and hand a job posting to your AI assistant whenever you want a
tailored CV** — it drives the prompt and scripts below end to end, so the
only thing you ever review is *what changed*, never *how it looks*.

## Structure

| Path | Purpose |
|---|---|
| [cv.yaml](cv.yaml) | Master CV content — the real, factual source of truth. |
| [cv-format.yaml](cv-format.yaml) | Shared theme/fonts/margins, identical across every generated CV. |
| [fonts/](fonts/) | Font files bundled so rendering is reproducible anywhere. |
| [prompts/tailor-cv.md](prompts/tailor-cv.md) | The contract an AI assistant follows to tailor a CV — what it may and may not change. |
| [scripts/render_application.sh](scripts/render_application.sh) | Renders a tailored `cv.yaml` + `cv-format.yaml` into a named PDF. |
| [scripts/check_layout.sh](scripts/check_layout.sh) / [check_layout.py](scripts/check_layout.py) | Enforces the pagination rules above before a CV is considered done. |
| `applications/<Company> - <Job Title>/` | Generated per-job CVs, job description, and a change summary (created as you tailor). |

## Under the hood

Rendering is powered by [RenderCV](https://github.com/rendercv/rendercv) v2.8
and typeset with Typst — so output is real, print-quality PDF/HTML/PNG, not a
screenshot of a web page. To render the master CV manually:

```bash
rendercv render cv.yaml -d cv-format.yaml -lc cv-format.yaml -s cv-format.yaml
```

This produces PDF/HTML/Typst/PNG/Markdown output in `rendercv_output/`.

## Using this for your own CV

This repo is a working instance, but the pattern generalizes: fork it,
replace the contents of `cv.yaml` with your own experience, leave
`cv-format.yaml` and the scripts as-is (or restyle them once), and you have
the same tailoring workflow for your own job search.
