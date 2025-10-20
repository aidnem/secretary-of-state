"""
A script to convert a description of a state machine into a mermaid flow diagram to display states
and transitions in a human-readable format.
"""

import sys

import jsonschema

from secretary_of_state import schema
from secretary_of_state.loaders.loader_factory import create_loader
from secretary_of_state.machine_description import MachineDescription, Transition
import secretary_of_state.unique_condition as uc
from secretary_of_state.loaders.base_loader import BaseLoader


def usage():
    print("secretary-of-state:", file=sys.stderr)
    print("\tconverts csv state machines to mermaid diagrams", file=sys.stderr)
    print("usage:", file=sys.stderr)
    print("\tsecretary [file]", file=sys.stderr)
    print("", file=sys.stderr)
    print("\t[file]: path to a toml file", file=sys.stderr)


def separate_chains(
    transitions: list[Transition],
) -> tuple[dict[str, list[Transition]], list[Transition]]:
    """
    Separate a list of transitions into "chains" (a mapping of each trigger to a list of what
    transitions it can cause and in which order they are checked) and non-chains (triggers with
    only one transition)
    """
    chains: dict[str, list[Transition]] = {}
    non_chains: list[Transition] = []

    # First, move through the entire list of transitions and track which have been seen
    for transition in transitions:
        if (trigger := transition["trigger"]) in chains:
            chains[trigger].append(transition)
        else:
            chains[trigger] = [transition]

    to_delete: set[str] = set()
    # Next, move all triggers that have only one transition to non_chains
    for trigger, transitions in chains.items():
        if len(transitions) == 1:
            to_delete.add(trigger)
            non_chains.append(transitions[0])

    for trigger in to_delete:
        del chains[trigger]

    return chains, non_chains


def render_chain(
    context: uc.ConditionContext,
    trigger: str,
    transitions: list[Transition],
):
    """
    Render a chain of conditional transitions starting from a state
    """
    assert (
        len(transitions) >= 2
    ), 'Less than 2 transition "chain" made it to render_chain,'

    assert (
        "condition" in transitions[0]
    ), "First transition in chain must have a condition"

    last_node: str = context.node(transitions[0]["condition"])
    print(f"    {context.get_state()} -->|{trigger}| {last_node}")
    print(f"    {last_node} -.->|true| {transitions[0]['destination']}")

    for transition in transitions[1:-1]:
        assert (
            "condition" in transition
        ), "Non-last transition in chain must have a condition"
        next_node: str = context.node(transition["condition"])

        print(f"    {last_node} -.->|false| {next_node}")
        print(f"    {next_node} -.->|true| {transition['destination']}")

        last_node = next_node

    transition = transitions[-1]
    final_node: str
    if "condition" in transition:
        final_node = context.node(transition["condition"])
        print(f"    {final_node} -.->|true| {transition['destination']}")
    else:
        final_node = transition["destination"]

    print(f"    {last_node} -.->|false| {final_node}")


def render_non_chain(context: uc.ConditionContext, transition: Transition):
    """
    Render a non-chain (single transition) to stdout
    """

    if "condition" in transition:
        cond_node = context.node(transition["condition"])
        print(f"    {context.get_state()} -->|{transition['trigger']}| {cond_node}")

        print(f"    {cond_node} -.->|true| {transition['destination']}")
    else:
        print(
            f"    {context.get_state()} -->|{transition['trigger']}| {transition['destination']}"
        )


def render_state(state: str, transitions: list[Transition]):
    """
    Render a node for the state as well as the edges coming out of said state
    """
    # First, break up transitions into "chains" (sets of transitions that share one trigger but have different conditions) and non-chains
    chains, non_chains = separate_chains(transitions)

    context: uc.ConditionContext = uc.ConditionContext(state)

    for trigger, chain in chains.items():
        render_chain(context, trigger, chain)

    for transition in non_chains:
        render_non_chain(context, transition)


def render_machine(state_machine: MachineDescription):
    """
    Render all states in a state machine to a markdown diagram printed to stdout
    """
    print("```mermaid")
    print("flowchart LR\n")
    print("classDef state font-size:40px,padding:10px\n")
    for state in state_machine:
        render_state(state, state_machine[state])
    print("```")


def main():
    """
    Main entry point for the script. Takes a filename as the only argument and prints the markdown
    to stdout.
    """

    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    fp = sys.argv[1]

    loader: BaseLoader = create_loader(fp)

    machine_description: MachineDescription = loader.load()

    jsonschema.validate(instance=machine_description, schema=schema.SCHEMA)

    render_machine(machine_description)
