from typing import Self

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None,props=None) -> None:
        self.tag=tag
        self.value=value
        self.children=children
        self.props=props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self) -> str:
        props = ""
        if self.props:
            for value in self.props:
                props += f' {value}="{self.props[value]}"'
        return props

    def __eq__(self, __value: Self) -> bool:
        if isinstance(__value, HTMLNode):
            return (self.tag, self.value, self.children, self.props) == (__value.tag, __value.value, __value.children, __value.props)
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

