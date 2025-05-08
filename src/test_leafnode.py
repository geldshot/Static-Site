import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html(self):
        node = LeafNode("p", "For Cadia!")
        expected = "<p>For Cadia!</p>"

        actual = node.to_html()

        self.assertEqual(expected, actual)

    def test_leaf_repr(self):
        node = LeafNode("a", "this way to narnia",{"href":"https://www.linux.org/forums/"})
        expected = "HTMLNode(a, this way to narnia, None,  href=\"https://www.linux.org/forums/\")"

        actual = str(node)

        self.assertEqual(expected, actual)

    def test_leaf_no_tag_html(self):
        node = LeafNode(value="assembly is cool")
        expected = "assembly is cool"

        actual = node.to_html()

        self.assertEqual(expected, actual)

    def test_leaf_no_value_error(self):
        expected = "value cannot be None"
        with self.assertRaises(ValueError) as context:
            node = LeafNode()
        
        self.assertEqual(expected, str(context.exception))