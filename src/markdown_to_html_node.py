from blockutils import *
from blocknode import *
from htmlnode import HTMLNode
from leafnode import LeafNode
from nodeutils import text_to_textnodes
from parentnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node


def markdown_to_html_node(markdown: str):
    blocks: list[str] = markdown_to_blocks(markdown)
    html_nodes: list[HTMLNode] = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:

            title, level = get_heading_level(block)
            html_nodes.append(
                ParentNode(f"h{level}", children=text_to_children(title), props=None))

        elif block_type == BlockType.CODE_BLOCK:
            html_nodes.append(
                code_to_html_node(block))
        elif block_type == BlockType.ORDERED_LIST:
            # If it's an ordered list, create an <ol> node with <li> children
            html_nodes.append(
                ParentNode("ol", children=get_ol_children(block), props=None))
        elif block_type == BlockType.UNORDERED_LIST:
            # If it's an unordered list, create a <ul> node with <li> children
            html_nodes.append(
                ParentNode("ul", children=get_ul_children(block), props=None))
        elif block_type == BlockType.QUOTE:
            # If it's a quote, create a <blockquote> node (children not handled)
            html_nodes.append(
                quote_to_html_node(block))
        else:
            # For any other block type, default to a paragraph
            html_nodes.append(paragraph_to_html_node(block))

    html_element = ParentNode("div", children=html_nodes, props=None)
    return html_element


def get_heading_level(block: str):
    bup = block.split(" ", maxsplit=1)
    return bup[1], len(bup[0])


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children=children)


def quote_to_html_node(block):
    lines = block.split("\n")
    lines = [line[2:].strip(">") for line in lines]
    quote_text = " ".join(lines)
    children = text_to_children(quote_text)
    return ParentNode("blockquote", children=children, props=None)


def get_ol_children(block: str):
    items = block.split("\n")
    items = [item[3:] for item in items]
    li_nodes = [ParentNode("li", children=text_to_children(item), props=None)
                for item in items]
    return li_nodes


def get_ul_children(block: str):
    items = block.split("\n")
    items = [item[2:] for item in items]
    li_nodes = [ParentNode("li", children=text_to_children(item), props=None)
                for item in items]
    return li_nodes


def text_to_children(text: str):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
    return html_nodes


def code_to_html_node(text):
    clean = text.strip('```').removeprefix('\n')

    rawChild = TextNode(clean, TextType.TEXT)
    childNode = text_node_to_html_node(rawChild)
    pre = ParentNode("pre", children=[ParentNode(
        "code", children=[childNode], props=None)], props=None)
    return pre
