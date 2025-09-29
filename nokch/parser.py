from .err import ErrorReporter
from .nodes import Assign, BinOp, Number, UnaryOp, Var
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

    def parse(self):
        stmts = []
        while (tok := self.peek()) and tok.type != T.EOF:
            stmts.append(self.statement())
        return stmts

    def statement(self):
        tok = self.peek()
        if tok and tok.type == T.IDENT:
            ident = self.eat(T.IDENT)
            if (next_tok := self.peek()) and next_tok.type in (
                T.ASSIGN,
                T.ADD_AUG,
                T.SUB_AUG,
                T.MUL_AUG,
                T.DIV_AUG,
                T.MOD_AUG,
                T.POW_AUG,
                T.FDIV_AUG,
                T.BAND_AUG,
                T.BOR_AUG,
                T.BXOR_AUG,
                T.LSHIFT_AUG,
                T.RSHIFT_AUG,
            ):
                op = self.eat(next_tok.type).type
                expr = self.expr()
                self.eat(T.SEMI)
                return Assign(Var(ident.val), expr, op)
        node = self.expr()
        tok = self.peek()
        if tok and tok.type == T.SEMI:
            self.eat(T.SEMI)
        return node

    # ----------------- expression precedence -----------------

    def expr(self):
        return self.comparison()

    def comparison(self):
        node = self.bitwise_or()
        while (tok := self.peek()) and tok.type in (
            T.EQ,
            T.NE,
            T.LT,
            T.LE,
            T.GT,
            T.GE,
        ):
            op = self.eat(tok.type).type
            node = BinOp(node, op, self.bitwise_or())
        return node

    def bitwise_or(self):
        node = self.bitwise_xor()
        while (tok := self.peek()) and tok.type == T.BIT_OR:
            op = self.eat(T.BIT_OR).type
            node = BinOp(node, op, self.bitwise_xor())
        return node

    def bitwise_xor(self):
        node = self.bitwise_and()
        while (tok := self.peek()) and tok.type == T.BIT_XOR:
            op = self.eat(T.BIT_XOR).type
            node = BinOp(node, op, self.bitwise_and())
        return node

    def bitwise_and(self):
        node = self.shift()
        while (tok := self.peek()) and tok.type == T.BIT_AND:
            op = self.eat(T.BIT_AND).type
            node = BinOp(node, op, self.shift())
        return node

    def shift(self):
        node = self.additive()
        while (tok := self.peek()) and tok.type in (T.LSHIFT, T.RSHIFT):
            op = self.eat(tok.type).type
            node = BinOp(node, op, self.additive())
        return node

    def additive(self):
        node = self.multiplicative()
        while (tok := self.peek()) and tok.type in (T.ADD, T.SUB):
            op = self.eat(tok.type).type
            node = BinOp(node, op, self.multiplicative())
        return node

    def multiplicative(self):
        node = self.unary()
        while (tok := self.peek()) and tok.type in (T.MUL, T.DIV, T.FDIV, T.MOD):
            op = self.eat(tok.type).type
            node = BinOp(node, op, self.unary())
        return node

    def unary(self):
        tok = self.peek()
        if tok and tok.type in (T.ADD, T.SUB, T.BIT_NOT):
            op = self.eat(tok.type).type
            return UnaryOp(op, self.unary())
        return self.power()

    def power(self):
        node = self.factor()
        while (tok := self.peek()) and tok.type == T.POW:
            op = self.eat(T.POW).type
            node = BinOp(node, op, self.factor())
        return node

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
