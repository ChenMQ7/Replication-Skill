---
name: applied-empirical-replication-v3
description: Conduct auditable applied-empirical paper replications, replication-package audits, and independent code reconstruction from available data. Use when a user requests replication, validation, or a full replication report, with human checkpoints and retained evidence.
license: MIT
metadata:
  revision: "0.1.0-beta.1"
  source_revision: "2026-09-27-source-semantics-and-diagnostic-boundaries"
---

# Applied Empirical Replication Skill

This document is the complete normative workflow specification for version 3. It contains the route rules, Phase 0–7 procedures, checkpoints, validation contract, controlled vocabulary, and artifact schemas needed to run the skill. The files in `templates/` are operational starters copied into a run folder; they reduce transcription errors but never add or override policy. If a template and this document conflict, stop and correct the template before use.

## Contents

- [1. Identity and roles](#1-skill-identity-intended-users-and-roles)
- [2. Replication contract](#2-replication-contract)
- [3. Run folders and evidence](#3-run-folder-evidence-system-and-artifact-lifecycle)
- [4. Checkpoint governance](#4-checkpoint-governance)
- [5. Validation and claim decisions](#5-measurement-validation-and-claim-decision-contract)
- [6. Phase 0: Intake](#6-phase-0--intake-and-scope)
- [7. Phase 1: Paper understanding](#7-phase-1--paper-and-design-understanding)
- [8. Phase 2: Source audit](#8-phase-2--source-code-data-and-route-audit)
- [9. Phase 3: Independent targets](#9-phase-3--independent-result-mapping)
- [10. Phase 4: Environment and design](#10-phase-4--environment-and-reconstruction-plan)
- [11. Phase 5: Execution](#11-phase-5--execution-reconstruction-and-targeted-batches)
- [12. Phase 6: Validation](#12-phase-6--output-mapping-validation-and-mismatch-audit)
- [13. Phase 7: Reporting](#13-phase-7--full-audit-report-reconciliation-and-delivery)
- [14. Specialized branches](#14-specialized-applied-empirical-branches)
- [15. Vocabulary](#15-controlled-vocabulary)
- [16. Templates](#16-canonical-template-library)
- [17. Use and maintenance](#17-operational-use-and-maintenance)

## 1. Skill Identity, Intended Users, and Roles

### 1.1 Purpose

Use this skill to conduct an auditable applied-empirical replication. Pursue the most complete reproduction of the approved empirical target universe that permitted evidence and methods can support, and determine which reported results can be regenerated or independently reconstructed. Recover usable inputs and resolve operational gaps where feasible; completing phases or documenting limitations alone does not satisfy this objective. Completeness never authorizes fabricated inputs, unsupported analytical choices, target-driven tuning, or violations of the approved access and checkpoint boundaries.

The required deliverable is an evidence package containing paper understanding, source and input boundaries, independent paper targets, environment and execution records, validation results, mismatch analysis, reviewer decisions, and a complete English Markdown report.

### 1.2 Current paper boundary

The skill currently covers applied empirical research only, including:

1. regression, descriptive, causal, panel, and event-study papers;
2. randomized experiments and encouragement designs;
3. measurement, correlation, and administrative-data studies;
4. formula, accounting, calibration, and delta-method result families used in applied empirical papers; and
5. structural-estimation applications, subject to the hard-stop rule in Section 14.

Pure theory, formal-model, simulation-only, and quantitative-model workflows are not currently included in this scope. The skill prohibits the fabrication of missing operational details and does not present copied outputs as newly generated evidence.

### 1.3 When to trigger this skill

Trigger the skill when the user supplies or identifies a paper and asks for a replication, reproduction, audit, independent reconstruction, validation of a replication package, or a complete replication report.

A paper is mandatory. Code, data, appendices, README files, survey instruments, pre-existing output files, and package documentation are optional inputs. Their presence does not by itself authorize their use.

### 1.4 Roles

The operator is the agent executing the workflow. The operator must follow the approved route, save actual evidence, stop at each checkpoint, and never silently broaden scope.

The reviewer is the person who approves or returns each checkpoint. Unless the user designates someone else, the user is the reviewer. A reviewer may approve a narrower scope, an alternative software route, a reconstruction design, an accepted caveat, or a final claim boundary. A reviewer cannot retroactively turn an unexecuted or ineligible result into a raw pass.

### 1.5 Hard role boundaries

The operator must:

1. retain named artifacts in the run folder;
2. identify uncertainties rather than resolve them silently;
3. wait for explicit reviewer approval at CP0 through CP7;
4. preserve original package materials; and
5. use the final report only to summarize evidence already retained.

The reviewer must:

1. approve scope and exclusions;
2. approve any route that departs from the original software or requires replacement code;
3. approve the pre-execution validation contract;
4. decide whether unresolved items justify a return loop or a final limitation; and
5. approve the final report wording and delivery.

### 1.6 Prohibited claims

Never state that a paper has been fully reproduced when a result family is blocked, open, diagnostic only, or outside the approved evidence boundary. Never call a translated or independently reconstructed route an official author-code rerun. Never use a human-approved caveat to overwrite the raw comparison status.

## 2. Replication Contract

### 2.1 Inputs

At intake, declare every supplied or discovered item:

1. paper PDF and bibliographic source;
2. appendix, online appendix, README, and instructions;
3. author code, its presence and assessed usability, and whether inspection and execution are permitted;
4. raw, intermediate, analysis-ready, and output data;
5. external data sources and credentials;
6. software, operating-system, hardware, and rendering requirements; and
7. pre-existing tables, figures, or paper-build artifacts.

### 2.2 Default target universe

The default target universe is all empirical results in the main text and appendix. This includes numerical tables, reported estimates, descriptive quantities, fit statistics, tests, and empirical figures where a validation route exists.

Every exclusion, blocked family, partial route, precomputed artifact, manual-design item, pattern-only route, or backing-data route must be recorded at Phase 0 or Phase 3 and approved by the reviewer. Difficult appendices may not be silently omitted.

### 2.3 Supported intake routes and code policy

This version supports exactly two primary routes:

```text
Route A — paper + usable public code + usable public data
Route B — paper + usable public data + independent code reconstruction
```

By default, if supplied code passes the permitted usability audit, use Route A: inspect, document, and execute it subject to license and safety constraints. Do not propose or require an independent-reconstruction test unless the user requests one. If code is missing, not provided, or fails the documented usability criteria, use Route B and write replacement code from the paper, approved documentation, and approved data.

An explicit user request for independent reconstruction also selects Route B, even when author code is present. Apply that restriction immediately at intake, record the request and code-access boundary, and submit them for CP0 approval. Existing author code is then `quarantined`: only its filename, path, and hash may be inventoried. Do not open, read, run, summarize, or infer the analytical workflow from its contents, including through helper tools or other agents. Paper text, appendices, README instructions, codebooks, and data remain subject to their separately recorded permissions; permission to read documentation does not permit inspecting embedded author-code content. Quarantine must not be lifted to solve an implementation problem without an explicit reviewer decision and a recorded change to the claim boundary.

Record code state separately from access policy (`permitted` or `quarantined`), with read, execute, and summarize permissions recorded explicitly. Code states are `usable`, `missing`, `unusable`, `not_provided`, and `present_unassessed`. Use `present_unassessed` when code exists but its contents have not been inspected; quarantine is not evidence that code is missing or unusable. “Unusable” requires a recorded reason such as unreadable or corrupt files, no executable analytical content, irrecoverable dependencies, or a legal/technical execution barrier. Software unavailability alone normally triggers a translated or blocked Route A subroute, not automatic reclassification as missing code. Record any prior author-code exposure and its effect on the independence claim.

### 2.4 Data sufficiency boundary

A data file is not an eligible input merely because it exists. It must have a recorded source role, pass applicable integrity checks, be approved for execution, and be used in an executed batch before it can support a replication claim.

Both supported routes require usable public data for the approved result families. If that requirement fails, stop the affected family, classify it as blocked or not closed, and request usable data or an approved scope reduction. Data-unavailable reconstruction is outside this version.

### 2.5 Required outputs

Every run produces:

1. a paper-specific run folder under the approved replication-runs location;
2. a completed phase roadmap and checkpoint record;
3. independent paper targets and a target-to-output map;
4. source, environment, execution, and validation evidence;
5. a mismatch and caveat record where needed; and
6. a full English Markdown replication audit report.

## 3. Run Folder, Evidence System, and Artifact Lifecycle

### 3.1 Canonical directory map

Create the following structure before substantive work:

```text
replication_runs/<paper_slug>/
  phase_roadmap.md
  checkpoint_record.md
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
```

The numeric directory and phase number always match. Historical runs with other layouts remain historical evidence and are never retroactively reorganized.

### 3.2 Evidence-retention contract

Every phase ends with saved evidence before its checkpoint:

| Phase | Minimum retained evidence |
| --- | --- |
| 0 | manifest, scope record, artifact inventory, integrity precheck, environment precheck, code-access decision, roadmap, checkpoint record |
| 1 | paper-content record, design map, claims inventory, target-universe register |
| 2 | code/data audit, data inventory, integrity ledger, dependency graph, route-scope matrix, identifier and session audit |
| 3 | target table, extraction record, table schemas, manual-review decisions, result map, dependency graph, figure contract |
| 4 | environment decision, version or lock evidence, dependency triage, route contract, reconstruction design, specification audit, crosswalks, batch plan |
| 5 | scripts, command manifest, successful and failed logs, output manifest, model metadata, warning ledger, seed record, late-input re-audit events, targeted fixes, figure backing artifacts |
| 6 | output-to-paper map, eligibility audit, comparison matrix, validation summary, mismatch audit, accepted caveats, figure evidence, review decisions |
| 7 | full report, limitations, reconciliation, delivery manifest, checksums, and final checkpoint record |

Conversation, terminal summaries, and unstored intermediate objects never substitute for evidence.

Maintain one run-level `open_issue_register.md`, created when the first unresolved issue is found and updated through closure. Phase-specific audits retain the detailed evidence; the register links to them and makes the next action and approval boundary visible. Do not create competing current issue lists in each phase.

### 3.3 Artifact ownership and lifecycle

Each artifact has one canonical path:

1. 00_intake/artifact_inventory.csv is created in Phase 0 and updated append-only throughout the run. Do not create a second canonical inventory in Phase 2.
2. 04_environment_plan/batch_plan.csv is a pre-execution plan. Actual executions are recorded only in 05_execution/logs/command_manifest.csv.
3. 05_execution/generated_outputs/reproduced_output_long.csv is generated in Phase 5. Phase 6 reads and maps it; it does not create a second copy.
4. 06_validation/comparison_matrix.csv is the immutable raw numerical record after validation. Reviewer disposition is recorded separately in accepted_caveats.csv.
5. A targeted return loop creates a dated new batch and new generated artifacts; it does not erase a prior failed batch.

An approved validation-only return creates a new dated validation version without requiring new empirical execution. Preserve earlier matrices, reports, user edits, and submission-time hashes. Identify the current approved version in run governance; never overwrite a frozen matrix to implement a later correction.

Before replacing a file already cited as evidence or inventoried with a checksum, preserve the referenced bytes and identify the successor version. Record finalized artifacts after their bytes are stable; a hash alone cannot recover an overwritten version. If historical bytes cannot be recovered, retain the old hash, identify and verify any successor, and disclose the retention gap without claiming historical integrity was verified. This does not require archiving every uncited working draft.

### 3.4 Original package preservation

Before a route can write into a supplied package, create a copied working package or record baseline hashes of overwrite-prone directories. The final report must state:

```text
original_package_modified
working_copy_modified
modifications_logged
```

### 3.5 Integrity and provenance

For material inputs, record actual path or URL, retrieval date, expected and observed file type, parse result, relevant schema check, checksum where practical, source role, approval state, and first batch that used the input.

## 4. Checkpoint Governance

### 4.1 Hard gates

The workflow has CP0 through CP7. At each checkpoint the operator must:

1. summarize completed work from saved artifacts;
2. list artifact paths reviewed;
3. show key outputs and quality evidence;
4. list unresolved issues, assumptions, and closure requirements;
5. request an explicit reviewer decision; and
6. stop until a decision is recorded.

Only `approved` authorizes the next phase. `pending`, `revise`, `blocked`, silence, elapsed time, or an operator’s own judgment do not constitute approval. A run requested as “autonomous” still records the user as reviewer unless another reviewer is named; the user may pre-authorize bounded decisions in writing, but the operator may not infer blanket approval.

### 4.2 Checkpoint decisions

| Checkpoint | Required approval |
| --- | --- |
| CP0 | paper, inputs, scope, roadmap, code boundary, and provisional route |
| CP1 | paper understanding, empirical design, claims inventory, and target universe |
| CP2 | source and data sufficiency, route feasibility, restrictions, and audit boundary |
| CP3 | independent targets, extraction review, figure contract, and validation standards |
| CP4 | environment, software route, reconstruction design, assumptions, seed policy, and batches |
| CP5 | execution logs, generated outputs, warnings, failures, and narrow follow-up |
| CP6 | validation, mismatch triage, reviewer disposition, and any return loop |
| CP7 | report wording, reconciliation, limitations, package, and delivery |

### 4.3 Checkpoint record requirements

Every CP entry must state:

```text
checkpoint
date
reviewer
phase goal
completed work
artifact paths reviewed
key outputs
unresolved issues
evidence retained after checkpoint
reviewer decision
approval wording
required changes
next authorized action
```

After a decision, append its exact wording and synchronize the current manifest and roadmap. Preserve submitted packets and their historical status labels; snapshot hash-covered governance before updating it. A historical `pending` label is resolved by the later approval event, not by rewriting submitted evidence.

### 4.4 Return-loop rule

If validation exposes a target-extraction problem, return to Phase 3. If it exposes an environment or route issue, return to Phase 4. If it exposes an implementation issue, return to Phase 5. If a material execution input becomes newly usable after CP4, return first to Phase 2 for an audit amendment and then to Phase 4 for a plan amendment before authorizing a new batch. Save the reason, approved scope, new batch identifier, and resulting evidence. Do not silently replace an earlier result.

If the issue is an incorrect comparison-eligibility decision and existing approved sources and outputs suffice, request a bounded Phase 6 re-review under Section 12.4. This does not authorize new fits, samples, target edits, source recovery, or changes to the numerical standard. Stop at a new CP6 decision before revising the Phase 7 report.

### 4.5 Unresolved issues, recovery, and permission to proceed

At every checkpoint with unresolved issues, explain **what is unresolved, what it affects, what can be done, when it must be done, and what the reviewer is being asked to approve**. A raw result status does not answer these workflow questions.

For each material issue, record a stable issue ID; evidence and checks already completed; affected inputs, targets and downstream dependencies; proposed recovery action or the specific information still needed; responsible phase and operator/reviewer; the first dependent action that must wait; required approval and actual decision; and observable closure evidence. Before numerical target IDs exist, identify the affected families and refine the scope at Phase 3. Distinguish a supported solution ready to implement, a testable but unverified recovery proposal, and an external prerequisite for which no usable source has been found. Do not promise that a proposal will resolve the issue.

Use one of the following workflow dispositions, separately from raw validation outcomes:

| Disposition | Meaning and permission boundary |
| --- | --- |
| Resolve before dependent work | Identify the affected next action and do not execute it until the required evidence/design and approval exist. Unaffected approved work may continue. |
| Carry to a named later phase | The later phase is responsible for this task by design; name its action, expected artifact and completion gate. Include the carry-forward in the current CP decision. Approval to advance does not approve an unresolved analytical choice. |
| Hold the affected route; continue others | The dependency cannot currently be satisfied. Keep its targets in scope, state the recovery trigger and obtain approval for the partial progression. Do not propagate a local hold to unrelated targets. |
| Retain in the final report | Following documented recovery review, the reviewer chooses reporting with the limitation. Preserve the raw outcome and explain what could reopen the issue; do not claim that all feasible work is impossible or exhausted. |

Use the earliest relevant phase and checkpoint, not a generic promise to fix everything in the next phase:

Before the relevant initial checkpoint, include the issue in that normal phase submission. An amendment is required when changing an already approved source, target or design boundary; the table does not require duplicate approvals for work already covered by the current phase or batch.

| Issue | Responsible work and gate |
| --- | --- |
| Phase 1 question about units, questionnaire meaning, keys or input coverage | Carry to Phase 2 source audit under CP1 approval; provide source evidence at CP2. An operational choice still unresolved at that point must be held or explicitly proposed for CP4. |
| Target transcription, unit annotation or source-display conflict | Phase 3 review; later changes to frozen target metadata or values require a scoped CP3 amendment. Preserve both source displays while a conflict is unresolved. |
| New or newly usable execution input, or changed input-admission boundary | Phase 2 admission audit and CP2 amendment, then Phase 4 plan/CP4 amendment before use. Newly reading a permitted document without changing the input boundary does not by itself require re-admitting all data. |
| Sample rule, transformation, estimator or inference procedure not yet specified | Phase 4 design and CP4 approval before dependent execution. A method name alone does not supply an executable specification. |
| Implementation, required export or render omission within the approved design | Phase 5 bounded repair, authorized in the current batch or by a scoped return; CP5 review and affected Phase 6 validation follow. Any changed analytical rule first requires CP4. |
| Comparison-eligibility mistake using sufficient existing evidence | Approved Phase 6-only re-review under Section 12.4; no new estimates or target edits; stop at a new CP6 decision. |
| Eligible numerical residual, unresolved external prerequisite or pending human figure decision | Phase 6 documents the evidence and offers a scoped recovery/review action or a retained limitation for CP6. Phase 7 reports the decision; it does not implement a missing estimator, obtain missing data or grant human acceptance. |

Before recommending advancement from any phase with material gaps, first identify concrete recovery actions within that phase's responsibility. Complete feasible checks already covered by the current approval unless the reviewer explicitly defers them. Where additional authority is needed, submit a bounded recovery proposal with permitted sources, concrete checks, affected targets, expected artifacts and a stopping condition; obtain the required amendment before acting. Do not make acceptance of the current inputs or limitations the default recommendation merely because unaffected work can proceed or many results have been generated.

Recommend carrying an issue forward only after recording the current-phase checks and why the remaining work belongs in a named later phase, requires a presently unavailable external prerequisite, or has been explicitly deferred by the reviewer. Name the first dependent action that must wait and the evidence needed to reopen or close the issue. Source availability, source identity and recoverable field semantics belong to Phase 2; target transcription belongs to Phase 3; operational estimator and transformation design belongs to Phase 4. Do not postpone a feasible source check by relabeling it as a later design task. Conversely, do not execute a later phase's estimation or reconstruction early in the name of completeness. Unaffected approved work may continue, but moving to another phase still requires its checkpoint approval.

After a recovery attempt, update the same issue with what was checked, what was learned and which targets remain affected. A negative search in one catalogue is not proof of absence from all raw files or questionnaires. Revisit a hold when new evidence or a concrete untested linkage becomes available; do not repeat the same unchanged search indefinitely. There is no fixed number of recovery rounds. Each approval request must state whether it authorizes a source check, design amendment, execution batch, validation review or reporting only. Every CP0–CP7 stop remains in force.

## 5. Measurement, Validation, and Claim-Decision Contract

### 5.1 Analytical units

A statistic target is one reported quantity, such as a coefficient, standard error, confidence-interval endpoint, sample size, p-value, fit statistic, or summary value.

A result target is the paper row, model column, panel cell, or equivalent reported result composed of one or more statistic targets.

A result family is a coherent table, figure, regression family, event-study family, calibration family, or other paper claim unit.

### 5.2 Comparison-eligibility gate

Before any numerical difference is computed, verify that the paper target and reproduced output share:

1. outcome definition;
2. input or treatment definition;
3. start and end period;
4. frequency;
5. transformation and units;
6. sample and aggregation;
7. weights, controls, fixed effects, and clustering where relevant; and
8. covariance route for inference statistics where relevant.

If a required element differs or remains unresolved, name that element, the supporting source evidence, the affected statistic IDs, and what would resolve it. Set comparison_performed to false, leave differences blank, and assign the applicable Section 5.7 state. A numerical match alone does not establish eligibility; a numerical mismatch alone does not invalidate an otherwise supported comparison.

Apply this gate within the approved input boundary. When an analysis-ready file is approved as an input, undisclosed upstream cleaning or the existence of another diagnostic sample does not by itself disqualify its documented baseline use. Establish the target's definition and sample from permitted evidence; disclose inherited preparation separately. Retain a hold where a material target-specific requirement is genuinely unsupported or conflicts with the input. Do not assume that all prepared fields are eligible, or require full raw-to-analysis reconstruction when that is outside scope.

Assess each hold at the narrowest justified dependency scope. Test whether a disputed filter actually changes the required row identities; equal counts alone are insufficient, and a redundant filter does not resolve a separate outcome-definition conflict. Once the target's sample rule is established, a differing reported N is a numerical residual, not grounds by itself to suppress comparison. Never choose a sample because its count or estimate is closer to the paper.

### 5.3 Pre-execution validation standard

Every statistic target must receive a validation standard in Phase 3 before execution. Phase 6 cannot loosen a standard after seeing a result.

The priority order is:

1. exact-artifact comparison when a permitted, auditable, unrounded reference output exists;
2. display-precision comparison when the paper is the only available numerical target;
3. an explicitly reviewer-approved, target-specific standard for stochastic or nonstandard outputs; or
4. no comparison claim when none of the above is possible.

### 5.4 Exact-artifact standard

When a permitted unrounded reference output is available, compare parsed numerical values under the documented parser and numeric representation. Integers and counts require exact equality. Floating values require equality up to documented machine representation tolerance. The tolerance must be stated in the target table and may not be used to hide a substantive difference.

An author precomputed table may be a reference artifact in an allowed author-code route. It is never independent regenerated output in an independent-reconstruction route.

### 5.5 Display-precision standard

For a value x printed to d decimal places, a reproduced value r meets the display-precision standard if:

```text
absolute_difference < 0.5 × 10^(-d)
```

Apply the rule in the paper's displayed units. Normalize percentages, logged quantities, ratios, and exponentiated quantities before comparison. Record the paper display string, display precision, unit transformation, and interval in the target table.

For a reported inequality such as p < 0.01, the reproduced p-value must satisfy the same inequality. For a reported significance marker, assess the marker against the paper-declared alpha, sidedness, and adjustment rule where those are recoverable.

### 5.6 Statistic-specific defaults

| Statistic | Default standard |
| --- | --- |
| coefficient, marginal effect, mean, share, ratio, elasticity | exact-artifact where available, otherwise display-precision |
| standard error, confidence-interval endpoint, t, z, F, chi-square, fit statistic | exact-artifact where available, otherwise display-precision |
| observation count, cluster count, event count, categorical result | exact equality |
| p-value or significance marker | reported precision or reported threshold, plus paper-declared inference rule |
| sample definition | eligibility audit plus exact count where reported |
| joint test | test-statistic and p-value standard separately |
| figure | predeclared figure-validation route; never included in numerical pass rate |
| stochastic estimator, randomization inference, or bootstrap output | approved seed and repeated-run standard, with run-scale and variation evidence |

Coefficient, standard error, sample size, fit statistic, and joint test are evaluated separately. A successful coefficient does not close a result whose required inference or sample component is unresolved.

### 5.7 Raw validation outcomes

Use only these raw outcomes in comparison_matrix.csv:

```text
strict_pass
pass_with_note
residual
not_comparable
not_closed
blocked
```

strict_pass means the predeclared standard and eligibility gate both passed.

pass_with_note means the numerical standard passed but a documented issue remains. It is shown separately and never enters the strict-pass numerator.

residual means an eligible comparison was performed but did not meet the standard.

not_comparable means the estimand match was not established.

not_closed means required evidence, operational detail, or output is missing.

blocked means an access, data, or other external condition prevents the required work.

For non-compared targets, record output availability separately from comparability. Use `blocked` when an identified external prerequisite prevents the work; otherwise use `not_closed` when the matching output or required operational procedure has not been completed, and `not_comparable` when an available mapped output cannot be established as the same statistic. Preserve overlapping reasons in the closure requirement, but assign one raw state per target. A diagnostic substitute does not make a missing required output available.

### 5.8 Route labels and result closure

Route labels describe how evidence was produced, for example:

```text
official_same_software_rerun
patched_author_script_route
translated_replication
translated_regression_reconstruction
summary_stat_reconstruction
formula_reconstruction
delta_method_inference_reconstruction
precomputed_output_validation
backing_data_validation
event_study_pattern_validation
manual_design_figure_validation
structural_input_data_audit
structural_internal_consistency_validation
supplemental_output_calibration
partial_coverage
blocked_restricted_data
documentation_only_validation
```

Result-target closure states are:

```text
fully_closed
closed_with_note
open
blocked
out_of_scope
diagnostic_only
```

Route labels and closure states are not pass labels.

### 5.9 Quality metrics

Let A be all approved in-scope direct numerical statistic targets. Let E be the subset with completed eligibility audits and direct numerical comparisons. Let S be strict_pass targets, N be pass_with_note targets, and R be residual targets.

```text
direct_numerical_coverage = E / A
strict_numerical_pass_rate = S / E
conditional_agreement_rate = (S + N) / E
strict_target_attainment = S / A
```

Report A, E, S, N, R, not_comparable, not_closed, blocked, and out_of_scope counts explicitly. Do not silently remove difficult targets from A.

Check E = S + N + R and A = E + not_comparable + not_closed + blocked. E is a subtotal, not another disjoint outcome. Approved out-of-scope items are reported separately. A zero denominator yields an unavailable rate, not a zero or perfect score. Duplicated prose displays, categorical checks, diagnostic variants, and unrequested exports never create additional primary numerical credit; retain linked displays and inference statements separately where relevant.

Also report:

1. result-target full-closure rate: fully closed result targets divided by approved result targets;
2. result-family coverage: approved result families with a completed declared route divided by all approved result families; and
3. figure-route coverage: figures with completed declared validation routes divided by all in-scope figures.

Use the granularity frozen in Phase 3. If result IDs were defined only at family level, disclose that result-entry and family closure coincide; do not invent a finer denominator in Phase 7. An open family can contain eligible passing statistics. A high conditional pass rate does not establish broad coverage or a probability that the paper is correct.

### 5.10 Paper-level logic gate

The report may state fully reproduced within approved scope only when all of the following hold:

1. every approved result family is fully closed;
2. every approved direct numerical target is covered;
3. every required statistic target is strict_pass;
4. no residual, not_closed, blocked, or non-comparable item remains in approved scope; and
5. every in-scope figure has completed its declared validation route.

If scope is substantially covered but residuals, notes, or open items remain, use reproduced with documented residuals. If only some approved families close, use partial replication. If the evidence audits inputs, patterns, or intermediate artifacts without closing paper results, use diagnostic validation only. A percentage alone never authorizes a full-reproduction claim.

### 5.11 Caveats and reporting disposition

Reviewer acceptance of a caveat is recorded separately from raw outcome. An accepted caveat must include paper and reproduced values, difference, likely reason, evidence path, why it does not change the stated claim boundary, reviewer approval, and final-report wording.

Permission to report a partial outcome is not a target-specific numerical exception or figure acceptance. Record general reporting permission in the checkpoint record; create accepted-caveat entries only for decisions actually made, without altering raw outcomes.

## 6. Phase 0 — Intake and Scope

### 6.1 Purpose and entry boundary

Phase 0 establishes what exists, what may be used, what is excluded, and what requires later audit. Do not deeply inspect code, write reconstruction code, execute analysis, or extract final targets before CP0.

### 6.2 Required actions

1. create the paper-specific run folder;
2. record citation, DOI or stable source, paper edition, and supplied paths;
3. inventory code, data, documentation, archives, output files, and likely external dependencies;
4. classify the run as Route A or Route B, record the code state and access policy, and apply any explicit independent-reconstruction restriction before content inspection;
5. record initial data availability and likely sufficiency risks;
6. precheck expected languages, proprietary software, build tools, credentials, data volume, and rendering needs;
7. create a paper-specific roadmap and checkpoint record; and
8. state provisional scope and route without claiming feasibility.

Code is provisionally usable only when permitted evidence establishes that it is readable, contains relevant analytical content, has an identifiable entry point or recoverable execution order, and can legally and technically be inspected. Do not inspect quarantined code to establish usability; record `present_unassessed` when no permitted usability assessment exists. Data are provisionally usable only when they are publicly accessible or supplied with permission, parseable, attributable to a source, and plausibly cover at least one approved result family. Final feasibility is decided at CP2.

### 6.3 Required Phase 0 artifacts

```text
00_intake/input_manifest.yml
00_intake/scope_confirmation.md
00_intake/artifact_inventory.csv
00_intake/environment_requirements_precheck.md
00_intake/code_access_decision.md
00_intake/route_decision.md
phase_roadmap.md
checkpoint_record.md
```

### 6.4 CP0 packet

Show the manifest, scope confirmation, inventory, environment precheck, code-access decision, Route A/B decision, roadmap, and checkpoint record. Explain input availability, initial exclusions, expected software, data risks, and provisional route. CP0 approval authorizes Phase 1 only.

## 7. Phase 1 — Paper and Design Understanding

### 7.1 Purpose

Read the paper and approved supporting documents sufficiently to explain its research question, empirical setting, data or model, estimands, claims, and result universe. Do not infer details not supported by the paper or approved documentation.

### 7.2 Paper-type classification

Classify the closest branch:

```text
applied_empirical_regression
randomized_experiment_or_encouragement_design
measurement_validation_or_correlation
precomputed_artifact_or_manual_design_item
```

For randomized studies, record assignment, compliance, ITT, IV or LATE logic, sample flow, treatment arms, attrition, and outcome families.

### 7.3 Required records

```text
01_paper_understanding/paper_content_for_final_report.md
01_paper_understanding/empirical_design_map.yml
01_paper_understanding/claims_inventory.csv
01_paper_understanding/target_universe_register.csv
```

The paper-content record explains question, contribution, design or model, units, data sources, variables or parameters, main findings, interpretation limits, and scope. The design map records treatment or input, outcomes, controls, fixed effects, clustering, weights, sample rules, periods, identification strategy, and unresolved details.

### 7.4 Target-universe register

List every main-text and appendix empirical result family. Distinguish empirical results from narrative, theory, conceptual diagrams, and manual-design figures. State each family’s role in the paper claim and any preliminary uncertainty.

### 7.5 CP1 packet

Show paper-content record, design map, claims inventory, source documents used, paper-type decision, target-universe register, and open questions. CP1 approval authorizes Phase 2 only.

## 8. Phase 2 — Source, Code, Data, and Route Audit

### 8.1 Purpose

Determine which approved inputs can genuinely support which result families. Separate files that merely exist from files that passed integrity checks, were approved for execution, and were used in completed batches.

### 8.2 Usable-code audit

For readable author code whose inspection is permitted, identify master scripts, helper scripts, output-producing scripts, dependencies, execution order, hard-coded paths, random-seed behavior, manual steps, outputs, and overwrite risks. Build an execution dependency graph. Do not assume that a paper-build script regenerates all paper exhibits. Skip this content audit for quarantined code and retain only the metadata allowed by Section 2.3.

### 8.3 Reconstruction-route input audit

For Route B, record why code is missing, not provided, or unusable, or cite the explicit independent-reconstruction request and quarantine boundary. Record any permitted recovery attempts and the approved documentation describing the intended analysis; a quarantine instruction does not authorize code recovery or content inspection. Build any reconstruction dependency graph from those permitted sources and data, not from quarantined code. Do not treat precomputed outputs, result-like workbooks, cached estimates, or derived author artifacts as replacement source data. Phase 2 determines which result families have sufficiently documented specifications and usable public data to enter reconstruction planning.

### 8.4 Data and source audit

Inventory raw, intermediate, analysis-ready, summary, figure, formula, structural, precomputed, and supplemental artifacts. Record whether an analysis file is an explicit analysis-data input, a derived artifact, or an output. Identify external URLs, restricted sources, credentials, expected schemas, and coverage requirements.

For every candidate execution input, test parseability, schema, units, row grain, keys, time and population coverage, missingness, duplicates, labels or codebooks, provenance, license, and consistency with the paper’s description. A filename or README assertion does not establish usability.

Resolve field semantics from permitted labels, questionnaires, periods and construction evidence, not variable-name similarity or paper-matching counts. Distinguish self-reported measures from composites, assignment from receipt and behavior, and questionnaire respondent/manager roles. Trace ambiguous categorical codes to their question and response dictionary; a code defined for another question is not automatically transferable. Retain a local hold when the semantic crosswalk is missing, even if either coding direction would produce plausible groups.

A correct dataset release does not establish coverage for every analysis. Check question availability and valid-response intersections by wave, population and module; distinguish nonresponse or special codes from substantive values. A question appearing in an instrument does not prove its field is in the released extract. Analyses of attrition or linked relatives require identifiable eligible units and links, not only aggregate counts or a similarly named proxy. Keep source editions separate: a matching count in another edition supports a version hypothesis, not a new exclusion rule or replacement of frozen paper targets.

For historical or geographic recovery, distinguish source-count reconstruction from boundary harmonization and respondent linkage. Record the dated geographic units, verified code changes, allocation assumptions, coverage and unmatched units. Recover a missing count from a documented accounting identity only where its components cover the same unit and period; retain observed/recovered flags and conservation checks. Unobserved counts are not automatically zero. Conserved totals do not establish correct local exposures; new allocation or linkage rules require CP2/CP4 review before dependent execution.

### 8.5 Identifier and session audit

Before aggregation or estimation, test uniqueness and reuse of identifiers, unit-period coverage, treatment-stream integrity, panel completeness, duplicate rows, unexpected merges, and the relation between rows and claimed analytical units. A serious identifier flaw is a data-integrity issue even if an analysis script runs.

Use qualified keys when identifiers repeat across households, waves, zones, or treatment streams, and check merge cardinality and assignment consistency. Distinguish respondent-level measures from household summaries such as “any member.” Identical analytical rows without original person IDs are not proven duplicate observations: retain them unless a source-supported deduplication rule exists, and document the resulting linkage limits.

When an intermediate file fails an integrity check, identify its actual downstream dependencies before stopping other routes. A proposed bypass using admitted round/source files must verify keys, periods, roles, join cardinality, included identities and unmatched exceptions against the intended analysis unit. Submit changed admission/design boundaries through CP2/CP4. A successful lineage check may support explicitly approved prepared inputs; it does not repair the rejected file or establish complete raw-to-analysis reconstruction. Save unresolved exceptions rather than silently dropping them.

### 8.6 Route-scope decision

For each result family, state required inputs, input presence, restrictions, external dependencies, author-local paths, feasible route, outputs that may be claimed, and closure requirement. A partial route may be useful but must retain a partial claim boundary.

### 8.7 Required Phase 2 artifacts

```text
02_source_and_artifact_audit/code_data_audit.md
02_source_and_artifact_audit/data_inventory.csv
02_source_and_artifact_audit/execution_dag.yml
02_source_and_artifact_audit/route_scope_matrix.csv
02_source_and_artifact_audit/external_file_integrity_ledger.csv
02_source_and_artifact_audit/identifier_session_audit.md
```

Update the run-level artifact inventory.

### 8.8 CP2 packet

Show source and data inventories, integrity evidence, code-state and Route A/B decision, execution graph where applicable, route matrix, identifier/session findings, restrictions, and result-family feasibility. For each material source gap, also show the permitted recovery checks completed, what they established, and the remaining specific prerequisite or proposed recovery action. Apply Section 4.5 before recommending a partial progression: the presence of usable inputs for other families does not by itself justify leaving a feasible source check undone. CP2 approval authorizes Phase 3 only.

## 9. Phase 3 — Independent Result Mapping

### 9.1 Purpose and anti-leakage rule

Define paper targets independently before execution. Phase 5 scripts must not contain paper target values. A permitted supplemental calibration target requires explicit reviewer approval, route label, and claim boundary.

### 9.2 Establish paper source and extraction provenance

Record paper edition, file hash where practical, page number, table or figure label, and whether each target came from text extraction, table extraction, OCR, manual transcription, or another approved paper source.

### 9.3 Text-layer PDF extraction

For a readable PDF:

1. extract page-labeled text;
2. identify candidate tables and figure captions;
3. build a table schema before recording values;
4. record headers, panels, spans, blank-cell meanings, row labels, and column labels;
5. capture statistic type, displayed value, display precision, units, and source page; and
6. flag ambiguous cells for review.

### 9.4 Scanned or low-quality PDF extraction

For a scanned or low-confidence page:

1. render the relevant page at reviewable resolution;
2. run OCR only as a candidate extraction method;
3. compare OCR output to the page image;
4. manually transcribe ambiguous targets;
5. save image path, extraction method, confidence, and reviewer decision; and
6. hold low-confidence cells for CP3 review.

### 9.5 Table-schema and manual-review rule

Multi-level headers, panel blocks, repeated row labels, merged cells, blank cells, and footnote-dependent quantities require a saved schema before extraction. Never guess a blank-cell interpretation. The target table records confidence and needs_human_review for every uncertain target.

Where displayed values appear internally inconsistent, first check that the labels refer to the same population, model and units. Test any claimed arithmetic relationship with the combined rounding bounds of all displayed inputs; do not assume a displayed contrast is an unadjusted difference of displayed means. Save a source-conflict record if the relationship remains unsupported. Keep the original targets distinct; do not rewrite them or choose an undocumented adjusted model to force consistency.

### 9.6 Required result-mapping artifacts

```text
03_result_mapping/result_map.yml
03_result_mapping/paper_target_table.csv
03_result_mapping/original_results_extracted.csv
03_result_mapping/target_results_review.md
03_result_mapping/paper_target_manual_review_decisions.csv
03_result_mapping/result_dependency_graph.yml
03_result_mapping/figure_validation_contract.csv
03_result_mapping/table_schemas/
```

### 9.7 Target and dependency mapping

For every target, record paper item, page, panel, row and column labels, statistic, paper display string, paper value, units, display precision, source, extraction method, confidence, reviewer flag, result family, route label, allowed target use, validation standard, tolerance or precision rule, expected failure mode, and notes.

Map each result family to required scripts or replacement modules, data roles, upstream dependencies, outputs, and closure conditions. Identify the specific parent statistic, sample, column, or transformation when a dependency is narrower than a whole family. A downstream claim cannot close while a dependency it actually requires is open, blocked, or diagnostic only; unrelated open columns do not automatically withhold an otherwise supported statistic or inference statement.

### 9.8 Figure contract

Choose the figure route before execution:

```text
pixel_level_visual_equality
backing_data_series_validation
event_study_pattern_validation
formula_grid_reconstruction
paper_text_anchor_validation
visual_pattern_validation
manual_only_design_figure
```

Record original source page, expected output, backing data or arrays if available, validation standard, reviewer requirement, and whether the result is numerical or visual only.

Make the contract checkable against the actual render: list required panels, groups, periods or grid points, pooled/reference points, visible numerical labels and their denominator (for example, total N versus group N), uncertainty method, and any required qualitative patterns. Distinguish printed numerical anchors from unprinted endpoints; only the former receive direct numerical targets unless a permitted unrounded reference exists. Define the operator and human review requirements separately.

### 9.9 CP3 packet

Show target table, extraction evidence, table schemas, manual-review decisions, result map, dependency graph, figure contract, and every target-specific validation standard. CP3 approval authorizes Phase 4 only.

## 10. Phase 4 — Environment and Reconstruction Plan

### 10.1 Purpose

Choose and document the approved execution environment and route before code is run or replacement code is written.

### 10.2 Software route decision

Identify original software, locally available software, proprietary requirements, rendering requirements, database or credential requirements, and expected run time. Choose one approved route:

```text
official_same_software_rerun
patched_author_script_route
translated_replication
independent_reconstruction
partial_or_blocked_route
```

Do not silently translate. A translated route requires a translation contract and CP4 approval.

### 10.3 Environment isolation and version locking

Use an isolated environment and a lock or version record where feasible:

1. R: use renv and retain renv.lock when feasible;
2. Python: use an isolated environment and retain a requirements lock, environment lock, or equivalent exact dependency record;
3. Julia: retain Project.toml and Manifest.toml when applicable;
4. Stata, MATLAB, SAS, and other proprietary systems: retain exact version, edition, relevant package versions, license-dependent limitations, and executed commands;
5. containerization: use a container when feasible and appropriate; otherwise state why an isolated environment plus lock or version record is the reproducibility route; and
6. all routes: retain session information, operating-system facts, package versions, hardware-sensitive notes, and environment build logs.

A session-info file alone is not sufficient when a lockfile or equivalent is feasible. If neither a lock nor a container is possible, record the exception and obtain CP4 approval.

State what was actually tested: installed-version agreement, a cached restore, a clean restore without that cache, or execution on another machine are different evidence levels. Retain commands and results for the claimed level; do not describe a cached restore as a portable rebuild. Distinguish proposed resource limits from implemented controls and measured usage. A missing mandatory CP4 safeguard requires a scoped decision before the affected execution continues, not an after-the-fact claim of compliance.

### 10.4 Dependency triage

Classify each dependency as:

```text
core_required
raw_data_route_only
optional_helper_only
plotting_only
developer_tool_only
unused_declared
unknown_until_execution
```

Do not install every dependency blindly. Record declared source, scripts and functions using it, install status, failure reason, and action.

### 10.5 Random-seed and repeated-run policy

For every stochastic result family, turn the Phase 3 validation standard into an executable policy before CP4. Record whether the route is deterministic; any seed, RNG, repetition rule, or parallelization instruction recovered from the paper, appendix, documentation, or approved author code; and the reproducibility-relevant execution settings.

If the available materials specify a seed or repetition procedure, follow that procedure and record it. If they do not, the operator must not silently choose seed values or a number of runs. The CP4 packet must contain a proposed seed and repeated-run policy for reviewer approval. The policy must state:

1. the proposed seed values or a reproducible seed-generation rule;
2. the proposed number and scale of runs, with a reason tied to the relevant result family;
3. the target-specific variation standard already approved in Phase 3;
4. the outputs retained for every run; and
5. how the Phase 6 comparison will use the repeated-run evidence.

A deterministic route requires no repeated-run check; record that decision in `seed_policy.md`. If observed variation exceeds the approved standard, retain every run and do not select a convenient single run as the replication output. Any change to the approved seed or repeated-run policy requires a return to Phase 4 and reviewer approval.

For computationally substantial stochastic routes, propose runtime, memory and storage limits, a replay check, and a precision criterion tied to the approved target standard. Specify RNG implementation and relevant package/parallel state, not only the top-level seed: cached generators or command order may affect replay. Record failed, superseded, replay and current production runs separately. Computational reproducibility and Monte Carlo precision do not establish paper-target eligibility. No universal draw count, seed count, or bootstrap variant is prescribed.

### 10.6 Translation contract

A translated route must state:

```text
original_software
translated_software
data_reader
model_formula_mapping
fixed_effects_mapping
cluster_or_robust_se_mapping
weights_mapping
missing_value_policy
sample_restriction_policy
rounding_policy
known_non_equivalences
claim_boundary
```

### 10.7 Reconstruction design

For Route B only, create a reconstruction design before writing replacement code. It states the code-state evidence or explicit independent-reconstruction request, the code-access boundary, permitted source data and documentation, excluded derived or result-like artifacts, paper specification sources, replacement language, result families, route per family, whether any target values are allowed as calibration inputs, validation outputs, expected caveats, non-reconstructable families, and required approval.

Before CP4, reconcile every approved numerical target with a planned output in the result map and batch plan, or a named open/blocked reason. Include descriptive rows, subgroup means, counts, joint tests and prose conversions, not only regression coefficients. Phase 5 receives the required statistic definitions and output identifiers, not the paper's target values. Verify this output coverage again at CP5; running every planned model is insufficient if required exports are absent.

### 10.8 Specification, crosswalk, and structural rules

For formulas and accounting quantities, document endpoints, lags, smoothing, deflators, base years, aggregation, trimming, and transformations. For regressions and summary statistics, document sample rules, outcome and variable definitions, weights, controls, fixed effects, clustering, and candidate operational rules.

Specify the population for each summary or derived percentage: an outcome-specific observed sample, a fitted-model sample, and a treatment-by-subgroup intersection are different denominators. Record the parent model/sample and any numerator/denominator transformation. Label the approved primary rule separately from diagnostic alternatives; numerical closeness cannot promote an alternative to primary.

Specify the order and population of transformations: currency conversion, one- or two-tail winsorization, quantile convention, row versus unique-unit cutoffs, sum versus mean across observed periods, transform-before versus transform-after aggregation, and all-missing versus zero handling where relevant. There is no universal winsorization or missing-baseline convention. A questionnaire-based component reconstruction needs verified links, component meanings, response-code handling and domain checks; a household-head field is not a substitute for a plot manager's attribute. An established approved rule may be implemented in Phase 5; an unresolved choice needs CP4 approval.

For specialized methods such as variable selection, IV quantiles or trimmed bounds, identify the application-specific ingredients needed to implement that estimator (for example, candidate dictionary and penalty rule, moments and normalization, or trimming population, ties and inference). Cite what is recovered and what is still missing. Keep an ordinary-regression fallback or a software-default diagnostic separate from the required estimator. A correct formula alone does not establish its input population, units, matching or normalization.

For reconstructed indices or latent measures, specify item coding, missingness, the population used to fit loadings, centering/scaling, sign orientation, normalization and whether subgroups reuse or refit the measure. Anchor sign conventions in source semantics; do not orient or rescale a measure to improve agreement with target values. For fitted plots, specify which variable is the outcome, axis units, conditioning values or fixed-effect normalization, bins or evaluation grid, and uncertainty. A reversed regression or a change in conditioning is a specification change, not merely a cosmetic redraw.

Where observations link to multiple people, places or periods, identify the analytical unit and the source-supported covariance/cluster construction. A feasible point estimator does not supply a missing inference rule. Do not invent a composite cluster key or impose a new complete-case population to obtain standard errors; hold the dependent inference targets locally and seek a CP4 decision while evaluating independently supported point estimates under their own eligibility rules.

For structural estimation, apply the hard stop in Section 14 before claiming a reconstructed estimator.

### 10.9 Batch plan

A batch is one bounded Phase 5 execution unit: a coherent, logged set of commands that produces named artifacts. A batch may prepare already approved inputs, execute author code, execute approved replacement code, generate a figure, export standardized outputs, or test a localized approved fix.

A batch is not a source-discovery or data-collection task; those belong to Phase 2. A batch is also not the final comparison with paper targets; that belongs to Phase 6. Writing replacement code occurs in Phase 5, and the execution of that code is recorded through one or more reconstruction batches.

One batch may support one result family, several related result families, or an upstream preparation step with no direct paper target. Each batch must state its type, purpose, affected result families or upstream role, permitted inputs, commands, expected outputs, expected runtime, seed policy where relevant, risks, and the Phase 6 destination for its outputs.

A batch may not silently change the approved inputs, route, target universe, or reconstruction design. A targeted fix must have its own bounded batch rather than modifying a baseline execution record.

### 10.10 Required Phase 4 artifacts

```text
04_environment_plan/environment_status.md
04_environment_plan/software_route_decision.md
04_environment_plan/session_info.txt
04_environment_plan/dependency_triage.csv
04_environment_plan/specification_completeness_audit.csv
04_environment_plan/result_family_sample_rules.csv
04_environment_plan/outcome_crosswalk.csv
04_environment_plan/variable_definition_audit.csv
04_environment_plan/seed_policy.md
04_environment_plan/batch_plan.csv
```

Add `04_environment_plan/code_reconstruction_design.md` for Route B. Add `04_environment_plan/translation_contract.md` for any translated Route A or Route B implementation. If no lockfile, container, or equivalent exact environment record is feasible, CP4 must approve the documented exception before execution.

### 10.11 CP4 packet

Show environment and lock evidence, route decision, dependency plan, seed policy, translation or reconstruction design, specification audits, crosswalks, structural decision, and batch plan. CP4 approval authorizes Phase 5 only.

## 11. Phase 5 — Execution, Reconstruction, and Targeted Batches

### 11.1 Purpose

Execute only the approved route and batches. Preserve both successful and failed evidence.

### 11.2 Preparation

Use a copied working package or verified output snapshot where writing could overwrite supplied materials. Create build, logs, and generated-output locations. Record every allowed route modification before it changes execution.

### 11.3 Author-code route

Run approved author scripts in the documented order. Record commands, working directories, start and end time, exit code, logs, generated paths, warnings, environment, and any compatibility fix. Do not label pre-existing outputs as generated unless their generation is evidenced in the current command manifest.

### 11.4 Independent reconstruction route

For Route B, Phase 5 is where the operator writes and executes the replacement code approved in `04_environment_plan/code_reconstruction_design.md`, using only its permitted sources. Author code quarantined under Section 2.3 remains excluded. Store the replacement scripts and supporting modules in `05_execution/build/scripts/`.

Each script or module must be traceable to the approved reconstruction design: its permitted inputs, paper specification sources, transformations or sample rules, model or formula, intended result families or upstream purpose, and generated outputs must be identifiable from retained artifacts. A script may support more than one related result family; the skill does not require an artificial one-script-per-result structure.

Do not use paper target values inside replacement code, except for a calibration use explicitly approved in the Phase 3 target record and the Phase 4 reconstruction design. For every executed reconstruction batch, export long-format values together with source-file references, sample definition, model or formula identifier, route label, and caveat flag.

Retain retrievable fitted row identities or source-row masks, exclusion reasons, cluster keys, and join lineage sufficient to check the approved sample; N alone is not a sample audit. Preserve source-file/row identity where original IDs are absent without claiming to recover missing person identities. For a summary, keep the population specified in Phase 4 rather than automatically imposing the regression mask. For a model-dependent conversion or subgroup mean, use its actual parent sample and approved subgroup intersection, full-precision outputs and units; do not substitute a paper denominator or a rounded printed coefficient.

Keep full precision for decision boundaries and derived assignments. When exporting and reloading cutoffs, quantiles or scores, verify that ties and row membership remain identical to the approved calculation. Retain the quantile/tie rule and original masks; do not reconstruct assignments from display-rounded boundaries or choose a new convention because it matches the paper better.

If implementation reveals a material undocumented operational choice or requires a departure from the CP4-approved design, stop that affected batch and return to Phase 4 for an approved design amendment.

### 11.5 Model and warning records

For iterative, de-meaned, or optimized models, record model identifier, convergence state, iterations, finite or undefined standard errors, estimate sanity, affected target identifiers, and required follow-up before any pass count is computed.

Warnings receive a separate classification:

```text
blocking_error
target_affecting_warning
pass_with_note_version_warning
pass_with_note_plotting_warning
pass_with_note_numerical_warning
pre_existing_package_log
non_executed_route_warning
```

### 11.6 Late availability of a previously audited input

This rule applies only when a material external input was already recorded in Phase 2 as missing, inaccessible, corrupted, unparseable, restricted, or otherwise unusable, and becomes available after CP4. It does not move source discovery or data-sufficiency auditing into Phase 5.

The newly available input must not be used directly in an execution batch. First return to Phase 2 to record its source, access conditions, integrity checks, schema and coverage results, intended role, and affected result families. Obtain a documented CP2 amendment for the revised route or scope. Then update the Phase 4 environment, reconstruction design, and batch plan, and obtain a CP4 amendment before execution.

Only after those amendments may the input enter a newly approved batch. Retain a dated late-input re-audit event and identify the first approved batch that used the input. The input cannot support a replication claim before that batch has executed and its outputs have passed Phase 6 eligibility and validation.

### 11.7 Targeted-fix batches

Use a targeted-fix batch only for a localized, documented issue. State prior evidence, hypothesis, allowed change, prohibited change, expected affected targets, commands, success criterion, and return checkpoint. Never tune data or model choices solely to match paper numbers.

Separate new estimation, exports from saved fits, and render-only repairs. Declare which samples, estimates, backing arrays, targets and standards must remain unchanged, then verify those invariants and preserve the previous version. For a label/layout-only repair, reuse the approved backing and compare its values or hash; do not refit models. For a field correction, retain the approved sample/estimator unless a separate design amendment changes them. A repaired implementation can still produce a numerical residual.

### 11.8 Required Phase 5 artifacts

```text
05_execution/build/scripts/
05_execution/build/route_modification_ledger.csv
05_execution/build/model_warning_ledger.csv
05_execution/build/parser_transformation_ledger.csv
05_execution/build/seed_record.csv
05_execution/logs/command_manifest.csv
05_execution/logs/<command logs>
05_execution/generated_outputs/generated_output_manifest.csv
05_execution/generated_outputs/reproduced_output_long.csv
05_execution/generated_outputs/model_and_sample_metadata.csv
05_execution/generated_outputs/figure_backing_artifacts/
```

Add a dated `late_input_reaudit_event.md` only when a previously audited input becomes newly available and a dated `targeted_fix_batch.md` only when a targeted fix is approved. The parser/transformation ledger records every type conversion, recode, merge, filter, deduplication, missing-value rule, unit conversion, and bounded repair that can affect a target.

### 11.9 CP5 packet

Show command manifest, successful and failed logs, output manifest, generated long-format outputs, warning and convergence evidence, seed records, late-input re-audit events, and targeted-fix results. CP5 approval authorizes Phase 6 only.

## 12. Phase 6 — Output Mapping, Validation, and Mismatch Audit

### 12.1 Purpose

Map generated outputs to independent paper targets, complete the eligibility gate, apply the predeclared standards, preserve raw outcomes, and determine which result families are closed.

### 12.2 Output mapping

For every reproduced statistic, record generating artifact, script, source files, integrity identifiers, model or formula identifier, sample definition, row and column labels, statistic, reproduced value, standard error, sample size, fit statistic, route label, and caveat flag.

Reconcile from the complete approved target register, not only from outputs that happened to be generated. Explicitly mark unmatched targets and their output-availability/closure reasons. Keep linked prose conversions and inference statements attached to their actual parent outputs; their separate review must not duplicate primary numerical credit.

### 12.3 Numerical validation

For each target:

1. complete the comparison-eligibility audit;
2. map the generated statistic to the independent paper target;
3. apply its Phase 3 standard;
4. compute permitted absolute and relative differences;
5. assess sign, standard error, sample size, significance, fit statistic, and joint test separately where relevant;
6. assign one raw outcome;
7. determine result-target and result-family closure; and
8. retain evidence paths and closure requirements.

### 12.4 Mismatch triage

Classify mismatches:

```text
target_extraction_error
paper_package_disagreement
rounding_or_display_precision
software_translation_difference
variance_estimator_difference
sample_construction_difference
missing_or_restricted_data
precomputed_output_only
implementation_bug
unknown
```

Return target-extraction issues to Phase 3, route issues to Phase 4, and implementation issues to Phase 5. An unresolved material sample, period, transformation, or definition requirement remains a diagnostic or non-closure under Section 5.2; a hypothesis offered to explain an eligible residual does not retroactively make that comparison ineligible.

For an authorized eligibility-only re-review, preserve the old decisions and outputs, define the affected target set, and record source/row evidence for both lifted and retained holds. Freeze the revised eligibility decisions before computing new differences. Acknowledge previously viewed outputs; do not claim a blind review. Keep targets, mappings, estimates and standards fixed unless a separate approved return changes them. Compare every newly eligible target, retain new residuals as well as passes, document each status transition, and verify that out-of-scope-of-review records are unchanged. Submit a new CP6 packet and stop; reporting revisions follow approval.

### 12.5 Specialized numerical triage

For summary statistics, document weights and bounded sensitivity checks rather than silently selecting the best match.

For regressions, evaluate core estimate, standard error, sample size, and fit statistic separately.

When N differs, reconcile actual included and excluded row identities, not just totals. Show sequential losses and overlapping missingness for outcome, baseline, controls and joins, distinguishing owner/manager/plot/period populations. A paper N equal to an outcome-observed count may suggest a missing-baseline question; it does not authorize filling missing values with zero, dropping controls or deleting observations to reach that N. Record candidate explanations as unconfirmed unless source evidence establishes the rule.

For formula and delta-method results, evaluate point estimate, standard error, joint test, and covariance route separately.

For a qualitative statistical claim, record the estimand, population, comparison and test actually supported by the source. Common direction, equality of slopes, equality of levels and equivalence are different claims; significance in one subgroup but not another is not itself a test of their difference. Specify the joint-testing or multiplicity scope where relevant. If the original test is undisclosed, label an approved alternative as diagnostic and report what it tests; neither a favorable nor an unfavorable diagnostic automatically reproduces or refutes the original claim. Internal accounting identities, finite covariance checks and exact seeded replay test implementation properties, not agreement with the paper.

For structural estimators, do not close the estimator from downstream consistency checks when the Section 14 hard-stop requirements remain unavailable.

### 12.6 Figure validation

File existence is only a manifest check. Use the predeclared route and retain evidence:

| Tier | Test | Evidence |
| --- | --- | --- |
| 1 | file exists and nonzero size | file manifest |
| 2 | page count or image dimensions | integrity record |
| 3 | rendered page is nonblank | render artifact |
| 4 | visual comparison with original output | side-by-side review sheet, source-page render, reviewer, decision |
| 5 | backing array or plotted-series comparison | arrays, mapping, numerical comparison |

Tier 4 requires a saved review sheet containing original source page or original output, reproduced figure, comparison criteria, reviewer, date, and decision. It is visual evidence and does not enter the numerical pass-rate numerator.

Keep the operator's visual findings separate from a required human decision. Generated backing data or approval to issue a report does not complete a pending human-review condition. Apply the reviewer requirement in the figure contract when calculating completed figure-route coverage.

Check each declared criterion on the current render as well as its backing. A correct total in a CSV does not satisfy a required on-figure label; seasonal points do not substitute for a required pooled point. Record label/series completeness, uncertainty-method agreement, numerical anchors, pattern findings and human decisions separately. A repair updates only the affected criteria: correct labels do not waive a CI-method difference or a remaining numerical residual. Retain explicit current render/backing/review version pointers so reporting does not revive a superseded defect.

For instrument or workflow diagrams, check source-content coverage, branches, sequence, panel titles and readable rendered text. Automated text-presence checks help locate omissions but cannot establish absence of clipping, incorrect ordering or illegible glyphs. A complete instrument diagram does not demonstrate availability of all depicted microdata. For decompositions and other constructed figures, distinguish internal identity checks from comparison with original backing values and the declared visual criteria.

### 12.7 Required Phase 6 artifacts

```text
06_validation/output_to_paper_map.csv
06_validation/comparison_eligibility_audit.csv
06_validation/comparison_matrix.csv
06_validation/validation_summary.md
06_validation/mismatch_audit.md
06_validation/accepted_caveats.csv
06_validation/warning_triage.csv
06_validation/figure_validation/
```

Add `fit_stat_triage.csv` when fit statistics are in scope and `summary_stat_triage.csv` when multiple documented definitions, transformations, or weights require bounded triage. Freeze `comparison_matrix.csv` after CP6. Later target-specific caveat decisions belong in `accepted_caveats.csv`; general reporting permission belongs in the checkpoint record. A corrected eligibility audit follows the versioned return rule and never overwrites the frozen matrix.

### 12.8 CP6 packet

Show output mapping, eligibility audit, raw comparison matrix, metric denominators and counts, mismatch audit, figure evidence, warnings, caveats, result-family closure table, and proposed final claim boundary. CP6 approval authorizes Phase 7 only.

## 13. Phase 7 — Full Audit Report, Reconciliation, and Delivery

### 13.1 Purpose and entry condition

Phase 7 assembles the final audit from retained evidence. It is not a one-page results summary. Enter only after CP6 validation evidence and closure states exist.

### 13.2 Reconciliation

Reconcile, before reporting:

1. run-level artifact inventory against actual used inputs;
2. source roles, integrity, approval, and execution status;
3. target-table counts against comparison-matrix counts;
4. raw outcomes against validation-summary totals;
5. caveat ledger against residuals and final wording;
6. figure contract against figure evidence; and
7. report claim boundary against result-family closure.

Also reconcile current manifest/roadmap status with the latest explicit checkpoint decisions and canonical artifact versions. Keep submission-time wording and hashes as historical evidence. Validate generated report tables against the approved matrix, including full-precision values, non-compared rows, residuals, separate linked-display counts, and pending figure decisions; a report must not silently recompute validation.

Reconcile inventory entries to current bytes, preserved historical bytes, or an explicitly documented retention exception and verified successor. Do not refresh expected hashes to conceal changes. Keep instruction-version changes separate from original-input integrity. Missing historical bytes must be disclosed and assessed for their effect on the audit claim; missing or inconsistent evidence needed to support a current result remains a blocking reconciliation issue. After approval, preserve the submitted packet and its checksums before updating live governance, then link a separate closure event and current verification record.

Any unresolved count, route, source-use, figure, or closure inconsistency blocks CP7. Fix the originating artifact and rerun reconciliation; do not reconcile by changing only report prose.

### 13.3 Required report content

The report must contain:

1. executive summary with route, counts, residuals, figures, open items, and claim boundary;
2. paper question, design, data, main findings, and interpretation limit;
3. scope, input ledger, source-use boundary, and code-access decision;
4. paper-specific Phase 0 through 7 and CP0 through 7 history;
5. source audit and data-integrity findings;
6. environment, implementation, route, and execution details;
7. independent target and validation contract;
8. validation by result family;
9. full detailed difference table;
10. quality metrics and explicit denominators;
11. open items and closure requirements;
12. figures and backing evidence;
13. artifact index and reconciliation;
14. reusable skill lessons; and
15. final assessment using Section 5.10 wording only.

### 13.4 Delivery artifacts

```text
07_report/replication_report.md
07_report/limitations.md
07_report/artifact_reconciliation.md
07_report/package_manifest.txt
07_report/checksums.sha256
```

Create an external delivery copy only after the in-run report is reconciled and CP7 approves it.

### 13.5 CP7 packet

Show final report, limitations, reconciliation, manifest, checksums, final status counts, and external-delivery location if requested. CP7 approval closes the run.

Record final approval as a dated closure event with the approved report/manifest version, preserved submitted-state evidence, and synchronized current governance. A closed audit may still conclude partial replication and retain unresolved targets or figure decisions. General CP7 approval does not convert these to passes or authorize a new run, further empirical work, or unrequested external sharing.

## 14. Specialized Applied-Empirical Branches

### 14.1 Missing-code reconstruction

Use only for Route B, when author code is missing, unusable, not provided, or quarantined under an explicit independent-reconstruction request. Build targets independently, define permitted source inputs and excluded derived/result-like artifacts, obtain CP4 approval for reconstruction design, implement the approved reconstruction scripts and supporting modules, and report reconstructed, backing-validated, calibrated, pattern-validated, and unclosed families separately.

### 14.2 Multi-route packages and result-family scope gaps

When a paper has several executable routes, use route_scope_matrix.csv. State scripts included and excluded, data requirements, restrictions, outputs claimed, scope status, and reviewer approval per route. Do not collapse a successful subset into a paper-wide success.

### 14.3 Difference-in-differences and event studies

Record treatment timing, never-treated and not-yet-treated comparators, anticipation rules, event-time binning, omitted period, estimator and weighting, cohort support, fixed effects, clustering, and pretrend or joint-test definitions. For staggered adoption, do not silently substitute a two-way fixed-effects estimator when the paper uses a cohort-robust estimator. Validate plotted coefficients, confidence intervals, event support, and omitted category separately.

### 14.4 Instrumental variables and encouragement designs

Record instrument assignment, treatment take-up, exclusion restriction interpretation, first stage, reduced form, estimand population, weak-instrument diagnostics, covariance route, and any finite-sample correction. Validate first-stage, reduced-form, IV estimate, sample, and inference separately; a matching IV coefficient does not close a mismatched first stage.

### 14.5 Regression discontinuity and threshold designs

Record running variable, cutoff, treatment rule, bandwidth, polynomial order, kernel, covariates, bias correction, variance method, mass-point handling, donut or manipulation checks, and plotting bins. Do not select a bandwidth or polynomial because it best matches the paper unless it is documented or approved as a sensitivity.

### 14.6 Formula and delta-method results

Document the formula, inputs, transformations, covariance route, window and endpoint conventions, and tests. Point estimates, uncertainty, and joint tests receive separate closure states.

### 14.7 Structural-estimation hard stop

Before claiming a structural estimator has been reconstructed, independently recover:

```text
moment_function
weighting_matrix_construction
optimization_constraints
starting_values
covariance_or_standard_error_route
overidentification_test_route
```

If any critical item is unavailable, use not_closed for the estimator. Input audits, formula checks, and downstream pattern evidence may be useful but cannot close the estimator.

### 14.8 Manual-design and figure-only items

Classify conceptual timelines, diagrams, or non-data design figures as manual-design items. Do not fabricate exact numerical points from a plot. State whether the evidence is visual, backing-data, formula-grid, text-anchor, or manual only.

## 15. Controlled Vocabulary

### 15.1 Access statuses

```text
provided
public
restricted
missing
unknown
```

### 15.2 Source-use statuses

```text
exists
integrity_checked
approved_for_execution
used_in_completed_batch
rejected_download
excluded_author_derived_artifact
```

### 15.3 Result classifications

```text
fully_reproducible
translated_reproducible
precomputed_output_only
manual_design_figure
artifact_level_validation
pattern_target
mechanism_target
blocked_restricted_data
not_in_scope
```

## 16. Canonical Template Library

### 16.1 Instantiation rule

Create run artifacts from these embedded schemas. Add paper-specific columns or sections when needed, but do not remove required fields. Supporting template files may later be synchronized from this document; they do not override it.

### 16.2 Run-governance templates

#### input_manifest.yml

```yaml
paper:
  title:
  authors:
  year:
  venue:
  doi_or_url:
  local_path:
  edition_or_version:
inputs:
  code_paths: []
  data_paths: []
  appendix_paths: []
  documentation_paths: []
  existing_output_paths: []
access:
  code_status:
  data_status:
  restrictions:
scope:
  main_text_empirical_results: true
  appendix_empirical_results: true
  approved_exclusions: []
code_access:
  policy:
  independent_reconstruction_requested:
  request_evidence:
  read_allowed:
  execute_allowed:
  summarize_allowed:
  prior_code_exposure:
  route_selected:
  replacement_code_required:
environment:
  expected_software: []
  external_dependencies: []
reviewer:
  name:
  role:
```

#### phase_roadmap.md

```markdown
# Paper-Specific Phase Roadmap

| Phase | Goal | Approved actions | Required artifacts | Checkpoint | Status |
| --- | --- | --- | --- | --- | --- |
| 0 | Intake and scope |  |  | CP0 | pending |
| 1 | Paper and design understanding |  |  | CP1 | pending |
| 2 | Source, code, data, and route audit |  |  | CP2 | pending |
| 3 | Independent result mapping |  |  | CP3 | pending |
| 4 | Environment and reconstruction plan |  |  | CP4 | pending |
| 5 | Execution and targeted batches |  |  | CP5 | pending |
| 6 | Validation and mismatch audit |  |  | CP6 | pending |
| 7 | Report, reconciliation, and delivery |  |  | CP7 | pending |

## Approved Scope

## Approved Exclusions and Closure Requirements

## Route Boundary

## Open-Issue Register and Authorized Next Actions
```

#### checkpoint_record.md

```markdown
# Checkpoint Record

Rule: only `approved` authorizes the next phase. Copy the entry below for CP0 through CP7 and complete every field. Cite actual artifact paths.

## CP0: Intake and Scope
## CP1: Paper Understanding
## CP2: Source and Route Audit
## CP3: Independent Result Mapping
## CP4: Environment and Reconstruction Plan
## CP5: Execution Review
## CP6: Validation Review
## CP7: Final Delivery Review

For each heading, add:

- Date:
- Reviewer:
- Phase goal:
- Completed work:
- Artifact paths reviewed:
- Key outputs:
- Unresolved issues:
- Open-issue IDs, proposed actions, responsible phases, and approval boundaries:
- Evidence retained after checkpoint:
- Reviewer decision: pending
- Approval wording:
- Required changes:
- Next authorized action:
- Notes:
```

#### open_issue_register.md

```markdown
# Open-Issue Register

Update this single run-level register when a material issue is found or reviewed. Workflow disposition is separate from raw validation outcome. Preserve earlier decisions and link to detailed phase evidence.

## Current Issue Summary

| Issue ID | Problem and affected scope | Workflow disposition | Next action and responsible phase | Required gate / actual decision | Closure evidence or remaining prerequisite |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

## Issue [ID]

- First identified phase/date:
- Problem, evidence, and uncertainty:
- Affected inputs, families/target IDs, and downstream dependencies:
- Recovery checks already completed and outcomes:
- Proposed action and whether supported, unverified, or externally blocked:
- Operator/reviewer and responsible phase:
- First dependent action that must wait:
- Workflow disposition and justification:
- Required approval and actual decision/wording:
- Next authorized action, expected artifact, and stopping condition:
- Closure test and evidence, or trigger for reopening:
- Raw outcome and effect on the final claim, where applicable:
- Dated updates and superseded decisions:
```

#### code_access_decision.md

```markdown
# Code Access Decision

## Code Status

Allowed values: `usable`, `missing`, `unusable`, `not_provided`, `present_unassessed`.

- Code status:

## Location and Inventory

- Paths inventoried:
- Files identified as code:
- Inventory hash evidence:

## Handling Rule

- Access policy:
- Independent-reconstruction request and evidence:
- Read allowed:
- Execute allowed:
- Summarize allowed:
- Usability decision and evidence:
- If unusable, precise reason:
- Prior author-code exposure and independence claim boundary:

## Consequence for This Run

- Selected Route A or Route B:
- Replacement code required:
- Reviewer approval:
- Claim boundary:
```

#### environment_requirements_precheck.md

```markdown
# Environment Requirements Precheck

## Expected software and versions

## Proprietary software or credentials

## Likely dependencies and build tools

## Data volume, runtime, and hardware

## Rendering and headless requirements

## Initial risks and CP0 decision
```

#### scope_confirmation.md

```markdown
# Scope Confirmation

- Default target universe: all main-text and appendix empirical results
- Approved exclusions:
- Partial or blocked families:
- Code-access boundary:
- Initial route:
- Required reviewer decision:
```

#### route_decision.md

```markdown
# Intake Route Decision

- Selected route: Route A / Route B
- Code state and usability evidence:
- Code-access policy and independent-reconstruction request evidence:
- Public-data availability evidence:
- Result families provisionally covered:
- Result families provisionally blocked:
- Recovery or clarification required:
- Reviewer decision:
```

#### artifact_inventory.csv

```text
artifact_id,path_or_url,artifact_type,origin,role_candidate,access_status,exists_status,integrity_status,checksum,created_or_retrieved_at,approved_for_execution,used_in_batch,canonical_owner_phase,notes
```

### 16.3 Paper-understanding templates

#### paper_content_for_final_report.md

```markdown
# Paper Content Record

## Citation
## Research Question and Contribution
## Paper Type and Design or Model
## Data, Units, and Sample
## Treatment, Inputs, Outcomes, and Parameters
## Main Tables and Figures
## Main Findings
## Interpretation Limits
## In-Scope Results
## Excluded or Open Results
## Sources Read
```

#### empirical_design_map.yml

```yaml
paper_type:
research_question:
unit_of_observation:
time_period:
data_sources: []
identification_strategy:
treatment_or_input:
outcomes: []
controls: []
fixed_effects: []
weights:
cluster_or_robust_se:
sample_restrictions: []
main_estimands: []
unresolved_specifications: []
```

#### claims_inventory.csv

```text
claim_id,claim_text,claim_type,paper_location,result_family,empirical_support,target_status,notes
```

#### target_universe_register.csv

```text
family_id,paper_item,paper_location,result_type,claim_role,in_main_text,in_appendix,provisional_route,in_scope,exclusion_or_block_reason,closure_requirement,review_status,notes
```

### 16.4 Source, data, and route-audit templates

#### external_file_integrity_ledger.csv

```text
file_id,path_or_url,expected_type,observed_type,parse_status,required_schema_status,coverage_status,retrieval_time,checksum,content_status,data_role,approved_for_execution,used_in_batch,notes
```

#### route_scope_matrix.csv

```text
route_id,route_description,scripts_included,scripts_excluded,input_data_required,input_data_present,requires_restricted_data,requires_author_local_paths,requires_external_credentials,outputs_claimed,scope_status,human_approval_status
```

#### result_dependency_graph.yml

```yaml
result_families:
  - family_id:
    description:
    upstream_families: []
    required_parent_targets_or_columns: []
    dependency_evidence:
    closure_condition:
    downstream_claims: []
```

#### late_input_reaudit_event.md

```markdown
# Late Input Re-audit Event

- Input and Phase 2 recorded status:
- What changed after CP4:
- Why the input is needed:
- Updated source and retrieval evidence:
- Integrity, schema, and coverage result:
- Affected result families and route/scope effect:
- CP2 amendment:
- Phase 4 plan amendment:
- CP4 amendment:
- First approved batch using it:
- Claim boundary:
```

#### code_data_audit.md

```markdown
# Code and Data Audit

## Code access boundary
## Script inventory and execution order
## Data inventory and roles
## Release, question/module coverage, valid-response intersections and eligible-unit linkage
## Source editions, semantic crosswalks and unresolved proxy boundaries
## Historical/geographic recovery: units, count identities, allocation, lineage and holds
## Inputs, outputs, and pre-existing artifacts
## Hard-coded paths and manual steps
## Randomness and seeds
## Identifier and session findings
## Route feasibility
## Open issues
```

#### data_inventory.csv

```text
data_id,path,role,unit_of_observation,time_coverage,key_fields,source_origin,access_status,integrity_id,used_by,notes
```

#### execution_dag.yml

```yaml
nodes:
  - node_id:
    type:
    path_or_command:
    inputs: []
    outputs: []
edges: []
```

#### identifier_session_audit.md

```markdown
# Identifier and Session Audit

## Claimed unit and row grain
## Candidate primary and panel keys
## Duplicate and uniqueness tests
## Panel, wave, cohort, and period coverage
## Merge cardinality and unmatched-record checks
## Treatment, cluster, household, firm, or geographic identifier reuse
## Missingness and attrition relevant to sample construction
## Result-family implications and blocking issues
## Evidence paths and reviewer decision
```

### 16.5 Result-mapping templates

#### paper_target_table.csv

```text
result_id,paper_item,page,panel,row_label,column_label,statistic,paper_display_string,paper_value,unit,display_precision,tolerance_or_precision_rule,package_reference_value,source,extraction_method,confidence,needs_human_review,source_conflict_flag,source_conflict_description,result_family,route_label,route_confidence,target_values_allowed_as_inputs,validation_standard,expected_failure_mode,figure_validation_method,notes
```

#### result_map.yml

```yaml
paper_results:
  - result_id:
    table_or_figure:
    paper_location:
    result_family:
    statistic_targets: []
    expected_input_roles: []
    expected_scripts_or_modules: []
    expected_generated_artifacts: []
    reported_precision:
    validation_standard:
    figure_validation_method:
    closure_condition:
```

#### comparison_eligibility_audit.csv

```text
comparison_eligibility_id,result_id,outcome_definition_match,input_definition_match,time_window_match,frequency_match,transformation_match,sample_match,aggregation_match,weights_controls_fe_match,covariance_route_match,eligible,closure_requirement,evidence_path,notes,output_available,approved_input_boundary,specific_unresolved_requirement,affected_dependency_scope,sample_identity_evidence,decision_version,prior_decision_id
```

#### original_results_extracted.csv

```text
result_id,paper_item,page,panel,row_label,column_label,statistic,paper_display_string,paper_value,display_precision,unit,extraction_method,source_image_or_text_path,confidence,review_status,notes
```

#### paper_target_manual_review_decisions.csv

```text
review_id,result_id,issue_type,source_page,evidence_path,reviewer,decision,corrected_value,review_date,notes
```

#### figure_validation_contract.csv

```text
figure_id,paper_item,paper_page,expected_output,validation_route,backing_artifact_expected,original_source_evidence,standard,reviewer_required,claim_boundary,notes,required_panels_series_points,required_visible_labels_and_denominators,uncertainty_method,printed_numeric_anchors,pattern_criteria
```

#### target_results_review.md

```markdown
# Target Results Review

## Paper edition and extraction provenance
## Target counts by result family and statistic
## Table schemas reviewed
## Low-confidence and ambiguous targets
## Paper/package source conflicts
## Figure-validation contracts
## Validation standards and tolerance rules
## Manual-review decisions
## CP3 readiness and unresolved items
```

Create one YAML file in `03_result_mapping/table_schemas/` per complex table, using this schema.

#### table_schema.yml

```yaml
paper_item:
source_page:
panels: []
column_levels: []
rows: []
statistic_location_rule:
parentheses_meaning:
blank_cell_meaning:
footnote_rules: []
ambiguous_cells: []
review_status:
```

### 16.6 Environment and reconstruction templates

#### environment_status.md

```markdown
# Environment Status

## Operating system and hardware
## Available and required software
## Runtime and package versions
## Isolation, lockfile, or container status
## Environment-build commands and logs
## Proprietary software, license, credential, and rendering constraints
## Known environment differences from the paper
## Verification actually performed: versions, cached restore, clean restore, or cross-machine execution
## Verification evidence and portability limits
## Proposed versus implemented and measured resource safeguards
## CP4 exception or approval required
```

#### software_route_decision.md

```markdown
# Software Route Decision

- Intake route: Route A / Route B
- Original software and version:
- Locally available software and version:
- Selected execution route:
- Translation required:
- Compatibility modifications anticipated:
- Known non-equivalences:
- Result families covered:
- Result families blocked:
- Claim boundary:
- Reviewer decision:
```

#### dependency_triage.csv

```text
package,declared_by,used_by_script,used_function,required_for_baseline_route,required_for_raw_data_route,required_for_optional_helper,installed_status,install_failure_reason,action
```

#### code_reconstruction_design.md

```markdown
# Code Reconstruction Design

- Code state and reason for Route B:
- Code-access policy and independent-reconstruction request evidence:
- Code read or executed:
- Prior author-code exposure and independence claim boundary:
- Replacement language:
- Allowed data files:
- Forbidden files:
- Paper specification sources:
- Result families:
- Reconstruction route per family:
- Measurement construction: item codes, fitting population, centering/scaling, sign, normalization and reuse/refitting:
- Sample and transformation rules: full-precision boundaries, quantile/tie conventions and retained row masks:
- Fitted plots: outcome direction, units, conditioning, bins/grid and uncertainty:
- Analytical unit, linked entities and covariance/cluster rule; point/inference eligibility boundaries:
- Primary specification versus approved diagnostics and their claim boundaries:
- Target values allowed inside code:
- Validation outputs:
- All-target planned-output or open/blocked-reason reconciliation:
- Expected caveats:
- Not reconstructable without author code:
- Human approval required before Phase 5:
```

#### specification_completeness_audit.csv

```text
specification_id,result_family,rule_category,paper_statement,operational_rule,status,evidence_path,approved_sensitivity,closure_requirement,notes
```

#### result_family_sample_rules.csv

```text
sample_rule_id,result_family,paper_item,unit,period_start,period_end,inclusion_rule,exclusion_rule,weights,missing_value_policy,evidence_path,notes
```

#### outcome_crosswalk.csv

```text
crosswalk_id,paper_outcome_label,package_or_reconstructed_variable,definition,unit,transformation,period,source_file,evidence_path,notes
```

#### variable_definition_audit.csv

```text
variable_id,paper_label,variable_name,source_file,definition,unit,transformation,missing_value_rule,used_in_result_families,evidence_path,notes
```

#### batch_plan.csv

```text
batch_id,batch_type,purpose,result_families_or_upstream_role,allowed_inputs,commands,expected_outputs,expected_runtime,seed_policy,risk,validation_destination,approval_status,notes
```

#### seed_policy.md

```markdown
# Seed and Stochastic-Execution Policy

- Affected result families:
- Deterministic or stochastic route:
- Recovered seed, RNG, or repetition instruction:
- Parallelization and reproducibility constraints:
- Proposed seed values or reproducible seed-generation rule:
- Proposed number and scale of repeated runs, with justification:
- Target-specific variation standard from Phase 3:
- RNG/package-state initialization and replay procedure:
- Runtime, memory, and storage limits when material:
- Outputs retained per run:
- Phase 6 use of repeated-run evidence:
- Reviewer approval:
```

#### translation_contract.md

```markdown
# Translation Contract

- Original and translated software:
- Data-reader mapping:
- Estimator or formula mapping:
- Fixed-effects mapping:
- Weight mapping:
- Robust or clustered covariance mapping:
- Missing-value behavior:
- Factor and reference-level behavior:
- Sample-restriction mapping:
- Optimization defaults:
- Rounding policy:
- Known non-equivalences:
- Validation consequences:
- Claim boundary:
- Reviewer approval:
```

#### structural_estimation_checklist.md

```markdown
# Structural Estimation Checklist

- Moment function independently recoverable:
- Weighting matrix construction independently recoverable:
- Optimization constraints recoverable:
- Starting values recoverable:
- Covariance or standard-error route recoverable:
- Overidentification-test route recoverable:
- Eligible closure state:
- Evidence paths:
- Reviewer decision:
```

### 16.7 Execution templates

#### command_manifest.csv

```text
command_id,stage,working_directory,command,started_at,ended_at,exit_code,log_path,generated_files,notes
```

#### route_modification_ledger.csv

```text
modification_id,route_id,script_or_environment,original_state,modified_state,reason,allowed_without_approval,reviewer_approval,evidence_path,affected_result_families,notes
```

#### targeted_fix_batch.md

```markdown
# Targeted Fix Batch

- Batch identifier:
- Prior evidence:
- Localized issue:
- Hypothesis:
- Allowed change:
- Prohibited change:
- Affected result identifiers:
- Inputs:
- Commands:
- Expected outputs:
- Success criterion:
- Invariants and checks for unchanged samples, values, backing, targets, and standards:
- Linked open-issue IDs and required design/source amendments:
- Expected issue-state update and remaining limitations:
- Required checkpoint:
```

#### model_warning_ledger.csv

```text
warning_id,model_id,script,warning_text,convergence_status,iterations,standard_error_status,estimate_sanity_status,affected_result_ids,excluded_from_pass_count,required_follow_up,final_status,notes
```

#### parser_transformation_ledger.csv

```text
event_id,batch_id,script,input_artifact,output_artifact,operation_type,variable_or_rows_affected,rule_or_code,evidence_or_rationale,record_count_before,record_count_after,target_ids_affected,review_required,notes
```

#### seed_record.csv

```text
run_id,batch_id,result_family,seed,rng_implementation,parallelization_setting,run_scale,started_at,ended_at,output_artifacts,target_outputs,notes
```

#### reproduced_output_long.csv

```text
result_id,paper_item,generated_artifact,generating_script,source_files,source_integrity_ids,model_or_formula_id,sample_definition,sample_rule_id,outcome_crosswalk_id,row_label,column_label,statistic,reproduced_value,standard_error,sample_size,fit_stat,route_label,caveat_flag,notes
```

#### generated_output_manifest.csv

```text
output_id,path,generating_command_id,generating_script,file_type,created_at,size,hash,result_families,pre_existing_before_run,notes
```

#### model_and_sample_metadata.csv

```text
model_or_formula_id,result_family,sample_definition,observation_count,cluster_count,weights,fixed_effects,covariance_route,convergence_status,seed_or_run_id,notes,sample_identity_artifact,exclusion_artifact,join_lineage_artifact,parent_model_or_output_id,summary_population_or_subgroup_rule
```

### 16.8 Validation templates

#### comparison_matrix.csv

```text
result_id,table_or_figure,panel,row_label,column_label,statistic_type,original_value,replicated_value,comparison_performed,comparison_eligibility_id,absolute_difference,relative_difference,display_precision_match,sign_agreement,standard_error_match,sample_size_match,significance_agreement,core_estimate_pass,standard_error_pass,sample_size_pass,fit_stat_pass,joint_test_pass,route_label,validation_standard,raw_validation_outcome,closure_state,closure_requirement,notes
```

#### accepted_caveats.csv

```text
caveat_id,result_id,paper_value,reproduced_value,difference,raw_validation_outcome,likely_reason,evidence_path,why_not_a_blocking_failure,reviewer_approval,final_report_wording,notes
```

#### fit_stat_triage.csv

```text
triage_id,result_id,fit_statistic,paper_value,reproduced_value,difference,eligible,likely_reason,raw_validation_outcome,closure_requirement,notes
```

#### summary_stat_triage.csv

```text
triage_id,result_id,variable,statistic,paper_value,reproduced_value,weighting_rule,sample_rule,transformation,best_candidate_status,raw_validation_outcome,closure_requirement,notes
```

#### warning_triage.csv

```text
warning_id,warning_text,script,output_potentially_affected,target_validation_result,classification,reason,requires_fix,reported_in_final,notes
```

#### output_to_paper_map.csv

```text
map_id,result_id,generated_artifact,generated_location,generated_statistic,source_result_id,eligibility_id,route_label,evidence_path,notes
```

#### validation_summary.md

```markdown
# Validation Summary

## Approved Scope and Denominators
## Direct Numerical Coverage
## Strict Numerical Pass Rate
## Conditional Agreement Rate
## Strict Target Attainment
## Separate Linked-Display and Inference Reviews
## Qualitative Claims: Source Estimand/Test, Diagnostic Alternatives and Claim Boundaries
## Result-Target and Result-Family Closure
## Figure-Route Coverage
## Raw Outcome Counts
## Residuals, Open Items, and Blocked Items
## Proposed Claim Boundary
```

#### mismatch_audit.md

```markdown
# Mismatch Audit

| Result ID | Raw outcome | Mismatch classification | Evidence | Return phase or closure requirement | Reviewer disposition |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |
```

#### figure_review_sheet.md

```markdown
# Figure Review Sheet

- Figure identifier:
- Declared route and tier:
- Original source page or output:
- Reproduced figure:
- Backing arrays if applicable:
- Comparison criteria:
- Criterion-level findings for panels/series/points, visible labels, intervals, anchors, and patterns:
- Current render/backing/review versions and superseded artifacts:
- Instrument/workflow content, sequence and rendered readability, where applicable:
- Internal construction checks versus source-value or visual agreement:
- Operator findings and evidence:
- Human decision required by contract:
- Reviewer:
- Review date:
- Decision:
- Claim boundary:
```

### 16.9 Final-report and reconciliation templates

#### replication_report.md

```markdown
# Replication Audit Report: [Paper Title]

**Paper:** [citation]  
**Replication run:** [run slug]  
**Report date:** [date]  
**Route:**  
**Author-code status:** [usable / missing / unusable / not_provided / present_unassessed]  
**Author-code access policy:** [permitted / quarantined]

## 1. Executive Summary

State the route, approved scope, direct-validation denominators and totals, reviewed residuals, figure-route results, open families, blocked families, and precise claim boundary.

## 2. What the Paper Does

Cover the research question, design or model, data, intervention or estimation strategy, central findings, and interpretation limit.

## 3. Scope, Inputs, and Code-Access Boundary

### 3.1 Approved replication scope

### 3.2 Input and source-use ledger

| Artifact | Present | Integrity checked | Approved | Used | Role / restriction |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

### 3.3 Code-access decision and external dependencies

## 4. Paper-Specific Roadmap and Human Checkpoints

For every phase, write the phase goal, actions, artifacts, issues, resolution, checkpoint review, and reusable lesson.

### 4.1 Phase 0, CP0: Intake and scope

### 4.2 Phase 1, CP1: Paper and design understanding

### 4.3 Phase 2, CP2: Source, code, and data audit

### 4.4 Phase 3, CP3: Result mapping and target review

### 4.5 Phase 4, CP4: Environment and reconstruction plan

### 4.6 Phase 5, CP5: Execution batches and targeted follow-up

### 4.7 Phase 6, CP6: Validation, mismatch audit, and human verification

### 4.8 Phase 7, CP7: Final report and reconciliation

## 5. Source Audit and Data Integrity

Include data roles, keys, session completeness, source limitations, checksum/integrity evidence, and any restricted or absent inputs.

## 6. Environment and Implementation

Include software, versions, route choice, replacement-code boundary, parser/cleaning rules, model conventions, and execution batches.

## 7. Result Mapping and Validation Contract

Explain the independent target table, table schemas, figure routes, comparison eligibility gate, tolerance, count rule, and status vocabulary.

## 8. Validation Results by Result Family

| Result family | Direct checks or route | Closure state | Evidence and claim boundary |
| --- | ---: | --- | --- |
|  |  |  |  |

## 9. Detailed Difference Table

Include every in-scope numerical target in the detailed comparison table or a linked complete table. Include non-compared targets and every residual. Preserve raw matrix status and add human reporting disposition separately.

| Result family | Cell / result ID | Statistic | Paper | Reproduced | Difference | Raw outcome | Reviewer disposition | Likely reason |
| --- | --- | --- | ---: | ---: | ---: | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |

## 10. Quality Metrics and Denominators

Report A, E, S, N, and R; direct numerical coverage; strict numerical pass rate; conditional agreement rate; strict target attainment; result-target closure; result-family coverage; and figure-route coverage.

## 11. Open Items and Closure Requirements

| Result family | Available evidence | Why open or blocked | Effect on paper claim | What would close it |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

Link unresolved issue IDs to recovery attempts, remaining actions, responsible phases, required approvals, and the reviewer's decision to report rather than execute them. Do not present an untested proposal as a completed solution or an open route as permanently impossible.

## 12. Figures and Backing Evidence

| Figure | Declared validation route | Backing or review artifact | Outcome |
| --- | --- | --- | --- |
|  |  |  |  |

## 13. Audit Artifacts and File Index

List the roadmap, checkpoint record, code-access decision, integrity ledger, target table, scripts, logs, generated outputs, validation matrix, `accepted_caveats.csv`, and reconciliation file.

## 14. Lessons for the Skill

Record only reusable improvements grounded in this run.

## 15. Final Assessment

Use exactly one of: `fully reproduced within approved scope`, `reproduced with documented residuals`, `partial replication`, or `diagnostic validation only`. State what was reproduced, what was validated by another route, what remains open, and what the report does not establish.
```

#### artifact_reconciliation.md

```markdown
# Artifact Reconciliation

## Source and Input Reconciliation

| Artifact | Exists | Integrity checked | Approved | Used in completed batch | Notes |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

## Target and Comparison Reconciliation

## Figure Reconciliation

## Report Count Reconciliation

## Current Approval and Canonical-Version Reconciliation

## Historical Report and Submitted-State Preservation

| Inventoried path/version | Expected hash | Current or archived byte location | Verified successor | Retention exception and claim effect |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

Separate instruction-version changes from original-input integrity. Link the immutable submitted packet, approval event and current governance verification; do not silently replace historical expected hashes.

## Rejected, Restricted, and Excluded Artifacts

## Final Reconciliation Statement
```

#### limitations.md

```markdown
# Limitations and Open Items

| Result family | Status | Evidence available | Limitation | Claim effect | Closure requirement |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

For every retained issue, link the run-level issue ID and state recovery attempts, proposed next action, responsible phase, prerequisite/approval, and the decision permitting reporting with the limitation.
```

#### package_manifest.txt

```text
path
role
origin
hash
included_in_delivery
```

### 16.10 Template coverage rule

Every artifact named in a phase’s required-artifact list must have a maintained starter in `templates/`, except generated logs, session/environment records, checksums, copied scripts, rendered figures, and paper-specific directories. Before release, compare one-line CSV headers and Markdown/YAML fields against this section. A schema mismatch blocks use until the template or specification is corrected.

## 17. Operational Use and Maintenance

### 17.1 Starting a run

Create a new paper-specific run folder. Complete Phase 0 only, produce the CP0 packet, and stop for approval. Never skip a checkpoint because a package appears straightforward.

If using the optional Python helpers, run `scripts/init_run.py --help` for Phase 0 scaffolding and `scripts/audit_run.py --help` for numerical-ledger checks. They require Python 3.10 or later and its standard library. The initializer saves blank intake records and the instruction version; the operator must complete the audit and request CP0 approval. The ledger checker reads explicitly supplied target, comparison, eligibility and scope files. It checks IDs, states and denominators without approving analytical eligibility, inferring reviewer decisions or changing raw outcomes.

When continuing an existing run, read its saved instruction version, current manifest, roadmap, latest checkpoint decisions and open-issue register. Locate the current approved artifacts and distinguish them from historical submissions. Confirm the next authorized action before executing it. A newly installed skill version does not retroactively change an existing run's standards; discuss any proposed migration with the reviewer.

### 17.2 Supporting-file maintenance

This SKILL.md is the sole normative source, and `templates/` contains only operational artifact starters. If a future update changes a rule, field, route label, or report requirement, update this document first and then synchronize every affected template. Do not create a parallel reference specification.

Use `scripts/sync_templates.py` to check exact agreement with the embedded starters. Its explicit `--write` option regenerates template copies inside the skill folder; it never updates run artifacts. In the source repository, run `python3 tools/check_release.py` and `python3 -m unittest discover -s tests -v` before preparing a release. These checks cover packaging and helper behavior; retain separate evidence for actual agent use and statistical validation.
