"""Zero-dependency tests for website localization completeness."""
import json
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
WEB=ROOT/"web"

class LocalizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.locales={lang:json.loads((WEB/"locales"/f"{lang}.json").read_text(encoding="utf-8"))
                     for lang in ("en","zh","fr")}
    def test_same_keys_across_languages(self):
        reference=set(self.locales["en"]["ui"])
        self.assertTrue(reference)
        for lang,bundle in self.locales.items():
            self.assertEqual(set(bundle["ui"]),reference,lang)
            for key,value in bundle["ui"].items():
                self.assertIsInstance(value,str,(lang,key))
                self.assertTrue(value.strip(),(lang,key))
    def test_all_html_keys_exist(self):
        keys=set(self.locales["en"]["ui"])
        for filename in ("index.html","explore.html"):
            content=(WEB/filename).read_text(encoding="utf-8")
            used=set(re.findall(r'data-i18n(?:-html|-placeholder)?="([^"]+)"',content))
            self.assertFalse(used-keys,(filename,sorted(used-keys)))
    def test_interpolated_keys_exist(self):
        keys=set(self.locales["en"]["ui"])
        for filename in ("app.js","explore.js"):
            source=(WEB/filename).read_text(encoding="utf-8")
            used=set(re.findall(r'I\.t\(["\']([^"\']+)["\']\)',source))
            self.assertFalse(used-keys,(filename,sorted(used-keys)))
    def test_all_known_signals_translated(self):
        feed=json.loads((WEB/"signals.json").read_text(encoding="utf-8"))
        ids={s["id"] for s in feed["signals"]}
        for lang in ("zh","fr"):
            self.assertEqual(set(self.locales[lang]["signals"]),ids,lang)
            for sig in self.locales[lang]["signals"].values():
                for field in ("title","problem","questions","limitations"):
                    self.assertTrue(sig.get(field), (lang,field))
    def test_bundles_are_json_not_html_from_sources(self):
        for lang,bundle in self.locales.items():
            for signal in bundle["signals"].values():
                self.assertNotIn("source_url",signal,lang)
                self.assertNotIn("source_locator",signal,lang)
if __name__=="__main__":unittest.main()
