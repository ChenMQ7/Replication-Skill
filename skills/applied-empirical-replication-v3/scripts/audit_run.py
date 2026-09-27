"""Check numerical-ledger structure and counts. Does not approve a replication."""
from collections import Counter
from decimal import Decimal, InvalidOperation, localcontext
from pathlib import Path
import argparse
import json
import sys
from skill_files import read_csv, unique_index

COMPARED = {'strict_pass', 'pass_with_note', 'residual'}
UNCOMPARED = {'not_comparable', 'not_closed', 'blocked'}
SCOPE_GROUPS = {'primary_ids', 'linked_ids', 'other_ids', 'excluded_ids'}


def finite(value):
    try:
        result = Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError(f'Invalid number: {value!r}') from exc
    if not result.is_finite():
        raise ValueError(f'Nonfinite number: {value!r}')
    return result


def display_precision_pass(original, reproduced, decimals):
    """Section 5.5, for eligible values already expressed in the same units.

    This deliberately uses the strict open interval in SKILL.md. It is not a
    generic rounding implementation and does not decide analytical eligibility.
    """
    if isinstance(decimals, bool) or not isinstance(decimals, int) or not 0 <= decimals <= 100:
        raise ValueError('Decimal places must be an integer between 0 and 100.')
    x, r = finite(original), finite(reproduced)
    if max(abs(x.adjusted()), abs(r.adjusted())) > 1000:
        raise ValueError('Magnitude exceeds this helper\'s supported range.')
    with localcontext() as context:
        context.prec = max(50, len(x.as_tuple().digits), len(r.as_tuple().digits), decimals + 5) + 2200
        return abs(x - r) < Decimal('0.5') * (Decimal(10) ** -decimals)


def boolean(value, label):
    if value.strip().lower() not in {'true', 'false'}:
        raise ValueError(f'{label}: expected true or false')
    return value.strip().lower() == 'true'


def audit(target_path, matrix_path, eligibility_path, scope_path):
    targets = unique_index(read_csv(target_path, ['result_id']), 'result_id', 'targets')
    matrix = unique_index(read_csv(matrix_path, [
        'result_id','comparison_performed','comparison_eligibility_id',
        'original_value','replicated_value','absolute_difference','relative_difference',
        'raw_validation_outcome',
    ]), 'result_id', 'matrix')
    eligible = unique_index(read_csv(eligibility_path, ['comparison_eligibility_id','result_id','eligible']), 'comparison_eligibility_id', 'eligibility')
    scope = json.loads(Path(scope_path).read_text(encoding='utf-8'))
    if not isinstance(scope, dict) or set(scope) != SCOPE_GROUPS:
        raise ValueError('Scope must contain exactly primary_ids, linked_ids, other_ids and excluded_ids.')
    union = set()
    for group, ids in scope.items():
        if not isinstance(ids, list) or any(not isinstance(i, str) or not i.strip() for i in ids):
            raise ValueError(f'{group}: expected a list of nonempty target IDs')
        if len(ids) != len(set(ids)) or union.intersection(ids):
            raise ValueError('Scope has duplicate or overlapping target IDs.')
        union.update(ids)
    if union != set(targets):
        raise ValueError('Scope must partition every registered target ID exactly once.')
    if set(matrix) != set(targets):
        raise ValueError('Matrix IDs must match all registered targets, including non-compared and excluded rows.')
    for key, row in matrix.items():
        performed = boolean(row['comparison_performed'], key)
        if key in scope['excluded_ids']:
            if performed or row['raw_validation_outcome'].strip():
                raise ValueError(f'{key}: excluded row must be non-compared with blank raw outcome; record exclusion approval separately.')
            if row['absolute_difference'].strip() or row['relative_difference'].strip():
                raise ValueError(f'{key}: excluded row must not contain differences')
            continue
        outcome = row['raw_validation_outcome'].strip()
        if outcome not in COMPARED | UNCOMPARED:
            raise ValueError(f'{key}: unknown raw outcome {outcome!r}')
        if performed != (outcome in COMPARED):
            raise ValueError(f'{key}: comparison flag conflicts with raw outcome')
        if performed:
            entry = eligible.get(row['comparison_eligibility_id'])
            if entry is None or entry['result_id'] != key or not boolean(entry['eligible'], key):
                raise ValueError(f'{key}: missing, mismatched or ineligible audit reference')
            finite(row['original_value']); finite(row['replicated_value'])
            if finite(row['absolute_difference']) < 0:
                raise ValueError(f'{key}: negative absolute difference')
            if row['relative_difference'].strip():
                finite(row['relative_difference'])
        elif row['absolute_difference'].strip() or row['relative_difference'].strip():
            raise ValueError(f'{key}: non-compared rows must leave differences blank')
    raw = Counter(matrix[i]['raw_validation_outcome'].strip() for i in scope['primary_ids'])
    A = len(scope['primary_ids'])
    S, N, R = (raw[s] for s in ['strict_pass','pass_with_note','residual'])
    E = S + N + R
    assert A == E + sum(raw[s] for s in UNCOMPARED)
    def rate(numerator, denominator):
        return None if denominator == 0 else numerator / denominator
    return {
        'A': A, 'E': E, 'S': S, 'N': N, 'R': R,
        'raw_outcomes': {s: raw[s] for s in sorted(COMPARED | UNCOMPARED)},
        'direct_numerical_coverage': rate(E,A),
        'strict_numerical_pass_rate': rate(S,E),
        'conditional_agreement_rate': rate(S+N,E),
        'strict_target_attainment': rate(S,A),
        'separate_counts': {g: len(scope[g]) for g in ['linked_ids','other_ids','excluded_ids']},
        'checked': 'IDs, supplied eligibility references, state consistency and primary denominators',
        'not_checked': 'Source semantics, correctness of numerical decisions, approval authenticity, figures, family closure or report prose',
        'paper_level_assessment': 'requires reviewer assessment under SKILL.md Section 5.10',
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ['targets','matrix','eligibility','scope']:
        parser.add_argument('--'+name, required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        print(json.dumps(audit(args.targets,args.matrix,args.eligibility,args.scope), indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
