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


## Phase 9B.2 — external validation readiness

`.github/workflows/verify.yml` is a proposed read-only verification workflow. Its presence **does not** mean GitHub rulesets or deployment IAM are configured. Run `python3 tools/validate_repo_policy.py` and `python3 -m unittest discover -s tests -v` locally. For real GitHub evidence follow [the field-validation procedure](docs/github-field-validation.md), and for actual coding-agent runtime checks use [the sandbox trial protocol](docs/coding-agent-field-test.md). All human approvals remain unsigned and pending.
