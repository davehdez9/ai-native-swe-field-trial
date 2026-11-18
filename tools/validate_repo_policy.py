"""Small fail-closed *static* CI policy checker; not a GitHub ruleset verifier."""
from pathlib import Path
import re, sys

REPO = Path(__file__).resolve().parents[1]
CHECKOUT = 'actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683'
PYTHON = 'actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065'

def verify_workflow(text):
    issues=[]
    # Static checks are not a YAML/security parser; they check the supplied template contract.
    required = {
        'check out using a reviewed SHA': CHECKOUT,
        'set up Python using a reviewed SHA': PYTHON,
        'no checkout credentials': 'persist-credentials: false',
        'read-only token': 'contents: read',
        'pull request trigger': 'pull_request:',
        'merge queue trigger': 'merge_group:',
        'run tests': 'python3 -m unittest discover -s tests -v',
        'run policy checker': 'python3 tools/validate_repo_policy.py',
    }
    for desc,token in required.items():
        if token not in text: issues.append('missing '+desc)
    # Remove comment-only lines before forbidden-condition checks.
    effective='\n'.join(line for line in text.splitlines() if not line.lstrip().startswith('#'))
    forbidden = [r'(?m)^\s*pull_request_target\s*:',r'(?m)^\s*workflow_run\s*:',r'(?m)^\s*id-token\s*:\s*write\b',r'(?m)^\s*contents\s*:\s*write\b',r'(?m)^\s*deployments\s*:\s*write\b',r'\bsecrets\.',r'(?m)^\s*environment\s*:']
    for pat in forbidden:
        if re.search(pat,effective,re.I): issues.append('forbidden workflow setting: '+pat)
    # Allow exact 40 hex action revisions only and disallow extension actions.
    for action in re.findall(r'(?m)^\s*uses:\s*([^\s#]+)',effective):
        if action not in (CHECKOUT,PYTHON): issues.append('unreviewed action: '+action)
    return issues

def main():
    issues=verify_workflow((REPO/'.github/workflows/verify.yml').read_text())
    if issues:
        for issue in issues: print('BLOCKED:',issue)
        return 1
    print('PASS: local workflow-template checks only; live protection remains unverified')
    return 0
if __name__=='__main__': sys.exit(main())
