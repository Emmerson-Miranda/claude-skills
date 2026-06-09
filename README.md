# claude-skills

A collection of reusable skills for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) — Anthropic's CLI coding agent.

Each skill is a folder containing a `SKILL.md` instruction file that Claude reads automatically when relevant, making complex or repetitive workflows repeatable without re-explaining them every time.

---

## Available Skills

| Skill | Description |
|---|---|
| [quiz-generator](skills/quiz-generator/) | Generate multiple-choice study questions from any Markdown document, outputting a structured YAML quiz, a human-readable summary, and an interactive HTML test |
| [pdf-to-markdown](skills/pdf-to-markdown/) | Convert an attached PDF into a faithful, complete Markdown file — preserving all content, structure, tables (as lists), and non-Latin scripts |
| [claude-skills-version](skills/claude-skills-version/) | Reports the current version of this claude-skills collection |

---

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed and authenticated
- `zip` available on your system (pre-installed on macOS and most Linux distros)

---

## Installation

### Option A — Install script (recommended)

```bash
# Clone the repo
git clone https://github.com/Emmerson-Miranda/claude-skills.git
cd claude-skills

# List available skills
./install.sh

# Install a specific skill
./install.sh quiz-generator
```

### Option B — Manual install

```bash
git clone https://github.com/Emmerson-Miranda/claude-skills.git
cd claude-skills/skills

# Package the skill as a zip
zip -r quiz-generator.skill quiz-generator/

# Install via Claude Code
claude skill install quiz-generator.skill
```

### Option C — Download the pre-packaged `.skill` file

1. Go to the [Releases](https://github.com/Emmerson-Miranda/claude-skills/releases) page
2. Download `quiz-generator.skill`
3. Run:

```bash
claude skill install ~/Downloads/quiz-generator.skill
```

---

## Usage after installation

Once installed, Claude Code detects the skill automatically based on your prompt — no flags needed.

```bash
# Generate study questions from a Markdown file
claude --file my-notes.md "Generate study questions"

# Spanish prompt works too
claude --file apuntes.md "Genera preguntas de estudio"

# Focus on a specific topic
claude --file chapter3.md "Generate 15 hard questions about memory management"

# Skip the summary file
claude --file notes.md "Generate study questions, skip the summary"
```

**Every run produces three output files:**

```
my-notes-quiz.yaml          ← structured quiz data (YAML)
my-notes-quiz-summary.md    ← human-readable overview + answer key
my-notes-quiz.html          ← interactive browser test with scoring
```

---

## Skill Reference

### quiz-generator

Reads a Markdown document, maps every distinct concept, and generates multiple-choice questions that cover all the knowledge in the file.

**Outputs:**

| File | Description |
|---|---|
| `<source>-quiz.yaml` | Full quiz with questions, options, correct answers, explanations, difficulty, and tags |
| `<source>-quiz-summary.md` | Coverage map, statistics, questions-at-a-glance answer key, and key concepts list |
| `<source>-quiz.html` | Self-contained interactive test — radio buttons (single) / checkboxes (multiple), per-question validation, final score |

**Key behaviours:**
- Targets ~20 questions but exceeds that if the document has more concepts — full coverage wins over a round number
- Mixes `single` and `multiple` answer questions (~40% / ~60%)
- Balances difficulty: ~30% easy, ~45% medium, ~25% hard
- Output language matches the source document automatically

See [`skills/quiz-generator/SKILL.md`](skills/quiz-generator/SKILL.md) for the full specification and [`skills/quiz-generator/references/yaml-schema.md`](skills/quiz-generator/references/yaml-schema.md) for the complete YAML schema.

**Example outputs:** [`skills/quiz-generator/examples/`](skills/quiz-generator/examples/)

---

### pdf-to-markdown

Converts an attached PDF into a complete Markdown file without summarizing or omitting any
content — including parallel columns, footnotes, and metadata.

**Key behaviours:**
- Preserves every paragraph, list, heading, and footnote — losing information is treated as an error
- Converts tables into bullet lists (no Markdown tables)
- Wraps structured term/word-study analysis in blockquotes
- Preserves Hebrew, Greek, and other non-Latin scripts exactly
- Saves output as `<source-basename>.md` (or a chapter-numbered name if specified)

See [`skills/pdf-to-markdown/SKILL.md`](skills/pdf-to-markdown/SKILL.md) for the full specification and [`skills/pdf-to-markdown/references/term-analysis-block.md`](skills/pdf-to-markdown/references/term-analysis-block.md) for the term-analysis block template.

---

## Contributing

Contributions are welcome! To add a new skill:

1. Create a folder under `skills/your-skill-name/`
2. Add a `SKILL.md` with a YAML frontmatter block (`name` and `description` are required)
3. Optionally add a `references/` folder for supporting docs and an `examples/` folder
4. Open a PR with a short description of what the skill does

See the [quiz-generator skill](skills/quiz-generator/) as a reference implementation.

---

## License

MIT
