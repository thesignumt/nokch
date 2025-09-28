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


@dataclass
class Var:
    name: str


@dataclass
class Assign:
    target: Var  # the variable being assigned
    value: "AST"  # the expression assigned to it


AST = Union["Number", "BinOp", "Var", "Assign"]
