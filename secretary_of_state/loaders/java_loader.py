import sys
import tomllib
from attr import define

import re
import regex

from secretary_of_state.loaders.base_loader import BaseLoader
from secretary_of_state.machine_description import MachineDescription


@define
class JavaLoader(BaseLoader):
    def load(self) -> MachineDescription:
        # Load the file into a string
        file_contents = self.load_if_present(lambda f: str(f.read(), encoding="utf-8"))

        # Find a state machine configuration
        config_match = re.search(
            r"(\S+).*=.*new StateMachineConfiguration[\s\S]+new StateMachine",
            file_contents,
        )

        if config_match is None:
            print(
                f"[ERROR] JavaLoader: No state machine configuration was found in {self.fp}"
            )
            sys.exit(1)

        config_str = config_match.group(0)
        config_name = config_match.group(1)

        # Trim comments from the config
        config_str = re.sub(r"\/\/.*$\n", "", config_str, flags=re.MULTILINE)

        # Trim the `new StateMachineConfiguration` line
        config_str = re.sub(r"\S+.*=.*new StateMachineConfiguration.*;", "", config_str)

        # Trim the `new StateMachine` line
        config_str = re.sub(r"^.*new StateMachine$", "", config_str, flags=re.MULTILINE)

        # Remove all carriage returns
        # config_str = config_str.replace("\r", "")

        # Find the name of the state type and trigger type
        state_type_match = re.search(r"\.configure\((.*)\..*\)", config_str)

        if state_type_match is None:
            print(
                "[ERROR] JavaLoader: Couldn't determine State generic type. Try manually inputting toml instead."
            )
            sys.exit(1)

        state_type_prefix: str = state_type_match.group(1) + "."
        # Remove all occurrences of the state type
        config_str = config_str.replace(state_type_prefix, "")

        trigger_type_match = re.search(r"\.permit(?:If)?\((\w+)", config_str)

        if trigger_type_match is None:
            print(
                "[ERROR] JavaLoader: Couldn't determine Trigger generic type. Try manually inputting toml instead."
            )
            sys.exit(1)

        trigger_prefix_str = trigger_type_match.group(1) + "."

        config_str = config_str.replace(trigger_prefix_str, "")

        # Convert the "cleaned" java to TOML:

        # Replace '[ConfigurationName].configure([State]) with [State] = \['
        config_str = config_str.replace(config_name, "")
        config_str = re.sub(r"\.configure\((\S+)\)", r"\1 = [\n", config_str)

        # Convert all multi-line permit and permitIf statements to be single line
        config_str = re.sub(
            r"\.permit\((\w*?),\r?\n?\s*(\w*)\)", r".permit(\1, \2)", config_str
        )

        config_str = regex.sub(
            r"\.permitIf\(\r?\n?\s*(\S*),\r?\n?\s*(\S*)\,\r?\n?\s*((?:[^()]|(?:\((?3)\)))*)\r?\n?\)(;?)[\r\n]+",
            r".permitIf(\1, \2, <START_SECRETARY_CONDITION>\3<END_SECRETARY_CONDITION>)\4\n",
            config_str,
            flags=re.MULTILINE,
        )

        # Remove newlines from between the SECRETARY_CONDITION tags
        while (
            maybe_match := re.search(
                "<START_SECRETARY_CONDITION>.*?<END_SECRETARY_CONDITION>",
                config_str,
                flags=re.DOTALL,
            )
        ) is not None:
            new_text = maybe_match.group(0)
            new_text = new_text.replace("\r", "")
            new_text = new_text.replace("\n", "")
            new_text = re.sub(r"\s+", " ", new_text)
            new_text = new_text.replace("<START_SECRETARY_CONDITION>", "")
            new_text = new_text.replace("<END_SECRETARY_CONDITION>", "")
            config_str = config_str.replace(maybe_match.group(0), new_text)

        # Flatten all indenting
        config_str = re.sub(r"^\s*(\S)", r"\1", config_str, flags=re.MULTILINE)

        # Turn ; into a newline followed by the ending ] of the array
        config_str = config_str.replace(";", "\n]\n")

        # Turn permit statements into non-conditional transitions
        config_str = re.sub(
            r"\.permit\((\w*?),\s*(\w*)\)",
            r'    { trigger = "\1", destination = "\2" },',
            config_str,
        )

        # Turn permitIf statements into conditional transitions
        config_str = re.sub(
            r"\.permitIf\(\s*(\S*),\s*(\S*)\,\s*(.*)\r?\n?\)",
            r'    { trigger = "\1", condition = "\3", destination = "\2" },',
            config_str,
            flags=re.MULTILINE,
        )

        # Remove the leading `() ->` from conditional transitions
        config_str = config_str.replace('condition = "() -> ', 'condition = "')

        return tomllib.loads(config_str)
