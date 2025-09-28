from .err import ErrorReporter
from .nodes import BinOp, Number
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

    def advance(self) -> Token | None:
        tok = self.peek()
        if tok:
            self.pos += 1
        return tok

    def eat(self, expected_type: T) -> Token:
        tok = self.peek()
        if tok and tok.type == expected_type:
            return self.advance()  # pyright: ignore
        got = tok.type if tok else "EOF"
        pos = (tok.line, tok.col) if tok else (-1, -1)
        self.err(f"expected {expected_type}, got {got}", E.SYNTAX, pos)

    # Grammar rules
    def factor(self):
        tok = self.peek()
        if tok is None:
            line = self.tokens[-1].line
            col = self.tokens[-1].col
            self.err("unexpected EOF", E.SYNTAX, (line, col))

        if tok.type == T.INT:
            return Number(int(self.eat(T.INT).val))
        elif tok.type == T.FLOAT:
            return Number(float(self.eat(T.FLOAT).val))
        elif tok.type == T.LPAREN:
            self.eat(T.LPAREN)
            node = self.expr()
            self.eat(T.RPAREN)
            return node
        elif tok.type == T.IDENT:
            return Var(self.eat(T.IDENT).val)
        self.err("unexpected token", E.SYNTAX, tok)

    def term(self):
        node = self.factor()
        while (tok := self.peek()) and tok.type in (T.MUL, T.DIV, T.FDIV, T.MOD, T.POW):
            op = self.eat(tok.type).type
            node = BinOp(node, op, self.factor())
        return node

    def expr(self):
        node = self.term()
        while (tok := self.peek()) and tok.type in (T.ADD, T.SUB):
            op = self.eat(tok.type).type
            node = BinOp(node, op, self.term())
        return node
