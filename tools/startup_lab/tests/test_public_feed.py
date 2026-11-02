import json
import tempfile
import unittest
from pathlib import Path
from startup_lab.public_feed import build

class FeedTests(unittest.TestCase):
    def test_empty_feed(self):
        with tempfile.TemporaryDirectory() as directory:
            r=build(directory)
            self.assertEqual(r["count"],0)
            self.assertEqual(r["dataset_status"],"provisional_only")
    def test_cited_signal(self):
        with tempfile.TemporaryDirectory() as directory:
            folder=Path(directory)/"data"/"provisional";folder.mkdir(parents=True)
            r={"id":"one","title":"A problem","domain":"Developer Tools",
               "problem":"Something is difficult","source_url":"https://example.org/source",
               "source_locator":"comment","observed_at":"2026-11-03",
               "review_state":"ai_source_read_only","human_reviewed":False,
               "limitations":["single source"]}
            (folder/"one.json").write_text(json.dumps(r))
            self.assertEqual(build(directory)["signals"][0]["source_locator"],"comment")
    def test_approved_flag_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            folder=Path(directory)/"data"/"provisional";folder.mkdir(parents=True)
            (folder/"bad.json").write_text(json.dumps({"human_reviewed":True,"review_state":"approved"}))
            with self.assertRaises(ValueError):build(directory)
if __name__=="__main__":unittest.main()
