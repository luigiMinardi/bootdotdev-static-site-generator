import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("a", "This is a Link", None, {"href":"https://www.boot.dev","target":"_blank"})
        node2 = HTMLNode("div", children=[node])
        node3 = HTMLNode()

        node_repr = "HTMLNode(a, This is a Link, None, {'href': 'https://www.boot.dev', 'target': '_blank'})"

        self.assertEqual(node_repr, repr(node))
        self.assertEqual(f"HTMLNode(div, None, [{node_repr}], None)", repr(node2))
        self.assertEqual("HTMLNode(None, None, None, None)", repr(node3))

    def test_eq(self):
        node = HTMLNode("a", "This is a Link", None, {"href":"https://www.boot.dev","target":"_blank"})
        node2 = HTMLNode("a", "This is a Link", None, {"href":"https://www.boot.dev","target":"_blank"})
        self.assertEqual(node,node2)

    def test_prop_to_html(self):
        node = HTMLNode("a", "This is a Link", props={"href":"https://www.boot.dev","target":"_blank"})
        self.assertEqual(' href="https://www.boot.dev" target="_blank"', node.props_to_html())

    def test_prop_to_html_none(self):
        node = HTMLNode("a", "This is a Link")
        self.assertEqual('', node.props_to_html())
