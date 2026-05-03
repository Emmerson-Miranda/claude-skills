---
name: quiz-generator
description: >
  Generates multiple-choice study questions (single or multi-select) from Markdown documents,
  and outputs them in a structured YAML format. Use this skill whenever the user wants to
  create study questions, flashcards, quizzes, or practice tests from any document or notes —
  even if they say things like "generate questions from this", "make a quiz", "help me study
  this", "create practice questions", or "turn this into a test". Always use this skill when
  a Markdown (or any text) file is involved and the goal is learning or self-assessment.
---

# Quiz Generator Skill

Generates structured multiple-choice study questions from a Markdown document and outputs
them as a YAML file ready to use in study tools, scripts, or Claude Code pipelines.

---

## Workflow

### 1. Read the source document

- Accept input as: uploaded `.md` file, pasted Markdown text, or a file path.
- Extract the main topics, concepts, definitions, processes, and facts.
- Identify natural groupings or sections to distribute questions evenly.

### 2. Analyse and plan questions

**Coverage is the priority.** Before writing any questions, do a full inventory of the document:

1. List every distinct concept, definition, fact, process, list, and relationship in the document.
2. Group them by section or topic.
3. Assign at least one question per distinct concept — do not merge or skip concepts to stay under a number limit.

**Question count rules:**
- Target **up to 20 questions** for a typical document.
- If the document contains more than 20 distinct concepts, **exceed 20** — there is no hard cap. Full knowledge coverage always wins over a round number.
- Only generate fewer than 20 if the document genuinely does not contain enough material (e.g. a very short or narrow document).
- If the user specifies a number explicitly, treat it as a minimum floor, not a ceiling.

**Question type mapping:**
- Key **facts / definitions** → `single` answer
- Lists, characteristics, steps, or multi-part concepts → `multiple` answer
- Recommended split: ~40% single, ~60% multiple

**Difficulty distribution:**
- Aim for a balanced mix: ~30% easy, ~45% medium, ~25% hard
- Easy → recall / definitions
- Medium → comprehension / application
- Hard → analysis / edge cases / relationships between concepts

### 3. Generate the YAML output

Use the canonical schema below. Output **only valid YAML** — no prose before or after,
no markdown code fences, unless the user asks to see it in the chat.

```yaml
quiz:
  title: "Topic Name"           # derived from the document title or first heading
  source: "filename.md"         # original file name, or "pasted content" if no file
  generated_at: "YYYY-MM-DD"   # today's date

  questions:
    - id: 1
      question: "Question text here?"
      type: single              # single | multiple
      options:
        - id: a
          text: "Option A"
        - id: b
          text: "Option B"
        - id: c
          text: "Option C"
        - id: d
          text: "Option D"
      answers: [b]              # always a list, even for single-answer questions
      explanation: "Brief explanation of why these answers are correct."
      difficulty: medium        # easy | medium | hard
      tags: [tag1, tag2]        # 1-3 relevant topic tags from the document
```

### 4. Quality checks before outputting

**Coverage:**
- [ ] Every major section of the document has at least one question
- [ ] No significant concept, definition, or fact from the document is left uncovered
- [ ] If concepts remain uncovered after 20 questions, add more questions until all are covered

**Question quality:**
- [ ] Every question has **at least 3 options** (4 preferred)
- [ ] `answers` list matches valid `option.id` values
- [ ] `type: multiple` questions have **2 or more correct answers**
- [ ] `type: single` questions have **exactly 1 correct answer**
- [ ] Explanations are concise (1-3 sentences) and educational
- [ ] No duplicate questions
- [ ] Tags are lowercase, no spaces (use hyphens if needed)

### 5. Save the YAML output file

- Default filename: `<source-basename>-quiz.yaml`  
  Example: `redes.md` → `redes-quiz.yaml`
- If running in Claude Code, save to the same directory as the source file unless told otherwise.
- If in Claude.ai chat, present the YAML in a code block for the user to copy.

### 6. Generate the HTML test file

After saving the YAML, always generate a companion `<source-basename>-quiz.html` file.

The HTML file is a **fully self-contained, interactive test** — no external scripts or stylesheets. All CSS and JavaScript must be inlined.

**Behaviour requirements:**

- Render every question from the YAML in order, numbered.
- `type: single` → render options as **radio buttons** (only one selectable).
- `type: multiple` → render options as **checkboxes** (multiple selectable).
- Each question has an individual **"Check answer"** button.
  - On click: compare the user's selection against `answers`.
  - Mark correct options green, incorrect/missed options red.
  - Show the `explanation` text below the options.
  - Disable the question's inputs and button after it is checked (no re-attempts).
