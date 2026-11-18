"""Read-only GitHub API *observational* audit. Never authorizes merging/deployment.

Requires GH_TOKEN from a secure local environment, not a file or CLI argument.
A 403/404 is BLOCKED/UNKNOWN (could be plan, permission or protection mode).
RuleSET-only repos require additional manual confirmation: this audits branch protection API.
"""
import argparse, json, os, re, sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import quote

SAFE_NAME=re.compile(r'^[A-Za-z0-9_.-]{1,100}$')
EXPECTED='pilot-policy-and-tests'
def check_payload(branch,pr,reviews,runs,expected=EXPECTED):
    issues=[]
    if not isinstance(branch,dict) or not isinstance(pr,dict): return ['missing branch or PR data']
    status=branch.get('required_status_checks') or {}
    checks=status.get('checks') or []
    contexts=set(status.get('contexts') or [])
    contexts.update(x.get('context') for x in checks if isinstance(x,dict))
    if expected not in contexts: issues.append('expected check not required by branch protection')
    review_rule=branch.get('required_pull_request_reviews') or {}
    if review_rule.get('required_approving_review_count',0)<1: issues.append('one human reviewer not required')
    if review_rule.get('dismiss_stale_reviews') is not True: issues.append('stale reviews not dismissed')
    if review_rule.get('require_last_push_approval') is not True: issues.append('last push approval not required')
    if (branch.get('enforce_admins') or {}).get('enabled') is not True: issues.append('admins not enforced by branch protection')
    for key in ('allow_force_pushes','allow_deletions'):
        if (branch.get(key) or {}).get('enabled') is not False: issues.append(key+' not explicitly disabled')
    if pr.get('state')!='open': issues.append('PR is not open')
    if pr.get('draft',True): issues.append('PR is draft')
    sha=((pr.get('head') or {}).get('sha') or '')
    actor=((pr.get('user') or {}).get('login') or '').lower()
    if not re.fullmatch('[0-9a-f]{40}',sha): issues.append('head SHA missing or malformed')
    # GitHub API returns timeline of reviews; use last per user, and ensure after commit/push.
    latest={}
    for item in reviews if isinstance(reviews,list) else []:
        who=((item.get('user') or {}).get('login') or '').lower()
        if who: latest[who]=item
    valid=[v for k,v in latest.items() if k!=actor and v.get('state')=='APPROVED' and v.get('commit_id')==sha and (v.get('user') or {}).get('type')=='User']
    if not valid: issues.append('no distinct human approval tied to current head SHA')
    matching=[x for x in (runs.get('check_runs') or []) if x.get('name')==expected and x.get('head_sha')==sha and (x.get('app') or {}).get('slug')=='github-actions']
    if not any(x.get('status')=='completed' and x.get('conclusion')=='success' for x in matching): issues.append('required GitHub Actions check not successful for PR head SHA')
    # Even a clean observation cannot prove bypass resistance or authorize deployment.
    return issues

def api_get(path,token):
    req=Request('https://api.github.com'+path,headers={
        'Accept':'application/vnd.github+json','Authorization':'Bearer '+token,
        'X-GitHub-Api-Version':'2022-11-28','User-Agent':'ai-swe-phase9b2-readonly-audit'})
    with urlopen(req,timeout=15) as response: return json.load(response)

def main(argv=None):
    parser=argparse.ArgumentParser(description='Read-only GitHub protection & PR observation')
    parser.add_argument('--owner',required=True)
    parser.add_argument('--repo',required=True)
    parser.add_argument('--branch',default='main')
    parser.add_argument('--pull',required=True,type=int)
    args=parser.parse_args(argv)
    if not all(SAFE_NAME.fullmatch(s) for s in (args.owner,args.repo,args.branch)) or args.pull<1:
        print('BLOCKED: invalid repository/branch/PR identifier');return 2
    token=os.getenv('GH_TOKEN','')
    if not token:
        print('BLOCKED: GH_TOKEN not set; no authenticated GitHub evidence collected');return 2
    base='/repos/'+quote(args.owner,safe='')+'/'+quote(args.repo,safe='')
    try:
        branch=api_get(base+'/branches/'+quote(args.branch,safe='')+'/protection',token)
        pr=api_get(base+'/pulls/'+str(args.pull),token)
        reviews=api_get(base+'/pulls/'+str(args.pull)+'/reviews?per_page=100',token)
        head=(pr.get('head') or {}).get('sha','')
        if not re.fullmatch('[0-9a-f]{40}',head): raise ValueError('invalid PR head SHA')
        runs=api_get(base+'/commits/'+head+'/check-runs?per_page=100',token)
    except (HTTPError,URLError,OSError,ValueError,KeyError) as exc:
        print('BLOCKED: cannot obtain complete authenticated evidence:',type(exc).__name__)
        return 2
    issues=check_payload(branch,pr,reviews,runs)
    if issues:
        for issue in issues:print('BLOCKED:',issue)
        return 1
    print('OBSERVED: configured branch-protection, review and CI indicators present for',head)
    print('NOT VERIFIED: repository rulesets, bypass privileges, reviewer eligibility, complete paginated history, production IAM or deploy approval')
    print('NOT AUTHORIZED: merge or deployment')
    return 0
if __name__=='__main__':sys.exit(main())
