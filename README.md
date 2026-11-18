# Phase 9B field-pilot: personal task tracker

A locally version-controlled, Python standard-library application. This is an **author-driven AI-assisted local integration pilot**, not an independent real coding-agent execution or a customer validation study.

Phase 9 baseline is commit `baseline`; Phase 9B change adds due dates, overdue filtering and a tiny CLI. Reproduce tests with:

```bash
python3 -m unittest discover -s tests -v
python3 -m src.cli --store /tmp/phase9b-tasks.json add --id T1 --title 'Review plan' --due 2026-12-01
python3 -m src.cli --store /tmp/phase9b-tasks.json overdue --as-of 2026-12-02
```

No cloud services, API credentials or production deployment. See `docs/` for task contract and evidence. `AGENTS.md` is written guidance **only**, not an enforceable sandbox. Git history contains baseline, test-first red commit, and green implementation.
