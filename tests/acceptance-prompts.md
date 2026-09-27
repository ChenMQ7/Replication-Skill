# Fresh-session prompts

These prompts are inputs to the independent tests in [release checks](../docs/release-checks.md). Replace the paths with evaluator-approved inputs. Start a new session for each test. Give the agent the skill and the prompt, without the evaluator's expected answer. Record actual tool use and saved artifacts.

## Standard intake

Use the supplied replication skill to replicate the paper. The input folder contains the paper, data and the authors' scripts. Store the run in the specified empty parent directory. Begin the work.

## Independent reconstruction intake

Use the supplied replication skill to reconstruct this paper from its paper and data, independently of the supplied author code. Store the run in the specified parent directory. Begin the work.

## Incomplete inputs

Use the supplied replication skill with this paper and package. Some inputs may need to be located. Identify what can be done and what evidence is needed next.

## Resume

Continue the supplied run using its saved instructions and evidence. Establish its current approval state before taking the next action.

## Mixed-result report

Inspect the supplied validation packet and draft the report section permitted by its saved approval. Preserve the recorded numerical decisions and figure-review state. Do not execute new analysis.

## Recording the evaluation

The evaluator retains host/model settings, instruction hash, input permissions, prompt, transcript or tool trace, output paths, observed behavior and decision. Empty evidence fields mean the test has not been completed. An agent's own statement that it followed a rule is insufficient when file access or actual stopping behavior can be checked.
