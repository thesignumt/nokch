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
    COMMA = ","

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
    BAND_AUG = "&="
    BOR_AUG = "|="
    BXOR_AUG = "^="
    LSHIFT_AUG = "<<="
    RSHIFT_AUG = ">>="

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
    IDENT = "IDENT"
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
    LBRACKET = "["
    RBRACKET = "]"
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
        line: int,
        col: int = 0,
    ) -> None:
        self.type = type_
        self.val = val
        self.metadata = metadata if metadata is not None else {}
        self.line = line
        self.col = col

    def __repr__(self) -> str:
        parts = [f"{self.type}"]
        if self.val is not None:
            parts.append(repr(self.val))
        parts.append(f"line={self.line}, col={self.col}")
        return "Token(" + ", ".join(parts) + ")"


class E(str, Enum):
    """error types"""

    ERROR = "ERROR"  # general error
    SYNTAX = "SYNTAX"
    TYPE = "TYPE"  # wrong type "5" + 3
    NAME = "NAME"  # name not defined in scope print(x)
    VALUE = "VALUE"  # bad value for type int('abc')
    RUNTIME = "RUNTIME"
