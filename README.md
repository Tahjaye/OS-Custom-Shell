# C-Shell CLI Tool


A command-line interface tool for performing various file and directory operations across different operating systems (Windows, Linux, and macOS).

## Features

- Cross-platform support (Windows, Linux, macOS)
- File operations:
  - Create files
  - Delete files
  - Rename files
- Directory operations:
  - make directory
  - remove directory
  - change directory
- convenience operations (pwd, cat, echo)
- Command piping
- Interactive help system
- Support for multiple file extensions (.txt, .pdf, .docx)

## Installation

##### 1. Ensure you have Python 3.x installed on your system
##### 2. Clone this repository:
```bash
git clone https://github.com/Tahjaye/OS-Custom-Shell.git
cd custom-shell
```

## Usage

Run the program:
```bash
python Shell.py
```

### Available Commands

- File Operations:
   - `create <filename>`: Create a new file.
   - `delete <filename>`: Delete an existing file.
   - `rename <old_filename> <new_filename>`: Rename an existing file (prompts for new name).

- Directory Operations:
   - `make <dir_name>`: Create a new directory.
   - `remove <dir_name>`: Remove an existing directory.
   - `change <dir_name>`: Change the current working directory.

- Convenience Operations:
   - `pwd`: Print the current working directory.
   - `cat <filename>`: Display the contents of a file.
   - `echo <text>`: Display the provided text.

- General Commands:
   - `help`: Display general help information.
   - `help <command>`: Display help for a specific command.
   - `c`: Clear the screen.
   - `e`: Exit the program.

### Command Piping

The tool supports basic command piping using `<`, `>`, and `|` operators.

### Examples

```bash
>> create test.txt
>> rename test.txt
Enter new filename: newtest.txt
>> delete newtest.txt
```

## Project Structure

- `Shell.py` - Entry point and main program loop.
- `Commands.py` - Handles execution of commands.
- `input_parser.py` - Parses and validates user input.
- `.\static\constant_types.py` - Defines constants, enums, and type definitions.
- `.\static\exceptions` - Definition of custom exceptions .
- `.\static\help.json` - Stores the help details for command `General` `Specific`


## Technical Details

### Dependencies

- Python 3.x


### Key Components

##### 1. **Platform Detection**
   - Automatically detects the operating system
   - Adjusts commands based on the platform

##### 2. **Input Validation**
   - Validates file extensions
   - Checks for valid operations
   - Parses piped commands

##### 3. **Error Handling**
   - Custom exceptions for various error scenarios
   - User-friendly error messages

##### 4. **Help System**
   - General for all commands 
   - Specific help for a certain command ex:` help <create> `

## Error Handling

The tool uses custom exceptions:
- `InvalidCommand` - For invalid user inputs
- `FileOperationError` - For file-related errors
- `CommonException` - For general errors

## Limitations

- Limited to basic file operations
- Supports only .txt, .pdf, and .docx file extensions
- Basic command piping functionality

## License

[Licence](LICENSE)
