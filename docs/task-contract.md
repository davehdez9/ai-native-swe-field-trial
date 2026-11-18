# Task contract — P9B-001 / revision 1

- **Origin:** Phase 9 profile B `personal-task-tracker`; source at the preserved Phase 9 RC1 tag.
- **Problem (hypothesis, not user validated):** A local user wants to identify unfinished tasks whose due date has passed.
- **Goal:** add optional due dates and a deterministic overdue view, preserving previous JSON data.
- **Allowed work:** tracker library; command-line interface; tests; this pilot's documentation.
- **Not authorized:** production, personal/sensitive datasets, network calls, package installation, live agent tools, independent human approval.
- **AC-01:** Existing JSON tasks without `due_date` still load; legacy add/complete behavior remains.
- **AC-02:** Due date is optional; valid dates must match strict ISO `YYYY-MM-DD`; impossible dates fail without saving.
- **AC-03:** Overdue returns only unfinished dated tasks with date **strictly before** a caller-supplied reference date. Return IDs sorted by due date and then ID; no wall-clock dependency.
- **AC-04:** Invalid or malformed files fail predictably; no silent rewrite on read failure.
- **AC-05:** CLI supports `add`, `complete`, `list`, `overdue`; no network, stdout JSON on success, nonzero on errors.
- **AC-06:** Tests define negative and backward-compatibility cases before code change; capture red and green results against Git revisions.
- **Completion:** ready for human review once local tests and static boundary checks pass; acceptance and release remain separately authorized.
