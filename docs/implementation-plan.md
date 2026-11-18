# Implementation plan — P9B-001

1. Commit acceptance criteria and negative tests without changing the baseline code. Record expected failures.
2. Add strict date normalization and overdue query without breaking old records.
3. Add argparse CLI commands with JSON output and controlled nonzero errors.
4. Run legacy and new tests, CLI smoke, source tree diff and safe backup/restore.
5. Save exact commit, test evidence and limitations in the handoff. Do not claim real-world approval.
