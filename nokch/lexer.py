"""lexical analysis 😃"""

from .tokens import T, Token


class Lexer:
    def __init__(self, code) -> None:
        if isinstance(code, str):
            code = [code]  # normalize list[str]
        self.lines = code
        self.line_index = 0
        self.text = self.lines[self.line_index] if self.lines else ""
        self.pos = 0
        self.c_char = self.text[0] if self.text else None

    def advance(self, offset: int = 1) -> None:
        self.pos += offset
        if self.pos < len(self.text):
            self.c_char = self.text[self.pos]
        else:
            self.c_char = None

    def peek(self, offset: int = 1) -> str | None:
        pos = self.pos + offset
        if pos < len(self.text):
            return self.text[pos]
        return None

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
            return Token(T.FLOAT, float(num_str))
        return Token(T.INT, int(num_str))

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

        keywords = {"if": T.IF, "else": T.ELSE}
        token_type = keywords.get(result, T.IDENTIFIER)

        if token_type == T.ELSE:
            offset = 0
            while (next_char := self.peek(offset)) is not None and next_char.isspace():
                offset += 1

            if next_char == "i" and self.peek(offset + 1) == "f":
                self.advance(offset + 2)  # advance past `if`
                token_type = T.ELSE_IF
        return Token(token_type, result if token_type == T.IDENTIFIER else None)

    def get_next_token(self) -> Token:
        while self.c_char is not None:
            if self.c_char.isspace():
                self.skip_whitespace()
                continue

            if self.c_char.isdigit():
                return self.number()

            if self.c_char.isalpha() or self.c_char == "_":
                return self.identifier()

            if self.c_char == "+":
                self.advance()
                if self.c_char == "+":
                    return Token(T.INC)
                return Token(T.ADD)
            if self.c_char == "-":
                self.advance()
                if self.c_char == "+":
                    return Token(T.INC)
                return Token(T.SUB)
            if self.c_char == "*":
                self.advance()
                if self.c_char == "*":
                    self.advance()
                    return Token(T.POW)
                return Token(T.MUL)
            if self.c_char == "/":
                self.advance()
                if self.c_char == "/":
                    self.advance()
                    return Token(T.FDIV)
                return Token(T.DIV)
            if self.c_char == "%":
                self.advance()
                return Token(T.MOD)
            if self.c_char == "=":
                self.advance()
                if self.c_char == "=":
                    self.advance()
                    return Token(T.EQ)
                return Token(T.ASSIGN)
            if self.c_char == "!":
                self.advance()
                if self.c_char == "=":
                    self.advance()
                    return Token(T.NE)
                else:
                    pass  # raise unexpected character '!' at position
            if self.c_char == "<":
                self.advance()
                if self.c_char == "=":
                    self.advance()
                    return Token(T.LE)
                return Token(T.LT)
            if self.c_char == ">":
                self.advance()
                if self.c_char == "=":
                    self.advance()
                    return Token(T.GE)
                return Token(T.GT)
            if self.c_char == "(":
                self.advance()
                return Token(T.LPAREN)
            if self.c_char == ")":
                self.advance()
                return Token(T.RPAREN)
            if self.c_char == "{":
                self.advance()
                return Token(T.LBRACE)
            if self.c_char == "}":
                self.advance()
                return Token(T.RBRACE)
            if self.c_char == ";":
                self.advance()
                return Token(T.SEMICOLON)

            raise ValueError(f"Unknown character: {self.c_char}")

        return Token(T.EOF)

    def next_line(self) -> bool:
        """Move to the next line if any. Returns False if no more lines."""
        self.line_index += 1
        if self.line_index < len(self.lines):
            self.text = self.lines[self.line_index]
            self.pos = 0
            self.c_char = self.text[0] if self.text else None
            return True
        return False

    def __call__(self):
        tokens = []
        while True:
            while (tok := self.get_next_token()).type != T.EOF:
                tokens.append(tok)
            if not self.next_line():
                break
        tokens.append(Token(T.EOF))
        return tokens
