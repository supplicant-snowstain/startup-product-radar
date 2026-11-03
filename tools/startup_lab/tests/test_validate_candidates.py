import json
import tempfile
import unittest
from pathlib import Path
from startup_lab.product_candidates import stage
from startup_lab.validate_candidates import validate

class CandidateValidationTests(unittest.TestCase):
    def test_staged_record_validates(self):
        with tempfile.TemporaryDirectory() as d:
            stage(d,[{"name":"Example","source_url":"https://example.org/tool","observed_at":"2026-11-03"}])
            self.assertEqual(validate(d)["errors"],[])
    def test_candidate_cannot_claim_human_review(self):
        with tempfile.TemporaryDirectory() as d:
            result=stage(d,[{"name":"Example","source_url":"https://example.org/tool","observed_at":"2026-11-03"}])
            path=Path(d)/result["created"][0]
            data=json.loads(path.read_text());data["source_checked"]=True
            path.write_text(json.dumps(data))
            self.assertTrue(validate(d)["errors"])
if __name__=="__main__":unittest.main()
