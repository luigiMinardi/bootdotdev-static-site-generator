from collections.abc import Sequence
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
                f'TextNode of TextType "{text_node.text_type}" has not been implemented yet.'
            )


class Delimiters(Enum):
    CODE = "`"
    ITALIC = "*"
    BOLD = "**"
    LINK = "["
    IMAGE = "!["
    LINK_MID = "]("
    LINK_CLOSE = ")"


def _split_nodes_debug(old_nodes: Sequence[TextNode]) -> None:
    delimiters_debug: dict[str, list[int]] = {
        Delimiters.CODE.value: [],
        Delimiters.ITALIC.value: [],
        Delimiters.BOLD.value: [],
        Delimiters.LINK.value: [],
        Delimiters.IMAGE.value: [],
        Delimiters.LINK_MID.value: [],
        Delimiters.LINK_CLOSE.value: [],
    }

    for node in old_nodes:
        for i in range(len(node.text)):
            if node.text[i] == Delimiters.CODE.value:
                delimiters_debug[Delimiters.CODE.value].append(i)

            if i + 1 < len(node.text):
                if (
                    node.text[i] == Delimiters.ITALIC.value
                    and node.text[i + 1] == Delimiters.ITALIC.value
                    and i - 1 not in delimiters_debug[Delimiters.BOLD.value]
                ):
                    delimiters_debug[Delimiters.BOLD.value].append(i)
                elif (
                    node.text[i] == Delimiters.ITALIC.value
                    and i - 1 not in delimiters_debug[Delimiters.BOLD.value]
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

            if i == len(node.text) - 1:
                if (
                    node.text[i] == Delimiters.ITALIC.value
                    and node.text[i - 1] != Delimiters.ITALIC.value
                ):
                    delimiters_debug[Delimiters.ITALIC.value].append(i)

    print("\nAll delimiters:", delimiters_debug)

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
        Delimiters.LINK_CLOSE.value: [],
    }

    for node in old_nodes:
        print("parsing node", node, delimiters_left, delimiters_right)
        for i in range(len(node.text)):

            if (
                node.text[i] == Delimiters.CODE.value
                and (
                    len(delimiters_left[Delimiters.CODE.value])
                    < len(delimiters_right[Delimiters.CODE.value])
                    or len(delimiters_left[Delimiters.CODE.value])
                    == len(delimiters_right[Delimiters.CODE.value])
                )
                and i not in delimiters_right[Delimiters.CODE.value]
            ):
                delimiters_left[Delimiters.CODE.value].append(i)

            if (
                node.text[i] == Delimiters.CODE.value
                and len(delimiters_left[Delimiters.CODE.value])
                > len(delimiters_right[Delimiters.CODE.value])
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
                            len(delimiters_left[Delimiters.BOLD.value])
                            < len(delimiters_right[Delimiters.BOLD.value])
                            or len(delimiters_left[Delimiters.BOLD.value])
                            == len(delimiters_right[Delimiters.BOLD.value])
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
                        and len(delimiters_left[Delimiters.BOLD.value])
                        > len(delimiters_right[Delimiters.BOLD.value])
                    ):
                        if delimiters_left[Delimiters.BOLD.value][-1] == i - 2:
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
                        len(delimiters_left[Delimiters.ITALIC.value])
                        < len(delimiters_right[Delimiters.ITALIC.value])
                        or len(delimiters_left[Delimiters.ITALIC.value])
                        == len(delimiters_right[Delimiters.ITALIC.value])
                    )
                ):
                    delimiters_left[Delimiters.ITALIC.value].append(i)

                if node.text[i] == "!" and node.text[i + 1] == Delimiters.LINK.value:
                    delimiters_left[Delimiters.IMAGE.value].append(i)

                if node.text[i] == "]" and node.text[i + 1] == "(":
                    delimiters_right[Delimiters.LINK_MID.value].append(i)

            if node.text[i] == Delimiters.LINK.value and node.text[i - 1] != "!":
                delimiters_left[Delimiters.LINK.value].append(i)

            if node.text[i] == Delimiters.LINK_CLOSE.value:
                delimiters_right[Delimiters.LINK_CLOSE.value].append(i)

            if (
                node.text[i] == Delimiters.ITALIC.value
                and node.text[i - 1] != " "
                and i not in delimiters_left[Delimiters.ITALIC.value]
                and i not in delimiters_right[Delimiters.BOLD.value]
                and i not in delimiters_left[Delimiters.BOLD.value]
                and i - 1 not in delimiters_right[Delimiters.BOLD.value]
                and i - 1 not in delimiters_left[Delimiters.BOLD.value]
                and len(delimiters_left[Delimiters.ITALIC.value])
                > len(delimiters_right[Delimiters.ITALIC.value])
            ):
                if delimiters_left[Delimiters.ITALIC.value][-1] == i - 1:
                    delimiters_left[Delimiters.ITALIC.value].pop()
                    if i + 1 < len(node.text):
                        if node.text[i + 1] != " ":
                            delimiters_left[Delimiters.ITALIC.value].append(i)
                else:
                    delimiters_right[Delimiters.ITALIC.value].append(i)

    print("left:", delimiters_left, "\nright:", delimiters_right)