- At the bottom of the page, a **"See my score"** button (always visible).
  - On click: calculate score = number of fully-correct questions / total questions × 100.
  - Display a results banner: e.g. "Score: 14 / 20 — 70%".
  - Unchecked questions count as 0 (wrong).
- Style guidelines (inline CSS, no frameworks):
  - Clean, readable layout; max-width ~800 px centred.
  - Difficulty badge per question (easy = green, medium = orange, hard = red).
  - Correct answer highlight = light green background; wrong = light red background.
  - Missed correct answer (user didn't select it) = yellow highlight.

**HTML file structure:**

```html
<!DOCTYPE html>
<html lang="{quiz.language or 'en'}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{quiz.title}</title>
  <style>/* all styles inline here */</style>
</head>
<body>
  <h1>{quiz.title}</h1>
  <p class="meta">Source: {quiz.source} · Generated: {quiz.generated_at} · {n} questions</p>

  <form id="quiz-form">
    <!-- one <section class="question"> per question -->
  </form>

  <div id="score-area">
    <button type="button" id="score-btn">See my score</button>
    <div id="score-result" hidden></div>
  </div>

  <script>/* all JS inline here */</script>
</body>
</html>
```

**Saving the HTML file:**
- Filename: `<source-basename>-quiz.html`
  Example: `redes.md` → `redes-quiz.html`
- Save alongside the YAML and summary files.
- In Claude.ai chat, inform the user the file has been saved and they can open it in a browser.

---

### 7. Generate the summary Markdown file

After saving the YAML, always generate a companion `<source-basename>-quiz-summary.md` file.

The summary serves as a **human-readable overview** of the quiz — useful for quick review,
sharing with others, or printing. It must be generated from the final YAML data.

**Required sections:**

```markdown
# Quiz Summary: {title}

**Source:** {source}
**Generated:** {generated_at}
**Total questions:** {n}

---

## Coverage Map

| Topic / Tag | Questions | Types |
|---|---|---|
| tcp-ip | 3 | 1 single, 2 multiple |
| modelo-osi | 4 | 2 single, 2 multiple |

---

## Statistics

| Metric | Value |
|---|---|
| Total questions | {n} |
| Single-answer | {count} ({pct}%) |
| Multiple-answer | {count} ({pct}%) |
| Easy | {count} ({pct}%) |
| Medium | {count} ({pct}%) |
| Hard | {count} ({pct}%) |

---

## Questions at a Glance

Numbered list of all questions with correct answers — no explanations,
so the student can use this as a quick self-test answer key.

1. ¿Question text? → **b, c**
2. ¿Question text? → **a**

---

## Key Concepts Covered

Bullet list of the main concepts/topics tested, derived from tags and question content.

- TCP handshake de 3 vías
- Diferencias entre TCP y UDP
- Capas del modelo OSI
```

**Saving the summary:**
- Filename: `<source-basename>-quiz-summary.md`
  Example: `redes.md` → `redes-quiz-summary.md`
- Save alongside the YAML file.
- In Claude.ai chat, render it as Markdown after the YAML output.

---

## Options the user can specify

| Option | Default | Example |
|---|---|---|
| Number of questions | enough to cover all content (target ~20, no hard cap) | "genera exactamente 15 preguntas" |
| Difficulty filter | mixed (30% easy / 45% medium / 25% hard) | "solo preguntas difíciles" |
| Question type | mixed (~40% single / ~60% multiple) | "solo multi-selección" |
| Language of output | same as document | "preguntas en inglés" |
| Output filename | `<source>-quiz.yaml` | "guárdalo como examen1.yaml" |
| Summary file | always generated alongside YAML | "no generes el resumen" |
| HTML test file | always generated alongside YAML | "no generes el HTML" |
| Tags/topics to focus on | all | "enfócate en el capítulo 3" |

---

## Example invocations (Claude Code)

```bash
# Basic usage — generates quiz YAML + summary MD + interactive HTML test
claude --file notas.md "Genera preguntas de estudio usando el quiz-generator skill"

# Custom quantity
claude --file notas.md "Genera 20 preguntas de estudio en YAML"

# Focus on a topic
claude --file notas.md "Genera 10 preguntas difíciles sobre el tema de redes"

# Skip the summary
claude --file notas.md "Genera preguntas de estudio, no generes el resumen"
```

---

## Reference

See `references/yaml-schema.md` for the full annotated schema with all optional fields
and extended examples.
