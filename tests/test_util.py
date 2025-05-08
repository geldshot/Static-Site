import unittest

from src.node.leafnode import LeafNode
from src.node.textnode import TextNode, TextType
from src.node.util import text_node_to_html_node, split_nodes_delimiter

class TestTextToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("Bold text node", TextType.BOLD)
        
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text node")

    def test_link(self):
        node = TextNode("This is a link", TextType.LINK, "https://www.google.com")

        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props["href"], "https://www.google.com")

    def test_img(self):
        node = TextNode("This is the image", TextType.IMAGE, "psych no image")

        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["alt"], "This is the image")
        self.assertEqual(html_node.props["src"], "psych no image")

class TestSplitDelimiter(unittest.TestCase):
    def test_split(self):
        node = TextNode("simple **bold** test", TextType.TEXT)
        first = TextNode("simple ", TextType.TEXT)
        second = TextNode("bold", TextType.BOLD)
        third = TextNode(" test", TextType.TEXT)

        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(len(nodes), 3)
        self.assertEqual(first, nodes[0])
        self.assertEqual(second, nodes[1])
        self.assertEqual(third, nodes[2])

    def test_non_default(self):
        node = TextNode("code with _italics_ in the middle", TextType.CODE)
        first = TextNode("code with ", TextType.CODE)
        second = TextNode("italics", TextType.ITALIC)
        third = TextNode(" in the middle", TextType.CODE)

        nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)

        self.assertEqual(len(nodes), 3)
        self.assertEqual(first, nodes[0])
        self.assertEqual(second, nodes[1])
        self.assertEqual(third, nodes[2])