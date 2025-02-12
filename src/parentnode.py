from collections.abc import Sequence
from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: Sequence[HTMLNode], props: None | dict = None) -> None:
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("All ParentNodes requires a tag")
        if not self.children:
            raise ValueError("All ParentNodes requires a children object")
        return f"<{self.tag}{self.props_to_html() if self.props else ''}>{''.join([c.to_html() for c in self.children])}</{self.tag}>" 

    def __repr__(self) -> str:
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
