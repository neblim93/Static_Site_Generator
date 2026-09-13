import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from textnode_splitter import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_uneq_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_uneq_texttype(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_uneq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "some url")
        node2 = TextNode("This is a text node", TextType.BOLD, "some other url")
        self.assertNotEqual(node, node2)

    def test_url_none(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node, node2)

    def test_uneq_url_none(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD, "some url")
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})

    def test_invalid_text_type(self):
        node = TextNode("This is a text node", "invalid_type", "https://www.google.com")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    # Delimiter Tests

    def test_single_bold_delimiter(self):
        bold_node = TextNode("This is **a bolded** text node", TextType.TEXT)
        result_nodes = split_nodes_delimiter([bold_node], "**", TextType.BOLD)
        self.assertListEqual(
            result_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("a bolded", TextType.BOLD),
                TextNode(" text node", TextType.TEXT),
            ],
        )

    def test_bold_italic_delimiter(self):
        bold_node = TextNode("This is **a bolded** text node", TextType.TEXT)
        italic_node = TextNode("This is _an italicized_ text node", TextType.TEXT)
        result_nodes = split_nodes_delimiter(
            [bold_node, italic_node], "_", TextType.ITALIC
        )
        self.assertListEqual(
            result_nodes,
            [
                TextNode("This is **a bolded** text node", TextType.TEXT),
                TextNode("This is ", TextType.TEXT),
                TextNode("an italicized", TextType.ITALIC),
                TextNode(" text node", TextType.TEXT),
            ],
        )

    def test_bold_and_italic_delimiter(self):
        bold_node = TextNode("This is **a bolded** text node", TextType.TEXT)
        italic_node = TextNode("This is _an italicized_ text node", TextType.TEXT)
        result_nodes = [bold_node, italic_node]
        result_nodes = split_nodes_delimiter(result_nodes, "**", TextType.BOLD)
        result_nodes = split_nodes_delimiter(result_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            result_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("a bolded", TextType.BOLD),
                TextNode(" text node", TextType.TEXT),
                TextNode("This is ", TextType.TEXT),
                TextNode("an italicized", TextType.ITALIC),
                TextNode(" text node", TextType.TEXT),
            ],
        )

    def test_start_bold_delimiter(self):
        bold_node = TextNode("**This is a bolded** text node", TextType.TEXT)
        result_nodes = split_nodes_delimiter([bold_node], "**", TextType.BOLD)
        self.assertListEqual(
            result_nodes,
            [
                TextNode("This is a bolded", TextType.BOLD),
                TextNode(" text node", TextType.TEXT),
            ],
        )

    def test_end_bold_delimiter(self):
        bold_node = TextNode("This is **a bolded text node**", TextType.TEXT)
        result_nodes = split_nodes_delimiter([bold_node], "**", TextType.BOLD)
        self.assertListEqual(
            result_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("a bolded text node", TextType.BOLD),
            ],
        )

    def test_single_code_delimiter(self):
        code_node = TextNode("This is `a code` text node", TextType.TEXT)
        result_nodes = split_nodes_delimiter([code_node], "`", TextType.CODE)
        self.assertListEqual(
            result_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("a code", TextType.CODE),
                TextNode(" text node", TextType.TEXT),
            ],
        )

    def test_unclosed_code_delimiter(self):
        code_node = TextNode("This is a code` text node", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([code_node], "`", TextType.CODE)

    def test_unchanged_bold_node(self):
        bold_node = TextNode("This is **a bolded** text node", TextType.BOLD)
        result_nodes = split_nodes_delimiter([bold_node], "**", TextType.BOLD)
        self.assertListEqual(
            result_nodes, [TextNode("This is **a bolded** text node", TextType.BOLD)]
        )

    #Image Tests
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_mult_images(self):
        node1 = TextNode(
            "This is text with an ![image1](https://i.imgur.com/image1.png) and another ![second image1](https://i.imgur.com/image12.png)",
            TextType.TEXT,
        )
        node2 = TextNode(
            "This is text with an ![image2](https://i.imgur.com/image2.png) and another ![second image2](https://i.imgur.com/image22.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node1, node2])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image1", TextType.IMAGE, "https://i.imgur.com/image1.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image1", TextType.IMAGE, "https://i.imgur.com/image12.png"),
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image2", TextType.IMAGE, "https://i.imgur.com/image2.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image2", TextType.IMAGE, "https://i.imgur.com/image22.png"),
            ],
            new_nodes,
        )

    def test_split_start_image(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) this is a start image",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" this is a start image", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_end_image(self):
        node = TextNode(
            "this is an end image ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("this is an end image ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_no_image(self):
        node = TextNode(
            "there is no image",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("there is no image", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_not_image(self):
        node = TextNode(
            "this is an end image ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.BOLD,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("this is an end image ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.BOLD),
            ],
            new_nodes,
        )

    #Link Tests
    def test_split_links(self):
        node = TextNode(
            "This is text with an [anchor](https://i.imgur.com/zjjcJKZ) and another [second anchor](https://i.imgur.com/3elNhQu)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("anchor", TextType.LINK, "https://i.imgur.com/zjjcJKZ"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second anchor", TextType.LINK, "https://i.imgur.com/3elNhQu"
                ),
            ],
            new_nodes,
        )

    def test_split_mult_links(self):
        node1 = TextNode(
            "This is text with an [anchor1](https://i.imgur.com/image1) and another [second anchor1](https://i.imgur.com/image12)",
            TextType.TEXT,
        )
        node2 = TextNode(
            "This is text with an [anchor2](https://i.imgur.com/image2) and another [second anchor2](https://i.imgur.com/image22)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node1, node2])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("anchor1", TextType.LINK, "https://i.imgur.com/image1"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second anchor1", TextType.LINK, "https://i.imgur.com/image12"),
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("anchor2", TextType.LINK, "https://i.imgur.com/image2"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second anchor2", TextType.LINK, "https://i.imgur.com/image22"),
            ],
            new_nodes,
        )

    def test_split_start_link(self):
        node = TextNode(
            "[anchor](https://i.imgur.com/zjjcJKZ) this is a start link",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("anchor", TextType.LINK, "https://i.imgur.com/zjjcJKZ"),
                TextNode(" this is a start link", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_end_link(self):
        node = TextNode(
            "this is an end link [anchor](https://i.imgur.com/zjjcJKZ)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("this is an end link ", TextType.TEXT),
                TextNode("anchor", TextType.LINK, "https://i.imgur.com/zjjcJKZ"),
            ],
            new_nodes,
        )

    def test_split_no_link(self):
        node = TextNode(
            "there is no link",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("there is no link", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_not_link(self):
        node = TextNode(
            "this is an end link [anchor](https://i.imgur.com/zjjcJKZ)",
            TextType.BOLD,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("this is an end link [anchor](https://i.imgur.com/zjjcJKZ)", TextType.BOLD),
            ],
            new_nodes,
        )

    #Text to TextNodes

    def test_split_text_with_all_font_types(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes
        )

    def test_split_text_with_start_font(self):
        text = "**This is text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes
        )

    def test_split_text_with_end_font(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)**extratext**"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode("extratext", TextType.BOLD)
            ],
            new_nodes
        )

    def test_split_text_with_start_link(self):
        text = "[link](https://boot.dev) This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            new_nodes
        )

    def test_split_empty_text(self):
        text = ""
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
            ],
            new_nodes
        )

    def test_split_text_font_type_not_closed(self):
        text = "This is **text with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        with self.assertRaises(ValueError):
            text_to_textnodes(text)

    def test_split_text_no_splits(self):
        text = "This is text with an italic word and a code block and an obi wan image(https://i.imgur.com/fJRm4Vk.jpeg) and a link(https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is text with an italic word and a code block and an obi wan image(https://i.imgur.com/fJRm4Vk.jpeg) and a link(https://boot.dev)", TextType.TEXT),
            ],
            new_nodes
        )

if __name__ == "__main__":
    unittest.main()
