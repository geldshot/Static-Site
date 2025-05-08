import unittest

from src.node.blockutil import BlockType
from src.node.blockutil import markdown_to_blocks, block_to_block_type

class TestMarkdownToBlocks(unittest.TestCase):
    def test_simple_block(self):
        md = """
this is a paragraph

Another paragraph with [link](google.com)
still the same paragraph

- list part one
- list part two
"""
        expected = [
            "this is a paragraph",
            "Another paragraph with [link](google.com)\nstill the same paragraph",
            "- list part one\n- list part two"
        ]

        actual = markdown_to_blocks(md)

        self.assertEqual(expected, actual)

    def test_extra_new_lines(self):
        md = """
this is a paragraph



Another paragraph with [link](google.com)
still the same paragraph


- list part one
- list part two
"""
        expected = [
            "this is a paragraph",
            "Another paragraph with [link](google.com)\nstill the same paragraph",
            "- list part one\n- list part two"
        ]

        actual = markdown_to_blocks(md)

        self.assertEqual(expected, actual)

class TestBlockToBlockType(unittest.TestCase):
    def test_normal(self):
        block = """normal paragraph
just like so"""

        actual = block_to_block_type(block)

        self.assertEqual(BlockType.PARAGRAPH, actual)

    def test_code(self):
        block = """```
        this is a code block
        ```"""

        actual = block_to_block_type(block)

        self.assertEqual(BlockType.CODE, actual)

    def test_heading(self):
        block = "### heading"

        actual = block_to_block_type(block)

        self.assertEqual(BlockType.HEADING, actual)

    def test_quote(self):
        block = """> this is a quote
> quote continued
> quote continued"""

        actual = block_to_block_type(block)

        self.assertEqual(BlockType.QUOTE, actual)

    def test_unordered_list(self):
        block = """- this list
- is not ordered"""

        actual = block_to_block_type(block)

        self.assertEqual(BlockType.UNORDERED_LIST, actual)

    def test_ordered_list(self):
        block = """1. list is
2. ordered
3. correclty"""

        actual = block_to_block_type(block)

        self.assertEqual(BlockType.ORDERED_LIST, actual)