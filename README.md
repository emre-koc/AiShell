# AI Shell

AI Shell is a Python-based interactive shell with syntax highlighting, autocompletion, and support for basic Bash commands.

## Features

- Interactive command-line interface
- Syntax highlighting using Pygments
- Autocompletion of commands
- Support for basic Bash commands (e.g., `cd`, `ls`, `pwd`, `echo`, `cat`)
- Execution of external commands using `os.system()`
- Virtual environment for isolated dependencies

## Prerequisites

- Python 3.6 or higher
- pip package manager

## One-line Installation

You can install AI Shell with a single command using curl:

```bash
curl -fsSL https://raw.githubusercontent.com/emre-koc/AiShell/main/setup.sh | bash
```

This command will:
- Download the setup script from the GitHub repository
- Execute the setup script, which will:
  - Create a virtual environment named `vaishell` in `~/.aishell`
  - Install the required dependencies in the virtual environment
  - Create an executable `aishell` script in `~/.aishell`
  - Add `~/.aishell` to the `PATH` environment variable

After running this command, restart your terminal or run `source ~/.bashrc` to apply the changes.

## Manual Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/emre-koc/AiShell.git
   ```

2. Change to the project directory:

   ```bash
   cd AiShell
   ```

3. Run the setup script:

   ```bash
   ./setup.sh
   ```

4. Restart your terminal or run `source ~/.bashrc` to apply the changes.

## Usage

To start the AI Shell, simply run the `aishell` command from anywhere in your terminal:

```bash
aishell
```

This will activate the virtual environment and launch the AI Shell.

Inside the AI Shell, you can:
- Execute basic Bash commands like `cd`, `ls`, `pwd`, `echo`, `cat`
- Run external commands, which will be executed using `os.system()`
- Use the `exit` command or press `Ctrl+D` to exit the shell

## Customization

You can customize the AI Shell by modifying the `aishell.py` file located in `~/.aishell`. This file contains the main implementation of the shell.

To add more commands or change the behavior of existing commands, update the `commands` list and the corresponding logic in the `shell()` function.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the GitHub repository.

## License

This project is licensed under the [MIT License](LICENSE).