from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    if re.match(r'^#{1,6} ', block):
        return BlockType.HEADING
    elif re.match(r'^```', block):
        return BlockType.CODE
    elif re.match(r'^> ', block):
        return BlockType.QUOTE
    elif re.match(r'^[-*+] ', block):
        return BlockType.UNORDERED_LIST
    elif re.match(r'^\d+\. ', block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

