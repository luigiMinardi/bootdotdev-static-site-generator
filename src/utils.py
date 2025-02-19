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

    for node in old_nodes:
        for i in range(len(node.text)):
            if node.text[i] == Delimiters.CODE.value:
                delimiters_debug[Delimiters.CODE.value].append(i)

            if i + 1 < len(node.text):
                if (
                    node.text[i] == Delimiters.ITALIC.value
                    and node.text[i + 1] == Delimiters.ITALIC.value
                    and i-1 not in delimiters_debug[Delimiters.BOLD.value]
                ):
                    delimiters_debug[Delimiters.BOLD.value].append(i)
                elif (
                    node.text[i] == Delimiters.ITALIC.value
                    and i-1 not in delimiters_debug[Delimiters.BOLD.value]
                ):
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

    delimiters_left: dict[str, list[int]] = {
        Delimiters.CODE.value: [],
        Delimiters.ITALIC.value: [],
        Delimiters.BOLD.value: [],
        Delimiters.LINK.value: [],
        Delimiters.IMAGE.value: [],
    }

    delimiters_right: dict[str, list[int]] = {
        Delimiters.CODE.value: [],
        Delimiters.ITALIC.value: [],
        Delimiters.BOLD.value: [],
        Delimiters.LINK_MID.value: [],
        Delimiters.LINK_CLOSE.value: []
    }


    for node in old_nodes:
        #i = 0
        #while i < len(node.text):
        for i in range(len(node.text)):

            if (
                node.text[i] == Delimiters.CODE.value
                and (
                    len(delimiters_left[Delimiters.CODE.value]) < len(delimiters_right[Delimiters.CODE.value])
                    or len(delimiters_left[Delimiters.CODE.value]) == len(delimiters_right[Delimiters.CODE.value])
                )
                and i not in delimiters_right[Delimiters.CODE.value]
            ):
                delimiters_left[Delimiters.CODE.value].append(i)

            if (
                node.text[i] == Delimiters.CODE.value
                and len(delimiters_left[Delimiters.CODE.value]) > len(delimiters_right[Delimiters.CODE.value])
                and i not in delimiters_left[Delimiters.CODE.value]
            ):
                delimiters_right[Delimiters.CODE.value].append(i)

            if i + 1 < len(node.text):
                if i + 2 < len(node.text):
                    if (
                        node.text[i] == Delimiters.ITALIC.value
                        and node.text[i + 1] == Delimiters.ITALIC.value
                        and node.text[i + 2] != " "
                        and i not in delimiters_right[Delimiters.BOLD.value]
                        and i - 1 not in delimiters_left[Delimiters.BOLD.value]
                        and i - 1 not in delimiters_right[Delimiters.BOLD.value]
                        and (
                            len(delimiters_left[Delimiters.BOLD.value]) < len(delimiters_right[Delimiters.BOLD.value])
                            or len(delimiters_left[Delimiters.BOLD.value]) == len(delimiters_right[Delimiters.BOLD.value])
                        )
                    ):
                        delimiters_left[Delimiters.BOLD.value].append(i)

                    if (
                        node.text[i] == Delimiters.ITALIC.value
                        and node.text[i + 1] == Delimiters.ITALIC.value
                        and node.text[i - 1] != " "
                        and i not in delimiters_left[Delimiters.BOLD.value]
                        and i - 1 not in delimiters_right[Delimiters.BOLD.value]
                        and i - 1 not in delimiters_left[Delimiters.BOLD.value]
                        and len(delimiters_left[Delimiters.BOLD.value]) > len(delimiters_right[Delimiters.BOLD.value])
                    ):
                        if delimiters_left[Delimiters.BOLD.value][-1] == i-2:
                            delimiters_left[Delimiters.BOLD.value].pop()
                        else:
                            delimiters_right[Delimiters.BOLD.value].append(i)

                if (
                    node.text[i] == Delimiters.ITALIC.value
                    and node.text[i + 1] != " "
                    and i not in delimiters_right[Delimiters.ITALIC.value]
                    and i not in delimiters_right[Delimiters.BOLD.value]
                    and i not in delimiters_left[Delimiters.BOLD.value]
                    and i - 1 not in delimiters_left[Delimiters.BOLD.value]
                    and i - 1 not in delimiters_right[Delimiters.BOLD.value]
                    and (
                        len(delimiters_left[Delimiters.ITALIC.value]) < len(delimiters_right[Delimiters.ITALIC.value])
                        or len(delimiters_left[Delimiters.ITALIC.value]) == len(delimiters_right[Delimiters.ITALIC.value])
                    )
                ):
                    delimiters_left[Delimiters.ITALIC.value].append(i)

            if (
                node.text[i] == Delimiters.ITALIC.value
                and node.text[i - 1] != " "
                and i not in delimiters_left[Delimiters.ITALIC.value]
                and i not in delimiters_right[Delimiters.BOLD.value]
                and i not in delimiters_left[Delimiters.BOLD.value]
                and i - 1 not in delimiters_right[Delimiters.BOLD.value]
                and i - 1 not in delimiters_left[Delimiters.BOLD.value]
                and len(delimiters_left[Delimiters.ITALIC.value]) > len(delimiters_right[Delimiters.ITALIC.value])
            ):
                if delimiters_left[Delimiters.ITALIC.value][-1] == i-1:
                    delimiters_left[Delimiters.ITALIC.value].pop()
                    if i + 1 < len(node.text):
                        if node.text[i + 1] != " ":
                            delimiters_left[Delimiters.ITALIC.value].append(i)
                else:
                    delimiters_right[Delimiters.ITALIC.value].append(i)

            '''
                if node.text[i] == "!" and node.text[i + 1] == Delimiters.LINK.value:
                    delimiters[Delimiters.IMAGE.value].append(i)

                if node.text[i] == Delimiters.LINK.value and node.text[i - 1] != "!":
                    delimiters[Delimiters.LINK.value].append(i)

                if node.text[i] == "]" and node.text[i + 1] == "(":
                    delimiters[Delimiters.LINK_MID.value].append(i)

            if node.text[i] == Delimiters.LINK_CLOSE.value:
                delimiters[Delimiters.LINK_CLOSE.value].append(i)

            if i == len(node.text) -1:
                if node.text[i] == Delimiters.ITALIC.value and node.text[i-1] != Delimiters.ITALIC.value:
                    delimiters[Delimiters.ITALIC.value].append(i)
            if i - 1 >= 0:
            '''

            #i += 1
    print("left:", delimiters_left,"\nright:", delimiters_right)
