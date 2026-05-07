#!/usr/bin/env python3
"""Convert a quiz YAML file to an interactive HTML page.

Usage:
    python yaml_to_html.py <quiz.yaml>

Output: <quiz>.html in the same directory.
Options and question order are shuffled randomly each time the page is loaded in the browser.
"""

import sys
import yaml
import html as html_lib
from pathlib import Path

DIFFICULTY_BADGE = {
    'easy': 'badge-easy',
    'medium': 'badge-medium',
    'hard': 'badge-hard',
}

_CSS = """    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: system-ui, -apple-system, sans-serif;
      background: #f5f7fa;
      color: #1a1a2e;
      padding: 2rem 1rem;
    }
    .container { max-width: 800px; margin: 0 auto; }
    h1 { font-size: 1.8rem; margin-bottom: 0.25rem; }
    .meta { color: #666; font-size: 0.85rem; margin-bottom: 2rem; }

    .question {
      background: #fff;
      border: 1px solid #e0e4ef;
      border-radius: 10px;
      padding: 1.5rem;
      margin-bottom: 1.5rem;
    }
    .question-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 1rem;
      margin-bottom: 1rem;
    }
    .question-text { font-weight: 600; font-size: 1rem; flex: 1; }
    .badge {
      font-size: 0.7rem;
      font-weight: 700;
      text-transform: uppercase;
      padding: 3px 8px;
      border-radius: 20px;
      white-space: nowrap;
    }
    .badge-easy   { background: #d4edda; color: #155724; }
    .badge-medium { background: #fff3cd; color: #856404; }
    .badge-hard   { background: #f8d7da; color: #721c24; }

    .question-meta {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      flex-wrap: wrap;
      margin-bottom: 1rem;
      font-size: 0.78rem;
      color: #555;
    }
    .topic-label {
      font-weight: 600;
      color: #4a6cf7;
    }
    .tag {
      background: #eef0ff;
      color: #4a6cf7;
      padding: 2px 7px;
      border-radius: 20px;
      font-size: 0.72rem;
    }

    .options { list-style: none; display: flex; flex-direction: column; gap: 0.5rem; }
    .option-label {
      display: flex;
      align-items: center;
      gap: 0.6rem;
      padding: 0.6rem 0.8rem;
      border: 1px solid #dee2e6;
      border-radius: 6px;
      cursor: pointer;
      transition: background 0.15s;
    }
    .option-label:hover { background: #f0f2ff; }
    .option-label input { accent-color: #4a6cf7; }

    .option-label.correct  { background: #d4edda; border-color: #28a745; }
    .option-label.wrong    { background: #f8d7da; border-color: #dc3545; }
    .option-label.missed   { background: #fff3cd; border-color: #ffc107; }

    .check-btn {
      margin-top: 1rem;
      padding: 0.5rem 1.2rem;
      background: #4a6cf7;
      color: #fff;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      font-size: 0.9rem;
      font-weight: 600;
    }
    .check-btn:hover:not(:disabled) { background: #3756d6; }
    .check-btn:disabled { opacity: 0.5; cursor: not-allowed; }

    .explanation {
      display: none;
      margin-top: 1rem;
      padding: 0.75rem 1rem;
      background: #eef0ff;
      border-left: 4px solid #4a6cf7;
      border-radius: 0 6px 6px 0;
      font-size: 0.9rem;
      color: #333;
    }

    #score-area {
      text-align: center;
      margin-top: 2rem;
      padding: 2rem;
      background: #fff;
      border: 1px solid #e0e4ef;
      border-radius: 10px;
    }
    #score-btn {
      padding: 0.75rem 2rem;
      background: #198754;
      color: #fff;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      font-size: 1rem;
      font-weight: 700;
    }
    #score-btn:hover { background: #157347; }
    #score-result {
      margin-top: 1.25rem;
      font-size: 1.4rem;
      font-weight: 700;
    }
    .score-pass { color: #155724; }
    .score-fail { color: #721c24; }

    #quiz-form { display: flex; flex-direction: column; }
    .topic-scores { margin-top: 1rem; text-align: left; display: inline-block; min-width: 220px; }
    .topic-score-row {
      display: flex;
      justify-content: space-between;
      gap: 1.5rem;
      font-size: 0.9rem;
      padding: 0.3rem 0;
      border-bottom: 1px solid #e0e4ef;
    }
    .topic-score-row:last-child { border-bottom: none; }
    .topic-score-name { color: #4a6cf7; font-weight: 600; }
    .topic-score-val { color: #555; }
    .question-number {
      font-size: 0.75rem;
      font-weight: 700;
      color: #aaa;
      margin-bottom: 0.35rem;
      display: block;
    }
"""

