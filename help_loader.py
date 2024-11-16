from dataclasses import dataclass
from typing import Dict, Optional
import json

@dataclass
class General:
    """Stores detailed help information for each command."""
    create: str
    delete: str
    rename: str
    modify: str
    list: str

    def help_command(self, command: str) -> str:
        """Retrieve detailed help for a specific command."""
        return getattr(self, command, "Error: Command not found.")

@dataclass
class Info:
    """Stores brief descriptions for each command."""
    create: str
    delete: str
    rename: str
    modify: str
    list: str

    def __str__(self) -> str:
        """Return all command descriptions as a formatted string."""
        return "\n".join([self.create, self.delete, self.rename, self.modify, self.list])

@dataclass
class Help:
    """Encapsulates both general and info help categories."""
    general: General
    info: Info

    def __post_init__(self):
        self.general = General(**self.general)
        self.info = Info(**self.info)

class LoadHelp:
    """Loads help details from a JSON file and provides access to help information."""
    def __init__(self, filepath: str = "./help.json") -> None:
        self._filepath = filepath
        self._help_data: Optional[Help] = None

    def load_help_data(self) -> Dict:
        with open(self._filepath, "r") as f:
            return json.load(f)

    def get_help(self) -> Help:
        if not self._help_data:
            try:
                data = self.load_help_data()
                self._help_data = Help(**data)
            except ValueError as e:
                print(f"\033[91mError loading help data: {e}\033[0m")
                raise
        return self._help_data

    def display_help(self, command: Optional[str] = None, category: str = "general"):
        """Display help for a specific command or all command summaries."""
        help_data = self.get_help()

        if command:
            # Display specific help for the command in the specified category
            if category == "general":
                print(help_data.general.help_command(command))
            elif category == "info":
                print(getattr(help_data.info, command, "Error: Command not found."))
            else:
                print("Error: Invalid category specified.")
        else:
            # Display all command summaries from the "info" category
            print(help_data.info)

# Usage example
loader = LoadHelp(filepath="help.json")
loader.display_help(command="create", category="general")  # For detailed help on 'create'
loader.display_help()  # To display summaries of all commands
