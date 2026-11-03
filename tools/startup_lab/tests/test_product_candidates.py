import json
import tempfile
import unittest
from pathlib import Path
from startup_lab.product_candidates import stage

class CandidateTests(unittest.TestCase):
    def test_dedup_and_no_publication(self):
        with tempfile.TemporaryDirectory() as d:
            entry={"name":"A tool","source_url":"https://example.org/tool?utm_source=x","observed_at":"2026-11-03"}
            result=stage(d,[entry,{**entry,"source_url":"https://example.org/tool"}])
            self.assertEqual(len(result["created"]),1)
            self.assertEqual(len(result["duplicates"]),1)
            saved=json.loads((Path(d)/result["created"][0]).read_text())
            self.assertFalse(saved["source_checked"])
            self.assertIsNone(saved["launch_date"])
            self.assertFalse((Path(d)/"data"/"products").exists())
    def test_invalid_url(self):
        with tempfile.TemporaryDirectory() as d:
            r=stage(d,[{"name":"Oops","source_url":"http://localhost/private","observed_at":"2026-11-03"}])
            self.assertEqual(len(r["errors"]),1)
    def test_repeat_is_idempotent(self):
        with tempfile.TemporaryDirectory() as d:
            e={"name":"A","source_url":"https://example.org/a","observed_at":"2026-11-03"}
            stage(d,[e])
            self.assertEqual(len(stage(d,[e])["duplicates"]),1)
if __name__=="__main__":unittest.main()
