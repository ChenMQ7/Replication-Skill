# Contributing

Report a concrete problem with the skill version, host, affected phase, expected behavior and observed behavior. Attach the smallest shareable evidence that explains it. Remove credentials, personal paths and restricted data.

For a change, explain the case or test that motivates it. Edit `skills/applied-empirical-replication-v3/SKILL.md` first when a rule or schema changes. Then regenerate the template copies:

```sh
python3 skills/applied-empirical-replication-v3/scripts/sync_templates.py --write
python3 tools/check_release.py
python3 -m unittest discover -s tests -v
```

Tests should check behavior: preserved files, rejected invalid states, correct denominators or refusal to overwrite a run. A text search alone cannot demonstrate that an agent follows a checkpoint.

Keep documentation, comments, commit messages and pull requests in English. Prefer specific statements about behavior and evidence. Keep technical terms, numbers and restrictions intact when editing prose. The [humanizer guidelines](https://github.com/blader/humanizer) are an optional editing reference, not a runtime dependency.

Do not silently broaden research scope, change numerical thresholds or treat a partial historical case as a full replication. Describe any migration effect on existing runs. Changes to the skill do not rewrite frozen run evidence.

Contribution review checks consistency with the License and the terms of any third-party material. Include external code or datasets only when their provenance and redistribution terms are clear.
