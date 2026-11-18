# GitHub field trial — human-operated procedure (Phase 9B.2)

**State: NOT EXECUTED.** This file is a reproducible field procedure, not evidence of a configured GitHub repository.

## 1. Publish safely
1. Create a fresh **test-only** GitHub repository without production credentials, customer data or deployments.
2. Invite a real reviewer with repository access. Record that person's approval outside the source-controlled PR content.
3. Push the `phase9b2-review-readiness` branch, open a PR targeting `main` using ordinary GitHub UI.
4. Confirm `.github/workflows/verify.yml` triggers read-only validation on PR. Do not enable untrusted PR write tokens, `pull_request_target`, workflow self-approval or any deploy job.

## 2. Independently protect the target branch
A repository admin must configure a main-branch ruleset/branch protection with pull requests required, at least one qualified human reviewer distinct from author, stale review dismissal, last-push approval, required named CI job **pilot-policy-and-tests**, checks from approved GitHub Apps, no force-push/deletion and no bypass for ordinary actors. Rulesets and protected environments must be verified separately; a repository file cannot install or enforce these settings. Confirm plan/repository support in GitHub settings.

## 3. Collect evidence
- PR URL and exact head SHA, checks page, code diff and run logs.
- Red/green local Git history and clean working tree.
- Reviewer comments, approvals, final merge decision and review-time estimates.
- Run `GH_TOKEN=... python3 tools/github_readonly_audit.py --owner OWNER --repo REPO --pull NUMBER` from a secured workstation using a **read-only** token scoped appropriately. Never commit token or raw API JSON. The checker reports **observations only**, never permission to merge/deploy.
- Confirm by direct UI inspection the branch's *effective* rulesets, bypass list, actor identities and security policies; the included checker does not exhaustively verify these.

## 4. Mandatory negative scenarios (separate throwaway PRs)
- Missing/failed CI: PR must not merge.
- No independent reviewer: PR must not merge.
- Additional push after approval: require fresh approval.
- Attempt to change `.github/workflows/verify.yml` and `tools/validate_repo_policy.py`: protected review/check must still prevent unreviewed bypass.
- Fork PR or untrusted content: inspect run permissions; no access to sensitive secrets or writable tokens.
- Attempt to push directly to protected `main` by ordinary contributor: server must deny.

**Do not do actual production deploy or touch live user data in this trial.**

## 5. Exit criteria
Collect independent screenshots/logs with precise times and repository details redacted as needed. Mark `PASS` only after a separate human owner reviews the evidence. If protection API data is unavailable, record `BLOCKED/NOT VERIFIED`, not success.
