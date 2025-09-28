import sys

from .tokens import E, Token


class ErrorReporter:
    """Error reporter with filename and GCC-like code preview."""

    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

    def __init__(self, filename: str = "<stdin>", source: list[str] | None = None):
        self.filename = filename
        self.source = source or []

    def set_source(self, filename: str, source: list[str]):
        self.filename = filename
        self.source = source

    def __call__(
        self,
        message: str,
        type_: E,
        token_or_line,
        span: int = 1,
    ):
        line = self._get_pos(token_or_line)
        self._print_error(line, message, error_type=type_, span=span)
        sys.exit(1)

    def _get_pos(self, token_or_line):
        if hasattr(token_or_line, "line") and hasattr(token_or_line, "col"):
            return token_or_line.line, token_or_line.col
        if hasattr(token_or_line, "line"):
            return token_or_line.line, 0
        if isinstance(token_or_line, tuple):
            return token_or_line
        return token_or_line, 0

    def _print_error(self, pos, message: str, error_type: E, span: int = 1):
        line, col = pos
        print(
            f"{self.BOLD}{self.RED}[{error_type.value}]:{self.RESET} "
            f"{self.CYAN}{self.filename}{self.RESET}:"
            f"{self.YELLOW}{line}{self.RESET}:{self.YELLOW}{col}{self.RESET}: "
            f"{self.GREEN}{message}{self.RESET}"
        )

        if 1 <= line <= len(self.source):
            src_line = self.source[line - 1].rstrip("\n")
            lineno_str = f"{line}"
            pad = len(lineno_str)

            print(f" {self.CYAN}{lineno_str}{self.RESET} | {src_line}")

            underline = " " * (col - 1) + f"{self.RED}^" + "~" * (span - 1) + self.RESET
            print(" " * (pad + 1) + " | " + underline)
