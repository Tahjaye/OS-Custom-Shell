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
    """ A class that contains the various directory operations that the program supports."""

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



#A dictionary that maps each file operation to its corresponding commands
# for different platforms. Each key represents a FileOperation, and its value
# is a nested dictionary where keys are Platforms and values are lists of
# command-line arguments.
FILE_OPERATIONS: Dict[FileOperation, Dict[Platform, List[str]]] = {
    FileOperation.CREATE: {
        Platform.WINDOWS: ["cmd", "/c", "type", "nul", ">"],  # Command for creating a file on Windows
        Platform.LINUX: ["touch"],  # Command for creating a file on Linux
        Platform.MAC: ["touch"],  # Command for creating a file on macOS
    },
    FileOperation.DELETE: {
        Platform.WINDOWS: ["cmd", "/c", "del"],  # Command for deleting a file on Windows
        Platform.LINUX: ["rm"],  # Command for deleting a file on Linux
        Platform.MAC: ["rm"],  # Command for deleting a file on macOS
    },
    FileOperation.RENAME: {
        Platform.WINDOWS: ["cmd", "/c", "ren"],  # Command for renaming a file on Windows
        Platform.LINUX: ["mv"],  # Command for renaming a file on Linux
        Platform.MAC: ["mv"],  # Command for renaming a file on macOS
    },
}

DIRECTORY_OPERATIONS: Dict[DirectoryOperations, Dict[Platform, List[str]]] = {
    DirectoryOperations.CHANGE: {
        Platform.WINDOWS: ["cd"],  # Command for changing directory on Windows
        Platform.LINUX: ["cd"],  # Command for changing directory on Linux
        Platform.MAC: ["cd"],  # Command for changing directory on macOS
    },
    DirectoryOperations.LIST: {
        Platform.WINDOWS: ["dir"],  # Command for listing directory contents on Windows
        Platform.LINUX: ["ls"],  # Command for listing directory contents on Linux
        Platform.MAC: ["ls"],  # Command for listing directory contents on macOS
    },
    DirectoryOperations.MAKE: {
        Platform.WINDOWS: ["cmd", "/c", "mkdir"],  # Command for creating a directory on Windows
        Platform.LINUX: ["mkdir"],  # Command for creating a directory on Linux
        Platform.MAC: ["mkdir"],  # Command for creating a directory on macOS
    },
    DirectoryOperations.REMOVE: {
        Platform.WINDOWS: ["cmd", "/c", "rmdir", "/s", "/q"],  # Command for removing a directory on Windows
        Platform.LINUX: ["rmdir"],  # Command for removing a directory on Linux
        Platform.MAC: ["rmdir"],  # Command for removing a directory on macOS
    },
    DirectoryOperations.CURRENT: {
        Platform.WINDOWS: ["cd"],  # Command for getting the current directory on Windows
        Platform.LINUX: ["pwd"],  # Command for getting the current directory on Linux
        Platform.MAC: ["pwd"],  # Command for getting the current directory on macOS
    },
    DirectoryOperations.MOVE: {
        Platform.WINDOWS: ["cmd", "/c", "move"],  # Command for moving a directory on Windows
        Platform.LINUX: ["mv"],  # Command for moving a directory on Linux
        Platform.MAC: ["mv"],  # Command for moving a directory on macOS
    },
}


# A dictionary to store different ASCII color codes for console output formatting.
ConsoleColors = {
    "RESET": "\033[0m",  # Resets color to default
    "RED": "\033[1;31m",  # Red color for text
    "BLUE": "\033[1;34m",  # Blue color for text
    "MAGENTA": "\033[1;35m",  # Magenta color for text
    "CYAN": "\033[1;36m",  # Cyan color for text
}


# A list that contains the valid file extensions that the program supports.
VALID_EXTENSIONS = [".txt", ".pdf", ".docx",".dat",".csv",".json",".xml",".html",".css",".js",".py",".java",".cpp",".c",".h",".hpp",".php",".sql",".sh",".bat"]

# A list of valid pipe symbols that may be used in command-line operations.
PIPES: list[str] = ["<", ">", "|"]
