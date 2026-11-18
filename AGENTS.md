# Task boundary (documentation, not a technical sandbox)

- Allowed implementation targets: `src/tracker.py`, `src/cli.py`, `tests/test_tracker.py`, `tests/test_cli.py`, `README.md` and `docs/`.
- No network, cloud credentials, production deploy, destructive file operations, external dependencies or unreviewed merges.
- Run `python3 -m unittest discover -s tests -v` and record actual stdout/exit status.
- A passing local test is not human or external CI approval. Escalate schema changes that are not backward compatible.
