import re

from .textnode import TextNode, TextType
from .leafnode import LeafNode

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
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for node in old_nodes:
        text = node.text
        splits = text.split(delimiter, maxsplit=2)
        count = len(splits)
        
        while count == 3:
            new_nodes.append(TextNode(splits[0], node.text_type, node.url))
            new_nodes.append(TextNode(splits[1], text_type, node.url))
            
            text = splits[2]
            splits = text.split(delimiter, maxsplit=2)
            count = len(splits)
        
        new_nodes.append(TextNode(text, node.text_type))
    
    return new_nodes

def extract_markdown_images(text):
    regex = "\\!\\[(.*?)\\]\\((.*?)\\)"
    
    matches = re.findall(regex, text)
    
    return matches

def extract_markdown_links(text):
    regex = "(?:^|[^\\!])\\[(.*?)\\]\\((.*?)\\)"
    
    matches = re.findall(regex, text)
    
    return matches

def split_nodes_images(old_nodes):
    new_nodes = []
    text = None
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        text = node.text
        
        for image in images:
            splits = text.split(f'![{image[0]}]({image[1]})', maxsplit=1 )
            
            if splits[0]:
                new_nodes.append(TextNode(splits[0], node.text_type))
            
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            text = splits[1]
        if text:
            new_nodes.append(TextNode(text, node.text_type, node.url))

    return new_nodes

def split_nodes_links(old_nodes):
    new_nodes = []

    for node in old_nodes:
        links = extract_markdown_links(node.text)
        text = node.text
        
        for link in links:
            splits = text.split(f'[{link[0]}]({link[1]})', maxsplit=1 )

            if splits[0]:
                new_nodes.append(TextNode(splits[0], node.text_type))
            
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            text = splits[1]
        if text:
            new_nodes.append(TextNode(text, node.text_type, node.url))

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text)]

    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_links(nodes)
    nodes = split_nodes_images(nodes)
    
    return nodes