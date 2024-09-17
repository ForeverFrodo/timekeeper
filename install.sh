#!/bin/bash

# Default locations
default_data_dir="$HOME/.timekeeper"
default_install_dir="/usr/local/bin"

# Prompt user for data directory
read -p "📜 Where should timekeeper store it's logs and config? [${default_data_dir}]: " data_dir  
data_dir=${data_dir:-$default_data_dir}

# Prompt user for install directory
read -p "⚡ Where should timekeeper place the command? [${default_install_dir}]: " install_dir
install_dir=${install_dir:-$default_install_dir}

# Create the data directory if it doesn't exist
mkdir -p "$data_dir"

# Write the data directory to the Python script
python_script="timekeeper.py"
sed -i "s|DATA_DIR = .*|DATA_DIR = '$data_dir'|" "$python_script"

# Change permissions of the Python script
chmod +x "$python_script"

# Copy the Python script to the install directory
cp "$python_script" "$install_dir/timekeeper"

# Print completion message
echo "✅ Installation complete. Look for your log files in $data_dir as you use Timekeeper."