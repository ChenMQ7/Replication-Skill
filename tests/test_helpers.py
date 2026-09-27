"""Unit tests use invented ledger rows, not research inputs or paper results."""
from pathlib import Path
import csv
import json
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/applied-empirical-replication-v3'
sys.path.insert(0, str(SKILL / 'scripts'))
sys.path.insert(0, str(ROOT / 'tools'))
from audit_run import audit, display_precision_pass
from init_run import initialize, DIRECTORIES
from skill_files import embedded_templates, template_errors, sha256, read_csv
from check_release import check


class TemporaryCase(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)


class PrecisionTests(unittest.TestCase):
    def test_display_interval(self):
        self.assertTrue(display_precision_pass('0.213', '0.212973378', 3))
        self.assertTrue(display_precision_pass('-0.036', '-0.0362378', 3))
        self.assertFalse(display_precision_pass('0.213', '0.2135', 3))
        self.assertFalse(display_precision_pass('-0.036', '-0.0365', 3))
        self.assertFalse(display_precision_pass('0.213', '0.214', 3))
        self.assertTrue(display_precision_pass('0', '0', 0))

    def test_invalid_precision(self):
        for decimals in [-1, 101, True, 1.5, '3']:
            with self.subTest(decimals=decimals), self.assertRaises(ValueError):
                display_precision_pass('1', '1', decimals)

    def test_invalid_values(self):
        for value in ['NaN', 'Infinity', 'invalid', '1e1001']:
            with self.subTest(value=value), self.assertRaises(ValueError):
                display_precision_pass(value, '1', 3)


class TemplateTests(TemporaryCase):
    def test_all_starters_match(self):
        self.assertEqual(len(embedded_templates()), 63)
        self.assertEqual(template_errors(), [])

    def test_code_access_starter_is_complete(self):
        body = embedded_templates()['code_access_decision.md']
        for field in ['Access policy:', 'Prior author-code exposure',
                      'Replacement code required:', 'Reviewer approval:']:
            self.assertIn(field, body)

    def test_drift_is_detected(self):
        copy = self.base / 'skill'
        shutil.copytree(SKILL, copy)
        (copy / 'templates/input_manifest.yml').write_text('changed\n')
        self.assertTrue(any('differs' in e for e in template_errors(copy)))

    def test_missing_and_unexpected_starters(self):
        copy = self.base / 'skill'
        shutil.copytree(SKILL, copy)
        (copy / 'templates/input_manifest.yml').unlink()
        (copy / 'templates/extra.md').write_text('extra\n')
        errors = template_errors(copy)
        self.assertTrue(any('Missing' in e for e in errors))
        self.assertTrue(any('Unexpected' in e for e in errors))


