from htmlnode import HTMLNode
from textnode import TextNode, TextType


def main():
    txt_nd = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev")
    htmltxt_nd = HTMLNode("a", "This is a Link", None, {"href":"https://www.boot.dev","target":"_blank"})

    print(txt_nd, htmltxt_nd.props_to_html())

if __name__ == "__main__":
    main()
