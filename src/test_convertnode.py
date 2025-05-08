import unittest

from leafnode import LeafNode
from textnode import TextNode, TextType
from convertnode import text_node_to_html_node

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