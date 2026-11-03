import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
class IdeaStoryTests(unittest.TestCase):
    def test_stories_are_complete_in_three_languages(self):
        feed=json.loads((ROOT/"web/signals.json").read_text(encoding="utf-8"))
        data=json.loads((ROOT/"web/idea-stories.json").read_text(encoding="utf-8"))
        self.assertEqual(data["kind"],"illustrative_editorial_explanation")
        self.assertEqual({s["id"] for s in feed["signals"]},set(data["stories"]))
        for id,translations in data["stories"].items():
            for lang in ("en","zh","fr"):
                self.assertIn(lang,translations,id)
                for field in ("who","friction","idea","why","unknown"):
                    self.assertTrue(translations[lang][field].strip(),(id,lang,field))
                self.assertNotIn("source_url",translations[lang])
if __name__=="__main__":unittest.main()
