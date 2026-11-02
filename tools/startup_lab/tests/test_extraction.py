import json
import tempfile
import unittest
from pathlib import Path
from startup_lab.extraction import review_candidate,promote,canonical_url

def candidate():
    return {"statement":"A public product announcement states the beta is open.",
            "source_url":"https://product.example.io/launch",
            "source_locator":"paragraph:2","observed_at":"2026-11-03",
            "limitations":"Official statement, not independent adoption evidence.",
            "evidence_type":"founder-claim","direction":"context",
            "dimension":"distribution","review_status":"approved",
            "source_checked":True,"reviewed_by":"curator"}

class ExtractionTests(unittest.TestCase):
    def test_approval_gate(self):
        c=candidate();c["review_status"]="pending"
        self.assertFalse(review_candidate(c)["accepted"])
    def test_source_verification_gate(self):
        c=candidate();c["source_checked"]=False
        self.assertFalse(review_candidate(c)["accepted"])
    def test_synthetic_domains_rejected(self):
        c=candidate();c["source_url"]="https://example.org/demo"
        self.assertFalse(review_candidate(c)["accepted"])
    def test_deterministic_identifiers(self):
        c=candidate()
        self.assertEqual(review_candidate(c)["record"]["id"],review_candidate(c)["record"]["id"])
    def test_idempotent_promotion(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/"candidate.json"
            path.write_text(json.dumps(candidate()))
            first=promote(path,Path(d)/"output")
            second=promote(path,Path(d)/"output")
            self.assertEqual(first["record"]["id"],second["record"]["id"])
            self.assertEqual(len(list((Path(d)/"output").glob("*.json"))),1)
    def test_bad_dates(self):
        c=candidate();c["observed_at"]="2026-02-31"
        self.assertFalse(review_candidate(c)["accepted"])
    def test_url_normalization(self):
        self.assertEqual(canonical_url("https://PRODUCT.example.io"),"https://product.example.io/")
if __name__=="__main__":unittest.main()
