from enum import Enum
from typing import Any


class Token:
    def __init__(self, type_: "T", val: Any = None) -> None:
        self.type = type_
        self.val = val

    def __repr__(self) -> str:
        if self.val is not None:
            return f"Token({self.type}, {self.val})"
        return f"Token({self.type})"


class T(Enum):
    # Operators
    PLUS = "+"
    MINUS = "-"
    MUL = "*"
    DIV = "/"
    MOD = "%"
    POW = "**"
    FLOORDIV = "//"
    ASSIGN = "="
    SEMICOLON = ";"

    # Literals
    IDENTIFIER = "IDENTIFIER"
    INT = "INT"
    FLOAT = "FLOAT"
    STR = "STR"

    # Special
    EOF = "EOF"
