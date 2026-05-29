from textnode import TextNode, TextType, text_node_to_html_node
import re
from blocktype import BlockType, block_to_block_type
from htmlnode import HTMLNode, ParentNode, LeafNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        text = node.text
        

        while delimiter in text:
            start = text.find(delimiter)
            end = text.find(delimiter, start + len(delimiter))
            if end == -1:
                raise Exception("Closing delimiter not found")

            if start > 0:
                result.append(TextNode(text[:start], TextType.TEXT))
            result.append(TextNode(text[start + len(delimiter):end], text_type))
            text = text[end + len(delimiter):]

        if text:
            result.append(TextNode(text, TextType.TEXT))

    return result


def extract_markdown_images(text):
    result = []
    if "![" not in text:
        return result
    result = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', text)
    return result

def extract_markdown_links(text):
    result = []
    if "](" not in text:
        return result
    result = re.findall(r'(?<!!)\[([^\]]*)\]\(([^)]+)\)', text)
    return result


def split_nodes_image(old_nodes):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        text = node.text
        
        if extract_markdown_images(text) == []:
            result.append(node)
            continue
        images = extract_markdown_images(text)
        for image in images:
            sections = text.split(f"![{image[0]}]({image[1]})", 1)
            if sections[0] != "":
                result.append(TextNode(sections[0], TextType.TEXT))
            result.append(TextNode(image[0], TextType.IMAGE, image[1]))
            text = sections[1]
        
        if text != "":
            result.append(TextNode(text, TextType.TEXT))
            

    return result

def split_nodes_link(old_nodes):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        text = node.text
        
        if extract_markdown_links(text) == []:
            result.append(node)
            continue
        links = extract_markdown_links(text)
        for link in links:
            sections = text.split(f"[{link[0]}]({link[1]})", 1)
            if sections[0] != "":
                result.append(TextNode(sections[0], TextType.TEXT))
            result.append(TextNode(link[0], TextType.LINK, link[1]))
            text = sections[1]
        
        if text != "":
            result.append(TextNode(text, TextType.TEXT))
            

    return result

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    result = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        if block == "":
            continue
        result.append(block.strip())
    return result

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    parent = ParentNode("div", [])
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            div = "p"
            normalized_block = block.replace("\n", " ")
            parent.children.append(ParentNode(div, text_to_children(normalized_block)))
        elif block_type == BlockType.HEADING:
            m = re.match(r'^(#{1,6})\s', block)
            num = len(m.group(1))
            div = f"h{num}"
            block = re.sub(r'^#{1,6}\s', '', block)
            parent.children.append(ParentNode(div, text_to_children(block)))
        elif block_type == BlockType.CODE:
            block = re.sub(r'^```.*\n', '', block, count=1)
            block = re.sub(r'\n```$', '\n', block, count=1)
            inner_block = LeafNode("code", block)
            parent.children.append(ParentNode("pre", [inner_block]))
        elif block_type == BlockType.QUOTE:
            div = "blockquote"
            lines = [line.lstrip('> ') for line in block.splitlines()]
            block = '\n'.join(lines)
            parent.children.append(ParentNode(div, text_to_children(block)))
        elif block_type == BlockType.UNORDERED_LIST:
            div = "ul"
            list_items = []
            for line in block.splitlines():
                line = line.lstrip("- ")
                list_items.append(ParentNode("li", text_to_children(line)))
            parent.children.append(ParentNode(div, list_items))
        elif block_type == BlockType.ORDERED_LIST:
            div = "ol"
            list_items = []
            for line in block.splitlines():
                line = re.sub(r'^\d+\.\s', '', line)
                list_items.append(ParentNode("li", text_to_children(line)))
            parent.children.append(ParentNode(div, list_items))
        else:
            raise Exception("Unrecogniseable block type")
        
    return parent

def text_to_children(text):
    result = []
    nodes = text_to_textnodes(text)
    for node in nodes:
        result.append(text_node_to_html_node(node))
    return result



