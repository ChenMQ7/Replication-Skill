"""Shared file handling for optional skill helpers. Python standard library only."""
from pathlib import Path
import csv
import hashlib
import re

SKILL_ROOT = Path(__file__).resolve().parents[1]


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def embedded_templates(skill_root=SKILL_ROOT):
    text = (Path(skill_root) / 'SKILL.md').read_text(encoding='utf-8')
    library = text.split('## 16. Canonical Template Library\n', 1)[1]
    library = library.split('## 17. Operational Use and Maintenance\n', 1)[0]
    matches = re.findall(r'^#### ([\w.-]+)\n\n```[^\n]*\n(.*?)\n```', library, re.M | re.S)
    result = {}
    for name, body in matches:
        if name in result or not re.fullmatch(r'[a-z][a-z0-9_]*\.(md|csv|yml|txt)', name):
            raise ValueError(f'Invalid or duplicate template name: {name}')
        result[name] = body + '\n'
    if not result:
        raise ValueError('No embedded templates found.')
    return result


def template_errors(skill_root=SKILL_ROOT):
    root = Path(skill_root)
    embedded = embedded_templates(root)
    errors = []
    actual = {p.name for p in (root / 'templates').iterdir() if p.name != 'README.md'}
    for name in sorted(actual - embedded.keys()):
        errors.append(f'Unexpected template: {name}')
    for name, expected in embedded.items():
        path = root / 'templates' / name
        if path.is_symlink() or not path.is_file():
            errors.append(f'Missing or non-regular template: {name}')
        elif path.read_text(encoding='utf-8') != expected:
            errors.append(f'Template differs from SKILL.md: {name}')
    return errors


def read_csv(path, required):
    with Path(path).open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        fields = reader.fieldnames or []
        if len(fields) != len(set(fields)):
            raise ValueError(f'{Path(path).name}: duplicate column names')
        missing = set(required) - set(fields)
        if missing:
            raise ValueError(f'{Path(path).name}: missing columns {sorted(missing)}')
        rows = list(reader)
    for row in rows:
        if None in row or any(value is None for value in row.values()):
            raise ValueError(f'{Path(path).name}: malformed CSV row')
    return rows


def unique_index(rows, field, label):
    result = {}
    for row in rows:
        key = row[field].strip()
        if not key or key in result:
            raise ValueError(f'{label}: blank or duplicate {field}: {key!r}')
        result[key] = row
    return result
