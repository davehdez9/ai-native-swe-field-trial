import unittest
from tools.github_readonly_audit import check_payload
from tools.validate_repo_policy import verify_workflow, REPO
SHA='a'*40
def fixtures():
    b={'required_status_checks':{'checks':[{'context':'pilot-policy-and-tests','app_id':15368}]},
       'required_pull_request_reviews':{'required_approving_review_count':1,'dismiss_stale_reviews':True,'require_last_push_approval':True},
       'enforce_admins':{'enabled':True},'allow_force_pushes':{'enabled':False},'allow_deletions':{'enabled':False}}
    p={'state':'open','draft':False,'head':{'sha':SHA},'user':{'login':'developer'}}
    rev=[{'user':{'login':'peer','type':'User'},'commit_id':SHA,'state':'APPROVED'}]
    checks={'check_runs':[{'name':'pilot-policy-and-tests','head_sha':SHA,'status':'completed','conclusion':'success','app':{'slug':'github-actions'}}]}
    return b,p,rev,checks
class ExternalReadinessTests(unittest.TestCase):
    def test_baseline_observation(self):self.assertEqual(check_payload(*fixtures()),[])
    def test_missing_required_check(self):
        b,p,r,c=fixtures();b['required_status_checks']['checks']=[]
        self.assertTrue(check_payload(b,p,r,c))
    def test_missing_human_review(self):
        b,p,r,c=fixtures();r.clear();self.assertTrue(check_payload(b,p,r,c))
    def test_self_approved(self):
        b,p,r,c=fixtures();r[0]['user']['login']='developer';self.assertTrue(check_payload(b,p,r,c))
    def test_stale_review_commit(self):
        b,p,r,c=fixtures();r[0]['commit_id']='b'*40;self.assertTrue(check_payload(b,p,r,c))
    def test_failed_check(self):
        b,p,r,c=fixtures();c['check_runs'][0]['conclusion']='failure';self.assertTrue(check_payload(b,p,r,c))
    def test_agent_reported_check(self):
        b,p,r,c=fixtures();c['check_runs'][0]['app']['slug']='custom-agent';self.assertTrue(check_payload(b,p,r,c))
    def test_force_push_enabled(self):
        b,p,r,c=fixtures();b['allow_force_pushes']['enabled']=True;self.assertTrue(check_payload(b,p,r,c))
    def test_missing_branch_protection(self):self.assertTrue(check_payload({}, {}, [], {}))
    def test_draft_pr(self):
        b,p,r,c=fixtures();p['draft']=True;self.assertTrue(check_payload(b,p,r,c))
    def test_stale_review_rule_missing(self):
        b,p,r,c=fixtures();b['required_pull_request_reviews']['dismiss_stale_reviews']=False;self.assertTrue(check_payload(b,p,r,c))
    def test_required_last_push_missing(self):
        b,p,r,c=fixtures();b['required_pull_request_reviews']['require_last_push_approval']=False;self.assertTrue(check_payload(b,p,r,c))
    def test_policy_file_pass(self):
        t=(REPO/'.github/workflows/verify.yml').read_text();self.assertEqual(verify_workflow(t),[])
    def test_policy_detects_write_privilege(self):
        t=(REPO/'.github/workflows/verify.yml').read_text();self.assertTrue(verify_workflow(t+'\npermissions:\n  contents: write\n'))
    def test_policy_detects_unpinned_action(self):
        t=(REPO/'.github/workflows/verify.yml').read_text();self.assertTrue(verify_workflow(t.replace('actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803','actions/checkout@v4')))
    def test_policy_detects_pr_target(self):
        t=(REPO/'.github/workflows/verify.yml').read_text();self.assertTrue(verify_workflow(t+'\npull_request_target:\n'))
