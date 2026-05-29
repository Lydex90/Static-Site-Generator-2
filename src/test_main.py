import unittest

from main import extract_title

class TestTextNode(unittest.TestCase):
    def test_1(self):
        markdown = "# Supposably"
        self.assertEqual(extract_title(markdown), "Supposably")
    def test_2(self):
        markdown = md = """\
# Heading One

## Heading Two
"""
        self.assertEqual(extract_title(markdown), "Heading One")
    def test_3(self):
        markdown = "no heading here"
        with self.assertRaises(Exception):
            extract_title(markdown)

if __name__ == "__main__":
    unittest.main()