# CV Repo

This repo holds Yusef Nsar's CV, built with [RenderCV](https://github.com/rendercv/rendercv) v2.8.

**Primary goal**: produce a *perfectly tailored* CV for each job Yusef
applies to, even for postings that don't match his current stack. When a
job posting is pasted, that's a request to tailor — use the `tailor-cv`
skill (`.claude/skills/tailor-cv/SKILL.md`, has the full workflow contract)
without asking about fit; only ask if company/title is missing or ambiguous.
When asked for a cover letter for one of these applications, use the
`tailor-cover-letter` skill (`.claude/skills/tailor-cover-letter/SKILL.md`)
instead.

- `cv.yaml` — master CV, source of truth for all real experience/skills/
  projects. Holds only the `cv:` key. Never edit as part of tailoring.
- `cv-format.yaml` — shared `design:`/`locale:`/`settings:`, merged in at
  render time via `-d`/`-lc`/`-s`. Never edit as part of tailoring — must
  stay identical across every rendered CV.
- `rendercv_output/` — rendered output of the master `cv.yaml`.
- `fonts/` — Calibri; `scripts/render_application.sh` copies it next to
  whichever YAML is being rendered (Typst only resolves fonts that way).
- `web-cv/` — separate web/React CV rendering, not part of the RenderCV pipeline.
- `applications/` — tailored, job-posting-specific CV versions.
- `scripts/render_application.sh`, `scripts/check_layout.sh`(+`.py`),
  `scripts/check_ats.py` — pagination/ATS checks and render helper used by
  the `tailor-cv` skill; see that skill for usage, they're not needed outside it.

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
