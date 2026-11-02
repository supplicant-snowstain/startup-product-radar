import json
import tempfile
import unittest
from pathlib import Path
from startup_lab.retrieval import retrieve,evidence_sides
from startup_lab.report_candidates import report_candidates

class RetrievalTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)
        f=self.root/"data"/"evidence";f.mkdir(parents=True)
        for id,direction in [("ev-one","support"),("ev-two","contradict")]:
            (f/(id+".json")).write_text(json.dumps({
                "id":id,"statement":"Freelancers need better invoice tracking",
                "source_url":"https://research.example.io/"+id,
                "observed_at":"2026-11-03","evidence_type":"independent",
                "dimension":"user_need","direction":direction}),encoding="utf-8")
    def tearDown(self): self.tmp.cleanup()
    def test_search_citations(self):
        result=retrieve(self.root,"invoice tracking")
        self.assertEqual(result["total_matches"],2)
        self.assertTrue(all(x["source_url"].startswith("https://") for x in result["results"]))
    def test_opposing_evidence_not_conclusion(self):
        result=evidence_sides(self.root,"invoice")
        self.assertTrue(result["potential_disagreement"])
        self.assertIn("manual review",result["warning"])
    def test_missing_evidence(self):
        self.assertEqual(retrieve(self.root,"saxophone")["total_matches"],0)
    def test_blank_query(self):
        with self.assertRaises(ValueError):retrieve(self.root," ")
    def test_links_unreviewed(self):
        p=self.root/"report.md"
        p.write_text("# Research\n[Product](https://valid.example.io/a)\n[Product again](https://valid.example.io/a)\n")
        r=report_candidates(p)
        self.assertEqual(len(r["candidates"]),1)
        self.assertFalse(r["candidates"][0]["source_checked"])
        self.assertIsNone(r["candidates"][0]["statement"])
