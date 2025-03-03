import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.TEXT_BOLD)
        node2 = TextNode("This is a text node", TextType.TEXT_BOLD)
        self.assertEqual(node, node2)

    def test_url_eq(self):
        node = TextNode("This is a text node", TextType.LINK, "https://blank.page")
        node2 = TextNode("This is a text node", TextType.LINK, "https://blank.page")
        self.assertEqual(node, node2)

    def test_type_not_eq(self):
        node = TextNode("This is a text node", TextType.TEXT_BOLD)
        node2 = TextNode("This is a text node", TextType.TEXT_ITALIC)
        self.assertNotEqual(node, node2)

    def test_text_not_eq(self):
        node = TextNode("This is a text node", TextType.TEXT_BOLD)
        node2 = TextNode("This is also a text node", TextType.TEXT_BOLD)
        self.assertNotEqual(node, node2)

    def test_no_url(self):
        node = TextNode("This is a text node", TextType.TEXT_BOLD)
        self.assertEqual(node.url, None)

    def test_wrong_text_type(self):
        with self.assertRaises(TypeError) as cm:
            TextNode("This is a text node", "bold")  # type: ignore
        self.assertEqual(str(cm.exception), "bold is not of type <enum 'TextType'>")

    def test_no_url_in_link_or_image(self):
        with self.assertRaises(ValueError) as cm:
            TextNode("This is a text node", TextType.LINK)
        self.assertEqual(
            str(cm.exception),
            f"url is needed in the text type {TextType.LINK}, add an url please.",
        )

        with self.assertRaises(ValueError) as cm:
            TextNode("This is a text node", TextType.IMAGE)
        self.assertEqual(
            str(cm.exception),
            f"url is needed in the text type {TextType.IMAGE}, add an url please.",
        )

    def test_url_shouldnt_be_in_text_types_that_dont_need_it(self):
        with self.assertRaises(ValueError) as cm:
            TextNode("This is a text node", TextType.TEXT_BOLD, "https://blank.page")

        self.assertEqual(
            str(cm.exception),
            f"url doesn't work with the text type {TextType.TEXT_BOLD}, use {TextType.IMAGE} or {TextType.LINK}",
        )

        with self.assertRaises(ValueError) as cm:
            TextNode("This is a text node", TextType.TEXT_NORMAL, "https://blank.page")

        self.assertEqual(
            str(cm.exception),
            f"url doesn't work with the text type {TextType.TEXT_NORMAL}, use {TextType.IMAGE} or {TextType.LINK}",
        )

        with self.assertRaises(ValueError) as cm:
            TextNode("This is a text node", TextType.TEXT_ITALIC, "https://blank.page")

        self.assertEqual(
            str(cm.exception),
            f"url doesn't work with the text type {TextType.TEXT_ITALIC}, use {TextType.IMAGE} or {TextType.LINK}",
        )

    def test_repr(self):
        node = TextNode("This is a text node", TextType.LINK, "https://blank.page")
        self.assertEqual(
            "TextNode('This is a text node', TextType.LINK, 'https://blank.page')",
            repr(node),
        )

        node2 = TextNode("This is a text node", TextType.TEXT_NORMAL)
        self.assertEqual(
            "TextNode('This is a text node', TextType.TEXT_NORMAL, None)",
            repr(node2),
        )


if __name__ == "__main__":
    unittest.main()
