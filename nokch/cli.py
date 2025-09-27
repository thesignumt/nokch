import argparse
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from nokch.interpreter import Interpreter


def get_ver():
    try:
        return version("nokch")
    except PackageNotFoundError:
        return "unknown"


def valid_file(path_str: str) -> Path:
    p = Path(path_str)
    if not p.exists():
        raise argparse.ArgumentTypeError(f"{p} does not exist")
    if not p.is_file():
        raise argparse.ArgumentTypeError(f"{p} is not a file")
    if p.suffix != ".nkch":
        raise argparse.ArgumentTypeError(f"{p} must have .nkch extension")
    return p


def main():
    parser = argparse.ArgumentParser(description=f"nokch {get_ver()}")
    parser.add_argument("path", type=valid_file, help="path to .nkch file to interpret")
    args = parser.parse_args()

    Interpreter(args.path)()


if __name__ == "__main__":
    main()
