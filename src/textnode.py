from enum import Enum


class TextType(Enum):
    TEXT_NORMAL = "normal"
    TEXT_BOLD = "bold"
    TEXT_ITALIC = "italic"
    TEXT_CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, txt_type: TextType, url: None | str = None) -> None:
        self.text: str = text
        self.text_type: TextType = txt_type
        self.url: None | str = url

        if not isinstance(self.text_type, TextType):
            raise TypeError(f"{self.text_type} is not of type {TextType}")

        if self.url and (
            self.text_type is not TextType.LINK and self.text_type is not TextType.IMAGE
        ):
            """
            what is here is not a LINK nor an IMAGE but it has an URL value
            thus should raise an error
            """
            raise ValueError(
                f"url doesn't work with the text type {self.text_type}, use {TextType.IMAGE} or {TextType.LINK}"
            )

        if not self.url and (
            self.text_type is TextType.LINK or self.text_type is TextType.IMAGE
        ):
            """
            what is here is either a LINK or an IMAGE but it DOESNT have an URL
            thus should raise an error
            """
            raise ValueError(
                f"url is needed in the text type {self.text_type}, add an url please."
            )

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, TextNode):
            return (self.text, self.text_type, self.url) == (
                __value.text,
                __value.text_type,
                __value.url,
            )
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"TextNode('{self.text}', {self.text_type}, {"'" + self.url + "'" if self.url else None})"
