import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
    new: list[TextNode] = []
    for old in old_nodes:
        if old.text_type != TextType.TEXT:
            new.append(old)
            continue

        if old.text.count(delimiter) % 2 == 1 or old.text.count(delimiter) == 1:
            raise ValueError("Delimiter must be used in pairs")

        if old.text.count(delimiter) == 0:
            new.append(old)
            continue

        parts = old.text.split(delimiter)

        inside = old.text.startswith(delimiter)

        for part in parts:
            if len(part) == 0:
                # inside = not inside
                continue
            if inside:
                new.append(TextNode(part, text_type))
                inside = not inside
            else:
                new.append(TextNode(part, TextType.TEXT))
                inside = not inside
    return new


def extract_markdown_images(text):
    # images
    imgrx = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(imgrx, text)
    return [(match[0], match[1]) for match in matches]


def extract_markdown_links(text):
    linkrx = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(linkrx, text)
    return [(match[0], match[1]) for match in matches]


def split_nodes_image(old_nodes: list[TextNode]):
    new_nodes = []
    imgrx = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # If no images found, keep the original node
        if not re.search(imgrx, node.text):
            new_nodes.append(node)
            continue

        # Split the text around image markdown
        current_text = node.text

        while True:
            match = re.search(imgrx, current_text)
            if not match:
                # Add remaining text if any
                if current_text:
                    new_nodes.append(TextNode(current_text, TextType.TEXT))
                break

            # Add text before the image (if any)
            before_text = current_text[:match.start()]
            if before_text:
                new_nodes.append(TextNode(before_text, TextType.TEXT))

            # Add the image node
            alt_text = match.group(1)
            url = match.group(2)
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))

            # Continue with the text after the image
            current_text = current_text[match.end():]

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # If no links found, keep the original node
        if not re.search(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", node.text):
            new_nodes.append(node)
            continue

        # Split the text around link markdown
        current_text = node.text

        while True:
            match = re.search(
                r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", current_text)
            if not match:
                # Add remaining text if any
                if current_text:
                    new_nodes.append(TextNode(current_text, TextType.TEXT))
                break
            # Add text before the link (if any)
            before_text = current_text[:match.start()]
            if before_text:
                new_nodes.append(TextNode(before_text, TextType.TEXT))

            # Add the link node
            link_text = match.group(1)
            url = match.group(2)
            new_nodes.append(TextNode(link_text, TextType.LINK, url))

            # Continue with the text after the link
            current_text = current_text[match.end():]

    return new_nodes


def text_to_textnodes(text):
    nodes = []
    if not text:
        return nodes

    nodes.append(TextNode(text, TextType.TEXT))
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

    return nodes

    # This created nodes for EVERYTHING in the split result

    # node = TextNode(
    #     "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
    #     TextType.TEXT,
    # )
    # new_nodes = split_nodes_image([node])
    # for node in new_nodes:
    #     print(node)  # For debugging purposes, can be removed later


text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
text1 = "**bold**_italic_`code`"
node_list = text_to_textnodes(text1)
for node in node_list:
    print(node)
