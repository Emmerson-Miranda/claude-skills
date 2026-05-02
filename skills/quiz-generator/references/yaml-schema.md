# Quiz YAML Schema — Full Reference

## Top-level structure

```yaml
quiz:
  title: string          # Required. Human-readable title of the quiz.
  source: string         # Required. Source filename or "pasted content".
  generated_at: string   # Required. ISO date YYYY-MM-DD.
  language: string       # Optional. e.g. "es", "en". Defaults to document language.
  description: string    # Optional. Brief description of the quiz topic.

  questions:
    - ...                # One or more question objects (see below)
```

---

## Question object

```yaml
- id: integer            # Required. Sequential number starting at 1.

  question: string       # Required. The question text. End with "?".
                         # For multi-select, hint to the student:
                         # "¿Cuáles de las siguientes...?" or
                         # "Selecciona todas las que apliquen."

  type: single | multiple
                         # Required.
                         # single   → exactly 1 correct answer
                         # multiple → 2 or more correct answers

  options:               # Required. List of answer options.
    - id: string         # Required. Single lowercase letter: a, b, c, d ...
      text: string       # Required. The option text (no trailing period needed).

  answers: [string, ...] # Required. List of correct option IDs.
                         # Always a list, even for single-answer questions.
                         # Example single:   answers: [b]
                         # Example multiple: answers: [a, c, d]

  explanation: string    # Required. 1-3 sentences explaining why the answers are correct.
                         # Mention the incorrect options briefly if helpful.

  difficulty: easy | medium | hard
                         # Required.
                         # easy   → recall / definition
                         # medium → comprehension / application
                         # hard   → analysis / edge cases / multi-concept

  tags: [string, ...]    # Required. 1-3 topic tags. Lowercase, hyphens allowed.
                         # Example: [redes, tcp-ip, modelo-osi]

  hint: string           # Optional. A nudge without giving away the answer.
  points: integer        # Optional. Weight for scoring. Default 1.
  time_limit_seconds: integer  # Optional. Per-question timer for timed quizzes.
```

---

## Full worked example

```yaml
quiz:
  title: "Fundamentos de Redes"
  source: "redes.md"
  generated_at: "2026-05-01"
  language: "es"

  questions:
    - id: 1
      question: "¿Cuál es la función principal de la capa de transporte en el modelo OSI?"
      type: single
      options:
        - id: a
          text: "Enrutar paquetes entre redes distintas"
        - id: b
          text: "Garantizar la entrega confiable de datos extremo a extremo"
        - id: c
          text: "Convertir datos a señales eléctricas"
        - id: d
          text: "Gestionar sesiones entre aplicaciones"
      answers: [b]
      explanation: "La capa de transporte (capa 4) es responsable de la entrega confiable de segmentos de extremo a extremo usando protocolos como TCP. El enrutamiento corresponde a la capa 3, las señales a la capa 1, y las sesiones a la capa 5."
      difficulty: medium
      tags: [modelo-osi, capa-transporte]

    - id: 2
      question: "¿Cuáles de las siguientes características corresponden al protocolo TCP? Selecciona todas las que apliquen."
      type: multiple
      options:
        - id: a
          text: "Orientado a conexión"
        - id: b
          text: "No garantiza el orden de los paquetes"
        - id: c
          text: "Control de flujo"
        - id: d
          text: "Menor latencia que UDP"
        - id: e
          text: "Acuse de recibo (ACK)"
      answers: [a, c, e]
      explanation: "TCP es orientado a conexión (handshake de 3 vías), implementa control de flujo con ventana deslizante, y usa ACKs para confirmar entrega. UDP (no TCP) es más rápido y no garantiza orden ni entrega."
      difficulty: hard
      tags: [tcp, protocolos, capa-transporte]
      hint: "Piensa en las garantías que ofrece TCP vs UDP."
```

---

## Validation rules

| Rule | Description |
|---|---|
| `answers` ⊆ `options[].id` | Every answer ID must exist as an option |
| `type: single` → `len(answers) == 1` | Single-answer questions have exactly one correct answer |
| `type: multiple` → `len(answers) >= 2` | Multi-select questions have at least two correct answers |
| `len(options) >= 3` | Minimum 3 options per question (4 recommended) |
| `id` unique | No two questions share the same `id` |
| `difficulty` ∈ {easy, medium, hard} | Only valid difficulty values |
