import unittest

from blocktype import block_to_block_type, BlockType

class TestTextNode(unittest.TestCase):

    def test_heading_single(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)

    def test_heading_multiple_hashes(self):
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)

    def test_heading_too_many_hashes(self):
        self.assertEqual(block_to_block_type("####### Too many"), BlockType.PARAGRAPH)

    def test_code_block(self):
        self.assertEqual(block_to_block_type("```python"), BlockType.CODE)

    def test_code_not_inline(self):
        self.assertEqual(block_to_block_type("some ``` code"), BlockType.PARAGRAPH)

    def test_quote(self):
        self.assertEqual(block_to_block_type("> A quote"), BlockType.QUOTE)

    def test_unordered_list_dash(self):
        self.assertEqual(block_to_block_type("- item"), BlockType.UNORDERED_LIST)

    def test_unordered_list_asterisk(self):
        self.assertEqual(block_to_block_type("* item"), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. item"), BlockType.ORDERED_LIST)

    def test_plain_text_is_paragraph(self):
        self.assertEqual(block_to_block_type("just plain text"), BlockType.PARAGRAPH)




if __name__ == "__main__":
    unittest.main()