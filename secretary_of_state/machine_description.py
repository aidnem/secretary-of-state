"""
Contains types to represent state machine transitions and descriptions
"""

from typing import NotRequired, TypedDict


class Transition(TypedDict):
    """
    Describes a state machine transition, which has a trigger, destination, and optionally a
    condition
    """

    trigger: str
    destination: str
    condition: NotRequired[str]


MachineDescription = dict[str, list[Transition]]
"""Describes a state machine by mapping each state to a list of Transitions"""
