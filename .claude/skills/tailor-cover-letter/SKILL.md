---
name: tailor-cover-letter
description: Write a casual, compact cover letter for a job Yusef has already tailored a CV for. Triggers when the user asks for a cover letter for one of the applications/ folders. Uses that folder's job_description.md and tailored cv.yaml as source material and writes cover_letter.txt alongside them.
---

# Tailor a Cover Letter

Goal: a short, casual, high-signal cover letter for one specific
`applications/` folder — not a generic one, and not a rehash of the whole
CV.

## Ground truth

Read only from the target application folder:
- `job_description.md` — what to speak to.
- `cv.yaml` (the tailored one in that folder, not the root) — what to draw
  bullets from. Never invent an achievement not already in it.

## Style contract (match this exactly — see example below)

- Opens with `Hi <Company/Team> team,` (use their team name if the JD
  gives one, e.g. "Multiple team"; otherwise `Hi <Company> team,`).
- Second line: one sentence — who Yusef is (role + years, drawn from
  `cv.yaml` headline/summary) + why *this specific* role stood out, tied
  to something concrete in the JD (not "I'm excited about this
  opportunity").
- `A quick snapshot of what I'd bring:` then 3-5 bullets, each pulling a
  real highlight from `cv.yaml` (with numbers where the CV has them) and,
  where natural, tying it back to a specific phrase/requirement from the
  JD. Last bullet is usually a soft/culture-fit line, not another
  technical bullet.
- Closer: `Happy to walk through any of this in more depth. CV attached.`
- Sign-off: `Best,` then `Yusef Nsar` then, on its own line,
  `yusef.nsar.dev@gmail.com | +201551663871 | yusef-nsar.dev`.
- Tone: casual, direct, first person, no corporate filler ("passionate
  about", "team player", "excited to leverage"). Short sentences. It
  should read like Yusef wrote it in five minutes, not like a form letter.
- Compact: whole thing fits comfortably on one screen — roughly the same
  length as the example, not longer.

## Steps

1. Read `applications/<folder>/job_description.md` and
   `applications/<folder>/cv.yaml` fully.
2. Pick the 3-5 strongest, most JD-relevant highlights already present in
   the tailored `cv.yaml` — reuse its wording/numbers, don't reintroduce
   claims that were cut during tailoring.
3. Write `applications/<folder>/cover_letter.txt` following the style
   contract above.
4. Report back the path.

## Example

```
Hi Multiple team,

I'm Yusef, a senior frontend engineer with 5 years building React/Next.js products at scale — the Senior Next.js Developer role stood out because it's the same mix I've been doing: shipping quality frontend work while raising the bar for the team around it.

A quick snapshot of what I'd bring:

- Rebuilt CIB's mobile and web banking platform on React and React Native, scaling it to 1.7M+ active users, and built a self-serve analytics dashboard with React and GraphQL that cut ad hoc reporting requests 70% — all under shared component/coding standards.
- Rebuilt Epicore's legacy frontend on React, TypeScript, and Next.js, boosting Lighthouse scores 74% and CI/CD speed 250%.
- At Propio, I run our architecture review board, author RFCs that set engineering-wide coding standards, and mentor engineers on system design and code review — cut onboarding ramp-up time in half for the last 4 I mentored. That peer-review/mentorship/technical-roadmap mix is exactly what you're describing for this role.
- I like clear, direct communication and giving feedback that's meant to lift people up, not tear them down — sounds like a good culture fit for how you've described the team.

Happy to walk through any of this in more depth. CV attached.

Best,
Yusef Nsar
yusef.nsar.dev@gmail.com | +201551663871 | yusef-nsar.dev
```

This is style guidance only — content must always come from the specific
folder's JD and tailored CV, not be copied verbatim.
