from dataclasses import dataclass
from typing import Union

from .tokens import T


@dataclass
class Number:
    value: int | float


@dataclass
class BinOp:
    left: "AST"
    op: T
    right: "AST"


AST = Union[Number, BinOp]
