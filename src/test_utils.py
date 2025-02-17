from enum import Enum
import unittest

from htmlnode import HTMLNode
from textnode import TextNode, TextType
from utils import text_node_to_html_node

class TextTypeToHTML(Enum):
    normal = None
    bold = "b"
    italic = "i"
    code = "code"
    link = "a"
    image = "img"

class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text_normal(self):
        text = "hello world"
        text_type = TextType.TEXT_NORMAL
        tag = TextTypeToHTML[text_type.value].value

        url = None
        props = None

        text_node = TextNode(text, text_type, url)
        html_node = text_node_to_html_node(text_node)

        self.assertIsInstance(html_node, HTMLNode)
        self.assertEqual(html_node, HTMLNode(tag, text, None, props))
        self.assertEqual(str(html_node), f'HTMLNode({tag}, {text}, None, {props})')


    def test_text_bold(self):
        text = "hello world"
        text_type = TextType.TEXT_BOLD
        tag = TextTypeToHTML[text_type.value].value

        url = None
        props = None

        text_node = TextNode(text, text_type, url)
        html_node = text_node_to_html_node(text_node)

        self.assertIsInstance(html_node, HTMLNode)
        self.assertEqual(html_node, HTMLNode(tag, text, None, props))
        self.assertEqual(str(html_node), f'HTMLNode({tag}, {text}, None, {props})')


    def test_text_italic(self):
        text = "hello world"
        text_type = TextType.TEXT_ITALIC
        tag = TextTypeToHTML[text_type.value].value

        url = None
        props = None

        text_node = TextNode(text, text_type, url)
        html_node = text_node_to_html_node(text_node)

        self.assertIsInstance(html_node, HTMLNode)
        self.assertEqual(html_node, HTMLNode(tag, text, None, props))
        self.assertEqual(str(html_node), f'HTMLNode({tag}, {text}, None, {props})')


    def test_text_code(self):
        text = "hello world"
        text_type = TextType.TEXT_CODE
        tag = TextTypeToHTML[text_type.value].value

        url = None
        props = None

        text_node = TextNode(text, text_type, url)
        html_node = text_node_to_html_node(text_node)

        self.assertIsInstance(html_node, HTMLNode)
        self.assertEqual(html_node, HTMLNode(tag, text, None, props))
        self.assertEqual(str(html_node), f'HTMLNode({tag}, {text}, None, {props})')


    def test_text_link(self):
        text = "hello world"
        text_type = TextType.LINK
        tag = TextTypeToHTML[text_type.value].value

        url = "https://www.boot.dev/img/bootdev-logo-full-small.webp"
        props = {'href': url}

        text_node = TextNode(text, text_type, url)
        html_node = text_node_to_html_node(text_node)

        self.assertIsInstance(html_node, HTMLNode)
        self.assertEqual(html_node, HTMLNode(tag, text, None, props))
        self.assertEqual(str(html_node), f'HTMLNode({tag}, {text}, None, {props})')


    def test_text_image(self):
        text = ""
        text_type = TextType.IMAGE
        tag = TextTypeToHTML[text_type.value].value

        url = "https://www.boot.dev/img/bootdev-logo-full-small.webp"
        alt = "hello world"
        props = {'src': url, 'alt': alt}

        text_node = TextNode(alt, text_type, url)
        html_node = text_node_to_html_node(text_node)

        self.assertIsInstance(html_node, HTMLNode)
        self.assertEqual(html_node, HTMLNode(tag, text, None, props))
        self.assertEqual(str(html_node), f'HTMLNode({tag}, {text}, None, {props})')


    def test_text_type_not_implemented(self):
        text_node = TextNode("hello world",TextType.TEXT_CODE)
        text_node.text_type = "not_implemented" #type: ignore

        with self.assertRaises(NotImplementedError) as cm:
            text_node_to_html_node(text_node)

        self.assertEqual(str(cm.exception), 'TextNode of TextType "not_implemented" has not been implemented yet.')