class InitializationTests(TemporaryCase):
    def setUp(self):
        super().setUp()
        self.paper = self.base / 'paper.txt'
        self.paper.write_text('File-existence fixture. No paper analysis is performed.\n')
        self.destination = self.base / 'run'

    def test_default_intake_only(self):
        original_hash = sha256(self.paper)
        receipt = initialize(self.destination, self.paper, 'Example paper')
        self.assertEqual(receipt['CP0'], 'pending')
        self.assertIsNone(receipt['route_selected'])
        self.assertFalse(receipt['analysis_executed'])
        self.assertFalse(receipt['inputs_inspected'])
        manifest = (self.destination / '00_intake/input_manifest.yml').read_text()
        self.assertIn('independent_reconstruction_requested: false', manifest)
        self.assertIn('next_phase_authorized: false', manifest)
        self.assertNotIn('policy: quarantined', manifest)
        self.assertEqual(original_hash, sha256(self.paper))
        self.assertEqual(receipt['skill_sha256'], sha256(SKILL / 'SKILL.md'))
        for directory in DIRECTORIES:
            self.assertTrue((self.destination / directory).is_dir())
        self.assertEqual(list((self.destination / '07_report').iterdir()), [])

    def test_explicit_independent_intake(self):
        initialize(self.destination, self.paper, 'Example paper', independent=True)
        manifest = (self.destination / '00_intake/input_manifest.yml').read_text()
        self.assertIn('policy: quarantined', manifest)
        self.assertIn('read_allowed: false', manifest)
        self.assertIn('execute_allowed: false', manifest)
        self.assertIn('summarize_allowed: false', manifest)

    def test_existing_empty_directory_is_refused(self):
        self.destination.mkdir()
        with self.assertRaises(ValueError):
            initialize(self.destination, self.paper, 'Example paper')
        self.assertEqual(list(self.destination.iterdir()), [])

    def test_existing_content_is_preserved(self):
        self.destination.mkdir()
        sentinel = self.destination / 'notes.md'
        sentinel.write_text('Keep these notes.\n')
        original_hash = sha256(sentinel)
        with self.assertRaises(ValueError):
            initialize(self.destination, self.paper, 'Example paper')
        self.assertEqual(sha256(sentinel), original_hash)

    def test_symlink_is_refused(self):
        target = self.base / 'target'
        target.mkdir()
        self.destination.symlink_to(target, target_is_directory=True)
        with self.assertRaises(ValueError):
            initialize(self.destination, self.paper, 'Example paper')
        self.assertEqual(list(target.iterdir()), [])

    def test_invalid_inputs_create_nothing(self):
        cases = [(self.destination, self.base / 'absent', 'Title'),
                 (self.destination, self.paper, ' '),
                 (self.base / 'absent/run', self.paper, 'Title')]
        for destination, paper, title in cases:
            with self.subTest(title=title, paper=paper), self.assertRaises((ValueError, OSError)):
                initialize(destination, paper, title)
            self.assertFalse(destination.exists())

    def test_relocated_cli_from_unrelated_directory(self):
        copied = self.base / 'project/.agents/skills/applied-empirical-replication-v3'
        shutil.copytree(SKILL, copied)
        for arguments in [
            [str(copied / 'scripts/sync_templates.py')],
            [str(copied / 'scripts/init_run.py'), str(self.destination),
             '--paper', str(self.paper), '--title', 'Example paper'],
        ]:
            result = subprocess.run([sys.executable, *arguments], cwd=self.base,
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.destination / 'checkpoint_record.md').is_file())


