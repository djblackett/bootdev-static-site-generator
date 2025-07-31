import logging
import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        textnode = TextNode("Hello there", TextType.LINK,
                            "www.generalkenobi.fett")
        textnode2 = TextNode("Hello there", TextType.IMAGE,
                             "www.generalkenobi.fett")
        self.assertNotEqual(textnode, textnode2)

    def test_repr(self):
        textnode = TextNode("Hello there", TextType.LINK,
                            "www.generalkenobi.fett")
        self.assertEqual(
            str(textnode), "TextNode(('Hello there', 'link', 'www.generalkenobi.fett'))")

    def test_repr_fail(self):
        textnode = TextNode("Hello there", TextType.LINK,
                            "www.generalkenobi.fett")
        self.assertNotEqual(
            str(textnode), "TextNode(('Hello there', 'link', None))")

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)

        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")

    def test_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")

    def test_code(self):
        node = TextNode("print('hi')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hi')")

    def test_link(self):
        node = TextNode("Google", TextType.LINK, "https://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Google")
        self.assertEqual(html_node.props, {"href": "https://google.com"})

    def test_image(self):
        node = TextNode("Alt text", TextType.IMAGE,
                        "https://img.com/img.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertIsNone(html_node.value)
        self.assertEqual(html_node.props, {
            "src": "https://img.com/img.png", "alt": "Alt text"})

    def test_invalid_type(self):
        class DummyType:
            pass
        node = TextNode("Invalid", DummyType()) # type: ignore
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)


if __name__ == "__main__":
    unittest.main()
