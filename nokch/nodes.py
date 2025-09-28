from dataclasses import dataclass
from typing import Union


@dataclass
class Number:
    value: int | float


@dataclass
class BinOp:
    op: str
    left: "AST"
    right: "AST"


AST = Union[Number, BinOp]
