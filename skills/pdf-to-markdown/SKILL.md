---
name: pdf-to-markdown
description: >
  Converts an attached PDF into a faithful, complete Markdown (.md) file — preserving every
  paragraph, list, table, footnote, heading, and special character without summarizing,
  compressing, or omitting content. Use this skill whenever the user wants to convert a PDF
  to Markdown, extract the full text of a PDF, or turn a PDF (including documents with
  parallel columns, tables, structured term/word-study blocks, or non-Latin scripts like
  Hebrew/Greek) into a structured Markdown file. Triggers on phrases like "convert this PDF
  to Markdown", "extract this PDF", "pasa este PDF a Markdown", or "conviértelo a .md".
---

# PDF to Markdown Skill

Converts an attached PDF document into a Markdown file that preserves **all** of its
content and structure. Fidelity is the priority — this skill is for complete, lossless
conversion, not summarization.

---

## Workflow

### 1. Content preservation — the most important rule

- Copy **all** text from the PDF, without exception.
- Fix grammatical errors only if it's safe to do so; otherwise leave the text as-is.
- **Do not summarize, compress, or omit** any paragraph, sentence, list, fact, note,
  footnote, header, or section — no matter how minor it seems. Losing any information is
  a serious error.
- If a section looks repetitive or low-value, include it anyway. Deciding what to keep is
  not your call — that belongs to the document's author.
- When the PDF has parallel columns (two or more blocks of text side by side), read **all**
  columns and dump their content sequentially into the Markdown, without skipping any.
  Order is left-to-right, then top-to-bottom.

### 2. Structure and hierarchy

- Mirror the heading hierarchy of the original: main title → `#`, sections → `##`,
  subsections → `###`, etc.
- Preserve the order of content exactly as it appears in the PDF.
- Use horizontal rules (`---`) where the PDF shows a clear visual separation between
  sections.

### 3. Structured term/keyword analysis blocks

When the PDF presents a word or term together with structured analysis (root, semantic
range, usage, contrast, context, impact, application, questions...), wrap the whole
analysis in a blockquote so it stays visually grouped:

```
> ### Term — "Translation"
>
> **Root and word family:**
> [full text, not summarized]
>
> **Semantic range:**
> - point 1
> - point 2
> - does NOT mean: [full text]
>
> **Usage and pattern:**
> [full text]
>
> **Translation contrast:**
> [full text]
>
> **Cultural context and mental image:**
> [full text]
>
> **Interpretive impact:**
> - point 1
> - point 2
>
> **Transformational application:**
> - Mind: [text]
> - Heart: [text]
> - Conduct: [text]
>
> **Reflection / self-examination questions:**
> 1. [full question]
> 2. [full question]
```

Separate each distinct term's blockquote with `---`. See
`references/term-analysis-block.md` for the full template.

Adapt field names/labels to whatever the PDF actually uses — the structure (blockquote,
bold sub-labels, nested lists) is what matters, not these exact label names.

### 4. End-of-section info blocks

When the PDF includes blocks at the end of a section or passage such as "Additional brief
context", "Possible interpretations", "What does your heart interpret?", or "Cross-
referenced verses" (or equivalents), include all of them with their headings and full
text.

### 5. Tables → lists

**Do not use Markdown tables.** Whenever the PDF presents information as a table, convert
it into a list where each item corresponds to a row:

```
- [Column A]: [Column B] · [Column C]
- [Column A]: [Column B] · [Column C]
```

If the table has column headers, include them as a bold title before the list items:

```
**[Header A] / [Header B] / [Header C]**
- [value A]: [value B] · [value C]
- [value A]: [value B] · [value C]
```

### 6. Hebrew, Greek, and other special characters

- Preserve every character in Hebrew, Greek, or any other non-Latin script exactly as it
  appears in the PDF.
- If the text extractor produces corrupted or unreadable Hebrew/Greek, use the visible PDF
  text as a reference and transcribe it manually with fidelity.
- Do not replace special characters with Latin approximations.

### 7. List formatting

- Bullet lists → use `-`.
- Numbered lists → use `1.`, `2.`, etc.
- Sub-lists → indent with 2 spaces.
- Never use `•`, `·`, or other bullet glyphs directly as Markdown list markers — use only
  `-` or numbering.

### 8. Italics, bold, and emphasis

- Use `**bold**` for internal labels within blocks (e.g. **Root and word family:**).
- Use `*italics*` for transliterated terms or work titles (e.g. *hevel*, *teshuvá*).
- Don't add emphasis where the original has none.

### 9. Metadata and footers

- Include any authorship, edition, copyright, or distribution notes that appear in the
  PDF, as-is, at the start or end of the Markdown according to their position in the
  original.

### 10. Output file naming

- Default filename: `<source-basename>.md`, derived from the PDF's filename or title.
- If the document is a numbered chapter/unit and the user gives a base name, use
  `<base-name>-capitulo<N>.md` (or `-chapterN` for English documents) — match the
  pattern the user specifies.
- Save the file to disk in the working directory (or the directory the user specifies)
  rather than printing the full content inline in chat — the volume of text is typically
  too large for a readable chat message.

### 11. Verification before delivering

Before finishing, check:

- [ ] Is all the PDF text present, with no omissions?
- [ ] Are all term-analysis blocks complete?
- [ ] Are there no Markdown tables — only lists?
- [ ] Is Hebrew/Greek text intact?
- [ ] Are end-of-section blocks (context, interpretations, cross-references) included?
- [ ] Does the output file have the correct name and location?

---

## Options the user can specify

| Option | Default | Example |
|---|---|---|
| Output filename | `<source-basename>.md` | "guárdalo como Genesis-capitulo1.md" |
| Output directory | working directory | "save it in `notas/`" |
| Chapter/unit number | none | "this is capítulo 3" |
| Language of output | same as the PDF | (rarely changed — fidelity means keep source language) |

---

## Reference

See `references/term-analysis-block.md` for the full annotated template for structured
term/word-study blocks (rule 3).
