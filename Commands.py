import os
import stat
import json
import subprocess
import static.constant_types as ct
from sys import platform
import shlex

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
        if is_valid_extension(args[2]):
            try:
                with open(args[2], 'w') as f:
                    f.write(args[0])
            except FileNotFoundError:
                print(f"File '{args[2]}' not found.")
        else:
            print(args[2][-3:].lower())
            print("Invalid file extension.")
    else:
        print("Invalid arguments.")
        

def list_sub_directories():
    # List the contents of the current directory
    for item in os.listdir('.'):
        if os.path.isdir(item):
            print(f"{item}/")  # Append '/' to directories to mimic `ls`
        else:
            print(item)  # Print files as they are

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


def print_help(args):
    # Load the help data from the JSON file
    with open('static/help.json', 'r') as json_file:
        help_data = json.load(json_file)
    
    # If the args list is empty, print the general help section
    if not args:
        print("General Help:\n")
        for command, description in help_data["general_help"].items():
            print(f"{command}: {description}")
    # If the args list contains one command, print specific help for that command
    elif len(args) == 1:
        command = args[0]
        if command in help_data["command_specific_help"]:
            print(f"Help for {command}:\n")
            command_help = help_data["command_specific_help"][command]
            print(f"Description: {command_help['description']}")
            print(f"Usage: {command_help['usage']}")
        else:
            print(f"No help available for command: {command}")
    else:
        print("Invalid arguments. Please provide either no arguments or one command.")



def is_valid_extension(filename,):
    # Extract the file extension (e.g., '.jpg', '.png')
    file_extension = os.path.splitext(filename)[1].lower()  # Normalize to lowercase for case-insensitivity
    
    # Check if the file extension is in the valid extensions list
    return file_extension in [ext.lower() for ext in ct.VALID_EXTENSIONS]

# Function to execute a single command
def execute_command(cmd):
    # Split the command into arguments (using shlex.split for proper parsing)
    cmd_parts = cmd.strip().split()
    
    # If running Windows commands, ensure we run via cmd.exe
    process = subprocess.Popen(cmd_parts, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()

    # Handle errors if any
    if error:
        print(f"Error in command '{cmd}': {error.decode()}")
        return None
    
    return output

# Function to simulate piping of multiple commands
def pipe(command_string):
    # Split the commands by the pipe symbol '|'
    commands = command_string.split('|')

    # Initialize a variable to hold the output of the previous command
    input_data = None

    # Loop through each command and execute them
    for i, cmd in enumerate(commands):
        # If this is not the first command, pass the previous output as input
        if input_data:
            process = subprocess.Popen(cmd.strip().split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            input_data, error = process.communicate(input=input_data)
        else:
            # For the first command, execute it without any input
            input_data = execute_command(cmd)

        # If the last command, print the output
        if i == len(commands) - 1:
            print(input_data.decode())

def handle_input_redirection(command_string):
    # Check if the '<' character is in the command (indicating input redirection)
    if '<' in command_string:
        # Split the command at '<' to separate the command and the filename
        parts = command_string.split('<')
        
        # Strip extra spaces from the command and filename
        cmd = parts[0].strip()
        filename = parts[1].strip()

        # Read the file contents
        try:
            with open(filename, 'r') as file:
                file_contents = file.read()
                
            # Return the command with the file contents inserted as input
            return cmd, file_contents
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return None, None
        except Exception as e:
            print(f"Error reading file '{filename}': {str(e)}")
            return None, None
    else:
        # No input redirection; return the command as is
        return command_string, None