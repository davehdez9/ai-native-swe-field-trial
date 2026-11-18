import unittest,tempfile,json,os
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

class SearchTests(unittest.TestCase):
    """Task-search contract (docs/task-search-contract.md, AC-S1..AC-S7)."""
    def setUp(self): self.tmp=tempfile.TemporaryDirectory();self.path=Path(self.tmp.name)/'tasks.json';self.store=TaskStore(self.path)
    def tearDown(self): self.tmp.cleanup()
    def ids(self,rows): return [r['id'] for r in rows]
    def seed(self):
        self.store.add('T1','Review plan');self.store.add('T2','Buy milk');self.store.add('T3','review PR')

    # AC-S1
    def test_search_substring_match(self):
        self.seed();self.assertEqual(self.ids(self.store.search('review')),['T1','T3'])
    def test_search_case_insensitive(self):
        self.seed()
        for q in ('REVIEW','ReViEw','review'):
            with self.subTest(q=q): self.assertEqual(self.ids(self.store.search(q)),['T1','T3'])
    def test_search_unicode_casefold(self):
        self.store.add('U1','Straße');self.store.add('U2','CAFÉ')
        self.assertEqual(self.ids(self.store.search('STRASSE')),['U1'])
        self.assertEqual(self.ids(self.store.search('café')),['U2'])
    def test_search_partial_and_full_title(self):
        self.seed()
        self.assertEqual(self.ids(self.store.search('view')),['T1','T3'])
        self.assertEqual(self.ids(self.store.search('k')),['T2'])
        self.assertEqual(self.ids(self.store.search('Buy milk')),['T2'])

    # AC-S2
    def test_search_includes_completed_and_incomplete(self):
        self.seed();self.store.complete('T1')
        rows=self.store.search('review')
        self.assertEqual([(r['id'],r['done']) for r in rows],[('T1',True),('T3',False)])
    def test_search_legacy_row_without_due_date(self):
        self.path.write_text(json.dumps([{'id':'legacy','title':'Old review','done':False}]))
        rows=self.store.search('REVIEW')
        self.assertEqual(self.ids(rows),['legacy']);self.assertNotIn('due_date',rows[0])

    # AC-S3
    def test_search_does_not_modify_file(self):
        self.seed()
        before=self.path.read_bytes();mtime=os.stat(self.path).st_mtime_ns
        for q in ('review','zzz','Buy'): self.store.search(q)
        self.assertEqual(self.path.read_bytes(),before)
        self.assertEqual(os.stat(self.path).st_mtime_ns,mtime)
        self.assertFalse(self.path.with_suffix('.json.tmp').exists())
    def test_search_rows_unchanged_by_search(self):
        self.seed();before=self.store.load();self.store.search('review')
        self.assertEqual(self.store.load(),before)

    # AC-S4
    def test_search_preserves_stored_order(self):
        for i in ('C','A','B'): self.store.add(i,'Task '+i)
        self.assertEqual(self.ids(self.store.search('task')),['C','A','B'])
        self.assertEqual(self.ids(self.store.search('task')),['C','A','B'])
    def test_search_returns_stored_shape(self):
        self.store.add('D1','Dated review','2026-12-01')
        self.assertEqual(self.store.search('review'),self.store.load())
        self.assertEqual(self.store.search('review')[0]['due_date'],'2026-12-01')

    # AC-S5
    def test_search_special_characters_literal(self):
        self.store.add('S1','abc');self.store.add('S2','fix (x)');self.store.add('S3','anything');self.store.add('S4','list [a]')
        self.assertEqual(self.store.search('a.c'),[])
        self.assertEqual(self.ids(self.store.search('(x)')),['S2'])
        self.assertEqual(self.store.search('.*'),[])
        self.assertEqual(self.ids(self.store.search('[a]')),['S4'])
    def test_search_backslash_and_percent_literal(self):
        self.store.add('P1','path C:\\tmp here');self.store.add('P2','C:/tmp');self.store.add('P3','done 100%');self.store.add('P4','100 percent')
        self.assertEqual(self.ids(self.store.search('C:\\tmp')),['P1'])
        self.assertEqual(self.ids(self.store.search('100%')),['P3'])

    # AC-S6
    def test_search_empty_query_rejected(self):
        self.seed()
        for q in ('','   ','\t\n'):
            with self.subTest(q=q), self.assertRaises(ValueError): self.store.search(q)
    def test_search_invalid_query_type_rejected(self):
        self.seed()
        for q in (None,12,b'x',['x']):
            with self.subTest(q=q), self.assertRaises(TypeError): self.store.search(q)
    def test_search_query_not_stripped(self):
        self.store.add('T1','Review plan');self.store.add('T2','a b')
        self.assertEqual(self.ids(self.store.search(' plan')),['T1'])
        self.assertEqual(self.store.search('a  b'),[])

    # AC-S7
    def test_search_missing_store_returns_empty(self):
        self.assertEqual(self.store.search('anything'),[]);self.assertFalse(self.path.exists())
    def test_search_no_match_returns_empty(self):
        self.seed();self.assertEqual(self.store.search('zzz'),[])
    def test_search_corrupt_json_rejected_without_rewrite(self):
        self.path.write_text('{broken')
        with self.assertRaises(ValueError): self.store.search('x')
        self.assertEqual(self.path.read_text(),'{broken')
    def test_search_invalid_record_rejected_without_rewrite(self):
        original='[{"id":"x","title":"hi","done":"yes"}]';self.path.write_text(original)
        with self.assertRaises(ValueError): self.store.search('hi')
        self.assertEqual(self.path.read_text(),original)

if __name__=='__main__':unittest.main()
