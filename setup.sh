#!/bin/bash

 # Set the GitHub repository URL
repo_url="https://raw.githubusercontent.com/emre-koc/AiShell/main"

# Store the current directory
original_dir=$(pwd)

# Set the destination directory
dest_dir="$HOME/.aishell"
#if user passes -f flag, the skip the check and install
if [ "$1" != "-f" ]; then
    # Check if the destination directory exists
    if [ -d "$dest_dir" ]; then
        # Check if the .installed file exists
        if [ -f "$dest_dir/.installed" ]; then
            echo "AI shell is already installed. Use the -f flag to force reinstallation."
            exit 1
        fi
    fi
fi

# Check if Python 3 is installed
if ! [ -x "$(command -v python3)" ]; then
    echo "Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# Create the destination directory if it doesn't exist
mkdir -p "$dest_dir"

# Check if aishell.py is present in the current directory
if [ -f "aishell.py" ]; then
    echo "aishell.py found in the current directory. Performing local install."
    cp "aishell.py" "$dest_dir/"
    cp "requirements.txt" "$dest_dir/"
else
    echo "Downloading aishell.py and requirements.txt from GitHub."
   
    # Download the aishell.py file
    curl -fsSL "$repo_url/aishell.py" -o "$dest_dir/aishell.py"
    # Download the requirements.txt file
    curl -fsSL "$repo_url/requirements.txt" -o "$dest_dir/requirements.txt"
fi


# Change to the destination directory
cd "$dest_dir"

# Create the virtual environment if it doesn't exist
if [ ! -d "vaishell" ]; then
    python3 -m venv vaishell
fi

# Activate the virtual environment
source "$dest_dir/vaishell/bin/activate"

# Install the dependencies from requirements.txt
pip install -r "$dest_dir/requirements.txt"

# Create the shell script to activate the virtual environment and start the shell
cat > "$dest_dir/aishell" << EOL
#!/bin/bash

# Activate the virtual environment
source "$dest_dir/vaishell/bin/activate"

# Start the AI shell
python "$dest_dir/aishell.py"
EOL

# Make the shell script executable
chmod +x "$dest_dir/aishell"

# Check the user's shell and add the appropriate configuration
if [[ "$SHELL" == *"/zsh"* ]]; then
    if ! grep -q "aishell" ~/.zshrc; then
        echo "export PATH=\"\$PATH:$dest_dir\"" >> ~/.zshrc
        echo "Added aishell to ~/.zshrc"
    else
        echo "aishell already exists in ~/.zshrc"
    fi
    source ~/.zshrc
elif [[ "$SHELL" == *"/bash"* ]]; then
    if ! grep -q "aishell" ~/.bashrc; then
        echo "export PATH=\"\$PATH:$dest_dir\"" >> ~/.bashrc
        echo "Added aishell to ~/.bashrc"
    else
        echo "aishell already exists in ~/.bashrc"
    fi
    source ~/.bashrc
else
    echo "Unsupported shell. Please add $dest_dir to your PATH manually."
fi

echo "Setup complete. You can now run 'aishell' to start your AI shell in the virtual environment."

touch "$dest_dir/.installed"

# Change back to the original directory
cd "$original_dir"