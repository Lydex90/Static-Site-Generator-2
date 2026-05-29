import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from markdwn_to_text import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks, markdown_to_html_node

class TestTextNode(unittest.TestCase):

    # split_nodes_delimiter
    def test_1(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])

    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])

    def test_split_bold(self):
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in the middle", TextType.TEXT),
        ])

    def test_split_italic(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(result, [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ])

    def test_non_text_node_passed_through(self):
        node = TextNode("already bold", TextType.BOLD)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [TextNode("already bold", TextType.BOLD)])

    def test_missing_closing_delimiter_raises(self):
        node = TextNode("This is `unclosed code", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_delimiter_at_start(self):
        node = TextNode("`code` at the start", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("code", TextType.CODE),
            TextNode(" at the start", TextType.TEXT),
        ])

    def test_mixed_list_multiple_nodes(self):
        nodes = [
            TextNode("Hello `world` foo", TextType.TEXT),
            TextNode("No delimiter here", TextType.TEXT),
        ]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("Hello ", TextType.TEXT),
            TextNode("world", TextType.CODE),
            TextNode(" foo", TextType.TEXT),
            TextNode("No delimiter here", TextType.TEXT),
        ])

    def test_list_with_mixed_types(self):
        nodes = [
            TextNode("already bold", TextType.BOLD),
            TextNode("has `code` here", TextType.TEXT),
            TextNode("also italic", TextType.ITALIC),
        ]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("already bold", TextType.BOLD),
            TextNode("has ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" here", TextType.TEXT),
            TextNode("also italic", TextType.ITALIC),
        ])

    def test_list_multiple_bold_nodes(self):
        nodes = [
            TextNode("**bold** start", TextType.TEXT),
            TextNode("end **bold**", TextType.TEXT),
        ]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(result, [
            TextNode("bold", TextType.BOLD),
            TextNode(" start", TextType.TEXT),
            TextNode("end ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ])

    def test_list_one_invalid_raises(self):
        nodes = [
            TextNode("valid `code` here", TextType.TEXT),
            TextNode("invalid `unclosed", TextType.TEXT),
        ]
        with self.assertRaises(Exception):
            split_nodes_delimiter(nodes, "`", TextType.CODE)

    # extract_markdown_images
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_single_image(self):
        matches = extract_markdown_images("![alt](https://example.com/img.png)")
        self.assertListEqual([("alt", "https://example.com/img.png")], matches)

    def test_extract_multiple_images(self):
        matches = extract_markdown_images("![cat](https://cats.com/cat.png) and ![dog](https://dogs.com/dog.png)")
        self.assertListEqual([("cat", "https://cats.com/cat.png"), ("dog", "https://dogs.com/dog.png")], matches)

    def test_extract_image_empty_alt(self):
        matches = extract_markdown_images("![](https://example.com/img.png)")
        self.assertListEqual([("", "https://example.com/img.png")], matches)

    def test_extract_image_no_images(self):
        matches = extract_markdown_images("This is plain text with no images")
        self.assertListEqual([], matches)

    def test_extract_image_does_not_match_links(self):
        matches = extract_markdown_images("Here is a [link](https://example.com) not an image")
        self.assertListEqual([], matches)

    # extract_markdown_links
    def test_extract_single_link(self):
        matches = extract_markdown_links("Visit [OpenAI](https://openai.com) for more")
        self.assertListEqual([("OpenAI", "https://openai.com")], matches)

    def test_extract_multiple_links(self):
        matches = extract_markdown_links("[Google](https://google.com) and [GitHub](https://github.com)")
        self.assertListEqual([("Google", "https://google.com"), ("GitHub", "https://github.com")], matches)

    def test_extract_link_empty_text(self):
        matches = extract_markdown_links("[](https://example.com)")
        self.assertListEqual([("", "https://example.com")], matches)

    def test_extract_link_no_links(self):
        matches = extract_markdown_links("No links here, just text")
        self.assertListEqual([], matches)

    def test_extract_link_does_not_match_images(self):
        matches = extract_markdown_links("Here is an ![image](https://example.com/img.png) not a link")
        self.assertListEqual([], matches)

    # split_nodes_image
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
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_images_no_images(self):
        node = TextNode("Just plain text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("Just plain text", TextType.TEXT)], new_nodes)

    def test_split_images_image_only(self):
        node = TextNode("![alt](https://example.com/img.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("alt", TextType.IMAGE, "https://example.com/img.png")],
            new_nodes,
        )

    def test_split_images_image_at_start(self):
        node = TextNode("![logo](https://example.com/logo.png) some text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("logo", TextType.IMAGE, "https://example.com/logo.png"),
                TextNode(" some text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_image_at_end(self):
        node = TextNode("some text ![logo](https://example.com/logo.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("some text ", TextType.TEXT),
                TextNode("logo", TextType.IMAGE, "https://example.com/logo.png"),
            ],
            new_nodes,
        )

    def test_split_images_multiple_nodes_input(self):
        nodes = [
            TextNode("![a](https://example.com/a.png)", TextType.TEXT),
            TextNode("plain", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("a", TextType.IMAGE, "https://example.com/a.png"),
                TextNode("plain", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_skips_non_text_type(self):
        node = TextNode("![a](https://example.com/a.png)", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("![a](https://example.com/a.png)", TextType.BOLD)],
            new_nodes,
        )

    def test_split_images_adjacent_images(self):
        node = TextNode(
            "![a](https://example.com/a.png)![b](https://example.com/b.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("a", TextType.IMAGE, "https://example.com/a.png"),
                TextNode("b", TextType.IMAGE, "https://example.com/b.png"),
            ],
            new_nodes,
        )

    def test_split_images_empty_alt_text(self):
        node = TextNode("before ![](https://example.com/img.png) after", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("before ", TextType.TEXT),
                TextNode("", TextType.IMAGE, "https://example.com/img.png"),
                TextNode(" after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_empty_input_list(self):
        new_nodes = split_nodes_image([])
        self.assertListEqual([], new_nodes)

    def test_split_images_preserves_order_across_mixed_nodes(self):
        nodes = [
            TextNode("text ![x](https://example.com/x.png) more", TextType.TEXT),
            TextNode("no images here", TextType.TEXT),
            TextNode("![y](https://example.com/y.png)", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("text ", TextType.TEXT),
                TextNode("x", TextType.IMAGE, "https://example.com/x.png"),
                TextNode(" more", TextType.TEXT),
                TextNode("no images here", TextType.TEXT),
                TextNode("y", TextType.IMAGE, "https://example.com/y.png"),
            ],
            new_nodes,
        )

    # split_nodes_link
    def test_split_links_basic(self):
        node = TextNode(
            "This is text with a [link](https://example.com) and another [second link](https://example.org)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://example.org"),
            ],
            new_nodes,
        )

    def test_split_links_no_links(self):
        node = TextNode("Just plain text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("Just plain text", TextType.TEXT)], new_nodes)

    def test_split_links_link_only(self):
        node = TextNode("[click here](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("click here", TextType.LINK, "https://example.com")],
            new_nodes,
        )

    def test_split_links_link_at_start(self):
        node = TextNode("[click](https://example.com) some text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("click", TextType.LINK, "https://example.com"),
                TextNode(" some text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_link_at_end(self):
        node = TextNode("some text [click](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("some text ", TextType.TEXT),
                TextNode("click", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

    def test_split_links_adjacent_links(self):
        node = TextNode(
            "[a](https://example.com)[b](https://example.org)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("a", TextType.LINK, "https://example.com"),
                TextNode("b", TextType.LINK, "https://example.org"),
            ],
            new_nodes,
        )

    def test_split_links_skips_non_text_type(self):
        node = TextNode("[a](https://example.com)", TextType.BOLD)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("[a](https://example.com)", TextType.BOLD)],
            new_nodes,
        )

    def test_split_links_empty_anchor_text(self):
        node = TextNode("before [](https://example.com) after", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("before ", TextType.TEXT),
                TextNode("", TextType.LINK, "https://example.com"),
                TextNode(" after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_empty_input_list(self):
        new_nodes = split_nodes_link([])
        self.assertListEqual([], new_nodes)

    def test_split_links_preserves_order_across_mixed_nodes(self):
        nodes = [
            TextNode("text [x](https://example.com) more", TextType.TEXT),
            TextNode("no links here", TextType.TEXT),
            TextNode("[y](https://example.org)", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("text ", TextType.TEXT),
                TextNode("x", TextType.LINK, "https://example.com"),
                TextNode(" more", TextType.TEXT),
                TextNode("no links here", TextType.TEXT),
                TextNode("y", TextType.LINK, "https://example.org"),
            ],
            new_nodes,
        )

    # New tests
    def test_text_to_nodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
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
            text_to_textnodes(text)
        )
    def test_plain_text_only(self):
        text = "Just plain text with no markdown"
        self.assertListEqual(
            [TextNode("Just plain text with no markdown", TextType.TEXT)],
            text_to_textnodes(text)
        )

    def test_bold_only(self):
        text = "**bold**"
        self.assertListEqual(
            [TextNode("bold", TextType.BOLD)],
            text_to_textnodes(text)
        )

    def test_italic_only(self):
        text = "_italic_"
        self.assertListEqual(
            [TextNode("italic", TextType.ITALIC)],
            text_to_textnodes(text)
        )

    def test_code_only(self):
        text = "`code block`"
        self.assertListEqual(
            [TextNode("code block", TextType.CODE)],
            text_to_textnodes(text)
        )

    def test_image_only(self):
        text = "![alt text](https://example.com/img.png)"
        self.assertListEqual(
            [TextNode("alt text", TextType.IMAGE, "https://example.com/img.png")],
            text_to_textnodes(text)
        )

    def test_link_only(self):
        text = "[click here](https://example.com)"
        self.assertListEqual(
            [TextNode("click here", TextType.LINK, "https://example.com")],
            text_to_textnodes(text)
        )

    def test_bold_and_italic(self):
        text = "**bold** and _italic_"
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            text_to_textnodes(text)
        )

    def test_multiple_of_same_type(self):
        text = "**one** and **two** and **three**"
        self.assertListEqual(
            [
                TextNode("one", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("two", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("three", TextType.BOLD),
            ],
            text_to_textnodes(text)
        )

    def test_image_and_link(self):
        text = "![img](https://example.com/img.png) and [link](https://example.com)"
        self.assertListEqual(
            [
                TextNode("img", TextType.IMAGE, "https://example.com/img.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            text_to_textnodes(text)
        )

    def test_all_types_no_surrounding_text(self):
        text = "**bold**_italic_`code`![img](https://example.com/img.png)[link](https://example.com)"
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode("italic", TextType.ITALIC),
                TextNode("code", TextType.CODE),
                TextNode("img", TextType.IMAGE, "https://example.com/img.png"),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            text_to_textnodes(text)
        )
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

    def test_single_block(self):
        md = """Just one paragraph"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just one paragraph"])

    def test_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_extra_blank_lines(self):
        md = """First block


Second block"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First block", "Second block"])

    def test_heading_and_paragraph(self):
        md = """# Heading one

Some paragraph text"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["# Heading one", "Some paragraph text"])

    def test_multiple_headings(self):
        md = """# Heading one

## Heading two

### Heading three"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["# Heading one", "## Heading two", "### Heading three"])


    def test_ordered_list(self):
        md = """1. First item
2. Second item
3. Third item"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["1. First item\n2. Second item\n3. Third item"])

    def test_blockquote(self):
        md = """> This is a quote

Regular paragraph"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["> This is a quote", "Regular paragraph"])


    def test_leading_and_trailing_whitespace_stripped(self):
        md = """   First block   

Second block   """
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First block", "Second block"])

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    def test_heading_h1(self):
        md = "# Hello World"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>Hello World</h1></div>")

    def test_heading_h3(self):
        md = "### This is **bold** heading"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h3>This is <b>bold</b> heading</h3></div>")

    def test_blockquote(self):
        md = "> This is a quote with _italic_ text"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>This is a quote with <i>italic</i> text</blockquote></div>")

    def test_blockquote_multiline(self):
        md = """\
> First line
> Second line
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>First line\nSecond line</blockquote></div>")

    def test_unordered_list(self):
        md = """\
- Item one
- Item **two**
- Item three
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li>Item one</li><li>Item <b>two</b></li><li>Item three</li></ul></div>")

    def test_ordered_list(self):
        md = """\
1. First
2. Second
3. Third
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ol><li>First</li><li>Second</li><li>Third</li></ol></div>")

    def test_ordered_list_with_inline(self):
        md = """\
1. First with `code`
2. Second with _italic_
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ol><li>First with <code>code</code></li><li>Second with <i>italic</i></li></ol></div>")

    def test_multiple_headings(self):
        md = """\
# Heading One

## Heading Two
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>Heading One</h1><h2>Heading Two</h2></div>")

    def test_mixed_blocks(self):
        md = """\
# Title

This is a paragraph

- list item one
- list item two
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>Title</h1><p>This is a paragraph</p><ul><li>list item one</li><li>list item two</li></ul></div>")

    def test_paragraph_with_link(self):
        md = "Check out [this link](https://example.com) for more"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, '<div><p>Check out <a href="https://example.com">this link</a> for more</p></div>')


if __name__ == "__main__":
    unittest.main()