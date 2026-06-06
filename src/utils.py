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
    ITALIC = "_"
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
    """
    Given a TextNode list (old_nodes) convert all nodes with
    TextType.TEXT_NORMAL that have the given delimiter at least twice and in
    pairs (e.g. delimiter is ** and the text is "**foo**" and not "**foo" or
    "**foo** **bar") split at the delimiter returning a new TextNode with the
    given text_type.

    Example:
    old_nodes = [TextNode("**foo** bar", TextType.TEXT_NORMAL)]
    delimiter = "**"
    text_type = TextType.TEXT_BOLD

    Results in:
    [
        TextNode("foo", TextType.TEXT_BOLD),
        TextNode(" bar", TextType.TEXT_NORMAL)
    ])

    Arguments:
        old_nodes (list[TextNode]): list of nodes to split by delimiter
        delimiter (str): delimiter to be used on the split
        text_type (TextType): TextType of the new nodes after the split
    Return:
        list[TextNode]: a new nodes list where normal text that had the
        delimiter were changed into text_type TextNode's, nodes that had a type
        other than normal were kept unchanged
    """
    return_list: list[TextNode] = []

    for node in old_nodes:
        if node.text_type is not TextType.TEXT_NORMAL:
            return_list.append(node)
            continue

        text: str = node.text
        delimiter_ranges_list: list[int] = list(find_all(text, delimiter))
        if len(delimiter_ranges_list) == 0:
            return_list.append(
                TextNode(text, TextType.TEXT_NORMAL))
            continue

        if len(delimiter_ranges_list) % 2 != 0:
            raise Exception(f"Invalid markdown syntax, delimiter found at {
                            delimiter_ranges_list[-1]
                            } did not found a closing pair")

        last_iteration: int = 0
        for i in range(1, len(delimiter_ranges_list), 2):
            start_with_delimiter: int = delimiter_ranges_list[i - 1]
            end_without_delimiter: int = delimiter_ranges_list[i]
            start_without_delimiter: int = start_with_delimiter + \
                len(delimiter)

            node_before_delimiter: int
            if i == 1:
                node_before_delimiter: str = text[:start_with_delimiter]
            else:
                previous_end_with_delimiter: int = delimiter_ranges_list[i-2] \
                    + len(delimiter)
                node_before_delimiter: str = \
                    text[previous_end_with_delimiter:start_with_delimiter]

            if node_before_delimiter != "":
                return_list.append(
                    TextNode(node_before_delimiter, TextType.TEXT_NORMAL))
            return_list.append(
                TextNode(
                    text[start_without_delimiter:end_without_delimiter],
                    text_type))
            last_iteration = i

        if (last_iteration != 0 and
            delimiter_ranges_list[last_iteration]
                + len(delimiter) < len(text) - 1):
            return_list.append(
                TextNode(
                    text[delimiter_ranges_list[last_iteration] +
                         len(delimiter):],
                    TextType.TEXT_NORMAL))
    if len(return_list) == 0:
        raise Exception(f"Empty list with:\nold_nodes {
            old_nodes}\ndelimiter {
            delimiter}\ntext_type: {text_type}")
    return return_list


def extract_markdown_images(text: str) -> list[tuple[str, str, int, int]]:
    """
    Check if a string has markdown images inside of it and return its values as
    tuples in a list being the first value the alt text and the second value
    the url.

    Arguments:
        text (str): text to search
    Return:
        list[tuple[str, str]]: a list with tuples representing all images
        found, the first argument is the alt text the second is the image url,
        the third is the start index and the forth is the closing index, the
        index are of the start of the position of its delimiter, so you need to
        take into account the delimiter lenght if you want to exclude it from
        your result. If nothing is found returns an empty list.
    """

    return_list: list[tuple[str, str, int, int]] = []
    i = 0
    while i < len(text):
        start = text.find(Delimiters.IMAGE.value, i)
        middle = text.find(Delimiters.LINK_MID.value, start)
        end = text.find(Delimiters.LINK_CLOSE.value, middle)

        check = 0
        while check != -1:
            check = text.find(
                Delimiters.LINK_MID.value, middle + 1, end)
            if check != -1 and middle != check:
                middle = check

        if start != -1 and middle != -1 and end != -1:
            return_list.append((
                text[start+len(Delimiters.IMAGE.value):middle],
                text[middle+len(Delimiters.LINK_MID.value):end],
                start,
                end
            ))
            i = end
        else:
            break
    return return_list


