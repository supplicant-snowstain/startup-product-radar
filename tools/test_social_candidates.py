#!/usr/bin/env python3
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("social", Path(__file__).with_name("extract_social_candidates.py"))
social = importlib.util.module_from_spec(spec)
spec.loader.exec_module(social)

class SocialCandidateTests(unittest.TestCase):
    def test_official_link_candidate_not_verified(self):
        html='<a href="https://x.com/ExampleProduct">X</a><a href="https://github.com/example">GitHub</a>'
        rows=social.candidates("example","https://example.com",html)
        self.assertEqual(len(rows),2)
        self.assertTrue(all(r["review_status"]=="pending_review" for r in rows))
        self.assertTrue(all(r["identity_status"]=="candidate" for r in rows))
    def test_share_links_excluded(self):
        html='<a href="https://twitter.com/intent/tweet?text=hi">share</a><a href="https://x.com/search?q=hi">search</a>'
        self.assertEqual(social.candidates("example","https://example.com",html),[])
    def test_deduplicates(self):
        html='<a href="https://x.com/brand">one</a><a href="https://x.com/brand?ref=home">two</a>'
        self.assertEqual(len(social.candidates("example","https://example.com",html)),1)

if __name__=="__main__":
    unittest.main()
