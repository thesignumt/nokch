from pathlib import Path

from icecream import ic

from .lexer import Lexer
from .parser import Parser


class Interpreter:
    def __init__(self, filepath: Path) -> None:
        self.file = filepath
        lines = self.file.read_text().splitlines()
        path = str(self.file.absolute())
        tokens = Lexer(lines, path)()
        ic(tokens)

        parser = Parser(tokens, path, lines)
        ast = parser.parse()
        ic(ast)
