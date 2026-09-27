# Replication Skill

Replicate an applied empirical paper with an AI agent and a human reviewer. Supply the paper and any available code or data. The skill guides input auditing, code execution or reconstruction, result-by-result validation, and a full English Markdown report.

The goal is to reproduce as much of the paper's main-text and appendix evidence as the permitted inputs and methods support. Each phase leaves files that a reviewer can inspect. Missing inputs, failed attempts and unresolved differences remain visible in the final assessment.

## Contents

- [Scope](#scope)
- [Requirements](#requirements)
- [Quick start](#quick-start)
- [Inputs and code policy](#inputs-and-code-policy)
- [Workflow and human review](#workflow-and-human-review)
- [What a run produces](#what-a-run-produces)
- [How results are validated](#how-results-are-validated)
- [Handling missing inputs and unresolved methods](#handling-missing-inputs-and-unresolved-methods)
- [Resuming a run](#resuming-a-run)
- [Repository layout](#repository-layout)
- [Optional helpers and checks](#optional-helpers-and-checks)
- [Evidence and release status](#evidence-and-release-status)
- [Common questions](#common-questions)
- [Contributing](#contributing)
- [License](#license)

## Scope

Use this skill to audit a replication package, rerun an author's analysis, or reconstruct missing analytical code from a paper and usable public data. It is intended for researchers and reviewers who can assess the paper's methods and the agent's proposed decisions.

The current scope includes regression, descriptive, causal, panel and event-study analyses; randomized experiments; measurement studies; and formula, accounting, calibration and structural-estimation applications within applied empirical papers. Specialized methods have additional review requirements in [Section 14 of SKILL.md](skills/applied-empirical-replication-v3/SKILL.md#14-specialized-applied-empirical-branches).

The default target universe includes all empirical results in the main text and appendix. Exclusions and partial validation routes require an explicit record and reviewer approval. Pure theory, simulation-only and standalone quantitative-model workflows, data-unavailable reconstruction, and extension analyses are outside this version.

## Requirements

- An agent with access to local files, PDF text and page images, and a terminal. Source recovery also needs a browser or search tool.
- A paper and permission to use the supplied materials. Execution requires usable public data for the affected result families.
- A writable run directory separate from the original author package.
- A human reviewer, normally the user, who can approve the scope, methods and interpretation of the results.
- Statistical software appropriate to the paper. The agent assesses software, package versions, licenses, compute and storage before execution.

Python 3.10 or later is needed only for the bundled helper scripts, which use the standard library. There is no universal statistical dependency installation: an R reconstruction and a Stata package rerun can require different environments. Docker is optional and depends on the approved environment plan.

Codex is the first target host. Other agents need equivalent tool access and their own compatibility checks. This package contains a standalone skill folder; it does not include a plugin manifest.

## Quick start

### 1. Load the skill

Download or clone the repository and give the agent the full path to:

```text
Replication-Skill/skills/applied-empirical-replication-v3/SKILL.md
```

Ask it to read the complete file. Keep the adjacent `templates/` and `scripts/` directories available.

For repository-local Codex discovery, copy the whole `applied-empirical-replication-v3` folder into your research repository's `.agents/skills/` directory. Check for an existing copy first and preserve any local edits. See the [official Codex skill documentation](https://learn.chatgpt.com/docs/build-skills) for discovery and installation behavior.

You can also ask Codex's skill installer to install `skills/applied-empirical-replication-v3` from `ChenMQ7/Replication-Skill`. Record the commit or version you install. Detailed setup instructions are in [Getting started](docs/getting-started.md).

### 2. Point the agent to your inputs

Replace the paths in this example with your actual locations:

```text
Use the applied-empirical-replication-v3 skill.

Paper: /path/to/inputs/paper.pdf
Appendix and package: /path/to/inputs/author-package/
New run folder: /path/to/replication_runs/my-paper/

Audit and use the supplied author code under the default policy.
Include the main-text and appendix empirical results in the initial scope.
Complete Phase 0, save the intake artifacts, and stop for my CP0 review.
```

When code is absent, state that in your request. The agent records the missing-code route and proposes a reconstruction from the permitted sources.

For an explicit independent-reconstruction test, replace the code-policy sentence with:

```text
Reconstruct the analysis independently from the paper, documentation and data.
Quarantine any author scripts: inventory filenames, paths and hashes only.
Do not read, run, summarize or infer a workflow from their contents.
```

### 3. Review the intake before proceeding

The Phase 0 delivery should identify the inputs, provisional route, target scope, environment risks and open issues, with links to saved evidence. The agent should request CP0 approval and stop. Read that packet before authorizing Phase 1.

Each subsequent phase follows the same review pattern. You can approve the proposed scope, request a revision or hold specific work. See [Reviewing checkpoints](docs/reviewing-checkpoints.md) for examples.

## Inputs and code policy

The paper is mandatory. Code and data can be absent at intake; the audit establishes which results are executable.

| Available inputs or request | Handling |
| --- | --- |
| Paper, usable public code and usable public data | Route A: audit and execute author code within the permitted access boundary. |
| Paper and usable public data; code missing, not supplied or demonstrably unusable | Route B: write replacement code from the paper and approved documentation and data. |
| Explicit independent-reconstruction request, even with author scripts present | Route B with author-code quarantine from intake. |
| Partial or unavailable data | Identify affected families, investigate feasible recovery, and request usable inputs or an approved scope decision. Supported families can proceed only within their approved boundaries. |

Include appendices, README files, questionnaires and codebooks when available. Distinguish raw, intermediate and analysis-ready datasets from precomputed tables or figures. An approved analysis-ready input can support a run, with its inherited preparation disclosed. Copying a precomputed result does not count as independently generating it.

Ordinary use does not automatically quarantine author code. Missing local software also does not, by itself, make author code unusable: translation, compatibility work or a software hold may be appropriate.

## Workflow and human review

The agent performs the work and saves evidence; the reviewer authorizes decisions at CP0 through CP7. A checkpoint is the review at the end of its corresponding phase.

| Phase | Work | Evidence submitted for review |
| --- | --- | --- |
| 0. Intake and scope | Identify the paper and inputs; set the provisional route, access policy and scope. | Input manifest, scope record, inventory, software precheck, roadmap and CP0 packet. |
| 1. Paper understanding | Explain the research question, design, data and empirical claims. | Paper-content record, design map and main-text/appendix result inventory. |
| 2. Source audit | Check source roles, file integrity, variables, identifiers, sample coverage and dependencies. | Data/code audit, source ledgers, route-scope matrix and recovery decisions. |
| 3. Independent result mapping | Extract targets from the paper without using execution outputs; define comparison standards. | Target table, extraction evidence, uncertain-cell review and figure-validation contracts. |
| 4. Environment and reconstruction plan | Specify the software route, sample rules, estimators, inference, seeds and execution batches. | Environment record, reconstruction or translation design, specification audit and batch plan. |
| 5. Execution | Run approved code or implement the approved reconstruction; retain successful and failed attempts. | Scripts, commands, logs, generated outputs, model metadata and warnings. |
| 6. Validation | Establish comparability, compare individual statistics, review figures and diagnose differences. | Eligibility audit, comparison matrix, metrics, mismatch evidence and proposed follow-up. |
| 7. Reporting | Reconcile the evidence and write the complete audit and its supported conclusion. | English Markdown report, limitations, artifact index, checksums and CP7 packet. |

The workflow can return to earlier phases. A change to frozen targets needs CP3 review; a new analytical design needs CP4 review. Execution repairs produce new batches and affected validation. Earlier submitted evidence is preserved.

## What a run produces

Each paper has its own run folder. Folder numbers match phase numbers:

```text
replication_runs/my-paper/
  phase_roadmap.md
  checkpoint_record.md
  open_issue_register.md       # created when an unresolved issue arises
  00_intake/
  01_paper_understanding/
  02_source_and_artifact_audit/
  03_result_mapping/
  04_environment_plan/
  05_execution/
    build/
    logs/
    generated_outputs/
  06_validation/
  07_report/
    replication_report.md
```

The final report explains what the paper does and how the replication was carried out. It includes the approved inputs and code-access boundary, decisions made at each phase, environment and implementation details, result-family findings, numerical differences, figure evidence, unresolved issues and the final claim boundary.

Every in-scope numerical target appears in a detailed comparison table or a linked complete table, including targets that could not be compared. The report links to the saved code, logs and audits. The [report template](skills/applied-empirical-replication-v3/templates/replication_report.md) shows its full structure.

## How results are validated

Targets and validation standards are defined in Phase 3, before analytical execution. The agent first checks that a generated value represents the same quantity as the paper: definition, units, period, sample, specification and relevant inference method must be supported by the evidence.

For eligible comparisons:

- An available permitted unrounded reference uses the exact-artifact standard, with documented machine-representation tolerance where applicable.
- A value printed to `d` decimal places uses `absolute_difference < 0.5 × 10^(-d)` when paper display is the reference. Values are compared in the paper's units; the exact half-unit boundary does not pass.
- Counts require exact equality. Reported inequalities and significance markers follow their declared thresholds and inference rules.
- Stochastic results need an approved seed and variation standard. Figures use their own predeclared contracts and are reported separately from numerical pass rates.

For example, a generated mean of `0.212973378` is within the display interval for a paper value of `0.213`. It can receive a strict pass once eligibility is established. Other reported quantities, such as coefficients, standard errors and sample sizes, are assessed separately.

Raw numerical outcomes are `strict_pass`, `pass_with_note`, `residual`, `not_comparable`, `not_closed` or `blocked`. Reviewer acceptance of a limitation is recorded separately and leaves the raw outcome intact.

Coverage and agreement use different denominators. With `A` approved primary numerical targets, `E` eligible completed comparisons, `S` strict passes and `N` passes with notes:

| Metric | Calculation |
| --- | --- |
| Direct numerical coverage | `E / A` |
| Strict numerical pass rate | `S / E` |
| Conditional agreement rate | `(S + N) / E` |
| Strict target attainment | `S / A` |

Reports include the counts, unresolved outcomes, result-family closure and figure-route coverage. Zero denominators yield unavailable rates. A full-reproduction conclusion also requires complete approved coverage, closed families, strict passes for all required numerical targets and completed figure routes. A high pass rate alone cannot establish that conclusion.

The governing definitions and exceptions are in [SKILL.md, Section 5](skills/applied-empirical-replication-v3/SKILL.md#5-measurement-validation-and-claim-decision-contract).

## Handling missing inputs and unresolved methods

The agent should pursue feasible source recovery and targeted diagnostics before proposing a final limitation. For each unresolved issue, it records the affected results, evidence already checked, a concrete next action, the responsible phase and any approval needed.

A local gap should hold only the results that depend on it. An unavailable follow-up survey, for example, need not stop an independently supported baseline table. Moving that baseline work forward does not close the follow-up results or remove them from scope.

The reviewer decides whether to authorize further recovery, revise a design, supply an input or accept a bounded final outcome. Newly found inputs require an admission review before use. The skill prohibits fabricated operational details, sample selection to chase a paper value and retroactive relaxation of tolerances.

## Resuming a run

Provide the existing run folder in a new session and ask:

```text
Resume this replication run using its recorded skill version.
Read the input manifest, phase roadmap, checkpoint record and open issues.
Identify the latest approved artifacts and the next authorized action.
Explain any conflicting state before executing further work.
Preserve earlier submissions and do not infer new approval.
```

The optional initializer saves a skill snapshot and version receipt. Existing runs retain their recorded standards; applying a newer skill version requires a discussed migration.

## Repository layout

```text
Replication-Skill/
  README.md
  LICENSE
  CHANGELOG.md
  CONTRIBUTING.md
  release.json
  skills/applied-empirical-replication-v3/
    SKILL.md
    templates/
    scripts/
  docs/
  tests/
  tools/
  .github/
```

[SKILL.md](skills/applied-empirical-replication-v3/SKILL.md) is the sole normative source. Its first five sections define roles, scope, evidence, approval and validation rules; Sections 6 through 13 describe the eight phases; the remaining sections cover specialized branches, vocabulary, complete templates and maintenance. The 63 template files are synchronized operational copies.

The README explains how to begin. The supporting guides cover [setup](docs/getting-started.md), [reviewer decisions](docs/reviewing-checkpoints.md), [helpers](docs/helpers.md), [historical cases](docs/tested-cases.md) and [release acceptance](docs/release-checks.md). Research inputs and generated run folders stay outside the skill directory.

## Optional helpers and checks

The helpers create records and check mechanical consistency. They do not execute a paper's analysis, approve checkpoints or establish that a paper has been reproduced.

From the repository root, create the intended run-parent directory, then initialize a new run:

```sh
python3 skills/applied-empirical-replication-v3/scripts/init_run.py \
  "replication_runs/my-paper" \
  --paper "local_inputs/paper.pdf" \
  --title "Paper title"
```

Replace the paths with your inputs. The initializer refuses an existing destination and leaves CP0 pending. Add `--independent-reconstruction` only when the user explicitly requests that boundary.

Check template agreement and the release files:

```sh
python3 skills/applied-empirical-replication-v3/scripts/sync_templates.py
python3 tools/check_release.py
python3 -m unittest discover -s tests -v
```

`audit_run.py` checks supplied numerical ledgers for ID, eligibility-reference, state and denominator consistency. Its inputs and limits are documented in [Optional helpers](docs/helpers.md).

## Evidence and release status

The workflow developed through historical author-package and independent-reconstruction cases, including Thompson et al. (2020), Experience-Based Discrimination, Vulnerability and Clientelism, Land Rental Markets and Zero-Sum Thinking. Their coverage varies. The recent independent-reconstruction audits concluded partial replication with recorded residuals or unresolved families. See the [case-status table](docs/tested-cases.md) for counts and limitations.

Those cases used earlier instruction versions and paper-specific decisions. Full historical reports and datasets are not bundled in this repository, and the cases have not been rerun as acceptance tests of this candidate.

For the local candidate, 34 helper tests passed on macOS with Python 3.10.8 and 3.12.14. The 63 template copies match the main specification; skill-format, YAML and static package checks passed. Tests include refusal to overwrite run folders, malformed-ledger handling, scope partitions and numerical boundaries.

Fresh-agent behavioral tests, a current-version run through real CP0 to CP7 decisions, cross-machine checks and GitHub CI execution remain pending. See [release checks](docs/release-checks.md) and [release.json](release.json) for the acceptance boundary. Complete replication of an arbitrary paper is not guaranteed.

## Common questions

### Do I need author code?

No. With usable data, the skill can guide code reconstruction from permitted sources. The reviewer approves the design in Phase 4 before implementation in Phase 5. Missing methodological details must be resolved or retained as explicit limitations.

### What if Stata or another required program is unavailable?

The agent assesses a translated route, compatibility work or a software hold and submits the implications for approval. Availability alone does not justify changing estimators or claiming equivalence between implementations.

### Can I leave the entire replication unattended?

The workflow requires human decisions at eight checkpoints. The reviewer approves scope, analytical choices and the final assessment. Runtime and cost depend on the paper and are assessed during intake and planning.

### Does approving the final report mean the paper passed?

CP7 approval accepts the report at its stated assessment. That assessment can be full reproduction within approved scope, reproduction with documented residuals, partial replication or diagnostic validation only.

### Can I upload a run folder to GitHub?

Review permissions and contents separately before sharing. Run folders may contain restricted data, paths, credentials or author materials. The repository's MIT License covers this project's files; it does not grant redistribution rights to external research inputs. Also check your agent provider's data-handling settings before supplying sensitive files.

## Contributing

Report issues with the skill version, affected phase, expected behavior, observed behavior and the smallest shareable evidence. Keep credentials, private data and quarantined author code out of issues and pull requests.

For workflow changes, update the canonical specification first, synchronize affected templates and run the checks. Explain the motivating case and any effect on existing runs. Documentation, comments and contribution messages should be in English. See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

The project is available under the [MIT License](LICENSE). Papers, author packages and third-party data retain their own terms. This repository does not redistribute those materials.
