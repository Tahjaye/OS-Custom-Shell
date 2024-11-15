import subprocess

class DirectoryOperations:
    CREATE = "create"
    DELETE = "delete"
    RENAME = "rename"
    CHANGE = "cd"
    LIST = "dir"  # Windows equivalent of 'ls'
    MAKE = "mkdir"
    REMOVE = "rmdir"
    CURRENT = "cd"  # Windows equivalent of 'pwd'
    MOVE = "move"  # Windows equivalent of 'mv'

    def run_command(self, command):
        """Runs a shell command using subprocess and handles output."""
        try:
            result = subprocess.run(command, capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                print(result.stdout)
            else:
                print(f"Error: {result.stderr}")
        except Exception as e:
            print(f"Command execution failed: {e}")

    def create_directory(self, dir_name):
        self.run_command(f"mkdir {dir_name}")

    def delete_directory(self, dir_name):
        self.run_command(f"rmdir {dir_name}")

    def rename_directory(self, old_name, new_name):
        self.run_command(f"ren {old_name} {new_name}")  # 'ren' is the Windows equivalent of 'mv' for renaming

    def change_directory(self, dir_name):
        # Note: Changing directories with subprocess won't affect the parent Python process' directory.
        self.run_command(f"cd {dir_name} && {self.CURRENT}")

    def list_directory(self):
        self.run_command(self.LIST)

    def current_directory(self):
        self.run_command(self.CURRENT)

    def move_item(self, source, destination):
        self.run_command(f"move {source} {destination}")

# Main script to accept user input and execute commands
ops = DirectoryOperations()

while True:
    command = input("Enter your command: ")
    print(f"\nYour command is: {command}")

    # Split the input into command and arguments
    arguments = command.split()

    # Check the command and execute the corresponding function
    if not arguments:
        print("No command entered. Please try again.")
        continue

    cmd = arguments[0].lower()
    if cmd == ops.CREATE and len(arguments) == 2:
        ops.create_directory(arguments[1])
    elif cmd == ops.DELETE and len(arguments) == 2:
        ops.delete_directory(arguments[1])
    elif cmd == ops.RENAME and len(arguments) == 3:
        ops.rename_directory(arguments[1], arguments[2])
    elif cmd == ops.CHANGE and len(arguments) == 2:
        ops.change_directory(arguments[1])
    elif cmd == ops.LIST:
        ops.list_directory()
    elif cmd == ops.CURRENT:
        ops.current_directory()
    elif cmd == ops.MOVE and len(arguments) == 3:
        ops.move_item(arguments[1], arguments[2])
    else:
        print("Invalid command or incorrect number of arguments.")