class LedgerTests(TemporaryCase):
    fields = ['result_id', 'comparison_performed', 'comparison_eligibility_id',
              'original_value', 'replicated_value', 'absolute_difference',
              'relative_difference', 'raw_validation_outcome']

    def setUp(self):
        super().setUp()
        outcomes = ['strict_pass', 'pass_with_note', 'residual',
                    'not_comparable', 'not_closed', 'blocked', 'strict_pass', '']
        self.rows = []
        self.eligibility = []
        for index, outcome in enumerate(outcomes):
            key = f't{index}'
            compared = outcome in {'strict_pass', 'pass_with_note', 'residual'}
            self.rows.append(dict(zip(self.fields, [
                key, str(compared).lower(), f'e{index}' if compared else '',
                '1' if compared else '', '1' if compared else '',
                '0' if compared else '', '0' if compared else '', outcome,
            ])))
            if compared:
                self.eligibility.append({'comparison_eligibility_id': f'e{index}',
                                         'result_id': key, 'eligible': 'true'})
        self.ids = [r['result_id'] for r in self.rows]
        self.scope = {'primary_ids': self.ids[:6], 'linked_ids': ['t6'],
                      'other_ids': [], 'excluded_ids': ['t7']}

    def write_csv(self, name, fields, rows):
        with (self.base / name).open('w', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

    def run_audit(self):
        self.write_csv('targets.csv', ['result_id'], [{'result_id': k} for k in self.ids])
        self.write_csv('matrix.csv', self.fields, self.rows)
        self.write_csv('eligibility.csv', ['comparison_eligibility_id', 'result_id', 'eligible'], self.eligibility)
        (self.base / 'scope.json').write_text(json.dumps(self.scope))
        paths = [self.base / n for n in ['targets.csv', 'matrix.csv', 'eligibility.csv', 'scope.json']]
        before = [sha256(p) for p in paths]
        result = audit(*paths)
        self.assertEqual(before, [sha256(p) for p in paths])
        return result

    def test_counts_and_denominators(self):
        result = self.run_audit()
        self.assertEqual([result[k] for k in ['A', 'E', 'S', 'N', 'R']], [6, 3, 1, 1, 1])
        self.assertEqual(result['direct_numerical_coverage'], 0.5)
        self.assertAlmostEqual(result['strict_numerical_pass_rate'], 1/3)
        self.assertAlmostEqual(result['conditional_agreement_rate'], 2/3)
        self.assertAlmostEqual(result['strict_target_attainment'], 1/6)
        self.assertEqual(result['separate_counts']['linked_ids'], 1)

    def test_empty_denominators_are_null(self):
        self.scope['other_ids'] = self.scope['primary_ids']
        self.scope['primary_ids'] = []
        result = self.run_audit()
        for key in ['direct_numerical_coverage', 'strict_numerical_pass_rate',
                    'conditional_agreement_rate', 'strict_target_attainment']:
            self.assertIsNone(result[key])

    def test_no_compared_results(self):
        self.scope['other_ids'] = self.scope['primary_ids'][:3]
        self.scope['primary_ids'] = self.scope['primary_ids'][3:]
        result = self.run_audit()
        self.assertEqual(result['direct_numerical_coverage'], 0)
        self.assertIsNone(result['strict_numerical_pass_rate'])

    def test_missing_matrix_row(self):
        self.rows.pop()
        with self.assertRaises(ValueError): self.run_audit()

    def test_duplicate_id(self):
        self.rows.append(self.rows[0].copy())
        with self.assertRaises(ValueError): self.run_audit()

    def test_false_comparison_flag_with_pass(self):
        self.rows[0]['comparison_performed'] = 'false'
        with self.assertRaises(ValueError): self.run_audit()

    def test_unknown_status(self):
        self.rows[0]['raw_validation_outcome'] = 'accepted'
        with self.assertRaises(ValueError): self.run_audit()

    def test_noncompared_difference(self):
        self.rows[3]['absolute_difference'] = '0'
        with self.assertRaises(ValueError): self.run_audit()

    def test_excluded_pass(self):
        self.rows[7]['raw_validation_outcome'] = 'strict_pass'
        with self.assertRaises(ValueError): self.run_audit()

    def test_missing_eligibility(self):
        self.eligibility.pop(0)
        with self.assertRaises(ValueError): self.run_audit()

    def test_ineligible_comparison(self):
        self.eligibility[0]['eligible'] = 'false'
        with self.assertRaises(ValueError): self.run_audit()

    def test_mismatched_eligibility(self):
        self.eligibility[0]['result_id'] = 't3'
        with self.assertRaises(ValueError): self.run_audit()

    def test_nonfinite_value(self):
        self.rows[0]['replicated_value'] = 'NaN'
        with self.assertRaises(ValueError): self.run_audit()

    def test_negative_absolute_difference(self):
        self.rows[0]['absolute_difference'] = '-1'
        with self.assertRaises(ValueError): self.run_audit()

    def test_overlapping_scope(self):
        self.scope['linked_ids'].append('t0')
        with self.assertRaises(ValueError): self.run_audit()

    def test_unpartitioned_target(self):
        self.scope['primary_ids'].pop()
        with self.assertRaises(ValueError): self.run_audit()

    def test_malformed_csv(self):
        for body in ['result_id,result_id\na,b\n', 'result_id,value\na\n', 'result_id\na,b\n']:
            path = self.base / 'bad.csv'
            path.write_text(body)
            with self.subTest(body=body), self.assertRaises(ValueError):
                read_csv(path, ['result_id'])


class ReleaseTests(TemporaryCase):
    def test_release_structure(self):
        self.assertEqual(check(ROOT), [])

    def test_unapproved_release_is_rejected(self):
        copied = self.base / 'release'
        shutil.copytree(ROOT, copied, ignore=shutil.ignore_patterns('__pycache__', '.git'))
        path = copied / 'release.json'
        metadata = json.loads(path.read_text())
        metadata['status'] = 'released'
        path.write_text(json.dumps(metadata))
        self.assertTrue(any('publication approval' in e for e in check(copied)))

    def test_broken_link_is_detected(self):
        copied = self.base / 'release'
        shutil.copytree(ROOT, copied, ignore=shutil.ignore_patterns('__pycache__', '.git'))
        path = copied / 'README.md'
        path.write_text(path.read_text() + '\n[Missing file](docs/absent.md)\n')
        self.assertTrue(any('Invalid local link' in e for e in check(copied)))


if __name__ == '__main__':
    unittest.main()
