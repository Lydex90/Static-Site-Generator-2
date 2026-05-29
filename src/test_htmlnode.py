import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "Alls secs mai couen", None, {
                                                        "href": "https://www.google.com",
                                                        "target": "_blank",
                                                        })
        node2 = HTMLNode("p", "Alls secs mai couen", None, {
                                                        "href": "https://www.google.com",
                                                        "target": "_blank",
                                                        })
        self.assertEqual(node.props_to_html(), node2.props_to_html())

    def test_expected_output_props(self):
        node = HTMLNode("p", "Alls secs mai couen", None, {
                                                        "href": "https://www.google.com",
                                                        "target": "_blank",
                                                        })
        output = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(),  output)

    def test_to_html(self):
        node = HTMLNode("p", "Alls secs mai couen", None, {
        "href": "https://www.google.com",
        "target": "_blank",
        })
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "I'm MEGABOLD")
        self.assertEqual(node.to_html(), "<b>I'm MEGABOLD</b>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_with_children_2(self):
        node = ParentNode("p",[
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
            ],)
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

if __name__ == "__main__":
    unittest.main()