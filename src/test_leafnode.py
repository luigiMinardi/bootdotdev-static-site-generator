import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode(tag="p", value="This is a paragraph of text.")
        node2 = LeafNode(tag="a", value="Click me!", props={"href": "https://www.google.com"})
        node3 = LeafNode(tag="p", value="This is a paragraph of text.")
        node4 = LeafNode(value="This is a paragraph of text.")

        self.assertEqual("<p>This is a paragraph of text.</p>",node.to_html())
        self.assertEqual('<a href="https://www.google.com">Click me!</a>', node2.to_html())
        with self.assertRaises(ValueError) as ctx:
            node3.value = None
            node3.to_html()
        self.assertEqual(repr(ctx.exception),"ValueError('All LeafNodes requires a value')")
        self.assertEqual("This is a paragraph of text.",node4.to_html())


