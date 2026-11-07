import csv
import json
import tempfile
import unittest
from pathlib import Path

from build_research_drafts import build, extract

class DraftTests(unittest.TestCase):
    def test_section_scoped_extraction(self):
        report = "## Deep dive: Alpha\n- JTBD: solve A\n- 可证伪假设：test A\n## Deep dive: Beta\n- JTBD: solve B\n"
        self.assertEqual(extract(report, "Alpha")["job"], "solve A")
        self.assertNotIn("solve B", str(extract(report, "Alpha")))
    def test_never_promote_reviewed_or_unindexed_candidates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            (root/"data").mkdir()
            (root/"index").mkdir()
            (root/"reports/2026/11").mkdir(parents=True)
            (root/"data/research_intelligence.json").write_text('{"products":{"approved":{}}}',encoding="utf-8")
            with (root/"index/products.csv").open("w",encoding="utf-8",newline="") as f:
                w=csv.DictWriter(f,fieldnames=["slug","name","first_observed"])
                w.writeheader()
                w.writerow({"slug":"approved","name":"Approved","first_observed":"2026-11-07"})
                w.writerow({"slug":"pending","name":"Pending","first_observed":"2026-11-07"})
            (root/"reports/2026/11/2026-11-07.md").write_text("## Approved\n- JTBD: existing\n## Pending\n- JTBD: a task\n",encoding="utf-8")
            result=build(root)
            self.assertEqual(result["kind"],"editorial_drafts_not_publication")
            self.assertEqual([d["slug"] for d in result["drafts"]],["pending"])
            self.assertEqual(result["drafts"][0]["review_status"],"needs_human_review")
            self.assertEqual(result["drafts"][0]["extracted_zh"]["job"],"a task")
            draft_slugs = {draft["slug"] for draft in result["drafts"]}
            self.assertNotIn("approved", draft_slugs)
if __name__=="__main__":
    unittest.main()
