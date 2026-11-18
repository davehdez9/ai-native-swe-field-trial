import unittest,tempfile
from pathlib import Path
from src.tracker import TaskStore
class TrackerTests(unittest.TestCase):
    def setUp(self): self.tmp=tempfile.TemporaryDirectory();self.path=Path(self.tmp.name)/'tasks.json';self.store=TaskStore(self.path)
    def tearDown(self): self.tmp.cleanup()
    def test_create_persist(self):
        self.store.add('T1','Review');self.assertEqual(TaskStore(self.path).load()[0]['title'],'Review')
    def test_mark_done(self):
        self.store.add('T1','Review');self.store.complete('T1');self.assertTrue(self.store.load()[0]['done'])
    def test_duplicate_denied(self):
        self.store.add('T1','Review')
        with self.assertRaises(ValueError): self.store.add('T1','Again')
    def test_missing_title_denied(self):
        with self.assertRaises(ValueError): self.store.add('T1','')
    def test_missing_task_denied(self):
        with self.assertRaises(KeyError): self.store.complete('nope')
    def test_corrupt_data_denied(self):
        self.path.write_text('{broken')
        with self.assertRaises(ValueError): self.store.load()
if __name__=='__main__':unittest.main()
