import unittest
from samplify import is_email, is_valid_ip, is_valid_url


class TestSamplifyTestCase(unittest.TestCase):

    def test_returns_false_if_invalid_url_passes(self):
        self.assertFalse(is_valid_url('py'))

    def test_returns_false_if_url_without_scheme_and_domain_passes(self):
        self.assertFalse(is_valid_url('/giantas/pyconfigreader/blob/master/tests/testconfigreader.py'))

    def test_returns_false_if_url_without_scheme_passes(self):
        self.assertFalse(is_valid_url('abc.com/giantas/pyconfigreader/blob/master/tests/testconfigreader.py'))

    def test_returns_false_if_valid_url(self):
        self.assertTrue(is_valid_url('https://github.com/giantas/pyconfigreader/blob/master/tests/testconfigreader.py'))

    def test_returns_false_if_file_url_passes(self):
        self.assertFalse(is_valid_url('file:///home/aswa/developer/whamfront/index.html'))

    def test_returns_false_if_invalid_ip_passes(self):
        self.assertFalse(is_valid_ip('127.0.0'))

    def test_returns_false_if_valid_ip_fails(self):
        self.assertTrue(is_valid_ip('127.0.0.1'))

    def test_returns_false_if_wrong_ip_version_returned(self):
        with self.subTest():
            self.assertEqual(is_valid_ip('127.0.0.1'), 4)

        with self.subTest():
            self.assertEqual(is_valid_ip('::1'), 6)

    def test_returns_false_if_invalid_emails_pass(self):
        invalid_emails = ['a', '1', 'abc@', '@y.net', 'net@net', '@@.com']
        for index, email in enumerate(invalid_emails):
            with self.subTest(index):
                self.assertFalse(is_email(email))

    def test_returns_false_if_valid_emails_fail(self):
        invalid_emails = ['a@abc.com', '1@2.com', 'abc@y.net', '123@y.net', 'a-t@co.ke', '6@7.com']
        for index, email in enumerate(invalid_emails):
            with self.subTest(index):
                self.assertTrue(is_email(email))


if __name__ == "__main__":
    unittest.main()
