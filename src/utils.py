from ast import Del
from collections.abc import Sequence
from enum import Enum
from typing import Any, TypedDict
from htmlnode import HTMLNode
from leafnode import LeafNode
from textnode import TextNode, TextType


def text_node_to_html_node(text_node: TextNode) -> HTMLNode:

    match text_node.text_type:
        case TextType.TEXT_NORMAL:
            return LeafNode(text_node.text)
        case TextType.TEXT_BOLD:
            return LeafNode(text_node.text, "b")
        case TextType.TEXT_ITALIC:
            return LeafNode(text_node.text, "i")
        case TextType.TEXT_CODE:
            return LeafNode(text_node.text, "code")
        case TextType.LINK:
            return LeafNode(text_node.text, "a", {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("", "img", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise NotImplementedError(f'TextNode of TextType "{text_node.text_type}" has not been implemented yet.')


class Delimiters(Enum):
    CODE = "`"
    ITALIC = "*"
    BOLD = "**"
    LINK = "["
    IMAGE = "!["
    LINK_MID = "]("
    LINK_CLOSE = ")"


def split_nodes_delimiter(old_nodes: Sequence[TextNode], delimiter: str, text_type: TextType) -> Sequence[TextNode]:
    delimiters_debug: dict[str, list[int]] = {
        Delimiters.CODE.value: [],
        Delimiters.ITALIC.value: [],
        Delimiters.BOLD.value: [],
        Delimiters.LINK.value: [],
        Delimiters.IMAGE.value: [],
        Delimiters.LINK_MID.value: [],
        Delimiters.LINK_CLOSE.value: []
    }
    print(delimiters_debug)
    for node in old_nodes:
        for i in range(len(node.text)):
            if node.text[i] == Delimiters.CODE.value:
                delimiters_debug[Delimiters.CODE.value].append(i)

            if i + 1 < len(node.text):
                if node.text[i] == Delimiters.ITALIC.value and node.text[i + 1] == Delimiters.ITALIC.value and i-1 not in delimiters_debug[Delimiters.BOLD.value]:
                    delimiters_debug[Delimiters.BOLD.value].append(i)
                elif node.text[i] == Delimiters.ITALIC.value and i not in delimiters_debug[Delimiters.ITALIC.value] and i-1 not in delimiters_debug[Delimiters.BOLD.value]:
                    delimiters_debug[Delimiters.ITALIC.value].append(i)

                if node.text[i] == "!" and node.text[i + 1] == Delimiters.LINK.value:
                    delimiters_debug[Delimiters.IMAGE.value].append(i)
                
                if node.text[i] == Delimiters.LINK.value and node.text[i - 1] != "!":
                    delimiters_debug[Delimiters.LINK.value].append(i)

                if node.text[i] == "]" and node.text[i + 1] == "(":
                    delimiters_debug[Delimiters.LINK_MID.value].append(i)

            if node.text[i] == Delimiters.LINK_CLOSE.value:
                delimiters_debug[Delimiters.LINK_CLOSE.value].append(i)


            if i == len(node.text) -1:
                if node.text[i] == Delimiters.ITALIC.value and node.text[i-1] != Delimiters.ITALIC.value:
                    delimiters_debug[Delimiters.ITALIC.value].append(i)

    print(delimiters_debug)
