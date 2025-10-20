"""
Contains a loader to load a config from a JSON file
"""

import json
from attr import define

from secretary_of_state.loaders.base_loader import BaseLoader
from secretary_of_state.machine_description import MachineDescription


@define
class JsonLoader(BaseLoader):
    """
    Loads a config from a JSON file
    """

    def load(self) -> MachineDescription:
        return self.load_if_present(json.load)
