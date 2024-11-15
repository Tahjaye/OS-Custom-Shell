"""
    This module defines custom exceptions for
    command validation, file operations, and common use cases.
    thrown when a user input a command that is not supported by
    the program.
"""
class InvalidCommand(SyntaxError):
    """
    Exception raised when an invalid command is encountered.
    """
    def __init__(self, message: str) -> None:
        super().__init__(message)

 
class FileOperationError(IOError):
    """
        Custom Exception that is raised for
        an invalid file operation.
    """
    def __init__(self, message: str) -> None:
        super().__init__(message)


class CommonException(Exception):
    """
        A general-purpose custom
        exception for common error scenarios.
    """
    def __init__(self, message: str) -> None:
        super().__init__(message)
