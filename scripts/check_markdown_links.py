#!/usr/bin/env python3
"""Validate repository-local links in Markdown files without network access."""
from __future__ import annotations
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {'.git', '.venv', 'node_modules'}
LINK_RE = re.compile(r'(?<!!)\[[^\]]*\]\(([^)]+)\)')

def markdown_files():
    for p in ROOT.rglob('*.md'):
        if not any(part in SKIP_DIRS for part in p.parts):
            yield p

def normalize_target(raw: str) -> str:
    target = raw.strip()
    if target.startswith('<') and target.endswith('>'):
        target = target[1:-1]
    # Optional Markdown title after a quoted path is intentionally ignored.
    if ' "' in target:
        target = target.split(' "', 1)[0]
    return unquote(target.split('#', 1)[0])

def main() -> int:
    failures=[]
    checked=0
    for md in markdown_files():
        text=md.read_text(encoding='utf-8')
        # Remove fenced code blocks to avoid checking example Markdown.
        text=re.sub(r'```.*?```', '', text, flags=re.S)
        for match in LINK_RE.finditer(text):
            raw=match.group(1)
            if raw.startswith(('http://','https://','mailto:','#')):
                continue
            target=normalize_target(raw)
            if not target:
                continue
            checked += 1
            resolved=(md.parent/target).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                failures.append((md,raw,'target escapes repository root'))
                continue
            if not resolved.exists():
                failures.append((md,raw,'target does not exist'))
    if failures:
        print('Broken internal Markdown links:')
        for md,raw,why in failures:
            print(f'  {md.relative_to(ROOT)} -> {raw} ({why})')
        return 1
    print(f'OK: checked {checked} internal links across repository Markdown files.')
    return 0

if __name__ == '__main__':
    sys.exit(main())
