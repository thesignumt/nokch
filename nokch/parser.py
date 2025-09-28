from .err import ErrorReporter
from .tokens import E, T, Token


class Parser:
    def __init__(
        self, tokens: list[Token], file: str = "<stdin>", lines: list[str] | None = None
    ):
        self.tokens = tokens
        self.pos = 0

        self.err = ErrorReporter(file, lines)

    def peek(self) -> Token | None:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def eat(self, expected_type: T) -> Token:
        tok = self.peek()
        if tok and tok.type == expected_type:
            self.pos += 1
            return tok
        got = tok.type if tok else "EOF"
        pos = tok.line if tok else ("?", "?")
        self.err(f"expected {expected_type}, got {got}", E.SYNTAX, pos)

    # Grammar rules
    def factor(self):
        tok = self.peek()
        if tok is None:
            line = self.tokens[-1].line
            col = self.tokens[-1].col
            self.err("unexpected EOF", E.SYNTAX, (line, col))

        if tok.type == T.INT:
            return ("number", int(self.eat(T.INT).val))
        elif tok.type == T.FLOAT:
            return ("number", float(self.eat(T.FLOAT).val))
        elif tok.type == T.LPAREN:
            self.eat(T.LPAREN)
            node = self.expr()
            self.eat(T.RPAREN)
            return node
        self.err("unexpected token", E.SYNTAX, tok)

    def term(self):
        node = self.factor()
        while (tok := self.peek()) and tok.type in (T.MUL, T.DIV, T.FDIV, T.MOD, T.POW):
            op = self.eat(tok.type).type
            right = self.factor()
            node = (op, node, right)
        return node

    def expr(self):
        node = self.term()
        while (tok := self.peek()) and tok.type in (T.ADD, T.SUB):
            op = self.eat(tok.type).type
            right = self.term()
            node = (op, node, right)
        return node
