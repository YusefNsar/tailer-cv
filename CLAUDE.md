# CV Repo

This repo holds Yusef Nsar's CV, built with [RenderCV](https://github.com/rendercv/rendercv) v2.8.

- `cv.yaml` — the master CV. Source of truth for all real experience, skills,
  and projects. Holds only the `cv:` key (plus an archived-content comment
  block). Never edit this as part of a job-application tailoring flow.
- `cv-format.yaml` — shared `design:`/`locale:`/`settings:` blocks, merged in
  at render time via rendercv's `-d`/`-lc`/`-s` flags. Never edit this as part
  of a tailoring flow either — formatting must stay identical across every
  rendered CV.
- `rendercv_output/` — rendered output of the master `cv.yaml` (pdf/html/typ/png/md).
- `fonts/` — Calibri font files used by the theme. Typst only resolves them
  when the `fonts/` folder sits next to the YAML being rendered, so
  `scripts/render_application.sh` temporarily copies it into the application
  folder for the render and removes it afterward.
- `web-cv/` — a separate web/React rendering of the CV (not part of the
  RenderCV pipeline).
- `applications/` — tailored, job-posting-specific CV versions (see below).
- `scripts/render_application.sh` — renders a tailored `cv.yaml` inside an
  `applications/` folder to a correctly-named PDF.
- `scripts/check_layout.sh` (+ `scripts/check_layout.py`, needs `pypdf`) —
  renders a `cv.yaml` to a scratch PDF and checks pagination: <=2 pages, and
  "Epicore" (the oldest employer, always the last `Professional Experience`
  entry) present on page 1, as a stand-in for "all 4 entries fit on page 1".
  Run this after every tailoring pass and compact content until it passes.
- `scripts/check_ats.py` (needs `pypdf`) — checks ATS keyword coverage of a
  rendered CV PDF against a `keywords.txt` requirement checklist (see the
  `tailor-cv` skill), reporting `required:`/`preferred:` coverage counts.
## Job-application tailoring flow

When the user pastes a job posting (title + company + description) and asks
for a tailored CV, use the `tailor-cv` skill
(`.claude/skills/tailor-cv/SKILL.md`) — it has the full workflow contract.

## Rendering

RenderCV is installed at `~/bin/rendercv` (v2.8). The master `cv.yaml` no
longer carries `design:`/`locale:`/`settings:` — always merge in
`cv-format.yaml` when rendering it directly:

```
rendercv render cv.yaml -d cv-format.yaml -lc cv-format.yaml -s cv-format.yaml
```

Use `scripts/render_application.sh` instead when rendering inside an
`applications/` subfolder — it does this merge automatically, temporarily
copies in `fonts/` so Calibri resolves correctly, and names/places the PDF
correctly.
