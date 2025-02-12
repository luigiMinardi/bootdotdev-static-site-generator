import unittest

from leafnode import LeafNode
from parentnode import ParentNode

class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("Bold text","b"),
                LeafNode("Normal text"),
                LeafNode("italic text","i"),
                LeafNode("Normal text"),
            ],
        )


        node_test = node.to_html()
        node_expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"

        node2 = ParentNode("p", [])
        with self.assertRaises(ValueError) as node2_test:
            node2.to_html()

        node3 = ParentNode('',children=[LeafNode("Bold", "b")])
        with self.assertRaises(ValueError) as node3_test:
            node3.to_html()

        node4 = ParentNode("div", [
            node,
            node,
            node,
            LeafNode("normal text"),
            LeafNode("italic text", "i")
            ])

        node4_test = node4.to_html()
        node4_expected = f"<div>{node_expected}{node_expected}{node_test}normal text<i>italic text</i></div>"

        self.assertEqual(node_test, node_expected)
        self.assertEqual(str(node2_test.exception), 'All ParentNodes requires a children object')
        self.assertEqual(str(node3_test.exception), 'All ParentNodes requires a tag')
        self.assertEqual(node4_test, node4_expected)

