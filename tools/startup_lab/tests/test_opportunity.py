import csv
import json
import tempfile
import unittest
from pathlib import Path
from startup_lab.opportunity import discover,explore

class OpportunityTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.root=Path(self.temp.name)
        (self.root/"data"/"needs").mkdir(parents=True)
        (self.root/"data"/"evidence").mkdir(parents=True)
        (self.root/"index").mkdir()
        (self.root/"index"/"products.csv").write_text("slug,name,website,category\nitem-a,Example A,https://example.org/a,productivity\n")
        self.need={"id":"need-001","title":"Invoice reconciliation","domain":"finance",
                   "user_segment":"freelancers","problem":"Manual invoice tracking takes time",
                   "evidence_ids":["ev-001","ev-absent"],"product_ids":["item-a","item-unknown"]}
        (self.root/"data"/"needs"/"need-001.json").write_text(json.dumps(self.need))
        ev={"id":"ev-001","statement":"Freelancers report invoice tracking difficulties",
            "source_url":"https://example.org/fixture","observed_at":"2026-11-03",
            "evidence_type":"user-report","direction":"support"}
        (self.root/"data"/"evidence"/"ev-001.json").write_text(json.dumps(ev))
    def tearDown(self):self.temp.cleanup()
    def test_discover(self):
        r=discover(self.root,"invoice")
        self.assertEqual(r["total"],1)
        self.assertEqual(r["cards"][0]["status"],"unverified_links")
    def test_discover_no_match(self):
        self.assertEqual(discover(self.root,"saxophone")["total"],0)
    def test_explore_links(self):
        r=explore(self.root,"need-001")
        self.assertEqual(r["missing_evidence_ids"],["ev-absent"])
        self.assertEqual(r["missing_product_ids"],["item-unknown"])
        self.assertEqual(len(r["evidence"]["support"]),1)
    def test_unknown_need(self):
        with self.assertRaises(ValueError):explore(self.root,"absent")
    def test_no_need_no_invention(self):
        (self.root/"data"/"needs"/"need-001.json").unlink()
        self.assertEqual(discover(self.root)["total"],0)
if __name__=="__main__":unittest.main()
