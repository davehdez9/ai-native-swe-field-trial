import json,subprocess,sys,tempfile,unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
class CLITests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.store=Path(self.temp.name)/'tasks.json'
    def tearDown(self): self.temp.cleanup()
    def call(self,*args):
        return subprocess.run([sys.executable,'-m','src.cli','--store',str(self.store),*args], cwd=ROOT, text=True,capture_output=True)
    def test_add_list_overdue_complete(self):
        a=self.call('add','--id','T1','--title','First','--due','2026-11-16')
        self.assertEqual(a.returncode,0,a.stderr)
        self.assertEqual(json.loads(a.stdout)['id'],'T1')
        b=self.call('list'); self.assertEqual(len(json.loads(b.stdout)),1)
        c=self.call('overdue','--as-of','2026-11-18')
        self.assertEqual([r['id'] for r in json.loads(c.stdout)],['T1'])
        d=self.call('complete','--id','T1');self.assertEqual(d.returncode,0,d.stderr)
        self.assertEqual(json.loads(self.call('overdue','--as-of','2026-11-18').stdout),[])
    def test_bad_date_exit_nonzero_and_no_file(self):
        p=self.call('add','--id','T1','--title','Test','--due','2026-02-30')
        self.assertNotEqual(p.returncode,0)
        self.assertFalse(self.store.exists())

    # Task search, AC-S8 (docs/task-search-contract.md)
    def seed(self):
        for i,t in (('T1','Review plan'),('T2','Buy milk'),('T3','review PR')):
            self.assertEqual(self.call('add','--id',i,'--title',t).returncode,0)
    def test_cli_search_returns_matches(self):
        self.seed();self.assertEqual(self.call('complete','--id','T1').returncode,0)
        p=self.call('search','--query','REVIEW')
        self.assertEqual(p.returncode,0,p.stderr)
        rows=json.loads(p.stdout)
        self.assertEqual([(r['id'],r['done']) for r in rows],[('T1',True),('T3',False)])
    def test_cli_search_no_match_empty_array(self):
        self.seed();p=self.call('search','--query','zzz')
        self.assertEqual(p.returncode,0,p.stderr);self.assertEqual(json.loads(p.stdout),[])
    def test_cli_search_missing_store_empty_array(self):
        p=self.call('search','--query','x')
        self.assertEqual(p.returncode,0,p.stderr);self.assertEqual(json.loads(p.stdout),[])
        self.assertFalse(self.store.exists())
    def test_cli_search_empty_query_error(self):
        self.seed();p=self.call('search','--query','')
        self.assertEqual(p.returncode,2);self.assertTrue(p.stderr.startswith('error:'),p.stderr);self.assertEqual(p.stdout,'')
    def test_cli_search_missing_query_arg(self):
        p=self.call('search');self.assertEqual(p.returncode,2)
        self.assertIn('--query',p.stderr)
    def test_cli_search_dash_prefixed_query(self):
        self.assertEqual(self.call('add','--id','T1','--title=fix -x').returncode,0)
        p=self.call('search','--query=-x')
        self.assertEqual(p.returncode,0,p.stderr);self.assertEqual([r['id'] for r in json.loads(p.stdout)],['T1'])
    def test_cli_search_corrupt_store_error(self):
        self.store.write_text('{broken');p=self.call('search','--query','x')
        self.assertEqual(p.returncode,2);self.assertTrue(p.stderr.startswith('error:'),p.stderr)
        self.assertEqual(self.store.read_text(),'{broken')
    def test_cli_overdue_unaffected_by_search(self):
        self.assertEqual(self.call('add','--id','T1','--title','Late','--due','2026-11-16').returncode,0)
        s=self.call('search','--query','late')
        self.assertEqual(s.returncode,0,s.stderr);self.assertEqual([r['id'] for r in json.loads(s.stdout)],['T1'])
        o=self.call('overdue','--as-of','2026-11-18')
        self.assertEqual(o.returncode,0,o.stderr);self.assertEqual([r['id'] for r in json.loads(o.stdout)],['T1'])
