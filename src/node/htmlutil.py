import re

from .blockutil import markdown_to_blocks, block_to_block_type
from .blockutil import BlockType
from .htmlnode import HTMLNode
from .parentnode import ParentNode
from .leafnode import LeafNode
from .textnode import TextNode
from .util import text_node_to_html_node, text_to_textnodes

def markdown_to_html_node(markdown):

    blocks = markdown_to_blocks(markdown)

    nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                nodes.append(block_to_paragraph(block))
            case BlockType.QUOTE:
                nodes.append(block_to_quote(block))
            case BlockType.HEADING:
                nodes.append(block_to_heading(block))
            case BlockType.CODE:
                nodes.append(block_to_code(block))
            case BlockType.UNORDERED_LIST:
                nodes.append(block_to_unordered_list(block))
            case BlockType.ORDERED_LIST:
                nodes.append(block_to_ordered_list(block))

    return ParentNode("div", nodes)

def block_to_unordered_list(block):
    block = block.replace("\n", "")
    list_items = block.split("- ")
    list_items = list_items[1:]
    list_html = list(map(lambda x: ParentNode("li", map(lambda y: text_node_to_html_node(y), text_to_textnodes(x))), list_items))
    return ParentNode("ul", list_html)

def block_to_ordered_list(block):
    regex = "(?:^|\n)\d+\\. (.*)"
    list_items = re.findall(regex, block)
    list_html = list(map(lambda x: ParentNode("li", map(lambda y: text_node_to_html_node(y), text_to_textnodes(x))), list_items))
    return ParentNode("ol", list_html)

def block_to_code(block):
    block = block.replace("```\n", "")
    block = block.replace("```", "")
    return ParentNode("pre", [LeafNode("code", block)])

def block_to_heading(block):
    heading_count = block.find(' ')
    block = block[heading_count+1:]
    return ParentNode(f'h{heading_count}',list(map(lambda y: text_node_to_html_node(y), text_to_textnodes(block))))

def block_to_quote(block):
    block = " ".join(list(map(lambda x: x.lstrip("> "), block.split("\n"))))
    new_block = text_to_textnodes(block)
    return ParentNode("blockquote",list(map(lambda y: text_node_to_html_node(y), new_block)))

def block_to_paragraph(block):
    block = block.replace("\n", " ")
    return ParentNode("p",list(map(lambda y: text_node_to_html_node(y), text_to_textnodes(block))))