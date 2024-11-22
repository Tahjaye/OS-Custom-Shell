import os
import stat

import static.constant_types as ct
from sys import platform

def get_platform() -> ct.Platform:
    """
    Gets the Operating System that the program is running on and check's
    then checks if O.S is Windows, Linux of Mac else raise OSError
    """

    if platform.startswith("win"):
        return ct.Platform.WINDOWS
    if platform.startswith("linux"):
        return ct.Platform.LINUX
    if platform.startswith("darwin"):
        return ct.Platform.MAC

    raise OSError("Unsupported operating system")


def get_working_directory() -> str:
    """
    Gets the current working directory of the program
    """

    return os.getcwd()
import Shell as sh
def clear_screen():
    """
    The function `clear_screen()`\n
    clears the terminal screen based on the platform being used.
    """

    os.system("cls" if os.name == "nt" else "clear")

def cat_file(file_path):
    """
    Mimics the `cat` command: reads and displays the content.

    Args:
        file_path (str): Path to the file to display.
    """
    try:
        # Open the file and read its content
        with open(file_path, 'r') as file:
            for line in file:
                print(line, end='')  # Avoid double newlines
    except FileNotFoundError:
        print(f"cat: {file_path}: No such file or directory")
    except PermissionError:
        print(f"cat: {file_path}: Permission denied")
    except Exception as e:
        print(f"cat: Error reading file {file_path}: {e}")


def create_file(file_name):
    with open(file_name, 'w') as f:
        pass
    print(f"File '{file_name}' created.")

def delete_file(file_name):
    try:
        os.remove(file_name)
        print(f"File '{file_name}' deleted.")
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")

def rename_file(old_name, new_name):
    try:
        os.rename(old_name, new_name)
        print(f"File '{old_name}' renamed to '{new_name}'.")
    except FileNotFoundError:
        print(f"File '{old_name}' not found.")

def make_directory(dir_name):
    try:
        os.makedirs(dir_name)
        print(f"Directory '{dir_name}' created.")
    except FileExistsError:
        print(f"Directory '{dir_name}' already exists.")

def remove_directory(dir_name):
    try:
        os.rmdir(dir_name)
        print(f"Directory '{dir_name}' deleted.")
    except FileNotFoundError:
        print(f"Directory '{dir_name}' not found.")
    except OSError:
        print(f"Directory '{dir_name}' is not empty.")

def change_directory(dir_name):
    try:
        os.chdir(dir_name)
        print(f"Changed to directory '{dir_name}'.")
    except FileNotFoundError:
        print(f"Directory '{dir_name}' not found.")


def list_permissions():
    for item in os.listdir('.'):
        stats = os.stat(item)
        permissions = stat.filemode(stats.st_mode)
        file_size = stats.st_size
        print(f"{permissions} {file_size} {item}")

def set_env_var(var_name, value):
    os.environ[var_name] = value
    print(f"Environment variable '{var_name}' set to '{value}'.")

def get_env_var(var_name):
    value = os.environ.get(var_name)
    if value:
        print(f"{var_name}={value}")
    else:
        print(f"Environment variable '{var_name}' not set.")

def current_working_directory():
    print(f"Current working directory: {os.getcwd()}")

def echo(*args):
    if len(args) == 0 :
        print("Echo is "+ "on" if sh.ECHO else "off")
    elif len(args) == 1:
        if args[0] == "on":
            sh.ECHO = True
            print("Echo is on")
        elif args[0] == "off":
            sh.ECHO = False
            print("Echo is off")
        else:
            print(args[0])
    elif len(args) ==2:
        print("Invalid number of arguments")
    elif len(args) == 3 and args[1] == ">":
        if args[2][-3:].lower() in ct.VALID_EXTENSIONS:
            try:
                with open(args[2], 'w') as f:
                    f.write(args[0])
            except FileNotFoundError:
                print(f"File '{args[2]}' not found.")
        else:
            print("Invalid file extension.")
    else:
        print("Invalid arguments.")
        

def list_sub_directories():
    for item in os.listdir('.'):
        if os.path.isdir(item):
            print(item)

def change_file_permissions(file_path, read_only=False, executable=False):
    """
    Change basic permissions of a file in an OS-redundant way.

    Args:
        file_path (str): Path to the file.
        read_only (bool): If True, makes the file read-only. If False, makes it writable.
        executable (bool): If True, adds execute permissions. If False, removes execute permissions.
    """
    try:
        # Get current permissions
        current_permissions = os.stat(file_path).st_mode

        if read_only:
            # Make the file read-only
            new_permissions = current_permissions & ~stat.S_IWRITE
        else:
            # Make the file writable
            new_permissions = current_permissions | stat.S_IWRITE

        if executable:
            # Add execute permissions for all users
            new_permissions |= stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
        else:
            # Remove execute permissions for all users
            new_permissions &= ~(stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

        # Apply the new permissions
        os.chmod(file_path, new_permissions)

        # Print a success message
        print(f"Permissions for '{file_path}' updated successfully.")
        print(f"Read-only: {'Enabled' if read_only else 'Disabled'}, Executable: {'Enabled' if executable else 'Disabled'}")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except PermissionError:
        print(f"Error: Permission denied when modifying '{file_path}'.")
    except Exception as e:
        print(f"Unexpected error: {e}")





#These functions were carried over and may need to be implemented if not else where

def handle_help():
    """
        This function is used to handle the help command
        when the user request any help information
        whether it is general help
        or specific help
        for a command.
        :param parsed_input: List of parsed words from user input.
    """

def handle_file_operation(parsed_input: list[str]):
    """
        This function handles the file operation/s that the user is requesting to do
        whether [create, delete, rename].
        :param operating_system: The operating system that the user ran the program on.
        :param parsed_input: List of parsed words from user input.
    """
    
