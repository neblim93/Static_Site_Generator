import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_multiple_props(self):
        node = HTMLNode(
            tag="a",
            value="Click me!",
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com" target="_blank"',
        )

    def test_props_to_html_none(self):
        node = HTMLNode(tag="p", value="Hello, world!")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty_dict(self):
        node = HTMLNode(tag="p", value="Hello, world!", props={})
        self.assertEqual(node.props_to_html(), "")

    def test_values(self):
        node = HTMLNode(tag="h1", value="Title")
        self.assertEqual(node.tag, "h1")
        self.assertEqual(node.value, "Title")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    #LeafNode Tests

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_props(self):
        node = LeafNode("a", "Check those google props", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Check those google props</a>')

    def test_leaf_to_html_no_value(self):
       node = LeafNode(tag = "a", value = None, props = {"href": "https://www.google.com"})
       with self.assertRaises(ValueError):
           node.to_html()

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(tag = None, value = "something here", props = {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), 'something here')


    #ParentNode Tests
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_mult_children(self):
        child_node_1 = LeafNode("span", "child")
        child_node_2 = LeafNode("span2", "child2")
        parent_node = ParentNode("div", [child_node_1, child_node_2])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span><span2>child2</span2></div>")


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_mult_grandchildren(self):
        grandchild_node_1 = LeafNode("b", "grandchild_1")
        grandchild_node_2 = LeafNode("a", "grandchild_2")
        child_node = ParentNode("span", [grandchild_node_1, grandchild_node_2])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild_1</b><a>grandchild_2</a></span></div>",
        )

    def test_to_html_with_grandchildren_props(self):
        grandchild_node = LeafNode("b", "grandchild", {"href": "https://www.google.com"})
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node], {"href": "https://www.bing.com"})
        self.assertEqual(
            parent_node.to_html(),
            '<div href="https://www.bing.com"><span><b href="https://www.google.com">grandchild</b></span></div>',
        )

    def test_to_html_with_no_children(self):
        parent_node = ParentNode("span", None, {"href": "https://www.bing.com"})
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_without_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_empty_children_list(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_to_html_with_raw_text_child(self):
        child_node = LeafNode(None, "Hello world")
        parent_node = ParentNode("p", [child_node])
        self.assertEqual(parent_node.to_html(), "<p>Hello world</p>")


if __name__ == "__main__":
    unittest.main()
