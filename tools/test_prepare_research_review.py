import csv
import json
import tempfile
import unittest
from pathlib import Path

from prepare_research_review import validate_export, prepare

FIELDS = ("job", "workflow", "alternatives", "evidence", "counterevidence", "experiment")
def payload():
    return {
        "slug": "pending",
        "source_report": "reports/2026/11/2026-11-07.md",
        "review_status": "requires_maintainer_approval",
        "intelligence": {
            **{key: {"zh": "有来源的内容", "en": "Source-based content", "fr": "Contenu sourcé"} for key in FIELDS},
            "source_status": "editorial_review_pending",
        },
    }
class ReviewExportTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root/"index").mkdir()
        (self.root/"data").mkdir()
        (self.root/"reports/2026/11").mkdir(parents=True)
        (self.root/"reports/2026/11/2026-11-07.md").write_text("# Research",encoding="utf-8")
        (self.root/"data/research_intelligence.json").write_text('{"products":{}}',encoding="utf-8")
        with (self.root/"index/products.csv").open("w",newline="",encoding="utf-8") as f:
            w=csv.DictWriter(f,fieldnames=["slug","first_observed"])
            w.writeheader()
            w.writerow({"slug":"pending","first_observed":"2026-11-07"})
    def test_valid_candidate_does_not_mutate_canonical(self):
        original=(self.root/"data/research_intelligence.json").read_text()
        result=prepare(payload(),self.root)
        self.assertIn("pending",result["products"])
        self.assertEqual((self.root/"data/research_intelligence.json").read_text(),original)
    def test_missing_translation_rejected(self):
        p=payload()
        p["intelligence"]["evidence"]["fr"]=""
        self.assertTrue(any("evidence.fr" in e for e in validate_export(p,self.root)))
    def test_unindexed_product_rejected(self):
        p=payload()
        p["slug"]="unindexed"
        self.assertIn("Product slug is not in research index",validate_export(p,self.root))
    def test_unapproved_export_rejected(self):
        p=payload()
        p["review_status"]="approved"
        self.assertTrue(validate_export(p,self.root))
    def test_existing_product_conflict(self):
        (self.root/"data/research_intelligence.json").write_text('{"products":{"pending":{}}}',encoding="utf-8")
        with self.assertRaisesRegex(ValueError,"already has curated"):
            prepare(payload(),self.root)
    def test_traversal_source_rejected(self):
        p=payload()
        p["source_report"]="../private.md"
        self.assertTrue(validate_export(p,self.root))
if __name__=="__main__":
    unittest.main()
