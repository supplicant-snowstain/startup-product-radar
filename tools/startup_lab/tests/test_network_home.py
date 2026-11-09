"""Regression checks for the graph-first landing page (no browser dependencies)."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WEB = ROOT / "web"

class NetworkHomeTests(unittest.TestCase):
    def test_homepage_embeds_existing_explorer(self):
        page = (WEB / "index.html").read_text(encoding="utf-8")
        self.assertIn('id="network-preview"', page)
        self.assertIn('src="./graph.html?embed=1"', page)
        self.assertIn('href="./graph.html"', page)
        self.assertIn('src="network-home.js"', page)
        self.assertIn('href="network-home.css"', page)

    def test_embedded_explorer_uses_same_origin_messages(self):
        source = (WEB / "graph.js").read_text(encoding="utf-8")
        self.assertIn('event.origin!==location.origin', source)
        self.assertIn('event.source!==window.parent', source)
        self.assertIn('graph-embedded', source)

    def test_language_support_and_evidence_warning(self):
        source = (WEB / "network-home.js").read_text(encoding="utf-8")
        for locale in ("zh", "en", "fr"):
            self.assertIn(locale + ":{", source)
        self.assertIn("radar-language-changed", source)
        page = (WEB / "index.html").read_text(encoding="utf-8")
        self.assertIn("product-market fit", page)

if __name__ == "__main__":
    unittest.main()
