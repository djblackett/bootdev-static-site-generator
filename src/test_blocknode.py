import unittest

from blockutils import markdown_to_blocks
from blocknode import BlockType, block_to_block_type


class TestBlockNode(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type(
            "###### Heading 6"), BlockType.HEADING)
        self.assertNotEqual(block_to_block_type(
            "####### Not heading"), BlockType.HEADING)

    def test_block_to_block_type_unordered_list(self):
        self.assertEqual(block_to_block_type(
            "- item 1\n- item 2"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type(
            "- only one item"), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ordered_list_ascending(self):
        self.assertEqual(
            block_to_block_type("1. item 1\n2. item 2\n3. item 3"),
            BlockType.ORDERED_LIST,
        )

    def test_block_to_block_type_ordered_list_not_ascending(self):
        self.assertNotEqual(
            block_to_block_type("1. item 1\n3. item 2\n2. item 3"),
            BlockType.ORDERED_LIST,
        )

    def test_block_to_block_type_code_block(self):
        self.assertEqual(
            block_to_block_type("```\ncode block\n```"),
            BlockType.CODE_BLOCK,
        )

    def test_block_to_block_type_code_block_not_closed(self):
        self.assertNotEqual(
            block_to_block_type("```not closed code block"),
            BlockType.CODE_BLOCK,
        )

    def test_block_to_block_type_quote(self):

        self.assertEqual(
            block_to_block_type("> quoted line\n> another quoted line"),
            BlockType.QUOTE,
        )

    def test_block_to_block_type_quote_not_all_quoted(self):
        self.assertNotEqual(
            block_to_block_type("> quoted line\nnot quoted"),
            BlockType.QUOTE,
        )

    def test_block_to_block_type_paragraph(self):
        self.assertEqual(
            block_to_block_type("Just a normal paragraph."),
            BlockType.PARAGRAPH,
        )
