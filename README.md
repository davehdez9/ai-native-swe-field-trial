# Phase 9B field-pilot: personal task tracker

A locally version-controlled, Python standard-library application. This is an **author-driven AI-assisted local integration pilot**, not an independent real coding-agent execution or a customer validation study.

Phase 9 baseline is commit `baseline`; Phase 9B change adds due dates, overdue filtering and a tiny CLI. Reproduce tests with:

```bash
python3 -m unittest discover -s tests -v
python3 -m src.cli --store /tmp/phase9b-tasks.json add --id T1 --title 'Review plan' --due 2026-12-01
python3 -m src.cli --store /tmp/phase9b-tasks.json overdue --as-of 2026-12-02
```

No cloud services, API credentials or production deployment. See `docs/` for task contract and evidence. `AGENTS.md` is written guidance **only**, not an enforceable sandbox. Git history contains baseline, test-first red commit, and green implementation.

## Known limitations

- A single local process is assumed; simultaneous writers can race, and `.tmp` filenames are not unique. Do **not** use this as a multi-user service.
- No automatic backup, access control, at-rest encryption, or scheduled reminder delivery.
- Dates are calendar dates without time zones; `overdue` uses the explicitly provided `--as-of`.
- JSON format is read-compatible with the Phase 9 baseline; writing a task does not rewrite legacy rows unless completing them.


## Phase 9B.3: task search

Search task titles, ignoring case, for a substring. Results include both completed and open tasks.

```bash
python3 -m src.cli --store /tmp/phase9b-tasks.json search --query review
python3 -m src.cli --store /tmp/phase9b-tasks.json search --query=-x   # use = when the query starts with '-'
```

- Matching is literal: `.`, `*`, `(`, `\`, `%` and similar characters match only themselves.
- Case is compared with `str.casefold()`, so `STRASSE` matches `Straße`. Locale-specific rules, such as Turkish dotted/dotless I, are not applied.
- Results come back in stored file order, the same order as `list`. No match prints `[]` and exits 0.
- An empty or whitespace-only query, or a corrupt store, prints `error: …` and exits 2.
- Search is read-only and never rewrites the store. The JSON schema is unchanged.

See [the task-search contract](docs/task-search-contract.md) and the red and green evidence files in `docs/`.

## Phase 9B.2 — external validation readiness

`.github/workflows/verify.yml` is a proposed read-only verification workflow. Its presence **does not** mean GitHub rulesets or deployment IAM are configured. Run `python3 tools/validate_repo_policy.py` and `python3 -m unittest discover -s tests -v` locally. For real GitHub evidence follow [the field-validation procedure](docs/github-field-validation.md), and for actual coding-agent runtime checks use [the sandbox trial protocol](docs/coding-agent-field-test.md). All human approvals remain unsigned and pending.
