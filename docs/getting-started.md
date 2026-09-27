# Getting started

## Requirements

Use an agent that can read local files, inspect PDF pages, run terminal commands and pause for your decisions. You need access to the paper and permission to use the supplied materials. Source recovery may need a browser or search tool. You remain the reviewer unless you name someone else.

Python 3.10 or later is needed only for the bundled helpers. Each paper has its own statistical environment. R, Stata, Python, Julia or another system may be appropriate; the skill does not install all of them. Proprietary software needs a valid local license. Runtime, memory and storage requirements are assessed for the chosen paper.

## Load or install the skill

For a local checkout, give the agent the full path to `skills/applied-empirical-replication-v3/SKILL.md` and ask it to use that skill. Check that it has read the complete file before starting intake.

For Codex discovery, copy the whole `applied-empirical-replication-v3` folder into your research repository's `.agents/skills/` directory. Keep templates and scripts beside `SKILL.md`. Check for an existing installation with the same name before copying; preserve any locally edited version. Avoid installing multiple copies with the same name.

You can ask Codex's skill installer to install `skills/applied-empirical-replication-v3` from `ChenMQ7/Replication-Skill`. Record the installed commit or version. Select a tagged release when one is available and the installer supports it; the current repository version is a candidate.

See the [official Codex skill documentation](https://learn.chatgpt.com/docs/build-skills) for current discovery locations and installer behavior. This candidate is a standalone skill; it has no plugin manifest or marketplace installation claim.

## Prepare the inputs

Keep the supplied package intact. Provide paths to the paper, appendix, code, data and README files that you have. State any access restrictions. Choose a separate writable parent folder for replication runs; avoid placing generated files inside the author's package.

For the standard author-code route, ask:

> Use this skill with the supplied paper, code and data. Save all work in a new run folder. Complete Phase 0 and stop for CP0. Audit author code under the default access policy.

For an independent reconstruction test, ask:

> Use this skill with the paper and data to reconstruct the analysis independently. Quarantine author scripts: inventory only their filenames, paths and hashes. Do not read or run them. Complete Phase 0 and stop for CP0.

The agent records the available evidence and provisional route at intake. The presence of a file does not establish that it can support a particular result.

## Optional Phase 0 scaffold

The agent can create the folders itself. To use the helper, create your intended run-parent directory and run this command from the repository root, replacing the example paths:

```sh
python3 skills/applied-empirical-replication-v3/scripts/init_run.py \
  "replication_runs/my-paper" \
  --paper "local_inputs/paper.pdf" \
  --title "Paper title"
```

Add `--independent-reconstruction` only for an explicit independent-reconstruction request. The helper refuses an existing destination. It creates blank intake records, empty later-phase folders and a snapshot of the instruction version. It does not inspect the inputs, choose a route, run analysis or approve CP0. Complete the intake records before requesting review.

## Review and resume

At each checkpoint, read the linked evidence and the requested decision. You can approve a scoped next step, request revisions or defer a route. See [the review guide](reviewing-checkpoints.md).

To resume in a new conversation, provide the run folder and ask:

> Read this run's saved skill version, manifest, roadmap, checkpoint record and open issues. Identify the latest approved artifacts and next authorized action. Explain any conflicting state before continuing. Preserve submitted versions and do not infer new approval.

Existing runs keep their recorded standards. Discuss a proposed skill-version migration before applying new rules.

## Output and common problems

The final report is `07_report/replication_report.md` inside the run folder. Its evidence includes source audits, targets, code, logs, comparisons, figure reviews and limitations. Sharing that package is a separate decision subject to data permissions.

If an input is unavailable, review the specific recovery proposal and affected results. If software is unavailable, approve a documented alternative or a local hold. If a PDF is scanned, the target extraction needs page-image checks. A nonzero helper exit code calls for inspecting the error; never repair a check by silently changing a frozen result.