def split_all_nodes(nodes: Sequence[TextNode]) -> Sequence[TextNode]:
    pass


def check_need_to_split_node(node: TextNode) -> bool:
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
        Delimiters.LINK_CLOSE.value: [],
    }
    print("parsing node", node, delimiters_left, delimiters_right)
    for i in range(len(node.text)):

        if (
            node.text[i] == Delimiters.CODE.value
            and (
                len(delimiters_left[Delimiters.CODE.value])
                < len(delimiters_right[Delimiters.CODE.value])
                or len(delimiters_left[Delimiters.CODE.value])
                == len(delimiters_right[Delimiters.CODE.value])
            )
            and i not in delimiters_right[Delimiters.CODE.value]
        ):
            delimiters_left[Delimiters.CODE.value].append(i)

        if (
            node.text[i] == Delimiters.CODE.value
            and len(delimiters_left[Delimiters.CODE.value])
            > len(delimiters_right[Delimiters.CODE.value])
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
                        len(delimiters_left[Delimiters.BOLD.value])
                        < len(delimiters_right[Delimiters.BOLD.value])
                        or len(delimiters_left[Delimiters.BOLD.value])
                        == len(delimiters_right[Delimiters.BOLD.value])
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
                    and len(delimiters_left[Delimiters.BOLD.value])
                    > len(delimiters_right[Delimiters.BOLD.value])
                ):
                    if delimiters_left[Delimiters.BOLD.value][-1] == i - 2:
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
                    len(delimiters_left[Delimiters.ITALIC.value])
                    < len(delimiters_right[Delimiters.ITALIC.value])
                    or len(delimiters_left[Delimiters.ITALIC.value])
                    == len(delimiters_right[Delimiters.ITALIC.value])
                )
            ):
                delimiters_left[Delimiters.ITALIC.value].append(i)

            if node.text[i] == "!" and node.text[i + 1] == Delimiters.LINK.value:
                delimiters_left[Delimiters.IMAGE.value].append(i)

            if node.text[i] == "]" and node.text[i + 1] == "(":
                delimiters_right[Delimiters.LINK_MID.value].append(i)

        if node.text[i] == Delimiters.LINK.value and node.text[i - 1] != "!":
            delimiters_left[Delimiters.LINK.value].append(i)

        if node.text[i] == Delimiters.LINK_CLOSE.value:
            delimiters_right[Delimiters.LINK_CLOSE.value].append(i)

        if (
            node.text[i] == Delimiters.ITALIC.value
            and node.text[i - 1] != " "
            and i not in delimiters_left[Delimiters.ITALIC.value]
            and i not in delimiters_right[Delimiters.BOLD.value]
            and i not in delimiters_left[Delimiters.BOLD.value]
            and i - 1 not in delimiters_right[Delimiters.BOLD.value]
            and i - 1 not in delimiters_left[Delimiters.BOLD.value]
            and len(delimiters_left[Delimiters.ITALIC.value])
            > len(delimiters_right[Delimiters.ITALIC.value])
        ):
            if delimiters_left[Delimiters.ITALIC.value][-1] == i - 1:
                delimiters_left[Delimiters.ITALIC.value].pop()
                if i + 1 < len(node.text):
                    if node.text[i + 1] != " ":
                        delimiters_left[Delimiters.ITALIC.value].append(i)
            else:
                delimiters_right[Delimiters.ITALIC.value].append(i)

    print("left:", delimiters_left, "\nright:", delimiters_right)
    if (
        (
            len(delimiters_left[Delimiters.CODE.value])
            and len(delimiters_right[Delimiters.CODE.value])
        )
        or (
            len(delimiters_left[Delimiters.ITALIC.value])
            and len(delimiters_right[Delimiters.ITALIC.value])
        )
        or (
            len(delimiters_left[Delimiters.BOLD.value])
            and len(delimiters_right[Delimiters.BOLD.value])
        )
        or (
            len(delimiters_left[Delimiters.IMAGE.value])
            and len(delimiters_right[Delimiters.LINK_MID.value])
            and len(delimiters_right[Delimiters.LINK_CLOSE.value])
        )
        or (
            len(delimiters_left[Delimiters.LINK.value])
            and len(delimiters_right[Delimiters.LINK_MID.value])
            and len(delimiters_right[Delimiters.LINK_CLOSE.value])
        )
    ):
        return True
    return False


