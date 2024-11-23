import subprocess
import shlex
from typing import Optional, List, Tuple
from dataclasses import dataclass
import os
import sys


@dataclass
class ParsedCommand:
    """Represents a parsed Windows command with its redirections"""

    command: List[str]
    input_file: Optional[str] = None
    output_file: Optional[str] = None
    append_output: bool = False


class CommandExecutor:
    """Handles Windows command execution with pipes and redirections"""

    def __init__(self, command_string: str):
        self.original_command = command_string.strip()
        self.commands: List[ParsedCommand] = []
        self._file_handles = []

        # Windows-specific shell commands that need cmd.exe
        self.CMD_COMMANDS = {
            "dir",
            "type",
            "copy",
            "move",
            "del",
            "rd",
            "md",
            "echo",
            "set",
            "where",
            "findstr",
        }

    def _needs_shell(self, command: str) -> bool:
        """Check if command needs to be run through cmd.exe"""
        return command.lower() in self.CMD_COMMANDS

    def _tokenize(self) -> List[str]:
        """Tokenize command string preserving Windows-style quotes"""
        try:
            if '"' in self.original_command:
                # Handle Windows-style quoted paths
                tokens = []
                current_token = []
                in_quotes = False

                for char in self.original_command:
                    if char == '"':
                        in_quotes = not in_quotes
                        current_token.append(char)
                    elif char.isspace() and not in_quotes:
                        if current_token:
                            tokens.append("".join(current_token))
                            current_token = []
                    else:
                        current_token.append(char)

                if current_token:
                    tokens.append("".join(current_token))
                return tokens
            else:
                return shlex.split(self.original_command)
        except ValueError as e:
            raise ValueError(f"Invalid command syntax: {str(e)}")

    def parse(self) -> None:
        """Parse the command string into WindowsCommand objects"""
        if not self.original_command:
            return

        tokens = self._tokenize()
        if not tokens:
            return

        current_command: List[str] = []
        current_input: Optional[str] = None
        current_output: Optional[str] = None
        append_output: bool = False
        i = 0

        while i < len(tokens):
            token = tokens[i]

            if token == "|":
                if not current_command:
                    raise ValueError("Empty command before pipe")
                if i == len(tokens) - 1:
                    raise ValueError("Missing command after pipe")

                self.commands.append(
                    ParsedCommand(
                        command=current_command,
                        input_file=current_input,
                        output_file=current_output,
                        append_output=append_output,
                    )
                )
                current_command = []
                current_input = None
                current_output = None
                append_output = False

            elif token == "<":
                if i == len(tokens) - 1:
                    raise ValueError("Missing input file after <")
                current_input = tokens[i + 1].strip('"')
                i += 1

            elif token == ">":
                if i == len(tokens) - 1:
                    raise ValueError("Missing output file after >")
                current_output = tokens[i + 1].strip('"')
                append_output = False
                i += 1

            elif token == ">>":
                if i == len(tokens) - 1:
                    raise ValueError("Missing output file after >>")
                current_output = tokens[i + 1].strip('"')
                append_output = True
                i += 1

            else:
                current_command.append(token)

            i += 1

        if current_command:
            self.commands.append(
                ParsedCommand(
                    command=current_command,
                    input_file=current_input,
                    output_file=current_output,
                    append_output=append_output,
                )
            )

    def _create_process(self, cmd: ParsedCommand, stdin, stdout) -> subprocess.Popen:
        """Create a Windows process with appropriate shell handling"""
        command_str = cmd.command[0]
        if self._needs_shell(command_str):
            # Use cmd.exe for built-in Windows commands
            full_cmd = ["cmd", "/c"] + cmd.command
            return subprocess.Popen(
                full_cmd,
                stdin=stdin,
                stdout=stdout,
                stderr=subprocess.PIPE,
                text=True,
                shell=False,  # We're explicitly using cmd.exe
            )
        else:
            # For regular executables
            return subprocess.Popen(
                cmd.command,
                stdin=stdin,
                stdout=stdout,
                stderr=subprocess.PIPE,
                text=True,
                shell=False,
            )

    def execute(self) -> None:
        """Execute the Windows commands with piping and redirections"""
        try:
            self.parse()
            if not self.commands:
                return

            processes = []
            prev_process = None

            for i, cmd in enumerate(self.commands):
                is_last = i == len(self.commands) - 1

                # Handle input redirection
                if i == 0 and cmd.input_file:
                    stdin_file = open(cmd.input_file, "r")
                    self._file_handles.append(stdin_file)
                    stdin = stdin_file
                else:
                    stdin = prev_process.stdout if prev_process else None

                # Handle output redirection
                if is_last and cmd.output_file:
                    mode = "a" if cmd.append_output else "w"
                    stdout_file = open(cmd.output_file, mode)
                    self._file_handles.append(stdout_file)
                    stdout = stdout_file
                else:
                    stdout = subprocess.PIPE if not is_last else sys.stdout

                try:
                    process = self._create_process(cmd, stdin, stdout)
                    processes.append(process)

                    # Do not close prev_process.stdout here
                    prev_process = process

                except FileNotFoundError:
                    raise RuntimeError(f"Command not found: {cmd.command[0]}")

            # Wait for all processes to complete
            for process in processes:
                stdout, stderr = process.communicate()
                if process.returncode != 0 and stderr:
                    print(f"Error: {stderr.strip()}", file=sys.stderr)

        except Exception as e:
            print(f"Error: {str(e)}", file=sys.stderr)

        finally:
            self.cleanup()

    def cleanup(self) -> None:
        """Clean up Windows file handles"""
        for handle in self._file_handles:
            try:
                handle.close()
            except Exception:
                pass
        self._file_handles.clear()
