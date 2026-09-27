# Reviewing checkpoints

The user is the reviewer by default. You need enough familiarity with the paper and its methods to assess the proposed decisions, or someone who can review those parts with you. The agent must provide the evidence, uncertainty and requested scope in the checkpoint packet.

| Checkpoint | Read and decide |
| --- | --- |
| CP0 | Confirm the paper, inputs, code-access policy, initial scope, software risks and roadmap. Approval permits Phase 1. |
| CP1 | Check the explanation of the paper, research design and main-text/appendix result inventory. Approval permits the source audit. |
| CP2 | Review source roles, data integrity, restrictions and feasible recovery checks. Decide which inputs and partial routes may proceed to target mapping. |
| CP3 | Inspect independent targets, uncertain transcriptions, units, numerical standards and figure contracts. Approve the comparison criteria before execution. |
| CP4 | Review the software environment, reconstruction or translation design, unresolved operational choices, stochastic policy and batches. Approval permits the specified execution. |
| CP5 | Review saved code, commands, outputs, warnings and failed attempts. Confirm what is ready for validation and whether a scoped repair is needed. |
| CP6 | Review eligible comparisons, retained differences, metric denominators, figure evidence and closure states. Approve a return loop or reporting with stated limits. |
| CP7 | Review the full report, artifact reconciliation, claim and delivery scope. Approval closes the audit at its stated assessment. |

The complete requirements are in [SKILL.md, Section 4](../skills/applied-empirical-replication-v3/SKILL.md#4-checkpoint-governance).

## Make the scope explicit

An approval can be short when the packet has a clear scope:

> Approve CP2 for the listed inputs and routes. Retain the stated local holds and proceed to Phase 3. Do not execute analysis.

For a revision, identify what must change:

> Return CP4 for revision. Verify the units and propose the sample rule for Table 3 before executing its batch. The other approved batches are unchanged.

The agent saves the decision's wording and updates current governance. Historical packets retain their submission state and hashes. A generic approval does not resolve an omitted analytical choice or waive a restriction.

## When problems remain

The packet should explain the problem, affected results, checks already completed, remaining action, responsible phase and required approval. Ask for those details if they are missing. A feasible source check should be completed or explicitly deferred; a method choice needs an approved design before execution.

New inputs require an admission review. Changes to frozen targets return to CP3; analytical design changes return to CP4. Approved implementation or rendering repairs return through Phase 5 and affected validation. An eligibility correction using sufficient existing evidence can use the bounded Phase 6 re-review route.

## Read the reported results carefully

Numerical agreement applies only after the comparison is eligible. A supported sample rule with a different N can yield an eligible numerical residual. An unsupported outcome definition can prevent comparison even when the numbers look close.

The report separates strict passes, passes with notes, residuals, non-comparable results, unclosed work and blocked results. Check both the coverage denominator and the pass-rate denominator. Accepting a caveat leaves the raw outcome unchanged.

Each figure follows its approved contract. Inspect the current source/render pair and any required numerical anchors, backing data and labels. Record criterion-specific human decisions when required. CP6 or CP7 approval alone does not mark every figure as accepted.
