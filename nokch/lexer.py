"""lexical analysis 😃"""

from typing import Any

from .err import ErrorReporter
from .tokens import E, T, Token


class Lexer:
    def __init__(self, code, filename: str = "<stdin>") -> None:
        if isinstance(code, str):
            code = [code]
        self.lines = code
        self.line_index = 0
        self.line = 1  # current line number
        self.text = self.lines[self.line_index] if self.lines else ""
        self.pos = 0
        self.col = 0  # current column
        self.c_char = self.text[0] if self.text else None

        self.error = ErrorReporter(filename, self.lines)

    def advance(self, offset: int = 1) -> None:
        for _ in range(offset):
            if self.c_char == "\n":
                self.line += 1
                self.col = 0
            else:
                self.col += 1

            self.pos += 1
            self.c_char = self.text[self.pos] if self.pos < len(self.text) else None

    def peek(self, offset: int = 1) -> str | None:
        pos = self.pos + offset
        return self.text[pos] if pos < len(self.text) else None

    def tok(
        self, type_: T, val: Any = None, *, pos: tuple[int, int] | None = None
    ) -> Token:
        if pos is None:
            return Token(type_, val, line=self.line, col=self.col)
        return Token(type_, val, line=pos[0], col=pos[1])

    def err(self, message: str, err_type: E) -> None:
        self.error(message, err_type, (self.line, self.col))

    def skip_whitespace(self) -> None:
        while self.c_char is not None and self.c_char.isspace():
            self.advance()

    def number(self) -> Token:
        num_str = ""
        has_dot = False
        while self.c_char is not None and (self.c_char.isdigit() or self.c_char == "."):
            if self.c_char == ".":
                if has_dot:
                    break
                has_dot = True
            num_str += self.c_char
            self.advance()
        if has_dot:
            return self.tok(T.FLOAT, float(num_str))
        return self.tok(T.INT, int(num_str))

    def identifier(self) -> Token:
        result = ""

        if self.c_char is not None and (self.c_char.isalpha() or self.c_char == "_"):
            result += self.c_char
            self.advance()

            while self.c_char is not None and (
                self.c_char.isalnum() or self.c_char == "_"
            ):
                result += self.c_char
                self.advance()

        else:
            raise ValueError(f"Invalid identifier start: {self.c_char}")

        keywords = {
            "if": T.IF,
            "else": T.ELSE,
            "true": T.TRUE,
            "false": T.FALSE,
            "null": T.NULL,
        }
        token_type = keywords.get(result, T.IDENT)

        if token_type == T.ELSE:
            offset = 0
            while (next_char := self.peek(offset)) is not None and next_char.isspace():
                offset += 1

            if next_char == "i" and self.peek(offset + 1) == "f":
                self.advance(offset + 2)  # advance past `if`
                token_type = T.ELSE_IF
        return self.tok(token_type, result if token_type == T.IDENT else None)

    def string(self) -> Token:
        if self.c_char not in ('"', "'"):
            self.err("Expected string literal start", E.SYNTAX)
            return self.tok(T.STRING, None)

        quote_type = self.c_char
        self.advance()  # skip opening quote

        content = ""
        while self.c_char is not None and self.c_char != quote_type:
            if self.c_char == "\\":
                self.advance()
                if self.c_char is None:
                    break
                escape_chars = {
                    "n": "\n",
                    "t": "\t",
                    "r": "\r",
                    '"': '"',
                    "'": "'",
                    "\\": "\\",
                }
                escaped = escape_chars.get(self.c_char)
                content += self.c_char if escaped is None else escaped
            else:
                content += self.c_char
            self.advance()

        if self.c_char != quote_type:
            self.err("Unterminated string literal", E.SYNTAX)
        else:
            self.advance()  # skip closing quote

        return Token(
            type_=T.STRING,
            val=None,  # val can be None since actual content is in metadata
            metadata={"content": content},
            line=(self.line, self.col),
        )

    def get_next_token(self) -> Token:
        while self.c_char is not None:
            if self.c_char.isspace():
                self.skip_whitespace()
                continue

            if self.c_char.isdigit():
                return self.number()

            if self.c_char.isalpha() or self.c_char == "_":
                return self.identifier()

            if self.c_char == '"' or self.c_char == "'":
                return self.string()

            if self.c_char == "+":
                self.advance()
                if self.c_char == "+":  # ++
                    return self.tok(T.INC)
                if self.c_char == "=":  # +=
                    self.advance()
                    return self.tok(T.ADD_AUG)
                return self.tok(T.ADD)
            if self.c_char == "-":
                self.advance()
                if self.c_char == "-":  # --
                    return self.tok(T.DEC)
                if self.c_char == "=":  # -=
                    self.advance()
                    return self.tok(T.SUB_AUG)
                return self.tok(T.SUB)
            if self.c_char == "*":
                self.advance()
                if self.c_char == "*":  # **
                    self.advance()
                    if self.c_char == "=":  # **=
                        self.advance()
                        return self.tok(T.POW_AUG)
                    return self.tok(T.POW)
                if self.c_char == "=":  # *=
                    self.advance()
                    return self.tok(T.MUL_AUG)
                return self.tok(T.MUL)
            if self.c_char == "/":
                self.advance()
                if self.c_char == "/":  # //
                    self.advance()
                    return self.tok(T.FDIV)
                if self.c_char == "=":  # /=
                    self.advance()
                    return self.tok(T.DIV_AUG)
                return self.tok(T.DIV)
            if self.c_char == "%":
                self.advance()
                if self.c_char == "=":  # %=
                    self.advance()
                    return self.tok(T.MOD_AUG)
                return self.tok(T.MOD)
            if self.c_char == "=":
                self.advance()
                if self.c_char == "=":
                    self.advance()
                    return self.tok(T.EQ)
                return self.tok(T.ASSIGN)
            if self.c_char == "!":
                self.advance()
                if self.c_char == "=":
                    self.advance()
                    return self.tok(T.NE)
                self.err("invalid syntax", E.SYNTAX)
            if self.c_char == "<":
                self.advance()
                if self.c_char == "=":  # <=
                    self.advance()
                    return self.tok(T.LE)
                if self.c_char == "<":  # <<
                    self.advance()
                    if self.c_char == "=":
                        self.advance()
                        return self.tok(T.LSHIFT_AUG)
                    return self.tok(T.LSHIFT)
                return self.tok(T.LT)
            if self.c_char == ">":
                self.advance()
                if self.c_char == "=":  # >=
                    self.advance()
                    return self.tok(T.GE)
                if self.c_char == ">":  # >>
                    self.advance()
                    if self.c_char == "=":
                        self.advance()
                        return self.tok(T.RSHIFT_AUG)
                    return self.tok(T.RSHIFT)
                return self.tok(T.GT)
            if self.c_char == "(":
                self.advance()
                return self.tok(T.LPAREN)
            if self.c_char == ")":
                self.advance()
                return self.tok(T.RPAREN)
            if self.c_char == "[":
                self.advance()
                return self.tok(T.LBRACKET)
            if self.c_char == "]":
                self.advance()
                return self.tok(T.RBRACKET)
            if self.c_char == "{":
                self.advance()
                return self.tok(T.LBRACE)
            if self.c_char == "}":
                self.advance()
                return self.tok(T.RBRACE)
            if self.c_char == "&":
                self.advance()
                if self.c_char == "=":  # &=
                    self.advance()
                    return self.tok(T.BAND_AUG)
                return self.tok(T.BIT_AND)
            if self.c_char == "|":
                self.advance()
                if self.c_char == "=":  # |=
                    self.advance()
                    return self.tok(T.BOR_AUG)
                return self.tok(T.BIT_OR)
            if self.c_char == "^":
                self.advance()
                if self.c_char == "=":  # ^=
                    self.advance()
                    return self.tok(T.BXOR_AUG)
                return self.tok(T.BIT_XOR)
            if self.c_char == "~":
                self.advance()
                return self.tok(T.BIT_NOT)
            if self.c_char == ";":
                self.advance()
                return self.tok(T.SEMI)
            if self.c_char == ",":
                self.advance()
                return self.tok(T.COMMA)

            self.err("unexpected " + self.c_char, E.SYNTAX)
        return self.tok(T.EOF)

    def next_line(self) -> bool:
        """Move to the next line if any. Returns False if no more lines."""
        self.line_index += 1
        if self.line_index < len(self.lines):
            self.text = self.lines[self.line_index]
            self.pos = 0
            self.col = 0
            self.c_char = self.text[0] if self.text else None
            self.line += 1
            return True
        return False

    def __call__(self):
        tokens = []
        while True:
            while (tok := self.get_next_token()).type != T.EOF:
                tokens.append(tok)
            if not self.next_line():
                break
        self.advance()
        tokens.append(self.tok(T.EOF))
        return tokens