def extract_markdown_links(text: str) -> list[tuple[str, str, int, int]]:
    """
    Check if a string has markdown links inside of it and return its values as
    tuples in a list being the first value the anchor text and the second value
    the url.

    Arguments:
        text (str): text to search
    Return:
        list[tuple[str, str, int, int]]: a list with tuples representing all
        links found, the first argument is the anchor text the second is the
        image url, the third is the start index and the forth is the closing
        index, the index are of the start of the position of its delimiter, so
        you need to take into account the delimiter lenght if you want to
        exclude it from your result. If nothing is found returns an empty list.
    """

    return_list: list[tuple[str, str, int, int]] = []
    i = 0
    while i < len(text):
        start = text.find(Delimiters.LINK.value, i)
        if start > 0 and text[start - 1] == "!":
            i = start + 1
            continue

        middle = text.find(Delimiters.LINK_MID.value, start)
        end = text.find(Delimiters.LINK_CLOSE.value, middle)

        check = 0
        while check != -1:
            check = text.find(
                Delimiters.LINK_MID.value, middle + 1, end)
            if check != -1 and middle != check:
                middle = check

        if start != -1 and middle != -1 and end != -1:
            return_list.append((
                text[start+len(Delimiters.LINK.value):middle],
                text[middle+len(Delimiters.LINK_MID.value):end],
                start,
                end,
            ))
            i = end
        else:
            break
    return return_list


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    """
    Given a TextNode list (old_nodes) convert all nodes with
    TextType.TEXT_NORMAL that have images into image nodes

    Arguments:
        old_nodes (list[TextNode]): list of nodes that might be converted
    Return:
        list[TextNode]: a new nodes list where normal text that had images
        were changed into TextNode's with type TextType.IMAGE, nodes that had a
        type other than normal were kept unchanged
    """
    return_list: list[TextNode] = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT_NORMAL:
            return_list.append(node)
            continue

        text: str = node.text
        images: list[tuple[str, str, int, int]] = extract_markdown_images(text)
        if len(images) == 0:
            return_list.append(
                TextNode(text, TextType.TEXT_NORMAL))
            continue

        last_parsed_idx: int = 0
        for i in range(len(images)):
            image = images[i]
            if i == 0 and image[2] != 0:
                return_list.append(
                    TextNode(text[:image[2]], TextType.TEXT_NORMAL)
                )
            else:
                return_list.append(
                    TextNode(
                        text[images[i-1][3] +
                             len(Delimiters.LINK_CLOSE.value):image[2]],
                        TextType.TEXT_NORMAL)
                )
            return_list.append(TextNode(image[0], TextType.IMAGE, image[1]))
            last_parsed_idx = image[3]
        if last_parsed_idx != 0 and last_parsed_idx + 1 < len(text) - 1:
            return_list.append(
                TextNode(text[last_parsed_idx+1:],
                         TextType.TEXT_NORMAL)
            )
    return return_list


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    """
    Given a TextNode list (old_nodes) convert all nodes with
    TextType.TEXT_NORMAL that have links into link nodes

    Arguments:
        old_nodes (list[TextNode]): list of nodes that might be converted
    Return:
        list[TextNode]: a new nodes list where normal text that had links
        were changed into TextNode's with type TextType.LINK, nodes that had a
        type other than normal were kept unchanged
    """
    return_list: list[TextNode] = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT_NORMAL:
            return_list.append(node)
            continue

        text: str = node.text
        links: list[tuple[str, str, int, int]] = extract_markdown_links(text)
        if len(links) == 0:
            return_list.append(
                TextNode(text, TextType.TEXT_NORMAL))
            continue

        last_parsed_idx: int = 0
        for i in range(len(links)):
            link = links[i]
            if i == 0 and link[2] != 0:
                return_list.append(
                    TextNode(text[:link[2]], TextType.TEXT_NORMAL)
                )
            else:
                return_list.append(
                    TextNode(
                        text[links[i-1][3] +
                             len(Delimiters.LINK_CLOSE.value):link[2]],
                        TextType.TEXT_NORMAL)
                )
            return_list.append(TextNode(link[0], TextType.LINK, link[1]))
            last_parsed_idx = link[3]
        if last_parsed_idx != 0 and last_parsed_idx + 1 < len(text) - 1:
            return_list.append(
                TextNode(text[last_parsed_idx+1:],
                         TextType.TEXT_NORMAL)
            )
    return return_list


