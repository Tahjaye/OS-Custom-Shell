import Commands as cd
import os
import subprocess
import shlex

ECHO = True
OS_PLATFORM= cd.get_platform()
CURRENT_DIRECTORY = cd.get_current_directory()

def execute_command(command):
    tokens = shlex.split(command)

    if not tokens:
        return

    cmd, *args = tokens # unpacks the first element of the list into cmd and the rest into args
    cmd = cmd.lower()# makes the shell case-insensitive
    if (cmd == "create" or cmd=="touch") and len(args) == 1:
        cd.create_file(args[0])
    elif cmd == "exit":
        print("Exiting shell.")
        exit(0)
    elif cmd == "cat" and len(args) == 1:
        cd.cat_file(args[0])
    elif cmd == "echo":
        cd.echo(*args)
    elif cmd == "clear":
        cd.clear_screen()
    elif (cmd =="current" or cmd == "pwd")and len(args) == 0:
        cd.current_working_directory()
    elif cmd == "help" and len(args) <= 1:
        if len(args) == 1:
            cd.print_help(args[0])
        elif len(args) == 0:
            cd.print_help()
    elif (cmd == "delete" or cmd == "rm") and len(args) == 1:
        cd.delete_file(args[0])
    elif (cmd == "rename"or cmd=="mv") and len(args) == 2:
        cd.rename_file(args[0], args[1])
    elif (cmd == "make" or cmd =="mkdir") and len(args) == 1:
        cd.make_directory(args[0])
    elif (cmd == "remove" or cmd == "rmdir") and len(args) == 1:
        cd.remove_directory(args[0])
    elif (cmd == "change" or cmd =="cd") and len(args) <= 1:
        if len(args) == 0:
            cd.current_working_directory()
        elif len(args) == 1:
            cd.change_directory(args[0])
    elif (cmd == "modify" or cmd == "chmod") and len(args) == 2:
        if args[0] not in ["+r", "-r", "+w", "-w", "+x", "-x"]:
            print("Invalid permissions. Permissions must be one of +r, -r, +w, -w, +x, -x.")
            return
        else:
            match(args[0]):
                case "+r":
                    cd.change_file_permissions(args[1], read_only=True, executable=False)
                case "-r":
                    cd.change_file_permissions(args[1], read_only=False, executable=False)
                case "+w":
                    cd.change_file_permissions(args[1], read_only=False, executable=False)
                case "-w":
                    cd.change_file_permissions(args[1], read_only=True, executable=False)
                case "+x":
                    cd.change_file_permissions(args[1], read_only=False, executable=True)
                case "-x":
                    cd.change_file_permissions(args[1], read_only=False, executable=False)
    elif cmd == "list" and len(args)==1 and args[0] == ["-l"]:
        cd.list_permissions()
    elif cmd == "set" and len(args) == 2:
        cd.set_env_var(args[0], args[1])
    elif cmd == "get" and len(args) == 1:
        cd.get_env_var(args[0])
    elif (cmd == "ls" or cmd =="dir") and len(args) == 0:
        cd.list_sub_directories()
    else:
        print(f"Unrecognized command: {command}, command or argument/s are incorrect.")
        print("Type 'help' for available commands.")
        

def process_io_redirection(command) -> str:
    """
    Processes a command with `<` for input redirection and replaces the file path
    with the file's contents in place.

    Args:
        command (str): The command string, e.g., "echo < test.txt".

    Returns:
        str: The command with the file contents replacing the file path.
        eg. echo "Hello, World!"
    """
    try:
        # Check if the command contains the input redirection operator
        if '<' in command:
            # Split the command by '<' to get the base command and the file path
            base_command, file_path = command.split('<', 1)

            # Strip any leading/trailing whitespace around the parts
            base_command = base_command.strip()
            file_path = file_path.strip()

            # Read the contents of the file
            with open(file_path, 'r') as file:
                file_contents = file.read().strip()

            # Return the reconstructed command with the file contents
            return f"{base_command} {file_contents}"
        else:
            return command  # No redirection to process

    except FileNotFoundError:
        return f"Error: File '{file_path}' not found."
    except PermissionError:
        return f"Error: Permission denied for file '{file_path}'."
    except Exception as e:
        return f"Error processing command: {e}"

def shell():
    
    print("Welcome to the shell! Type 'help' for available commands or 'exit' to quit.")
    while True:
        CURRENT_DIRECTORY = cd.get_current_directory()
        if ECHO:
            command = input(f"{CURRENT_DIRECTORY}>> ")
        else:
            command = input()
        execute_command(command)

if __name__ == "__main__":
    shell()