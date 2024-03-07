from typing import Self

class TextNode:
    def __init__(self, text: str, txt_type: str, url=None) -> None:
        self.text = text
        self.text_type = txt_type
        self.url = url

    def __eq__(self, __value: Self) -> bool:
        if isinstance(__value, TextNode):
            return (self.text, self.text_type, self.url) == (__value.text, __value.text_type, __value.url)
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


