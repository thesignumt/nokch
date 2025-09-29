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
class UnaryOp:
    op: T
    operand: "AST"


@dataclass
class Var:
    name: str


@dataclass
class String:
    value: str


@dataclass
class Assign:
    target: Var  # variable being assigned
    value: "AST"  # expression assigned to it
    op: T = T.ASSIGN  # assignment operator (default "=")


AST = Union["Number", "BinOp", "UnaryOp", "Var", "Assign", "String"]
