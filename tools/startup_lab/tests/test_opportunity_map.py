import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
class OpportunityMapTests(unittest.TestCase):
    def test_edges_reference_existing_signals(self):
        graph=json.loads((ROOT/'web/opportunity-map.json').read_text())
        feed=json.loads((ROOT/'web/signals.json').read_text())
        ids={s['id'] for s in feed['signals']}
        self.assertEqual(graph['review_state'],'editorial_hypothesis_not_verified')
        for e in graph['edges']:
            self.assertIn(e['from'],ids)
            self.assertIn(e['to'],ids)
            self.assertNotEqual(e['from'],e['to'])
            self.assertEqual(e['verification'],'editorial_hypothesis')
            self.assertTrue(e['reason'])
            self.assertEqual(e['evidence_ids'],[])
if __name__=='__main__':unittest.main()
