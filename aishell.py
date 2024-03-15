from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers.shell import BashLexer
import os

# Define the available commands and their completions
commands = ['cd', 'ls', 'pwd', 'echo', 'cat', 'exit']
command_completer = WordCompleter(commands)

def shell():
    session = PromptSession(lexer=PygmentsLexer(BashLexer))
    
    while True:
        try:
            command = session.prompt('> ', completer=command_completer)
            
            if command == 'exit':
                break
            elif command.startswith('cd '):
                directory = command.split(' ')[1]
                os.chdir(directory)
            else:
                os.system(command)
        except KeyboardInterrupt:
            continue
        except EOFError:
            break

if __name__ == '__main__':
    shell()