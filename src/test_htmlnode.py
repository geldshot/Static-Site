import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"href":"https://www.google.com", "alt":"where are we?"})
        expected = " href=\"https://www.google.com\" alt=\"where are we?\""
        
        actual = node.props_to_html()
        
        self.assertEqual(expected, actual)

    def test_repr(self):
        node = HTMLNode(tag="wirl", value=200, children="no children", props={"href":"https://www.google.com", "alt":"where are we?"})
        expected = "HTMLNode(wirl, 200, no children,  href=\"https://www.google.com\" alt=\"where are we?\")"

        actual = str(node)

        self.assertEqual(expected, actual)

    def test_empty_node(self):
        node = HTMLNode()
        expected = "HTMLNode(None, None, None, )"

        actual = str(node)

        self.assertEqual(expected, actual)