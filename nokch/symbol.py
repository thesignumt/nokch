from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class Symbol:
    name: str  # identifier
    type: str  # semantic type: "int", "float", "string", "func", etc.
    meta: dict[str, Any] = field(default_factory=dict)  # extra attributes


_ROOT = object()


class SymbolTable:
    def __init__(
        self, scope_name: str | object = _ROOT, parent: Optional["SymbolTable"] = None
    ):
        self.scope_name = scope_name
        self.symbols: dict[str, Symbol] = {}
        self.parent = parent

    @property
    def is_root(self) -> bool:
        return self.parent is None

    def define(self, symbol: Symbol) -> None:
        if symbol.name in self.symbols:
            raise Exception(f"Redefinition of {symbol.name} in scope {self.scope_name}")
        self.symbols[symbol.name] = symbol

    def resolve(self, name: str) -> Symbol | None:
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.resolve(name)
        return None

    def __repr__(self) -> str:
        name = "<root>" if self.is_root else self.scope_name
        parent = self.parent.scope_name if self.parent else None
        return f"<Scope {name}, parent={parent}, symbols={list(self.symbols.keys())}>"
