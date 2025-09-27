from typing import Any


class Interpreter:
    def __init__(self) -> None:
        print("interpreter.init")

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        print("interpreter.call")
