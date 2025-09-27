from pathlib import Path
from typing import Any

from icecream import ic

from .lexer import Lexer


class Interpreter:
    def __init__(self, filepath: Path) -> None:
        self.file = filepath

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        lines = self.file.read_text().splitlines()
        tokens = Lexer(lines)()
        ic(tokens)
