"""
Module to generate loaders based on file type
"""

from os import path
from secretary_of_state.loaders.base_loader import BaseLoader
from secretary_of_state.loaders.toml_loader import TomlLoader


def create_loader(fp: str) -> BaseLoader:
    """
    Return the correct machine loader based on the extension of `fp`
    """

    _, ext = path.splitext(fp)
    match ext:
        case ".toml":
            return TomlLoader(fp)
        case _:
            raise NotImplementedError(f"{ext} extension not implemented")
