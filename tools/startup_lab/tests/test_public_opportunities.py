import json
import tempfile
import unittest
from pathlib import Path
from startup_lab.public_opportunities import discover_public,explore_public

class PublicOpportunitiesTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name);folder=self.root/"data"/"provisional";folder.mkdir(parents=True)
        self.signal={"id":"one","kind":"user_problem_signal","title":"Local CI debugging",
                     "domain":"Developer Tools","user_segment":"engineers",
                     "problem":"CI debugging requires repeated commits",
                     "source_url":"https://news.ycombinator.com/item?id=1","source_locator":"comment",
                     "review_state":"ai_source_read_only","human_reviewed":False,"limitations":["one comment"]}
        (folder/"one.json").write_text(json.dumps(self.signal))
    def tearDown(self):self.tmp.cleanup()
    def test_discovery(self):
        self.assertEqual(discover_public(self.root,"CI")["total"],1)
        self.assertEqual(discover_public(self.root,"gardening")["total"],0)
    def test_explore(self):
        self.assertFalse(explore_public(self.root,"one")["signal"]["human_reviewed"])
    def test_no_fictitious_records(self):
        (self.root/"data"/"provisional"/"one.json").unlink()
        self.assertEqual(discover_public(self.root)["total"],0)
    def test_wrong_review_state_rejected(self):
        self.signal["human_reviewed"]=True
        (self.root/"data"/"provisional"/"one.json").write_text(json.dumps(self.signal))
        with self.assertRaises(ValueError):discover_public(self.root)
if __name__=="__main__":unittest.main()
