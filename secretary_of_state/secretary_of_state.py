from dataclasses import dataclass
import sys
import csv
import tomllib
from typing import Annotated, NotRequired, TypedDict

import jsonschema

from secretary_of_state import schema


class Transition(TypedDict):
    """
    Describes a state machine transition, which has a trigger, destination, and optionally a condition
    """

    trigger: str
    destination: str
    condition: NotRequired[str]


MachineDescription = dict[str, list[Transition]]
"""Describes a state machine by mapping each state to a list of Transitions"""


def usage():
    print("secretary-of-state:")
    print("\tconverts csv state machines to mermaid diagrams")
    print("usage:")
    print("\tsecretary [file]")
    print("")
    print("\t[file]: path to a toml file")


def render_machine(state_machine: dict):
    print("```mermaid")
    print("flowchart LR\n")
    print("classDef state font-size:40px,padding:10px\n")
    print("```")


def main():
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    fp = sys.argv[1]

    machine_description: MachineDescription = {}
    try:
        with open(fp, "rb") as tomlfile:
            machine_description = tomllib.load(tomlfile)
    except FileNotFoundError:
        print(f"[ERROR] File {fp} not found! Does the file exist?", file=sys.stderr)
        sys.exit(1)

    jsonschema.validate(instance=machine_description, schema=schema.SCHEMA)

    print(machine_description)
    print(
        "[ERROR] Actual generation of graphs is not yet supported. Please come back later :)"
    )
    sys.exit(1)
