# Release checks

The current candidate is `0.1.0-beta.1`. Local preparation does not publish a GitHub release. `release.json` records the candidate state and unresolved acceptance checks.

## Automated checks

From a clean checkout:

```sh
python3 tools/check_release.py
python3 -m unittest discover -s tests -v
```

The repository check covers metadata, embedded-template agreement, local Markdown links and anchors, packaging paths, English prose and common accidental secret patterns. It checks the limited frontmatter format used by this project; it is not a general YAML validator or a complete secret scanner.

The tests exercise helper behavior, including directory preservation, explicit reconstruction restrictions, template drift, malformed ledgers, duplicate target IDs, eligibility references, scope partitions, zero denominators and decimal-boundary cases. Fixture values are unit-test inputs, with no claim to represent a published paper.

The GitHub Actions workflow runs these checks on the configured Python versions. Until the repository is pushed and a workflow run succeeds, CI execution remains unverified. Local checks do not establish a fresh statistical-environment restore or cross-platform support.

## Independent acceptance tests

These tests remain pending for this release. Give a new agent session only the candidate package, the relevant request and permitted input files. Keep expected outcomes with the evaluator. Use separate scratch folders and preserve the candidate version and outputs. Never provide an invented reviewer approval.

| Test | Evidence required for acceptance |
| --- | --- |
| Installation | The intended host discovers or explicitly loads the complete skill folder. Record host/version and invocation. |
| Default code policy | A paper/code/data request reaches CP0 with the normal author-code route and no unsolicited quarantine. No analytical execution occurs. |
| Independent reconstruction | An explicit request applies quarantine before content inspection; the trace contains metadata-only author-code handling. |
| Missing input | The packet identifies affected results and feasible source-recovery actions; it does not fabricate data or silently delete targets. |
| Resume | A fresh session identifies the current approved packet and next action from saved governance, preserving historical pending packets. |
| Report review | A mixed-result fixture retains residuals, separate denominators and pending figure decisions. Generic CP7 approval does not grant per-figure acceptance. |
| End-to-end use | One manageable, licensed paper case passes through real CP0 to CP7 decisions, with all required artifacts and an evidence-supported final assessment. Numerical mismatches remain reportable outcomes. |

Use a small existing public case for end-to-end acceptance after the reviewer chooses it. Prior research runs are historical evidence, not a substitute for this test. Do not begin a new paper run merely to fill the release checklist.

## Before publication

Review the English documents and public file list. Confirm the license, absence of restricted materials, actual installation instructions and test results. Remove private paths from any later evidence excerpts. Keep the release candidate's remaining limits visible.

After approval, publish the reviewed files, run CI and create a versioned release. Record the commit and skill hash. Installation of a new release does not migrate an existing paper run automatically.
