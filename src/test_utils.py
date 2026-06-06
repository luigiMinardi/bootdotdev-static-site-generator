from enum import Enum
import unittest

from htmlnode import HTMLNode
from textnode import TextNode, TextType
from utils import (
    text_node_to_html_node,
    split_nodes_delimiter,
    Delimiters,
    find_all,
    extract_markdown_images,
    extract_markdown_links
)


class TextTypeToHTML(Enum):
    normal = None
    bold = "b"
    italic = "i"
    code = "code"
    link = "a"
    image = "img"


class TestTextNodeToHtmlNode(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.example_text = "hello world"
        cls.example_url = \
            "https://www.boot.dev/img/bootdev-logo-full-small.webp"

    def _test_text_node_to_html_helper(
        self,
        text: str,
        text_type: TextType,
        url: str | None = None,
        props: dict | None = None,
        expected_text: str | None = None,
    ) -> None:
        """
        Helper function to test the text_node_to_html_node() function since
        most tests are the same.

        text (str): The text of the HTML element (or alt text for images).
            [Used on Input]
        text_type (TextType): The text type of the TextNode that you want to
            test. [Used on Input]
        url (str | None): The URL value if needed. Used on TextType IMAGE or
            LINK for example. [Used on Input]
        props (dict | None): A dict representing all props the HTML element
            will have after the function have ran. [Used on Assertion]
        expected_text (str | None): The text expected on assertion, DEFAULTS TO
            the "text" argument if None. [Used on Assertion]

        How the "expected_text" works:
            self._test_text_node_to_html_helper("foo", TextType.TEXT_NORMAL)
                -> expected_text is "foo"

            self._test_text_node_to_html_helper(self.example_text,
                TextType.TEXT_NORMAL, expected_text="bar")
                    -> expected_text is "bar"

            On the first example the assertion will try to see if the HTML
                element innerHTML text is "foo"
            On the second example it will try to see if it's "bar"
        """
        tag = TextTypeToHTML[text_type.value].value
        expected_text = text if expected_text is None else expected_text

        text_node = TextNode(text, text_type, url)
        html_node = text_node_to_html_node(text_node)

        self.assertIsInstance(html_node, HTMLNode)
        self.assertEqual(html_node, HTMLNode(tag, expected_text, None, props))
        self.assertEqual(
            str(html_node), f"HTMLNode({tag}, {expected_text}, None, {props})"
        )

    def test_text_normal(self):
        self._test_text_node_to_html_helper(
            self.example_text, TextType.TEXT_NORMAL)

    def test_text_bold(self):
        self._test_text_node_to_html_helper(
            self.example_text, TextType.TEXT_BOLD)

    def test_text_italic(self):
        self._test_text_node_to_html_helper(
            self.example_text, TextType.TEXT_ITALIC)

    def test_text_code(self):
        self._test_text_node_to_html_helper(
            self.example_text, TextType.TEXT_CODE)

    def test_text_link(self):
        self._test_text_node_to_html_helper(
            self.example_text,
            TextType.LINK,
            self.example_url,
            {"href": self.example_url},
        )

    def test_text_image(self):
        self._test_text_node_to_html_helper(
            self.example_text,
            TextType.IMAGE,
            self.example_url,
            {"src": self.example_url, "alt": self.example_text},
            "",  # images shoudn't have inner text
        )

    def test_text_type_not_implemented(self):
        text_node = TextNode("hello world", TextType.TEXT_CODE)
        text_node.text_type = "not_implemented"  # type: ignore

        with self.assertRaises(NotImplementedError) as cm:
            text_node_to_html_node(text_node)

        self.assertEqual(
            str(cm.exception),
            'TextNode of TextType "not_implemented" has not been implemented yet.',
        )


class TestSplitNodes(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.example_url = \
            "https://www.boot.dev/img/bootdev-logo-full-small.webp"

    def test_split_nodes(self):
        """
        # old node list test from when I was trying to implement real
        # CommonMark
        nodes_list = [
            TextNode(
                f"***Lorem* ipsum** `dolor` sit* *amet, **consectetur adipiscing* elit**. **[Nunc ultrices aliquet nunc.]({
                    self.example_url
                })** *`Pellentesque `*`sodales quam` ![odio]({
                    self.example_url
                }), **quis**** *porta `**massa* condimentum`** ****ut.*",
                TextType.TEXT_NORMAL,
            )
        ]
        """
        nodes_list = [
            TextNode(
                f"***Lorem* ipsum** `dolor` sit* *amet, **consectetur adipiscing* elit**. **[Nunc ultrices aliquet nunc.]({
                    self.example_url
                })** *`Pellentesque `*`sodales quam` ![odio]({
                    self.example_url
                }), **quis**** *porta `**massa* condimentum`** ***ut.*",
                TextType.TEXT_NORMAL,
            )
        ]

        new_list = split_nodes_delimiter(
            nodes_list, Delimiters.BOLD.value, TextType.TEXT_BOLD)
        for node in new_list:
            recheck = list(find_all(node.text, Delimiters.BOLD.value))
            self.assertTrue(len(recheck) == 0 or len(recheck) % 2 != 0)

    def test_split_nodes_raises(self):
        nodes_list2 = [TextNode("*foo**bar*", TextType.TEXT_NORMAL)]

        with self.assertRaises(Exception) as cm:
            split_nodes_delimiter(
                nodes_list2, Delimiters.BOLD.value, TextType.TEXT_BOLD)

        self.assertEqual(
            str(cm.exception),
            'Invalid markdown syntax, delimiter found at 4 did not found a closing pair',
        )


class TestExtractMarkdownImagesAndLinks(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.example_url = \
            "https://www.boot.dev/img/bootdev-logo-full-small.webp"

        cls.example_text = f"""
            **[[[[[[[[[[Nunc ultrices aliquet nunc.](](](](](](]({
            cls.example_url
        }))** *`Pellentesque `*`sodales quam` ![![![![![(odio](](](](](]({
            cls.example_url
        }))
        )** *`Pellentesque `*`sodales quam` ![bar ]({
            cls.example_url
        })
        !)](** *`Pellentesque `*`sodales quam` [ foo]({
            cls.example_url
        })
        ![[])!()
        """

    def test_extract_markdown_images(self):
        res = extract_markdown_images(self.example_text)
        self.assertTrue(len(res) == 2)
        self.assertEqual(-1, res[0][1].find("]("))
        self.assertEqual(-1, res[1][1].find("]("))

    def test_extract_markdown_links(self):
        res = extract_markdown_links(self.example_text)
        self.assertTrue(len(res) == 2)
        self.assertEqual(-1, res[0][1].find("]("))
        self.assertEqual(-1, res[1][1].find("]("))
