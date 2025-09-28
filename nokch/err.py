import sys

from .tokens import E


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

    def do(self, message: str, type_: E, token_or_pos, span: int = 1):
        line, col = self._get_pos(token_or_pos)
        self._print_error(line, col, message, error_type=type_, span=span)
        sys.exit(1)

    def _get_pos(self, token_or_pos):
        if hasattr(token_or_pos, "pos"):
            return token_or_pos.pos
        return token_or_pos

    def _print_error(
        self, line: int, col: int, message: str, error_type: E, span: int = 1
    ):
        # headline
        print(
            f"{self.BOLD}{self.RED}[{error_type.value}]:{self.RESET} "
            f"{self.CYAN}{self.filename}{self.RESET}:"
            f"{self.YELLOW}{line}{self.RESET}:{self.YELLOW}{col}{self.RESET}: "
            f"{self.GREEN}{message}{self.RESET}"
        )

        # code preview with line numbers
        if 1 <= line <= len(self.source):
            src_line = self.source[line - 1].rstrip("\n")
            lineno_str = f"{line}"
            pad = len(lineno_str)

            # show source line
            print(f" {self.CYAN}{lineno_str}{self.RESET} | {src_line}")

            # underline the error span
            underline = " " * (col - 1) + f"{self.RED}^" + "~" * (span - 1) + self.RESET
            print(" " * (pad + 1) + " | " + underline)
