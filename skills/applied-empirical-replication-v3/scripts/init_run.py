"""Create a new Phase 0 scaffold without reading code or running analysis."""
from pathlib import Path
import argparse
import json
import re
import sys
from skill_files import SKILL_ROOT, embedded_templates, sha256, template_errors

DIRECTORIES = [
    '00_intake', '01_paper_understanding', '02_source_and_artifact_audit',
    '03_result_mapping/table_schemas', '04_environment_plan',
    '05_execution/build/scripts', '05_execution/logs',
    '05_execution/generated_outputs/figure_backing_artifacts',
    '06_validation/figure_validation', '07_report',
]
INTAKE = [
    'input_manifest.yml', 'scope_confirmation.md', 'artifact_inventory.csv',
    'environment_requirements_precheck.md', 'code_access_decision.md', 'route_decision.md',
]


def initialize(destination, paper, title, reviewer='user', independent=False):
    dest = Path(destination).expanduser().absolute()
    paper = Path(paper).expanduser().resolve(strict=True)
    if not paper.is_file():
        raise ValueError('Paper path must name a file.')
    if not title.strip() or not reviewer.strip():
        raise ValueError('Title and reviewer must be nonempty.')
    if dest.exists() or dest.is_symlink():
        raise ValueError('Run directory already exists. Resume it after reviewing its checkpoint record, or choose a new path.')
    if not dest.parent.is_dir():
        raise ValueError('Create the intended run-parent directory first.')
    errors = template_errors()
    if errors:
        raise ValueError('; '.join(errors))
    source = (SKILL_ROOT / 'SKILL.md').read_text(encoding='utf-8')
    revision = re.search(r'^  revision: "([^"]+)"$', source, re.M)
    if revision is None:
        raise ValueError('Cannot identify the instruction revision.')
    templates = embedded_templates()
    manifest = templates['input_manifest.yml']
    manifest = manifest.replace('  title:\n', '  title: ' + json.dumps(title) + '\n', 1)
    manifest = manifest.replace('  local_path:\n', '  local_path: ' + json.dumps(str(paper)) + '\n', 1)
    manifest = manifest.replace('  name:\n', '  name: ' + json.dumps(reviewer) + '\n', 1)
    manifest = manifest.replace('  role:\n', '  role: checkpoint reviewer\n', 1)
    manifest = manifest.replace('  independent_reconstruction_requested:\n', '  independent_reconstruction_requested: ' + str(independent).lower() + '\n')
    if independent:
        manifest = manifest.replace('  policy:\n', '  policy: quarantined\n')
        manifest = manifest.replace('  request_evidence:\n', '  request_evidence: "Explicit --independent-reconstruction option; record the user request during intake."\n')
        for key in ['read_allowed','execute_allowed','summarize_allowed']:
            manifest = manifest.replace(f'  {key}:\n', f'  {key}: false\n')
    manifest += '\nrun:\n  phase: 0\n  checkpoint: CP0\n  checkpoint_status: pending\n  next_phase_authorized: false\n'
    manifest += '  skill_revision: ' + json.dumps(revision[1]) + '\n'
    manifest += '  skill_sha256: ' + json.dumps(sha256(SKILL_ROOT / 'SKILL.md')) + '\n'
    # Reserve the destination exclusively. Partial failures remain visible for inspection.
    dest.mkdir()
    for directory in DIRECTORIES:
        (dest / directory).mkdir(parents=True, exist_ok=True)
    for name in INTAKE:
        body = manifest if name == 'input_manifest.yml' else templates[name]
        (dest / '00_intake' / name).write_text(body, encoding='utf-8')
    for name in ['phase_roadmap.md','checkpoint_record.md']:
        (dest / name).write_text(templates[name], encoding='utf-8')
    snapshot = dest / '00_intake/skill_snapshot'
    snapshot.mkdir()
    (snapshot / 'SKILL.md').write_text(source, encoding='utf-8')
    receipt = {
        'skill_revision': revision[1], 'skill_sha256': sha256(snapshot / 'SKILL.md'),
        'snapshot': '00_intake/skill_snapshot/SKILL.md',
        'scaffold_only': True, 'CP0': 'pending', 'analysis_executed': False,
        'inputs_inspected': False, 'route_selected': None,
    }
    (dest / '00_intake/skill_version.json').write_text(json.dumps(receipt, indent=2)+'\n', encoding='utf-8')
    return receipt


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run_directory', type=Path)
    parser.add_argument('--paper', type=Path, required=True)
    parser.add_argument('--title', required=True)
    parser.add_argument('--reviewer', default='user')
    parser.add_argument('--independent-reconstruction', action='store_true', help='Use only when the user explicitly requested independent reconstruction.')
    args = parser.parse_args(argv)
    try:
        receipt = initialize(args.run_directory, args.paper, args.title, args.reviewer, args.independent_reconstruction)
        print(json.dumps(receipt, indent=2))
        print('Complete the Phase 0 audit and request CP0 approval. No later phase is authorized.')
        return 0
    except (OSError, ValueError, IndexError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
