from importlib.metadata import PackageNotFoundError, version


def get_v():
    try:
        return version("nokch")
    except PackageNotFoundError:
        return "unknown"


__version__ = get_v()
