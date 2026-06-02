from collections.abc import Generator
from enum import Enum
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
            raise NotImplementedError(
                f'TextNode of TextType "{
                    text_node.text_type}" has not been implemented yet.'
            )


class Delimiters(Enum):
    CODE = "`"
    ITALIC = "*"
    BOLD = "**"
    LINK = "["
    IMAGE = "!["
    LINK_MID = "]("
    LINK_CLOSE = ")"


def find_all(string: str, value: str) -> Generator[int]:
    """
    Generator that find the index of "value" inside a given "string" and yields
    it.

    Examples:

    - Finding all values:
    all_values: list[int] = list(find_all("foo bar bazz bar", bar))
    print(all_values) # [7, 18, 34, 40]

    - Getting first value:
     generator: Generator[int] = find_all("foo bar bazz bar", bar)
     first: int = next(generator).
     print(first) # 7

    - Calling in a loop:
    generator: Generator[int] = find_all("foo bar bazz bar", bar)
    for i in generator:
        if i > 20:
            break;
        print(i) # 7, then 18, breaks before 34, consuming it.
    next(generator) # 40, the 34 was consumed inside the loop.

    - Avoiding consuming in a loop
    The way to avoid the loop to call next is by breaking after you did your
    logic making sure the loop will not continue to another iteration

    generator: Generator[int] = find_all("foo bar bazz bar", bar)
    result_list: list[int] = []
    results.append(i)
    for i in generator:
        result_list.append(i) # [7, 18]
        if len(i) >= 2:
            break;
    next(generator) # 34

    Arguments:
        string (str): string to search
        value (str): value to be searched
    Return (Yield):
        Generator[int]: the index representing the beginning of the value in
        the "string"
    """
    start = 0
    while True:
        start = string.find(value, start)
        if start == -1:
            return
        yield start
        start += len(value)


def split_nodes_delimiter(
    old_nodes: list[TextNode],
    delimiter: str,
    text_type: TextType
) -> list[TextNode]:
    raise NotImplementedError("WIP")

    return_list: list[TextNode] = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT_NORMAL:
            return_list.append(node)

        delimiter_range: list[int] = list(find_all(node.text, delimiter))

        if len(delimiter_range) % 2 != 0:
            raise Exception(f"Invalid markdown syntax, delimiter found at {
                            delimiter_range[-1]} did not found a closing pair")
        for i in range(1, len(delimiter_range), 2):
            start = delimiter_range[i - 1]
            end = delimiter_range[i + 1]
