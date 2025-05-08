import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_parent_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold statement"),
                LeafNode(None, "Normal statement"),
                ParentNode(
                    "h1",
                    [
                        LeafNode("i", "Italic statement")
                    ]
                ),
                LeafNode(None, "Another normal statement")
            ]
        )
        expected = "<p><b>Bold statement</b>Normal statement<h1><i>Italic statement</i></h1>Another normal statement</p>"

        actual = node.to_html()

        self.assertEqual(expected, actual)