def text_to_textnodes(text: str) -> list[TextNode]:
    """
    Given a text string convert all markdown delimiters into their TextNode's

    Arguments:
        text (str): text to be converted
    Return:
        list[TextNode]: a nodes list where every delimiter were converted into
        the correct TextNode.
    """
    start = [TextNode(text, TextType.TEXT_NORMAL)]
    images = split_nodes_image(start)
    links = split_nodes_link(images)
    bold = split_nodes_delimiter(
        links, Delimiters.BOLD.value, TextType.TEXT_BOLD)
    italic = split_nodes_delimiter(
        bold, Delimiters.ITALIC.value, TextType.TEXT_ITALIC)
    code = split_nodes_delimiter(
        italic, Delimiters.CODE.value, TextType.TEXT_CODE)
    return code


if __name__ == "__main__":
    """
    This is development testing, I'll leve it here to show a little of my
    toughts, it might be deleted/changed anytime and you shouldn't run this
    file directly unless developing in it and wanting to think about something.

    The state of tests here should be considered wrong and be rewritten every
    new time you use it unless you're still working on the same feature and not
    in the master branch
    """
    deli = "**"
    txt = "foo *bar **bazz**, **bar *bazz foo bar ** foo *bazz*"
    #      0123456789
    txt2 = "**bazz**, **bar *bazz foo bar **"
    txt3 = "this is a parsed bold text"
    nodes: list[TextNode] = [TextNode(txt, TextType.TEXT_NORMAL), TextNode(
        txt2, TextType.TEXT_NORMAL), TextNode("", TextType.TEXT_NORMAL), TextNode(txt3, TextType.TEXT_BOLD)]
    print(split_nodes_delimiter(nodes, "**", TextType.TEXT_BOLD))
    print(txt)
    lst = list(find_all(txt, deli))
    # [9, 15, 19, 39, 46]
    print(lst)
    last_iter: int = 0
    for i in range(1, len(lst), 2):
        start_with_deli = lst[i - 1]
        end_without_deli = lst[i]
        start_without_deli = start_with_deli + len(deli)
        end_with_deli = end_without_deli + len(deli)
        print(start_with_deli, end_with_deli,
              txt[start_with_deli:end_with_deli])
        print(start_without_deli, end_without_deli,
              txt[start_without_deli:end_without_deli])
        if i == 1:
            start = txt[:start_with_deli]
        else:
            previous_end_with_deli = lst[i-2]+len(deli)
            start = txt[previous_end_with_deli:start_with_deli]
        print('ist', i, start, len(start), start == "")
        if start != "":
            print('make start normal text')
        print('make start_without:end_without bold text')
        last_iter = i
        print('lip', last_iter, i)
    print('last iter', lst[last_iter], 'txt len', len(
        txt), 'lasttxt', len(txt)-1, txt[-1] == txt[len(txt)-1])
    if last_iter != 0 and lst[last_iter]+len(deli) < len(txt)-1:
        print('make lst[last_iter]+len(deli): normal text')
