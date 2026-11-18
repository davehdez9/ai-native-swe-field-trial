# Task contract: task search by title (Phase 9B.3)

- **Problem (a hypothesis, not validated with users):** a local user wants to find a task by part of its title.
- **Goal:** a read-only, case-insensitive title substring search in `TaskStore` and the existing CLI. Existing data and behavior stay unchanged.
- **Allowed changes:** `src/tracker.py`, `src/cli.py`, `tests/test_tracker.py`, `tests/test_cli.py`, `README.md`; new files `docs/task-search-contract.md`, `docs/search-red-test-evidence.txt`, `docs/search-green-test-evidence.txt`.
- **Not authorized:** changes to `AGENTS.md`, `.github/`, `tools/`, existing governance documents or other tests; network access; dependencies; push, merge or deploy; production data; claiming human approval.

## Acceptance criteria
- **AC-S1:** `TaskStore.search(query)` returns the tasks whose `title` contains `query` as a substring. Both sides are compared with `str.casefold()`.
- **AC-S2:** Results include both done and not-done tasks, and legacy rows that have no `due_date`.
- **AC-S3:** Search is read-only. It never writes, and the file bytes and mtime stay the same. No schema change, so the change is backward compatible.
- **AC-S4:** Results come back in stored file order (the same as `list`), with rows exactly as stored.
- **AC-S5:** Matching is literal. Regex and glob characters match only themselves.
- **AC-S6:** A query that is not a `str` raises `TypeError`. An empty or whitespace-only query raises `ValueError`. Other queries are used as given, without stripping.
- **AC-S7:** A missing store gives `[]` and creates no file. A corrupt or invalid store raises `ValueError` and is not rewritten.
- **AC-S8:** `--store PATH search --query TEXT` prints a JSON array on stdout and exits 0, including `[]` when nothing matches. An invalid query or a corrupt store prints `error: …` on stderr and exits 2. Existing commands are unchanged.

## Test mapping
| AC | Tests |
|---|---|
| S1 | `test_search_substring_match`, `test_search_case_insensitive`, `test_search_unicode_casefold`, `test_search_partial_and_full_title` |
| S2 | `test_search_includes_completed_and_incomplete`, `test_search_legacy_row_without_due_date` |
| S3 | `test_search_does_not_modify_file`, `test_search_rows_unchanged_by_search` |
| S4 | `test_search_preserves_stored_order`, `test_search_returns_stored_shape` |
| S5 | `test_search_special_characters_literal`, `test_search_backslash_and_percent_literal` |
| S6 | `test_search_empty_query_rejected`, `test_search_invalid_query_type_rejected`, `test_search_query_not_stripped` |
| S7 | `test_search_missing_store_returns_empty`, `test_search_no_match_returns_empty`, `test_search_corrupt_json_rejected_without_rewrite`, `test_search_invalid_record_rejected_without_rewrite` |
| S8 | `test_cli_search_returns_matches`, `test_cli_search_no_match_empty_array`, `test_cli_search_missing_store_empty_array`, `test_cli_search_empty_query_error`, `test_cli_search_missing_query_arg`, `test_cli_search_dash_prefixed_query`, `test_cli_search_corrupt_store_error`, `test_cli_overdue_unaffected_by_search`; the existing CLI tests also run as regression checks |

## Status
- Sandbox enforcement: **NOT VERIFIED.** A worktree, AGENTS.md and loaded settings are not proof that writes or network are actually denied. That needs separate boundary tests.
- Human review: **PENDING**. External CI: **NOT RUN**. Local green tests are not approval.
