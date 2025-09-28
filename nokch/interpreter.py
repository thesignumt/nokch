from pathlib import Path
from typing import Any

from icecream import ic

from .lexer import Lexer
from .parser import Parser
from .tokens import E


class Interpreter:
    def __init__(self, filepath: Path) -> None:
        self.file = filepath

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        lines = self.file.read_text().splitlines()
        path = str(self.file.absolute())
        tokens = Lexer(lines, path)()
        ic(tokens)

        parser = Parser(tokens, path, lines)
        ast = parser.expr()
        ic(ast)
