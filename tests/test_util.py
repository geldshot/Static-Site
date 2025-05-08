import unittest

from src.node.leafnode import LeafNode
from src.node.textnode import TextNode, TextType
from src.node.util import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_images, split_nodes_links

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

class TestSplitNodesImages(unittest.TestCase):
    def test_simple_split(self):
        node = TextNode("here's a simple ![split](test.png) okay?")
        expected = [
            TextNode("here's a simple "),
            TextNode("split", TextType.IMAGE, "test.png"),
            TextNode(" okay?")
        ]

        actual = split_nodes_images([node])

        self.assertEqual(3, len(actual))
        self.assertEqual(expected, actual)

    def test_multi_split(self):
        node = TextNode("now we ![have](multiple.png) for ![split](test.png) okay?")
        expected = [
            TextNode("now we "),
            TextNode("have", TextType.IMAGE, "multiple.png"),
            TextNode(" for "),
            TextNode("split", TextType.IMAGE, "test.png"),
            TextNode(" okay?")
        ]

        actual = split_nodes_images([node])

        self.assertEqual(5, len(actual))
        self.assertEqual(expected, actual)

    def test_empty_end_split(self):
        node = TextNode("no text after ![split](test.png)")
        expected = [
            TextNode("no text after "),
            TextNode("split", TextType.IMAGE, "test.png")
        ]

        actual = split_nodes_images([node])

        self.assertEqual(2, len(actual))
        self.assertEqual(expected, actual)

    def test_empty_start_split(self):
        node = TextNode("![split](test.png) no text before image")
        expected = [
            TextNode("split", TextType.IMAGE, "test.png"),
            TextNode(" no text before image")
        ]

        actual = split_nodes_images([node])

        self.assertEqual(2, len(actual))
        self.assertEqual(expected, actual)

class TestSplitNodesLinks(unittest.TestCase):
    def test_simple_split(self):
        node = TextNode("here's a simple [split](https://www.google.com) okay?")
        expected = [
            TextNode("here's a simple "),
            TextNode("split", TextType.LINK, "https://www.google.com"),
            TextNode(" okay?")
        ]

        actual = split_nodes_links([node])

        self.assertEqual(3, len(actual))
        self.assertEqual(expected, actual)

    def test_multiple_split(self):
        node = TextNode("multiple [link](fourswords.com) but no [zelda](minishcap.com) alright?")
        expected = [
            TextNode("multiple "),
            TextNode("link", TextType.LINK, "fourswords.com"),
            TextNode(" but no "),
            TextNode("zelda", TextType.LINK, "minishcap.com"),
            TextNode(" alright?")
        ]

        actual = split_nodes_links([node])

        self.assertEqual(5, len(actual))
        self.assertEqual(expected, actual)

    def test_empty_split_combined(self):
        node = TextNode("[link](butnoends.com)")
        expected = [
            TextNode("link", TextType.LINK, "butnoends.com")
        ]

        actual = split_nodes_links([node])

        self.assertEqual(1, len(actual))
        self.assertEqual(expected, actual)