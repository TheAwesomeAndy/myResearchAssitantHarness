#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

from pathlib import Path

MARKERS = ['data_local', 'restricted_data']
EXTENSIONS = {'.md', '.tex', '.txt', '.py', '.yml', '.yaml', '.json'}
SKIP = {'.git', '.venv', 'venv', '__pycache__'}

findings = []
for path in Path('.').rglob('*'):
    if not path.is_file():
        continue
    if path.suffix.lower() not in EXTENSIONS:
        continue
    if any(part in SKIP for part in path.parts):
        continue
    text = path.read_text(encoding='utf-8', errors='replace')
    for marker in MARKERS:
        pos = text.find(marker)
        if pos >= 0:
            line = text.count('\n', 0, pos) + 1
            findings.append(f'{path}:{line}: {marker}')

if findings:
    print('path marker check failed')
    print('\n'.join(findings))
    raise SystemExit(1)

print('path marker check passed')
