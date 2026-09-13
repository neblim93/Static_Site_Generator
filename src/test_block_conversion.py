import unittest

from block_conversion import BlockType, block_to_block_type
from markdown_extraction import markdown_to_blocks


class TestConversion(unittest.TestCase):
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

    def test_markdown_with_extra_lines_to_blocks(self):
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

    def test_markdown_to_blocks_empty(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    # Block Tests
    def test_block_type(self):
        block = "This is a normal paragraph\n with a second line in it"
        block_type_test = block_to_block_type(block)
        self.assertEqual(block_type_test, BlockType.PARAGRAPH)

    def test_block_type_heading(self):
        block_1 = "# This is a normal paragraph\n with a second line in it"
        block_2 = "##### This is a normal paragraph\n with a second line in it"
        block_3 = "#This is a normal paragraph\n with a second line in it"
        result_1 = block_to_block_type(block_1)
        result_2 = block_to_block_type(block_2)
        result_3 = block_to_block_type(block_3)
        self.assertListEqual(
            [result_1, result_2, result_3],
            [BlockType.HEADING, BlockType.HEADING, BlockType.PARAGRAPH],
        )

    def test_block_type_code(self):
        block_1 = "```\nThis is a normal paragraph\n with a second line in it```"
        block_2 = "```\nThis is a normal paragraph\n with a second line in it"
        block_3 = "```This is a normal paragraph\n with a second line in it```"
        result_1 = block_to_block_type(block_1)
        result_2 = block_to_block_type(block_2)
        result_3 = block_to_block_type(block_3)
        self.assertListEqual(
            [result_1, result_2, result_3],
            [BlockType.CODE, BlockType.PARAGRAPH, BlockType.PARAGRAPH],
        )

    def test_block_type_quote(self):
        block_1 = ">This is a normal paragraph\n>with a second line in it"
        block_2 = "> This is a normal paragraph\n> with a second line in it"
        block_3 = "This is a normal paragraph\n> with a second line in it"
        result_1 = block_to_block_type(block_1)
        result_2 = block_to_block_type(block_2)
        result_3 = block_to_block_type(block_3)
        self.assertListEqual(
            [result_1, result_2, result_3],
            [BlockType.QUOTE, BlockType.QUOTE, BlockType.PARAGRAPH],
        )

    def test_block_type_unordered_list(self):
        block_1 = "- Item_1\n- Item_3\n- Item_2"
        block_2 = "-Item_1\n- Item_3\n- Item_2"
        block_3 = "- Item_1\n - Item_3\n- Item_2"
        result_1 = block_to_block_type(block_1)
        result_2 = block_to_block_type(block_2)
        result_3 = block_to_block_type(block_3)
        self.assertListEqual(
            [result_1, result_2, result_3],
            [BlockType.UNORDERED_LIST, BlockType.PARAGRAPH, BlockType.PARAGRAPH],
        )

    def test_block_type_ordered_list(self):
        block_1 = "1. Item_1\n2. Item_2\n3. Item_3"
        block_2 = "1. Item_1\n3. Item_2\n3. Item_3"
        block_3 = "1.Item_1\n2. Item_2\n3. Item_3"
        result_1 = block_to_block_type(block_1)
        result_2 = block_to_block_type(block_2)
        result_3 = block_to_block_type(block_3)
        self.assertListEqual(
            [result_1, result_2, result_3],
            [BlockType.ORDERED_LIST, BlockType.PARAGRAPH, BlockType.PARAGRAPH],
        )


if __name__ == "__main__":
    unittest.main()
