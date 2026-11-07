#!/usr/bin/env python3
import importlib.util
import pathlib
import tempfile
import json
import subprocess
import sys
import unittest

SCRIPT = pathlib.Path(__file__).with_name("validate_relationships.py")
spec = importlib.util.spec_from_file_location("validate_relationships", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class RelationshipGateTests(unittest.TestCase):
    def setUp(self):
        self.good = {
            "id": "a-b", "from": "a", "to": "b", "type": "same_problem",
            "source_url": "https://example.org/source", "evidence_kind": "primary_documentation",
            "assertion": {"en": "A reviewed comparison"}, "review_status": "approved",
            "reviewed_at": "2026-11-08"
        }
    def test_valid_approved(self):
        self.assertEqual(module.validate({"schema_version":1,"relationships":[self.good]}, {"a","b"}), [])
    def test_unknown_product_rejected(self):
        self.assertTrue(module.validate({"schema_version":1,"relationships":[self.good]}, {"a"}))
    def test_missing_evidence_rejected(self):
        record = dict(self.good, source_url="")
        self.assertTrue(module.validate({"schema_version":1,"relationships":[record]}, {"a","b"}))
    def test_pending_not_published(self):
        with tempfile.TemporaryDirectory() as folder:
            root=pathlib.Path(folder)
            (root/"relations.json").write_text(json.dumps({"schema_version":1,"relationships":[dict(self.good,review_status="pending_review")]}))
            (root/"research.json").write_text(json.dumps({"reports":[{"products":[{"slug":"a"},{"slug":"b"}]}]}))
            result=subprocess.run([sys.executable,str(SCRIPT),"--relations",str(root/"relations.json"),"--research",str(root/"research.json"),"--output",str(root/"public.json")],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertEqual(json.loads((root/"public.json").read_text())["relationships"],[])
    def test_duplicate_id_rejected(self):
        self.assertTrue(module.validate({"schema_version":1,"relationships":[self.good,self.good]}, {"a","b"}))

if __name__ == "__main__":
    unittest.main()
