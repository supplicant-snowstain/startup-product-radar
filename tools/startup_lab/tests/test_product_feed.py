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
    def test_story_is_preserved(self):
        with tempfile.TemporaryDirectory() as d:
            folder=Path(d)/"data"/"products";folder.mkdir(parents=True)
            story={"en":{"who":"A developer","pain":"Slow feedback","solution":"Faster tests","benefit":"Less waiting","uncertainty":"Who pays?"}}
            record={"id":"product-demo","name":"Demo","description":"Example","category":"Tools","source_url":"https://example.org","source_type":"vendor","observed_at":"2026-11-03","date_precision":"unknown","verification_status":"provisional","story":story}
            (folder/"demo.json").write_text(json.dumps(record))
            self.assertEqual(build(d)["products"][0]["story"],story)
    def test_new_launch_requires_dated_source(self):
        with tempfile.TemporaryDirectory() as d:
            directory=Path(d)/"data"/"products"
            directory.mkdir(parents=True)
            item={"id":"example","name":"Example","description":"Example product","category":"Tools",
                  "source_url":"https://example.org/product","source_type":"official",
                  "observed_at":"2026-11-03","date_precision":"unknown",
                  "verification_status":"provisional","collection":"new_launch"}
            file=directory/"example.json"
            file.write_text(json.dumps(item))
            with self.assertRaises(ValueError):
                build(d)
            item.update({"date_precision":"day","launch_date":"2026-11-02",
                         "launch_source_url":"https://example.org/release"})
            file.write_text(json.dumps(item))
            self.assertEqual(build(d)["products"][0]["collection"],"new_launch")
    def test_rejects_invalid_public_source_url(self):
        with tempfile.TemporaryDirectory() as d:
            folder=Path(d)/"data"/"products";folder.mkdir(parents=True)
            record={"id":"x","name":"X","description":"Demo","category":"Tools",
                    "source_url":"http://localhost/internal","source_type":"official",
                    "observed_at":"2026-11-03","date_precision":"unknown",
                    "verification_status":"provisional"}
            (folder/"x.json").write_text(json.dumps(record))
            with self.assertRaises(ValueError):build(d)
    def test_rejects_impossible_observation_date(self):
        with tempfile.TemporaryDirectory() as d:
            folder=Path(d)/"data"/"products";folder.mkdir(parents=True)
            record={"id":"x","name":"X","description":"Demo","category":"Tools",
                    "source_url":"https://example.org","source_type":"official",
                    "observed_at":"2026-02-30","date_precision":"unknown",
                    "verification_status":"provisional"}
            (folder/"x.json").write_text(json.dumps(record))
            with self.assertRaises(ValueError):build(d)
    def test_bad_record_fails(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"data"/"products";p.mkdir(parents=True)
            (p/"x.json").write_text('{"name":"No source"}')
            with self.assertRaises(ValueError):build(d)
if __name__=="__main__":unittest.main()
