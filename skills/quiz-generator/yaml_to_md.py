#!/usr/bin/env python3
"""Convert a quiz YAML file to a Markdown summary.

Usage:
    python yaml_to_md.py <quiz.yaml>

Output: <quiz>-summary.md in the same directory.
"""

import sys
import yaml
from collections import defaultdict
from pathlib import Path


def render_md(quiz):
    title = quiz.get('title', 'Quiz')
    source = quiz.get('source', '')
    generated_at = str(quiz.get('generated_at', ''))
    questions = quiz.get('questions', [])
    n = len(questions)

    # --- header ---
    lines = [
        f'# Quiz Summary: {title}',
        '',
        f'**Source:** {source}',
        f'**Generated:** {generated_at}',
        f'**Total questions:** {n}',
        '',
        '---',
        '',
    ]

    # --- coverage map by topic ---
    topic_counts = defaultdict(lambda: defaultdict(int))
    for q in questions:
        topic = q.get('topic', 'Other')
        qtype = q.get('type', 'single')
        topic_counts[topic]['total'] += 1
        topic_counts[topic][qtype] += 1

    lines += [
        '## Coverage by Topic',
        '',
        '| Topic | Questions | Types |',
        '|---|---|---|',
    ]
    for topic, counts in topic_counts.items():
        total = counts['total']
        type_parts = []
        if counts.get('single'):
            type_parts.append(f"{counts['single']} single")
        if counts.get('multiple'):
            type_parts.append(f"{counts['multiple']} multiple")
        lines.append(f'| {topic} | {total} | {", ".join(type_parts)} |')

    lines += ['', '---', '']

    # --- coverage map by tag ---
    tag_counts = defaultdict(lambda: defaultdict(int))
    for q in questions:
        qtype = q.get('type', 'single')
        for tag in q.get('tags', []):
            tag_counts[tag]['total'] += 1
            tag_counts[tag][qtype] += 1

    lines += [
        '## Coverage by Tag',
        '',
        '| Topic / Tag | Questions | Types |',
        '|---|---|---|',
    ]
    for tag, counts in tag_counts.items():
        total = counts['total']
        type_parts = []
        if counts.get('single'):
            type_parts.append(f"{counts['single']} single")
        if counts.get('multiple'):
            type_parts.append(f"{counts['multiple']} multiple")
        lines.append(f'| {tag} | {total} | {", ".join(type_parts)} |')

    lines += ['', '---', '']

    # --- difficulty breakdown ---
    diff_counts = defaultdict(int)
    for q in questions:
        diff_counts[q.get('difficulty', 'medium')] += 1

    diff_order = ['easy', 'medium', 'hard']
    diff_parts = [
        f"{diff_counts[d]} {d}"
        for d in diff_order
        if diff_counts[d]
    ]
    lines += [
        '## Statistics',
        '',
        f'**Difficulty:** {" · ".join(diff_parts)}',
        '',
        '---',
        '',
    ]

    # --- questions at a glance ---
    lines += ['## Questions at a Glance', '']
    for i, q in enumerate(questions, 1):
        lines.append(f'{i}. {q["question"]} ')

    lines.append('')
    return '\n'.join(lines)


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
    md_content = render_md(quiz)

    stem = yaml_path.stem.removesuffix('-quiz')
    out_path = yaml_path.parent / f'{stem}-quiz-summary.md'
    out_path.write_text(md_content, encoding='utf-8')
    print(f'Written: {out_path}')


if __name__ == '__main__':
    main()
