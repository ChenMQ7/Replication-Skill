# Template Inventory

`SKILL.md` is the sole policy and schema authority. These files remain only because copying a checked starter into a run folder is safer and faster than retyping fields. A template must be synchronized whenever its schema changes in `SKILL.md`.

## Always-used governance and phase starters

- Phase 0: `input_manifest.yml`, `scope_confirmation.md`, `artifact_inventory.csv`, `environment_requirements_precheck.md`, `code_access_decision.md`, `route_decision.md`, `phase_roadmap.md`, `checkpoint_record.md`
- Phase 1: `paper_content_for_final_report.md`, `empirical_design_map.yml`, `claims_inventory.csv`, `target_universe_register.csv`
- Phase 2: `code_data_audit.md`, `data_inventory.csv`, `execution_dag.yml`, `route_scope_matrix.csv`, `external_file_integrity_ledger.csv`, `identifier_session_audit.md`
- Phase 3: `result_map.yml`, `paper_target_table.csv`, `original_results_extracted.csv`, `target_results_review.md`, `paper_target_manual_review_decisions.csv`, `result_dependency_graph.yml`, `figure_validation_contract.csv`, `table_schema.yml`
- Phase 4: `environment_status.md`, `software_route_decision.md`, `dependency_triage.csv`, `specification_completeness_audit.csv`, `result_family_sample_rules.csv`, `outcome_crosswalk.csv`, `variable_definition_audit.csv`, `seed_policy.md`, `batch_plan.csv`
- Phase 5: `command_manifest.csv`, `route_modification_ledger.csv`, `model_warning_ledger.csv`, `parser_transformation_ledger.csv`, `seed_record.csv`, `generated_output_manifest.csv`, `reproduced_output_long.csv`, `model_and_sample_metadata.csv`
- Phase 6: `output_to_paper_map.csv`, `comparison_eligibility_audit.csv`, `comparison_matrix.csv`, `validation_summary.md`, `mismatch_audit.md`, `accepted_caveats.csv`, `warning_triage.csv`, `figure_review_sheet.md`
- Phase 7: `replication_report.md`, `limitations.md`, `artifact_reconciliation.md`, `package_manifest.txt`

## Conditional starters

- Any material unresolved issue: instantiate `open_issue_register.md` at the run root; maintain the same register through all affected checkpoints (Section 4.5).
- Route B only: `code_reconstruction_design.md`
- Translated implementation only: `translation_contract.md`
- Structural-estimation application only: `structural_estimation_checklist.md`
- Previously audited input becomes newly available after CP4 only: `late_input_reaudit_event.md` (CP2 and CP4 amendments required by Section 11.6)
- Approved localized rerun only: `targeted_fix_batch.md`
- Fit-statistic ambiguity only: `fit_stat_triage.csv`
- Summary-statistic definition or weighting ambiguity only: `summary_stat_triage.csv`

Generated logs, checksums, session records, scripts, figures, and paper-specific table-schema copies are not static templates.

## Synchronization

All 63 starters are embedded in Section 16 of `SKILL.md`. Run `python3 scripts/sync_templates.py` from the skill folder to check their contents. Use its `--write` option after editing the canonical schema. Existing run artifacts are outside this synchronization step.
