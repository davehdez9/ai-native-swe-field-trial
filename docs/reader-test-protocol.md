# Independent reader usability protocol — NOT EXECUTED

**Purpose:** Test whether a person unfamiliar with the author can use the actual task tracker and Phase 9B stage contract without guidance. This is a future study, not completed evidence.

**Preparation:** Give the reader `README.md`, the repository, and a clean Python 3.11+ environment. Do not give walkthrough hints. Ask for no real customer/sensitive data. Record participant consent if collecting screen/audio recordings; do not collect identifiable logs unnecessarily.

**Tasks (record pass/fail, time, errors, and whether hints were needed):**
1. Locate the task contract and explain the feature's acceptance requirements in their own words.
2. Run all tests using the README's command and find the current implementation Git commit.
3. With a temporary store, add a task due on 2026-11-17 and find it via `overdue --as-of 2026-11-18`.
4. Mark the task complete and verify it is no longer overdue.
5. Add an impossible date (`2026-02-30`) and confirm the command fails without adding a task.
6. Identify whether this project has authorization for production deployment and who must approve engineering acceptance.

**Success threshold (proposed, not achieved):** reader completes all six without hints, identifies absent human approval, and no real data leaves the device. A failure triggers documentation rework and a re-test with a new reader.

| Item | Observation |
|---|---|
| Reader pseudonym | NOT TESTED |
| Date | NOT TESTED |
| Tasks passed | NOT TESTED |
| Hints/interventions | NOT TESTED |
| Reader-reported confusion | NOT TESTED |
| Independent judgment | PENDING |
