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

    # Bitwise Operators
    BIT_AND = "&"
    BIT_OR = "|"
    BIT_XOR = "^"
    BIT_NOT = "~"
    LSHIFT = "<<"
    RSHIFT = ">>"

    # Literals
    IDENTIFIER = "IDENTIFIER"
    INT = "INT"
    FLOAT = "FLOAT"
    STRING = "STRING"
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
    def __init__(
        self,
        type_: T,
        val: Any = None,
        metadata: dict[str, Any] | None = None,
        *,
        pos: tuple[int, int],
    ) -> None:
        self.type = type_
        self.val = val
        self.metadata = metadata if metadata is not None else {}
        self.pos = pos  # (line, col) tuple

    def __repr__(self) -> str:
        line, col = self.pos
        info: list[Any] = [self.type]
        if self.val is not None:
            info.append(self.val)
        info.append(f"pos=({line},{col})")
        return f"Token({', '.join(info)})"


class E(str, Enum):
    """error types"""

    ERROR = "ERROR"  # general error
    SYNTAX = "SYNTAX"
    TYPE = "TYPE"  # wrong type "5" + 3
    NAME = "NAME"  # name not defined in scope print(x)
    VALUE = "VALUE"  # bad value for type int('abc')
    RUNTIME = "RUNTIME"
