"""Static regression checks for graph search and evidence-safe discovery."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[3]

class GraphSearchTests(unittest.TestCase):
    def test_search_filters_both_modes(self):
        js = (ROOT / "web" / "graph.js").read_text(encoding="utf-8")
        self.assertIn('function visibleProducts()', js)
        self.assertIn('const list=visibleProducts().slice(0,36)', js)
        self.assertIn('for(const p of visibleProducts())', js)
        self.assertIn('const eligible=visibleProducts()', js)
        self.assertIn('searchInput.addEventListener("input"', js)

    def test_claim_provenance_labels(self):
        js = (ROOT / "web" / "graph.js").read_text(encoding="utf-8")
        self.assertIn('claimStatus:record?.claim_status==="documented"', js)
        self.assertIn("Documented · not independently verified", js)
        self.assertIn("Research hypothesis · unvalidated", js)
        self.assertIn("No reviewed research conclusion", js)

    def test_source_traceability_and_deep_links(self):
        js = (ROOT / "web" / "graph.js").read_text(encoding="utf-8")
        self.assertIn("sourceCount:Array.isArray(record?.sources)", js)
        self.assertIn("Public sources: ", js)
        self.assertIn('url.searchParams.set("id",selected)', js)
        self.assertIn('url.searchParams.delete("embed")', js)
        self.assertIn("Share this product research view", js)

    def test_relationship_type_filter(self):
        js = (ROOT / "web" / "graph.js").read_text(encoding="utf-8")
        self.assertIn('relationTypeFilter==="all"||r.type===relationTypeFilter', js)
        self.assertIn('relationSelect.id="graph-relation-type"', js)
        self.assertIn('relationSelect.addEventListener("change"', js)
        self.assertIn('relationTypeFilter=relationSelect.value', js)
        self.assertIn('$("graph-relation-type").hidden=mode!=="global"', js)
        self.assertIn('window.addEventListener("radar-language-changed",updateRelationLabels)', js)

    def test_empty_state_and_accessibility(self):
        js = (ROOT / "web" / "graph.js").read_text(encoding="utf-8")
        self.assertIn('No matching products.', js)
        self.assertIn('aria-label","Search products and research"', js)
        self.assertIn('graph-canvas").replaceChildren()', js)

if __name__ == "__main__":
    unittest.main()
