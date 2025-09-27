from enum import Enum
from typing import Any


class T(Enum):
    """token types for nokch"""

    # Operators
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"
    MOD = "%"
    POW = "**"
    FDIV = "//"  # Floor DIVision
    ASSIGN = "="
    SEMICOLON = ";"

    # Incremental Operators
    INC = "++"
    DEC = "--"

    # Augmented Assignment Operators
    # AUG
    ADD_AUG = "+="
    SUB_AUG = "-="
    MUL_AUG = "*="
    DIV_AUG = "/="
    MOD_AUG = "%="
    POW_AUG = "**="
    FDIV_AUG = "//="

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
    TRUE = "TRUE"
    FALSE = "FALSE"
    NULL = "NULL"

    # Keywords
    IF = "IF"
    ELSE = "ELSE"
    ELSE_IF = "ELSE_IF"

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
