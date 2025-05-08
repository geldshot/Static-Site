import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("test node", TextType.LINK, "https://www.google.com")
        
        actual = str(node)
        
        expected = "TextNode(test node, link, https://www.google.com)"
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()