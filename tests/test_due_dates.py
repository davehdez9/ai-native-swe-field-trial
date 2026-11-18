import json
import tempfile
import unittest
from pathlib import Path
from src.tracker import TaskStore

class DueDateContractTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.path = Path(self.dir.name) / 'tasks.json'
        self.store = TaskStore(self.path)
    def tearDown(self): self.dir.cleanup()

    def test_legacy_rows_read_and_query(self):
        self.path.write_text(json.dumps([{'id':'legacy','title':'Old','done':False}]))
        self.assertEqual(self.store.overdue('2026-11-18'), [])
        self.store.complete('legacy')
        self.assertTrue(self.store.load()[0]['done'])

    def test_date_optional_and_preserved(self):
        self.store.add('T1','One')
        self.store.add('T2','Two','2026-11-17')
        rows=self.store.load()
        self.assertIsNone(rows[0].get('due_date'))
        self.assertEqual(rows[1]['due_date'],'2026-11-17')

    def test_sort_boundary_and_completed(self):
        self.store.add('B','Later','2026-11-17')
        self.store.add('A','Earlier','2026-11-16')
        self.store.add('C','Current','2026-11-18')
        self.store.add('D','Done','2026-11-15')
        self.store.complete('D')
        self.assertEqual([r['id'] for r in self.store.overdue('2026-11-18')],['A','B'])
        self.assertEqual([r['id'] for r in self.store.overdue('2026-11-17')],['A'])

    def test_invalid_date_refused_without_write(self):
        for due in ('2026-2-03','2026-02-30','2026/03/04','2026-13-01','',12):
            with self.subTest(due=due), self.assertRaises((TypeError,ValueError)):
                self.store.add('bad','Wrong',due)
        self.assertFalse(self.path.exists())

    def test_invalid_reference_date_refused(self):
        with self.assertRaises(ValueError): self.store.overdue('2026-02-30')

    def test_invalid_row_is_not_silently_rewritten(self):
        original='[{"id":"x","title":"hi","done":"yes"}]'
        self.path.write_text(original)
        with self.assertRaises(ValueError): self.store.overdue('2026-11-18')
        self.assertEqual(self.path.read_text(),original)

    def test_duplicate_id_still_denied_with_due_dates(self):
        self.store.add('x','Initial','2026-11-17')
        with self.assertRaises(ValueError): self.store.add('x','Duplicate','2026-11-18')
