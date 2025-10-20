"""
Utility to generate unique node IDs for conditions
"""

from attrs import define, field


iota: int = -1


@define
class ConditionContext:
    """
    A context representing the 'context'/'scope' of one state within which conditions can be generated
    """

    _iota: int = field(default=-1, init=False)
    _state: str

    def node(self, condition: str) -> str:
        """
        Generate a unique node given the condition
        """
        self._iota += 1
        return f"{self._state}Condition{self._iota}" + '{"' + condition + '"}'

    def get_state(self) -> str:
        """
        Get the state this context is configured for
        """

        return self._state
