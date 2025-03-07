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


def split_nodes_delimiter(
    old_nodes: Sequence[TextNode], delimiter: str, text_type: TextType
) -> None:
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


def split_nodes_delimiter2(
    old_nodes: Sequence[TextNode], delimiter: str, text_type: TextType
) -> Sequence[TextNode]:

    res: Sequence[TextNode] = []

    for node in old_nodes:
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

        # print("start", node.text)
        i = 0
        while i < len(node.text):
            print(
                "current",
                i,
                node.text[i],
                node.text,
                code_pair,
                bold_pair,
                italic_pair,
                image_start,
                link_middle,
                looking_for_pair,
            )
            if (
                i != 0
                and looking_for_pair != None
                and looking_for_pair[0] > 0
                and len(node.text[0 : looking_for_pair[0]]) > 0
            ):
                print(
                    "normal",
                    i,
                    looking_for_pair,
                    "'",
                    node.text[0 : looking_for_pair[0]],
                    "'",
                )
                res.append(
                    TextNode(
                        node.text[0 : looking_for_pair[0]],
                        TextType.TEXT_NORMAL,
                    )
                )
                print(node.text[looking_for_pair[0] :])
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
                print("code start", i)
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
                    # print("code text start", node.text)
                    print("code end", i)
                    res.append(
                        TextNode(
                            node.text[code_pair + 1 : i],
                            TextType.TEXT_CODE,
                        )
                    )
                    # print("s", node.text[: code_pair])
                    # print("e", node.text[i + 1 :])
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
                        print("img start", i)
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
                        print("link start", i)
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
                        print("image end", i)
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
                        print("link end", i)
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
                    print("open bold", i, "'", node.text, "'")

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
                        print(
                            "handling situation",
                            italic_pair,
                            bold_pair,
                            transformation_pair,
                            i,
                        )

                        res.append(
                            TextNode(
                                node.text[italic_pair + 1 : i + 1],
                                TextType.TEXT_ITALIC,
                            )
                        )
                        print("sit", node.text[italic_pair + 1 : i + 1])

                        print("s", node.text[:italic_pair])
                        print("e", node.text[i + 2 :])
                        node.text = node.text[:italic_pair] + node.text[i + 2 :]
                        print("handled", node.text)
                        i = 0

                        italic_pair = None
                        bold_pair = None
                        transformation_pair = None
                        continue
                    else:
                        if code_pair == None or code_pair != last_code_symbol:
                            print("bold end", i)
                            """
                            print("bold text start", node.text)
                            print(bold_pair, i)
                            print("bold:", node.text[bold_pair + 2 : i])
                            """
                            res.append(
                                TextNode(
                                    node.text[bold_pair + 2 : i],
                                    TextType.TEXT_BOLD,
                                )
                            )
                            """
                            print("s", node.text[:bold_pair])
                            print("e", node.text[i + 2 :])
                            """
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

                    print("open italic", i)

            if (
                i > 0
                and node.text[i] == Delimiters.ITALIC.value
                and node.text[i - 1] != " "  # right delimiter (end)
                and node.text[i - 1] != Delimiters.ITALIC.value  # not end of BOLD
                and italic_pair != None
                and i != italic_pair
            ):
                if bold_pair != None and italic_pair < bold_pair:
                    print("we have a situation")
                    transformation_pair = i
                else:
                    print("italic end", i)
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
                print("finish line")
                if bold_pair != None:
                    print("unmatch bold", i, bold_pair, looking_for_pair)
                    if bold_pair + 2 <= len(node.text):
                        if node.text[bold_pair + 2] != Delimiters.ITALIC.value:
                            italic_pair = bold_pair  # try italic since bold unmatched
                    looking_for_pair = (bold_pair + 1, Delimiters.BOLD)
                    i = bold_pair
                    bold_pair = None
                elif italic_pair != None:
                    print("unmatch italic", i, italic_pair, looking_for_pair)
                    i = italic_pair
                    looking_for_pair = (italic_pair, Delimiters.ITALIC)
                    italic_pair = None
                i += 1
                continue

            i += 1
        print("finish", node.text)

    print(res)
    return res
