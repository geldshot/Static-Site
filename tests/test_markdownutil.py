import unittest

from src.node.markdownutil import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_simple_title(self):
        md = """
# this is a title

and this is a paragraph
"""

        expected = "this is a title"
        title = extract_title(md)

        self.assertEqual(expected, title)

    def test_middle_title(self):
        md = """
## this title is bait

# this is the actual title

and here's the body
"""
        expected = "this is the actual title"
        title = extract_title(md)

        self.assertEqual(expected, title)

    def test_bad_title(self):
        md = """
## testing not a title

mid sentence # not a title

# actual title
"""

        expected = "actual title"
        title = extract_title(md)

        self.assertEqual(expected, title)

    def test_no_title(self):
        md = """
no title in this one

just paragraphs
"""

        with self.assertRaises(Exception):
            extract_title(md)