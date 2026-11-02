import json
import unittest
from pathlib import Path
from startup_lab.evaluator import evaluate,evaluate_file

ROOT=Path(__file__).parents[1]
class EvaluatorTests(unittest.TestCase):
    def test_example_ready(self):
        self.assertEqual(evaluate_file(ROOT/'examples/idea.json')['status'],'evidence_review_ready')
    def test_vc_is_not_user_demand(self):
        e={'id':'vc','url':'https://example.org/vc','type':'investor_claim','dimension':'user_need','stance':'supports','observed_at':'2026-11-03','claim':'synthetic investment'}
        self.assertIn('INVESTOR_SIGNAL_NOT_DEMAND_VALIDATION',evaluate({'id':'vc-only','evidence':[e]})['risk_flags'])
    def test_invalid_url(self):
        c=json.loads((ROOT/'examples/idea.json').read_text()); c['evidence'][0]['url']='invalid'
        self.assertEqual(evaluate(c)['status'],'invalid_input')
    def test_duplicate_evidence_id(self):
        c=json.loads((ROOT/'examples/idea.json').read_text()); c['evidence'][1]['id']='e1'
        self.assertEqual(evaluate(c)['status'],'invalid_input')
    def test_empty(self):
        self.assertEqual(evaluate({'id':'empty','evidence':[]})['status'],'insufficient_evidence')
if __name__=='__main__': unittest.main()
