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
