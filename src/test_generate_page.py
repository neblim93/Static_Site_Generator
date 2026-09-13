import unittest

from generate_page import extract_title


class TestExtraction(unittest.TestCase):
    def test_header_extraction(self):
        markdown = "# This is an h1 header\na second line of text"
        header = extract_title(markdown)
        self.assertEqual("This is an h1 header", header)

    def test_header_extraction_not_present(self):
        markdown = "### This is an h1 header\na second line of text"
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_header_extraction_whitespace(self):
        markdown = "   # This is an h1 header   \na second line of text"
        header = extract_title(markdown)
        self.assertEqual("This is an h1 header", header)

    def test_header_multiple(self):
        markdown = "# This is an h1 header\n#a second line of text"
        header = extract_title(markdown)
        self.assertEqual("This is an h1 header", header)

    def test_header_following_line(self):
        markdown = "This is text\na second line of text\n# This is an h1 header"
        header = extract_title(markdown)
        self.assertEqual("This is an h1 header", header)

    def test_header_extraction_no_headers(self):
        markdown = "This is an h1 header\na second line of text"
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_header_extraction_no_text(self):
        markdown = ""
        with self.assertRaises(ValueError):
            extract_title(markdown)



if __name__ == "__main__":
    unittest.main()
