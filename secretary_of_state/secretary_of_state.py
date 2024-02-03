from dataclasses import dataclass
import sys
import csv

def usage():
    print("secretary-of-state:")
    print("\tconverts csv state machines to mermaid diagrams")
    print("usage:")
    print("\tsecretary [file]")
    print("")
    print("\t[file]: path to a csv file")

iota: int = -1
node_map: dict[str, str] = {}

def new_node_id() -> str:
    global iota

    iota += 1

    # if f"node{iota}" == 'node6':
    #     raise Exception("OOPSIE POOPSIE!")
    return f"node{iota}"

def get_node_id(name: str = "") -> str:
    """Get a unique node id"""
    global node_map

    if len(name):
        if name not in node_map:
            node_map[name] = new_node_id()
        return node_map[name]

    return new_node_id()

def render_or(current_state: str, prev_node: str, next_state: str, condition: str, first: bool) -> str:
    raise NotImplementedError("render_or() not implemeneted yet :(")
    conditions: list[str] = [c.strip() for c in condition.split('||')]

    for condition in conditions:
        condition_node = get_node_id()
        print(condition_node + "{" + condition + "}")

        if first:
            print(f"{prev_node} --> {condition_node}")
            prev_node = condition_node
            first = False

            continue

        print(f"{prev_node} -.->|false| {condition_node}")
        print(f"{prev_node} -.->|true| {next_state} ")
        prev_node = condition_node

    print(f"{prev_node} -.->|true| {next_state}")

    return prev_node

def render_and(current_state: str, prev_node: str, next_state: str, condition: str, first: bool) -> str:
    raise NotImplementedError("render_and() not implemeneted yet :(")
    conditions: list[str] = [c.strip() for c in condition.split('&&')]

    original_node = prev_node

    for condition in conditions:
        condition_node = get_node_id()
        print(condition_node + "{" + condition + "}")

        if first:
            print(f"{prev_node} --> {condition_node}")
            prev_node = condition_node
            first = False

            continue

        print(f"{prev_node} -.->|true| {condition_node}")
        print(f"{prev_node} -.->|false| {current_state} ")
        prev_node = condition_node

    print(f"{prev_node} -.->|true| {next_state}")

    return prev_node

def render_single(condition: str, in_node: str, out_true: str, out_false):
    print(in_node + '{"' + condition + '"}')

    print(f"{in_node} -.->|true| {out_true}")
    print(f"{in_node} -.->|false| {out_false}")

NON_TRANSITIONS = ["default","Not allowed","TBD"]

def render_table(rows: list[list[str]]):
    states_row = rows[0][1:] # Chop off first, empty square
    transition_rows = rows[1:]

    print("```mermaid")
    print("flowchart TB\n")
    print("classDef state font-size:40px,padding:10px\n")

    for row in transition_rows:
        current_state = row[0]
        current_state_node = get_node_id(current_state)
        num_transitions: int = 0
        for condition in row[1:]:
            if condition not in NON_TRANSITIONS:
                num_transitions += 1

        current_transition = 0

        print(current_state_node + ":::state")
        print(current_state_node + "([" +  current_state + "])")

        if num_transitions > 0:
            in_node = get_node_id()
            print(f"{current_state_node} --> {in_node}")
            for i, condition in enumerate(row[1:]):
                if condition in NON_TRANSITIONS:
                    continue
                current_transition += 1
                next_state = states_row[i]
                next_state_node = get_node_id(next_state)

                if current_transition == num_transitions:
                    # Last transition, return to current state if false
                    out_node: str = current_state_node
                else:
                    # otherwise, create a new node for a new transition
                    out_node: str = get_node_id()

                # if '||' in condition:
                #     prev_node = render_or(current_state, prev_node, next_state_node, condition, first)
                # elif '&&' in condition:
                #     prev_node = render_and(current_state, prev_node, next_state_node, condition, first)
                # else:
                #     prev_node = render_single(current_state, prev_node, next_state_node, condition, first)
                prev_node = render_single(condition, in_node, next_state_node, out_node)

                in_node = out_node

    print("```")

def main():
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    fp = sys.argv[1]

    rows: list[list[str]] = []
    try:
        with open(fp, newline='') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in csvreader:
                rows.append(row)
    except FileNotFoundError:
        print(f"[ERROR] File {fp} not found! Does the file exist?", file=sys.stderr)
        sys.exit(1)

    if len(rows) < 2:
        print(f"[ERROR] File must have at least 2 rows, found {rows}", file=sys.stderr)

    render_table(rows)