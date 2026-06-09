# Term/Word-Study Analysis Block — Template

Used by the `pdf-to-markdown` skill (rule 3) when a PDF presents a word or term together
with structured analysis. Wrap the entire analysis in a single Markdown blockquote so it
stays visually grouped and distinct from surrounding prose.

```markdown
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

## Notes

- Separate each distinct term's blockquote with a `---` horizontal rule.
- Every line of the analysis stays inside the blockquote (`>` prefix), including blank
  lines between sub-sections.
- Sub-list items (semantic range, impact, application, questions) are indented as normal
  Markdown lists *inside* the blockquote.
- Field labels above are examples — match the labels actually used in the source PDF
  (translate them if the source uses different wording, but keep the same structure:
  bold label, then full untruncated content).
- If the PDF doesn't include one of these fields for a given term, omit that field rather
  than inventing content.
