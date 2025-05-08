import unittest

from src.node.leafnode import LeafNode
from src.node.textnode import TextNode, TextType
from src.node.util import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links

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

class TestExtractLink(unittest.TestCase):
    def test_link_extract(self):
        text = "here's how we do a [link](https://www.google.com)"
        expected = [("link", "https://www.google.com")]

        actual = extract_markdown_links(text)

        self.assertEqual(expected, actual)

    def test_multiple_link_extract(self):
        text = "multiple links [link](https://zelda.nintendo.com/) wait that's zelda [zelda](https://www.speedrun.com/botw)"
        expected = [("link", "https://zelda.nintendo.com/"),
                    ("zelda", "https://www.speedrun.com/botw")
                    ]

        actual = extract_markdown_links(text)

        self.assertEqual(expected, actual)

    def test_image_not_extracted(self):
        text = "here's how we do a ![image](https://www.google.com)"
        expected = []

        actual = extract_markdown_links(text)

        self.assertEqual(expected, actual)

    def test_no_link_to_extract(self):
        text = "here's how we do no link"
        expected = []

        actual = extract_markdown_links(text)

        self.assertEqual(expected, actual)

    def test_empty_link(self):
        text = "here's how we do a []()"
        expected = [("", "")]

        actual = extract_markdown_links(text)

        self.assertEqual(expected, actual)

class TestExtractImage(unittest.TestCase):
    def test_image_extract(self):
        text = "here's how we do an ![image](https://www.ikea.com/us/en/images/products/blahaj-soft-toy-shark__0710175_pe727378_s5.jpg)"
        expected = [("image", "https://www.ikea.com/us/en/images/products/blahaj-soft-toy-shark__0710175_pe727378_s5.jpg")]

        actual = extract_markdown_images(text)

        self.assertEqual(expected, actual)

    def test_multiple_image_extract(self):
        text = "here's how we do an ![tiger](tiger.png) and ![lions](lion.png)"
        expected = [("tiger", "tiger.png"),
                    ("lions", "lion.png")]

        actual = extract_markdown_images(text)

        self.assertEqual(expected, actual)

    def test_link_not_extracted(self):
        text = "here's how we do a [link](https://www.google.com)"
        expected = []

        actual = extract_markdown_images(text)

        self.assertEqual(expected, actual)

    def test_no_image_to_extract(self):
        text = "but what if there is no image"
        expected = []

        actual = extract_markdown_images(text)

        self.assertEqual(expected, actual)

    def test_empty_image(self):
        text = "or if the image is empty ![]()"
        expected = [("", "")]

        actual = extract_markdown_images(text)

        self.assertEqual(expected, actual)