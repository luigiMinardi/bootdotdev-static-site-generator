import unittest

from textnode import TextNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_url_eq(self):
        node = TextNode("This is a text node", "bold", "https://blank.page")
        node2 = TextNode("This is a text node", "bold", "https://blank.page")
        self.assertEqual(node, node2)

    def test_type_not_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "italic")
        self.assertNotEqual(node, node2)

    def test_text_not_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is also a text node", "bold")
        self.assertNotEqual(node,node2)

    def test_no_url(self):
        node = TextNode("This is a text node", "bold")
        self.assertEqual(node.url, None)

    def test_repr(self):
        node = TextNode("This is a text node", "bold", "https://blank.page")
        self.assertEqual("TextNode(This is a text node, bold, https://blank.page)",repr(node))

if __name__ == "__main__":
    unittest.main()
