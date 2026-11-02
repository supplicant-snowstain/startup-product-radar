import unittest
from unittest.mock import patch
from startup_lab.source_verify import match_snapshot,validate_public_url,verify_source

class SourceVerifyTests(unittest.TestCase):
    def test_match(self):
        html='<html><script>ignore</script><p>Users requested offline export options in beta.</p></html>'
        self.assertTrue(match_snapshot(html,'offline export options')["excerpt_present"])
        self.assertFalse(match_snapshot(html,'subscription pricing changed')["excerpt_present"])
    def test_localhost(self):
        with self.assertRaises(ValueError): validate_public_url('http://localhost/private')
    def test_credentials(self):
        with self.assertRaises(ValueError):validate_public_url('https://name:password@example.org')
    @patch('startup_lab.source_verify.socket.getaddrinfo')
    def test_private_ip(self,mock):
        mock.return_value=[(2,1,6,'',('127.0.0.1',443))]
        with self.assertRaises(ValueError):validate_public_url('https://public-name.test')
    @patch('startup_lab.source_verify.socket.getaddrinfo')
    def test_fetch_is_fail_closed(self,mock):
        mock.return_value=[(2,1,6,'',('8.8.8.8',443))]
        result=verify_source('https://safe.test','An excerpt with sufficient characters')
        self.assertEqual(result["status"],'requires_secure_fetch_backend')
        self.assertIsNone(result["excerpt_present"])
if __name__=='__main__':unittest.main()
