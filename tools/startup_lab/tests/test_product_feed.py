import json
import tempfile
import unittest
from pathlib import Path
from startup_lab.product_feed import build

class ProductFeedTests(unittest.TestCase):
    def test_empty(self):
        with tempfile.TemporaryDirectory() as d:self.assertEqual(build(d)["products"],[])
    def test_observation_not_launch(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"data"/"products";p.mkdir(parents=True)
            (p/"x.json").write_text(json.dumps({"id":"x","name":"X","description":"demo","category":"tools","source_url":"https://example.org","source_type":"vendor","observed_at":"2026-11-03","date_precision":"unknown","verification_status":"provisional"}))
            item=build(d)["products"][0]
            self.assertEqual(item["observed_at"],"2026-11-03")
            self.assertIsNone(item["launch_date"])
    def test_bad_record_fails(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"data"/"products";p.mkdir(parents=True)
            (p/"x.json").write_text('{"name":"No source"}')
            with self.assertRaises(ValueError):build(d)
if __name__=="__main__":unittest.main()
