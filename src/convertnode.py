from textnode import TextNode, TextType
from leafnode import LeafNode

def text_node_to_html_node(text_node):
    match text_node.text_type.value:
        
        case TextType.TEXT.value:
            return LeafNode(None, text_node.text)
        
        case TextType.BOLD.value:
            return LeafNode("b",text_node.text)
        
        case TextType.ITALIC.value:
            return LeafNode("i", text_node.text)
        
        case TextType.CODE.value:
            return LeafNode("code", text_node.text)
        
        case TextType.LINK.value:
            return LeafNode("a", text_node.text, {"href":text_node.url})
        
        case TextType.IMAGE.value:
            return LeafNode("img", "", {"src":text_node.url, "alt":text_node.text})
        
        case _:
            raise Exception("invalid TextType")