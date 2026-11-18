# Phase 9B local pilot observations

| ID | Observation | Disposition |
|---|---|---|
| P9B-F01 | The Phase 9 example had no user-operable CLI; a unit-test-only library is a weak reader usability test. | Mitigated locally with JSON CLI; independent reader study open. |
| P9B-F02 | Existing JSON lacks due date fields, requiring backward-compatible reads. | Covered with contract and regression tests. |
| P9B-F03 | A fixed `.tmp` filename plus read/modify/write is unsafe for concurrent writers; `Path.replace` is not sufficient concurrency control. | Explicit limitation; do not upgrade Profile B to multi-user without redesign. |
| P9B-F04 | User-provided paths and titles have no access-control or data-classification policy beyond local user permissions. | Local fictional use only; real-user data blocked pending review. |
| P9B-F05 | This environment has no `claude`, `codex`, or `cursor` executable, external CI identity, real reviewer, customer validation or actual monitoring. | Kept as blocker; do not claim real-agent/production proof. |
| P9B-F06 | `AGENTS.md` is advisory prose, not a trustworthy boundary. | Enforcement remains blocked pending actual sandboxed agent trial and attempted bypass tests. |
