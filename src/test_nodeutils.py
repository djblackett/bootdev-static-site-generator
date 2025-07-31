import unittest
from nodeutils import extract_markdown_images, extract_markdown_links, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):

    def test_split_nodes_delimiter_basic_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_multiple_delimiters(self):
        node = TextNode("A `code` and `more code` here", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("A ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("more code", TextType.CODE),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_no_delimiter(self):
        node = TextNode("No code here", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [TextNode("No code here", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_unpaired_delimiter_raises(self):
        node = TextNode("This is `broken", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_split_nodes_delimiter_non_text_type_passes_through(self):
        node = TextNode("Not text", TextType.CODE)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [node])

    def test_split_nodes_delimiter_empty_string(self):
        node = TextNode("", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [TextNode("", TextType.TEXT)])

    def test_split_nodes_delimiter_adjacent_delimiters(self):
        node = TextNode("``", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = []
        self.assertEqual(result, expected)

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(text)
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                    ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(result, expected)

    def test_extract_markdown_links_basic(self):
        text = "This is a [link](https://example.com) in text."
        result = extract_markdown_links(text)
        expected = [("link", "https://example.com")]
        self.assertEqual(result, expected)

    def test_extract_markdown_links_multiple(self):
        text = "Links: [Google](https://google.com) and [GitHub](https://github.com)."
        result = extract_markdown_links(text)
        expected = [
            ("Google", "https://google.com"),
            ("GitHub", "https://github.com"),
        ]
        self.assertEqual(result, expected)

    def test_extract_markdown_links_ignores_images(self):
        text = "Image: ![alt](https://img.com/img.png) and [real link](https://real.com)"
        result = extract_markdown_links(text)
        expected = [("real link", "https://real.com")]
        self.assertEqual(result, expected)

    def test_extract_markdown_links_no_links(self):
        text = "No links here!"
        result = extract_markdown_links(text)
        expected = []
        self.assertEqual(result, expected)

    def test_extract_markdown_links_empty_text(self):
        text = ""
        result = extract_markdown_links(text)
        expected = []
        self.assertEqual(result, expected)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ], new_nodes,
        )

    def test_split_nodes_image_single_image(self):
        node = TextNode(
            "Here is an ![alt text](https://example.com/image.png) in the text.",
            TextType.TEXT,
        )
        result = split_nodes_image([node])
        expected = [
            TextNode("Here is an ", TextType.TEXT),
            TextNode("alt text", TextType.IMAGE,
                     "https://example.com/image.png"),
            TextNode(" in the text.", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_image_multiple_images(self):
        node = TextNode(
            "First ![one](url1) and second ![two](url2) done.",
            TextType.TEXT,
        )
        result = split_nodes_image([node])
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("one", TextType.IMAGE, "url1"),
            TextNode(" and second ", TextType.TEXT),
            TextNode("two", TextType.IMAGE, "url2"),
            TextNode(" done.", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_image_no_image(self):
        node = TextNode("Just plain text.", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [TextNode("Just plain text.", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_split_nodes_image_image_at_start(self):
        node = TextNode("![start](url) then text", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("start", TextType.IMAGE, "url"),
            TextNode(" then text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_image_image_at_end(self):
        node = TextNode("Text then ![end](url)", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("Text then ", TextType.TEXT),
            TextNode("end", TextType.IMAGE, "url"),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_image_adjacent_images(self):
        node = TextNode("![a](u1)![b](u2)", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("a", TextType.IMAGE, "u1"),
            TextNode("b", TextType.IMAGE, "u2"),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_image_empty_alt_and_url(self):
        node = TextNode("![  ]()", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("  ", TextType.IMAGE, ""),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_image_non_text_type(self):
        node = TextNode("![not shown](url)", TextType.IMAGE, "url")
        result = split_nodes_image([node])
        self.assertEqual(result, [node])

    def test_split_nodes_image_empty_string(self):
        node = TextNode("", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [TextNode("", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_split_nodes_link_basic(self):
        node = TextNode(
            "This is a [link](https://example.com) in text.", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" in text.", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_link_multiple_links(self):
        node = TextNode(
            "Links: [Google](https://google.com) and [GitHub](https://github.com).", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("Links: ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://google.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("GitHub", TextType.LINK, "https://github.com"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_link_no_links(self):
        node = TextNode("No links here!", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [TextNode("No links here!", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_split_nodes_link_ignores_images(self):
        node = TextNode(
            "Image: ![alt](https://img.com/img.png) and [real link](https://real.com)", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode(
                "Image: ![alt](https://img.com/img.png) and ", TextType.TEXT),
            TextNode("real link", TextType.LINK, "https://real.com"),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_link_link_at_start(self):
        node = TextNode("[start](url) then text", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("start", TextType.LINK, "url"),
            TextNode(" then text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_link_link_at_end(self):
        node = TextNode("Text then [end](url)", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("Text then ", TextType.TEXT),
            TextNode("end", TextType.LINK, "url"),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_link_adjacent_links(self):
        node = TextNode("[a](u1)[b](u2)", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("a", TextType.LINK, "u1"),
            TextNode("b", TextType.LINK, "u2"),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_link_empty_link_text_and_url(self):
        node = TextNode("[]()", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("", TextType.LINK, ""),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_link_non_text_type(self):
        node = TextNode("[not shown](url)", TextType.LINK, "url")
        result = split_nodes_link([node])
        self.assertEqual(result, [node])

    def test_split_nodes_link_empty_string(self):
        node = TextNode("", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [TextNode("", TextType.TEXT)]
        self.assertEqual(result, expected)


class TestTextToTextNodes(unittest.TestCase):

    def test_text_to_textnodes_plain_text(self):
        text = "Just some plain text."
        result = text_to_textnodes(text)
        expected = [TextNode("Just some plain text.", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_text_to_textnodes_code(self):
        text = "This is `code`."
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnodes_bold(self):
        text = "This is **bold** text."
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnodes_italic(self):
        text = "This is _italic_ text."
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text.", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnodes_image(self):
        text = "Here is an ![alt](url) image."
        result = text_to_textnodes(text)
        expected = [
            TextNode("Here is an ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "url"),
            TextNode(" image.", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnodes_link(self):
        text = "A [link](url) here."
        result = text_to_textnodes(text)
        expected = [
            TextNode("A ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
            TextNode(" here.", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnodes_all_features(self):
        text = "This is **bold** and _italic_ with `code`, ![img](url), and [link](url)."
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(", ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "url"),
            TextNode(", and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnodes_empty_string(self):
        text = ""
        result = text_to_textnodes(text)
        expected = []
        self.assertEqual(result, expected)

    def test_text_to_textnodes_adjacent_features(self):
        text = "**bold**_italic_`code`"
        result = text_to_textnodes(text)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnodes_image_and_link_adjacent(self):
        text = "![img](url)[link](url2)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("img", TextType.IMAGE, "url"),
            TextNode("link", TextType.LINK, "url2"),
        ]
        self.assertEqual(result, expected)
