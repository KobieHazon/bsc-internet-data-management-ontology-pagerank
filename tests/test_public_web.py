import unittest
from unittest.mock import Mock, patch
import public_web

class AnonymousRequestsTests(unittest.TestCase):
    def test_session_has_no_machine_credentials_and_checks_status(self):
        session = Mock()
        session.headers = {}
        session.get.return_value.is_redirect = False
        with patch('requests.Session') as factory:
            factory.return_value.__enter__.return_value = session
            public_web.get('https://example.test/page')
        self.assertIs(session.trust_env, False)
        session.get.assert_called_once_with('https://example.test/page', timeout=20, allow_redirects=False)
        session.get.return_value.raise_for_status.assert_called_once()

    def test_credentials_and_non_web_urls_are_rejected(self):
        for url in ['https://user:password@example.test', 'file:///tmp/page', 'ftp://example.test']:
            with self.assertRaises(ValueError):
                public_web.get(url)
