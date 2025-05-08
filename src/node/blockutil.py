from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = list(map(lambda x: x.strip(), filter(lambda x: x, markdown.split("\n\n"))))
    return blocks

def block_to_block_type(block):
    if re. match("^#{1,6} .*?", block):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    lines = block.split("\n")

    if [item for item in lines if item.startswith("> ")] == lines:
        return BlockType.QUOTE

    if [item for item in lines if item.startswith("- ")] == lines :
        return BlockType.UNORDERED_LIST

    if [int(item.split(".", maxsplit=1)[0]) for item in lines if re.match("^[\\d]+\\.", item)] == list(range(1,len(lines)+1)):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH