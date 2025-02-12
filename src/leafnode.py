from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, value: str, tag: None | str = None, props: None | dict = None) -> None:
        super().__init__(tag=tag,value=value,props=props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("All LeafNodes requires a value")
        if self.tag is None:
            return f"{self.value}"
        return f"<{self.tag}{self.props_to_html() if self.props else ''}>{self.value}</{self.tag}>" 

