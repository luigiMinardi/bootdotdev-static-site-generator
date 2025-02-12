from __future__ import annotations
from collections.abc import Sequence

class HTMLNode:
    def __init__(self, tag: None | str = None, value: None | str = None, children: None | Sequence[HTMLNode] = None, props: None | dict = None) -> None:
        self.tag: None | str = tag
        self.value: None | str = value
        self.children: None | Sequence[HTMLNode] = children
        self.props: None | dict = props

    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self) -> str:
        props = ""
        if self.props:
            for value in self.props:
                props += f' {value}="{self.props[value]}"'
        return props

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, HTMLNode):
            return (self.tag, self.value, self.children, self.props) == (__value.tag, __value.value, __value.children, __value.props)
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

