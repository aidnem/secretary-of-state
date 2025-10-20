"""
Base file loader interface
"""

from abc import abstractmethod

from attr import define

from secretary_of_state.machine_description import MachineDescription


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
