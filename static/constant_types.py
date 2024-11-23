from enum import StrEnum
from typing import Dict, List


class FileOperation(StrEnum):
    """
    A string enum class used to store all th operations/ commands available to
    use in file operations
    """

    CREATE = "create"
    DELETE = "delete"
    RENAME = "rename"


class DirectoryOperations(StrEnum):
    """A class that contains the various directory operations that the program supports."""

    CHANGE = "cd"
    LIST = "ls"
    MAKE = "mkdir"
    REMOVE = "rmdir"
    CURRENT = "pwd"
    MOVE = "mv"


class Platform(StrEnum):
    """
    A string enum class that stores the various platforms/ Operating Systems
    that the program supports.
    """

    WINDOWS = "win"
    LINUX = "linux"
    MAC = "darwin"


# A dictionary to store different ASCII color codes for console output formatting.
ConsoleColors = {
    "RESET": "\033[0m",  # Resets color to default
    "RED": "\033[1;31m",  # Red color for text
    "BLUE": "\033[1;34m",  # Blue color for text
    "MAGENTA": "\033[1;35m",  # Magenta color for text
    "CYAN": "\033[1;36m",  # Cyan color for text
}


# A list that contains the valid file extensions that the program supports.
VALID_EXTENSIONS = [
    ".txt",
    ".pdf",
    ".docx",
    ".dat",
    ".csv",
    ".json",
    ".xml",
    ".html",
    ".css",
    ".js",
    ".py",
    ".java",
    ".cpp",
    ".c",
    ".h",
    ".hpp",
    ".php",
    ".sql",
    ".sh",
    ".bat",
]

# A list of valid pipe symbols that may be used in command-line operations.
PIPES: list[str] = ["<", ">", "|"]
