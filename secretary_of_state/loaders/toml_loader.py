import sys
import tomllib
from attr import define

from secretary_of_state.loaders.base_loader import BaseLoader
from secretary_of_state.machine_description import MachineDescription


@define
class TomlLoader(BaseLoader):
    def load(self) -> MachineDescription:
        try:
            with open(self.fp, "rb") as f:
                return tomllib.load(f)
        except FileNotFoundError:
            print(
                f"[ERROR] File {self.fp} not found! Does the file exist?",
                file=sys.stderr,
            )
            sys.exit(1)
