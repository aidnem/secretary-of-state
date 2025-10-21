"""
Base file loader interface
"""

from abc import abstractmethod
import sys
from typing import BinaryIO, Callable, TypeVar

from attr import define

from secretary_of_state.machine_description import MachineDescription


T = TypeVar("T")


@define
class BaseLoader:
    """
    An abstract base class for file loaders
    """

    fp: str

    @abstractmethod
    def load(self) -> MachineDescription:
        """
        Load a state machine description from a file
        """

    def load_if_present(self, loader: Callable[[BinaryIO], T]) -> T:
        """
        If self.fp is a file that exists, open it and call `loader` on it.
        Otherwise, print an error message and exit.
        """

        try:
            with open(self.fp, "rb") as f:
                return loader(f)
        except FileNotFoundError:
            print(
                f"[ERROR] File {self.fp} not found! Does the file exist?",
                file=sys.stderr,
            )
            sys.exit(1)
