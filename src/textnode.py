from enum import Enum
from htmlnode import LeafNode



class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True

    def __repr__(self):
        return (f"TextNode({self.text}, {self.text_type.value}, {self.url})")
    
    # Leafnode:def __init__(self, tag, value, props=None):

def text_node_to_html_node(node):
    if not isinstance(node.text_type, TextType):
        raise Exception("TextType not recognised")
    if node.text_type == TextType.TEXT:
        return LeafNode(None, node.text)
    if node.text_type == TextType.BOLD:
        return LeafNode("b", node.text)
    if node.text_type == TextType.ITALIC:
        return LeafNode("i", node.text)
    if node.text_type == TextType.CODE:
        return LeafNode("code", node.text)
    if node.text_type == TextType.LINK:
        return LeafNode("a", node.text, {"href": node.url})
    if node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": node.url, "alt": node.text})








