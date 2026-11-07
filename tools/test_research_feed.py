import csv
import tempfile
import unittest
from pathlib import Path

from build_research_feed import build


class ResearchFeedTest(unittest.TestCase):
    def test_observation_not_launch_and_no_candidate_promotion(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "index").mkdir()
            (root / "reports/2026/11").mkdir(parents=True)
            (root / "data/product_candidates").mkdir(parents=True)
            (root / "reports/2026/11/2026-11-07.md").write_text("# Research sample\n", encoding="utf-8")
            with (root / "index/products.csv").open("w", encoding="utf-8", newline="") as f:
                w = csv.DictWriter(f, fieldnames=["slug", "name", "first_observed", "profile_path", "category", "ai_role", "website"])
                w.writeheader()
                w.writerow({"slug":"known","website":"https://example.org","name":"Known Research Product", "first_observed":"2026-11-07", "profile_path":"products/known.md", "category":"Developer Tools", "ai_role":"none"})
            (root / "data/product_candidates/candidate-abc.json").write_text('{"name":"Unreviewed"}', encoding="utf-8")
            (root / "data/research_intelligence.json").write_text('{"products":{"known":{"job":{"en":"A grounded user task"}}}}', encoding="utf-8")
            feed = build(root)
            self.assertEqual(feed["kind"], "research_observations")
            self.assertEqual(feed["reports"][0]["observed_at"], "2026-11-07")
            self.assertEqual(feed["reports"][0]["products"][0]["ai_role"], "none")
            self.assertEqual(feed["reports"][0]["products"][0]["slug"], "known")
            self.assertEqual(feed["reports"][0]["products"][0]["intelligence"]["job"]["en"], "A grounded user task")
            self.assertNotIn("Unreviewed", str(feed))
            self.assertNotIn("launch_date", str(feed))


if __name__ == "__main__":
    unittest.main()
