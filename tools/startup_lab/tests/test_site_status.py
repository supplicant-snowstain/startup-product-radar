import json
import tempfile
import unittest
from pathlib import Path
from startup_lab.site_status import build

class SiteStatusTests(unittest.TestCase):
    def test_counts_and_not_launch_recency(self):
        with tempfile.TemporaryDirectory() as d:
            web=Path(d)
            (web/"products.json").write_text(json.dumps({"count":2,"products":[{"collection":"new_launch"},{"collection":"case_study"}]}))
            (web/"signals.json").write_text(json.dumps({"count":1,"signals":[{}]}))
            result=build(web,commit="abc",built_at="2026-11-03T00:00:00+00:00")
            self.assertEqual(result["dated_launches"],1)
            self.assertEqual(result["case_studies"],1)
            self.assertEqual(result["problem_signals"],1)
            self.assertEqual(result["commit_sha"],"abc")
    def test_bad_feed_fails(self):
        with tempfile.TemporaryDirectory() as d:
            web=Path(d)
            (web/"products.json").write_text(json.dumps({"count":2,"products":[]}))
            (web/"signals.json").write_text(json.dumps({"count":0,"signals":[]}))
            with self.assertRaises(ValueError):build(web)
if __name__=="__main__":unittest.main()
