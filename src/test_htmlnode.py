import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        html_node_1 = HTMLNode("h1", "hello", children=None, props={"href": "www.hello.com", "target": "_blank"})
        html_node_2 = HTMLNode("h1", "hello", children=None, props={"href": "www.hello.com", "target": "_blank"})
        self.assertEqual(html_node_1, html_node_2)

    def test_ne(self):
        html_node_1 = HTMLNode("h1", "hello", children=None, props={"href": "www.hello.com", "target": "_blank"})
        html_node_2 = HTMLNode("h1", "hello", children=[], props={"href": "www.hello.com", "target": "_blank"})
        self.assertNotEqual(html_node_1, html_node_2)

    def test_props_to_html(self):
        node = HTMLNode("", "hello", children=None, props={"href": "www.hello.com", "target": "_blank"})
        html = node.props_to_html()
        self.assertEqual(html, ' href="www.hello.com" target="_blank"')

    
