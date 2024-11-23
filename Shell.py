import shlex
import Commands as cd
from piping_redirect import CommandExecutor

ECHO = True
OS_PLATFORM = cd.get_platform()
CURRENT_DIRECTORY = cd.get_working_directory()

VALID_PERMISSIONS = {"+r", "-r", "+w", "-w", "+x", "-x"}


def handle_file_permissions(args):
    if args[0] not in VALID_PERMISSIONS:
        print("Invalid permissions. Permissions must be one of +r, -r, +w, -w, +x, -x.")
        return False
    permissions_map = {
        "+r": (True, False),
        "-r": (False, False),
        "+w": (False, False),
        "-w": (True, False),
        "+x": (False, True),
        "-x": (False, False),
    }
    read_only, executable = permissions_map.get(args[0], (None, None))
    cd.change_file_permissions(args[1], read_only, executable)  # type: ignore
    return True


def execute_command(command):
    tokens = shlex.split(command)
    if not tokens:
        return

    if any(token in ["<", ">", ">>", "|"] for token in tokens):
        check_redirect = CommandExecutor(command)
        check_redirect.execute()
        return

    cmd, *args = tokens
    cmd = cmd.lower()

    commands = {
        "create": cd.create_file,
        "touch": cd.create_file,
        "exit": lambda: (print("Exiting shell."), exit(0)),
        "cat": cd.cat_file,
        "echo": cd.echo,
        "clear": cd.clear_screen,
        "current": cd.current_working_directory,
        "pwd": cd.current_working_directory,
        "help": lambda: cd.print_help(args[0] if args else None),
        "delete": cd.delete_file,
        "rm": cd.delete_file,
        "rename": cd.rename_file,
        "mv": cd.rename_file,
        "make": cd.make_directory,
        "mkdir": cd.make_directory,
        "remove": cd.remove_directory,
        "rmdir": cd.remove_directory,
        "change": cd.current_working_directory,
        "cd": cd.change_directory,
        "modify": lambda: handle_file_permissions(args),
        "chmod": lambda: handle_file_permissions(args),
        "list": lambda: cd.list_permissions() if args == ["-l"] else None,
        "set": cd.set_env_var,
        "get": cd.get_env_var,
        "ls": cd.list_sub_directories,
        "dir": cd.list_sub_directories,
    }

    if cmd in commands:
        # Check if the command should be executed with no arguments
        if cmd in {"clear", "exit", "help"}:
            if len(args) == 0:
                commands[cmd]()
            else:
                print(f"Invalid arguments for {cmd}.")
        elif cmd in {"modify", "chmod", "set", "get"}:
            if len(args) == 1 or len(args) == 0:
                commands[cmd]()
            else:
                print("Invalid number of arguments.")
        else:
            if len(args) == 1 or len(args) == 2:
                commands[cmd](*args)
            else:
                print(f"Invalid arguments for {cmd}.")
    else:
        print(f"Unrecognized command: {command}, command or argument/s are incorrect.")
        print("Type 'help' for available commands.")


def shell():
    print("Welcome to the shell! Type 'help' for available commands or 'exit' to quit.")
    while True:
        CURRENT_DIRECTORY = cd.get_working_directory()
        command = input(f"{CURRENT_DIRECTORY}>> ") if ECHO else input()

        execute_command(command)


if __name__ == "__main__":
    shell()
