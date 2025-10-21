"""
Contains a loader to load MachineDescriptions from toml files
"""

import tomllib
from attr import define

from secretary_of_state.loaders.base_loader import BaseLoader
from secretary_of_state.machine_description import MachineDescription


@define
class TomlLoader(BaseLoader):
    """
    Loads a config from a TOML file
    """

    def load(self) -> MachineDescription:
        return self.load_if_present(tomllib.load)
