# JsonSchema definition for machine description validation


from typing import Any


SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "title": "MachineDescription",
    "description": "Describes a state machine by mapping each state to a list of Transitions",
    "patternProperties": {
        "[a-zA-Z_][a-zA-Z0-9_]*": {
            "description": "Mapping of each state to an array of its transitions",
            "type": "array",
            "items": {
                "description": "Description of a transition, with a trigger, destination state, and an optional condition",
                "type": "object",
                "properties": {
                    "trigger": {
                        "description": "Name of the trigger for this transition",
                        "type": "string",
                    },
                    "destination": {
                        "description": "Name of the state that this transition will transition to if succesful",
                        "type": "string",
                    },
                    "condition": {
                        "description": "(optional) The condition that will allow this transition to succeed",
                        "type": "string",
                    },
                },
                "required": ["trigger", "destination"],
                "additionalProperties": False,
            },
        }
    },
    "additionalProperties": False,
}
