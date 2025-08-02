from blockutils import *
from blocknode import *
from codenode import CodeNode
from htmlnode import HTMLNode
from leafnode import LeafNode
from nodeutils import text_to_textnodes
from parentnode import ParentNode
from textnode import text_node_to_html_node


def markdown_to_html_node(markdown: str):
    # Split the markdown text into blocks (paragraphs, headings, etc.)
    blocks: list[str] = markdown_to_blocks(markdown)
    # Prepare a list to hold HTMLNode objects for each block
    html_nodes: list[HTMLNode] = []
    # Iterate through each block to determine its type and convert accordingly
    for block in blocks:
        # Determine the type of the current block (heading, paragraph, etc.)
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            # If it's a heading, extract the title and heading level
            title, level = get_heading_level(block)
            # Create an HTMLNode for the heading (e.g., <h1>, <h2>, etc.)
            html_nodes.append(
                ParentNode(f"h{level}", children=text_to_children(block), props=None))

        elif block_type == BlockType.CODE_BLOCK:
            # If it's a code block, wrap the block in a code block tag (incorrectly uses "```")
            # come back to this ***********
            html_nodes.append(
                CodeNode(block))
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
                ParentNode("blockquote", children=text_to_children(block), props=None))
        else:
            # For any other block type, default to a paragraph
            html_nodes.append(paragraph_block_to_node(block))

    # Concatenate the HTML for each node into a single string (not used)
    # html_string = ""
    # for node in html_nodes:
    #     html_string += node.to_html()
    # Wrap all nodes in a parent <div> node and return it
    html_element = ParentNode("div", children=html_nodes, props=None)
    return html_element


def get_heading_level(block: str):
    bup = block.split(" ", maxsplit=1)
    return bup[1], len(bup[0])


def code_block_to_html(block: str):
    pass


def paragraph_to_html(block: str):

    paragraphs = block.strip().split("\n\n")
    results = []
    for i, paragraph in enumerate(paragraphs):
        results.append(paragraph_to_html_single(paragraph))
    return ParentNode("div", children=results)


def paragraph_block_to_node(block: str) -> HTMLNode:
    # Step 1: Flatten the paragraph (convert single \n to spaces)
    flattened = re.sub(r"(?<!\n)\n(?!\n)", " ", block.strip())

    # Step 2: Convert to text nodes, then to inline HTMLNodes
    children = text_to_children(flattened)

    # Step 3: Wrap everything in a single <p> node
    return ParentNode("p", children=children)


def paragraph_to_html_single(block: str):

    block = re.sub(r"(?<!\n)\n(?!\n)", " ", block.strip())
    block = re.sub(r"\s+", " ", block)

    return ParentNode("p", children=text_to_children(block))


def get_ol_children(block: str):
    items = block.split("\n")
    items = [item[3:] for item in items]
    li_nodes = [HTMLNode("li", item, children=None, props=None)
                for item in items]
    return li_nodes


def get_ul_children(block: str):
    items = block.split("\n")
    items = [item[2:] for item in items]
    li_nodes = [HTMLNode("li", item, children=None, props=None)
                for item in items]
    return li_nodes


def text_to_children(text: str):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
    return html_nodes


def unordered_list_to_html(block: str):
    items = block.split("\n")
    items = [f"<li>{item}</li>" for item in items]
    return f"<ul>{''.join(items)}</ul>"


# def get_quote_children(block: str):
#     items = block.split("\n")
#     items = [HTMLNode("", item[2:], children=None, props=None)
#              for item in items]
#     return items

md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

md2 = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

# markdown_to_html_node(md)
html = markdown_to_html_node(md)
# print(html.to_html())

html2 = markdown_to_html_node(md2)
# print(html2.to_html())
