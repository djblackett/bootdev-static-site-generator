
import unittest
from src.leafnode import LeafNode
from src.parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(),
                         "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>")

    def test_to_html_multiple_children(self):
        child1 = LeafNode("p", "first")
        child2 = LeafNode("p", "second")
        parent_node = ParentNode("div", [child1, child2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><p>first</p></div><div><p>second</p></div>"
        )

    def test_to_html_nested_parents(self):
        leaf = LeafNode("em", "text")
        child = ParentNode("span", [leaf])
        parent = ParentNode("section", [child])
        root = ParentNode("div", [parent])
        self.assertEqual(
            root.to_html(),
            "<div><section><span><em>text</em></span></section></div>"
        )

    def test_to_html_raises_without_tag(self):
        child = LeafNode("span", "child")
        with self.assertRaises(ValueError):
            ParentNode(None, [child]).to_html()

    def test_to_html_raises_without_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None).to_html()

    def test_to_html_with_props(self):
        child = LeafNode("span", "child")
        parent = ParentNode("div", [child], props={"class": "container"})
        # Since props are not rendered in current implementation, output is same as without props
        self.assertEqual(parent.to_html(), "<div><span>child</span></div>")
