from dataclasses import dataclass
from typing import Dict
import json


@dataclass
class General:
    """
    This class is used to store the general - specific help
    for the help command, for each operation it stores details
    to which can be retrieved one by one, using the
    help_command function.
    """

    create: str
    delete: str
    rename: str
    modify: str
    list: str
    change: str
    make: str
    remove: str
    pwd: str

    def help_command(self, command: str) -> str:
        """
        This function is used to check if the command for which
        the help/details, is requested for by the user is a defined
        variable/attribute of the class if it is then it returns it
        if it is not it returns and empty string

        :param command: specific command for which the help operation is requesting.
        :return: the details of a specific command
        """
        return getattr(self, command, "")


@dataclass
class Info:
    """
    A data class to store and display details about supported commands.

    Attributes:
        Each attribute corresponds to a supported command and contains a brief
        description or usage information about that command.

    Methods:
        __str__():
            Returns a formatted string listing all supported commands and their details.
    """

    create: str
    delete: str
    rename: str
    modify: str
    list: str
    change: str
    make: str
    remove: str
    pwd: str

    def __str__(self) -> str:
        """
        Returns:
            str: A formatted string displaying all command details.
        """
        return "\n".join(f"{key}: {value}" for key, value in vars(self).items())


@dataclass
class Help:
    """
    This class is used to store all the types of help
    operations that is supported
    1. The general/specific help, ex: 'help delete'
    2. The information help which prints out all the
    supported command and a small detail of each

    This class used the dunder '__post_init__' method
    provided by data class to
    initialize the variables of the class shortly
    after the constructor for 'Help' class
    is called. This is done as the help class doesn't
    directly call the constructor
    of the composed classes.
    """

    general: General
    info: Info

    # noinspection PyArgumentList
    def __post_init__(self):
        # noinspection PyArgumentList
        self.general = General(**self.general)
        self.info = Info(**self.info)


class LoadHelp:
    """
    This class is used to load the details from the json file which contain all the
    details of the supported operation,
    and when the 'get_help' function is called it calls the 'load_help_data' function
    which gets the details from the json file then
    it serializes that information into the 'Help' class and returns it
    unless and error occurs then the raises a 'ValueError' in which is graciously
    caught then a formatted output is printed to the console in #FF0000|RED.
    """

    def __init__(self, filepath: str = "./help.json") -> None:
        self._filepath = filepath
        self._help_data: Help | None = None

    def load_help_data(self) -> Dict:
        with open(self._filepath, "r") as f:
            return json.load(f)

    def get_help(self) -> Help | None:
        help_data = {}
        if not self._help_data:
            try:
                data = self.load_help_data()
                help_data = Help(**data)
            except ValueError as e:
                print(f"\033[91mError loading help data: {e}\033[0m")
                return None
        return help_data

    def get_help_info(self, command=None):
        help_data = self.get_help()
        if command:
            return help_data.general.help_command(command)
        return help_data.info