# JS is a plain string — NOT an f-string — so ${...} template literals are safe.
_JS = """
  (function () {
    function shuffle(arr) {
      for (let i = arr.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [arr[i], arr[j]] = [arr[j], arr[i]];
      }
    }

    function assignRandomOrder(items) {
      const orders = items.map((_, i) => i);
      shuffle(orders);
      items.forEach((el, i) => { el.style.order = orders[i]; });
    }

    window.addEventListener('pageshow', function () {
      const questions = [...document.querySelectorAll('.question')];
      assignRandomOrder(questions);
      questions
        .slice()
        .sort((a, b) => parseInt(a.style.order) - parseInt(b.style.order))
        .forEach((q, i) => { q.querySelector('.question-number').textContent = 'Question ' + (i + 1); });

      document.querySelectorAll('.options').forEach(ul => {
        assignRandomOrder([...ul.querySelectorAll('li')]);
      });
    });

    const results = {};

    document.querySelectorAll('.check-btn').forEach(btn => {
      btn.addEventListener('click', function () {
        const section = this.closest('.question');
        const qId = section.dataset.id;
        const type = section.dataset.type;
        const correct = new Set(section.dataset.answers.split(',').map(s => s.trim()));

        let selected;
        if (type === 'single') {
          const checked = section.querySelector('input[type=radio]:checked');
          selected = new Set(checked ? [checked.value] : []);
        } else {
          selected = new Set(
            [...section.querySelectorAll('input[type=checkbox]:checked')].map(i => i.value)
          );
        }

        const isFullyCorrect =
          selected.size === correct.size &&
          [...selected].every(v => correct.has(v));

        results[qId] = isFullyCorrect;

        section.querySelectorAll('.option-label').forEach(label => {
          const input = label.querySelector('input');
          const val = input.value;
          label.classList.remove('correct', 'wrong', 'missed');
          if (correct.has(val) && selected.has(val)) {
            label.classList.add('correct');
          } else if (!correct.has(val) && selected.has(val)) {
            label.classList.add('wrong');
          } else if (correct.has(val) && !selected.has(val)) {
            label.classList.add('missed');
          }
          input.disabled = true;
        });

        section.querySelector('.explanation').style.display = 'block';
        this.disabled = true;
      });
    });

    document.getElementById('score-btn').addEventListener('click', function () {
      const questions = [...document.querySelectorAll('.question')];
      const total = questions.length;
      const correct = Object.values(results).filter(Boolean).length;
      const pct = Math.round((correct / total) * 100);

      const byTopic = {};
      questions.forEach(q => {
        const topic = q.dataset.topic || 'Other';
        if (!byTopic[topic]) byTopic[topic] = { correct: 0, total: 0 };
        byTopic[topic].total++;
        if (results[q.dataset.id]) byTopic[topic].correct++;
      });

      const topicRows = Object.entries(byTopic)
        .map(([topic, s]) => `<div class="topic-score-row">
          <span class="topic-score-name">${topic}</span>
          <span class="topic-score-val">${s.correct} / ${s.total}</span>
        </div>`)
        .join('');

      const el = document.getElementById('score-result');
      el.innerHTML = `<div>Score: ${correct} / ${total} — ${pct}%</div>
        <div class="topic-scores">${topicRows}</div>`;
      el.className = pct >= 60 ? 'score-pass' : 'score-fail';
      el.hidden = false;
    });
  })();
"""


def e(text):
    return html_lib.escape(str(text))


