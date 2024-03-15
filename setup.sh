#!/bin/bash

# Set the GitHub repository URL
repo_url="https://raw.githubusercontent.com/emre-koc/AiShell/main"

# Set the destination directory
dest_dir="$HOME/.aishell"

# Store the current directory
original_dir=$(pwd)

# Create the ~/.aishell directory if it doesn't exist
if [ ! -d "$dest_dir" ]; then
    mkdir "$dest_dir"
fi


# Download the aishell.py file
curl -fsSL "$repo_url/aishell.py" -o "$dest_dir/aishell.py"

# Change to the ~/.aishell directory
cd "$HOME/.aishell"

# Create the virtual environment if it doesn't exist
if [ ! -d "vaishell" ]; then
    python3 -m venv vaishell
fi


# Copy the aishell.py file to the ~/.aishell directory
cp aishell.py "$HOME/.aishell/"

# Create the shell script to activate the virtual environment and start the shell
cat > "$HOME/.aishell/aishell" << EOL
#!/bin/bash

# Activate the virtual environment
source "$HOME/.aishell/vaishell/bin/activate"

# Start the AI shell
python "$HOME/.aishell/aishell.py"
EOL

# Make the shell script executable
chmod +x "$HOME/.aishell/aishell"

# Add the ~/.aishell directory to the PATH
echo 'export PATH=$PATH:$HOME/.aishell' >> ~/.bashrc
source ~/.bashrc


# Change back to the original directory
cd "$original_dir"
