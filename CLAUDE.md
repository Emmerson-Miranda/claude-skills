# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A collection of Claude Code skills — each skill lives in `skills/<skill-name>/` as a folder that gets packaged and installed into Claude Code via `claude skill install`.

## Installing a skill

```bash
# List available skills
./install.sh

# Install a specific skill
./install.sh quiz-generator
```

`install.sh` zips the skill folder into a `.skill` file and runs `claude skill install` automatically. Requires `zip` and an authenticated `claude` CLI.

## Skill structure

Every skill folder must contain a `SKILL.md` with a YAML frontmatter block at the top:

```yaml
---
name: skill-name
description: >
  One or two sentences Claude uses to decide when to activate this skill.
  Phrase it in terms of user intent ("use this when the user wants to...").
---
```

Optional additions:
- `references/` — supporting docs the skill's instructions can reference (e.g. schema files)
- `examples/` — sample outputs to illustrate expected results

See `skills/quiz-generator/` as the reference implementation.

## quiz-generator skill

Generates multiple-choice YAML quizzes from Markdown documents. Two output files per run:

| File | Contents |
|---|---|
| `<source>-quiz.yaml` | Structured quiz: questions, options, answers, explanations, difficulty, tags |
| `<source>-quiz-summary.md` | Coverage map, statistics, answer key, key concepts |

YAML schema is defined in `skills/quiz-generator/references/yaml-schema.md`. Key constraints:
- `type: single` → exactly 1 answer; `type: multiple` → ≥ 2 answers
- `answers` values must be valid `options[].id` values
- Minimum 3 options per question (4 preferred)
- Tags: lowercase, hyphens only, 1–3 per question

## Adding a new skill

1. Create `skills/<your-skill-name>/SKILL.md` with frontmatter (`name` + `description` required)
2. Optionally add `references/` and `examples/`
3. Test locally: `./install.sh <your-skill-name>`
4. Update the skills table in `README.md`