def render_question(q):
    qid = q['id']
    qtype = q['type']
    answers = ','.join(str(a) for a in q['answers'])
    difficulty = q.get('difficulty', 'medium')
    badge_class = DIFFICULTY_BADGE.get(difficulty, 'badge-medium')
    topic = q.get('topic', '')
    tags = q.get('tags', [])
    input_type = 'radio' if qtype == 'single' else 'checkbox'

    tags_html = '\n        '.join(f'<span class="tag">{e(tag)}</span>' for tag in tags)
    if topic or tags:
        sep = '\n        &middot;' if tags_html else ''
        meta_block = (
            f'      <div class="question-meta">\n'
            f'        <span class="topic-label">{e(topic)}</span>{sep}\n'
            f'        {tags_html}\n'
            f'      </div>\n'
        )
    else:
        meta_block = ''

    options_lines = ''.join(
        f'        <li><label class="option-label">'
        f'<input type="{input_type}" name="q{qid}" value="{e(opt["id"])}"> '
        f'{e(opt["text"])}</label></li>\n'
        for opt in q['options']
    )

    return (
        f'    <!-- Question {qid} -->\n'
        f'    <section class="question" data-id="{qid}" data-type="{qtype}" data-answers="{answers}" data-topic="{e(topic)}">\n'
        f'      <div class="question-header">\n'
        f'        <div style="flex:1">\n'
        f'          <span class="question-number"></span>\n'
        f'          <p class="question-text">{e(q["question"])}</p>\n'
        f'        </div>\n'
        f'        <span class="badge {badge_class}" style="align-self:flex-start">{e(difficulty.capitalize())}</span>\n'
        f'      </div>\n'
        f'{meta_block}'
        f'      <ul class="options">\n'
        f'{options_lines}'
        f'      </ul>\n'
        f'      <button type="button" class="check-btn">Check answer</button>\n'
        f'      <p class="explanation">{e(q["explanation"])}</p>\n'
        f'    </section>\n'
    )


def render_html(quiz):
    title = quiz.get('title', 'Quiz')
    source = quiz.get('source', '')
    generated_at = str(quiz.get('generated_at', ''))
    language = quiz.get('language', 'en')
    questions = quiz.get('questions', [])
    n = len(questions)

    questions_html = '\n'.join(render_question(q) for q in questions)

    parts = [
        f'<!DOCTYPE html>\n',
        f'<html lang="{e(language)}">\n',
        f'<head>\n',
        f'  <meta charset="UTF-8">\n',
        f'  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n',
        f'  <title>{e(title)}</title>\n',
        f'  <style>\n',
        _CSS,
        f'  </style>\n',
        f'</head>\n',
        f'<body>\n',
        f'<div class="container">\n',
        f'  <h1>{e(title)}</h1>\n',
        f'  <p class="meta">Source: {e(source)} &middot; Generated: {e(generated_at)} &middot; {n} questions</p>\n',
        f'\n',
        f'  <form id="quiz-form">\n',
        f'\n',
        questions_html,
        f'\n',
        f'  </form>\n',
        f'\n',
        f'  <div id="score-area">\n',
        f'    <button type="button" id="score-btn">See my score</button>\n',
        f'    <div id="score-result" hidden></div>\n',
        f'  </div>\n',
        f'</div>\n',
        f'\n',
        f'<script>\n',
        _JS.lstrip('\n'),
        f'</script>\n',
        f'</body>\n',
        f'</html>\n',
    ]
    return ''.join(parts)


def main():
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} <quiz.yaml>', file=sys.stderr)
        sys.exit(1)

    yaml_path = Path(sys.argv[1])
    if not yaml_path.exists():
        print(f'Error: {yaml_path} not found', file=sys.stderr)
        sys.exit(1)

    with open(yaml_path, encoding='utf-8') as f:
        data = yaml.safe_load(f)

    quiz = data['quiz']
    html_content = render_html(quiz)

    out_path = yaml_path.with_suffix('.html')
    out_path.write_text(html_content, encoding='utf-8')
    print(f'Written: {out_path}')


if __name__ == '__main__':
    main()
