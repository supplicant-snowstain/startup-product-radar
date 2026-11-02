import csv
import json
import tempfile
import unittest
from pathlib import Path
from startup_lab.repository import audit_repository,idea_from_repository

class RepositoryTests(unittest.TestCase):
    def test_empty_repo_does_not_invent_evidence(self):
        with tempfile.TemporaryDirectory() as d:
            result=audit_repository(d)
            self.assertEqual(result["readiness"],"awaiting_verified_evidence")
            self.assertEqual(result["evidence_records"],0)

    def test_real_record_ingestion_and_missing_source(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            folder=root/"data"/"evidence"
            folder.mkdir(parents=True)
            record={"id":"obs-001","source_url":"https://example.com/public-report",
                    "observed_at":"2026-11-03","statement":"Fixture, not a real customer claim",
                    "evidence_type":"user-report","dimension":"user_need","stance":"supports"}
            (folder/"obs-001.json").write_text(json.dumps(record))
            idea=root/"idea.json"
            idea.write_text(json.dumps({"id":"trial","evidence_ids":["obs-001","obs-999"]}))
            result=idea_from_repository(root,idea)
            self.assertEqual(result["missing_evidence_ids"],["obs-999"])
            self.assertEqual(result["status"],"invalid_input")
            self.assertEqual(result["repository_audit"]["evidence_records"],1)

    def test_duplicate_evidence_ids_are_flagged(self):
        with tempfile.TemporaryDirectory() as d:
            folder=Path(d)/"data"/"evidence";folder.mkdir(parents=True)
            record={"id":"duplicate","source_url":"https://example.org",
                    "observed_at":"2026-11-03","statement":"Synthetic",
                    "evidence_type":"independent"}
            (folder/"a.json").write_text(json.dumps(record))
            (folder/"b.json").write_text(json.dumps(record))
            self.assertEqual(audit_repository(d)["duplicate_evidence_ids"],["duplicate"])
