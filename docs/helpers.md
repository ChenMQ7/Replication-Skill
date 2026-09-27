# Optional helpers

All helpers use Python 3.10 or later and its standard library. They make no network calls and do not run statistical software. Run their `--help` commands for options.

## Initialize a run

`skills/applied-empirical-replication-v3/scripts/init_run.py` creates the folders and Phase 0 starters described in [getting started](getting-started.md). It refuses any existing destination, including an empty folder or a symlink. It records CP0 as pending and saves the instruction snapshot. The operator still needs to inventory the inputs, complete the audit and request approval.

## Synchronize templates

```sh
python3 skills/applied-empirical-replication-v3/scripts/sync_templates.py
```

This read-only check compares the 63 starter files with Section 16. `--write` regenerates those copies after an intentional specification change. It does not remove unexpected files or update existing research runs. Review the diff before committing.

## Check a numerical ledger

```sh
python3 skills/applied-empirical-replication-v3/scripts/audit_run.py \
  --targets "replication_runs/my-paper/03_result_mapping/paper_target_table.csv" \
  --matrix "replication_runs/my-paper/06_validation/comparison_matrix.csv" \
  --eligibility "replication_runs/my-paper/06_validation/comparison_eligibility_audit.csv" \
  --scope "replication_runs/my-paper/06_validation/check_scope.json"
```

For a versioned review, pass the actual approved file paths. The checker does not choose a version by modification time.

`check_scope.json` is an optional helper input derived from the reviewed target register. It partitions every registered ID exactly once:

```json
{
  "primary_ids": ["T1.coefficient"],
  "linked_ids": ["text.linked_coefficient"],
  "other_ids": [],
  "excluded_ids": []
}
```

The names above illustrate the file format. Use the actual target IDs and the approved primary numerical universe. The helper cannot decide which items deserve primary numerical credit. Keep the scope file and its approval evidence with the validation artifacts.

The matrix must contain one row per registered ID, including holds and any excluded items represented in that register. For this helper, an excluded row has `comparison_performed=false`, blank differences and a blank raw outcome. Exclusion approval belongs in scope governance. This convention adds no raw status to the skill.

The checker rejects duplicate or missing IDs, overlapping scope groups, unknown raw outcomes, inconsistent comparison flags, missing eligibility references for compared rows and populated differences on non-compared rows. Its JSON output reports A, E, S, N, R and the four Section 5.9 rates. A zero denominator returns `null`. Linked displays and other groups are counted separately.

The check does not establish source semantics, validate the numerical pass/residual decision, authenticate approvals, inspect figures, determine family closure or reconcile report prose. It leaves all input files unchanged. A zero exit code means only that its stated mechanical checks passed.

The module also exposes `display_precision_pass` for unit testing the strict interval in Section 5.5. Call it only with eligible values already expressed in matching units. It deliberately rejects the exact half-unit boundary and nonfinite values. It is not used to override a frozen target-specific standard.

## Exit codes

The ledger and initialization tools return `0` for their stated successful operation and `2` for invalid inputs or file errors. The template checker returns `1` for differences and `2` for an invalid file operation. The repository checker returns `1` for a release-file problem. None of these codes authorizes a checkpoint or states a paper-level result.
