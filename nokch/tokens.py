from enum import Enum
from typing import Any


class T(Enum):
    """token types for nokch"""

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

    # Comparison Operators
    EQ = "=="
    NE = "!="
    LT = "<"
    LE = "<="
    GT = ">"
    GE = ">="

    # Literals
    IDENTIFIER = "IDENTIFIER"
    INT = "INT"
    FLOAT = "FLOAT"
    STR = "STR"

    # Keywords
    IF = "IF"
    ELSE = "ELSE"

    # Delimiters
    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"

    # Special
    EOF = "EOF"


class Token:
    def __init__(self, type_: T, val: Any = None) -> None:
        self.type = type_
        self.val = val

    def __repr__(self) -> str:
        if self.val is not None:
            return f"Token({self.type}, {self.val})"
        return f"Token({self.type})"
