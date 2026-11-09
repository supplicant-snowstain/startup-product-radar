"""Safety contract for opportunity evidence publication.

Run: python -m unittest discover -s tools -p 'test_opportunity_contract.py' -v
"""
import importlib.util
from pathlib import Path
import unittest

MODULE = Path(__file__).with_name("build_opportunity_feed.py")
spec = importlib.util.spec_from_file_location("build_opportunity_feed", MODULE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def record(status="approved", claim="documented", sources=None):
    return {
        "review_status": status,
        "claim_status": claim,
        "summary": {"zh": "测试", "en": "Test", "fr": "Essai"},
        "sources": [{"url": "https://example.org/source"}] if sources is None else sources,
    }


class OpportunityEvidenceContract(unittest.TestCase):
    def test_unreviewed_evidence_not_published(self):
        data = {"schema_version": 1, "products": {"example": {"founding": record(status="pending")}}}
        self.assertEqual(module.build(data, {"example"})["products"], {})

    def test_approved_documented_evidence_published(self):
        data = {"schema_version": 1, "products": {"example": {"founding": record()}}}
        self.assertEqual(module.build(data, {"example"})["products"]["example"]["founding"]["claim_status"], "documented")

    def test_approved_hypothesis_preserves_label(self):
        data = {"schema_version": 1, "products": {"example": {"future": record(claim="hypothesis")}}}
        self.assertEqual(module.build(data, {"example"})["products"]["example"]["future"]["claim_status"], "hypothesis")

    def test_missing_source_rejected(self):
        data = {"schema_version": 1, "products": {"example": {"growth": record(sources=[])}}}
        with self.assertRaises(ValueError):
            module.build(data, {"example"})

    def test_unknown_product_rejected(self):
        data = {"schema_version": 1, "products": {"invented": {"feedback": record()}}}
        with self.assertRaises(ValueError):
            module.build(data, {"example"})

    def test_untranslated_approved_claim_rejected(self):
        item = record()
        item["summary"].pop("fr")
        data = {"schema_version": 1, "products": {"example": {"timeline": item}}}
        with self.assertRaises(ValueError):
            module.build(data, {"example"})


if __name__ == "__main__":
    unittest.main()