def split_node(node: TextNode) -> Sequence[TextNode]:
    """
    THIS FUNCTION MUTATES "node" making it's "node.text" empty after finishing.
    """

    res: Sequence[TextNode] = []

    code_pair: int | None = None
    last_code_symbol: int | None = None

    image_start: int | None = None
    image_middle: int | None = None

    link_start: int | None = None
    link_middle: int | None = None

    bold_pair: int | None = None

    italic_pair: int | None = None

    transformation_pair: int | None = None
    looking_for_pair: tuple[int, Delimiters] | None = None

    i = 0
    while i < len(node.text):
        if (
            i != 0
            and looking_for_pair != None
            and looking_for_pair[0] > 0
            and len(node.text[0 : looking_for_pair[0]]) > 0
        ):
            res.append(
                TextNode(
                    node.text[0 : looking_for_pair[0]],
                    TextType.TEXT_NORMAL,
                )
            )
            node.text = node.text[looking_for_pair[0] :]
            match looking_for_pair[1]:
                case Delimiters.CODE:
                    code_pair = 0
                case Delimiters.BOLD:
                    bold_pair = 0
                case Delimiters.ITALIC:
                    italic_pair = 0
                case Delimiters.IMAGE:
                    image_start = 0
                case Delimiters.LINK:
                    link_start = 0
            i = 0
            looking_for_pair = None
            continue

        if node.text[i] == Delimiters.CODE.value:
            last_code_symbol = i

        if node.text[i] == Delimiters.CODE.value and code_pair == None:
            code_pair = i

            if italic_pair == None and bold_pair == None:
                looking_for_pair = (i, Delimiters.CODE)

        if bold_pair == None and italic_pair == None:
            if (
                i > 0
                and node.text[i] == Delimiters.CODE.value
                and code_pair != None
                and i != code_pair
            ):
                res.append(
                    TextNode(
                        node.text[code_pair + 1 : i],
                        TextType.TEXT_CODE,
                    )
                )
                node.text = node.text[:code_pair] + node.text[i + 1 :]
                i = 0
                code_pair = None
                continue

            if code_pair != None:
                if i + 1 >= len(node.text):
                    i = code_pair
                    code_pair = None
                i += 1
                continue

            if i + 1 < len(node.text):
                if (
                    node.text[i] == "!"
                    and node.text[i + 1] == Delimiters.LINK.value
                    and image_start == None
                ):
                    image_start = i
                    looking_for_pair = (i, Delimiters.IMAGE)
                elif (
                    node.text[i] == "]"
                    and node.text[i + 1] == "("
                    and image_start != None
                ):
                    image_middle = i

                if (
                    node.text[i - 1] != "!"
                    and node.text[i] == Delimiters.LINK.value
                    and link_start == None
                ):
                    link_start = i
                    looking_for_pair = (i, Delimiters.LINK)
                elif (
                    node.text[i] == "]"
                    and node.text[i + 1] == "("
                    and link_start != None
                ):
                    link_middle = i

                if (
                    node.text[i] == Delimiters.LINK_CLOSE.value
                    and image_start != None
                    and image_middle != None
                ):
                    res.append(
                        TextNode(
                            node.text[image_start + 2 : image_middle],
                            TextType.IMAGE,
                            node.text[image_middle + 2 : i],
                        )
                    )
                    node.text = node.text[:image_start] + node.text[i + 1 :]
                    i = 0
                    image_start = None
                    image_middle = None
                    continue

                if (
                    node.text[i] == Delimiters.LINK_CLOSE.value
                    and link_start != None
                    and link_middle != None
                ):
                    res.append(
                        TextNode(
                            node.text[link_start + 1 : link_middle],
                            TextType.LINK,
                            node.text[link_middle + 2 : i],
                        )
                    )
                    node.text = node.text[:link_start] + node.text[i + 1 :]

                    i = 0
                    link_start = None
                    link_middle = None
                    continue

        if i + 2 < len(node.text):
            if (
                node.text[i] == Delimiters.ITALIC.value
                and node.text[i + 1] == Delimiters.ITALIC.value  # BOLD
                and node.text[i + 2] != " "  # left delimiter (start)
                and bold_pair == None
                and code_pair == None
            ):
                bold_pair = i
                if italic_pair == None:
                    looking_for_pair = (i, Delimiters.BOLD)

            if (
                i > 0
                and node.text[i] == Delimiters.ITALIC.value
                and node.text[i + 1] == Delimiters.ITALIC.value  # BOLD
                and node.text[i - 1] != Delimiters.ITALIC.value
                and node.text[i - 1] != " "  # right delimiter (end)
                and bold_pair != None
                and i != bold_pair
            ):
                if transformation_pair != None and italic_pair != None:
                    res.append(
                        TextNode(
                            node.text[italic_pair + 1 : i + 1],
                            TextType.TEXT_ITALIC,
                        )
                    )
                    node.text = node.text[:italic_pair] + node.text[i + 2 :]
                    i = 0

                    italic_pair = None
                    bold_pair = None
                    transformation_pair = None
                    continue
                else:
                    if code_pair == None or code_pair != last_code_symbol:
                        res.append(
                            TextNode(
                                node.text[bold_pair + 2 : i],
                                TextType.TEXT_BOLD,
                            )
                        )
                        node.text = node.text[:bold_pair] + node.text[i + 2 :]
                        i = 0
                        italic_pair = None
                        code_pair = None
                        bold_pair = None
                        continue

            if (
                node.text[i] == Delimiters.ITALIC.value
                and node.text[i + 1] != Delimiters.ITALIC.value  # ITALIC
                and node.text[i + 1] != " "  # left delimiter (start)
                and italic_pair == None
                and bold_pair == None
                and code_pair == None
            ):
                italic_pair = i
                looking_for_pair = (i, Delimiters.ITALIC)

        if (
            i > 0
            and node.text[i] == Delimiters.ITALIC.value
            and node.text[i - 1] != " "  # right delimiter (end)
            and node.text[i - 1] != Delimiters.ITALIC.value  # not end of BOLD
            and italic_pair != None
            and i != italic_pair
        ):
            if bold_pair != None and italic_pair < bold_pair:
                transformation_pair = i
            else:
                if code_pair == None or code_pair != last_code_symbol:
                    if node.text[italic_pair + 1] == Delimiters.ITALIC.value:
                        italic_pair += 1
                    res.append(
                        TextNode(
                            node.text[italic_pair + 1 : i],
                            TextType.TEXT_ITALIC,
                        )
                    )
                    node.text = node.text[:italic_pair] + node.text[i + 1 :]
                    i = 0
                    italic_pair = None
                    code_pair = None
                    bold_pair = None
                    continue

        if i + 1 >= len(node.text):
            if bold_pair != None:
                if transformation_pair != None and italic_pair != None:
                    res.append(
                        TextNode(
                            node.text[italic_pair + 1 : i],
                            TextType.TEXT_ITALIC,
                        )
                    )
                    node.text = node.text[:italic_pair] + node.text[i + 1 :]
                    transformation_pair = None

                if bold_pair + 2 <= len(node.text) - 1:
                    if (
                        node.text[bold_pair + 2] != Delimiters.ITALIC.value
                    ):  # Not another bold possibility
                        italic_pair = bold_pair  # try italic since bold unmatched
                looking_for_pair = (bold_pair + 1, Delimiters.BOLD)
                i = bold_pair
                bold_pair = None
            elif italic_pair != None:
                i = italic_pair
                looking_for_pair = (italic_pair, Delimiters.ITALIC)
                italic_pair = None
            i += 1
            continue

        i += 1
    return res
