from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers.shell import BashLexer
from rich.console import Console
from rich.panel import Panel
import os
import subprocess
import getpass
import socket
import hashlib
import anthropic
import json
from var_dump import var_dump

CLAUDE_KEY_FILE = os.path.expanduser("~/.aishell/.claudekey")
console = Console()


#claude api functions

def get_claude_api_key():
    if not os.path.exists(CLAUDE_KEY_FILE):
        claude_api_key = input("Please enter your Claude API key: ")
        os.makedirs(os.path.dirname(CLAUDE_KEY_FILE), exist_ok=True)
        with open(CLAUDE_KEY_FILE, "w") as file:
            file.write(claude_api_key)
        print(f"Claude API key saved to {CLAUDE_KEY_FILE}")
    else:
        with open(CLAUDE_KEY_FILE, "r") as file:
            claude_api_key = file.read().strip()
    return claude_api_key

def send_prompt_to_claude(prompt):
    claude_api_key = get_claude_api_key()
    client = anthropic.Anthropic(
            # defaults to os.environ.get("ANTHROPIC_API_KEY")
            api_key=claude_api_key
        )
    opus_response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=100,
        system="Use JSON format with the keys. if you want to add some context add it under context key. Message should only contain text that is the exact answer for the prompt",
        temperature=0,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    var_dump(opus_response.content)
    response_text = opus_response.content[0].text
    json_data = json.loads(opus_response.content[0].text)

    #
    #print("Assistant:", response.content[0])

    # Access the parsed content
    #text = response.content[0]['text']
    #content_type = response.content[0]['type']

    #print("Response Text:", text)
    #print("Content Type:", content_type)
    return json_data



#action handlers

def identify_action(prompt):
    if "send files to git" in prompt.lower():
        return "git_commit"
    # Add more conditions for other actions
    else:
        return "none"
    

def execute_git_commit():
    # Get the changes in the git folder
    changes = subprocess.check_output(["git", "status"]).decode("utf-8")

    # Check if there are untracked files
    untracked_files = subprocess.check_output(["git", "ls-files", "--others", "--exclude-standard"]).decode("utf-8").strip()

    if untracked_files:
        console.print(Panel(f"Untracked files:\n{untracked_files}", title="[bold yellow]Untracked Files[/bold yellow]", title_align="left", border_style="yellow"))
        add_files = input("Do you want to add the untracked files? (y/n): ")
        if add_files.lower() == "y":
             # Prompt the user for files to exclude from the commit
            exclude_files = input("Enter files to exclude from the commit (separated by spaces), or press Enter to include all files: ")
            exclude_files = exclude_files.split()

            # Stage all files except the excluded ones
            if exclude_files:
                subprocess.run(["git", "add", "--all", "--"] + [f":!{file}" for file in exclude_files])
            else:
                subprocess.run(["git", "add", "--all"])
    else:
        subprocess.run(["git", "add", "--all"])
    
    changes = subprocess.check_output(["git", "status"]).decode("utf-8")

   

    # Send the changes to the Claude API for generating a commit message
    prompt = f"Please generate a commit message for the following changes:\n\n{changes}"
    commit_data = send_prompt_to_claude(prompt)

    # Ask user to confirm the commit message
    console.print(Panel(
        commit_data['message'],
        title="[bold green]AiShell[/bold green]",
        title_align="left",
        border_style="green",
        subtitle="Confirm your commit message 👇",
        expand=True
    ))

    if 'context' in commit_data:
        console.print(commit_data['context'])

    confirm = input("Do you want to commit the changes? (y/n): ")
    if confirm.lower() != "y":
        return

    # Execute the git commit command with the generated commit message
    subprocess.run(["git", "commit", "-m", commit_data['message']])


# Define the available commands and their completions
commands = ['cd', 'ls', 'pwd', 'echo', 'cat', 'exit', 'send files to git']
command_completer = WordCompleter(commands)

def get_directory_hash():
    current_dir = os.getcwd()
    dir_hash = hashlib.sha256(current_dir.encode('utf-8')).hexdigest()
    return dir_hash

def get_git_branch():
    try:
        branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode('utf-8').strip()
        return f"({branch})"
    except subprocess.CalledProcessError:
        return ""

def get_prompt():
    username = getpass.getuser()
    computer_name = socket.gethostname().split('.')[0]  # Remove '.local' from computer name
    current_dir = os.path.basename(os.getcwd())  # Get only the current folder name
    git_branch = get_git_branch()
    return f"{git_branch} {username}@{computer_name} {current_dir}> "

def shell():
    session = PromptSession(lexer=PygmentsLexer(BashLexer))
    cache_dir = os.path.expanduser('~/.aishell/cache')
    os.makedirs(cache_dir, exist_ok=True)
    console = Console()

    while True:
        try:
            prompt = get_prompt()
            dir_hash = get_directory_hash()
            history_file = os.path.join(cache_dir, f'{dir_hash}.history')

            # Load command history for the current directory
            if os.path.exists(history_file):
                with open(history_file, 'r') as f:
                    history = f.read().splitlines()
                    for item in history:
                        session.history.append_string(item)

            command = session.prompt(prompt, completer=command_completer)

            # Save command to history
            with open(history_file, 'a') as f:
                f.write(command + '\n')

            action = identify_action(command)
            if action == "git_commit":
                execute_git_commit()
            else:
                if command == 'exit':
                    break
                elif command.startswith('cd '):
                    directory = command.split(' ')[1]
                    os.chdir(directory)
                else:
                    result = subprocess.run(command, shell=True, capture_output=True, text=True)
                    if result.returncode == 0:
                        console.print(Panel(result.stdout, expand=False))
                    else:
                        console.print(Panel(result.stderr, expand=False, style="bold red"))
        except KeyboardInterrupt:
            exit()
        except EOFError:
            break

if __name__ == '__main__':
    shell()