

import unittest

from blockutils import markdown_to_blocks


class TestBlockUtils(unittest.TestCase):
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

    def test_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_only_whitespace(self):
        md = "   \n   \n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_single_paragraph(self):
        md = "This is a single paragraph."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single paragraph."])

    def test_multiple_paragraphs(self):
        md = "First paragraph.\n\nSecond paragraph."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First paragraph.", "Second paragraph."])

    def test_paragraph_with_blank_lines(self):
        md = "First paragraph.\n\n\nSecond paragraph."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First paragraph.", "Second paragraph."])

    def test_list_block(self):
        md = "- Item 1\n- Item 2\n- Item 3"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["- Item 1\n- Item 2\n- Item 3"])

    def test_mixed_blocks(self):
        md = "# Heading\n\nParagraph text\n\n- List item 1\n- List item 2"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading",
                "Paragraph text",
                "- List item 1\n- List item 2",
            ],
        )

    def test_trailing_and_leading_newlines(self):
        md = "\n\nFirst block\n\nSecond block\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First block", "Second block"])

    def test_block_with_internal_blank_lines(self):
        md = "Line 1\n\n\nLine 2"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Line 1", "Line 2"])
