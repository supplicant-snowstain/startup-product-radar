"""Static-site contract tests for published product and research records."""
import json
import unittest
from pathlib import Path
from startup_lab.product_feed import build as product_build
from startup_lab.public_feed import build as signal_build

ROOT=Path(__file__).resolve().parents[3]
class PublishedSiteContracts(unittest.TestCase):
    def test_product_page_exists_and_links_to_assets(self):
        page=(ROOT/"web"/"product.html").read_text(encoding="utf-8")
        for asset in ("product-detail.js","i18n.js","style.css"):
            self.assertIn(asset,page)
            self.assertTrue((ROOT/"web"/asset).is_file())
    def test_product_feed_matches_source(self):
        actual=json.loads((ROOT/"web"/"products.json").read_text(encoding="utf-8"))
        expected=product_build(ROOT)
        self.assertEqual(actual,expected,"Committed product feed differs from generated data")
    def test_signal_feed_matches_source(self):
        actual=json.loads((ROOT/"web"/"signals.json").read_text(encoding="utf-8"))
        self.assertEqual(actual,signal_build(ROOT),"Committed signal feed differs from generated data")
    def test_products_are_browsable_and_sourced(self):
        products=product_build(ROOT)["products"]
        self.assertGreaterEqual(len(products),3)
        for item in products:
            self.assertTrue(item["source_url"].startswith("https://"))
            self.assertIn(item["collection"],("new_launch","case_study"))
            if item["collection"]=="new_launch":
                self.assertTrue(item["launch_source_url"].startswith("https://"))
            self.assertTrue((item.get("story") or {}).get("zh"),item["name"])
if __name__=="__main__":unittest.main()
