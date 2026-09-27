"""Read-only structural checks for this repository, without network access."""
from pathlib import Path
from urllib.parse import unquote, urlsplit
import argparse
import csv
import io
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'skills/applied-empirical-replication-v3/scripts'))
from skill_files import embedded_templates, template_errors

SKILL_REL = Path('skills/applied-empirical-replication-v3')
IGNORED = {'.git', '__pycache__', '.venv'}


def without_fences(text):
    lines = []; fence = None
    for line in text.splitlines():
        match = re.match(r'^\s*(`{3,}|~{3,})', line)
        if match:
            token = match[1]
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            continue
        if fence is None:
            lines.append(line)
    if fence is not None:
        raise ValueError('Unclosed Markdown fence')
    return '\n'.join(lines)


def anchors(text):
    counts = {}; result = set()
    for line in without_fences(text).splitlines():
        match = re.match(r'^#{1,6}\s+(.+?)\s*#*$', line)
        if not match: continue
        base = re.sub(r'[^\w\- ]', '', match[1].lower()).replace(' ', '-')
        index = counts.get(base, 0); counts[base] = index + 1
        result.add(base if index == 0 else f'{base}-{index}')
    return result


def check(root=ROOT):
    root = Path(root).resolve()
    skill = root / SKILL_REL
    errors = []
    required = ['README.md','LICENSE','CHANGELOG.md','CONTRIBUTING.md','release.json',
                'docs/getting-started.md','docs/reviewing-checkpoints.md','docs/tested-cases.md',
                'docs/helpers.md','docs/release-checks.md',str(SKILL_REL/'SKILL.md'),
                '.github/workflows/check.yml','.github/ISSUE_TEMPLATE/bug_report.md']
    for name in required:
        if not (root/name).is_file(): errors.append(f'Missing release file: {name}')
    if errors: return errors
    release = json.loads((root/'release.json').read_text(encoding='utf-8'))
    text = (skill/'SKILL.md').read_text(encoding='utf-8')
    front = re.match(r'\A---\n(.*?)\n---\n', text, re.S)
    if front is None:
        errors.append('Missing YAML frontmatter')
    else:
        # Intentionally narrow: project metadata uses scalar values only.
        expected = {
            'name': release['skill'], 'license': 'MIT',
            'revision': json.dumps(release['version']),
        }
        for key, value in expected.items():
            if not re.search(r'^\s*'+key+': '+re.escape(value)+r'$', front[1], re.M):
                errors.append(f'Frontmatter disagrees with release metadata: {key}')
        if not re.search(r'^description: .+', front[1], re.M): errors.append('Missing description')
    if release['status'] not in {'candidate','released'}: errors.append('Unknown release status')
    if release['status']=='released' and not all(release.get(k) is True for k in ['publication_approved','fresh_session_end_to_end_verified']):
        errors.append('Released status requires publication approval and recorded end-to-end acceptance')
    outside = without_fences(text)
    if re.findall(r'^## (\d+)\. ', outside, re.M) != [str(i) for i in range(1,18)]:
        errors.append('Expected 17 numbered normative sections')
    errors.extend(template_errors(skill))
    for name, body in embedded_templates(skill).items():
        if name.endswith('.csv'):
            fields = next(csv.reader(io.StringIO(body)))
            if len(fields)!=len(set(fields)) or any(not f for f in fields):
                errors.append(f'Invalid CSV header: {name}')
    if (root/'CITATION.cff').exists(): errors.append('This release excludes CITATION.cff')
    if (skill/'templates/source_recovery_event.md').exists(): errors.append('Obsolete starter in package')
    patterns = [
        (r'/(?:Users|home)/[^\s/]+', 'personal absolute path'),
        (r'(?i)\b(?:ghp|github_pat)_[A-Za-z0-9_]{20,}', 'possible GitHub credential'),
        (r'\bsk-[A-Za-z0-9_-]{24,}', 'possible API credential'),
        (r'-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----', 'private key'),
        (r'[\u3400-\u9fff]', 'non-English CJK text'),
    ]
    allowed_roots={'README.md','LICENSE','CHANGELOG.md','CONTRIBUTING.md','.gitignore','release.json','skills','docs','tests','tools','.github'}
    for child in root.iterdir():
        if child.name not in allowed_roots | IGNORED:
            errors.append(f'Unexpected top-level release item: {child.name}')
    for path in root.rglob('*'):
        rel=path.relative_to(root)
        if any(p in IGNORED for p in rel.parts): continue
        if path.is_symlink():
            errors.append(f'Symlink in release: {rel}'); continue
        if not path.is_file(): continue
        if path.name=='.DS_Store' or path.suffix.lower() in {'.pdf','.rds','.dta','.parquet','.zip','.png','.jpg','.xlsx'}:
            errors.append(f'Unapproved binary or research input: {rel}'); continue
        if path.stat().st_size > 1024*1024:
            errors.append(f'Unexpected large release file: {rel}'); continue
        try: body=path.read_text(encoding='utf-8')
        except UnicodeError:
            errors.append(f'Non-text release file: {rel}'); continue
        for pattern,label in patterns:
            if re.search(pattern,body): errors.append(f'{label}: {rel}')
        if path.suffix != '.md': continue
        try: prose=without_fences(body)
        except ValueError as exc:
            errors.append(f'{rel}: {exc}'); continue
        for target in re.findall(r'\]\(([^\s)]+)\)',prose):
            parsed=urlsplit(target)
            if parsed.scheme or target.startswith('//'): continue
            dest=(path.parent/unquote(parsed.path)).resolve() if parsed.path else path
            if not dest.is_relative_to(root) or not dest.is_file():
                errors.append(f'Invalid local link in {rel}: {target}'); continue
            if parsed.fragment and dest.suffix=='.md' and unquote(parsed.fragment) not in anchors(dest.read_text(encoding='utf-8')):
                errors.append(f'Invalid anchor in {rel}: {target}')
    return errors


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=ROOT,help='Check another copy of this release tree.')
    args=parser.parse_args()
    try: errors=check(args.root)
    except (OSError,ValueError,KeyError,IndexError) as exc: errors=[str(exc)]
    print(json.dumps({'passed':not errors,'errors':errors,'claim':'Static package checks only'},indent=2))
    return 1 if errors else 0


if __name__=='__main__':
    sys.exit(main())
